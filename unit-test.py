import os
from bs4 import BeautifulSoup

# Paths wajib ada
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

def test_files_exist():
    """Cek semua file wajib ada"""
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]
    assert not missing, f"File hilang: {missing}"

def test_index_html_not_empty():
    """Cek apakah index.html tidak kosong"""
    path = "frontend/index.html"
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read().strip()
        assert len(contents) > 0, f"{path} kosong!"

def test_index_html_title(expected_title="Sharing Session"):
    """Cek apakah title HTML sesuai harapan"""
    path = "frontend/index.html"
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        title = soup.title.string.strip() if soup.title else ""
        assert title == expected_title, f"Title salah! Harusnya '{expected_title}', tapi dapat '{title}'"

if __name__ == "__main__":
    test_files_exist()
    test_index_html_not_empty()
    test_index_html_title()
    print("✅ Semua file & tes HTML berhasil!")
