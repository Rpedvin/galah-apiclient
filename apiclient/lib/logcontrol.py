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
This module provides functions to simplify management of the ``logging``
standard library module.

"""

import sys

import logging
logger = logging.getLogger("apiclient.logcontrol")

def init_logging():
    """Set up the logger with default values."""

    logging.basicConfig(format = "%(levelname)s - %(message)s\n" + "-" * 72)
    set_level("INFO")

def set_level(log_level):
    """Set the log level."""

    if log_level not in LOG_LEVELS:
        logger.critical(
            "Invalid log level %s. Choices are %s.",
            log_level,
            ", ".join(LOG_LEVELS)
        )
        sys.exit(1)

    logging.getLogger("apiclient").setLevel(LOG_LEVELS[log_level])

LOG_LEVELS = {
    "NOLOGGING": 100,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG
}
