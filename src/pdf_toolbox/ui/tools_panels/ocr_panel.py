from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.i18n import t
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class OcrPanel(ToolPanel):
    tool_id = "ocr"
    title_key = "panel_ocr"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.inputs = FilePicker("label_input_file", mode="files", filter_text="PDF (*.pdf)")
        self.output = OutputOptions()

        opt_row = QHBoxLayout()
        self.dpi_label = QLabel(t("label_dpi"))
        opt_row.addWidget(self.dpi_label)
        self.dpi = QSpinBox()
        self.dpi.setRange(100, 600)
        self.dpi.setValue(300)
        opt_row.addWidget(self.dpi)

        self.lang_label = QLabel(t("label_language"))
        opt_row.addWidget(self.lang_label)
        self.lang = QLineEdit()
        self.lang.setText("chi_sim+eng")
        opt_row.addWidget(self.lang, 1)

        self.out_pdf = QCheckBox(t("label_output_searchable_pdf"))
        self.out_pdf.setChecked(True)
        self.out_docx = QCheckBox(t("label_output_word"))
        self.out_docx.setChecked(True)
        self.run_btn = QPushButton(t("btn_start_ocr"))

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

    def apply_language(self) -> None:
        self.inputs.apply_language()
        self.output.apply_language()
        self.dpi_label.setText(t("label_dpi"))
        self.lang_label.setText(t("label_language"))
        self.out_pdf.setText(t("label_output_searchable_pdf"))
        self.out_docx.setText(t("label_output_word"))
        self.run_btn.setText(t("btn_start_ocr"))
