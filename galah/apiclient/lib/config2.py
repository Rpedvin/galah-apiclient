# stdlib
import argparse
import re

import logging
logger = logging.getLogger("apiclient.config")

class Action:
    def __init__(self, name, description, options):
        self.name = name
        self.description = description
        self.options = options

class Option:
    """
    Represents a settable configuration option.

    Configuration options can be set via the command line or through the
    configuration file. If a value for particular setting is present in both,
    the command line takes precedance.

    :ivar name: The configuraiton option's name.
    :ivar action: The action this setting applies to (for example: ``shell`` or
            ``login``). May be ``"*"`` if the setting applies to all actions
            (or does not apply specifically to any).
    :ivar description: A textual description of the option and what it does.
    :ivar expected_type: A valid Python type. The value provided by the user
            will be converted to this type automatically (a failure to do so
            will result in a ValidationFailure being raised).
    :ivar validator: May be either a function or a string. If it is a string,
            it will parsed as a regex and a configuration value will only be
            valid if it matches the regex. If it is a function, that function
            will be called with a single parameter `value`. If the value is
            not valid, a ValidationFailure should be raised. The return value
            of the function is ignored.
    :ivar required: If True, a MissingValue will be raised if the user does
            not provide a value for the setting (None still counts as a value).
    :ivar default: A default value to use if the user does not provide a value
            for the setting (None is a valid default value).
    :ivar saveable: Whether the option can be saved and loaded from the
            configuration file. If this is a string, it will be the path used
            in the configuration file.
    :ivar argparse_config: A dictionary of arguments to pass to the
            ``add_argument`` option.

    """

    class NoValue:
        pass

    def __init__(self, name, description = None, expected_type = str,
            validator = None, required = False, default = NoValue(),
            saveable = True, argparse_config = None):
        self.name = name
        self.description = description
        self.expected_type = expected_type
        self.required = required
        self.default = default
        self.saveable = saveable
        if argparse_config is None:
            self.argparse_config = {}
        else:
            self.argparse_config = argparse_config

        if self.required and type(self.default) is not NoValue:
            raise ValueError(
                "A configuration option cannot be required and have a default "
                "value as well."
            )

        if isinstance(validator, basestring):
            regex = re.compile(validator)
            self.validator = lambda s: regex.match(s) is not None
        else:
            self.validator = validator

    def validate(self, value):
        if not isinstance(value, self.expected_type):
            raise errors.ValidationFailure(
                name = self.name,
                value = value,
                reason = "Given value '%s' is not an instance of type %s." % (
                    repr(value), expected_type.__name__)
            )

        try:
            if self.validator is not None:
                self.validator(value)
        except errors.ValidationFailure:
            # If validation function threw an error add the name of the
            # config value to it.
            exc_info = sys.exc_info()
            exc_info[1].name = self.name
            exc_info[1].value = self.value
            raise exc_info[1], None, exc_info[2]
        except:
            raise errors.ValidationFailure(
                name = self.name,
                value = value,
                exc_info = sys.exc_info()
            )

def create_argparser(actions):
    """
    Creates an ``argparse.ArgumentParser`` object that can be used on the
    user's command line arguments.

    """

    global_parser = argparse.ArgumentParser(add_help = False)
    if "*" in actions:
        for i in actions["*"].options:
            global_parser.add_argument(*i.name, help = i.description,
                **i.argparse_config)

    parser = argparse.ArgumentParser(
        description = "A utility for interacting with Galah.",
        parents = [global_parser]
    )
    subs = parser.add_subparsers()        

    # Add all the global options.
    for k, v in actions.items():
        if k == "*":
            continue

        subparser = subs.add_parser(v.name, help = v.description,
            parents = [global_parser])

        for i in v.options:
            subparser.add_argument(*i.name, help = i.description,
                **i.argparse_config)

    return parser

# def parse_arguments(args = sys.argv[1:]):
#     """
#     Parses any given command line arguments.

#     :param args: A list of arguments to parse. It should not include the "first"
#             command line argument (the name of the executable).

#     """

#     option_list = []

#     # Go through the configuration options and map them to command line options
#     for i in KNOWN_OPTIONS.values():
#         if i.data_type is bool:
#             action = "store_false" if i.default_value == True else "store_true"
#         else:
#             action = "store"

#         required_string = ""
#         if i.required:
#             required_string = (
#                 " A value must be present for this option either as a command-"
#                 "line argument or within the configuration file."
#             )

#         default_string = ""
#         if i.default_value is not None:
#             default_string = " [Default: %s]" % (str(i.default_value), )

#         option_list.append(make_option(
#             "--" + i.name, action = action, dest = i.name,
#             help = i.description + required_string + default_string
#         ))

#     parser = OptionParser(
#         description = "Command line interface to Galah for use by instructors "
#                       "and administrators.",
#         option_list = option_list
#     )

#     options, args = parser.parse_args(args)

#     return (options, args)
