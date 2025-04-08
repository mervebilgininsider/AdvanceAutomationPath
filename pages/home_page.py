from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging

logger = logging.getLogger(__name__)

class HomePage:
    """Page Object Model for Insider Home Page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.actions = ActionChains(driver)
        logger.info("HomePage object initialized")

        self.cookie_accept_button = (By.ID, "wt-cli-accept-all-btn")
        self.push_notification_close = (By.CLASS_NAME, "close")
        self.company_menu = (By.XPATH, "//li[contains(@class, 'nav-item dropdown')][6]")
        self.careers_link = (By.XPATH, "//a[@href='https://useinsider.com/careers/']")
        self.agent_one_popup = (By.CSS_SELECTOR, "div.ins-notification-content")
        self.agent_one_close = (By.CSS_SELECTOR, "span.ins-close-button")

    def handle_agent_one_popup(self):
        """Handles and closes the Agent One popup if present"""
        try:
            short_wait = WebDriverWait(self.driver, 2)
            popup = short_wait.until(EC.presence_of_element_located(self.agent_one_popup))
            if popup.is_displayed():
                logger.info("Step 1.1: Closing Agent One popup")
                close_button = self.driver.find_element(*self.agent_one_close)
                self.driver.execute_script("arguments[0].click();", close_button)
                short_wait.until(EC.invisibility_of_element_located(self.agent_one_popup))
                logger.info("Agent One popup closed successfully")
        except:
            pass

    def open_page(self, url):
        """Opens the specified URL and waits for the page to load"""
        self.driver.get(url)
        logger.info(f"Navigated to URL: {url}")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert url in self.driver.current_url, f"Page failed to load: {url}"

    def accept_cookies(self):
        """Accepts the cookie notification"""
        logger.info("Step 2: Accepting cookie notification")
        try:
            accept_button = self.wait.until(EC.element_to_be_clickable(self.cookie_accept_button))
            accept_button.click()
            self.wait.until(EC.invisibility_of_element_located(self.cookie_accept_button))
            logger.info("Cookie notification accepted successfully")
        except Exception:
            logger.info("Cookie notification not visible or already accepted")

    def close_push_notification(self):
        """Closes the push notification if present"""
        try:
            push_close_button = self.wait.until(EC.element_to_be_clickable(self.push_notification_close))
            push_close_button.click()
            logger.info("Push notification closed successfully")
        except Exception:
            pass

    def navigate_to_careers(self):
        """Hovers over the 'Company' menu and clicks the 'Careers' option"""
        logger.info("Step 3: Navigating to Careers page")
        self.close_push_notification()
        self.handle_agent_one_popup()

        company_menu = self.wait.until(EC.presence_of_element_located(self.company_menu))
        self.actions.move_to_element(company_menu).perform()
        logger.info("Hovered over Company menu")
        
        self.handle_agent_one_popup()

        self.wait.until(EC.visibility_of_element_located(self.careers_link))
        assert self.driver.find_element(*self.careers_link).is_displayed(), "Careers link is not visible!"

        careers_link = self.wait.until(EC.element_to_be_clickable(self.careers_link))
        careers_link.click()
        logger.info("Clicked Careers link")

        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("Successfully navigated to Careers page")
