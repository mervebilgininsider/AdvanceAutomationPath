from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CareersPage:
    """Page Object Model for Insider Careers Page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        self.Locations_Section = (By.ID, "career-our-location")
        self.Teams_Section = (By.XPATH, "//section[@data-id='a8e7b90']")
        self.Life_at_Insider_Section = (By.ID, "find-job-widget")

    def verify_locations_section(self):
        """Verifies the visibility of the Locations section on the Careers page"""
        locations_element = self.wait.until(EC.presence_of_element_located(self.Locations_Section))
        self._scroll_to_element_and_wait(locations_element)
        self.wait.until(EC.visibility_of_element_located(self.Locations_Section))
        assert locations_element.is_displayed(), "Locations section is not visible!"

    def verify_teams_section(self):
        """Verifies the visibility of the Teams section on the Careers page"""
        teams_element = self.wait.until(EC.presence_of_element_located(self.Teams_Section))
        self._scroll_to_element_and_wait(teams_element)
        self.wait.until(EC.visibility_of_element_located(self.Teams_Section))
        assert teams_element.is_displayed(), "Teams section is not visible!"

    def verify_life_at_insider_section(self):
        """Verifies the visibility of the Life at Insider section on the Careers page"""
        life_element = self.wait.until(EC.presence_of_element_located(self.Life_at_Insider_Section))
        self._scroll_to_element_and_wait(life_element)
        self.wait.until(EC.visibility_of_element_located(self.Life_at_Insider_Section))
        assert life_element.is_displayed(), "Life at Insider section is not visible!"

    def _scroll_to_element_and_wait(self, element):
        """Scrolls to the specified element and waits for a fixed duration
        
        :param WebElement element: The web element to scroll to and make visible in the viewport
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)

   