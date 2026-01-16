from __future__ import annotations

import pikepdf

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.core.range_parser import parse_page_range
from pdf_toolbox.services.io.validators import ValidationError
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class ReorderPagesOperation(PdfOperation):
    tool_id = "reorder_pages"
    display_name = "重排页"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        order_expr = spec.params.get("order", "")
        outputs = []
        total_inputs = len(spec.inputs)

        for idx, src in enumerate(spec.inputs, start=1):
            with pikepdf.open(src) as pdf:
                total_pages = len(pdf.pages)
                order = parse_page_range(order_expr, total_pages)
                if len(order) != total_pages:
                    raise ValidationError("重排必须覆盖所有页且不重复")

                out_pdf = pikepdf.Pdf.new()
                for i, page_index in enumerate(order, start=1):
                    if token.is_cancelled():
                        return JobResult(success=False, cancelled=True, error="任务已取消")
                    out_pdf.pages.append(pdf.pages[page_index])
                    progress_cb("processing", i, total_pages, f"重排页 {page_index + 1}")

                name_index = idx if spec.output_name and total_inputs > 1 else None
                out_path = self._output_path(
                    src,
                    spec.output_dir,
                    "_reordered",
                    spec.output_name,
                    ext=".pdf",
                    index=name_index,
                    overwrite=spec.overwrite,
                )
                out_pdf.save(out_path)
                outputs.append(out_path)

        return JobResult(success=True, outputs=outputs)


