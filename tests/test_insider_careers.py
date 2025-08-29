"""
Test case is:

1. Home Page Operations
   1.1. Accept cookies
   1.2. Navigate to Careers page

2. Careers Page Verification
   2.1. Verify Locations section
   2.2. Verify Teams section
   2.3. Verify Life at Insider section

3. QA Careers Page Operations
   3.1. Navigate to QA Careers page
   3.2. Filter jobs by location and department
   3.3. Verify filtered job listings
   3.4. Verify 'View Role' buttons
"""
import logging
from tests.basetest import BaseTest
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
logger = logging.getLogger(__name__)

class TestInsiderCareers(BaseTest):
    def test_insider_careers(self):
        logger.info("Starting Insider Careers test workflow")

        # Step 1: Home Page Operations (setup_method ile zaten açıldı ve kontrol edildi)
        logger.info("Step 1: Home Page Operations")
        self.home_page.accept_cookies()
        self.home_page.navigate_to_careers()

        # Step 2: Careers Page Verification
        logger.info("Step 2: Careers Page Verification")
        careers_page = CareersPage(self.driver)
        careers_page.verify_sections()

        # Step 3: QA Careers Page Operations
        logger.info("Step 3: QA Careers Page Operations")
        qa_careers_page = QACareersPage(self.driver)
        qa_careers_page.navigate_to_qa_careers()
        qa_careers_page.filter_jobs("Istanbul, Turkiye", "Quality Assurance")
        qa_careers_page.verify_job_listings("Quality Assurance")
        qa_careers_page.verify_view_role_buttons()
        
        logger.info("Insider Careers test workflow completed successfully")
