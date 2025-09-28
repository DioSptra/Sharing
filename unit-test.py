import os
import sys
import time
from bs4 import BeautifulSoup

# === Daftar file wajib ===
REQUIRED_FILES = [
    "frontend/index.html",
    "frontend/style.css",
    "frontend/script.js",
    "backend/Dockerfile",
    "backend/requirements.txt",
    "backend/app.py",
    "nginx/Dockerfile",
    "nginx/default.conf",
    "docker-compose.yaml",
    ".env",
    "deploy.sh"
]

# Warna ANSI
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

LOADING_CHARS = ['|', '/', '-', '\\']

def spinner_print(msg, duration=0.1):
    """Animasi loading dengan warna sesuai status"""
    # Start merah
    sys.stdout.write(f"\r{RED}{msg} [START]{RESET}\n")
    sys.stdout.flush()
    time.sleep(0.3)

    # Loading kuning
    for _ in range(3):  # loop 3x biar keliatan
        for char in LOADING_CHARS:
            sys.stdout.write(f"\r{YELLOW}{msg} please wait... {char}{RESET}")
            sys.stdout.flush()
            time.sleep(duration)

    # Selesai hijau
    sys.stdout.write(f"\r{GREEN}{msg} ✅ Selesai!{RESET}\n")

def check_file(path):
    spinner_print(f"[CHECK] Mengecek file: {path}")
    if not os.path.isfile(path):
        print(f"{RED}[ERROR] File hilang: {path}{RESET}")
        raise FileNotFoundError(path)

def check_html_not_empty(path):
    spinner_print(f"[CHECK] Mengecek isi HTML: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read().strip()
        if len(contents) == 0:
            print(f"{RED}[ERROR] {path} kosong!{RESET}")
            raise ValueError(f"{path} kosong!")

def check_html_title(path, expected_title="Sharing Session"):
    spinner_print(f"[CHECK] Mengecek title HTML di {path}")
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        title = soup.title.string.strip() if soup.title else ""
        if title != expected_title:
            print(f"{RED}[ERROR] Title salah! Harusnya '{expected_title}', tapi dapat '{title}'{RESET}")
            raise AssertionError(f"Title salah!")

def main():
    print(f"{RED}=== START UNIT TEST ==={RESET}\n")

    # 1️⃣ Cek semua file wajib
    for f in REQUIRED_FILES:
        check_file(f)

    # 2️⃣ Cek konten HTML
    html_path = "frontend/index.html"
    check_html_not_empty(html_path)
    check_html_title(html_path, expected_title="Sharing Session")

    print(f"\n{GREEN}✅ SEMUA FILE AMAN DAN TIDAK ADA YANG MENCURIGAKAN ! ! !{RESET}")

if __name__ == "__main__":
    main()
