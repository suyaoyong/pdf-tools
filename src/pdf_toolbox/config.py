from __future__ import annotations

from pathlib import Path

APP_NAME = "PDF Toolbox Qt"
APP_ID = "pdf-toolbox-qt"

BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"

DEFAULT_OUTPUT_DIR = Path.home() / "Documents" / "PDFToolbox"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_TEMP_DIR = Path.home() / ".pdf_toolbox_tmp"
DEFAULT_TEMP_DIR.mkdir(parents=True, exist_ok=True)


