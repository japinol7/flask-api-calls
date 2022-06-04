import logging

LOGGER_FORMAT = '%(levelname)s: %(message)s'
LOGGER_LEVEL = logging.INFO
logging.basicConfig(format=LOGGER_FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(LOGGER_LEVEL)
