from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class OcrPanel(ToolPanel):
    tool_id = "ocr"
    title = "OCR 识别"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.inputs = FilePicker("输入文件", mode="files", filter_text="PDF (*.pdf)")
        self.output = OutputOptions()

        opt_row = QHBoxLayout()
        opt_row.addWidget(QLabel("DPI"))
        self.dpi = QSpinBox()
        self.dpi.setRange(100, 600)
        self.dpi.setValue(300)
        opt_row.addWidget(self.dpi)

        opt_row.addWidget(QLabel("语言"))
        self.lang = QLineEdit()
        self.lang.setText("chi_sim+eng")
        opt_row.addWidget(self.lang, 1)

        self.out_pdf = QCheckBox("输出可搜索 PDF")
        self.out_pdf.setChecked(True)
        self.out_docx = QCheckBox("输出 Word")
        self.out_docx.setChecked(True)
        self.run_btn = QPushButton("开始识别")

        layout.addWidget(self.inputs)
        layout.addLayout(opt_row)
        layout.addWidget(self.out_pdf)
        layout.addWidget(self.out_docx)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={
                "dpi": self.dpi.value(),
                "lang": self.lang.text().strip() or "chi_sim+eng",
                "output_pdf": self.out_pdf.isChecked(),
                "output_docx": self.out_docx.isChecked(),
            },
            overwrite=self.output.overwrite_checked(),
        )
