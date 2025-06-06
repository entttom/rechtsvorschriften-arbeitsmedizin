# 📚 Rechtsvorschriften Arbeitsmedizin - Automatischer PDF Downloader

> 🎯 **Ziel**: Automatisierte Sammlung und Aufbereitung aller arbeitsmedizinischen Rechtsvorschriften für KI-gestützte Recherche

Dieses Repository sammelt **automatisch** alle verlinkten Rechtsvorschriften von der offiziellen Website der [Arbeitsinspektion Österreich](https://www.arbeitsinspektion.gv.at/Service/Rechtsvorschriften/Rechtsvorschriften.html), wandelt HTML-Seiten in PDFs um und erstellt daraus intelligent aufgeteilte PDF-Dokumente, die perfekt für die Verwendung mit **Google NotebookLM** geeignet sind.

## 🌟 Was macht dieses Projekt besonders?

- ✅ **Vollautomatisch**: Läuft monatlich via GitHub Actions
- 📄 **Intelligente PDF-Erstellung**: HTML-Seiten werden sauber in PDFs konvertiert
- 🔄 **Intelligente Aufteilung**: PDFs werden nach Größe und Wortanzahl aufgeteilt (optimal für NotebookLM)
- 🗜️ **Optimierte Komprimierung**: Kleinere Dateien durch Ghostscript-Komprimierung
- 📋 **NotebookLM-ready**: Perfekt dimensioniert für KI-Analyse
- 🏷️ **Versionierung**: Automatische Releases mit Datumsmarkierung

## 🔧 Features im Detail

### 🤖 Automatisierung
- **Monatlicher Lauf**: Jeden 7. des Monats um 03:00 UTC
- **Manuelle Auslösung**: Jederzeit über GitHub Actions auslösbar
- **Automatische Bereinigung**: Behält nur die 2 neuesten Versionen

### 📊 Intelligente PDF-Verarbeitung
- **Größenlimit**: Maximal 190 MB pro PDF-Teil (NotebookLM-optimiert)
- **Wortlimit**: Maximal 490.000 Wörter pro PDF-Teil
- **Qualitätsoptimierung**: Automatische Komprimierung für bessere Performance

### 🌐 Robuste Web-Extraktion
- **User-Agent Spoofing**: Umgeht Bot-Schutz
- **Timeout-Handling**: Robuste Fehlerbehandlung
- **Link-Sammlung**: Automatische Erkennung aller relevanten Dokumente

## 📖 Verwendung mit Google NotebookLM

### 🎯 Was ist NotebookLM?
[Google NotebookLM](https://notebooklm.google.com/) ist ein KI-gestütztes Forschungstool, das Ihre Dokumente analysiert und als Wissensquelle für präzise Antworten nutzt. Perfekt für:
- ⚖️ **Juristische Recherche**
- 📋 **Compliance-Prüfungen** 
- 🎓 **Ausbildung & Schulungen**
- 💼 **Beratungstätigkeiten**

### 📥 Schritt-für-Schritt: PDFs zu NotebookLM hinzufügen

#### 1. 📋 PDFs herunterladen
1. Gehen Sie zu den [**Releases**](../../releases) dieses Repositories
2. Laden Sie die neueste Version herunter (erkennbar am Datum)
3. Sie erhalten mehrere PDF-Teile: `1_rechtsvorschriften_YYYY-MM-DD.pdf`, `2_rechtsvorschriften_YYYY-MM-DD.pdf`, etc.

#### 2. 🚀 NotebookLM starten
1. Besuchen Sie [**notebooklm.google.com**](https://notebooklm.google.com/)
2. Melden Sie sich mit Ihrem Google-Account an
3. Klicken Sie auf **"+ Neues Notizbuch"**

#### 3. 📁 Quellen hinzufügen
1. Klicken Sie auf **"Quellen"** → **"Hochladen"**
2. Wählen Sie **alle PDF-Teile** aus und laden Sie sie hoch
3. Warten Sie, bis NotebookLM alle Dokumente verarbeitet hat
4. ✅ **Fertig!** Sie haben jetzt Zugriff auf das gesamte österreichische Arbeitsrecht

#### 4. 💡 NotebookLM optimal nutzen

**🔍 Beispiel-Prompts für arbeitsmedizinische Recherche:**
```
"Welche Vorschriften gelten für Arbeitsplätze mit Bildschirmarbeit?"

"Welche Grenzwerte sind für Lärm am Arbeitsplatz definiert?"

"Was sind die Pflichten des Arbeitgebers bei der Gesundheitsüberwachung?"

"Welche besonderen Schutzbestimmungen gelten für schwangere Arbeitnehmerinnen?"
```

**📊 Nutzen Sie die Chat-Funktion für:**
- Gezielte Fragen zu spezifischen Vorschriften
- Vergleiche zwischen verschiedenen Regelungen
- Zusammenfassungen komplexer Rechtsbereiche
- Praktische Umsetzungshilfen

**🎵 Audio-Zusammenfassungen erstellen:**
- NotebookLM kann **Audio-Podcasts** aus den Dokumenten generieren
- Ideal für das Lernen unterwegs oder zur Vorbereitung von Schulungen

## 🖥️ Lokale Ausführung

### 📋 Voraussetzungen
```bash
# Ubuntu/Debian
sudo apt-get install wkhtmltopdf ghostscript

# macOS
brew install wkhtmltopdf ghostscript

# Python-Abhängigkeiten
pip install -r requirements.txt
```

### ▶️ Script ausführen
```bash
python pdf_downloader.py
```

Das Script erstellt automatisch:
- 📁 Einen `pdfs/` Ordner für Zwischendateien
- 📄 Aufgeteilte PDFs im Hauptverzeichnis: `1_rechtsvorschriften_YYYY-MM-DD.pdf`, etc.

## 🔄 GitHub Actions Workflow

### ⚙️ Automatische Ausführung
- **📅 Zeitplan**: Jeden 7. des Monats um 03:00 UTC
- **🚀 Manuell**: Über "Actions" → "PDF Downloader & Merger" → "Run workflow"

### 📦 Was passiert automatisch?
1. **🔄 Code auschecken**
2. **📦 Abhängigkeiten installieren** (wkhtmltopdf, Ghostscript, Python-Packages)
3. **🏃‍♂️ Script ausführen** und PDFs generieren
4. **📋 Release erstellen** mit allen PDF-Teilen
5. **🧹 Aufräumen**: Alte Releases löschen (behält die 2 neuesten)

### 📊 Ausgabe
Die generierten PDFs sind verfügbar als:
- **📋 GitHub Releases**: Einfach herunterzuladen
- **🏷️ Versioniert**: Nach Datum markiert
- **⚡ Sofort nutzbar**: Direkt für NotebookLM optimiert

## 📁 Projektstruktur

```
📦 rechtsvorschriften-arbeitsmedizin/
├── 📄 README.md                    # Diese Datei
├── 🐍 pdf_downloader.py           # Haupt-Script
├── 📋 requirements.txt            # Python-Abhängigkeiten
├── 📁 .github/workflows/
│   └── 🤖 main.yml               # GitHub Actions Workflow
└── 📁 pdfs/                      # Temporäre Dateien (gitignored)
```

## 🛠️ Technische Details

### 📊 PDF-Aufteilungslogik
```python
# Grenzen pro PDF-Teil
SIZE_LIMIT_MB = 190      # NotebookLM-optimiert
WORD_LIMIT = 490_000     # Optimale Verarbeitungsgeschwindigkeit
```

### 🔧 wkhtmltopdf Konfiguration
- **`no-images`**: Reduziert Dateigröße
- **Timeout**: 10 Sekunden pro Seite
- **User-Agent**: Verhindert Bot-Blocking

### 🗜️ Komprimierung
- **Ghostscript**: `-dPDFSETTINGS=/ebook` für optimale Balance zwischen Qualität und Größe
- **Automatisches Fallback**: Bei Komprimierungsfehlern wird die ursprüngliche Datei verwendet

## 🎯 Anwendungsfälle

### 👥 Für Arbeitsmediziner
- **📋 Compliance-Checks**: Schnelle Überprüfung aktueller Vorschriften
- **🎓 Weiterbildung**: Systematisches Lernen mit KI-Unterstützung
- **💼 Beratung**: Fundierte Antworten für Klienten

### 🏢 Für Unternehmen
- **⚖️ Rechtssicherheit**: Immer aktuelle Vorschriften verfügbar
- **👨‍🏫 Mitarbeiterschulung**: KI-gestützte Schulungsmaterialien
- **📊 Risikobewertung**: Systematische Analyse von Compliance-Anforderungen

### 🎓 Für Ausbildung
- **📚 Lehrmaterial**: Umfassende, durchsuchbare Wissensbasis
- **❓ Q&A-Sessions**: Interaktives Lernen mit NotebookLM
- **📝 Prüfungsvorbereitung**: Gezielte Wiederholung spezifischer Themen

## 🤝 Beitragen

Verbesserungsvorschläge sind willkommen! 
- 🐛 **Issues**: Für Bugs oder Feature-Requests
- 🔧 **Pull Requests**: Für Code-Verbesserungen
- 💡 **Diskussionen**: Für allgemeine Ideen

## 📜 Lizenz

MIT License - Frei verwendbar für alle Zwecke.

---

> 💡 **Tipp**: Kombinieren Sie die automatisch generierten PDFs mit NotebookLM für eine revolutionäre Art der Rechtsrecherche im Arbeitsschutz!

**📞 Support**: Bei Fragen öffnen Sie gerne ein [Issue](../../issues)
