import json

def read_cookies_from_file(file_path):
    """Membaca string cookie dari file."""
    try:
        with open(file_path, 'r') as file:
            cookie_string = file.read().strip()
        return cookie_string
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file: {e}")
        return None

def save_cookies_to_json(cookie_string, output_file):
    """Menyimpan string cookie ke file JSON."""
    cookies = {}
    try:
        cookie_pairs = cookie_string.split(';')
        for pair in cookie_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses cookies: {e}")

    # Simpan cookies ke file JSON
    with open(output_file, 'w') as file:
        json.dump({"cookies": cookies}, file, indent=4)

    print(f'Cookies berhasil disimpan ke {output_file}')

def main():
    input_file = 'cookies.txt'  # Nama file input
    output_file = 'cookies.json'  # Nama file output
    
    # Baca string cookie dari file
    cookie_string = read_cookies_from_file(input_file)
    if cookie_string:
        save_cookies_to_json(cookie_string, output_file)

if __name__ == "__main__":
    main()

