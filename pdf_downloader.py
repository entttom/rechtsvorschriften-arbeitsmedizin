import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfkit
from PyPDF2 import PdfMerger
from datetime import datetime

# Ausgangsseite
START_URL = "https://www.arbeitsinspektion.gv.at/Service/Rechtsvorschriften/Rechtsvorschriften.html"
OUTPUT_FOLDER = "pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTTP Header
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# PDFKit Optionen – keine Bilder rendern
PDFKIT_OPTIONS = {
    'no-images': ''
}

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

def download_or_render_pdf(url, index):
    """PDF direkt herunterladen oder HTML zu PDF umwandeln (ohne Bilder)."""
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[-1].lower()
    filename = f"{index:03d}.pdf"
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    try:
        if ext == ".pdf":
            print(f"PDF direkt herunterladen: {url}")
            response = requests.get(url, headers=HEADERS)
            with open(output_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"HTML rendern (ohne Bilder): {url}")
            pdfkit.from_url(url, output_path, options=PDFKIT_OPTIONS)
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
        return None

    return output_path

def combine_pdfs(pdf_paths, output_file):
    """Kombiniert eine Liste von PDFs zu einer Datei."""
    merger = PdfMerger()
    for path in pdf_paths:
        try:
            merger.append(path)
        except Exception as e:
            print(f"Fehler beim Kombinieren von {path}: {e}")
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

    # Dynamisches Datum z. B. "2025-04-11"
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"rechtsvorschriften_{date_str}.pdf"

    if pdf_paths:
        combine_pdfs(pdf_paths, output_filename)
    else:
        print("Keine PDFs zum Kombinieren gefunden.")

if __name__ == "__main__":
    main()
