from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from time import time


_NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)


@dataclass
class SkillDiscoveryService:
    skill_roots: list[Path]
    ttl_seconds: int = 300
    _last_refresh_ts: float = 0.0
    _skills: list[str] = field(default_factory=list)

    def refresh(self, force: bool = False) -> list[str]:
        now = time()
        if not force and self._skills and (now - self._last_refresh_ts) < self.ttl_seconds:
            return self._skills

        skills: list[str] = []
        for root in self.skill_roots:
            if not root.exists():
                continue
            for skill_md in root.rglob("SKILL.md"):
                text = skill_md.read_text(encoding="utf-8", errors="ignore")
                match = _NAME_RE.search(text)
                if match:
                    skills.append(match.group(1).strip().strip("\"'"))
                else:
                    skills.append(skill_md.parent.name)

        self._skills = sorted({s.lower() for s in skills})
        self._last_refresh_ts = now
        return self._skills

    def available_skills(self) -> list[str]:
        return self.refresh(force=False)

