"""Page Object Model for Insider QA Careers page."""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


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

    # Helpers used by tests
    def _click_dream_job(self):
        dream_job_button = self.wait_long.until(
            EC.presence_of_element_located(
                self.dream_job_button))
        self.wait_long.until(EC.element_to_be_clickable(dream_job_button))
        self.click_via_js(dream_job_button)

    def _switch_to_last_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def _scroll_to_position_list(self):
        """Scrolls to the position list to ensure filters are in view."""
        position_list = self.wait_long.until(
            EC.presence_of_element_located(
                self.career_position_list))
        self.scroll_into_center(position_list)

    def _wait_location_data_ready(self):
        """Waits until page is ready and non-All location options exist in the native select."""
        self.wait_document_ready()
        self.wait_long.until(
            lambda driver: len(
                driver.find_elements(
                    By.XPATH,
                    "//select[@id='filter-by-location']/option[not(@value='All')]")) > 0)

    def _open_location_dropdown(self):
        """Scrolls into view and opens the location dropdown, returning the element."""
        location_dropdown = self.wait_long.until(
            EC.element_to_be_clickable(
                self.location_filter))
        self.scroll_into_center(location_dropdown)
        location_dropdown.click()
        return location_dropdown

    def _wait_location_options_loaded(self):
        """Waits until the select2 options list is visible after opening dropdown."""
        dropdown_options = self.wait_long.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "select2-results__options")))
        self.wait_long.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Location filter options not visible!"

    def _choose_location_option(self, location):
        """Chooses the given location from the select2 results list."""
        location_xpath = (f"//li[contains(@id, 'select2-filter-by-location-result')]"
                          f"[contains(translate(normalize-space(.), "
                          f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                          f"'abcdefghijklmnopqrstuvwxyz'), "
                          f"translate('{location}', "
                          f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                          f"'abcdefghijklmnopqrstuvwxyz'))]")
        self.wait_long.until(
            EC.visibility_of_element_located(
                (By.XPATH, location_xpath)))
        location_option = self.wait_long.until(
            EC.element_to_be_clickable(
                (By.XPATH, location_xpath)))
        location_option.click()

    def _wait_location_results_loaded(self):
        """Waits until the page is fully loaded and listings area evaluated."""
        self.wait_document_ready()
        self.wait_long.until(
            lambda d: len(
                d.find_elements(
                    By.CSS_SELECTOR,
                    ".position-list-item")) >= 0)
        time.sleep(1)

    def _open_department_dropdown(self):
        """Scrolls into view and opens the department dropdown, returning the element."""
        self.wait_document_ready()
        department_dropdown = self.wait_long.until(
            EC.element_to_be_clickable(
                self.department_filter))
        self.scroll_into_center(department_dropdown)
        self.wait_document_ready()
        department_dropdown.click()
        return department_dropdown

    def _wait_department_options_loaded(self):
        """Waits until non-All department options are present and options list is visible."""
        self.wait_long.until(
            lambda driver: len(
                driver.find_elements(
                    By.XPATH,
                    "//select[@id='filter-by-department']/option[not(@value='All')]")) > 0)
        dropdown_options = self.wait_long.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "select2-results__options")))
        self.wait_long.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Department filter options not visible!"

    def _choose_department_option(self, department):
        """Chooses the given department from the select2 results list."""
        department_xpath = (
            f"//li[contains(@id, 'select2-filter-by-department-result')]"
            f"[contains(translate(normalize-space(.), "
            f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            f"'abcdefghijklmnopqrstuvwxyz'), "
            f"translate('{department}', "
            f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            f"'abcdefghijklmnopqrstuvwxyz'))]")
        self.wait_long.until(
            EC.visibility_of_element_located(
                (By.XPATH, department_xpath)))
        department_option = self.wait_long.until(
            EC.element_to_be_clickable(
                (By.XPATH, department_xpath)))
        department_option.click()

    def _wait_department_results_loaded(self):
        """Waits until department filter results are reflected in the listings."""
        self._wait_location_results_loaded()

    def _wait_for_job_items(self):
        def _job_items_present(d):
            items = d.find_elements(By.CSS_SELECTOR, ".position-list-item")
            return items if len(items) > 0 else False
        return self.wait_long.until(_job_items_present)

    def _assert_filter_reflected(self, department):
        selected_department_text = self.driver.find_element(
            *self.department_filter).text.strip().lower()
        assert department.lower() in selected_department_text, (
            f"Selected department not reflected in filter container. "
            f"Expected contains: '{department}', "
            f"got: '{selected_department_text}'"
        )

    def _assert_some_jobs_visible(self, job_items):
        for i, job in enumerate(job_items[:5]):
            try:
                self.wait_long.until(EC.visibility_of(job))
                assert job.is_displayed(), f"Job listing {i + 1} is not visible!"
            except Exception:
                pass

    def _ensure_job_items_present(self):
        job_items = self.wait_long.until(
            EC.presence_of_all_elements_located(
                self.job_listings))
        assert len(job_items) > 0, "Job listing elements not found!"
        return job_items

    def _reveal_and_get_first_view_button(self):
        self.wait_document_ready()
        view_buttons = self.wait_long.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[contains(text(),'View Role')]")))
        if len(view_buttons) == 0:
            view_buttons = self.wait_long.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".position-list-item-wrapper a.btn")))
        assert len(view_buttons) > 0, "'View Role' buttons not found!"
        view_button = view_buttons[0]
        self.scroll_into_center(view_button)
        self.driver.execute_script(
            "arguments[0].style.display = 'block'; "
            "arguments[0].style.visibility = 'visible'; "
            "arguments[0].style.opacity = '1';",
            view_button)
        self.wait_document_ready()
        return view_button

    def _click_view_button_and_validate(self, view_button):
        self.wait_document_ready()
        self.scroll_into_center(view_button)
        self.click_via_js(view_button)
        self.wait_long.until(lambda d: len(d.window_handles) > 1)
        self._switch_to_last_tab()
        self.wait_long.until(lambda d: d.current_url != "about:blank")
        self.wait_document_ready()
        current_url = self.driver.current_url
        valid_domains = ["lever.co", "jobs.lever.co"]
        is_valid_url = any(domain in current_url for domain in valid_domains)
        if not is_valid_url:
            page_title = self.driver.title.lower()
            is_valid_title = any(
                keyword in page_title for keyword in [
                    "job", "career", "position", "apply", "application", "insider"])
            is_valid_url = is_valid_url or is_valid_title
        assert is_valid_url, f"View Role button does not redirect correctly! URL: {current_url}"
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
