from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pdf_toolbox.core.job_queue import JobQueue
from pdf_toolbox.core.models import JobSpec
from pdf_toolbox.ui.tools_panels.compress_panel import CompressPanel
from pdf_toolbox.ui.tools_panels.convert_panels import ImagesToPdfPanel, PdfToImagesPanel, PptToPdfPanel
from pdf_toolbox.ui.tools_panels.delete_rotate_panel import DeleteRotatePanel
from pdf_toolbox.ui.tools_panels.merge_panel import MergePanel
from pdf_toolbox.ui.tools_panels.ocr_panel import OcrPanel
from pdf_toolbox.ui.tools_panels.reorder_panel import ReorderPanel
from pdf_toolbox.ui.tools_panels.split_panel import SplitPanel
from pdf_toolbox.ui.widgets.progress_list import ProgressList
from pdf_toolbox.services.io.validators import ValidationError


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF Toolbox Qt")
        self.resize(1000, 700)

        self.queue = JobQueue()
        self.queue.progress.connect(self._on_progress)
        self.queue.finished.connect(self._on_finished)

        self.tool_list = QListWidget()
        self.stack = QStackedWidget()
        self.progress_list = ProgressList()

        self._panels = [
            MergePanel(),
            SplitPanel(),
            DeleteRotatePanel(),
            ReorderPanel(),
            CompressPanel(),
            PdfToImagesPanel(),
            ImagesToPdfPanel(),
            PptToPdfPanel(),
            OcrPanel(),
        ]

        for panel in self._panels:
            self.tool_list.addItem(panel.title)
            self.stack.addWidget(panel)
            panel.run_btn.clicked.connect(lambda _, p=panel: self._submit(p))

        self.tool_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.tool_list.setCurrentRow(0)

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.tool_list, 1)
        top_layout.addWidget(self.stack, 4)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.progress_list)

        root = QWidget()
        root.setLayout(main_layout)
        self.setCentralWidget(root)

    def _submit(self, panel) -> None:
        try:
            spec = panel.build_spec()
            if not spec.inputs:
                raise ValidationError("未选择输入文件")
            if not spec.output_dir:
                raise ValidationError("未选择输出目录")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, "参数错误", str(exc))
            return

        job_id = self.queue.submit(spec)
        self.progress_list.add_job(job_id, panel.title, self.queue.cancel)

    def _on_progress(self, progress) -> None:
        self.progress_list.update_progress(progress)

    def _on_finished(self, job_id, result) -> None:
        self.progress_list.finish(job_id, result)
        if not result.success and not result.cancelled:
            QMessageBox.warning(self, "任务失败", result.error or "未知错误")
