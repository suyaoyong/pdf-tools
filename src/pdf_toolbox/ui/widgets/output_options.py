from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox

from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.config import DEFAULT_OUTPUT_DIR


class OutputOptions(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.output_dir = FilePicker("输出目录", mode="dir")
        self.output_dir.set_path(str(DEFAULT_OUTPUT_DIR))

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("输出名(可选)"))
        self.output_name = QLineEdit()
        name_row.addWidget(self.output_name, 1)

        self.overwrite = QCheckBox("覆盖已存在文件（否则自动改名）")

        layout.addWidget(self.output_dir)
        layout.addLayout(name_row)
        layout.addWidget(self.overwrite)

    def output_dir_path(self):
        return self.output_dir.path()

    def output_name_text(self) -> str:
        return self.output_name.text().strip() or None

    def overwrite_checked(self) -> bool:
        return self.overwrite.isChecked()


