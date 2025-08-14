
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from backend.config import EMAIL,PASSWORD
import time

# Her adımın durumunu tutan flag'ler
step_flags = {
    "open_page": False,
    "enter_email": False,
    "enter_password": False,
    "click_login": False,
}
def wait_for_element(driver,xpath, timeout=10):
    """Elementi bekler, bulamazsa None döner."""
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        return None
    

def login_to_capth(driver):
    # === STEP 2: Email gir ===
    if step_flags["open_page"] and not step_flags["enter_email"]:
        email_input = wait_for_element(driver,'//*[@id="__next"]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/input')
        if email_input:
            email_input.clear()
            email_input.send_keys(EMAIL)
            step_flags["enter_email"] = True
            print("[✓] Email girildi.")

    # === STEP 3: Şifre gir ===
    if step_flags["enter_email"] and not step_flags["enter_password"]:
        password_input = wait_for_element(driver,'//*[@id="__next"]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/input')
        if password_input:
            password_input.clear()
            password_input.send_keys(PASSWORD)
            step_flags["enter_password"] = True
            print("[✓] Şifre girildi.")

    # === STEP 4: Login butonuna tıkla ===
    if step_flags["enter_password"] and not step_flags["click_login"]:
        login_button = wait_for_element(driver,'//*[@id="__next"]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[3]/button')
        if login_button:
            login_button.click()
            step_flags["click_login"] = True
            print("[✓] Giriş butonuna basıldı.")
    
    
