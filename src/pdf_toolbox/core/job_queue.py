from __future__ import annotations

import logging
import uuid
from typing import Dict

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

from pdf_toolbox.core.models import JobProgress, JobResult, JobSpec
from pdf_toolbox.core.cancel import CancellationToken
from pdf_toolbox.core.range_parser import RangeParseError
from pdf_toolbox.services.io.validators import ValidationError
from pdf_toolbox.services.pdf_ops import get_operation

logger = logging.getLogger(__name__)

try:
    import pikepdf
except Exception:  # noqa: BLE001
    pikepdf = None

try:
    import fitz
except Exception:  # noqa: BLE001
    fitz = None


class JobSignals(QObject):
    progress = Signal(JobProgress)
    finished = Signal(str, JobResult)


class JobWorker(QRunnable):
    def __init__(self, job_id: str, spec: JobSpec, token: CancellationToken, signals: JobSignals) -> None:
        super().__init__()
        self.job_id = job_id
        self.spec = spec
        self.token = token
        self.signals = signals

    def run(self) -> None:
        try:
            if self.token.is_cancelled():
                self.signals.finished.emit(self.job_id, JobResult(success=False, cancelled=True, error="任务已取消"))
                return
            op = get_operation(self.spec.tool_id)
            op.validate(self.spec)
            result = op.run(self.spec, self._progress, self.token)
            self.signals.finished.emit(self.job_id, result)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Job failed: %s", self.job_id)
            message = _friendly_error(exc)
            self.signals.finished.emit(
                self.job_id, JobResult(success=False, error=message, cancelled=self.token.is_cancelled())
            )

    def _progress(self, stage: str, current: int, total: int, message: str = "") -> None:
        self.signals.progress.emit(JobProgress(self.job_id, stage, current, total, message))


class JobQueue(QObject):
    progress = Signal(JobProgress)
    finished = Signal(str, JobResult)

    def __init__(self) -> None:
        super().__init__()
        self._pool = QThreadPool.globalInstance()
        self._tokens: Dict[str, CancellationToken] = {}
        self._signals = JobSignals()
        self._signals.progress.connect(self.progress)
        self._signals.finished.connect(self._on_finished)

    def submit(self, spec: JobSpec) -> str:
        job_id = uuid.uuid4().hex
        token = CancellationToken()
        self._tokens[job_id] = token
        worker = JobWorker(job_id, spec, token, self._signals)
        self._pool.start(worker)
        return job_id

    def cancel(self, job_id: str) -> None:
        token = self._tokens.get(job_id)
        if token:
            token.cancel()

    def _on_finished(self, job_id: str, result: JobResult) -> None:
        self._tokens.pop(job_id, None)
        self.finished.emit(job_id, result)


def _friendly_error(exc: Exception) -> str:
    if isinstance(exc, ValidationError):
        return str(exc)
    if isinstance(exc, RangeParseError):
        return f"页码范围错误: {exc}"
    if pikepdf and isinstance(exc, pikepdf.PasswordError):
        return "文件已加密，无法处理。请先解密或输入正确密码。"
    if pikepdf and isinstance(exc, pikepdf.PdfError):
        return "PDF 文件可能已损坏或格式不受支持。"
    if fitz and isinstance(exc, fitz.FileDataError):
        return "PDF 文件可能已损坏或无法读取。"
    if isinstance(exc, PermissionError):
        return "权限不足，无法读取或写入文件。请检查权限或关闭占用程序。"
    if isinstance(exc, FileNotFoundError):
        return "文件不存在或路径无效。"
    if isinstance(exc, IsADirectoryError):
        return "选择了目录而不是文件。"
    return str(exc)


