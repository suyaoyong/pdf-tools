from __future__ import annotations

from pathlib import Path

from PIL import Image

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class ImagesToPdfOperation(PdfOperation):
    tool_id = "images_to_pdf"
    display_name = "图片转 PDF"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        images = [Image.open(p).convert("RGB") for p in spec.inputs]
        if not images:
            return JobResult(success=False, error="未选择图片")

        out_path = self._output_path(
            spec.inputs[0], spec.output_dir, "_images", spec.output_name, ext=".pdf", overwrite=spec.overwrite
        )

        total = len(images)
        for i in range(total):
            if token.is_cancelled():
                for img in images:
                    img.close()
                return JobResult(success=False, cancelled=True, error="任务已取消")
            progress_cb("processing", i + 1, total, f"处理图片 {i + 1}")

        first, rest = images[0], images[1:]
        first.save(out_path, save_all=True, append_images=rest)

        for img in images:
            img.close()

        return JobResult(success=True, outputs=[out_path])

