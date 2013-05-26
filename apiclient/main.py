#!/usr/bin/env python

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

import sys
import pprint
import os

def main():
    # Initialize the logging library.
    import lib.logcontrol
    import logging
    lib.logcontrol.init_logging()
    logger = logging.getLogger("apiclient")

    # Load up the configuration, this includes parsing any command line
    # arguments.
    import lib.config as config
    config.CONFIG = config.load_config()
    if "verbosity" in config.CONFIG:
        lib.logcontrol.set_level(config.CONFIG["verbosity"])
    logger.debug(
        "Final configuration dictionary...\n%s",
        pprint.pformat(config.CONFIG, width = 72)
    )

    # Set to True by any of the "do something and exit" options.
    exit_now = False

    # If the user wants to logout...
    if config.CONFIG.get("logout"):
        session_path = config.CONFIG["session-path"]
        if os.path.isfile(session_path):
            logger.info("Deleting session file at %s.", session_path)
            os.remove(session_path)
        else:
            logger.info(
                "No session file exists at %s. Doing nothing.",
                session_path
            )

        exit_now = True

    # If the user wants to clear the cache...
    if config.CONFIG.get("clear-api-info"):
        api_info_path = config.CONFIG["api-info-path"]
        if os.path.isfile(api_info_path):
            logger.info("Deleting session file at %s.", api_info_path)
            os.remove(api_info_path)
        else:
            logger.info(
                "No session file exists at %s. Doing nothing.",
                api_info_path
            )

        exit_now = True

    if exit_now:
        sys.exit(0)

    # Grab the user's old session information if they are already logged in.
    import lib.communicate
    session = lib.communicate.APIClientSession()
    session.load()

    save_session = False

    # Login if necessary
    import lib.ui
    if session.user is None:
        if config.CONFIG.get("use-oauth"):
            session.login_oauth2()
        else:
            session.login(*lib.ui.determine_credentials())

        save_session = True

    # Request the API info from the server if we don't have it cached
    if session.api_info is None:
        session.fetch_api_info()
        save_session = True

    # Save the session if we had to login or if we replenished our cache
    # (because they are tied together artificially by our design).
    if save_session:
        session.save()

    # Enter the shell or execute a command.
    if config.CONFIG.get("shell"):
        import lib.shell
        new_shell = lib.shell.APIShell(session)

        try:
            new_shell.cmdloop()
        except KeyboardInterrupt:
            while True:
                try:
                    new_shell.cmdloop("")
                except KeyboardInterrupt:
                    print "\nInterrupted..."
                else:
                    break

        print "Exiting..."
    else:
        # Perform the command the user wants to execute
        command_args, command_kwargs = lib.ui.parse_raw_args(config.ARGS)

        if command_args:
            session.call(command_args[0], *command_args[1:], **command_kwargs)
        else:
            logger.info("No command given. Doing nothing...")

if __name__ == "__main__":
    main()
