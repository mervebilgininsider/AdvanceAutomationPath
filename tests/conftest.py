"""Pytest configuration and fixtures for test automation."""

import sys
import os
import datetime
import logging
import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Adds command line option for browser selection

    :param pytest.Parser parser: The pytest command line parser to add options to
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox"
    )
    parser.addoption(
        "--screenshots-dir",
        action="store",
        default=None,
        help="Directory to store screenshots"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, _):
    """Configures HTML report generation

    :param pytest.Item item: The test item being executed
    :param pytest.CallInfo call: The call info for the current test phase
    """
    outcome = yield
    report = outcome.get_result()
    report.extra = getattr(report, "extra", [])
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        pass


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Creates a unique report directory for each test run"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    session_dir = os.path.join('reports', f'test_run_{timestamp}')
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    config.option.htmlpath = os.path.join(session_dir, 'report.html')

    screenshots_dir = os.path.join(session_dir, "screenshots")
    pytest.screenshots_dir = screenshots_dir
    pytest.report_dir = session_dir

    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
