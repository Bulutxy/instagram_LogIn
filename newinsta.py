from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


INSTAGRAM_USERNAME = "kullanici_adin"
INSTAGRAM_PASSWORD = "sifren"
TARGET_USER = "takip_edilecek_kullanici"  

driver = webdriver.Chrome()  
def instagram_giris():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(4)
    
    # Kullanıcı adı
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(INSTAGRAM_USERNAME)
    
    # Şifre
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(INSTAGRAM_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(6)  # Sayfanın yüklenmesi için bekle

def takip_et():
    driver.get(f"https://www.instagram.com/{TARGET_USER}/")
    time.sleep(4)
    
    try:
        # Takip et butonunu bul
        follow_button = driver.find_element(By.XPATH, "//button[text()='Follow']")
        follow_button.click()
        print(f"{TARGET_USER} takip edildi.")
    except Exception as e:
        print("Zaten takip ediliyor veya buton bulunamadı:", e)

def takipten_cikar():
    driver.get(f"https://www.instagram.com/{TARGET_USER}/")
    time.sleep(4)
    try:
        unfollow_button = driver.find_element(By.XPATH, "//button[text()='Following']")
        unfollow_button.click()
        time.sleep(2)
        # Çıkarma onay butonu
        confirm_button = driver.find_element(By.XPATH, "//button[text()='Unfollow']")
        confirm_button.click()
        print(f"{TARGET_USER} takipten çıkarıldı.")
    except Exception as e:
        print("Takipten çıkarma işlemi yapılamadı:", e)
        

def takipci_listesi_al_ve_kaydet():
    driver.get(f"https://www.instagram.com/{TARGET_USER}/followers/")
    time.sleep(4)
    
    # Popup açılır, burada takipçileri çekmek için aşağı kaydırma yapacağız
    followers_popup = driver.find_element(By.XPATH, "//div[@role='dialog']//ul")
    time.sleep(2)
    
    # Aşağı kaydırarak takipçileri yükle
    last_height = 0
    for i in range(5):  # 5 kere kaydırma (daha fazla istersen artır)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
        time.sleep(2)
    
    followers = followers_popup.find_elements(By.CSS_SELECTOR, "li")
    print(f"Toplam {len(followers)} takipçi bulundu.")
    
    takipci_isimleri = []
    for user in followers:
        name = user.find_element(By.CSS_SELECTOR, "a").text
        takipci_isimleri.append(name)
    
    # Dosyaya yaz
    with open("takipciler.txt", "w", encoding="utf-8") as f:
        for name in takipci_isimleri:
            f.write(name + "\n")
    
    print("Takipçi listesi 'takipciler.txt' dosyasına kaydedildi.")



# ------------------ Program Akışı ------------------

instagram_giris()
time.sleep(3)

takip_et()
time.sleep(3)

takipci_listesi_al_ve_kaydet()
time.sleep(3)

takipten_cikar()

time.sleep(3)
driver.quit()
