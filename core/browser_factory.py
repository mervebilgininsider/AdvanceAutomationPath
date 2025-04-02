from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os

class BrowserFactory:
    """WebDriver yöneten sınıf."""

    @staticmethod
    def get_driver(browser_name="chrome"):
        """Parametre olarak verilen tarayıcı için WebDriver'ı başlatır ve ayarları uygular.
        
        Args:
            browser_name (str): Kullanılacak tarayıcı adı ('chrome' veya 'firefox')
            
        Returns:
            WebDriver: Ayarlanmış tarayıcı sürücüsü
        """
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            chrome_options = ChromeOptions()

            # Push Notification'ı Devre Dışı Bırak
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)

            # WebDriver Başlat
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        elif browser_name == "firefox":
            firefox_options = FirefoxOptions()
            
            # Firefox için gerekli ayarlar
            firefox_options.set_preference("dom.webnotifications.enabled", False)
            
            # WebDriver Başlat
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        
        else:
            raise ValueError(f"Desteklenmeyen tarayıcı: {browser_name}. Desteklenen tarayıcılar: 'chrome', 'firefox'")
        
        driver.maximize_window()
        return driver

    @staticmethod
    def capture_screenshot(driver, test_name):
        """Test başarısız olursa ekran görüntüsü alır ve reports klasörüne kaydeder."""
        import pytest
        import datetime
        
        # Pytest tarafından oluşturulan screenshots_dir'i kullan
        # Eğer tanımlı değilse varsayılan olarak reports klasörünü kullan
        screenshots_dir = getattr(pytest, "screenshots_dir", None)
        
        if screenshots_dir is None:
            # Eğer pytest tarafından screenshots_dir tanımlanmamışsa
            # Tarih ve saat bilgisini al ve yeni bir klasör oluştur
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            screenshots_dir = os.path.join("reports", f"test_run_{timestamp}")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
        
        # Ekran görüntüsünü kaydet
        screenshot_path = os.path.join(screenshots_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Ekran görüntüsü kaydedildi: {screenshot_path}")
        
        # HTML rapora eklemek için ekran görüntüsünün göreceli yolunu döndür
        return screenshot_path
