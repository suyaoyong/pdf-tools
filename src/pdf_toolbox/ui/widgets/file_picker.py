from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

from pdf_toolbox.i18n import t


class FilePicker(QWidget):
    def __init__(self, label_key: str, mode: str = "file", filter_text: str = "All Files (*)") -> None:
        super().__init__()
        self.mode = mode
        self.filter_text = filter_text
        self.label_key = label_key

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(t(label_key))
        self.edit = QLineEdit()
        self.button = QPushButton(t("browse"))

        self.button.clicked.connect(self._on_browse)

        layout.addWidget(self.label)
        layout.addWidget(self.edit, 1)
        layout.addWidget(self.button)

    def _on_browse(self) -> None:
        if self.mode == "dir":
            path = QFileDialog.getExistingDirectory(self, t("select_folder"))
            if path:
                self.edit.setText(path)
        elif self.mode == "files":
            paths, _ = QFileDialog.getOpenFileNames(self, t("select_files"), filter=self.filter_text)
            if paths:
                self.edit.setText(";".join(paths))
        else:
            path, _ = QFileDialog.getOpenFileName(self, t("select_file"), filter=self.filter_text)
            if path:
                self.edit.setText(path)

    def apply_language(self) -> None:
        self.label.setText(t(self.label_key))
        self.button.setText(t("browse"))

    def paths(self) -> List[Path]:
        text = self.edit.text().strip()
        if not text:
            return []
        return [Path(p) for p in text.split(";") if p]

    def path(self) -> Optional[Path]:
        paths = self.paths()
        return paths[0] if paths else None

    def set_path(self, path: str) -> None:
        self.edit.setText(path)


