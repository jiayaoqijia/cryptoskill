from __future__ import annotations

from dataclasses import dataclass
import json
import os
import re

# Supported shorthand form for env-based interoperability:
# openclaw:<source>:<provider>:<id>
_OPENCLAW_REF = re.compile(
    r"^openclaw:(?P<source>env|file|exec):(?P<provider>[a-zA-Z0-9_-]+):(?P<id>[A-Za-z0-9._:/-]+)$"
)


@dataclass(frozen=True)
class SecretRef:
    source: str
    provider: str
    id: str


def parse_secret_ref(value: str) -> SecretRef | None:
    raw = value.strip()
    if not raw:
        return None

    # Official SecretRef object shape:
    # {"source":"env|file|exec","provider":"default","id":"..."}
    if raw.startswith("{"):
        try:
            data = json.loads(raw)
            if all(k in data for k in ("source", "provider", "id")):
                return SecretRef(
                    source=str(data["source"]),
                    provider=str(data["provider"]),
                    id=str(data["id"]),
                )
        except json.JSONDecodeError:
            pass

    m = _OPENCLAW_REF.match(raw)
    if not m:
        return None
    return SecretRef(
        source=m.group("source"),
        provider=m.group("provider"),
        id=m.group("id"),
    )


def load_secret_value(
    env_key: str,
    default: str | None = None,
) -> tuple[str | None, SecretRef | None]:
    # 1) if the primary env contains a SecretRef, it wins
    raw = os.getenv(env_key, "").strip()
    if raw:
        ref = parse_secret_ref(raw)
        if ref:
            return None, ref

    # 2) companion *_REF wins over plaintext, matching OpenClaw precedence
    ref_raw = os.getenv(f"{env_key}_REF", "").strip()
    if ref_raw:
        ref = parse_secret_ref(ref_raw)
        if ref:
            return None, ref

    # 3) fallback to plaintext env value
    if raw:
        return raw, None

    return default, None
