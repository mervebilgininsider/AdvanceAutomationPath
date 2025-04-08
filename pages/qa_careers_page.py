from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging

logger = logging.getLogger(__name__)

class QACareersPage:
    """Page Object Model for Insider QA Careers Page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.actions = ActionChains(driver)
        
        self.location_filter = (By.ID, "select2-filter-by-location-container")
        self.department_filter = (By.ID, "select2-filter-by-department-container")
        self.job_listings = (By.CSS_SELECTOR, ".position-list-item")
        self.view_role_buttons = (By.XPATH, "//a[contains(text(),'View Role')]")
        self.open_positions_link = (By.LINK_TEXT, "See all QA jobs")
        self.dream_job_button = (By.XPATH, "//a[contains(@class, 'btn-info') and contains(text(), 'Find your dream job')]")

    def navigate_to_qa_careers(self):
        """Navigates to the QA Careers page"""
        logger.info("Step 5: Navigating to QA Careers page")
        
        dream_job_button = self.wait.until(EC.presence_of_element_located(self.dream_job_button))
        self.wait.until(EC.element_to_be_clickable(dream_job_button))
        
        self.driver.execute_script("arguments[0].click();", dream_job_button)
        logger.info("Clicked 'Find your dream job' button")

        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("Successfully navigated to QA Careers page")

        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info("QA Careers page loaded successfully")
        
    def filter_jobs(self, location, department):
        """Filters job listings by location and department"""
        logger.info(f"Step 6: Filtering job listings - Location: {location}, Department: {department}")
        wait = WebDriverWait(self.driver, 30)
        
        logger.info("Step 6.1: Selecting location filter")
        location_dropdown = wait.until(EC.element_to_be_clickable(self.location_filter))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_dropdown)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        wait.until(lambda driver: len(driver.find_elements(By.XPATH, "//select[@id='filter-by-location']/option[not(@value='All')]")) > 0)
        logger.info("Location filter options loaded")
        
        location_dropdown.click()
        logger.info("Location filter dropdown opened")
        
        dropdown_options = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options")))
        wait.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Location filter options not visible!"
        
        location_xpath = f"//li[contains(@id, 'select2-filter-by-location-result') and contains(text(), '{location}')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, location_xpath)))
        location_option = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
        location_option.click()
        logger.info(f"Location filter selected: {location}")
        
        logger.info("Step 6.2: Selecting department filter")
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        department_dropdown = wait.until(EC.element_to_be_clickable(self.department_filter))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", department_dropdown)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        wait.until(lambda driver: len(driver.find_elements(By.XPATH, "//select[@id='filter-by-department']/option[not(@value='All')]")) > 0)
        logger.info("Department filter options loaded")
        
        department_dropdown.click()
        logger.info("Department filter dropdown opened")
        
        dropdown_options = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options")))
        wait.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Department filter options not visible!"
        
        department_xpath = f"//li[contains(@id, 'select2-filter-by-department-result') and contains(text(), '{department}')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, department_xpath)))
        department_option = wait.until(EC.element_to_be_clickable((By.XPATH, department_xpath)))
        department_option.click()
        logger.info(f"Department filter selected: {department}")

    def verify_job_listings(self, department):
        """Verifies the presence of filtered job listings"""
        logger.info("Step 7: Verifying filtered job listings")
        
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        long_wait = WebDriverWait(self.driver, 45)
        
        department_selector = (By.XPATH, f"//div[@id='jobs-list']//span[contains(@class, 'position-department') and contains(text(), '{department}')]")
        long_wait.until(EC.presence_of_element_located(department_selector))
        logger.info(f"Selected department '{department}' displayed in job list")
        
        job_items = self.wait.until(EC.presence_of_all_elements_located(self.job_listings))
        job_count = len(job_items)
        assert job_count > 0, "No job listings found matching the specified filters!"
        logger.info(f"Found {job_count} job listings matching the filters")
        
        for i, job in enumerate(job_items[:3]):
            self.wait.until(EC.visibility_of(job))
            assert job.is_displayed(), f"Job listing {i+1} is not visible!"
            logger.info(f"Job listing {i+1} displayed successfully")

    def verify_view_role_buttons(self):
        """Verifies the presence and functionality of 'View Role' buttons"""
        logger.info("Step 8: Verifying 'View Role' buttons")
        
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        long_wait = WebDriverWait(self.driver, 45)
        
        job_items = long_wait.until(EC.presence_of_all_elements_located(self.job_listings))
        assert len(job_items) > 0, "Job listing elements not found!"
        logger.info(f"Found {len(job_items)} job listing elements")
        
        job_item = job_items[0]
        logger.info(f"Found {len(job_items)} job listing elements - {job_item}")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_item)
        long_wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        self.actions.move_to_element(job_item).perform()
        logger.info("Hovered over job listing")
        
        view_buttons = long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(),'View Role')]")))
        
        if len(view_buttons) == 0:
            view_buttons = long_wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".position-list-item-wrapper a.btn")))
        
        assert len(view_buttons) > 0, "'View Role' buttons not found!"
        logger.info(f"Found {len(view_buttons)} 'View Role' buttons")
        
        view_button = view_buttons[0]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
        self.driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible'; arguments[0].style.opacity = '1';", view_button)
        long_wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        logger.info("Step 8.1: Clicking 'View Role' button")
        self.driver.execute_script("arguments[0].click();", view_button)
        
        logger.info("Step 8.2: Waiting for new tab to open")
        long_wait.until(lambda driver: len(driver.window_handles) > 1)
        
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        long_wait.until(lambda driver: driver.current_url != "about:blank")
        long_wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        current_url = self.driver.current_url
        logger.info(f"Page loaded: {current_url}")
        
        valid_domains = ["lever.co", "jobs.lever.co"]
        is_valid_url = any(domain in current_url for domain in valid_domains)
        
        if not is_valid_url:
            page_title = self.driver.title.lower()
            is_valid_title = any(keyword in page_title for keyword in ["job", "career", "position", "apply", "application", "insider"])
            is_valid_url = is_valid_url or is_valid_title
        
        assert is_valid_url, f"View Role button does not redirect correctly! URL: {current_url}"
        logger.info(f"View Role button verified successfully. URL: {current_url}")
        
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
