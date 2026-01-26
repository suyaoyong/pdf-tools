from __future__ import annotations

import os
from pathlib import Path

from pdf_toolbox.i18n import t

class ValidationError(ValueError):
    pass


def ensure_inputs(inputs: list[Path]) -> None:
    if not inputs:
        raise ValidationError(t("err_no_input_files"))
    for path in inputs:
        if not path.exists():
            raise ValidationError(t("err_file_missing", path=path))
        if not path.is_file():
            raise ValidationError(t("err_not_file", path=path))
        if not os.access(path, os.R_OK):
            raise ValidationError(t("err_no_read_perm", path=path))


def ensure_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        raise ValidationError(t("err_output_dir_missing", path=output_dir))
    if not output_dir.is_dir():
        raise ValidationError(t("err_output_not_dir", path=output_dir))
    if not os.access(output_dir, os.W_OK):
        raise ValidationError(t("err_no_write_perm", path=output_dir))


