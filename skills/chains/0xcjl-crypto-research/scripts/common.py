"""Shared deterministic IO and time helpers; no model calls or trading actions."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

UTC = timezone.utc
VERSION = "0.1.6"


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def instant(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timestamp requires a UTC offset or Z")
    return result.astimezone(UTC)


def number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Non-finite number")
    return result


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


def read_json(path: str | Path) -> Any:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, value: Any, *, exclusive: bool = False) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if exclusive:
        with target.open("x", encoding="utf-8") as handle:
            handle.write(text)
        return
    temporary = target.with_name(target.name + ".tmp-" + os.urandom(4).hex())
    with temporary.open("x", encoding="utf-8") as handle:
        handle.write(text)
    temporary.replace(target)


def safe_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}", value):
        raise ValueError("ID must start alphanumeric; only letters, digits, dot, dash, underscore")
    return value


def asset_key(asset: dict) -> str:
    chain = str(asset["chain"]).lower()
    address = str(asset.get("address") or "")
    native = str(asset.get("native_id") or "")
    if bool(address) == bool(native):
        raise ValueError("Asset requires exactly one of address or native_id")
    if chain == "sui" and address:
        match = re.fullmatch(r"0x([0-9a-fA-F]{1,64})::([A-Za-z_][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)", address)
        if not match:
            raise ValueError("Sui fungible asset requires Move coin type, not pool/object ID; generic types need explicit native_id and source")
        package, module, coin = match.groups()
        if int(package, 16) == 2 and module == "sui" and coin == "SUI":
            return "sui:native:sui"
        return f"sui:0x{package.lower().zfill(64)}::{module}::{coin}"
    # Solana base58 is case-sensitive. EVM equality is not; retain source display elsewhere.
    if address.startswith("0x"):
        if not re.fullmatch(r"0x[0-9a-fA-F]{40}", address):
            raise ValueError("Invalid EVM address")
        address = address.lower()
    return f"{chain}:{address or 'native:' + native.lower()}"


def ensure_runtime(path: str | Path) -> Path:
    root = Path(path).expanduser().resolve()
    skill = Path(__file__).resolve().parents[1]
    if root == skill or skill in root.parents:
        raise ValueError("Runtime data must be outside the installed skill")
    root.mkdir(parents=True, exist_ok=True)
    return root
