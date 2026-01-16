from __future__ import annotations

from typing import List

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox

from pdf_toolbox.core.presets import Preset, PresetStore


class PresetPicker(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("预设")
        self.combo = QComboBox()
        self.combo.addItem("无", None)

        self._presets: List[Preset] = PresetStore().load()
        for preset in self._presets:
            self.combo.addItem(preset.name, preset)

        layout.addWidget(self.label)
        layout.addWidget(self.combo, 1)

    def current(self) -> Preset | None:
        return self.combo.currentData()


