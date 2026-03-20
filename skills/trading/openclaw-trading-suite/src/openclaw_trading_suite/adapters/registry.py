from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .contracts import AdapterType, BaseAdapter


@dataclass
class AdapterRegistry:
    _adapters: dict[AdapterType, dict[str, BaseAdapter]] = field(
        default_factory=lambda: {
            AdapterType.EXECUTION: {},
            AdapterType.MARKET_DATA: {},
            AdapterType.NEWS: {},
        }
    )

    def register(self, adapter: BaseAdapter) -> None:
        self._adapters[adapter.adapter_type][adapter.name] = adapter

    def get(self, adapter_type: AdapterType, name: str) -> BaseAdapter:
        adapters = self._adapters[adapter_type]
        if name not in adapters:
            raise KeyError(f"adapter not found: type={adapter_type} name={name}")
        return adapters[name]

    def list_names(self, adapter_type: AdapterType) -> list[str]:
        return sorted(self._adapters[adapter_type].keys())

    def capability_snapshot(self) -> dict[str, Any]:
        return {
            adapter_type.value: self.list_names(adapter_type)
            for adapter_type in AdapterType
        }

