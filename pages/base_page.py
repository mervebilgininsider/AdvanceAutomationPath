"""Base page class for common WebDriver functionality."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """Base page class that provides common WebDriver functionality."""
    
    def __init__(self, driver):
        """Initialize the base page with driver and common utilities.
        
        :param WebDriver driver: The Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.actions = ActionChains(driver)
