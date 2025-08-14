from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bot import open_browser
import time
from selenium.webdriver.common.keys import Keys 
import websocket
import json,requests

def execute_buy(pair, amount):
    driver = open_browser.driver
    wait = WebDriverWait(driver, 15)

    # "all" butonuna tıkla
    # sellbutton = wait.until(EC.element_to_be_clickable((By.XPATH,
    #     '//*[@id="spot-layout"]/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]'
    # )))
    # sellbutton.click()

    # Miktar input'unu bul
    # Miktar input'unu bul
    amount_input = wait.until(EC.presence_of_element_located((By.XPATH,
        "//div[text()='Total']/following-sibling::div//input"
    )))
    
    # 1) Normal clear
    amount_input.clear()
    
    # 2) CTRL+A ve Backspace ile temizle
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.BACKSPACE)

    # 3) JavaScript ile garanti boşalt
    driver.execute_script("arguments[0].value = '';", amount_input)

    # Yeni değeri yaz
    amount_input.send_keys(str(amount))

    # "Sat" onay butonuna bas
    # confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH,
    #     "//button[contains(text(), 'Buy')]"
    # )))
    # confirm_button.click()

    buybutton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[2]/div/div[2]/div[4]/button'
    )))
    buybutton.click()
    # 

    return {
        "pair": pair,
        "type": "Buy",
        "amount": amount
    }


def execute_sell(pair, amount):
    driver = open_browser.driver
    wait = WebDriverWait(driver, 15)
    
    # sellbutton = wait.until(EC.element_to_be_clickable((By.XPATH,
    #     '//*[@id="spot-layout"]/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[3]'
    # )))
    # sellbutton.click()

    
    # Miktar input'unu bul
    amount_input = wait.until(EC.presence_of_element_located((By.XPATH,
        "//div[text()='Total']/following-sibling::div//input"
    )))

    # 1) Normal clear
    amount_input.clear()
    
    # 2) CTRL+A ve Backspace ile temizle
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.BACKSPACE)

    # 3) JavaScript ile garanti boşalt
    driver.execute_script("arguments[0].value = '';", amount_input)

    # Yeni değeri yaz
    amount_input.send_keys(str(amount))

    # "Sat" onay butonuna bas
    # confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH,
    #     "//button[contains(text(), 'Sell')]"
    # )))
    # confirm_button.click()
    sellbuton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[2]/div/div[2]/div[4]/button'
    )))
    sellbuton.click()

    return {
        "pair": pair,
        "type": "sell",
        "amount": amount
    }

def search():
    driver = open_browser.driver
    wait = WebDriverWait(driver, 15)

    

    #  butonuna click
    buybutton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[1]/div/div[2]/div/div[1]/span[1]/div'
    )))
    buybutton.click()
    time.sleep(1)

    container_xpath = "/html/body/div[3]/div/div/div/div/div/div[5]/div"

    container = wait.until(EC.presence_of_element_located((By.XPATH, container_xpath)))
    items = container.find_elements(By.XPATH, "./div")

    coin_list = []
    for item in items:
        try:
            coin_name = item.find_element(By.CSS_SELECTOR, "div.name-wrapper > span:first-child").text.strip()
            quote_coin = item.find_element(By.CSS_SELECTOR, "span.quoteCoin").text.strip()
            price = item.find_element(By.CSS_SELECTOR, "div.price").text.strip()
            change = item.find_element(By.CSS_SELECTOR, "div.change > span.rate").text.strip()
            coin_list.append({
                "coin": coin_name,
                "quote": quote_coin,
                "price": price,
                "change": change
            })
        except Exception as e:
            print("Hata:", e)
   
    return coin_list
    

def getcloseopen():
    try:
        
        driver = open_browser.driver
        #wait = WebDriverWait(driver, 15)
        
       
        # # target URL eth_usdt is given as an example
        url = "https://www.bydfi.com/tr/spot/eth_usdt"
        driver.get(url)
        time.sleep(10)
        seconds_back=60
        now = int(time.time())          # integer timestamp
        from_ts = now - seconds_back

        url = "https://www.bydfi.com/api/tv/tradingView/history"
        params = {
            "symbol": "ETH_USDT",
            "resolution": "1",
            "from": from_ts,
            "to": now
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": "TOKEN=ebfbadd5-4b9c-46b7-a901-4d6886260ff8;"
        }

        r = requests.get(url, params=params, headers=headers)
        data = r.json()
        
        if data.get("s") != "ok" or not data.get("c"):
            print("Veri alınamadı, muhtemelen aralık çok kısa veya henüz bar oluşmadı.")
            return None

        print("open:", data["o"][-1])
        print("close:", data["c"][-1])
        print("high:", data["h"][-1])
        print("low:", data["l"][-1])
        print("vol:", data["v"][-1])
        print("time (timestamp):", data["t"][-1])
        return data
        # Örnek kullanım
        # for i in range(50):
        #     get_eth_ohlcv_safe(60)  # son 60 saniyeyi al
        
        
    except KeyboardInterrupt:
        print("live stope")

        #k /html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[5]/div[2]
        #a /html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]

