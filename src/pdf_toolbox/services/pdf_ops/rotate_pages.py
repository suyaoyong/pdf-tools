from __future__ import annotations

import pikepdf

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.core.range_parser import parse_page_range
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class RotatePagesOperation(PdfOperation):
    tool_id = "rotate_pages"
    display_name = "旋转页"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        ranges = spec.params.get("ranges", "")
        angle = int(spec.params.get("angle", 90))
        outputs = []
        total_inputs = len(spec.inputs)

        for idx, src in enumerate(spec.inputs, start=1):
            with pikepdf.open(src) as pdf:
                total_pages = len(pdf.pages)
                rotate_indices = set(parse_page_range(ranges, total_pages))

                for i, page in enumerate(pdf.pages):
                    if token.is_cancelled():
                        return JobResult(success=False, cancelled=True, error="任务已取消")
                    if i in rotate_indices:
                        page.rotate(angle, True)
                    progress_cb("processing", i + 1, total_pages, f"处理页 {i + 1}")

                name_index = idx if spec.output_name and total_inputs > 1 else None
                out_path = self._output_path(
                    src,
                    spec.output_dir,
                    "_rotated",
                    spec.output_name,
                    ext=".pdf",
                    index=name_index,
                    overwrite=spec.overwrite,
                )
                pdf.save(out_path)
                outputs.append(out_path)

        return JobResult(success=True, outputs=outputs)


