import os
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfkit
from PyPDF2 import PdfMerger
from datetime import datetime

START_URL = "https://www.arbeitsinspektion.gv.at/Service/Rechtsvorschriften/Rechtsvorschriften.html"
OUTPUT_FOLDER = "pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PDFKIT_OPTIONS = {
    'no-images': ''
}

def get_all_links(url):
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
        print(f"Ghostscript-Fehler bei {input_path}: {e}")
        return input_path  # im Fehlerfall unkomprimierte Datei zurückgeben

def download_or_render_pdf(url, index):
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[-1].lower()
    raw_pdf = os.path.join(OUTPUT_FOLDER, f"raw_{index:03d}.pdf")
    compressed_pdf = os.path.join(OUTPUT_FOLDER, f"{index:03d}.pdf")

    try:
        if ext == ".pdf":
            print(f"PDF direkt herunterladen: {url}")
            response = requests.get(url, headers=HEADERS)
            with open(raw_pdf, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Render HTML zu PDF (ohne Bilder): {url}")
            pdfkit.from_url(url, raw_pdf, options=PDFKIT_OPTIONS)

        # Nach der Erstellung komprimieren
        return compress_pdf(raw_pdf, compressed_pdf)

    except Exception as e:
        print(f"Fehler bei {url}: {e}")
        return None

def combine_pdfs(pdf_paths, output_file):
    merger = PdfMerger()
    for path in pdf_paths:
        try:
            merger.append(path)
        except Exception as e:
            print(f"Fehler beim Hinzufügen {path}: {e}")
    merger.write(output_file)
    merger.close()
    print(f"Kombinierte PDF gespeichert unter: {output_file}")

def main():
    print("Sammle alle Links...")
    links = get_all_links(START_URL)
    print(f"{len(links)} Links gefunden.")

    pdf_paths = []
    for idx, link in enumerate(links):
        pdf_path = download_or_render_pdf(link, idx + 1)
        if pdf_path:
            pdf_paths.append(pdf_path)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"rechtsvorschriften_{date_str}.pdf"

    if pdf_paths:
        combine_pdfs(pdf_paths, output_filename)
    else:
        print("Keine PDFs zum Kombinieren gefunden.")

if __name__ == "__main__":
    main()