# GET /wsquote HTTP/2
# Host: quote.bydfi.pro
# Connection: Upgrade
# Pragma: no-cache
# Cache-Control: no-cache
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
# Upgrade: websocket
# Origin: https://www.bydfi.com
# Sec-Websocket-Version: 13
# Accept-Encoding: gzip, deflate, br
# Accept-Language: tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7
# Cookie: _cfuvid=b5gyoSLuoiD__yJbNaS3mkXe_n4VQtP3h82xkSDp.6U-1755067096541-0.0.1.1-604800000
# Sec-Websocket-Key: 0ThMLziV+/Sz8jGuk7+vcw==


# GET /api/tv/tradingView/history?symbol=ETH_USDT&resolution=1&from=1755060784&to=1755060844 HTTP/2
# Host: www.bydfi.com
# Cookie: _ga=GA1.1.442332415.1753473614; user_origin=3; agent=false; agent=false; vipCode=mZVhKc; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221155715685978251264%22%2C%22first_id%22%3A%22198432b871f774-0220cc84e196ca6-26011151-2073600-198432b8720b81%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4NDMyYjg3MWY3NzQtMDIyMGNjODRlMTk2Y2E2LTI2MDExMTUxLTIwNzM2MDAtMTk4NDMyYjg3MjBiODEiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTU1NzE1Njg1OTc4MjUxMjY0In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221155715685978251264%22%7D%7D; TOKEN=ebfbadd5-4b9c-46b7-a901-4d6886260ff8; user_origin=3; _cfuvid=o4Kx0ZsZkyG3zDwo_mvZbjWvqUDoEgGhUyakJG5_C8Q-1755065222197-0.0.1.1-604800000; cf_clearance=R_7UjGHG20SXLbGXKcm9J5_eO3An7ja8yEoSMy0RpEU-1755067419-1.2.1.1-y46n_qBJRAjChEBpENf50lIr8asy4JpsFuJK9WmCmiI8FTnvW5ci3iOZYNbg5Y3DP4PiEtrBd29CjMc8OT9j98JWAWnXTsV5Dpkw3Z6bl8PvqHZdAsy7.c4Z4O26fAKz9inYmh_ECMpd91gAorVcd2wLHD70uo0tsUd87VBZIgnO0wiQxViSBmNZ.OM0dI8cBQ_4okOipexGvYcUa5NvLXljc3H.ZvP2cS9wNljuuHY; _ga_7ZEWNTGRR0=GS2.1.s1755067300$o27$g1$t1755067421$j55$l0$h0
# Sec-Ch-Ua-Full-Version-List: "Not;A=Brand";v="99.0.0.0", "Google Chrome";v="139.0.7258.67", "Chromium";v="139.0.7258.67"
# Sec-Ch-Ua-Platform: "Windows"
# Sec-Ch-Ua: "Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"
# Sec-Ch-Ua-Bitness: "64"
# Sec-Ch-Ua-Model: ""
# Sec-Ch-Ua-Mobile: ?0
# Sec-Ch-Ua-Arch: "x86"
# Sec-Ch-Ua-Full-Version: "139.0.7258.67"
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
# Sec-Ch-Ua-Platform-Version: "10.0.0"
# Accept: */*
# Sec-Fetch-Site: same-origin
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://www.bydfi.com/tr/spot/eth_usdt
# Accept-Encoding: gzip, deflate, br
# Accept-Language: tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7
# Priority: u=1, i


# HTTP/2 200 OK
# Date: Wed, 13 Aug 2025 06:48:25 GMT
# Content-Type: text/plain;charset=UTF-8
# Vary: Origin
# Vary: Access-Control-Request-Method
# Vary: Access-Control-Request-Headers
# Vary: Origin
# Vary: Access-Control-Request-Method
# Vary: Access-Control-Request-Headers
# Strict-Transport-Security: max-age=31536000; includeSubdomains
# X-Frame-Options: SAMEORIGIN
# X-Content-Type-Options: nosniff
# X-Xss-Protection: 1; mode=block
# Cf-Cache-Status: DYNAMIC
# Speculation-Rules: "/cdn-cgi/speculation"
# Server: cloudflare
# Cf-Ray: 96e6444588c1d39c-FRA
# Alt-Svc: h3=":443"; ma=86400

# {"s":"ok","c":[4677.6100000000000000],"instance":1,"t":["1755060840"],"v":[6.88950000],"h":[4678.3100000000000000],"l":[4672.6800000000000000],"o":[4673.4000000000000000]}