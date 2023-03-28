import logging
import sys

LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT = '%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s'
LOGGER_FORMAT_NO_DATE = 'No datetime | %(levelname)s | %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
SYS_STDOUT = sys.stdout

log = logging.getLogger(__name__)
log.setLevel(LOGGER_LEVEL)


def add_stdout_handler(logger_format=LOGGER_FORMAT):
    stdout_handler = logging.StreamHandler(SYS_STDOUT)
    stdout_handler.setLevel(LOGGER_LEVEL)
    stdout_handler.setFormatter(logging.Formatter(fmt=logger_format, datefmt=LOGGER_DATE_FORMAT))
    log.addHandler(stdout_handler)


add_stdout_handler()
