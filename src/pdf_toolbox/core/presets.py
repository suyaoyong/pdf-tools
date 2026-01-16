from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from pdf_toolbox.config import ASSETS_DIR


@dataclass
class Preset:
    preset_id: str
    name: str
    tool_id: str
    params: Dict[str, Any]


class PresetStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (ASSETS_DIR / "presets.json")

    def load(self) -> List[Preset]:
        data = json.loads(self.path.read_text(encoding="utf-8-sig"))
        presets = []
        for item in data.get("presets", []):
            presets.append(
                Preset(
                    preset_id=item.get("id", ""),
                    name=item.get("name", ""),
                    tool_id=item.get("tool_id", ""),
                    params=item.get("params", {}),
                )
            )
        return presets


