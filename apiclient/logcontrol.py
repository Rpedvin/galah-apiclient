import logging

def init_logging():
	"""Set up the logger with default values."""

	logging.basicConfig(format = "%(levelname)s - %(message)s\n" + "-" * 72)
	set_level(logging.INFO)

def set_level(log_level):
	logging.getLogger("apiclient").setLevel(log_level)

LOG_LEVELS = {
    "NOLOGGING": 100,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG
}
