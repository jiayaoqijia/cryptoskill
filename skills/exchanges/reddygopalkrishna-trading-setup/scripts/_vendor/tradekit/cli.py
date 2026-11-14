"""Shared CLI plumbing: consistent JSON/markdown output and error handling.

Every skill script prints either JSON (--json) or concise markdown, and exits
non-zero with a one-line error the agent can act on.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence


def parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    return p


def add_json_flag(p: argparse.ArgumentParser) -> None:
    p.add_argument("--json", action="store_true", help="print machine-readable JSON")


def _clean(o: Any) -> Any:
    if isinstance(o, float):
        if math.isnan(o) or math.isinf(o):
            return None
        return o
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


def dump(obj: Any) -> str:
    return json.dumps(_clean(obj), indent=2, default=str)


def emit(obj: Any, as_json: bool, md: Optional[Callable[[Any], str]] = None) -> None:
    if as_json or md is None:
        print(dump(obj))
    else:
        print(md(obj))


def fail(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def run(main: Callable[[], Any]) -> None:
    """Wrap a script's main(): turn expected exceptions into clean one-line errors."""
    try:
        main()
    except KeyboardInterrupt:
        fail("interrupted", 130)
    except (ValueError, KeyError, RuntimeError, FileNotFoundError) as e:
        fail(str(e).strip("'\""))


def md_table(rows: List[Dict], cols: Sequence[str], headers: Optional[Sequence[str]] = None) -> str:
    if not rows:
        return "_no rows_"
    headers = headers or cols
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        cells = []
        for c in cols:
            v = r.get(c)
            if isinstance(v, float):
                v = f"{v:,.2f}"
            elif v is None:
                v = "-"
            cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def num(v: Optional[float], digits: int = 2) -> str:
    if v is None:
        return "-"
    return f"{v:,.{digits}f}"
