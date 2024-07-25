import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

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
        payment_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='btn-quickpay-pay']"))
        )
        print("┣ Tombol 'Bayar' ditemukan.")
        payment_button.click()
        return True
    except TimeoutException:
        print("┣ Tombol 'Bayar' tidak ditemukan.")
        return False
    except Exception as e:
        print(f"┣ Kesalahan saat mengklik tombol 'Bayar': {e}")
        return False

def click_payment_method(driver):
    """Mengklik tombol 'Pilih Pembayaran' jika ditemukan."""
    try:
        payment_button = driver.find_element(By.XPATH, "//span[normalize-space(text())='Pilih Pembayaran']")
        payment_button.click()
        return True
    except NoSuchElementException:
        return False

def switch_to_payment_frame(driver):
    """Memeriksa dan beralih ke iframe yang berisi tombol 'Bayar'."""
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    print(f"┣ Ditemukan {len(iframes)} iframe(s).")
    
    for i in range(len(iframes)):
        print(f"┣ Memeriksa iframe ke-{i+1}")
        try:
            driver.switch_to.frame(iframes[i])
            if driver.find_element(By.XPATH, "//button[@id='btn-quickpay-pay']"):
                print("┣ Tombol 'Bayar' ditemukan.")
                return True
        except NoSuchElementException:
            print(f"┣ Tombol 'Bayar' tidak ditemukan di iframe ke-{i+1}.")
            driver.switch_to.default_content()
        except StaleElementReferenceException:
            print(f"┣ StaleElementReferenceException pada iframe ke-{i+1}. Mencoba lagi.")
            driver.switch_to.default_content()
    return False

def continuously_wait_for_payment_button(driver, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if switch_to_payment_frame(driver):
                return True
        except Exception as e:
            print(f"┣ Terjadi kesalahan: {e}")
        time.sleep(1)
    print("┣ Timeout: Gagal menemukan tombol 'Bayar'.")
    return False

def tab_cart_process(driver, target_price):
    """Proses di tab pertama: menangani cart dan klik 'Pilih Pembayaran'."""
    url = "https://www.tokopedia.com/cart/shipment"
    driver.get(url)
    try:
        while True:
            print("┣ Menunggu nilai 'Total Belanja' berubah")
            if WebDriverWait(driver, 60).until(lambda d: check_total_bill(d, target_price)):
                print("┣ Nilai 'Total Belanja' berubah.")
                start_time = time.time()
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

            # Menunggu tombol 'Bayar' di dalam iframe
            print("┣ Menunggu tombol 'Bayar'...")
            if continuously_wait_for_payment_button(driver):
                # Mencatat waktu selesai
                if click_payment_button(driver):
                    print("┣ Berhasil menemukan dan mengklik tombol 'Bayar'")

                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"┣ Selesai dalam: {elapsed_time:.3f} detik")
                    input("Tekan Enter untuk keluar")
    except TimeoutException as e:
        print(f"┗ Timeout: Elemen yang diharapkan tidak muncul. {e}")

def main():
    # Konfigurasi BrowserStack
    browserstack_url = "https://<username>:<access_key>@hub-cloud.browserstack.com/wd/hub"
    desired_capabilities = {
        'browser': 'firefox',
        'browser_version': 'latest',
        'os': 'Windows',
        'os_version': '11',
        'name': 'BrowserStack Test',  # Nama sesi di BrowserStack
        'build': 'browserstack-build-1',
        'project': 'BrowserStack Sample'
    }
    
    # Setup opsi untuk Firefox
    options = Options()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")
    options.headless = True  # Aktifkan mode headless

    # Setup driver
    driver = webdriver.Remote(
        command_executor=browserstack_url,
        options=options,
        desired_capabilities=desired_capabilities
    )
    
    target_price = "Rp15.000"

    try:
        tab_cart_process(driver, target_price)
    except KeyboardInterrupt:
        print("┗ Skrip dihentikan oleh pengguna.")
    finally:
        driver.quit()
        print("┗ Driver berhenti.")

if __name__ == "__main__":
    main()
