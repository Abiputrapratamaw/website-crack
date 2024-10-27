import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

def download_file(url, folder):
    try:
        response = requests.get(url, stream=True)
        filename = os.path.join(folder, url.split("/")[-1])

        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Mengambil HTML dari halaman index
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Simpan HTML dari index
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
    file.write(soup.prettify())
print("HTML saved")

# Mengambil dan menyimpan CSS
for link in soup.find_all("link", {"rel": "stylesheet"}):
    css_url = urljoin(url, link["href"])
    download_file(css_url, output_dir)

# Mengambil dan menyimpan JavaScript
for script in soup.find_all("script", src=True):
    js_url = urljoin(url, script["src"])
    download_file(js_url, output_dir)

# Mengambil dan menyimpan gambar
for img in soup.find_all("img"):
    img_url = urljoin(url, img["src"])
    download_file(img_url, output_dir)

print("Download complete")
