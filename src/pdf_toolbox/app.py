from __future__ import annotations

import sys
from pathlib import Path

# Allow running app.py directly in VSCode without installing the package
_src_root = Path(__file__).resolve().parents[1]
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from PySide6.QtWidgets import QApplication

from pdf_toolbox.logging_conf import setup_logging
from pdf_toolbox.ui.main_window import MainWindow


def main() -> int:
    setup_logging()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
