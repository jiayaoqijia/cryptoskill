#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Any, Dict

from snaptrade_client import SnapTrade
from snaptrade_client.configuration import Configuration

DEFAULT_CONFIG_PATH = os.environ.get(
    "SNAPTRADE_CONFIG",
    str(Path.home() / ".openclaw" / "workspace" / "secrets" / "snaptrade.json"),
)


def load_config(path: str = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    data = json.loads(p.read_text())
    return data


def save_config(data: Dict[str, Any], path: str = DEFAULT_CONFIG_PATH) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2))
    try:
        os.chmod(p, 0o600)
    except Exception:
        pass


def get_client(cfg: Dict[str, Any]) -> SnapTrade:
    client_id = cfg.get("client_id")
    consumer_key = cfg.get("consumer_key")
    if not client_id or not consumer_key:
        raise ValueError("Missing client_id or consumer_key in config")
    config = Configuration(client_id=client_id, consumer_key=consumer_key)
    return SnapTrade(config)
