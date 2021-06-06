import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def read_file_as_string(file_name):
    res = []
    try:
        with open(file_name, "r", encoding='utf-8') as in_file:
            for line_in in in_file:
                res.append(line_in)
    except FileNotFoundError:
        logger.critical(f"Input file not found: {file_name}")
    except Exception:
        logger.critical(f"Error reading file: {file_name}")

    return ''.join(res)
