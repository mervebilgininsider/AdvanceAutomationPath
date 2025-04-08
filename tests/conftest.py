import sys
import os
import pytest
import datetime
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

# Configure logging
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
    """Adds command line option for browser selection"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Browser to run tests on: chrome or firefox"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Configures HTML report generation"""
    outcome = yield
    report = outcome.get_result()
    report.extra = getattr(report, "extra", [])
    setattr(item, f"rep_{report.when}", report)
    
    if report.when == "call" and report.failed:
        # Screenshot capture is handled in test_insider_careers.py
        pass

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Creates a unique report directory for each test run"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    
    session_dir = os.path.join('reports', f'test_run_{timestamp}')
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    config.option.htmlpath = os.path.join(session_dir, 'report.html')
    pytest.screenshots_dir = session_dir
