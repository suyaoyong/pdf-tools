from __future__ import annotations

import re
from typing import Iterable, List, Optional

from pdf_toolbox.i18n import t

_RANGE_RE = re.compile(r"^(\d+)(?:-(\d+))?$")


class RangeParseError(ValueError):
    pass


def _iter_tokens(expr: str) -> Iterable[str]:
    for token in expr.split(","):
        token = token.strip()
        if token:
            yield token


def parse_page_range(expr: str, max_pages: Optional[int] = None) -> List[int]:
    if not expr or not expr.strip():
        raise RangeParseError(t("range_empty"))

    seen = set()
    result: List[int] = []

    for token in _iter_tokens(expr):
        match = _RANGE_RE.match(token)
        if not match:
            raise RangeParseError(t("range_invalid", token=token))
        start = int(match.group(1))
        end = int(match.group(2) or start)
        if start < 1 or end < 1:
            raise RangeParseError(t("range_page_min"))
        if start > end:
            raise RangeParseError(t("range_start_gt_end", token=token))
        for page in range(start, end + 1):
            if max_pages is not None and page > max_pages:
                raise RangeParseError(t("range_page_out_of_range", page=page, max_pages=max_pages))
            if page not in seen:
                seen.add(page)
                result.append(page - 1)  # 0-based

    if not result:
        raise RangeParseError(t("range_empty"))

    return result


