"""Adapter contracts and registry."""

from .catalog import ADAPTER_SPECS, AdapterScope, AdapterSpec
from .contracts import (
    AdapterType,
    BaseAdapter,
    ExecutionAdapter,
    MarketDataAdapter,
    NewsAdapter,
)
from .registry import AdapterRegistry
from .healing import (
    AdapterAttempt,
    AdapterCallError,
    AdapterCallOutcome,
    call_with_healing,
)
from .resolution import ResolutionMode, ResolvedAdapterTarget, resolve_adapter_target
from .router import AdapterRouter
from .skill_discovery import SkillDiscoveryService

__all__ = [
    "ADAPTER_SPECS",
    "AdapterScope",
    "AdapterSpec",
    "AdapterType",
    "BaseAdapter",
    "ExecutionAdapter",
    "MarketDataAdapter",
    "NewsAdapter",
    "AdapterRegistry",
    "AdapterAttempt",
    "AdapterCallError",
    "AdapterCallOutcome",
    "call_with_healing",
    "ResolutionMode",
    "ResolvedAdapterTarget",
    "resolve_adapter_target",
    "AdapterRouter",
    "SkillDiscoveryService",
]
