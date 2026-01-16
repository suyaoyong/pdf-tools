from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterator
from contextlib import contextmanager

from pdf_toolbox.config import DEFAULT_TEMP_DIR


@contextmanager
def temp_dir(prefix: str = "pdf_toolbox_") -> Iterator[Path]:
    path = Path(tempfile.mkdtemp(prefix=prefix, dir=DEFAULT_TEMP_DIR))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


