import logging


# ----- Account -----
ACCOUNT_IDENTIFIER = "magnus.kz"
PASSWORD = "Januar2023"

# ----- Streak settings -----
STREAK_EMOJI = "🔥"
DAYS_TO_RUN_FOR = -1  # Use -1 to run for infinity (or CTRL+C is pressed)
SEND_TIMESTAMPS = [
    "9:00:00",
    "12:00:00",
    "15:00:00",
    "18:00:00",
    "21:00:00",
]  # If some of these are too close (10-15 seconds or less apart), the second one will likely be skipped. (European/Military local time)

# ----- Logging settings -----
LOG_LEVEL = logging.DEBUG
OTHER_LOGGER_LEVELS = logging.ERROR
LOG_WITH_COLORS = True

# ----- Data settings -----
# WARNING!!! This will use around 300 megabytes on your disk
SAVE_SELENIUM_DATA = True
SELENIUM_DATA_DIRECTORY = ".selenium_data"

# ----- Selenium settings -----
HEADLESS = False  # This is not recommended because there might be served a captcha on login which will need manual solving
