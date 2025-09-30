"""Base test class for common test setup and teardown."""

import traceback
import logging
import pytest
from helpers.driver_manager import DriverManager
from helpers.test_helper import TestHelper
from pages.home_page import HomePage
logger = logging.getLogger(__name__)

class BaseTest:
    """Base test class for common test setup and teardown."""
    driver = None
    home_page = None
    _request = None

    @pytest.fixture(autouse=True)
    def inject_request(self, request):
        """Injects pytest request fixture into the test instance."""
        self._request = request

    def setup_method(self, method):
        """Sets up the test environment."""
        self.driver = DriverManager.get_driver()
        self.home_page = HomePage(self.driver)
        try:
            self.home_page.open_page("https://useinsider.com/")
        except Exception as e:
            print(traceback.format_exc())
            pytest.skip(f"Ana sayfa yüklenemedi, test başlatılamıyor: {e}")

    def teardown_method(self, method):
        """Tears down the test environment."""
        request = self._request

        screenshot_path = TestHelper.capture_screenshot(
            self.driver, request.node.name)
        TestHelper.add_screenshot_to_report(request, screenshot_path)

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            logger.error(
                "Test execution failed. Screenshot captured and saved at: %s", screenshot_path)
        DriverManager.quit_driver(self.driver)
