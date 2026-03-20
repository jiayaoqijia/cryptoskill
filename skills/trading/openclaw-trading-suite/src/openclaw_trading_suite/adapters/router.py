from __future__ import annotations

from dataclasses import dataclass, field

from .contracts import AdapterType
from .resolution import ResolvedAdapterTarget, resolve_adapter_target
from .skill_discovery import SkillDiscoveryService


@dataclass
class AdapterRouter:
    discovery: SkillDiscoveryService
    # True means prefer skill-backed path if available; False means prefer direct adapter.
    provider_preferences: dict[str, bool] = field(default_factory=dict)

    def set_preference(self, provider: str, prefer_skill: bool) -> None:
        self.provider_preferences[provider] = prefer_skill

    def resolve(
        self,
        provider: str,
        adapter_type: AdapterType,
        force_refresh_skills: bool = False,
    ) -> ResolvedAdapterTarget:
        skill_names = self.discovery.refresh(force=force_refresh_skills)
        prefer_skill = self.provider_preferences.get(provider, True)
        return resolve_adapter_target(
            provider=provider,
            adapter_type=adapter_type,
            available_skill_names=skill_names,
            prefer_skill=prefer_skill,
        )

