from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class JobSpec:
    tool_id: str
    inputs: List[Path]
    output_dir: Path
    output_name: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    overwrite: bool = False


@dataclass
class JobProgress:
    job_id: str
    stage: str
    current: int
    total: int
    message: str = ""


@dataclass
class JobResult:
    success: bool
    outputs: List[Path] = field(default_factory=list)
    warning: Optional[str] = None
    error: Optional[str] = None
    cancelled: bool = False


