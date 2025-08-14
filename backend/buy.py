from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bot import open_browser


def run_buy(pair):
    driver = open_browser.driver
    driver.get(f"https://www.bydfi.com/en/spot/{pair}")

    wait = WebDriverWait(driver, 15)

    # Al butonuna tıklama
    buybutton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[2]/div/div[2]/div[1]/div[2]'
    )))
    buybutton.click()
    
    
    
    coin_element = wait.until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="spot-layout"]/div[2]/div/div[2]/div[3]/div/span[2]'
        )))
    coin_name = coin_element.text.strip()
    print("coin_name: ",coin_name)
    
    # try:
    #     # Balance alanı bekleniyor
    #     balance_element = wait.until(EC.presence_of_element_located((By.XPATH,
    #         '//*[@id="spot-layout"]/div[1]/div[1]/div[3]/div[2]/div/div[2]/div[3]/div/span[2]'
    #     )))
    #     balance = balance_element.text.strip()
    # except:
    #     balance = "0"

    try:
        price_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[text()='Fiyat']/following-sibling::div//input")
        ))

        # Burada text_to_be_present_in_element_value yerine value attribute’unun dolmasını bekleyebiliriz:
        def price_value_loaded(driver):
            val = price_element.get_attribute("value")
            return val is not None and val.strip() != "" and val.strip() != "0"

        wait.until(price_value_loaded)

        price = price_element.get_attribute("value").strip()
        print("Price found:", price)

    except Exception as e:
        print("Price not found:", e)
        price = "0"

    # try:
    #     coin = driver.find_element(By.XPATH,
    #         '//*[@id="spot-layout"]/div[1]/div[1]/div[3]/div[2]/div/div[2]/div[4]/div[1]/div/div[2]/span'
    #     ).text  # .text ile iç metni alıyoruz
    # except:
    #     coin = "0"




    #//*[@id="spot-layout"]/div[1]/div[1]/div[3]/div[2]/div/div[2]/div[4]/div[1]/div/div[2]/span
    return {
        "type": "buy",
        "balance": coin_name,
        "price": price,
        # "coin":coin
    }
