from app.tools.logger.logger import log


def read_file_as_string(file_name):
    res = []
    try:
        with open(file_name, "r", encoding='utf-8') as in_file:
            for line_in in in_file:
                res.append(line_in)
    except FileNotFoundError:
        log.critical(f"Input file not found: {file_name}")
    except Exception:
        log.critical(f"Error reading file: {file_name}")

    return ''.join(res)


def read_file_as_list(file_name):
    res = []
    try:
        with open(file_name, "r", encoding='utf-8') as in_file:
            for line_in in in_file:
                res.append(line_in)
    except FileNotFoundError:
        log.critical(f"Input file not found: {file_name}")
    except Exception:
        log.critical(f"Error reading file: {file_name}")

    return res


def read_file_as_list_strip(file_name):
    res = []
    try:
        with open(file_name, "r", encoding='utf-8') as in_file:
            for line_in in in_file:
                res.append(line_in.strip())
    except FileNotFoundError:
        log.critical(f"Input file not found: {file_name}")
    except Exception:
        log.critical(f"Error reading file: {file_name}")

    return res


def time_seconds_format_to_hms(seconds, zero_first=False):
    if zero_first:
        return f'{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 3600 % 60:02d}'
    return f'{seconds // 3600}:{seconds % 3600 // 60:02d}:{seconds % 3600 % 60:02d}'


def time_seconds_format_to_min_sec(seconds, zero_first=False):
    if zero_first:
        return f'{seconds % 3600 // 60:02d}:{seconds % 3600 % 60:02d}'
    return f'{seconds % 3600 // 60}:{seconds % 3600 % 60:02d}'
