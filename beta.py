from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_tokopedia():
    # Path to the Firefox binary
    firefox_binary_path = r'/opt/firefox/firefox'

    # Path to the geckodriver binary
    geckodriver_path = r'/usr/local/bin/geckodriver'

    options = Options()
    options.binary_location = firefox_binary_path
    options.add_argument('--headless')  # Enable headless mode

    # Service object with the geckodriver path
    service = Service(geckodriver_path)

    # Initialize the Firefox driver with the specified options and service
    driver = webdriver.Firefox(options=options, service=service)

    try:
        # Open Tokopedia
        print("Opening Tokopedia...")
        driver.get("https://www.tokopedia.com")

        # Wait for the page to load
        print("Waiting for the page to load...")
        time.sleep(5)  # Adjust as needed

        # Locate the search input element
        print("Locating the search input element...")
        search_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Cari di Tokopedia"]')

        # Print the placeholder attribute of the search input element
        placeholder_text = search_input.get_attribute("placeholder")
        print(f'Placeholder text: {placeholder_text}')

        # Send keys to the input field and press Enter
        print("Sending keys to the search input field...")
        search_input.send_keys("Laptop")
        search_input.send_keys(Keys.RETURN)  # Press Enter

        # Wait for a while to see the results
        print("Waiting for search results...")
        time.sleep(5)  # Adjust as needed

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Quitting the driver...")
        driver.quit()

if __name__ == "__main__":
    search_tokopedia()
