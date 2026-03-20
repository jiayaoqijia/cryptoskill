from __future__ import annotations

import re
from typing import Any

_PAIR_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|private[_-]?key)\b\s*[:=]\s*([^\s,;]+)"),
    re.compile(r"(?i)\b(bearer)\s+([A-Za-z0-9._-]+)"),
]
_LONG_TOKEN = re.compile(r"\b[A-Za-z0-9_-]{24,}\b")
_AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")


def _mask(value: str) -> str:
    if len(value) <= 6:
        return "***"
    return f"{value[:3]}***{value[-2:]}"


def redact_sensitive(text: str) -> str:
    out = text
    for pattern in _PAIR_PATTERNS:
        out = pattern.sub(lambda m: f"{m.group(1)}={_mask(m.group(2))}", out)
    out = _AWS_KEY.sub("***AWS_KEY***", out)
    out = _LONG_TOKEN.sub(lambda m: _mask(m.group(0)), out)
    return out


def redact_structure(obj: Any) -> Any:
    if isinstance(obj, dict):
        redacted: dict[str, Any] = {}
        for key, value in obj.items():
            lk = key.lower()
            if any(tok in lk for tok in ["key", "secret", "token", "password", "private"]):
                redacted[key] = "***"
            else:
                redacted[key] = redact_structure(value)
        return redacted
    if isinstance(obj, list):
        return [redact_structure(v) for v in obj]
    if isinstance(obj, str):
        return redact_sensitive(obj)
    return obj

