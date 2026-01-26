from __future__ import annotations

from PySide6.QtWidgets import QWidget

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.i18n import t


class ToolPanel(QWidget):
    tool_id: str = ""
    title_key: str = ""

    @property
    def title(self) -> str:
        return t(self.title_key)

    def apply_language(self) -> None:
        return None

    def build_spec(self) -> JobSpec:
        raise NotImplementedError


