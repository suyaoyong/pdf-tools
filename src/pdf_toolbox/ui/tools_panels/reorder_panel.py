from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.range_input import RangeInput
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class ReorderPanel(ToolPanel):
    tool_id = "reorder_pages"
    title = "重排"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.input_pdf = FilePicker("输入PDF", mode="files", filter_text="PDF Files (*.pdf)")
        self.order_input = RangeInput("新顺序", "3,1,2,4-6")
        self.output = OutputOptions()
        self.run_btn = QPushButton("开始重排")

        layout.addWidget(self.input_pdf)
        layout.addWidget(self.order_input)
        layout.addWidget(QLabel("提示: 顺序必须覆盖所有页且不重复"))
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


