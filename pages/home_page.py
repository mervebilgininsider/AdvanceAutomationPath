"""Page Object Model for Insider Home page."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object Model for Insider Home Page"""

    def __init__(self, driver):
        super().__init__(driver)

        self.cookie_accept_button = (By.ID, "wt-cli-accept-all-btn")
        self.push_notification_close = (By.CLASS_NAME, "close")
        self.company_menu = (
            By.XPATH, "//li[contains(@class, 'nav-item dropdown')][6]")
        self.careers_link = (
            By.XPATH, "//a[@href='https://useinsider.com/careers/']")
        self.agent_one_popup = (
            By.CSS_SELECTOR,
            "div.ins-notification-content")
        self.agent_one_close = (By.CSS_SELECTOR, "span.ins-close-button")

    def handle_agent_one_popup(self):
        """Handles and closes the Agent One popup if present"""
        try:
            popup = self.wait_short.until(
                EC.presence_of_element_located(
                    self.agent_one_popup))
            if popup.is_displayed():
                close_button = self.driver.find_element(*self.agent_one_close)
                self.driver.execute_script(
                    "arguments[0].click();", close_button)
                self.wait_short.until(
                    EC.invisibility_of_element_located(
                        self.agent_one_popup))
        except BaseException:
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
        try:
            accept_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.cookie_accept_button))
            accept_button.click()
            self.wait.until(
                EC.invisibility_of_element_located(
                    self.cookie_accept_button))
        except Exception:
            pass

    def close_push_notification(self):
        """Closes the push notification if present"""
        try:
            push_close_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.push_notification_close))
            push_close_button.click()
        except Exception:
            pass

    def hover_company_menu(self):
        """Hovers over the Company menu"""
        company_menu = self.wait.until(
            EC.presence_of_element_located(
                self.company_menu))
        self.actions.move_to_element(company_menu).perform()

    def click_careers_link(self):
        """Clicks on the Careers link"""
        self.wait.until(EC.visibility_of_element_located(self.careers_link))
        assert self.driver.find_element(
            *self.careers_link).is_displayed(), "Careers link is not visible!"

        careers_link = self.wait.until(
            EC.element_to_be_clickable(
                self.careers_link))
        careers_link.click()

    def switch_to_new_window(self):
        """Switches to the newly opened window"""
        self.driver.switch_to.window(self.driver.window_handles[-1])
