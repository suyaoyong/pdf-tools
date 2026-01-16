from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.range_input import RangeInput
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class SplitPanel(ToolPanel):
    tool_id = "split_extract"
    title = "拆分/提取"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.input_pdf = FilePicker("输入PDF", mode="files", filter_text="PDF Files (*.pdf)")
        self.range_input = RangeInput()
        self.mode = QComboBox()
        self.mode.addItem("提取为单个PDF", "extract_one")
        self.mode.addItem("按页拆分多个PDF", "split_many")

        self.output = OutputOptions()
        self.run_btn = QPushButton("开始拆分/提取")

        layout.addWidget(self.input_pdf)
        layout.addWidget(self.range_input)
        layout.addWidget(self.mode)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.input_pdf.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={"ranges": self.range_input.text(), "mode": self.mode.currentData()},
            overwrite=self.output.overwrite_checked(),
        )


