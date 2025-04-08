from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
import platform
import logging

logger = logging.getLogger(__name__)

class BrowserFactory:
    """Manages WebDriver instances and configurations."""

    @staticmethod
    def get_driver(browser_name="chrome"):
        """Initializes and configures WebDriver for the specified browser.
        
        Args:
            browser_name (str): Name of the browser to use ('chrome' or 'firefox')
            
        Returns:
            WebDriver: Configured browser driver
        """
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            logger.info("Initializing Chrome browser")
            chrome_options = ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)

            if platform.system() == "Darwin" and platform.machine() == "arm64":
                chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                chrome_options.add_argument("--no-sandbox")

            driver = webdriver.Chrome(options=chrome_options)
        
        elif browser_name == "firefox":
            logger.info("Initializing Firefox browser")
            firefox_options = FirefoxOptions()
            firefox_options.set_preference("dom.webnotifications.enabled", False)
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        
        else:
            logger.error(f"Unsupported browser: {browser_name}")
            raise ValueError(f"Unsupported browser: {browser_name}. Supported browsers: 'chrome', 'firefox'")
        
        driver.maximize_window()
        logger.info("Browser initialized successfully")
        return driver

    @staticmethod
    def capture_screenshot(driver, test_name):
        """Captures and saves a screenshot to the reports directory when a test fails."""
        import pytest
        import datetime
        
        screenshots_dir = getattr(pytest, "screenshots_dir", None)
        
        if screenshots_dir is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            screenshots_dir = os.path.join("reports", f"test_run_{timestamp}")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
        
        screenshot_path = os.path.join(screenshots_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        return screenshot_path
