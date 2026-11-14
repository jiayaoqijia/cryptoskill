"""Shared plumbing for the JSON REST broker adapters (Fyers, Upstox, Dhan, Groww).

Secrets are only ever put in request headers. They are never written into error
messages: errors carry the HTTP status and the broker's own response body.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, Optional

from .. import config, http
from .base import BrokerError


def call(label: str, method: str, url: str, headers: Dict[str, str], params: Optional[Dict] = None,
         body: Optional[Any] = None, form: Optional[Dict] = None) -> Any:
    """One HTTP call. Returns parsed JSON. Raises BrokerError with the broker's message on failure."""
    try:
        raw = http.request(method, url, params=params, data=form, json_body=body, headers=headers)
    except http.HTTPError as e:
        raise BrokerError(f"{label} {method} {_path(url)} failed [{e.status}] {_brief(e.body)}") from None
    except RuntimeError as e:
        raise BrokerError(f"{label} {method} {_path(url)}: {e}") from None
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise BrokerError(f"{label} {method} {_path(url)}: response was not JSON") from None


def _path(url: str) -> str:
    return "/" + url.split("://", 1)[-1].split("/", 1)[-1] if "/" in url.split("://", 1)[-1] else url


def _brief(text: str, n: int = 300) -> str:
    return (text or "").replace("\n", " ")[:n]


def need(label: str, **creds) -> None:
    """Raise a clear error naming (not showing) missing credentials."""
    missing = [k for k, v in creds.items() if not v]
    if missing:
        raise BrokerError(f"{label}: missing {', '.join(missing)}. Run the {label.lower()}-login step in "
                          "trading-setup (or set the matching environment variables).")


def product_for(order: Dict, table: Dict[str, str], broker_label: str, default: str = "CNC") -> str:
    cfg = config.load()["broker"]
    raw = str(order.get("product") or cfg.get("default_product") or default).upper()
    if raw in table:
        return table[raw]
    if raw in table.values():
        return raw
    raise BrokerError(f"{broker_label}: product {raw!r} not supported (use {', '.join(sorted(set(table) | set(table.values())))})")


def whole_qty(order: Dict, label: str) -> int:
    if not float(order["qty"]).is_integer():
        raise BrokerError(f"{label} quantities must be whole numbers")
    return int(order["qty"])


def f(x, default: float = 0.0) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def first(d: Dict, keys: Iterable[str], default=None):
    for k in keys:
        if d.get(k) not in (None, ""):
            return d[k]
    return default
