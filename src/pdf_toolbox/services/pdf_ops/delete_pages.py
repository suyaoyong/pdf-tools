from __future__ import annotations

import pikepdf

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.core.range_parser import parse_page_range
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class DeletePagesOperation(PdfOperation):
    tool_id = "delete_pages"
    display_name = "删除页"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        ranges = spec.params.get("ranges", "")
        outputs = []
        total_inputs = len(spec.inputs)

        for idx, src in enumerate(spec.inputs, start=1):
            with pikepdf.open(src) as pdf:
                total_pages = len(pdf.pages)
                delete_indices = set(parse_page_range(ranges, total_pages))

                out_pdf = pikepdf.Pdf.new()
                for i, page in enumerate(pdf.pages):
                    if token.is_cancelled():
                        return JobResult(success=False, cancelled=True, error="任务已取消")
                    if i not in delete_indices:
                        out_pdf.pages.append(page)
                    progress_cb("processing", i + 1, total_pages, f"处理页 {i + 1}")

                name_index = idx if spec.output_name and total_inputs > 1 else None
                out_path = self._output_path(
                    src,
                    spec.output_dir,
                    "_deleted",
                    spec.output_name,
                    ext=".pdf",
                    index=name_index,
                    overwrite=spec.overwrite,
                )
                out_pdf.save(out_path)
                outputs.append(out_path)

        return JobResult(success=True, outputs=outputs)


