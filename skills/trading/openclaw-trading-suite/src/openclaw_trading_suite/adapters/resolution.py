from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .catalog import ADAPTER_SPECS
from .contracts import AdapterType


class ResolutionMode(str, Enum):
    DIRECT_ADAPTER = "direct_adapter"
    SKILL_BACKED = "skill_backed"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class ResolvedAdapterTarget:
    provider: str
    adapter_type: AdapterType
    mode: ResolutionMode
    matched_skill: str | None
    reason: str


def _find_spec(provider: str, adapter_type: AdapterType):
    for spec in ADAPTER_SPECS:
        if spec.provider == provider and spec.adapter_type == adapter_type:
            return spec
    return None


def resolve_adapter_target(
    provider: str,
    adapter_type: AdapterType,
    available_skill_names: list[str] | None = None,
    prefer_skill: bool = True,
) -> ResolvedAdapterTarget:
    available = [name.lower() for name in (available_skill_names or [])]
    spec = _find_spec(provider, adapter_type)
    if spec is None:
        return ResolvedAdapterTarget(
            provider=provider,
            adapter_type=adapter_type,
            mode=ResolutionMode.UNAVAILABLE,
            matched_skill=None,
            reason="provider_not_in_catalog",
        )

    if prefer_skill:
        for alias in spec.skill_aliases:
            for skill_name in available:
                if alias in skill_name:
                    return ResolvedAdapterTarget(
                        provider=provider,
                        adapter_type=adapter_type,
                        mode=ResolutionMode.SKILL_BACKED,
                        matched_skill=skill_name,
                        reason="matched_local_skill_alias",
                    )

    return ResolvedAdapterTarget(
        provider=provider,
        adapter_type=adapter_type,
        mode=ResolutionMode.DIRECT_ADAPTER,
        matched_skill=None,
        reason="using_direct_adapter",
    )

