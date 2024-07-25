from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

def buy_now_shopee_with_profile():
    # Path to the Firefox binary
    firefox_binary_path = r'/opt/firefox/firefox'

    # Path to the geckodriver binary
    geckodriver_path = r'/usr/local/bin/geckodriver'

    # Path to the Firefox profile directory
    profile_path = '/home/cloxt00/.mozilla/firefox/6fyahcuq.default'

    options = Options()
    options.binary_location = firefox_binary_path
    options.profile = profile_path  # Use the existing Firefox profile
    options.headless = False  # Set to True if you want to run in headless mode

    # Service object with the geckodriver path
    service = Service(geckodriver_path)

    # Initialize the Firefox driver with the specified options and service
    driver = webdriver.Firefox(options=options, service=service)

    try:
        # Navigate to the Shopee product page
        print("Navigating to the Shopee product page...")
        driver.get("https://shopee.co.id/BIOAQUA-Moisturizer-SymWhite-377-Cream-Pemutih-Wajah-50g-Krim-Penghilang-Flek-Hitam-Di-Wajah-Whitening-Fade-Dark-Spot-Mosturizer-Mencerahkan-Day-Cream-Night-Cream-Pelembab-Wajah-Kering-Dan-Kusam-Moisturizing-Brightening-i.297682305.18474821895")

        # Wait for the page to load
        print("Waiting for the page to load...")
        time.sleep(5)  # Adjust as needed


    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Quitting the driver...")
        driver.quit()

if __name__ == "__main__":
    buy_now_shopee_with_profile()
