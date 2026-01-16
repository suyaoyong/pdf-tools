from __future__ import annotations

from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QProgressBar, QPushButton

from pdf_toolbox.core.models import JobProgress, JobResult


class ProgressList(QTableWidget):
    def __init__(self) -> None:
        super().__init__(0, 4)
        self.setHorizontalHeaderLabels(["任务", "进度", "状态", "操作"])
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 260)
        self.setColumnWidth(3, 80)
        self._rows: Dict[str, int] = {}
        self._cancel_callbacks: Dict[str, callable] = {}

    def add_job(self, job_id: str, title: str, cancel_cb) -> None:
        row = self.rowCount()
        self.insertRow(row)
        self._rows[job_id] = row
        self._cancel_callbacks[job_id] = cancel_cb

        self.setItem(row, 0, QTableWidgetItem(title))
        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        self.setCellWidget(row, 1, progress)
        self.setItem(row, 2, QTableWidgetItem("等待中"))

        btn = QPushButton("取消")
        btn.clicked.connect(lambda: cancel_cb(job_id))
        self.setCellWidget(row, 3, btn)

    def update_progress(self, progress: JobProgress) -> None:
        row = self._rows.get(progress.job_id)
        if row is None:
            return
        bar = self.cellWidget(row, 1)
        if isinstance(bar, QProgressBar) and progress.total > 0:
            value = int(progress.current * 100 / progress.total)
            bar.setValue(value)
        status = f"{progress.stage}: {progress.message}" if progress.message else progress.stage
        item = self.item(row, 2)
        if item:
            item.setText(status)

    def finish(self, job_id: str, result: JobResult) -> None:
        row = self._rows.get(job_id)
        if row is None:
            return
        bar = self.cellWidget(row, 1)
        if isinstance(bar, QProgressBar):
            bar.setValue(100 if result.success else 0)
        item = self.item(row, 2)
        if item:
            if result.cancelled:
                item.setText("已取消")
            elif result.success:
                item.setText("完成")
            else:
                item.setText(result.error or "失败")
        btn = self.cellWidget(row, 3)
        if isinstance(btn, QPushButton):
            btn.setEnabled(False)


