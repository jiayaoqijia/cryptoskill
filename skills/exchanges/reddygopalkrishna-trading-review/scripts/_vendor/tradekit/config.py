"""User configuration and paths.

Everything lives under TRADING_SKILLS_HOME (default ~/.trading-skills):
    config.json    risk limits, data provider, broker, account settings
    secrets.json   broker credentials (chmod 600) - env vars take precedence
    cache/         downloaded market data
    journal.db     SQLite trade journal
    paper/         paper broker state
    approvals/     pre-trade gate approvals consumed by trading-broker
    audit.log      JSONL log of every order action
    KILL_SWITCH    if this file exists, no order can be submitted
"""

from __future__ import annotations

import copy
import json
import os
import stat
from pathlib import Path
from typing import Any, Dict

DEFAULTS: Dict[str, Any] = {
    "version": 1,
    "account": {
        "equity": 100000.0,          # used when the broker cannot report equity
        "currency": "USD",
        "timezone": "UTC",
        "benchmark": None,           # e.g. "^GSPC", "SPY", "^NSEI", "BTC-USD"
    },
    "data": {
        "provider": "yahoo",         # yahoo | csv | kite
        "csv_dir": None,             # folder of SYMBOL.csv files for the csv provider
        "cache_ttl_minutes": 60,
        "sec_user_agent": None,      # "Your Name you@example.com" - SEC asks automated clients to identify themselves
    },
    "broker": {
        "name": "paper",             # paper | kite
        "live_trading_enabled": False,
        "default_product": None,     # broker-specific (kite: CNC | MIS | NRML)
        "default_exchange": None,    # broker-specific (kite: e.g. NSE)
        "default_order_type": "LIMIT",
    },
    "risk": {
        "risk_per_trade_pct": 1.0,
        "max_position_pct": 20.0,
        "max_open_risk_pct": 6.0,
        "max_open_positions": 8,
        "max_daily_loss_pct": 3.0,
        "max_drawdown_pct": 15.0,
        "min_reward_risk": 1.5,
        "max_consecutive_losses": 3,
        "approval_ttl_minutes": 30,
        "confirm_ttl_minutes": 10,
        "no_entries_last_minutes": 30,   # trading-entry: no new intraday entries this close to the close
    },
    "costs": {
        "commission_pct": 0.03,      # percent of notional per side
        "commission_fixed": 0.0,     # fixed per order
        "slippage_pct": 0.05,        # percent per fill
    },
}


def home() -> Path:
    env = os.environ.get("TRADING_SKILLS_HOME") or os.environ.get("TRADINGKIT_SKILLS_HOME")  # legacy name
    if env:
        p = Path(env).expanduser()
    else:
        p = Path.home() / ".trading-skills"
        legacy = Path.home() / ".tradingkit-skills"   # v0.1 folder: keep using it so no data is lost
        if not p.exists() and legacy.is_dir():
            p = legacy
    p.mkdir(parents=True, exist_ok=True)
    return p


def path(*parts: str) -> Path:
    p = home().joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load() -> Dict[str, Any]:
    f = home() / "config.json"
    user: Dict[str, Any] = {}
    if f.exists():
        try:
            user = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            raise RuntimeError(f"{f} is not valid JSON: {e}") from e
    return _deep_merge(DEFAULTS, user)


def save(cfg: Dict[str, Any]) -> Path:
    f = home() / "config.json"
    f.write_text(json.dumps(cfg, indent=2, sort_keys=False) + "\n")
    return f


def exists() -> bool:
    return (home() / "config.json").exists()


def coerce(value: str) -> Any:
    """Turn a CLI string into bool/int/float/null/json when it looks like one."""
    low = value.strip().lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "none", ""):
        return None
    try:
        if any(c in value for c in ".eE"):
            return float(value)
        return int(value)
    except ValueError:
        pass
    if value.strip().startswith(("{", "[")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    return value


def set_key(cfg: Dict[str, Any], dotted: str, value: Any) -> Dict[str, Any]:
    keys = dotted.split(".")
    node = cfg
    for k in keys[:-1]:
        if k not in node or not isinstance(node[k], dict):
            node[k] = {}
        node = node[k]
    node[keys[-1]] = value
    return cfg


def get_key(cfg: Dict[str, Any], dotted: str, default: Any = None) -> Any:
    node: Any = cfg
    for k in dotted.split("."):
        if not isinstance(node, dict) or k not in node:
            return default
        node = node[k]
    return node


# ---------------------------------------------------------------- secrets

def load_secrets() -> Dict[str, Any]:
    f = home() / "secrets.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text())
    except json.JSONDecodeError:
        return {}


def save_secrets(data: Dict[str, Any]) -> Path:
    f = home() / "secrets.json"
    f.write_text(json.dumps(data, indent=2) + "\n")
    try:
        os.chmod(f, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return f


def secret(name: str, env: str) -> Any:
    """Environment variable wins over secrets.json."""
    v = os.environ.get(env)
    if v:
        return v
    return load_secrets().get(name)


def mask(value: Any) -> str:
    if not value:
        return "(not set)"
    s = str(value)
    return s[:3] + "***" + s[-2:] if len(s) > 8 else "***"


# ---------------------------------------------------------------- kill switch

def kill_switch_on() -> bool:
    return (home() / "KILL_SWITCH").exists()


def set_kill_switch(on: bool, reason: str = "") -> None:
    f = home() / "KILL_SWITCH"
    if on:
        f.write_text(reason or "manual")
    elif f.exists():
        f.unlink()
