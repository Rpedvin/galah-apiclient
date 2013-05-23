# Copyright (c) 2013 Galah Group LLC
# Copyright (c) 2013 Other contributers as noted in the CONTRIBUTERS file
#
# This file is part of galah-apiclient.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module is responsible for all communications with the Galah server.

"""

import pprint
import pickle
import os
import os.path
import sys
import function
import time
import urlparse

import config
import utils
import ui

import logging
logger = logging.getLogger("apiclient.communicate")

requests = utils.requests_module()

def _parse_api_info(api_info):
    """
    Breaks up API info into a more useable form.

    :param api_info: A list of dictionaries as returned by Galah.
    :returns: A dictionary such that each value is a :class:`function.Function`
            object, and each key is the name of the function.

    """

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
        """
        Saves the session.

        This is done by saving a "session file" containing the cookies and any
        other credientials, as well as a cache file containing the API data.

        """

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
        """
        Loads any data saved by a previous call to :meth:`save`.

        """

        session_file_path = config.CONFIG["session-path"]

        if os.path.isfile(session_file_path):
            logger.info("Loading session file from %s.", session_file_path)

            try:
                with open(session_file_path, "r") as f:
                    self.user, self.requests_session = pickle.load(f)
            except IOError:
                logger.warn(
                    "Could not load session from %s." %
                        (session_file_path, )
                )
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
        Attempts to authenticate with Galah using the given email and password.

        .. note::

            To actually get the credentials from the user, see
            :func:`apiclient.ui.determine_credentials`

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

        logger.info("Logged in as %s.", self.user)

    def fetch_api_info(self):
        """
        Queries the server for the known API commands.

        ``api_info_raw`` will be set to equal the returned text as a single
        ASCII string.

        ``api_info`` will be set appropriately.

        """

        logger.info("Fetching API Info...")

        r = self._send_api_command({"api_name": "get_api_info"})

        if r.status_code != requests.codes.ok:
            logger.critical("Could not get API info from Galah.")
            sys.exit(1)

        self.api_info_raw = r.text.encode("ascii")

        try:
            self.api_info = _parse_api_info(r.json())
        except ValueError:
            logger.critical(
                "Galah did not give us valid API info. It gave us...\n%s",
                self.api_info_raw,
                exc_info = sys.exc_info()
            )
            sys.exit(1)

        logger.debug(
            "Loaded API info...\n%s",
            "\n".join(str(i) for i in self.api_info.values())
        )

    def call(self, command, *args, **kwargs):
        """
        Performs an API command on the server.

        If the server signals that it wants us to download a file, it will be
        done automatically within this function.

        If the server sent text as a response, it will be sent to standard
        output.

        """

        if command not in self.api_info:
            logger.critical(
                "%s is not a known command. You can try using --clear-api-info "
                "to reload the list of available commands.",
                command
            )
            sys.exit(1)

        try:
            request = self.api_info[command].resolve_arguments(
                *args, **kwargs
            )
        except TypeError as e:
            logger.critical(
                "Could not parse command, %s\nUsage: %s",
                str(e),
                str(self.api_info[command]),
                exc_info = sys.exc_info()
            )
            sys.exit(1)

        request["api_name"] = command

        logger.debug(
            "Prepared request for Galah...\n%s",
            pprint.pformat(request, width = 72)
        )

        logger.info(
            "Executing %s command on Galah as user %s.", command, self.user
        )

        r = self._send_api_command(request)

        if r.headers["X-CallSuccess"] != "True":
            if r.headers["X-ErrorType"] == "PermissionError":
                logger.info("The server sent back: %s", r.text)

                logger.critical(
                    "You do not have sufficient permissions to use that "
                    "command."
                )
            else:
                logger.critical("%s", r.text)

            sys.exit(1)
        elif r.status_code != requests.codes.ok:
            logger.critical("An unknown server error occurred.")
            sys.exit(1)

        # If the response is a file...
        if "X-Download" in r.headers:
            default_name = r.headers.get(
                "X-Download-DefaultName", "downloaded_file"
            )

            url = urlparse.urljoin(
                config.CONFIG["host"], r.headers["X-Download"]
            )

            self.download(url, default_name)
        else:
            print r.text

    def _requester(self):
        """
        Determines the most appropriate object to send an HTTP request through.

        :returns: Either the ``requests`` module itself, or a
                ``requests.Session`` object.

        Use this function whenever your about to send a get or post request to
        the server.

        .. code-block::

            self._requester().get("https://galah.galah.com/do/things")

        """

        if self.requests_session:
            return self.requests_session
        else:
            return requests

    def _send_api_command(self, request):
        """
        Send an API command to Galah.

        :param request: A properly formed JSON object to send Galah.
        :returns: A ``requests.Response`` object.

        """

        try:
            requester = self._requester()

            return requester.post(
                config.CONFIG["host"] + "/api/call",
                data = utils.to_json(request),
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

    def download(self, url, file_name):
        """
        Downloads a file from Galah.

        :param url: The URL of the resource.
        :param file_name: The name of the file. Galah will supply this with a
                custom HTTP header.

        """

        try:
            return self._download(url, file_name)
        except KeyboardInterrupt:
            print "\rDownload cancelled by you." + " " * 40
            sys.exit(1)

    def _download(self, url, file_name):
        """
        See :meth:`download`.

        """
        downloads_directory = config.CONFIG["downloads-directory"]

        # Find an available file path
        final_file_path = utils.find_available_file(
            os.path.join(downloads_directory, file_name)
        )
        final_file_name = os.path.basename(final_file_path)

        logger.debug("File will be saved to %s.", final_file_path)

        # Get a generator function that makes a pretty progress bar.
        bar = ui.progress_bar_indeterminate()

        # Actually try to grab the file from the server
        while True:
            ui.print_carriage(
                "%s Trying to download file... %s" %
                    (ui.progress_bar(0.0), " " * 30)
            )

            # Ask the server for the file
            try:
                file_request = self.requests_session.get(
                    url, timeout = 1, stream = True
                )
            except requests.exceptions.Timeout:
                logger.info(
                    "Request timed out. Server did not accept connection after "
                    "1 second."
                )

            # If it's giving it to us...
            if file_request.status_code == 200:
                logger.debug(
                    "Response headers...\n%s",
                    pprint.pformat(file_request.headers, width = 72)
                )

                if "content-length" in file_request.headers:
                    size = float(file_request.headers["content-length"])
                else:
                    logger.info("File is of unknown size.")

                    size = 0
                    ui.print_carriage(
                        ui.progress_bar(-1) + " Downloading file."
                    )

                # Download the file in chunks.
                chunk_size = 124
                downloaded = 0
                with open(final_file_path, "wb") as f:
                    for chunk in file_request.iter_content(124):
                        if size != 0:
                            ui.print_carriage(
                                ui.progress_bar(downloaded / size) +
                                " Downloading file."
                            )
                            downloaded += chunk_size

                        f.write(chunk)

            # If the server got particularly angry at us...
            if (file_request.status_code == 500 or
                    ("X-CallSuccess" in file_request.headers and
                    file_request.headers["X-CallSuccess"] == "False")):
                logger.critical(
                    "500 response. The server encountered an error."
                )
                sys.exit(1)

            if file_request.status_code == requests.codes.ok:
                break

            # Make sure that the trying prompt appears for at least a moment or
            # so
            time.sleep(0.5)

            period = 0.1
            wait_for = 4
            for i in xrange(int(wait_for / period)):
                ui.print_carriage(
                    next(bar) + " Download not ready yet. Waiting."
                )

                time.sleep(period)

        print "File saved to %s." % utils.shorten_path(final_file_path)
