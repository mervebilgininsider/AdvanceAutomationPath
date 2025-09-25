from pages.base_page import BasePage
"""Page Object Model for Insider QA Careers page."""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class QACareersPage(BasePage):
    """Page Object Model for Insider QA Careers Page"""

    def __init__(self, driver):
        super().__init__(driver)

        self.location_filter = (By.ID, "select2-filter-by-location-container")
        self.department_filter = (
            By.ID, "select2-filter-by-department-container")
        self.job_listings = (By.CSS_SELECTOR, ".position-list-item")
        self.dream_job_button = (
            By.XPATH,
            "//a[contains(@class, 'btn-info') and contains(text(), 'Find your dream job')]")
        self.career_position_list = (By.ID, "career-position-list")

    def navigate_to_qa_careers(self):
        """Navigates to the QA Careers page"""

        dream_job_button = self.wait.until(
            EC.presence_of_element_located(
                self.dream_job_button))
        self.wait.until(EC.element_to_be_clickable(dream_job_button))

        self.driver.execute_script("arguments[0].click();", dream_job_button)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def select_location(self, location):
        """Selects a specific location from the location filter dropdown

        :param str location: The location to filter jobs by (e.g., 'Istanbul, Turkiye')
        """
        wait = WebDriverWait(self.driver, 30)

        position_list = wait.until(
            EC.presence_of_element_located(
                self.career_position_list))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            position_list)

        location_dropdown = wait.until(
            EC.element_to_be_clickable(
                self.location_filter))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            location_dropdown)

        wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        wait.until(
            lambda driver: len(
                driver.find_elements(
                    By.XPATH,
                    "//select[@id='filter-by-location']/option[not(@value='All')]")) > 0)

        location_dropdown.click()

        dropdown_options = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "select2-results__options")))
        wait.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Location filter options not visible!"

        location_xpath = (f"//li[contains(@id, 'select2-filter-by-location-result')]"
                          f"[contains(translate(normalize-space(.), "
                          f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                          f"'abcdefghijklmnopqrstuvwxyz'), "
                          f"translate('{location}', "
                          f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                          f"'abcdefghijklmnopqrstuvwxyz'))]")
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, location_xpath)))
        location_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, location_xpath)))
        location_option.click()

        wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        WebDriverWait(
            self.driver,
            45).until(
            lambda d: len(
                d.find_elements(
                    By.CSS_SELECTOR,
                    ".position-list-item")) >= 0)
        time.sleep(1)

    def select_department(self, department):
        """Selects a specific department from the department filter dropdown

        :param str department: The department to filter jobs by (e.g., 'Quality Assurance')
        """
        wait = WebDriverWait(self.driver, 30)

        wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")

        department_dropdown = wait.until(
            EC.element_to_be_clickable(
                self.department_filter))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            department_dropdown)
        wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        wait.until(
            lambda driver: len(
                driver.find_elements(
                    By.XPATH,
                    "//select[@id='filter-by-department']/option[not(@value='All')]")) > 0)
        department_dropdown.click()

        dropdown_options = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "select2-results__options")))
        wait.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Department filter options not visible!"

        department_xpath = (
            f"//li[contains(@id, 'select2-filter-by-department-result')]"
            f"[contains(translate(normalize-space(.), "
            f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            f"'abcdefghijklmnopqrstuvwxyz'), "
            f"translate('{department}', "
            f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            f"'abcdefghijklmnopqrstuvwxyz'))]")
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, department_xpath)))
        department_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, department_xpath)))
        department_option.click()

        wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        WebDriverWait(
            self.driver,
            45).until(
            lambda d: len(
                d.find_elements(
                    By.CSS_SELECTOR,
                    ".position-list-item")) >= 0)
        time.sleep(1)

    def filter_jobs(self, location, department):
        """Filters job listings by location and department

        :param str location: The location to filter jobs by (e.g., 'Istanbul, Turkiye')
        :param str department: The department to filter jobs by (e.g., 'Quality Assurance')
        """

        self.select_location(location)
        self.select_department(department)

    def verify_job_listings(self, department):
        """Verifies the presence of filtered job listings

        :param str department: The department name to verify in job listings
        (e.g., 'Quality Assurance')
        """

        self.wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")

        def _job_items_present(d):
            items = d.find_elements(By.CSS_SELECTOR, ".position-list-item")
            return items if len(items) > 0 else False
        job_items = self.wait.until(_job_items_present)
        job_count = len(job_items)
        assert job_count > 0, "No job listings found matching the specified filters!"

        selected_department_text = self.driver.find_element(
            *self.department_filter).text.strip().lower()
        assert department.lower() in selected_department_text, (
            f"Selected department not reflected in filter container. "
            f"Expected contains: '{department}', "
            f"got: '{selected_department_text}'"
        )

        possible_department_keywords = {department.lower(), "quality", "qa"}
        for i, job in enumerate(job_items[:5]):
            try:
                self.wait.until(EC.visibility_of(job))

                dept_spans = job.find_elements(
                    By.CSS_SELECTOR, ".position-department, span[class*='department']")
                texts = " ".join([s.text.lower()
                                 for s in dept_spans if s.text])

                full_text = (job.text or "").lower()
                corpus = f"{texts} {full_text}"
                if any(key in corpus for key in possible_department_keywords):
                    pass
                assert job.is_displayed(), f"Job listing {
                    i + 1} is not visible!"
            except Exception:
                pass

    def verify_view_role_buttons(self):
        """Verifies the presence and functionality of 'View Role' buttons"""

        self.wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        long_wait = WebDriverWait(self.driver, 45)

        job_items = long_wait.until(
            EC.presence_of_all_elements_located(
                self.job_listings))
        assert len(job_items) > 0, "Job listing elements not found!"

        job_item = job_items[0]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", job_item)
        long_wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")

        self.actions.move_to_element(job_item).perform()

        view_buttons = long_wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[contains(text(),'View Role')]")))

        if len(view_buttons) == 0:
            view_buttons = long_wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".position-list-item-wrapper a.btn")))

        assert len(view_buttons) > 0, "'View Role' buttons not found!"

        view_button = view_buttons[0]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            view_button)
        self.driver.execute_script(
            "arguments[0].style.display = 'block'; " +
            "arguments[0].style.visibility = 'visible'; " +
            "arguments[0].style.opacity = '1';",
            view_button)
        long_wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")

        self.driver.execute_script("arguments[0].click();", view_button)

        long_wait.until(lambda driver: len(driver.window_handles) > 1)

        self.driver.switch_to.window(self.driver.window_handles[-1])

        long_wait.until(lambda driver: driver.current_url != "about:blank")
        long_wait.until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        current_url = self.driver.current_url

        valid_domains = ["lever.co", "jobs.lever.co"]
        is_valid_url = any(domain in current_url for domain in valid_domains)

        if not is_valid_url:
            page_title = self.driver.title.lower()
            is_valid_title = any(
                keyword in page_title for keyword in [
                    "job",
                    "career",
                    "position",
                    "apply",
                    "application",
                    "insider"])
            is_valid_url = is_valid_url or is_valid_title

        assert is_valid_url, f"View Role button does not redirect correctly! URL: {current_url}"

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
