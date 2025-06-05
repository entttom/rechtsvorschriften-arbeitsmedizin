import os
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfkit
from PyPDF2 import PdfMerger, PdfReader
from datetime import datetime

# Ausgangs-URL
START_URL = "https://www.arbeitsinspektion.gv.at/Service/Rechtsvorschriften/Rechtsvorschriften.html"
OUTPUT_FOLDER = "pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTTP Header
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# wkhtmltopdf Optionen
PDFKIT_OPTIONS = {
    'no-images': ''
}

# Maximale Größe pro Teil-PDF (in MB) und in Bytes
SIZE_LIMIT_MB = 190
SIZE_LIMIT_BYTES = SIZE_LIMIT_MB * 1024 * 1024

# Maximale Wortzahl pro Teil-PDF
WORD_LIMIT = 490_000

def get_all_links(url):
    """Sammelt alle ausgehenden Links."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
        full_url = urljoin(url, tag['href'])
        if full_url.startswith("http"):
            links.add(full_url)
    return list(links)

def compress_pdf(input_path, output_path):
    """Komprimiert eine PDF mit Ghostscript."""
    try:
        subprocess.run([
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_path}", input_path
        ], check=True)
        print(f"✅ PDF komprimiert: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Fehler bei Komprimierung von {input_path}: {e}")
        # Falls Kompression fehlschlägt, gib die unveränderte Datei zurück
        return input_path

def download_or_render_pdf(url, index):
    """Lädt PDF oder rendert HTML zu PDF, dann komprimiert sie."""
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[-1].lower()
    raw_pdf = os.path.join(OUTPUT_FOLDER, f"raw_{index:03d}.pdf")
    compressed_pdf = os.path.join(OUTPUT_FOLDER, f"{index:03d}.pdf")

    try:
        if ext == ".pdf":
            print(f"⬇️  PDF herunterladen: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            with open(raw_pdf, 'wb') as f:
                f.write(response.content)
        else:
            print(f"🌐 HTML rendern: {url}")
            pdfkit.from_url(url, raw_pdf, options=PDFKIT_OPTIONS)

        return compress_pdf(raw_pdf, compressed_pdf)
    except Exception as e:
        print(f"❌ Fehler bei {url}: {e}")
        return None

def count_words_in_pdf_pypdf2(path: str, stop_at_limit: bool = True) -> int:
    """
    Zählt Wörter in einer PDF (PyPDF2). 
    Wenn 'stop_at_limit' True ist, bricht es ab, sobald WORD_LIMIT auf dieser Datei erreicht ist.
    """
    reader = PdfReader(path)
    total_words = 0

    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            # Wenn Text-Extraktion auf dieser Seite fehlschlägt, überspringen
            continue

        word_count_on_page = len(text.split())
        total_words += word_count_on_page

        if stop_at_limit and total_words > WORD_LIMIT:
            # Abbruch, sobald die PDF selbst schon über WORD_LIMIT liegt
            return total_words

    return total_words

def combine_pdfs_split(pdf_paths, base_filename):
    """
    Führt alle PDFs zusammen und splittet in Teile, sobald
    entweder
      1) Gesamtgröße > SIZE_LIMIT_BYTES (190 MB) oder
      2) Gesamt-Wortzahl > WORD_LIMIT (490.000 Wörter)
    überschritten würde.
    """
    part = 1
    current_merger = PdfMerger()
    current_size = 0      # in Bytes
    current_words = 0     # aktuelle Wortzahl im Merger

    for path in pdf_paths:
        file_size = os.path.getsize(path)
        word_count = count_words_in_pdf_pypdf2(path, stop_at_limit=True)

        exceeds_size  = (current_size + file_size)   > SIZE_LIMIT_BYTES
        exceeds_words = (current_words + word_count) > WORD_LIMIT

        # Wenn eine der Grenzen überschritten würde und wir bereits Dateien im aktuellen Merger haben:
        if (exceeds_size or exceeds_words) and current_size > 0:
            output_filename = f"{part}_{base_filename}.pdf"
            current_merger.write(output_filename)
            current_merger.close()
            print(
                f"📄 Gespeichert: {output_filename} "
                f"→ {current_size/1024/1024:.2f} MB, {current_words} Wörter"
            )

            # Neuen Merger für den nächsten Part anlegen
            part += 1
            current_merger = PdfMerger()
            current_size = 0
            current_words = 0

        # Datei dem aktuellen Merger hinzufügen
        current_merger.append(path)
        current_size  += file_size
        current_words += word_count

    # Letzten Part speichern, falls noch Inhalte im Merger sind
    if current_size > 0:
        output_filename = f"{part}_{base_filename}.pdf"
        current_merger.write(output_filename)
        current_merger.close()
        print(
            f"📄 Gespeichert: {output_filename} "
            f"→ {current_size/1024/1024:.2f} MB, {current_words} Wörter"
        )

def main():
    print("🔍 Sammle Links...")
    links = get_all_links(START_URL)
    print(f"🔗 {len(links)} Links gefunden.")

    pdf_paths = []
    for idx, link in enumerate(links, start=1):
        pdf_path = download_or_render_pdf(link, idx)
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
