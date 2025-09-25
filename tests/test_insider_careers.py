"""Test cases for Insider Careers page automation."""

import logging
from tests.basetest import BaseTest
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
logger = logging.getLogger(__name__)

"""
Test case is:

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
        self.home_page.navigate_to_careers()
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
        qa_careers_page.navigate_to_qa_careers()
        logger.info("QA Careers page navigated")

        logger.info("7. Filter jobs by location and department")
        qa_careers_page.filter_jobs("Istanbul, Turkiye", "Quality Assurance")
        logger.info("Jobs filtered by location and department")

        logger.info("8. Verify filtered job listings")
        qa_careers_page.verify_job_listings("Quality Assurance")
        logger.info("Filtered job listings verified")

        logger.info("9. Verify 'View Role' buttons")
        qa_careers_page.verify_view_role_buttons()
        logger.info("'View Role' buttons verified")

        logger.info("Insider Careers test workflow completed successfully")
