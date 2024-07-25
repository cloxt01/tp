from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import json
import time

def load_cookies(file_path):
    """Memuat cookies dari file JSON."""
    with open(file_path, 'r') as file:
        cookies = json.load(file)
    return cookies

def apply_cookies(driver, cookies):
    """Menerapkan cookies ke driver."""
    for name, value in cookies.items():
        # Konversi nilai cookie ke string
        cookie = {
            'name': name,
            'value': str(value)
        }
        driver.add_cookie(cookie)

def main():
    # Path ke geckodriver
    geckodriver_path = '/usr/local/bin/geckodriver'

    # Path ke file cookies
    cookies_file = 'cookies.json'

    # Setup Firefox options
    options = Options()
    options.headless = False  # Atur ke True jika ingin mode headless

    # Setup WebDriver
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(options=options, service=service)

    try:
        # Navigasi ke halaman login atau halaman yang membutuhkan cookies
        driver.get("https://www.tokopedia.com")

        # Tunggu beberapa saat untuk memastikan halaman sepenuhnya dimuat
        time.sleep(5)

        # Muat cookies dari file JSON
        cookies = load_cookies(cookies_file)

        # Terapkan cookies ke driver
        apply_cookies(driver, cookies)

        # Navigasi ulang ke halaman setelah cookie diterapkan
        driver.refresh()

        # Tunggu beberapa saat untuk melihat hasil
        time.sleep(10)
    finally:
        # Tutup browser
        driver.quit()

if __name__ == "__main__":
    main()
