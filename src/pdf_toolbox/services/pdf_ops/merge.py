from __future__ import annotations

import pikepdf

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class MergeOperation(PdfOperation):
    tool_id = "merge"
    display_name = "合并 PDF"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        total_pages = 0
        for path in spec.inputs:
            with pikepdf.open(path) as pdf:
                total_pages += len(pdf.pages)

        out_path = self._output_path(
            spec.inputs[0], spec.output_dir, "_merged", spec.output_name, ext=".pdf", overwrite=spec.overwrite
        )

        out_pdf = pikepdf.Pdf.new()
        current = 0
        for path in spec.inputs:
            with pikepdf.open(path) as pdf:
                for page in pdf.pages:
                    if token.is_cancelled():
                        return JobResult(success=False, cancelled=True, error="任务已取消")
                    out_pdf.pages.append(page)
                    current += 1
                    progress_cb("processing", current, total_pages, f"合并: {path.name}")

        out_pdf.save(out_path)
        progress_cb("writing", total_pages, total_pages, "写入完成")
        return JobResult(success=True, outputs=[out_path])
