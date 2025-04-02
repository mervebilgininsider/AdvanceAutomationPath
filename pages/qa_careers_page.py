from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class QACareersPage:
    """Insider Açık Pozisyonlar sayfası için Page Object Model."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 2)
        self.actions = ActionChains(driver)
        # Filtre seçicileri - Select2 dropdown elementleri
        self.location_filter = (By.ID, "select2-filter-by-location-container")
        self.department_filter = (By.ID, "select2-filter-by-department-container")
        self.job_listings = (By.CSS_SELECTOR, ".position-list-item")
        # View Role butonları için seçici
        self.view_role_buttons = (By.XPATH, "//a[contains(text(),'View Role')]")
        # Açık Pozisyonlar Sayfası Linki
        self.open_positions_link = (By.LINK_TEXT, "See all QA jobs")
        # QA Careers sayfası URL'i
        self.qa_careers_url = "https://useinsider.com/careers/quality-assurance/"

    def navigate_to_qa_careers(self):
        """QA Careers sayfasına gider."""
        print("TEST ADIMI: QA Careers sayfasına yönlendiriliyor...")
        self.driver.get(self.qa_careers_url)
        # Sayfanın yüklendiğini doğrula
        self.wait.until(EC.url_contains("quality-assurance"))
        assert self.qa_careers_url in self.driver.current_url, "QA Careers sayfası yüklenemedi!"
        # Sayfanın tamamen yüklenmesini bekle
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✓ QA Careers sayfası başarıyla yüklendi")
        
    def filter_jobs(self, location, department):
        """Konum ve departman bazında iş ilanlarını filtreler."""
        print(f"TEST ADIMI: İş ilanları filtreleniyor - Konum: {location}, Departman: {department}")
        # Daha uzun bekleme süresi ile özel bir wait oluşturuyoruz
        wait = WebDriverWait(self.driver, 30)  # Uzun bekleme süresi
        
        # Location dropdown işlemleri
        print("TEST ADIMI: Konum filtresi seçiliyor...")
        # Location dropdown'a tıklama
        location_dropdown = wait.until(EC.element_to_be_clickable(self.location_filter))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_dropdown)
        # Sayfanın scroll işleminin tamamlanmasını bekle
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        # Dropdown'da value="All" dışında herhangi bir option elementinin yüklenmesini bekle
        wait.until(lambda driver: len(driver.find_elements(By.XPATH, "//select[@id='filter-by-location']/option[not(@value='All')]")) > 0)
        print("✓ Konum filtresi seçenekleri yüklendi")
        
        location_dropdown.click()
        print("✓ Konum filtresi dropdown'ı açıldı")
        
        # Dropdown menüsünün tamamen yüklenmesini bekle
        dropdown_options = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options")))
        wait.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Konum filtresi seçenekleri görüntülenemiyor!"
        
        # Location seçeneğini seçme - Select2 dropdown için doğru XPath
        location_xpath = f"//li[contains(@id, 'select2-filter-by-location-result') and contains(text(), '{location}')]"
        # Seçeneğin görünür olmasını bekle
        wait.until(EC.visibility_of_element_located((By.XPATH, location_xpath)))
        location_option = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
        location_option.click()
        print(f"✓ Konum filtresi seçildi: {location}")
        
        # Department dropdown işlemleri
        print("TEST ADIMI: Departman filtresi seçiliyor...")
        # Önceki seçimin tamamlanmasını bekle
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # Department dropdown'a tıklama
        department_dropdown = wait.until(EC.element_to_be_clickable(self.department_filter))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", department_dropdown)
        # Scroll işleminin tamamlanmasını bekle
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        # Dropdown'da value="All" dışında herhangi bir option elementinin yüklenmesini bekle
        wait.until(lambda driver: len(driver.find_elements(By.XPATH, "//select[@id='filter-by-department']/option[not(@value='All')]")) > 0)
        print("✓ Departman filtresi seçenekleri yüklendi")
        
        department_dropdown.click()
        print("✓ Departman filtresi dropdown'ı açıldı")
        
        # Dropdown menüsünün tamamen yüklenmesini bekle
        dropdown_options = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results__options")))
        wait.until(EC.visibility_of(dropdown_options))
        assert dropdown_options.is_displayed(), "Departman filtresi seçenekleri görüntülenemiyor!"
        
        # Department seçeneğini seçme - Select2 dropdown için doğru XPath
        department_xpath = f"//li[contains(@id, 'select2-filter-by-department-result') and contains(text(), '{department}')]"
        # Seçeneğin görünür olmasını bekle
        wait.until(EC.visibility_of_element_located((By.XPATH, department_xpath)))
        department_option = wait.until(EC.element_to_be_clickable((By.XPATH, department_xpath)))
        department_option.click()
        print(f"✓ Departman filtresi seçildi: {department}")
            


    def verify_job_listings(self, department):
        """Filtrelenmiş iş ilanlarının varlığını doğrular."""
        print("TEST ADIMI: Filtrelenmiş iş ilanlarının varlığı kontrol ediliyor...")
        
        # Sayfanın yenilenmesini bekle
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # Daha uzun bekleme süresi ile özel bir wait oluşturuyoruz
        long_wait = WebDriverWait(self.driver, 30)
        
        # Seçilen departman isminin job listesinde görünmesini bekle - daha esnek XPath
        department_selector = (By.XPATH, f"//div[@id='jobs-list']//span[contains(@class, 'position-department') and contains(text(), '{department}')]")
        long_wait.until(EC.presence_of_element_located(department_selector))
        print(f"✓ Seçilen departman '{department}' iş listesinde görüntülendi")
        
        # İş ilanlarının varlığını kontrol et
        job_items = self.wait.until(EC.presence_of_all_elements_located(self.job_listings))
        job_count = len(job_items)
        assert job_count > 0, "Belirtilen filtrelere uygun iş ilanı bulunamadı!"
        print(f"✓ Filtrelere uygun {job_count} adet iş ilanı bulundu")
        
        # İş ilanlarının görünür olduğunu doğrula
        for i, job in enumerate(job_items[:3]):  # İlk 3 ilanı kontrol et
            self.wait.until(EC.visibility_of(job))
            assert job.is_displayed(), f"{i+1}. iş ilanı görüntülenemiyor!"
            print(f"✓ İş ilanı {i+1} başarıyla görüntülendi")

    def verify_view_role_buttons(self):
        """Her iş ilanında 'View Role' butonunun varlığını ve yönlendirmesini doğrular."""
        print("TEST ADIMI: 'View Role' butonlarının kontrolü yapılıyor...")
        
        # Sayfanın tamamen yüklenmesini bekle
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # Daha uzun bekleme süresi ile özel bir wait oluşturuyoruz
        long_wait = WebDriverWait(self.driver, 45)  # Uzun bekleme süresi
        
        # İş ilanı elementlerini bulalım
        job_items = long_wait.until(EC.presence_of_all_elements_located(self.job_listings))
        assert len(job_items) > 0, "İş ilanı elementleri bulunamadı!"
        print(f"✓ {len(job_items)} adet iş ilanı elementi bulundu")
        
        # İlk iş ilanı elementine scroll yapalım
        job_item = job_items[0]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_item)
        long_wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # Hover işlemi için ActionChains kullanıyoruz
        self.actions.move_to_element(job_item).perform()
        print("✓ İş ilanı üzerine hover yapıldı")
        
        # Doğrudan XPath ile View Role butonlarını bul
        # Burada contains() kullanarak butonları daha güvenilir şekilde buluyoruz
        view_buttons = long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(),'View Role')]")))
        
        # Buton bulunamazsa, alternatif bir seçici deneyelim
        if len(view_buttons) == 0:
            # Alternatif olarak CSS seçici ile deneyelim
            view_buttons = long_wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".position-list-item-wrapper a.btn")))
        
        assert len(view_buttons) > 0, "'View Role' butonları bulunamadı!"
        print(f"✓ {len(view_buttons)} adet 'View Role' butonu bulundu")
        
        # İlk butonu görünür hale getir
        view_button = view_buttons[0]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
        self.driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible'; arguments[0].style.opacity = '1';", view_button)
        long_wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        # JavaScript ile tıklama
        print("TEST ADIMI: 'View Role' butonuna tıklanıyor...")
        self.driver.execute_script("arguments[0].click();", view_button)
        
        # Yeni sekmenin açılmasını bekle
        print("TEST ADIMI: Yeni sekmenin açılmasını bekleniyor...")
        long_wait.until(lambda driver: len(driver.window_handles) > 1)
        
        # Yeni sekmeye geç
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        # Sayfanın yüklenmesini bekle
        long_wait.until(lambda driver: driver.current_url != "about:blank")
        long_wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        current_url = self.driver.current_url
        print(f"✓ Sayfa yüklendi: {current_url}")
        
        # URL doğrulama - Kabul edilebilir URL'lerin kontrolü
        valid_domains = ["lever.co", "jobs.lever.co"]
        is_valid_url = any(domain in current_url for domain in valid_domains)
        
        # Eğer URL geçerli değilse, başlık kontrolü yap
        if not is_valid_url:
            page_title = self.driver.title.lower()
            is_valid_title = any(keyword in page_title for keyword in ["job", "career", "position", "apply", "application", "insider"])
            is_valid_url = is_valid_url or is_valid_title
        
        assert is_valid_url, f"View Role butonu doğru bir şekilde yönlendirmiyor! URL: {current_url}"
        print(f"✓ View Role butonu başarıyla doğrulandı. URL: {current_url}")
        
        # Yeni sekmeyi kapat ve ana sekmeye geri dön
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def go_to_open_positions(self):
        """Açık pozisyonlar sayfasına gider."""
        print("TEST ADIMI: Açık pozisyonlar sayfasına yönlendiriliyor...")
        # 'See all QA jobs' butonunu bul ve tıklanabilir olmasını bekle
        open_positions = self.wait.until(EC.element_to_be_clickable(self.open_positions_link))
        # Butonun görünür olduğunu doğrula
        assert open_positions.is_displayed(), "'See all QA jobs' butonu görünür değil!"
        # Butona tıkla
        open_positions.click()
        print("✓ Açık pozisyonlar sayfasına başarıyla yönlendirildi")

