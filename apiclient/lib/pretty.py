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
A module that makes it easier to make your output "pretty".

"""

def pretty_list(the_list, conjunction = "and", none_string = "nothing"):
    """
    Returns a grammatically correct string representing the given list. For
    example...

    >>> pretty_list(["John", "Bill", "Stacy"])
    "John, Bill, and Stacy"
    >>> pretty_list(["Bill", "Jorgan"], "or")
    "Bill or Jorgan"
    >>> pretty_list([], none_string = "nobody")
    "nobody"

    """

    the_list = list(the_list)

    if len(the_list) == 0:
        return none_string
    elif len(the_list) == 1:
        return str(the_list[0])
    elif len(the_list) == 2:
        return str(the_list[0]) + " " + conjunction + " " + str(the_list[1])
    else:
        # Add every item except the last two together seperated by commas
        result = ", ".join([str(s) for s in the_list[:-2]]) + ", "

        # Add the last two items, joined together by a command and the given
        # conjunction
        result += "%s, %s %s" % \
            (str(the_list[-2]), conjunction, str(the_list[-1]))

        return result

def plural_if(zstring, zcondition):
    """
    Returns zstring pluralized (adds an 's' to the end) if zcondition is True or
    if zcondition is not equal to 1.

    Example usage could be ``plural_if("cow", len(cow_list))``.

    """

    # If they gave us a boolean value, just use that, otherwise, assume the
    # value is some integral type.
    if type(zcondition) is bool:
        plural = zcondition
    else:
        plural = zcondition != 1

    return zstring + ("s" if plural else "")

colors = {
    "black": "0;30",
    "bright gray": "0;37",
    "blue": "0;34",
    "white": "1;37",
    "green": "0;32",
    "bright blue": "1;34",
    "cyan": "0;36",
    "bright green": "1;32",
    "red": "0;31",
    "bright cyan": "1;36",
    "purple": "0;35",
    "bright red": "1;31",
    "yellow": "0;33",
    "bright purple": "1;35",
    "dark gray": "1;30",
    "bright yellow": "1;33",
    "normal": "0"
}

def color(text, color_name):
    return "\033[%sm%s\033[0m" % (colors[color_name.lower()], text)
