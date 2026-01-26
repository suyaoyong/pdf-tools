from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QSpinBox, QCheckBox, QLabel, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions
from pdf_toolbox.ui.widgets.preset_picker import PresetPicker
from pdf_toolbox.i18n import t


class CompressPanel(ToolPanel):
    tool_id = "compress"
    title_key = "panel_compress"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.inputs = FilePicker("label_input_pdf", mode="files", filter_text="PDF Files (*.pdf)")

        self.mode = QComboBox()
        self.mode.addItem(t("label_basic_compress"), "compress_basic")
        self.mode.addItem(t("label_image_reencode"), "compress_images")

        self.preset = PresetPicker()

        self.linearize = QCheckBox(t("label_linearize"))
        self.recompress = QCheckBox(t("label_recompress"))
        self.recompress.setChecked(True)

        self.dpi = QSpinBox()
        self.dpi.setRange(72, 600)
        self.dpi.setValue(150)
        self.dpi.setSuffix(" dpi")

        self.quality = QSpinBox()
        self.quality.setRange(30, 95)
        self.quality.setValue(75)

        self.max_side = QSpinBox()
        self.max_side.setRange(500, 5000)
        self.max_side.setValue(1600)

        self.grayscale = QCheckBox(t("label_grayscale"))

        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_compress"))
        self.image_label = QLabel(t("label_image_compress_options"))

        layout.addWidget(self.inputs)
        layout.addWidget(self.mode)
        layout.addWidget(self.preset)
        layout.addWidget(self.linearize)
        layout.addWidget(self.recompress)
        layout.addWidget(self.image_label)
        layout.addWidget(self.dpi)
        layout.addWidget(self.quality)
        layout.addWidget(self.max_side)
        layout.addWidget(self.grayscale)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

        self.mode.currentIndexChanged.connect(self._toggle_fields)
        self._toggle_fields()

    def _toggle_fields(self) -> None:
        is_image = self.mode.currentData() == "compress_images"
        self.dpi.setEnabled(is_image)
        self.quality.setEnabled(is_image)
        self.max_side.setEnabled(is_image)
        self.grayscale.setEnabled(is_image)
        self.linearize.setEnabled(not is_image)
        self.recompress.setEnabled(not is_image)

    def build_spec(self) -> JobSpec:
        preset = self.preset.current()
        tool_id = self.mode.currentData()
        params = {}
        if preset:
            tool_id = preset.tool_id
            params.update(preset.params)
        if tool_id == "compress_basic":
            params.update({
                "linearize": self.linearize.isChecked(),
                "recompress_streams": self.recompress.isChecked(),
            })
        else:
            params.update({
                "dpi": self.dpi.value(),
                "jpeg_quality": self.quality.value(),
                "max_side": self.max_side.value(),
                "grayscale": self.grayscale.isChecked(),
            })
        return JobSpec(
            tool_id=tool_id,
            inputs=self.inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params=params,
            overwrite=self.output.overwrite_checked(),
        )

    def apply_language(self) -> None:
        self.inputs.apply_language()
        self.mode.setItemText(0, t("label_basic_compress"))
        self.mode.setItemText(1, t("label_image_reencode"))
        self.preset.apply_language()
        self.linearize.setText(t("label_linearize"))
        self.recompress.setText(t("label_recompress"))
        self.grayscale.setText(t("label_grayscale"))
        self.image_label.setText(t("label_image_compress_options"))
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_compress"))


