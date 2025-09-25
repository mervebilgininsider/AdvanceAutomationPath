"""Helper utilities for screenshots and pytest-html report attachments."""

import os
import logging
from datetime import datetime
from pytest_html.extras import image, html

logger = logging.getLogger(__name__)


class TestHelper:
    """Provides helper methods for test operations"""

    @staticmethod
    def capture_screenshot(driver, test_name):
        """
        Captures a screenshot and saves it to the screenshots directory.

        :param WebDriver driver: The Selenium WebDriver instance used to capture the screenshot
        :param str test_name: The name of the test to use in the screenshot filename
        :return: The path to the saved screenshot
        :rtype: str
        """
        screenshots_dir = os.environ.get("SCREENSHOT_DIR", "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(
            screenshots_dir, f"{test_name}_{timestamp}.png")
        try:
            driver.save_screenshot(screenshot_path)
            logger.info("Screenshot captured and saved to: %s", screenshot_path)
        except Exception as e:
            logger.error("Screenshot could not be captured: %s", e)
        return screenshot_path

    @staticmethod
    def add_screenshot_to_report(request, screenshot_path):
        """
        Adds screenshot to HTML report.

        :param pytest.FixtureRequest request: The pytest request object to attach the screenshot to
        :param str screenshot_path: The file path of the screenshot to add to the report
        """
        if hasattr(request.node, "rep_call"):
            rel_path = os.path.relpath(
                screenshot_path, start=os.path.dirname(
                    request.config.option.htmlpath))
            request.node.rep_call.extra = getattr(
                request.node.rep_call, "extra", []) + [
                image(rel_path), html(
                    f"<div>Screenshot: <a href='{rel_path}'>{
                        request.node.name}.png</a></div>")]

    @staticmethod
    def handle_test_failure(request, driver):
        """Handles test failure by capturing screenshot and adding to report

        :param pytest.FixtureRequest request: The pytest request object containing test information
        :param WebDriver driver: The Selenium WebDriver instance used for the test
        """
        if request.node.rep_call.failed if hasattr(
                request.node, "rep_call") else False:
            screenshot_path = TestHelper.capture_screenshot(
                driver, request.node.name)
            TestHelper.add_screenshot_to_report(request, screenshot_path)
            logger.error("Test execution failed. Screenshot captured and saved at: %s",
                screenshot_path)
