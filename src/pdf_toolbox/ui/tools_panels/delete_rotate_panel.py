from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.range_input import RangeInput
from pdf_toolbox.ui.widgets.output_options import OutputOptions
from pdf_toolbox.i18n import t


class DeleteRotatePanel(ToolPanel):
    tool_id = "delete_rotate"
    title_key = "panel_delete_rotate"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.input_pdf = FilePicker("label_input_pdf", mode="files", filter_text="PDF Files (*.pdf)")
        self.range_input = RangeInput()

        self.action = QComboBox()
        self.action.addItem(t("option_delete_pages"), "delete_pages")
        self.action.addItem(t("option_rotate_pages"), "rotate_pages")

        self.angle = QComboBox()
        self.angle.addItem("90°", 90)
        self.angle.addItem("180°", 180)
        self.angle.addItem("270°", 270)

        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_execute"))

        layout.addWidget(self.input_pdf)
        layout.addWidget(self.range_input)
        layout.addWidget(self.action)
        layout.addWidget(self.angle)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def apply_language(self) -> None:
        self.input_pdf.apply_language()
        self.range_input.apply_language()
        self.action.setItemText(0, t("option_delete_pages"))
        self.action.setItemText(1, t("option_rotate_pages"))
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_execute"))

    def build_spec(self) -> JobSpec:
        tool_id = self.action.currentData()
        params = {"ranges": self.range_input.text()}
        if tool_id == "rotate_pages":
            params["angle"] = self.angle.currentData()
        return JobSpec(
            tool_id=tool_id,
            inputs=self.input_pdf.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params=params,
            overwrite=self.output.overwrite_checked(),
        )


