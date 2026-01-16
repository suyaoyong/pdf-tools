from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

from pdf_toolbox.core.cancel import CancellationToken
from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.services.io.naming import resolve_output_path
from pdf_toolbox.services.io.validators import ensure_inputs, ensure_output_dir, ValidationError

ProgressCb = Callable[[str, int, int, str], None]


class PdfOperation(ABC):
    tool_id: str = ""
    display_name: str = ""

    def validate(self, spec: JobSpec) -> None:
        ensure_inputs(spec.inputs)
        ensure_output_dir(spec.output_dir)

    def _output_path(
        self,
        input_path: Path,
        output_dir: Path,
        suffix: str,
        output_name: str | None,
        ext: str | None = None,
        index: int | None = None,
        overwrite: bool = False,
    ) -> Path:
        return resolve_output_path(
            input_path=input_path,
            output_dir=output_dir,
            suffix=suffix,
            output_name=output_name,
            ext=ext,
            index=index,
            overwrite=overwrite,
        )

    def _check_cancel(self, token: CancellationToken) -> None:
        if token.is_cancelled():
            raise RuntimeError("任务已取消")

    @abstractmethod
    def run(self, spec: JobSpec, progress_cb: ProgressCb, token: CancellationToken) -> JobResult:
        raise NotImplementedError
