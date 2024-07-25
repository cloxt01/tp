from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def check_total_bill(driver, target_price):
    """Memeriksa apakah elemen total bill memiliki nilai yang diharapkan."""
    try:
        total_bill_element = driver.find_element(By.CSS_SELECTOR, 'div.css-8olzao p[data-testid="lblSafSummaryTotalBill"]')
        price_now = total_bill_element.text.strip()
        print(f"┣ Harga saat ini: {price_now}")
        if "Rp" in price_now and price_now != target_price:
            print("┣ Harga berubah:", price_now, " != ", target_price)
            return True
        elif "Rp" in price_now and price_now == target_price:
            print(f"┣ Harga masih {price_now}. Refreshing page...")
            driver.refresh()
            return False
    except NoSuchElementException:
        return False

def click_payment_button(driver):
    """Mengklik tombol 'Bayar' jika ditemukan."""
    try:
        # Menunggu hingga tombol tersedia
        payment_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='btn-quickpay-pay']"))
        )
        print("┣ Tombol 'Bayar' ditemukan.")
        payment_button.click()
        return True
    except TimeoutException:
        print("┣ Tombol 'Bayar' tidak ditemukan.")
        return False

def click_payment_method(driver):
    """Mengklik tombol 'Pilih Pembayaran' jika ditemukan."""
    try:
        payment_button = driver.find_element(By.XPATH, "//span[normalize-space(text())='Pilih Pembayaran']")
        payment_button.click()
        return True
    except NoSuchElementException:
        return False
    
def wait_for_total_bill_and_proceed(target_price):
    """Menunggu elemen total bill muncul dan melakukan pembayaran jika tersedia."""
    geckodriver_path = '/usr/local/bin/geckodriver'
    firefox_binary_path = '/opt/firefox/firefox'
    profile_path = '/home/cloxt00/.mozilla/firefox/6fyahcuq.default'

    options = Options()
    options.binary_location = firefox_binary_path
    options.headless = True  # Aktifkan mode headless
    
    # Ubah user-agent untuk menghindari deteksi bot
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")

    profile = webdriver.FirefoxProfile(profile_path)
    options.profile = profile

    service = Service(geckodriver_path)
    driver = webdriver.Firefox(options=options, service=service)

    try:
        url = "https://www.tokopedia.com/cart/shipment"
        print("┏ Navigasi ke ", url, "...")
        driver.get(url)

        while True:
            print("┣ Menunggu nilai 'Total Belanja' berubah")
            if WebDriverWait(driver, 60).until(lambda d: check_total_bill(d, target_price)):
                print("┣ Nilai 'Total Belanja' berubah.")
                break

        print("┣ Menunggu tombol 'Pilih Pembayaran'...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='Pilih Pembayaran']"))
        )
        if click_payment_method(driver):
            print("┣ Berhasil mengklik tombol 'Pilih Pembayaran'.")

            # Tampilkan sumber halaman setelah mengklik tombol 'Pilih Pembayaran'
            page_source = driver.page_source
            with open("page_source_after_payment_selection.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            print("┣ Sumber halaman setelah mengklik 'Pilih Pembayaran' telah disimpan ke 'page_source_after_payment_selection.html'.")

            # Buka tab baru dan navigasi ke halaman pembayaran
            print("┏ Membuka tab baru untuk navigasi ke halaman pembayaran...")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            payment_url = "https://pay.tokopedia.com/v2/payment?back_url=&device=default_v3&src=iframe"
            driver.get(payment_url)

            # Menunggu beberapa saat untuk memastikan tombol 'Bayar' siap
            print("┣ Menunggu tombol 'Bayar'...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@id='btn-quickpay-pay']")))

            if click_payment_button(driver):
                print("┣ Berhasil menemukan elemen 'Bayar'")
            else:
                print("┗ Gagal mengklik tombol 'Bayar'.")
        else:
            print("┗ Gagal mengklik tombol 'Pilih Pembayaran'.")

    except TimeoutException as e:
        print(f"┗ Timeout: Elemen yang diharapkan tidak muncul. {e}")

    finally:
        print("[DEBUG] Menutup driver...")
        driver.quit()

if __name__ == "__main__":
    target_price = "Rp15.000"
    # Masukkan harga produk saat ini
    wait_for_total_bill_and_proceed(target_price)
