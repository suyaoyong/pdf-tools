from __future__ import annotations

import io
import os
import shutil
from pathlib import Path

import fitz
import pikepdf
import pytesseract
from docx import Document
from PIL import Image

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.config import BASE_DIR
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class OcrOperation(PdfOperation):
    tool_id = "ocr"
    display_name = "OCR 识别"

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        if not spec.params.get("output_pdf") and not spec.params.get("output_docx"):
            return JobResult(success=False, error="请至少选择一种输出格式。")
        bundled = BASE_DIR / "tesseract" / "tesseract.exe"
        tesseract_cmd = (
            os.environ.get("TESSERACT_CMD")
            or (str(bundled) if bundled.exists() else None)
            or shutil.which("tesseract")
            or shutil.which("tesseract.exe")
        )
        if not tesseract_cmd:
            return JobResult(
                success=False,
                error="未检测到 Tesseract OCR。请在应用目录放置 tesseract\\tesseract.exe，或设置环境变量 TESSERACT_CMD，或配置到 PATH。",
            )
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        dpi = int(spec.params.get("dpi", 300))
        lang = str(spec.params.get("lang", "chi_sim+eng"))
        outputs: list[Path] = []

        total_inputs = len(spec.inputs)
        for idx, src in enumerate(spec.inputs, start=1):
            if token.is_cancelled():
                return JobResult(success=False, cancelled=True, error="任务已取消")

            doc = fitz.open(src)
            total_pages = doc.page_count

            pdf_out = None
            pdf_path = None
            if spec.params.get("output_pdf"):
                name_index = idx if spec.output_name and total_inputs > 1 else None
                pdf_path = self._output_path(
                    src,
                    spec.output_dir,
                    "_ocr",
                    spec.output_name,
                    ext=".pdf",
                    index=name_index,
                    overwrite=spec.overwrite,
                )
                pdf_out = pikepdf.Pdf.new()

            docx = Document() if spec.params.get("output_docx") else None
            docx_path = None
            if docx:
                name_index = idx if spec.output_name and total_inputs > 1 else None
                docx_path = self._output_path(
                    src,
                    spec.output_dir,
                    "_ocr",
                    spec.output_name,
                    ext=".docx",
                    index=name_index,
                    overwrite=spec.overwrite,
                )

            for i in range(total_pages):
                if token.is_cancelled():
                    doc.close()
                    return JobResult(success=False, cancelled=True, error="任务已取消")

                page = doc.load_page(i)
                zoom = dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                if pdf_out is not None:
                    pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf", lang=lang)
                    with pikepdf.open(io.BytesIO(pdf_bytes)) as page_pdf:
                        pdf_out.pages.extend(page_pdf.pages)

                if docx is not None:
                    text = pytesseract.image_to_string(img, lang=lang)
                    if text.strip():
                        docx.add_paragraph(text)
                    if i < total_pages - 1:
                        docx.add_page_break()

                progress_cb("processing", i + 1, total_pages, f"OCR: {src.name} 第 {i + 1} 页")

            doc.close()

            if pdf_out is not None and pdf_path is not None:
                pdf_out.save(pdf_path)
                outputs.append(pdf_path)
            if docx is not None and docx_path is not None:
                docx.save(docx_path)
                outputs.append(docx_path)

        return JobResult(success=True, outputs=outputs)
