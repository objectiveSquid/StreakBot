import config

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

import logging
import time
import sys


class StreakBot:
    def __init__(self) -> None:
        self.__logger = logging.getLogger("selenium_bot")

        logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(
            config.OTHER_LOGGER_LEVELS,
        )
        logging.getLogger("selenium.webdriver.common.selenium_manager").setLevel(
            config.OTHER_LOGGER_LEVELS,
        )
        logging.getLogger("selenium.webdriver.common.service").setLevel(
            config.OTHER_LOGGER_LEVELS,
        )
        logging.getLogger("urllib3.connectionpool").setLevel(
            config.OTHER_LOGGER_LEVELS,
        )
        logging.getLogger("urllib3.util.retry").setLevel(
            config.OTHER_LOGGER_LEVELS,
        )

        self.__logger.debug("Creating selenium instance")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(f"user-data-dir={config.SELENIUM_DATA_DIRECTORY}")
        options.add_argument(
            "--use-fake-ui-for-media-stream"
        )  # This allows all media access
        if config.HEADLESS:
            options.add_argument("--headless")
            options.add_argument("--disable-crash-reporter")
            if sys.platform == "win32":
                options.add_argument("--disable-gpu")  # Windows only
        self.__driver = webdriver.Chrome(options=options)
        self.__logger.info("Launched selenium instance")
        self.__long_waiter = WebDriverWait(self.__driver, 7.5)
        self.__medium_waiter = WebDriverWait(self.__driver, 3.5)
        self.__short_waiter = WebDriverWait(self.__driver, 1)
        self.__logged_in = False

    def login(self, account_identifier: str, password: str) -> None:
        if self.__logged_in:
            self.__logger.error(
                "Already logged in. Please create a new `SnapBot` object if you want to use another account"
            )
            return

        self.__driver.get("https://accounts.snapchat.com/accounts/v2/login")
        try:
            # Wait for welcome page and go to chat page
            self.__short_waiter.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='WebChatBanner_title']")
                )
            ).click()

            self.__logger.warning(
                "Already logged in, using currently logged in account."
            )
            self.__logged_in = True
            do_login = False
        except TimeoutException:
            do_login = True

        if do_login:
            # This skips accept cookies page
            self.__driver.add_cookie(
                {
                    "name": "sc-cookies-accepted",
                    "value": "true",
                    "domain": ".snapchat.com",
                }
            )
            self.__driver.add_cookie(
                {"name": "EssentialSession", "value": "true", "domain": ".snapchat.com"}
            )
            self.__driver.add_cookie(
                {"name": "Marketing", "value": "false", "domain": ".snapchat.com"}
            )
            self.__driver.add_cookie(
                {"name": "Performance", "value": "false", "domain": ".snapchat.com"}
            )
            self.__driver.add_cookie(
                {"name": "Preferences", "value": "false", "domain": ".snapchat.com"}
            )
            self.__logger.debug("Added cookie selection")
            self.__driver.refresh()

            # Wait for username page and submit username
            self.__medium_waiter.until(
                EC.presence_of_element_located((By.ID, "accountIdentifier"))
            ).send_keys(account_identifier)
            time.sleep(0.5)
            self.__driver.find_element(
                By.XPATH, '//*[@id="account_identifier_form"]/div[3]/button'
            ).click()
            self.__logger.debug("Submitted account identifier")

            # Wait for probable captcha
            try:
                self.__short_waiter.until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, "iframe"))
                )
                self.__logger.info("Captcha detected on login, waiting for solve...")
                while True:
                    try:
                        self.__long_waiter.until(
                            EC.presence_of_element_located((By.ID, "password"))
                        )
                        self.__logger.info("Captcha completed")
                        break
                    except TimeoutException:
                        continue
            except TimeoutException:
                self.__logger.debug("No captcha found")

            # Wait for password page and submit password
            self.__short_waiter.until(
                EC.presence_of_element_located((By.ID, "password"))
            ).send_keys(password)
            self.__driver.find_element(
                By.XPATH, '//*[@id="password_form"]/div[3]/button'
            ).click()
            self.__logger.debug("Submitted password")

            # Wait for welcome page and go to chat page
            self.__medium_waiter.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='WebChatBanner_title']")
                )
            ).click()
            self.__logger.debug("Went to chat page")

        # Wait for chat page and ignore notifcations
        try:
            self.__medium_waiter.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="root"]/div[1]/div[2]/div/div/div[4]/div[2]/button[1]',
                    )
                )
            ).click()
            self.__logger.debug("Clicked ignore notifications")
        except TimeoutException:
            self.__logger.debug("Ignore notifications popup did not appear")
        self.__logger.info("Finished logging in")
        self.__logged_in = True

    def send_streaks(self) -> None:
        if not self.__logged_in:
            self.__logger.error(
                "Not logged in, please execute the `login` function before sending streaks"
            )
            return

        self.__logger.info("Starting to send streaks")

        # Open camera menu
        self.__driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/button',
        ).click()
        self.__logger.debug("Went to camera menu")

        # Wait for possible camera permissions popup
        try:
            self.__short_waiter.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div[1]/div/div/div[4]/div[2]/button',
                    )
                )
            ).click()
            self.__logger.info("Waiting for accept camera and microphone...")
        except TimeoutException:
            pass
        while True:
            try:
                self.__long_waiter.until_not(
                    EC.visibility_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "tag_name[alt=landing-page-camera-mic-callout]",
                        )
                    )
                )
                self.__logger.info("Camera and microphone accepted")
                break
            except TimeoutException:
                continue

        # Take picture
        self.__short_waiter.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]',
                )
            )
        ).click()
        self.__logger.debug("Captured image")

        # Click select recipients button
        self.__short_waiter.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="snap-preview-container"]/div[2]/button[2]')
            )
        ).click()
        self.__logger.debug("Went to select recipients page")

        # Select people with streaks
        checked_names = []
        selected_names = []
        friend_elements = self.__driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/form/div/ul/li[3]',
        ).find_elements(By.XPATH, "following-sibling::*")
        for friend_element in friend_elements:
            try:
                display_name = friend_element.find_element(
                    By.CSS_SELECTOR, '[class$="nonIntl"]'
                ).text
            except NoSuchElementException:
                continue
            if display_name in checked_names:
                continue
            checked_names.append(display_name)
            has_streak = config.STREAK_EMOJI in friend_element.text.replace(
                display_name, ""
            )
            self.__logger.debug(
                f"Checked '{display_name}' for streak, result: {has_streak}"
            )
            if has_streak:
                friend_element.click()
                selected_names.append(display_name)
                self.__logger.info(f"Selected name '{display_name}' for streak.")

        # Click send button
        self.__driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/form/div[2]/button',
        ).click()

        self.__logger.info(f"Sent streak to {len(selected_names)} people")

    @property
    def driver(self) -> webdriver.Chrome:
        return self.__driver
