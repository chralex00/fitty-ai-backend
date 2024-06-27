import logging
from logging import Logger
import sys

LOGGER: Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)

LOGGER.addHandler(stream_handler)