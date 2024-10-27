import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Mengecek apakah argumen URL dan nama folder sudah diberikan
if len(sys.argv) != 3:
    print("Usage: python3 download_website.py <url_website> <nama_folder>")
    sys.exit(1)

# Mendapatkan URL dan nama folder dari argumen
url = sys.argv[1]
output_dir = sys.argv[2]

# Membuat direktori penyimpanan jika belum ada
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_file(url, folder, original_path):
    try:
        response = requests.get(url, stream=True)
        # Memastikan path sesuai dengan struktur folder asli
        full_path = os.path.join(folder, original_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {full_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Mengambil HTML dari halaman index
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Simpan HTML dari index
index_path = os.path.join(output_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as file:
    file.write(soup.prettify())
print("HTML saved to index.html")

# Mengambil dan menyimpan CSS
for link in soup.find_all("link", {"rel": "stylesheet"}):
    css_url = urljoin(url, link["href"])
    css_path = urlparse(link["href"]).path.lstrip('/')
    download_file(css_url, output_dir, css_path)

# Mengambil dan menyimpan JavaScript
for script in soup.find_all("script", src=True):
    js_url = urljoin(url, script["src"])
    js_path = urlparse(script["src"]).path.lstrip('/')
    download_file(js_url, output_dir, js_path)

# Mengambil dan menyimpan gambar
for img in soup.find_all("img"):
    img_url = urljoin(url, img["src"])
    img_path = urlparse(img["src"]).path.lstrip('/')
    download_file(img_url, output_dir, img_path)

print("Download complete")
