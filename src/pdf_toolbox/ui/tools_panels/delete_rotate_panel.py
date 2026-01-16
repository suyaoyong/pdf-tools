from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.range_input import RangeInput
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class DeleteRotatePanel(ToolPanel):
    tool_id = "delete_rotate"
    title = "删除/旋转"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.input_pdf = FilePicker("输入PDF", mode="files", filter_text="PDF Files (*.pdf)")
        self.range_input = RangeInput()

        self.action = QComboBox()
        self.action.addItem("删除页", "delete_pages")
        self.action.addItem("旋转页", "rotate_pages")

        self.angle = QComboBox()
        self.angle.addItem("90°", 90)
        self.angle.addItem("180°", 180)
        self.angle.addItem("270°", 270)

        self.output = OutputOptions()
        self.run_btn = QPushButton("开始执行")

        layout.addWidget(self.input_pdf)
        layout.addWidget(self.range_input)
        layout.addWidget(self.action)
        layout.addWidget(self.angle)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

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


