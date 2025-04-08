from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger(__name__)

class CareersPage:
    """Page Object Model for Insider Careers Page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        self.locations_section = (By.ID, "career-our-location")
        self.teams_section = (By.XPATH, "//section[@data-id='a8e7b90']")
        self.life_at_insider_section = (By.ID, "find-job-widget")

    def verify_sections(self):
        """Verifies the visibility of specified sections on the Careers page"""
        logger.info("Step 4: Verifying Careers page sections")
        
        logger.info("Step 4.1: Verifying Locations section")
        locations_element = self.wait.until(EC.presence_of_element_located(self.locations_section))
        self._scroll_to_element_and_wait(locations_element)
        self.wait.until(EC.visibility_of_element_located(self.locations_section))
        assert locations_element.is_displayed(), "Locations section is not visible!"
        logger.info("Locations section displayed successfully")
        
        logger.info("Step 4.2: Verifying Teams section")
        teams_element = self.wait.until(EC.presence_of_element_located(self.teams_section))
        self._scroll_to_element_and_wait(teams_element)
        self.wait.until(EC.visibility_of_element_located(self.teams_section))
        assert teams_element.is_displayed(), "Teams section is not visible!"
        logger.info("Teams section displayed successfully")
        
        logger.info("Step 4.3: Verifying Life at Insider section")
        life_element = self.wait.until(EC.presence_of_element_located(self.life_at_insider_section))
        self._scroll_to_element_and_wait(life_element)
        self.wait.until(EC.visibility_of_element_located(self.life_at_insider_section))
        assert life_element.is_displayed(), "Life at Insider section is not visible!"
        logger.info("Life at Insider section displayed successfully")

    def _scroll_to_element_and_wait(self, element):
        """Scrolls to the specified element and waits for a fixed duration"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)

   