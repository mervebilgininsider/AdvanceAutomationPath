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
        """Creates and returns a WebDriver instance based on the specified browser"""
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
                
                # Set ChromeDriver path for ARM64
                driver_path = os.path.expanduser("~/.wdm/drivers/chromedriver/mac64/134.0.6998.165/chromedriver-mac-arm64/chromedriver")
                if not os.path.exists(driver_path):
                    driver_path = ChromeDriverManager().install()
                
                return webdriver.Chrome(service=ChromeService(driver_path), options=options)
            
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            
        elif browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
       
        else:
            logger.error(f"Unsupported browser type specified: {browser}")
            raise ValueError(f"Unsupported browser type specified: {browser}")

    @staticmethod
    def quit_driver(driver, test_name=None):
        """Safely quits the WebDriver instance after capturing screenshot if test failed"""
        if driver:
            try:
                # Capture screenshot if test failed
                if test_name:
                    screenshots_dir = "screenshots"
                    if not os.path.exists(screenshots_dir):
                        os.makedirs(screenshots_dir)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot captured and saved to: {screenshot_path}")
                
                driver.quit()
                logger.info("WebDriver instance terminated successfully")
            except Exception as e:
                logger.error(f"Error occurred while quitting WebDriver: {str(e)}") 