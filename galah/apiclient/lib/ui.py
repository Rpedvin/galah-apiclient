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
This module handles most of the direct interaction with the user during normal
operation.

"""

import sys
import getpass
import re
import pprint
import config
import os

import logging
logger = logging.getLogger("apiclient.ui")

KEY_VALUE_RE = re.compile(r"(?P<name>[a-z_]+)(?!\\)=(?P<value>.*)")
def parse_raw_args(args):
    """
    Parses the command the user gave on the command line.

    :param args: The arguments the user provided (as provided by
            :data:`apiclient.config.ARGS`).
    :returns: A tuple ``(args, kwargs)``.

    .. code-block:: text

        >>> ui.parse_raw_args(["first", "second", "bar=apple sauce", "boom=bang"])
        (['first', 'second'], {'bar': 'apple sauce', 'boom': 'bang'})

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

    :returns: ``(user, password)``

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

import sys
def print_carriage(text, width = 72):
    """
    Prints some text to standard out, followed by a carriage return. Also
    flushes standard out afterwards.

    """

    sys.stdout.write("\r" + str(text) + " " * (width - len(text)) + "\r")
    sys.stdout.flush()

def progress_bar_indeterminate(size = 20, ball = "#####"):
    """
    A generator function that creates an indeterminate progress bar.

    :param size: The width of the progress bar.
    :param ball: The characters to use for the ball.

    .. code-block:: python

        >>> a = ui.progress_bar_indeterminate(7, "--")
        >>> next(a)
        '[ --  ]'
        >>> next(a)
        '[  -- ]'
        >>> next(a)
        '[   --]'
        >>> next(a)
        '[  -- ]'
        >>> next(a)
        '[ --  ]'
        >>> next(a)
        '[--   ]'

    """

    position = 0
    going_right = True
    adjusted_size = size - len(ball) - 2

    if adjusted_size <= 1:
        raise ValueError("size not big enough.")

    while True:
        position += 1 if going_right else -1

        if position == adjusted_size:
            going_right = False
        elif position == 0:
            going_right = True

        result = "[" + " " * (position) + ball + " " * (adjusted_size - position) + "]"

        yield "".join(result)

def progress_bar(progress, size = 20):
    """
    Returns an ASCII progress bar.

    :param progress: A floating point number between 0 and 1 representing the
            progress that has been completed already.
    :param size: The width of the bar.

    .. code-block:: python

        >>> ui.progress_bar(0.5, 10)
        '[####    ]'

    """

    size -= 2
    if size <= 0:
        raise ValueError("size not big enough.")

    if progress < 0:
        return "[" + "?" * size + "]"
    else:
        progress = min(progress, 1)
        done = int(round(size * progress))
        return "[" + "#" * done + " " * (size - done) + "]"
