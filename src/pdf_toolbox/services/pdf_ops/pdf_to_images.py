from __future__ import annotations

import fitz
from PIL import Image

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class PdfToImagesOperation(PdfOperation):
    tool_id = "pdf_to_images"
    display_name = "PDF 转图片"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        dpi = int(spec.params.get("dpi", 150))
        fmt = str(spec.params.get("format", "png")).lower()
        outputs = []
        pil_format = "JPEG" if fmt in {"jpg", "jpeg"} else "PNG"

        total_inputs = len(spec.inputs)
        for idx, src in enumerate(spec.inputs, start=1):
            doc = fitz.open(src)
            total_pages = doc.page_count

            for i in range(total_pages):
                if token.is_cancelled():
                    doc.close()
                    return JobResult(success=False, cancelled=True, error="任务已取消")
                page = doc.load_page(i)
                zoom = dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ext = f".{fmt}"
                name_index = idx if spec.output_name and total_inputs > 1 else None
                out_path = self._output_path(
                    src,
                    spec.output_dir,
                    f"_p{i+1}",
                    spec.output_name,
                    ext=ext,
                    index=name_index,
                    overwrite=spec.overwrite,
                )
                img.save(out_path, format=pil_format)
                outputs.append(out_path)
                progress_cb("processing", i + 1, total_pages, f"导出页 {i + 1}")

            doc.close()

        return JobResult(success=True, outputs=outputs)

