from process_time import get_time_of_day_seconds, convert_timestamps
from logger import configure_logging
from bot import StreakBot
import config

import logging
import time


def main() -> None:
    configure_logging(config.LOG_LEVEL, config.LOG_WITH_COLORS)

    main_logger = logging.getLogger("main")

    run_timestamps = convert_timestamps()
    if len(run_timestamps) == 0:
        return

    bot = StreakBot()
    bot.login(config.ACCOUNT_IDENTIFIER, config.PASSWORD)

    iterations_left = config.DAYS_TO_RUN_FOR * len(run_timestamps)

    try:
        while iterations_left != 0:
            time_to_wait = run_timestamps[0][0] - get_time_of_day_seconds()
            target_timestamp = run_timestamps[0][1]
            run_timestamps.append(run_timestamps.pop(0))
            if time_to_wait <= 0:
                continue
            main_logger.info(
                f"Sleeping for {time_to_wait} seconds (until {target_timestamp})"
            )
            time.sleep(time_to_wait)
            bot.send_streaks()
            iterations_left -= 1
    except KeyboardInterrupt:
        pass

    main_logger.info("Quitting")
    bot.driver.quit()


if __name__ == "__main__":
    main()
