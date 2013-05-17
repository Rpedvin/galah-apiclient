import utils
import sys
import os
import pprint
import logcontrol

import logging
logger = logging.getLogger("apiclient.config")

#: A dictionary with the configuration values in it.
CONFIG = None

#: The arguments the user passed in on the command line.
ARGS = None

class Path(str):
    pass

class ConfigOption:
    def __init__(self, name, default_value = None, required = False,
            description = None, data_type = None):
        self.name = name
        self.default_value = default_value
        self.required = required
        self.description = description

        if data_type is None and self.default_value is not None:
            self.data_type = type(self.default_value)
        elif data_type is None:
            self.data_type = str
        else:
            self.data_type = data_type

# The configuration options that are known
__option_list = [
    ConfigOption(
        "use-oauth", default_value = False,
        description =
            "If set, authentication will be done via OAuth rather than "
            "internal auth over HTTP(S)."
    ),
    ConfigOption(
        "no-verify-certificate", default_value = False,
        description =
            "If set, when connecting over HTTPS, the certificate presented by "
            "the server will not be authenticated with a known certificate "
            "authority."
    ),
    ConfigOption(
        "user",
        description = "The user we will try to authenticate as."
    ),
    ConfigOption(
        "host", required = True,
        description =
            "The URL where a running Galah instance is available. For example: "
            "'https://www.mygalahinstance.edu'."
    ),
    ConfigOption(
        "session-path", default_value = "~/.cache/galah/session",
        data_type = Path,
        description =
            "The location of the session file. This stores any cookies Galah "
            "has given you. Anyone who gains access to your session file can "
            "impersonate you, so be careful. If any directories are missing "
            "from the path they will be created."
    ),
    ConfigOption(
        "api-info-path", default_value = "~/.cache/galah/api-info",
        data_type = Path,
        description =
            "The location of the API info cache. This contains information on "
            "all of the commands the server supports and is automatically "
            "updated by the API client."
    ),
    ConfigOption(
        "downloads-directory", default_value = "~/Downloads/",
        data_type = Path,
        description =
            "The directory to place downloads from the server into. It will "
            "not be created if it does not exist."
    ),
    ConfigOption(
        "verbosity", default_value = "INFO",
        description =
            "The desired logging level. Choices are %s." %
                (", ".join(logcontrol.LOG_LEVELS), )
    )
]
KNOWN_OPTIONS = dict((i.name, i) for i in __option_list)

#: The places the API client will look for a configuration file, in order of
#: priority (the first configuration file found is used).
DEFAULT_CONFIG_PATHS = [
    "~/.config/galah/api.yml",
    "/etc/galah/api.yml"
]

def generate_search_path(user_supplied):
    """
    Generates a list of paths to search through for the configuraiton file.

    :params user_supplied: A path to a configuration file that the user supplied
            on the command line. A list with only this in it wil be returned if
            this argument is not ``None``.

    :returns: A list of paths.

    .. warning::

        The returned list does not necessarily contain only absolute paths,
        therefore you should call :func:`utils.resolve_paths` on the returned
        list if you want absolute paths.

    """

    # If the user supplied a file path, only use that path.
    if user_supplied:
        return [user_supplied]

    # If the user gave us a path list, make sure to prepend that to the default
    # paths
    if "GALAH_CONFIG_PATH" in os.environ:
        return os.environ["GALAH_CONFIG_PATH"].split(":") + DEFAULT_CONFIG_PATHS

    return DEFAULT_CONFIG_PATHS

