import utils
import sys

CONFIG = None

# The default configuration settings
DEFAULT_CONFIG = {
    "galah_host": "http://localhost:5000",
    "use_oauth": False,
    "verify_certificate": True
}

#: The places the API client will always look for a configuration file, in order
#: of priority (the first configuration file found is used).
DEFAULT_CONFIG_PATHS = [
    "~/.config/galah/api_config.json",
    "/etc/galah/api_config.json",
    "./api_config.json",

    # Deprecated configuration file locations below
    "~/.galah/config/api_client.config",
    "/etc/galah/api_client.config",
    "./api_client.config"
]

import logging
logger = logging.getLogger("apiclient.config")

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

    # Figure out all of the places we should look for a configuration file.
    possible_config_paths = _generate_search_paths(user_supplied)

    # Ensure any ., .., and ~ symbols are correctly handled.
    possible_config_paths = utils.resolve_paths(possible_config_paths)

    logger.debug(
        "Searching through %s for configuration file.",
        str(possible_config_paths)
    )

    for i in possible_config_paths:
        if os.path.isfile(i):
            try:
                return dict(
                    DEFAULT_CONFIG.items() + utils.load_json(open(i)).items()
                )
            except IOError:
                logger.critical(
                    "Could not open configuration file at %s.",
                    i,
                    exc_info = sys.exc_info()
                )
                raise
            except ValueError:
                logger.critical(
                    "Could not parse configuration file at %s.",
                    i,
                    exc_info = sys.exc_info()
                )
                raise

    return DEFAULT_CONFIG
