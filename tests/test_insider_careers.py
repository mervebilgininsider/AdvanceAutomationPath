# pylint: disable=protected-access
"""Test cases for Insider Careers page automation."""

import logging
from selenium.webdriver.common.by import By
from tests.basetest import BaseTest
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
logger = logging.getLogger(__name__)

""" Test case is:

    1. Accept cookies
    2. Navigate to Careers page
    3. Verify Locations section
    4. Verify Teams section
    5. Verify Life at Insider section
    6. Navigate to QA Careers page
    7. Filter jobs by location and department
    8. Verify filtered job listings
    9. Verify 'View Role' buttons

"""

class TestInsiderCareers(BaseTest):
    """Test class for Insider Careers page automation workflow."""
    def test_insider_careers(self):
        """Test the complete Insider Careers workflow from homepage to job filtering."""
        logger.info("Starting Insider Careers test workflow")

        logger.info("1. Accept cookies")
        self.home_page.accept_cookies()
        logger.info("Cookies accepted or not visible")

        logger.info("2. Navigate to Careers page")
        self.home_page.close_push_notification()
        self.home_page.handle_agent_one_popup()
        self.home_page.hover_company_menu()
        self.home_page.handle_agent_one_popup()
        self.home_page.click_careers_link()
        self.home_page.switch_to_new_window()
        careers_page = CareersPage(self.driver)
        logger.info("Careers page navigated")

        logger.info("3. Verify Locations section")
        careers_page.verify_locations_section()
        logger.info("Locations section verified")

        logger.info("4. Verify Teams section")
        careers_page.verify_teams_section()
        logger.info("Teams section verified")

        logger.info("5. Verify Life at Insider section")
        careers_page.verify_life_at_insider_section()
        logger.info("Life at Insider section verified")

        logger.info("6. Navigate to QA Careers page")
        qa_careers_page = QACareersPage(self.driver)
        qa_careers_page._click_dream_job()
        qa_careers_page._switch_to_last_tab()
        qa_careers_page.wait_until_visible((By.TAG_NAME, "body"))
        logger.info("QA Careers page navigated")

        logger.info("7. Filter jobs by location and department")
        qa_careers_page._scroll_to_position_list()
        qa_careers_page._wait_location_data_ready()
        qa_careers_page._open_location_dropdown()
        qa_careers_page._wait_location_options_loaded()
        qa_careers_page._choose_location_option("Istanbul, Turkiye")
        qa_careers_page._wait_location_results_loaded()
        qa_careers_page._open_department_dropdown()
        qa_careers_page._wait_department_options_loaded()
        qa_careers_page._choose_department_option("Quality Assurance")
        qa_careers_page._wait_department_results_loaded()
        logger.info("Jobs filtered by location and department")

        logger.info("8. Verify filtered job listings")
        job_items = qa_careers_page._wait_for_job_items()
        qa_careers_page._assert_filter_reflected("Quality Assurance")
        qa_careers_page._assert_some_jobs_visible(job_items)
        logger.info("Filtered job listings verified")

        logger.info("9. Verify 'View Role' buttons")
        qa_careers_page.wait_document_ready()
        job_items = qa_careers_page._ensure_job_items_present()
        qa_careers_page.scroll_into_center(job_items[0])
        qa_careers_page.actions.move_to_element(job_items[0]).perform()
        view_button = qa_careers_page._reveal_and_get_first_view_button()
        qa_careers_page._click_view_button_and_validate(view_button)
        logger.info("'View Role' buttons verified")

        logger.info("Insider Careers test workflow completed successfully")
