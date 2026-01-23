from __future__ import annotations

import sys
from pathlib import Path

APP_NAME = "PDF Toolbox Qt"
APP_ID = "pdf-toolbox-qt"

if getattr(sys, "frozen", False):
    base_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
else:
    base_dir = Path(__file__).resolve().parents[2]

BASE_DIR = base_dir
ASSETS_DIR = BASE_DIR / "assets"

DEFAULT_OUTPUT_DIR = Path.home() / "Documents" / "PDFToolbox"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_TEMP_DIR = Path.home() / ".pdf_toolbox_tmp"
DEFAULT_TEMP_DIR.mkdir(parents=True, exist_ok=True)


