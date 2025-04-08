import pytest
import os
import logging
from core.browser_factory import BrowserFactory
from pages import qa_careers_page
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
from pytest_html.extras import image, html

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver(request):
    """Creates and manages the WebDriver instance for each test"""
    browser = request.config.getoption("--browser", default="chrome")
    logger.info(f"Initializing {browser} browser")
    driver = BrowserFactory.get_driver(browser)
    test_name = request.node.name
    
    yield driver
    
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot_path = BrowserFactory.capture_screenshot(driver, test_name)
        logger.error(f"Test failed. Screenshot saved at: {screenshot_path}")
        
        if hasattr(request.node, "rep_call"):
            request.node.rep_call.extra = [
                image(screenshot_path),
                html(f"<div>Screenshot: <a href='{screenshot_path}'>{test_name}.png</a></div>")
            ]
        
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures test results for reporting"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def test_insider_careers(driver):
    """Tests the Insider Careers workflow"""
    logger.info("Starting Insider Careers test workflow")
    
    # Step 1: Home Page Operations
    logger.info("Step 1: Home Page Operations")
    home_page = HomePage(driver)
    home_page.open_homepage()
    home_page.accept_cookies()
    home_page.navigate_to_careers()

    # Step 2: Careers Page Verification
    logger.info("Step 2: Careers Page Verification")
    careers_page = CareersPage(driver)
    careers_page.verify_sections()

    # Step 3: QA Careers Page Operations
    logger.info("Step 3: QA Careers Page Operations")
    qa_careers_page = QACareersPage(driver)
    qa_careers_page.navigate_to_qa_careers()
    qa_careers_page.go_to_open_positions()
    qa_careers_page.filter_jobs("Istanbul, Turkiye","Quality Assurance")
    qa_careers_page.verify_job_listings("Quality Assurance")
    qa_careers_page.verify_view_role_buttons()
    
    logger.info("Insider Careers test workflow completed successfully")