def parse_arguments(args = sys.argv[1:]):
    from optparse import OptionParser, make_option

    option_list = [
        make_option(
            "--config", "-c", metavar = "FILE",
            help =
                "The configuration file to use. An error will occur if the "
                "file is not a valid configuration file."
        ),
        make_option(
            "--logout", action = "store_true",
            help =
                "If set, the script will log you out and then exit "
                "immediately. Logging you out means removing the session file."
        ),
        make_option(
            "--clear-api-info", action = "store_true", dest="clear-api-info",
            help =
                "If set, the script will clear the API Info cache and then "
                "exit immediately"
        ),
    ]

    # Go through the configuration options and map them to command line options
    for i in KNOWN_OPTIONS.values():
        if i.data_type is bool:
            action = "store_false" if i.default_value == True else "store_true"
        else:
            action = "store"

        required_string = ""
        if i.required:
            required_string = (
                " A value must be present for this option either as a command-"
                "line argument or within the configuration file."
            )

        default_string = ""
        if i.default_value is not None:
            default_string = " [Default: %s]" % (str(i.default_value), )

        option_list.append(make_option(
            "--" + i.name, action = action, dest = i.name,
            help = i.description + required_string + default_string
        ))

    parser = OptionParser(
        description = "Command line interface to Galah for use by instructors "
                      "and administrators.",
        option_list = option_list
    )

    options, args = parser.parse_args(args)

    return (options, args)

def load_config(user_supplied = None):
    """
    Searches through the proper list of paths to find the configuration file and
    returns a single file.

    :param user_supplied: Passed directly to :func:`generate_search_path`.

    :returns: A ``dict``.

    .. seealso::
        :func:`generate_search_path` is used to figure out where to look for the
                configuration file.

    """

    global ARGS
    options, ARGS = parse_arguments()
    options = dict(i for i in options.__dict__.items() if i[1] is not None)

    if "verbosity" in options:
        logcontrol.set_level(options["verbosity"])

    logger.debug(
        "Command line options passed in...\n%s",
        pprint.pformat(options)
    )
    logger.debug(
        "Command line arguments passed in...\n%s",
        pprint.pformat(ARGS)
    )

    # Try and find a configuration file
    config_file_path = None
    if options.get("config") is not None:
        config_file_path = options["config"]
    else:
        # Figure out all of the places we should look for a configuration file.
        possible_config_paths = generate_search_path(user_supplied)

        # Ensure any ., .., and ~ symbols are correctly handled.
        possible_config_paths = utils.resolve_paths(possible_config_paths)

        logger.debug(
            "Searching for configuration file in...\n%s",
            pprint.pformat(possible_config_paths, width = 72)
        )

        for i in possible_config_paths:
            if os.path.isfile(i):
                config_file_path = i
                break

    configuration = {}
    if config_file_path is not None:
        logger.info("Loading configuration file at %s.", config_file_path)

        try:
            f = open(config_file_path)
        except IOError:
            logger.critical(
                "Could not open configuration file at %s.",
                config_file_path,
                exc_info = sys.exc_info()
            )
            raise

        try:
            configuration = utils.load_yaml(f)

            if not isinstance(configuration, dict):
                logger.critical(
                    "Your configuration file is not properly formatted. "
                    "The top level item must be a dictionary."
                )
                sys.exit(1)
        except ValueError:
            logger.critical(
                "Could not parse configuration file at %s.",
                config_file_path,
                exc_info = sys.exc_info()
            )
            raise
        finally:
            f.close()

    # Make a dictionary with the default values in it
    default_configuration = dict(
        (i.name, i.default_value) for i in KNOWN_OPTIONS.values()
                if i.default_value
    )

    # Join the various dictionaries we have together. Priority is bottom-to-top.
    final_config = dict(
        default_configuration.items() +
        configuration.items() +
        options.items()
    )

    for i in (j.name for j in KNOWN_OPTIONS.values() if j.required):
        if i not in final_config:
            logger.critical(
                "Required value %s is unspecified. This value needs to be "
                "set in either the configuration file or on the command line.",
                i
            )
            sys.exit(1)

    # Go through and resolve any paths
    for i in (j.name for j in KNOWN_OPTIONS.values()
            if j.data_type is Path):
        if i in final_config:
            final_config[i] = utils.resolve_path(final_config[i])

    return final_config
