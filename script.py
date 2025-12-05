# spam_simulator_modern.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import random
import string

# ==== Konfiguration ====
SITE_URL = "https://febel.ch/Kommentare.html"
SAVE_URL = "https://febel.ch/save.php"
NUM_SPAMS = 15

# ==== Moderner Weg: Chrome headless shell direkt nutzen ====
def get_driver():
    options = Options()
    
    # Kein binary_location mehr – nutze deinen installierten Chrome!
    # Wichtige Flags für reCAPTCHA v3 (Anti-Detection)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')  # Für Windows oft hilfreich
    options.add_argument('--disable-dev-shm-usage')  # Vermeidet Crashes

    # Zufälliger User-Agent pro Start
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')

    # Vollständig neuen Profil-Ordner pro Start (killt Cookies, LocalStorage, reCAPTCHA-History)
    options.add_argument(f'--user-data-dir=C:\\temp\\chrome-profile-{random.randint(1000,9999)}')
    
    # Für sichtbaren Modus (Debug: Sieh, wie der Bot lädt)
    # options.add_argument('--headless=new')  # ← AUSKOMMENTIERT: Browser sichtbar!
    
    # Selenium Manager lädt Driver automatisch (kein Pfad!)
    service = Service()  # Automatisch: Passt zu deiner Chrome-Version
    driver = webdriver.Chrome(service=service, options=options)
    
    # Extra Anti-Detection (für reCAPTCHA)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            window.chrome = { runtime: {}, app: {}, webstore: {} };
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            Object.defineProperty(navigator, 'languages', {get: () => ['de-DE', 'de']});
        """
    })

    # In get_driver(), direkt nach driver = webdriver.Chrome(...)
    driver.execute_script("window.open('','_blank');")  # Öffnet zweiten Tab (optional)
    # Oder einfach: Nicht headless laufen lassen!
    # → Kommentiere diese Zeile AUS:
    # options.add_argument('--headless=new')
    return driver

# ==== Rest wie vorher (Token holen + POST) ====
def get_recaptcha_token():
    driver = get_driver()
    try:
        driver.get(SITE_URL)
        print("Seite geladen – warte auf reCAPTCHA v3 Token (kann 2–6 Sek. dauern)...")

        # WICHTIG: Warte nicht nur auf das Element, sondern auf ein Token mit >200 Zeichen!
        token = WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.ID, "recaptchaResponse").get_attribute("value") or ""
        )
        
        # Nochmal explizit prüfen, ob es wirklich lang genug ist
        for _ in range(30):  # max 30 Sekunden warten
            token = driver.find_element(By.ID, "recaptchaResponse").get_attribute("value")
            if token and len(token) > 200:
                print(f"Token erfolgreich erhalten! ({len(token)} Zeichen)")
                return token
            print(f"Noch kein gültiges Token... (aktuell {len(token)} Zeichen) – warte...")
            time.sleep(1)

        print("Timeout: Kein gültiges Token nach 30 Sekunden.")
        return None

    except Exception as e:
        print(f"Fehler beim Laden/Token: {e}")
        driver.save_screenshot("error_debug.png")  # ← super hilfreich!
        return None
    finally:
        driver.quit()

# ==== Spam-Loop ====
def simulate_spam():
    for i in range(1, NUM_SPAMS + 1):
        print(f"\nSpam #{i}/{NUM_SPAMS}")
        token = get_recaptcha_token()
        if not token:
            print("Kein Token → überspringe")
            time.sleep(3)
            continue

        payload = {
            "name": f"Live-Test Bot #{i}",
            "email": f"bot{i}@spamtest.ch",
            "comment": f"Spam-Simulation #{i} – reCAPTCHA v3 wurde clientseitig generiert!\nZeit: {time.strftime('%H:%M:%S')}\nLerneffekt: Ohne Server-Check = offene Tür!",
            "recaptcha_response": token
        }

        r = requests.post(SAVE_URL, data=payload, timeout=10)
        if r.status_code == 200:
            print("Erfolg: Kommentar gespeichert!")
        else:
            print(f"Fehler: {r.status_code} – {r.text[:200]}")

        time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    print("Starte moderne Spam-Simulation (2025-Methode mit headless-shell)")
    simulate_spam()
    print("\nFertig! Schau jetzt auf https://febel.ch/Kommentare.html – die Bots sind da.")
