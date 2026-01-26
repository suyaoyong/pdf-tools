from __future__ import annotations

import io

import fitz
from PIL import Image

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.i18n import t
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class ImagesToPdfOperation(PdfOperation):
    tool_id = "images_to_pdf"
    display_name = "Images to PDF"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        page_size = _page_size_from_params(spec.params)
        if not spec.inputs:
            return JobResult(success=False, error=t("err_no_images_selected"))

        out_path = self._output_path(
            spec.inputs[0], spec.output_dir, "_images", spec.output_name, ext=".pdf", overwrite=spec.overwrite
        )

        doc = fitz.open()
        total = len(spec.inputs)
        try:
            for i, img_path in enumerate(spec.inputs):
                if token.is_cancelled():
                    return JobResult(success=False, cancelled=True, error=t("err_cancelled"))
                progress_cb("processing", i + 1, total, t("progress_process_page", page=i + 1))
                with Image.open(img_path) as img:
                    rgb = img.convert("RGB")
                    img_bytes = _image_bytes(rgb)
                    rect = _image_rect(rgb.size, page_size)
                    page = doc.new_page(width=page_size[0], height=page_size[1])
                    page.insert_image(rect, stream=img_bytes)
                    rgb.close()
            if doc.page_count == 0:
                return JobResult(success=False, error=t("err_no_images_selected"))
            doc.save(out_path)
        finally:
            doc.close()

        return JobResult(success=True, outputs=[out_path])


def _page_size_from_params(params: dict | None) -> tuple[int, int]:
    sizes = {
        "a4": (595, 842),
        "letter": (612, 792),
    }
    if not params:
        return sizes["a4"]
    return sizes.get(str(params.get("page_size", "a4")).lower(), sizes["a4"])


def _image_bytes(img: Image.Image) -> bytes:
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def _image_rect(image_size: tuple[int, int], page_size: tuple[int, int]) -> fitz.Rect:
    img_w, img_h = image_size
    page_w, page_h = page_size
    scale = min(page_w / img_w, page_h / img_h, 1.0)
    rect_w = img_w * scale
    rect_h = img_h * scale
    x0 = (page_w - rect_w) / 2
    y0 = (page_h - rect_h) / 2
    return fitz.Rect(x0, y0, x0 + rect_w, y0 + rect_h)

