import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_cookies(driver, cookies_file):
    with open(cookies_file, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def buy_now_lazada_with_profile():
    # Path to the Firefox binary
    firefox_binary_path = r'/opt/firefox/firefox'

    # Path to the geckodriver binary
    geckodriver_path = r'/usr/local/bin/geckodriver'

    # Path to the Firefox profile directory
    profile_path = '/home/cloxt00/.mozilla/firefox/6fyahcuq.default'

    # Path to the cookies file
    cookies_file = 'cookies.json'

    options = Options()
    options.binary_location = firefox_binary_path
    options.profile = profile_path  # Use the existing Firefox profile
    options.headless = False  # Set to True if you want to run in headless mode

    # Service object with the geckodriver path
    service = Service(geckodriver_path)

    # Initialize the Firefox driver with the specified options and service
    driver = webdriver.Firefox(options=options, service=service)

    try:
        print("Loading cookies from the file...")
        load_cookies(driver, cookies_file)

        # Navigate to the Lazada checkout page
        print("Navigating to the Lazada checkout page...")
        driver.get("https://checkout.lazada.co.id/shipping?spm=a2o4j.cart.proceed_to_checkout.proceed_to_checkout")

        # Wait for the 'Lihat Semua Metode >' element to appear
        print("Waiting for the 'Lihat Semua Metode >' element to appear...")
        wait = WebDriverWait(driver, 20)
        lihat_metode_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='payment-card-header-action' and contains(text(), 'Lihat Semua Metode >')]")))

        # Click the 'Lihat Semua Metode >' element
        print("Clicking the 'Lihat Semua Metode >' element...")
        lihat_metode_element.click()

        # Wait for the 'Bank Transfer' element to appear
        print("Waiting for the 'Bank Transfer' element to appear...")
        bank_transfer_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-wrapper small']//div[@class='title-wrapper']//div[@class='title bold' and contains(text(), 'Bank Transfer')]")))

        # Click the 'Bank Transfer' element
        print("Clicking the 'Bank Transfer' element...")
        out = input("Press Enter to quitting")
        bank_transfer_element.click()

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Quitting the driver...")
        driver.quit()

if __name__ == "__main__":
    buy_now_lazada_with_profile()
