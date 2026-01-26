from __future__ import annotations

import fitz
from PIL import Image

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.i18n import t
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class CompressImagesOperation(PdfOperation):
    tool_id = "compress_images"
    display_name = "Image Re-encode Compression"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        dpi = int(spec.params.get("dpi", 150))
        jpeg_quality = int(spec.params.get("jpeg_quality", 75))
        grayscale = bool(spec.params.get("grayscale", False))
        max_side = int(spec.params.get("max_side", 1600))
        outputs = []
        total_inputs = len(spec.inputs)

        for idx, src in enumerate(spec.inputs, start=1):
            name_index = idx if spec.output_name and total_inputs > 1 else None
            out_path = self._output_path(
                src,
                spec.output_dir,
                "_imgcompressed",
                spec.output_name,
                ext=".pdf",
                index=name_index,
                overwrite=spec.overwrite,
            )

            doc = fitz.open(src)
            total_pages = doc.page_count
            out_doc = fitz.open()

            for i in range(total_pages):
                if token.is_cancelled():
                    doc.close()
                    out_doc.close()
                    return JobResult(success=False, cancelled=True, error=t("err_cancelled"))
                page = doc.load_page(i)
                zoom = dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                if max_side > 0:
                    scale = max(img.width, img.height) / max_side
                    if scale > 1:
                        img = img.resize((int(img.width / scale), int(img.height / scale)), Image.LANCZOS)
                if grayscale:
                    img = img.convert("L").convert("RGB")

                img_bytes = _image_to_bytes(img, jpeg_quality)
                rect = fitz.Rect(0, 0, img.width * 72 / dpi, img.height * 72 / dpi)
                out_page = out_doc.new_page(width=rect.width, height=rect.height)
                out_page.insert_image(rect, stream=img_bytes)
                progress_cb("processing", i + 1, total_pages, t("progress_reencode_page", page=i + 1))

            out_doc.save(out_path)
            out_doc.close()
            doc.close()
            outputs.append(out_path)

        return JobResult(success=True, outputs=outputs)


def _image_to_bytes(img: Image.Image, quality: int) -> bytes:
    from io import BytesIO

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()


