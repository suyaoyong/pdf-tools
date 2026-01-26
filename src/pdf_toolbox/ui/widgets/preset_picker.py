from __future__ import annotations

from typing import List

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox

from pdf_toolbox.core.presets import Preset, PresetStore
from pdf_toolbox.i18n import t


class PresetPicker(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(t("label_preset"))
        self.combo = QComboBox()
        self.combo.addItem(t("label_preset_none"), None)

        self._presets: List[Preset] = PresetStore().load()
        for preset in self._presets:
            self.combo.addItem(preset.name, preset)

        layout.addWidget(self.label)
        layout.addWidget(self.combo, 1)

    def current(self) -> Preset | None:
        return self.combo.currentData()

    def apply_language(self) -> None:
        self.label.setText(t("label_preset"))
        self.combo.setItemText(0, t("label_preset_none"))


