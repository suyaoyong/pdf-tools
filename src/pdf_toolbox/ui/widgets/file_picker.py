from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog


class FilePicker(QWidget):
    def __init__(self, label: str, mode: str = "file", filter_text: str = "All Files (*)") -> None:
        super().__init__()
        self.mode = mode
        self.filter_text = filter_text

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label)
        self.edit = QLineEdit()
        self.button = QPushButton("浏览")

        self.button.clicked.connect(self._on_browse)

        layout.addWidget(self.label)
        layout.addWidget(self.edit, 1)
        layout.addWidget(self.button)

    def _on_browse(self) -> None:
        if self.mode == "dir":
            path = QFileDialog.getExistingDirectory(self, "选择目录")
            if path:
                self.edit.setText(path)
        elif self.mode == "files":
            paths, _ = QFileDialog.getOpenFileNames(self, "选择文件", filter=self.filter_text)
            if paths:
                self.edit.setText(";".join(paths))
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", filter=self.filter_text)
            if path:
                self.edit.setText(path)

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


