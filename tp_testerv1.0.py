from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def check_total_bill(driver):
    """Memeriksa apakah elemen total bill memiliki nilai yang diharapkan."""
    try:
        total_bill_element = driver.find_element(By.CSS_SELECTOR, 'div.css-8olzao p[data-testid="lblSafSummaryTotalBill"]')
        return total_bill_element.is_displayed() and "Rp" in total_bill_element.text.strip()
    except NoSuchElementException:
        return False
    
def click_payment_button(driver):
    """Mengklik tombol 'Bayar' jika ditemukan."""
    try:
        # Menunggu hingga tombol tersedia
        payment_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='btn-quickpay-pay']"))
        )
        print("[DEBUG] Tombol 'Bayar' ditemukan.")
        payment_button.click()
        return True
    except NoSuchElementException:
        print("[DEBUG] Tombol 'Bayar' tidak ditemukan.")
        return False

def wait_for_total_bill_and_proceed():
    """Menunggu elemen total bill muncul dan melakukan pembayaran jika tersedia."""
    geckodriver_path = '/usr/local/bin/geckodriver'
    firefox_binary_path = '/opt/firefox/firefox'
    profile_path= '/home/cloxt00/.mozilla/firefox/6fyahcuq.default'

    options = Options()
    options.binary_location = firefox_binary_path
    options.headless = True  # Aktifkan mode headless
    
    profile = FirefoxProfile(profile_path)
    options.profile = profile

    service = Service(geckodriver_path)
    driver = webdriver.Firefox(options=options, service=service)

    try:
        url = "https://www.tokopedia.com/cart/shipment"
        print("[DEBUG] Navigasi ke ", url, "...")
        driver.get(url)

        print("[DEBUG] Menunggu elemen 'Total Belanja' mengandung 'Rp'...")
        WebDriverWait(driver, 120).until(lambda d: check_total_bill(d))
        print("[DEBUG] Elemen 'Total Belanja' mengandung 'Rp'.")

        print("[DEBUG] Menunggu tombol 'Pilih Pembayaran'...")
        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='Pilih Pembayaran']"))
        )

        if click_payment_button(driver):
            print("[DEBUG] Berhasil mengklik tombol 'Bayar'.")

            # Memeriksa apakah ada pesan kesalahan
            try:
                error_message_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-n-message="true"]'))
                )
                if error_message_element.is_displayed():
                    print(f"[DEBUG] Pesan Kesalahan: {error_message_element.text}")
                    return
            except TimeoutException:
                print("[DEBUG] Tidak ada pesan kesalahan yang ditemukan.")
            
            print("[DEBUG] Menunggu elemen 'Bayar'...")
            WebDriverWait(driver, 120).until(
                lambda d: "Rp" in d.find_element(By.CSS_SELECTOR, 'h4.css-1wikf7o-unf-heading.e1hd7sid4').text
            )
            print("[DEBUG] Berhasil menemukan elemen 'Bayar'")

        else:
            print("[DEBUG] Gagal mengklik tombol 'Bayar'.")

    except TimeoutException as e:
        print(f"[DEBUG] Timeout: Elemen yang diharapkan tidak muncul. {e}")

    finally:
        out = input("Press Enter to quitting")
        print("[DEBUG] Menutup driver...")
        driver.quit()

if __name__ == "__main__":
    wait_for_total_bill_and_proceed()
