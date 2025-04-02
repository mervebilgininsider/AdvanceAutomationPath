import sys
import os
import pytest
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

# Komut satırı parametresi ekliyoruz - tarayıcı seçimi için
def pytest_addoption(parser):
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Testlerin çalıştırılacağı tarayıcı: chrome veya firefox"
    )

# HTML rapor oluşturma için yapılandırma
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.extra = getattr(report, "extra", [])
    setattr(item, f"rep_{report.when}", report)
    
    # Test başarısız olduğunda ekran görüntüsünü rapora ekle
    if report.when == "call" and report.failed:
        # Ekran görüntüsü ekleme işlemi test_insider_careers.py içinde yapılıyor
        pass

# Her test çalıştığında benzersiz bir rapor klasörü oluştur
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Tarih ve saat bilgisini al
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Test oturumu için benzersiz bir klasör oluştur
    session_dir = os.path.join('reports', f'test_run_{timestamp}')
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    # HTML rapor dosyasının yolunu ayarla
    config.option.htmlpath = os.path.join(session_dir, 'report.html')
    
    # Ekran görüntüleri için klasör yolunu kaydet
    pytest.screenshots_dir = session_dir
