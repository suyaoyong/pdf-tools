from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QSpinBox, QVBoxLayout

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.i18n import t
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions


class PdfToImagesPanel(ToolPanel):
    tool_id = "pdf_to_images"
    title_key = "panel_pdf_to_images"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.pdf_inputs = FilePicker("label_input_pdf", mode="files", filter_text="PDF Files (*.pdf)")

        self.dpi = QSpinBox()
        self.dpi.setRange(72, 600)
        self.dpi.setValue(150)
        self.dpi.setSuffix(" dpi")

        self.format = QComboBox()
        self.format.addItem("PNG", "png")
        self.format.addItem("JPG", "jpg")

        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_convert"))
        self.options_label = QLabel(t("label_pdf_to_images_options"))

        layout.addWidget(self.pdf_inputs)
        layout.addWidget(self.options_label)
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

    def apply_language(self) -> None:
        self.pdf_inputs.apply_language()
        self.output.apply_language()
        self.options_label.setText(t("label_pdf_to_images_options"))
        self.run_btn.setText(t("btn_start_convert"))


class ImagesToPdfPanel(ToolPanel):
    tool_id = "images_to_pdf"
    title_key = "panel_images_to_pdf"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.image_inputs = FilePicker(
            "label_input_images", mode="files", filter_text="Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        self.page_size = QComboBox()
        self.page_size.addItem("A4", "a4")
        self.page_size.addItem("Letter", "letter")
        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_convert"))
        self.page_size_label = QLabel(t("label_page_size"))

        layout.addWidget(self.image_inputs)
        layout.addWidget(self.page_size_label)
        layout.addWidget(self.page_size)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.image_inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={"page_size": self.page_size.currentData()},
            overwrite=self.output.overwrite_checked(),
        )

    def apply_language(self) -> None:
        self.image_inputs.apply_language()
        self.page_size_label.setText(t("label_page_size"))
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_convert"))


class PptToPdfPanel(ToolPanel):
    tool_id = "ppt_to_pdf"
    title_key = "panel_ppt_to_pdf"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.ppt_inputs = FilePicker(
            "label_input_ppt", mode="files", filter_text="PowerPoint Files (*.ppt *.pptx *.pps *.ppsx)"
        )
        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_convert"))

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

    def apply_language(self) -> None:
        self.ppt_inputs.apply_language()
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_convert"))
