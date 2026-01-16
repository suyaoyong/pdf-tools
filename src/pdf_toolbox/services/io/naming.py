from __future__ import annotations

from pathlib import Path
from typing import Optional


def _safe_name(name: str) -> str:
    return "".join(c for c in name if c not in "\\/:*?\"<>|").strip()


def build_output_path(
    input_path: Path,
    output_dir: Path,
    suffix: str,
    output_name: Optional[str] = None,
    ext: Optional[str] = None,
    index: Optional[int] = None,
) -> Path:
    stem = output_name or input_path.stem
    if index is not None:
        stem = f"{stem}_{index}"
    name = _safe_name(stem + suffix)
    return output_dir / f"{name}{ext or input_path.suffix}"


def resolve_output_path(
    input_path: Path,
    output_dir: Path,
    suffix: str,
    output_name: Optional[str] = None,
    ext: Optional[str] = None,
    index: Optional[int] = None,
    overwrite: bool = False,
) -> Path:
    path = build_output_path(input_path, output_dir, suffix, output_name, ext, index)
    if overwrite:
        return path
    if not path.exists():
        return path
    stem = path.stem
    for i in range(1, 1000):
        candidate = path.with_name(f"{stem}_{i}{path.suffix}")
        if not candidate.exists():
            return candidate
    return path
