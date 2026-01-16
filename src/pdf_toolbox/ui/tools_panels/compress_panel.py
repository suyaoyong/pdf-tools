from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QComboBox, QSpinBox, QCheckBox, QLabel, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions
from pdf_toolbox.ui.widgets.preset_picker import PresetPicker


class CompressPanel(ToolPanel):
    tool_id = "compress"
    title = "压缩"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.inputs = FilePicker("输入PDF", mode="files", filter_text="PDF Files (*.pdf)")

        self.mode = QComboBox()
        self.mode.addItem("基础压缩", "compress_basic")
        self.mode.addItem("图片重编码压缩", "compress_images")

        self.preset = PresetPicker()

        self.linearize = QCheckBox("线性化 (网络优化)")
        self.recompress = QCheckBox("重压缩流")
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

        self.grayscale = QCheckBox("灰度")

        self.output = OutputOptions()
        self.run_btn = QPushButton("开始压缩")

        layout.addWidget(self.inputs)
        layout.addWidget(self.mode)
        layout.addWidget(self.preset)
        layout.addWidget(self.linearize)
        layout.addWidget(self.recompress)
        layout.addWidget(QLabel("图片压缩参数"))
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


