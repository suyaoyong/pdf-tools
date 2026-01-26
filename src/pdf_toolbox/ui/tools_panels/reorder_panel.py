from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.range_input import RangeInput
from pdf_toolbox.ui.widgets.output_options import OutputOptions
from pdf_toolbox.i18n import t


class ReorderPanel(ToolPanel):
    tool_id = "reorder_pages"
    title_key = "panel_reorder"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.input_pdf = FilePicker("label_input_pdf", mode="files", filter_text="PDF Files (*.pdf)")
        self.order_input = RangeInput("label_new_order", "placeholder_new_order")
        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_reorder"))
        self.tip_label = QLabel(t("label_tip_reorder"))

        layout.addWidget(self.input_pdf)
        layout.addWidget(self.order_input)
        layout.addWidget(self.tip_label)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.input_pdf.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={"order": self.order_input.text()},
            overwrite=self.output.overwrite_checked(),
        )

    def apply_language(self) -> None:
        self.input_pdf.apply_language()
        self.order_input.apply_language()
        self.tip_label.setText(t("label_tip_reorder"))
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_reorder"))


