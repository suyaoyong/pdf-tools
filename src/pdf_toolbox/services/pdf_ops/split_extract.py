from __future__ import annotations

import pikepdf

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.core.range_parser import parse_page_range
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class SplitExtractOperation(PdfOperation):
    tool_id = "split_extract"
    display_name = "拆分/提取"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        mode = spec.params.get("mode", "extract_one")
        ranges = spec.params.get("ranges", "")
        outputs = []

        total_files = len(spec.inputs)
        for file_index, src in enumerate(spec.inputs, start=1):
            with pikepdf.open(src) as pdf:
                total_pages = len(pdf.pages)
                indices = parse_page_range(ranges, total_pages)

                if mode == "split_many":
                    total = len(indices)
                    for i, page_index in enumerate(indices, start=1):
                        if token.is_cancelled():
                            return JobResult(success=False, cancelled=True, error="任务已取消")
                        out_pdf = pikepdf.Pdf.new()
                        out_pdf.pages.append(pdf.pages[page_index])
                        out_path = self._output_path(
                            src,
                            spec.output_dir,
                            f"_p{page_index + 1}",
                            None,
                            ext=".pdf",
                            overwrite=spec.overwrite,
                        )
                        out_pdf.save(out_path)
                        outputs.append(out_path)
                        progress_cb("processing", i, total, f"拆分页 {page_index + 1}")
                else:
                    out_pdf = pikepdf.Pdf.new()
                    for idx, page_index in enumerate(indices, start=1):
                        if token.is_cancelled():
                            return JobResult(success=False, cancelled=True, error="任务已取消")
                        out_pdf.pages.append(pdf.pages[page_index])
                        progress_cb("processing", idx, len(indices), f"提取页 {page_index + 1}")
                    suffix = f"_extract" if total_files == 1 else f"_extract_{file_index}"
                    out_path = self._output_path(
                        src, spec.output_dir, suffix, spec.output_name, ext=".pdf", overwrite=spec.overwrite
                    )
                    out_pdf.save(out_path)
                    outputs.append(out_path)

        return JobResult(success=True, outputs=outputs)
