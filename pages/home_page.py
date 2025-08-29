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

        self.Cookie_Accept_Button = (By.ID, "wt-cli-accept-all-btn")
        self.Push_Notification_Close = (By.CLASS_NAME, "close")
        self.Company_Menu = (By.XPATH, "//li[contains(@class, 'nav-item dropdown')][6]")
        self.Careers_Link = (By.XPATH, "//a[@href='https://useinsider.com/careers/']")
        self.Agent_One_Popup = (By.CSS_SELECTOR, "div.ins-notification-content")
        self.Agent_One_Close = (By.CSS_SELECTOR, "span.ins-close-button")

    def handle_agent_one_popup(self):
        """Handles and closes the Agent One popup if present"""
        try:
            short_wait = WebDriverWait(self.driver, 2)
            popup = short_wait.until(EC.presence_of_element_located(self.Agent_One_Popup))
            if popup.is_displayed():
                close_button = self.driver.find_element(*self.Agent_One_Close)
                self.driver.execute_script("arguments[0].click();", close_button)
                short_wait.until(EC.invisibility_of_element_located(self.Agent_One_Popup))
        except:
            pass

    def open_page(self, url):
        """
        Opens the specified URL and waits for the page to load
        :param str url: The URL address to navigate to in the browser
        """
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert url in self.driver.current_url, f"Page failed to load: {url}"

    def accept_cookies(self):
        """Accepts the cookie notification"""
        logger.info("Step 2: Accepting cookie notification")
        try:
            accept_button = self.wait.until(EC.element_to_be_clickable(self.Cookie_Accept_Button))
            accept_button.click()
            self.wait.until(EC.invisibility_of_element_located(self.Cookie_Accept_Button))
        except Exception:
            pass

    def close_push_notification(self):
        """Closes the push notification if present"""
        try:
            push_close_button = self.wait.until(EC.element_to_be_clickable(self.Push_Notification_Close))
            push_close_button.click()
        except Exception:
            pass

    def navigate_to_careers(self):
        """Hovers over the 'Company' menu and clicks the 'Careers' option"""
        self.close_push_notification()
        self.handle_agent_one_popup()

        company_menu = self.wait.until(EC.presence_of_element_located(self.Company_Menu))
        self.actions.move_to_element(company_menu).perform()
        
        self.handle_agent_one_popup()

        self.wait.until(EC.visibility_of_element_located(self.Careers_Link))
        assert self.driver.find_element(*self.Careers_Link).is_displayed(), "Careers link is not visible!"

        careers_link = self.wait.until(EC.element_to_be_clickable(self.Careers_Link))
        careers_link.click()

        self.driver.switch_to.window(self.driver.window_handles[-1])
