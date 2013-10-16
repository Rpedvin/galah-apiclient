"""
This file contains the actual actions and options that the API Client supports.
It was split off from the main config module due to its sheer size. Note that
this module is fairly coupled with the config module and they should not be
considered indepenent.

"""

def get_actions():
    """
    Creates and returns a dictionary mapping action names to Action objects.

    """

    from config2 import Option, Action

    _action_list = []

    # Global options
    _action_list.append(Action(
        name = "*",
        description = None,
        options = [
            Option(
                name = ["--host"],
                description = "The URL of the host to connect to. Example: "
                        "https://galah.myschool.edu",
                validator = "^https?://.+$",
            ),
            Option(
                name = ["-v", "--verbosity"],
                description =
                    "The desired verbosity. May be specified more than once.",
                argparse_config = {
                    "action": "count"
                }
            ),
            Option(
                name = ["-q", "--quiet"],
                description = "If set, no output at all will be printed.",
                argparse_config = {
                    "action": "store_true"
                }
            ),
            Option(
                name = ["--show-tracebacks"],
                description =
                    "Whether to display trace backs when *expected* "
                    "exceptions are encountered.",
                saveable = "show-tracebacks",
                argparse_config = {
                    "action": "store_true",
                    "dest": "show-tracebacks"
                }
            ),
            Option(
                name = ["--no-show-tracebacks"],
                description = "Negates the effects of show-tracebacks",
                saveable = "show-tracebacks",
                argparse_config = {
                    "action": "store_true",
                    "dest": "show-tracebacks"
                }
            ),
            Option(
                name = ["--ca-certs-path"],
                default = "~/.cache/galah/ca_certs",
                description =
                    "The location of the file containing a collection of certificate "
                    "authority certificates. This is used when verifying SSL "
                    "connections. If the file does not exist, a file with a default "
                    "set of certificates will be placed there."
            ),
        ]
    ))

    # Login options
    _action_list.append(Action(
        name = "login",
        description = "Authenticate with Galah as a particular user.",
        options = [
            Option(
                name = ["user"],
                description = "The user to login as."
            ),
            Option(
                name = ["--use-oauth"],
                description =
                    "If set, authentication will be done via OAuth rather "
                    "than internal auth over HTTP(S).",
                saveable = "login/use-oauth",
                argparse_config = {
                    "action": "store_true",
                    "dest": "use_oauth"
                }
            ),
            Option(
                name = ["--no-use-oauth"],
                description = "Negates the effect of use-oauth.",
                saveable = "login/use-oauth",
                argparse_config = {
                    "action": "store_false",
                    "dest": "use_oauth"
                }
            )
        ]
    ))

    return dict((i.name, i) for i in _action_list)
