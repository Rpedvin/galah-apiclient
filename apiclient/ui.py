import sys
import getpass
import re
import pprint
import config

import logging
logger = logging.getLogger("apiclient.user")

KEY_VALUE_RE = re.compile(r"(?P<name>[a-z_]+)(?!\\)=(?P<value>.*)")
def parse_raw_args(args):
    """
    Parses the command the user gave on the command line.

    :param args: The arguments the user provided (as provided by
            :data:`apiclient.config.ARGS`).
    :returns: A tuple ``(args, kwargs)``.

    """


    keyword_arguments = {}
    positional_arguments = []

    keyword_mode = False
    for i in args[:]:
        match = KEY_VALUE_RE.match(i)
        if not match and keyword_mode:
            logger.critical(
                "Positional argument with value '%s' specified on the command "
                "line after a keyword argument has been specified.",
                i
            )
            sys.exit(1)
        elif match and not keyword_mode:
            keyword_mode = True

        if match:
            keyword_arguments[match.group("name")] = match.group("value")
        else:
            positional_arguments.append(i)

    logger.debug(
        "Found keyword arguments...\n%s",
        pprint.pformat(keyword_arguments)
    )
    logger.debug(
        "Found positional_arguments...\n%s",
        pprint.pformat(positional_arguments)
    )

    return (positional_arguments, keyword_arguments)

def determine_credentials():
    """
    Determines the username and password the user wants to log in with.

    This is done by checking the configuration and environmental variables for
    the needed values, and prompting the user when they are unavailable.

    """

    if "user" in config.CONFIG:
        user = config.CONFIG["user"]
    else:
        user = raw_input("What user would you like to log in as?: ")
        if not user:
            logger.critical("No user name was specified.")
            sys.exit(1)

    if "GALAH_PASSWORD" in os.environ:
        logger.info(
            "Using password from GALAH_PASSWORD environmental variable."
        )
        password = os.environ["GALAH_PASSWORD"]
    else:
        password = \
            getpass.getpass("Please enter password for user %s: " % (user, ))

    return (user, password)
