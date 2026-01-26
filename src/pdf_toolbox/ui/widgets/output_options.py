from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox

from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.config import DEFAULT_OUTPUT_DIR
from pdf_toolbox.i18n import t


class OutputOptions(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.output_dir = FilePicker("label_output_dir", mode="dir")
        self.output_dir.set_path(str(DEFAULT_OUTPUT_DIR))

        name_row = QHBoxLayout()
        self.name_label = QLabel(t("label_output_name_optional"))
        name_row.addWidget(self.name_label)
        self.output_name = QLineEdit()
        name_row.addWidget(self.output_name, 1)

        self.overwrite = QCheckBox(t("label_overwrite"))

        layout.addWidget(self.output_dir)
        layout.addLayout(name_row)
        layout.addWidget(self.overwrite)

    def output_dir_path(self):
        return self.output_dir.path()

    def output_name_text(self) -> str:
        return self.output_name.text().strip() or None

    def overwrite_checked(self) -> bool:
        return self.overwrite.isChecked()

    def apply_language(self) -> None:
        self.output_dir.apply_language()
        self.name_label.setText(t("label_output_name_optional"))
        self.overwrite.setText(t("label_overwrite"))


