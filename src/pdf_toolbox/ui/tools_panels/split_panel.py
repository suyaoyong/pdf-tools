from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.range_input import RangeInput
from pdf_toolbox.ui.widgets.output_options import OutputOptions
from pdf_toolbox.i18n import t


class SplitPanel(ToolPanel):
    tool_id = "split_extract"
    title_key = "panel_split_extract"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.input_pdf = FilePicker("label_input_pdf", mode="files", filter_text="PDF Files (*.pdf)")
        self.range_input = RangeInput()
        self.mode = QComboBox()
        self.mode.addItem(t("option_extract_one_pdf"), "extract_one")
        self.mode.addItem(t("option_split_many_pdf"), "split_many")

        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_split_extract"))

        layout.addWidget(self.input_pdf)
        layout.addWidget(self.range_input)
        layout.addWidget(self.mode)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def apply_language(self) -> None:
        self.input_pdf.apply_language()
        self.range_input.apply_language()
        self.mode.setItemText(0, t("option_extract_one_pdf"))
        self.mode.setItemText(1, t("option_split_many_pdf"))
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_split_extract"))

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.input_pdf.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={"ranges": self.range_input.text(), "mode": self.mode.currentData()},
            overwrite=self.output.overwrite_checked(),
        )


