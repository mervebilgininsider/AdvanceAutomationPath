import pytest
from helpers.driver_manager import DriverManager
from helpers.test_helper import TestHelper
from pages.home_page import HomePage
import logging

class BaseTest:
    driver = None
    home_page = None
    _request = None

    @pytest.fixture(autouse=True)
    def inject_request(self, request):
        self._request = request

    def setup_method(self, method):
        logger = logging.getLogger(__name__)
        self.driver = DriverManager.get_driver()
        self.home_page = HomePage(self.driver)
        try:
            self.home_page.open_page("https://useinsider.com/")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            pytest.skip(f"Ana sayfa yüklenemedi, test başlatılamıyor: {e}")

    def teardown_method(self, method):
        logger = logging.getLogger(__name__)
        request = self._request
        # Her durumda ekran görüntüsü al ve rapora ekle
        screenshot_path = TestHelper.capture_screenshot(self.driver, request.node.name)
        TestHelper.add_screenshot_to_report(request, screenshot_path)
        # Fail durumunda sadece logla
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            logger.error(f"Test execution failed. Screenshot captured and saved at: {screenshot_path}")
        DriverManager.quit_driver(self.driver, request.node.name) 