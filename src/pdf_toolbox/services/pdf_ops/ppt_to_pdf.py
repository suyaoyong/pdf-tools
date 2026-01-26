from __future__ import annotations

from pathlib import Path

from pdf_toolbox.core.models import JobResult, JobSpec
from pdf_toolbox.i18n import t
from pdf_toolbox.services.io.validators import ValidationError
from pdf_toolbox.services.pdf_ops.base import PdfOperation, ProgressCb


class PptToPdfOperation(PdfOperation):
    tool_id = "ppt_to_pdf"
    display_name = "PPT to PDF"

    _allowed_exts = {".ppt", ".pptx", ".pps", ".ppsx"}

    def validate(self, spec: JobSpec) -> None:
        super().validate(spec)
        for path in spec.inputs:
            if path.suffix.lower() not in self._allowed_exts:
                raise ValidationError(t("err_invalid_file_type", name=path.name))

    def run(self, spec: JobSpec, progress_cb: ProgressCb, token) -> JobResult:
        try:
            import pythoncom
            import win32com.client  # type: ignore
        except Exception as exc:  # noqa: BLE001
            return JobResult(success=False, error=t("err_missing_office_components", error=exc))

        pythoncom.CoInitialize()
        app = None
        outputs: list[Path] = []

        try:
            app = _create_ppt_app(win32com.client)
            _configure_app(app)
            total = len(spec.inputs)

            for idx, src in enumerate(spec.inputs, start=1):
                self._check_cancel(token)
                progress_cb("processing", idx - 1, total, t("progress_convert_file", name=src.name))

                out_path = self._output_path(
                    src,
                    spec.output_dir,
                    "_ppt",
                    spec.output_name,
                    ext=".pdf",
                    overwrite=spec.overwrite,
                )

                presentation = None
                try:
                    presentation = app.Presentations.Open(str(src), ReadOnly=True, WithWindow=False)
                    presentation.SaveAs(str(out_path), 32)  # 32 = ppSaveAsPDF
                finally:
                    if presentation is not None:
                        presentation.Close()

                outputs.append(out_path)
                progress_cb("processing", idx, total, t("progress_complete_file", name=src.name))

            return JobResult(success=True, outputs=outputs)
        finally:
            if app is not None:
                try:
                    app.Quit()
                except Exception:  # noqa: BLE001
                    pass
            pythoncom.CoUninitialize()


def _create_ppt_app(win32_client):
    last_exc: Exception | None = None
    for prog_id in ("PowerPoint.Application", "KWPP.Application"):
        try:
            return win32_client.DispatchEx(prog_id)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
    raise RuntimeError(t("err_no_ppt_engine", error=last_exc))


def _configure_app(app) -> None:
    try:
        if hasattr(app, "Visible"):
            app.Visible = 0
    except Exception:  # noqa: BLE001
        pass
    try:
        if hasattr(app, "DisplayAlerts"):
            app.DisplayAlerts = 0
    except Exception:  # noqa: BLE001
        pass
