import os
import logging
import pytest
from datetime import datetime
from pytest_html.extras import image, html

logger = logging.getLogger(__name__)

class TestHelper:
    """Provides helper methods for test operations"""
    
    @staticmethod
    def capture_screenshot(driver, test_name):
        """Captures a screenshot and saves it to the screenshots directory"""
        screenshots_dir = getattr(pytest, "screenshots_dir", "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot captured and saved to: {screenshot_path}")
        return screenshot_path

    @staticmethod
    def add_screenshot_to_report(request, screenshot_path):
        """Adds screenshot to HTML report"""
        if hasattr(request.node, "rep_call"):
            request.node.rep_call.extra = [
                image(screenshot_path),
                html(f"<div>Screenshot: <a href='{screenshot_path}'>{request.node.name}.png</a></div>")
            ]

    @staticmethod
    def handle_test_failure(request, driver):
        """Handles test failure by capturing screenshot and adding to report"""
        if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
            screenshot_path = TestHelper.capture_screenshot(driver, request.node.name)
            TestHelper.add_screenshot_to_report(request, screenshot_path)
            logger.error(f"Test execution failed. Screenshot captured and saved at: {screenshot_path}") 