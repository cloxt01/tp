from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pickle
import time

def use_cookies_to_login():
    # Path to the Firefox binary
    firefox_binary_path = r'/opt/firefox/firefox'
    # Path to the geckodriver binary
    geckodriver_path = r'/usr/local/bin/geckodriver'

    options = Options()
    options.binary_location = firefox_binary_path
    options.headless = False  # Aktifkan mode headless
    options.set_preference("general.useragent.override", "User-Agent-Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    # Service object with the geckodriver path
    service = Service(geckodriver_path)
    
    # Initialize the Firefox driver with the specified options and service
    driver = webdriver.Firefox(options=options, service=service)


    try:
        # Open Tokopedia
        driver.get("https://shopee.com")

        # Load cookies

        # Wait for the page to load
        print("Waiting for the page to load...")
        time.sleep(5)  # Adjust as needed
    finally:
        driver.quit()

if __name__ == "__main__":
    use_cookies_to_login()
