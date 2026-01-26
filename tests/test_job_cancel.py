import time
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEventLoop, QTimer

from pdf_toolbox.core.job_queue import JobQueue
from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.i18n import t
from pdf_toolbox.services.pdf_ops import OP_REGISTRY
from pdf_toolbox.services.pdf_ops.base import PdfOperation


class DummyOp(PdfOperation):
    tool_id = "_test_dummy"
    display_name = "Dummy"

    def validate(self, spec):
        return None

    def run(self, spec, progress_cb, token):
        total = 50
        for i in range(total):
            if token.is_cancelled():
                return JobResult(success=False, cancelled=True, error=t("err_cancelled"))
            time.sleep(0.01)
            progress_cb("processing", i + 1, total, "")
        return JobResult(success=True, outputs=[])


def test_job_cancel():
    app = QCoreApplication.instance() or QCoreApplication([])
    OP_REGISTRY[DummyOp.tool_id] = DummyOp()

    queue = JobQueue()
    finished = {}

    def on_finished(job_id, result):
        finished["result"] = result
        loop.quit()

    queue.finished.connect(on_finished)

    spec = JobSpec(tool_id=DummyOp.tool_id, inputs=[Path("dummy")], output_dir=Path("."))
    job_id = queue.submit(spec)

    loop = QEventLoop()
    QTimer.singleShot(50, lambda: queue.cancel(job_id))
    QTimer.singleShot(2000, loop.quit)
    loop.exec()

    result = finished.get("result")
    assert result is not None
    assert result.cancelled is True


