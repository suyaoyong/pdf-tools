from __future__ import annotations

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

from pdf_toolbox.i18n import t


class RangeInput(QWidget):
    def __init__(self, label_key: str = "label_page_range", placeholder_key: str = "placeholder_page_range") -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label_key = label_key
        self.placeholder_key = placeholder_key

        self.label = QLabel(t(label_key))
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(t(placeholder_key))

        layout.addWidget(self.label)
        layout.addWidget(self.edit, 1)

    def text(self) -> str:
        return self.edit.text().strip()

    def apply_language(self) -> None:
        self.label.setText(t(self.label_key))
        self.edit.setPlaceholderText(t(self.placeholder_key))


