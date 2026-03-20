from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional

from defillama_sdk import DefiLlama


@dataclass
class Context:
    client: DefiLlama
    pro_client: DefiLlama
    compact: bool = False


def build_clients(api_key: Optional[str]) -> tuple[DefiLlama, DefiLlama]:
    client = DefiLlama()
    if api_key:
        pro_client = DefiLlama({"api_key": api_key})
    else:
        pro_client = DefiLlama()
    return client, pro_client


def dump_json(data: Any, compact: bool = False) -> None:
    if compact:
        output = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        output = json.dumps(data, ensure_ascii=False, indent=2)
    print(output)


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_json_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"无效 JSON: {exc}") from exc
