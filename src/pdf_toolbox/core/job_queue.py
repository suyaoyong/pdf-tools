from __future__ import annotations

import logging
import uuid
from typing import Dict

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

from pdf_toolbox.core.models import JobProgress, JobResult, JobSpec
from pdf_toolbox.core.cancel import CancellationToken
from pdf_toolbox.core.range_parser import RangeParseError
from pdf_toolbox.i18n import t
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
                self.signals.finished.emit(
                    self.job_id, JobResult(success=False, cancelled=True, error=t("err_cancelled"))
                )
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
        return t("err_page_range", error=str(exc))
    if pikepdf and isinstance(exc, pikepdf.PasswordError):
        return t("err_pdf_encrypted")
    if pikepdf and isinstance(exc, pikepdf.PdfError):
        return t("err_pdf_corrupt_format")
    if fitz and isinstance(exc, fitz.FileDataError):
        return t("err_pdf_corrupt_read")
    if isinstance(exc, PermissionError):
        return t("err_permission")
    if isinstance(exc, FileNotFoundError):
        return t("err_file_not_found")
    if isinstance(exc, IsADirectoryError):
        return t("err_is_directory")
    return str(exc)


