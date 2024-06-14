import config

import logging
import time


_timestamp_logger = logging.getLogger("timestamps")


def convert_timestamps() -> list[tuple[int, str]]:
    day_times = []

    for timestamp in config.SEND_TIMESTAMPS:
        if any([not part.isdigit() for part in timestamp.split(":")]):
            _timestamp_logger.warning(
                f"Invalid timestamp in config file: '{timestamp}'"
            )
            continue

        try:
            hour, minute, second = timestamp.split(":")
        except ValueError:
            continue
        hour = int(hour)
        minute = int(minute)
        second = int(second)

        day_times.append(((hour * 3600) + (minute * 60) + second, timestamp))

    if len(timestamp) == 0:
        _timestamp_logger.critical("No valid timestamps found in config file")
    return list(sorted(set(day_times)))


def get_time_of_day_seconds() -> int:
    current_local_time = time.localtime()

    hours = current_local_time.tm_hour
    minutes = current_local_time.tm_min
    seconds = current_local_time.tm_sec

    return hours * 3600 + minutes * 60 + seconds
