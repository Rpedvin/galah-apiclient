import sys

import logging
logger = logging.getLogger("apiclient.logcontrol")

def init_logging():
    """Set up the logger with default values."""

    logging.basicConfig(format = "%(levelname)s - %(message)s\n" + "-" * 72)
    set_level("INFO")

def set_level(log_level):
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
