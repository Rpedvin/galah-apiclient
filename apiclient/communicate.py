import pickle
import os
import sys

import config
import utils

import logging
logger = logging.getLogger("apiclient.communicate")

requests = utils.requests_module()

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
            logger.critical("Could not save session to %s." % (file_path, ))
            sys.exit(1)

    def load(self):
        file_path = config.CONFIG["session-path"]

        if not os.path.isfile(file_path):
            logger.debug("No session file found at %s.", file_path)
            return

        try:
            with open(file_path, "r") as f:
                return pickle.load(f)
        except IOError:
            logger.critical("Could not load session from %s." % (file_path, ))
            sys.exit(1)

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
            logger.critical("Could not log in with given credientials.")
            sys.exit(1)

        self.user = email
        self.requests_session = session
