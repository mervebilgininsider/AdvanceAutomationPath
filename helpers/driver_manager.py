import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import platform
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class DriverManager:
    """Manages WebDriver instances and configurations"""
    
    @staticmethod
    def get_driver(browser="chrome"):
        """Creates and returns a WebDriver instance based on the specified browser
        
        :param str browser: The browser type to initialize ("chrome" or "firefox", default: "chrome")
        :return: A configured WebDriver instance
        :rtype: WebDriver
        """
        logger.info(f"Initializing WebDriver instance for {browser} browser")
        
        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            
            # Handle ARM64 architecture on macOS
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                # PATH'teki chromedriver kullanılacak
                return webdriver.Chrome(options=options)
            
            # PATH'teki chromedriver kullanılacak
            return webdriver.Chrome(options=options)
            
        elif browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
       
        else:
            logger.error(f"Unsupported browser type specified: {browser}")
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
                logger.error(f"Error occurred while quitting WebDriver: {str(e)}")