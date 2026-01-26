from pdf_toolbox.services.pdf_ops.base import PdfOperation
from pdf_toolbox.services.pdf_ops.compress_basic import CompressBasicOperation
from pdf_toolbox.services.pdf_ops.compress_images import CompressImagesOperation
from pdf_toolbox.services.pdf_ops.delete_pages import DeletePagesOperation
from pdf_toolbox.services.pdf_ops.images_to_pdf import ImagesToPdfOperation
from pdf_toolbox.services.pdf_ops.merge import MergeOperation
from pdf_toolbox.services.pdf_ops.ocr import OcrOperation
from pdf_toolbox.services.pdf_ops.pdf_to_images import PdfToImagesOperation
from pdf_toolbox.services.pdf_ops.ppt_to_pdf import PptToPdfOperation
from pdf_toolbox.services.pdf_ops.reorder_pages import ReorderPagesOperation
from pdf_toolbox.services.pdf_ops.rotate_pages import RotatePagesOperation
from pdf_toolbox.services.pdf_ops.split_extract import SplitExtractOperation
from pdf_toolbox.i18n import t

_OPS = [
    MergeOperation(),
    SplitExtractOperation(),
    DeletePagesOperation(),
    RotatePagesOperation(),
    ReorderPagesOperation(),
    CompressBasicOperation(),
    CompressImagesOperation(),
    PdfToImagesOperation(),
    ImagesToPdfOperation(),
    PptToPdfOperation(),
    OcrOperation(),
]

OP_REGISTRY = {op.tool_id: op for op in _OPS}


def get_operation(tool_id: str) -> PdfOperation:
    if tool_id not in OP_REGISTRY:
        raise ValueError(t("err_tool_not_found", tool_id=tool_id))
    return OP_REGISTRY[tool_id]
