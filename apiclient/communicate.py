import pprint
import pickle
import os
import os.path
import sys
import function

import config
import utils

import logging
logger = logging.getLogger("apiclient.communicate")

requests = utils.requests_module()

def _form_call(api_name, *args, **kwargs):
    """
    Transforms an API Call into a dict suitable to send to Galah.

    """

    return dict([("api_name", api_name), ("args", args)] + kwargs.items())

def _parse_api_info(api_info):
    result = {}
    for command in api_info:
        result[command["name"]] = function.Function(
            name = command["name"],
            params = [
                function.Function.Parameter(
                    name = i["name"],
                    default_value = i.get("default_value"),
                    param_type = str
                ) for i in command.get("args", [])
            ]
        )

    return result

class APIClientSession:
    """
    Represents an authenticated API client session.

    .. note::

        Do not confuse with a requests session object.

    """

    def __init__(self, requests_session = None, user = None,
            api_info_raw = None, api_info = None):
        self.user = user
        self.requests_session = requests_session
        self.api_info_raw = api_info_raw
        self.api_info = api_info

    def save(self):
        session_file_path = config.CONFIG["session-path"]

        if self.user:
            logger.info("Saving session to %s.", session_file_path)

            try:
                if utils.prepare_directory(session_file_path):
                    logger.info(
                        "Created directory(s) %s.",
                        os.path.dirname(session_file_path)
                    )

                with open(session_file_path, "w") as f:
                    os.chmod(session_file_path, 0o600)
                    pickle.dump((self.user, self.requests_session), f)
            except IOError:
                logger.warn(
                    "Could not save session to %s.",
                    session_file_path,
                    exc_info = sys.exc_info()
                )

        api_info_file_path = config.CONFIG["api-info-path"]

        if self.api_info_raw:
            logger.info("Saving API info to %s.", api_info_file_path)

            try:
                if utils.prepare_directory(api_info_file_path):
                    logger.info(
                        "Created directory(s) %s.",
                        os.path.dirname(api_info_file_path)
                    )

                with open(api_info_file_path, "wb") as f:
                    f.write(self.api_info_raw)
            except IOError:
                logger.warn(
                    "Could not save API Info to %s.",
                    api_info_file_path,
                    exc_info = sys.exc_info()
                )

    def load(self):
        session_file_path = config.CONFIG["session-path"]

        if os.path.isfile(session_file_path):
            logger.info("Loading session file from %s.", session_file_path)

            try:
                with open(session_file_path, "r") as f:
                    self.user, self.requests_session = pickle.load(f)
            except IOError:
                logger.critical("Could not load session from %s." % (session_file_path, ))
                sys.exit(1)
        else:
            logger.debug("No session file found at %s.", session_file_path)

        api_info_file_path = config.CONFIG["api-info-path"]

        if os.path.isfile(api_info_file_path):
            logger.info("Loading API Info from %s.", api_info_file_path)

            try:
                with open(api_info_file_path, "rb") as f:
                    self.api_info_raw = f.read().encode("ascii")
                    self.api_info = _parse_api_info(
                        utils.json_module().loads(self.api_info_raw)
                    )

                    logger.debug(
                        "Loaded API info...\n%s",
                        "\n".join(str(i) for i in self.api_info.values())
                    )
            except IOError:
                logger.warn(
                    "Could not load API Info from %s.",
                    api_info_file_path,
                    exc_info = sys.exc_info()
                )

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

    def fetch_api_info(self):
        try:
            r = requests.post(
                config.CONFIG["host"] + "/api/call",
                data = utils.json_module().dumps(_form_call("get_api_info")),
                headers = {"Content-Type": "application/json"},
                verify = not config.CONFIG.get("no-verify-certificate", False)
            )
        except requests.exceptions.ConnectionError as e:
            logger.critical(
                "Galah did not respond at %s.",
                config.CONFIG["host"] + "/api/call",
                exc_info = sys.exc_info()
            )
            sys.exit(1)

        if r is None or r.status_code != requests.codes.ok:
            logger.critical("Could not get API info from Galah.")
            sys.exit(1)

        self.api_info_raw = r.text.encode("ascii")
        self.api_info = _parse_api_info(r.json())

        logger.debug(
            "Loaded API info...\n%s",
            "\n".join(str(i) for i in self.api_info.values())
        )

