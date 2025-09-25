"""WebDriver management utilities for browser automation."""

import logging
import platform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages WebDriver instances and configurations"""

    @staticmethod
    def get_driver(browser="chrome"):
        """Creates and returns a WebDriver instance based on the specified browser

        :param str browser: The browser type to initialize ("chrome" or "firefox",
        default: "chrome")
        :return: A configured WebDriver instance
        :rtype: WebDriver
        """
        logger.info("Initializing WebDriver instance for %s browser", browser)

        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")

            if platform.system() == "Darwin" and platform.machine() == "arm64":
                options.binary_location = (
                    "/Applications/Google Chrome.app"
                    "/Contents/MacOS/Google Chrome")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

                return webdriver.Chrome(options=options)

            return webdriver.Chrome(options=options)

        elif browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            return webdriver.Firefox(
                service=FirefoxService(
                    GeckoDriverManager().install()),
                options=options)

        else:
            logger.error("Unsupported browser type specified: %s", browser)
            raise ValueError(f"Unsupported browser type specified: {browser}")

    @staticmethod
    def quit_driver(driver):
        """Safely quits the WebDriver instance

        :param WebDriver driver: The WebDriver instance to quit
        """
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver instance terminated successfully")
            except Exception as e:
                logger.error("Error occurred while quitting WebDriver: %s", str(e))
