import os
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfkit
from PyPDF2 import PdfMerger
from datetime import datetime

# Ausgangs-URL
START_URL = "https://www.arbeitsinspektion.gv.at/Service/Rechtsvorschriften/Rechtsvorschriften.html"
OUTPUT_FOLDER = "pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTTP Header
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Optionen für HTML zu PDF (ohne Bilder)
PDFKIT_OPTIONS = {
    'no-images': ''
}

# PDF-Größenlimit
MAX_SIZE_MB = 100
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def get_all_links(url):
    """Sammelt alle externen Links (http/https) auf der Seite."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
        full_url = urljoin(url, tag['href'])
        if full_url.startswith("http"):
            links.add(full_url)
    return list(links)

def compress_pdf(input_path, output_path):
    """Komprimiert ein PDF mit Ghostscript."""
    try:
        subprocess.run([
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_path}", input_path
        ], check=True)
        print(f"PDF komprimiert: {output_path}")
        return output_path
    except Exception as e:
        print(f"Fehler bei Komprimierung von {input_path}: {e}")
        return input_path

def download_or_render_pdf(url, index):
    """Lädt PDF oder rendert HTML zu PDF und komprimiert es."""
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[-1].lower()
    raw_pdf = os.path.join(OUTPUT_FOLDER, f"raw_{index:03d}.pdf")
    compressed_pdf = os.path.join(OUTPUT_FOLDER, f"{index:03d}.pdf")

    try:
        if ext == ".pdf":
            print(f"PDF herunterladen: {url}")
            response = requests.get(url, headers=HEADERS)
            with open(raw_pdf, 'wb') as f:
                f.write(response.content)
        else:
            print(f"HTML rendern: {url}")
            pdfkit.from_url(url, raw_pdf, options=PDFKIT_OPTIONS)
        return compress_pdf(raw_pdf, compressed_pdf)
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
        return None

def combine_pdfs_split(pdf_paths, base_filename):
    """Fasst PDFs zusammen und splittet in Teile unter 512 MB."""
    part = 1
    current_merger = PdfMerger()
    current_size = 0
    current_files = []

    for path in pdf_paths:
        file_size = os.path.getsize(path)
        if current_size + file_size > MAX_SIZE_BYTES and current_files:
            output = f"{base_filename}_part{part}.pdf"
            current_merger.write(output)
            current_merger.close()
            print(f"📄 Gespeichert: {output} ({current_size / 1024 / 1024:.2f} MB)")
            part += 1
            current_merger = PdfMerger()
            current_size = 0
            current_files = []

        current_merger.append(path)
        current_size += file_size
        current_files.append(path)

    if current_files:
        output = f"{base_filename}_part{part}.pdf"
        current_merger.write(output)
        current_merger.close()
        print(f"📄 Gespeichert: {output} ({current_size / 1024 / 1024:.2f} MB)")

def main():
    print("🔗 Sammle Links...")
    links = get_all_links(START_URL)
    print(f"🔍 {len(links)} Links gefunden.")

    pdf_paths = []
    for idx, link in enumerate(links):
        pdf_path = download_or_render_pdf(link, idx + 1)
        if pdf_path:
            pdf_paths.append(pdf_path)

    date_str = datetime.now().strftime("%Y-%m-%d")
    base_filename = f"rechtsvorschriften_{date_str}"

    if pdf_paths:
        combine_pdfs_split(pdf_paths, base_filename)
    else:
        print("⚠️ Keine PDFs zum Zusammenführen.")

if __name__ == "__main__":
    main()
