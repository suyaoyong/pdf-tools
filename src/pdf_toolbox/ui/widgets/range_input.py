from __future__ import annotations

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit


class RangeInput(QWidget):
    def __init__(self, label: str = "页码范围", placeholder: str = "1-3,8,10-12") -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(placeholder)

        layout.addWidget(self.label)
        layout.addWidget(self.edit, 1)

    def text(self) -> str:
        return self.edit.text().strip()


