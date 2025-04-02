import pytest
import os
from core.browser_factory import BrowserFactory
from pages import qa_careers_page
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
from pytest_html.extras import image, html

@pytest.fixture(scope="function")
def driver(request):
    # Tarayıcı parametresini al, varsayılan olarak Chrome kullan
    browser = request.config.getoption("--browser", default="chrome")
    driver = BrowserFactory.get_driver(browser)
    
    # Test adını al (hata durumunda ekran görüntüsü için)
    test_name = request.node.name
    
    yield driver
    
    # Test başarısız olduysa ekran görüntüsü al ve HTML rapora ekle
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot_path = BrowserFactory.capture_screenshot(driver, test_name)
        
        # HTML rapora ekran görüntüsünü ekle
        if hasattr(request.node, "rep_call"):
            request.node.rep_call.extra = [
                image(screenshot_path),
                html(f"<div>Ekran görüntüsü: <a href='{screenshot_path}'>{test_name}.png</a></div>")
            ]
        
    driver.quit()

# pytest_runtest_makereport fonksiyonu ile test sonucunu yakalıyoruz
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def test_insider_careers(driver):
    home_page = HomePage(driver)
    home_page.open_homepage()
    home_page.accept_cookies()
    home_page.navigate_to_careers()

    careers_page = CareersPage(driver)
    careers_page.verify_sections()

    qa_careers_page = QACareersPage(driver)
    qa_careers_page.navigate_to_qa_careers()
    qa_careers_page.go_to_open_positions()
    qa_careers_page.filter_jobs("Istanbul, Turkiye","Quality Assurance")
    qa_careers_page.verify_job_listings("Quality Assurance")
    qa_careers_page.verify_view_role_buttons()
