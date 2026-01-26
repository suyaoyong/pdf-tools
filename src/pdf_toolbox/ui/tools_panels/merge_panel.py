from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton

from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.base import ToolPanel
from pdf_toolbox.ui.widgets.file_picker import FilePicker
from pdf_toolbox.ui.widgets.output_options import OutputOptions
from pdf_toolbox.i18n import t


class MergePanel(ToolPanel):
    tool_id = "merge"
    title_key = "panel_merge"

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.inputs = FilePicker("label_input_pdf", mode="files", filter_text="PDF Files (*.pdf)")
        self.keep_bookmarks = QCheckBox(t("label_keep_bookmarks"))
        self.output = OutputOptions()
        self.run_btn = QPushButton(t("btn_start_merge"))

        layout.addWidget(self.inputs)
        layout.addWidget(self.keep_bookmarks)
        layout.addWidget(self.output)
        layout.addWidget(self.run_btn)

    def apply_language(self) -> None:
        self.inputs.apply_language()
        self.keep_bookmarks.setText(t("label_keep_bookmarks"))
        self.output.apply_language()
        self.run_btn.setText(t("btn_start_merge"))

    def build_spec(self) -> JobSpec:
        return JobSpec(
            tool_id=self.tool_id,
            inputs=self.inputs.paths(),
            output_dir=self.output.output_dir_path(),
            output_name=self.output.output_name_text(),
            params={"keep_bookmarks": self.keep_bookmarks.isChecked()},
            overwrite=self.output.overwrite_checked(),
        )


