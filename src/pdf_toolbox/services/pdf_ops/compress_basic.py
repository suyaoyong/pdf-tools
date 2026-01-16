from __future__ import annotations

import pikepdf

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class CompressBasicOperation(PdfOperation):
    tool_id = "compress_basic"
    display_name = "基础压缩"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        linearize = bool(spec.params.get("linearize", False))
        recompress = bool(spec.params.get("recompress_streams", True))
        outputs = []
        total_inputs = len(spec.inputs)

        for idx, src in enumerate(spec.inputs, start=1):
            name_index = idx if spec.output_name and total_inputs > 1 else None
            out_path = self._output_path(
                src,
                spec.output_dir,
                "_compressed",
                spec.output_name,
                ext=".pdf",
                index=name_index,
                overwrite=spec.overwrite,
            )

            with pikepdf.open(src) as pdf:
                progress_cb("processing", 1, 1, f"重写: {src.name}")
                if token.is_cancelled():
                    return JobResult(success=False, cancelled=True, error="任务已取消")
                save_kwargs = {"linearize": linearize}
                if recompress:
                    try:
                        pdf.save(out_path, **save_kwargs, compress_streams=True, recompress_flate=True)
                    except TypeError:
                        pdf.save(out_path, **save_kwargs)
                else:
                    pdf.save(out_path, **save_kwargs)

            outputs.append(out_path)

        return JobResult(success=True, outputs=outputs)


