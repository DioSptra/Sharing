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

LOADING_CHARS = ['|', '/', '-', '\\']

def spinner_print(msg, duration=0.3):
    """Animasi loading singkat di console"""
    for char in LOADING_CHARS:
        sys.stdout.write(f"\r{msg} {char}")
        sys.stdout.flush()
        time.sleep(duration)
    sys.stdout.write(f"\r{msg} ✅\n")

def check_file(path):
    """Cek keberadaan file dengan animasi loading"""
    spinner_print(f"[CHECK] Mengecek file: {path}")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"[ERROR] File hilang: {path}")

def check_html_not_empty(path):
    spinner_print(f"[CHECK] Mengecek isi HTML: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read().strip()
        if len(contents) == 0:
            raise ValueError(f"[ERROR] {path} kosong!")

def check_html_title(path, expected_title="Sharing Session"):
    spinner_print(f"[CHECK] Mengecek title HTML di {path}")
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        title = soup.title.string.strip() if soup.title else ""
        if title != expected_title:
            raise AssertionError(f"[ERROR] Title salah! Harusnya '{expected_title}', tapi dapat '{title}'")

def main():
    print("=== START UNIT TEST ===\n")

    # 1️⃣ Cek semua file wajib
    for f in REQUIRED_FILES:
        check_file(f)

    # 2️⃣ Cek konten HTML
    html_path = "frontend/index.html"
    check_html_not_empty(html_path)
    check_html_title(html_path, expected_title="Sharing Session")  # sesuaikan title kamu

    print("\n✅ SEMUA FILE AMAN ✅ DAN TIDAK ADA YANG MENCURIGAKAN ✅")

if __name__ == "__main__":
    main()
