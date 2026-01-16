from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QSpinBox, QVBoxLayout

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class PdfToImagesPanel(ToolPanel):
    tool_id = "pdf_to_images"
    title = "PDF -> 图片"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.pdf_inputs = FilePicker("输入PDF", mode="files", filter_text="PDF Files (*.pdf)")

        self.dpi = QSpinBox()
        self.dpi.setRange(72, 600)
        self.dpi.setValue(150)
        self.dpi.setSuffix(" dpi")

        self.format = QComboBox()
        self.format.addItem("PNG", "png")
        self.format.addItem("JPG", "jpg")

        self.output = OutputOptions()
        self.run_btn = QPushButton("开始转换")

        layout.addWidget(self.pdf_inputs)
        layout.addWidget(QLabel("PDF -> 图片 参数"))
        layout.addWidget(self.dpi)
        layout.addWidget(self.format)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.pdf_inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={"dpi": self.dpi.value(), "format": self.format.currentData()},
            overwrite=self.output.overwrite_checked(),
        )


class ImagesToPdfPanel(ToolPanel):
    tool_id = "images_to_pdf"
    title = "图片 -> PDF"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.image_inputs = FilePicker(
            "输入图片", mode="files", filter_text="Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        self.output = OutputOptions()
        self.run_btn = QPushButton("开始转换")

        layout.addWidget(self.image_inputs)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.image_inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={},
            overwrite=self.output.overwrite_checked(),
        )


class PptToPdfPanel(ToolPanel):
    tool_id = "ppt_to_pdf"
    title = "PPT -> PDF"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.ppt_inputs = FilePicker(
            "输入PPT", mode="files", filter_text="PowerPoint Files (*.ppt *.pptx *.pps *.ppsx)"
        )
        self.output = OutputOptions()
        self.run_btn = QPushButton("开始转换")

        layout.addWidget(self.ppt_inputs)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.ppt_inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={},
            overwrite=self.output.overwrite_checked(),
        )
