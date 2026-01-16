from __future__ import annotations

import os
from pathlib import Path


class ValidationError(ValueError):
    pass


def ensure_inputs(inputs: list[Path]) -> None:
    if not inputs:
        raise ValidationError("未选择输入文件")
    for path in inputs:
        if not path.exists():
            raise ValidationError(f"文件不存在: {path}")
        if not path.is_file():
            raise ValidationError(f"不是文件: {path}")
        if not os.access(path, os.R_OK):
            raise ValidationError(f"无读取权限: {path}")


def ensure_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        raise ValidationError(f"输出目录不存在: {output_dir}")
    if not output_dir.is_dir():
        raise ValidationError(f"输出路径不是目录: {output_dir}")
    if not os.access(output_dir, os.W_OK):
        raise ValidationError(f"无写入权限: {output_dir}")


