from pages.base_page import BasePage
"""Page Object Model for Insider Careers page."""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CareersPage(BasePage):
    """Page Object Model for Insider Careers Page"""

    def __init__(self, driver):
        super().__init__(driver)

        self.locations_section = (By.ID, "career-our-location")
        self.teams_section = (By.XPATH, "//section[@data-id='a8e7b90']")
        self.life_at_insider_section = (By.ID, "find-job-widget")

    def verify_locations_section(self):
        """Verifies the visibility of the Locations section on the Careers page"""
        locations_element = self.wait.until(
            EC.presence_of_element_located(
                self.locations_section))
        self._scroll_to_element_and_wait(locations_element)
        self.wait.until(
            EC.visibility_of_element_located(
                self.locations_section))
        assert locations_element.is_displayed(), "Locations section is not visible!"

    def verify_teams_section(self):
        """Verifies the visibility of the Teams section on the Careers page"""
        teams_element = self.wait.until(
            EC.presence_of_element_located(
                self.teams_section))
        self._scroll_to_element_and_wait(teams_element)
        self.wait.until(EC.visibility_of_element_located(self.teams_section))
        assert teams_element.is_displayed(), "Teams section is not visible!"

    def verify_life_at_insider_section(self):
        """Verifies the visibility of the Life at Insider section on the Careers page"""
        life_element = self.wait.until(
            EC.presence_of_element_located(
                self.life_at_insider_section))
        self._scroll_to_element_and_wait(life_element)
        self.wait.until(
            EC.visibility_of_element_located(
                self.life_at_insider_section))
        assert life_element.is_displayed(), "Life at Insider section is not visible!"

    def _scroll_to_element_and_wait(self, element):
        """Scrolls to the specified element and waits for a fixed duration

        :param WebElement element: The web element to scroll to and make visible in the viewport
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
