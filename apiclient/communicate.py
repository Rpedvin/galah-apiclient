import pickle
import os
import getpass
import sys

import config
import utils

import logging
logger = logging.getLogger("apiclient.communicate")

requests = utils.requests_module()

class BadLogin(RuntimeError):
    def __init__(self, *args, **kwargs):
        RuntimeError.__init__(self, *args, **kwargs)

class APIClientSession:
    """
    Represents an authenticated API client session.

    .. note::

        Do not confuse with a requests session object.

    """

    def __init__(self, requests_session = None, user = None):
        self.user = user
        self.requests_session = requests_session

    def save(self):
        file_path = config.CONFIG["session-path"]

        try:
            with open(file_path, "w") as f:
                os.chmod(file_path, 0o600)
                pickle.dump(self, f)
        except IOError:
            logger.warn("Could not save session to %s." % (file_path, ))
            raise

    def load(self):
        file_path = config.CONFIG["session-path"]

        if not os.path.isfile(file_path):
            logger.debug("No session file found at %s.", file_path)
            return

        try:
            with open(file_path, "r") as f:
                return pickle.load(f)
        except IOError:
            logger.warn("Could not load session from %s." % (file_path, ))
            raise

    def login(self, email, password):
        """
        Attempts to authenticate with Galah using the credentials provided
        through various sources.

        """

        session = requests.session()

        request = session.post(
            config.CONFIG["host"] + "/api/login",
            data = {"email": email, "password": password}
        )

        request.raise_for_status()

        # Check if we successfully logged in.
        if request.headers["X-CallSuccess"] != "True":
            raise BadLogin(request.text)

        self.user = email
        self.requests_session = session

def determine_credentials():
    """
    Determines the username and password the user wants to log in with.

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
