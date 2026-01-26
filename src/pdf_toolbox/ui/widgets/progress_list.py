from __future__ import annotations

from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from pdf_toolbox.core.models import JobProgress, JobResult
from pdf_toolbox.i18n import t


class ProgressList(QTableWidget):
    def __init__(self) -> None:
        super().__init__(0, 4)
        self.setHorizontalHeaderLabels(
            [t("header_task"), t("header_progress"), t("header_status"), t("header_action")]
        )
        self.setColumnWidth(0, 180)
        self.setColumnWidth(1, 140)
        self.setColumnWidth(2, 220)
        self.setColumnWidth(3, 70)
        self.horizontalHeader().setFixedHeight(24)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(26)
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
        self.setItem(row, 2, QTableWidgetItem(t("status_waiting")))

        btn = QPushButton(t("action_cancel"))
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
        stage = _translate_stage(progress.stage)
        status = f"{stage}: {progress.message}" if progress.message else stage
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
                item.setText(t("status_cancelled"))
            elif result.success:
                item.setText(t("status_completed"))
            else:
                item.setText(result.error or t("status_failed"))
        btn = self.cellWidget(row, 3)
        if isinstance(btn, QPushButton):
            btn.setEnabled(False)

    def apply_language(self) -> None:
        self.setHorizontalHeaderLabels(
            [t("header_task"), t("header_progress"), t("header_status"), t("header_action")]
        )
        for row in range(self.rowCount()):
            item = self.item(row, 2)
            if item:
                item.setText(_translate_status(item.text()))
            btn = self.cellWidget(row, 3)
            if isinstance(btn, QPushButton):
                btn.setText(t("action_cancel"))


def _translate_stage(stage: str) -> str:
    stages = {
        "processing": t("stage_processing"),
        "writing": t("stage_writing"),
    }
    return stages.get(stage, stage)


def _translate_status(status: str) -> str:
    map_keys = {
        "Waiting": "status_waiting",
        "等待中": "status_waiting",
        "Cancelled": "status_cancelled",
        "已取消": "status_cancelled",
        "Completed": "status_completed",
        "完成": "status_completed",
        "Failed": "status_failed",
        "失败": "status_failed",
    }
    key = map_keys.get(status)
    return t(key) if key else status


