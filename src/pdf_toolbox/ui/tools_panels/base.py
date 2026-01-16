from __future__ import annotations

from PySide6.QtWidgets import QWidget

from pdf_toolbox.core.models import JobSpec


class ToolPanel(QWidget):
    tool_id: str = ""
    title: str = ""

    def build_spec(self) -> JobSpec:
        raise NotImplementedError


