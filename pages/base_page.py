"""Base page class for common WebDriver functionality."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base page class that provides common WebDriver functionality."""

    def __init__(self, driver):
        """Initialize the base page with driver and common utilities.

        :param WebDriver driver: The Selenium WebDriver instance
        """
        self.driver = driver
        self.wait_short = WebDriverWait(driver, 2)
        self.wait = WebDriverWait(driver, 5)
        self.wait_long = WebDriverWait(driver, 45)
        self.actions = ActionChains(driver)

    def wait_document_ready(self, timeout: int = 30) -> None:
        """Block until document.readyState becomes 'complete'.

        :param int timeout: Maximum time to wait in seconds (default: 30)
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def scroll_into_center(self, element) -> None:
        """Scroll the given element into viewport center using JavaScript.

        :param WebElement element: The element to scroll into view
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def wait_until_visible(self, locator, timeout: int = 30):
        """Wait until a locator resolves to a visible element.

        :param tuple locator: Locator tuple, e.g. (By.ID, 'value')
        :param int timeout: Maximum time to wait in seconds
        :return: The visible WebElement
        """
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator, timeout: int = 30):
        """Wait until a locator resolves to a clickable element.

        :param tuple locator: Locator tuple, e.g. (By.ID, 'value')
        :param int timeout: Maximum time to wait in seconds
        :return: The clickable WebElement
        """
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def click_via_js(self, element) -> None:
        """Click the given element using JavaScript to avoid overlay issues.

        :param WebElement element: The element to click
        """
        self.driver.execute_script("arguments[0].click();", element)
