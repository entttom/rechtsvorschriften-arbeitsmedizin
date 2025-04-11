# Rechtsvorschriften PDF Downloader

Dieses Repository lädt automatisch alle verlinkten Rechtsvorschriften von [arbeitsinspektion.gv.at](https://www.arbeitsinspektion.gv.at/Service/Rechtsvorschriften/Rechtsvorschriften.html), wandelt HTML-Seiten in PDFs um, lädt PDF-Dateien direkt herunter und kombiniert sie zu einem einzigen PDF-Dokument.

## Features

- Automatischer PDF-Download via GitHub Actions
- HTML-Seiten werden mit `wkhtmltopdf` gerendert
- Kombinierte Datei wird als Artefakt bereitgestellt

## Lokale Ausführung

```bash
pip install -r requirements.txt
python pdf_downloader.py
```

## GitHub Actions

Das Script wird automatisch:
- bei jedem manuellen Start (`workflow_dispatch`)
- täglich um 05:00 UTC (`cron`)

Ergebnis: eine kombinierte PDF als Artefakt im Workflow.

## Lizenz

MIT
