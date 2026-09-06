#!/usr/bin/env python3
"""Map code snippets to known vulnerability patterns and Solodit evidence."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

from pydantic import Field
from spoon_ai.tools.base import BaseTool

from solodit_client import SoloditAPIError, SoloditClient


@dataclass
class PatternRule:
    """Pattern rule for lightweight static matching."""

    name: str
    severity: str
    regex: str
    rationale: str
    remediation: str


PATTERN_RULES: List[PatternRule] = [
    PatternRule(
        name="unchecked-low-level-call",
        severity="HIGH",
        regex=r"\.call\s*\{[^}]*\}\s*\([^)]*\)\s*;",
        rationale="Low-level call return values may be ignored, causing silent failure.",
        remediation="Capture success flag and revert when call fails.",
    ),
    PatternRule(
        name="tx-origin-auth",
        severity="HIGH",
        regex=r"tx\.origin",
        rationale="tx.origin based auth can be bypassed via phishing proxy contracts.",
        remediation="Use msg.sender for authorization checks.",
    ),
    PatternRule(
        name="external-call-before-state-update",
        severity="HIGH",
        regex=r"call\(|transfer\(|send\(",
        rationale="Potential reentrancy if external interaction happens before state update.",
        remediation="Apply checks-effects-interactions and use reentrancy guard.",
    ),
    PatternRule(
        name="dangerous-delegatecall",
        severity="HIGH",
        regex=r"delegatecall\(",
        rationale="delegatecall to untrusted target can corrupt storage and control flow.",
        remediation="Restrict target and validate selector/implementation address.",
    ),
]


class AuditPatternMatcherTool(BaseTool):
    """Perform lightweight pattern matching + evidence retrieval from Solodit."""

    name: str = "audit_pattern_matcher"
    description: str = "Match Solidity snippets to known risks and attach Solodit examples"
    parameters: dict = Field(
        default={
            "type": "object",
            "properties": {
                "code_or_summary": {
                    "type": "string",
                    "description": "Solidity snippet or finding summary",
                },
                "evidence_limit": {"type": "integer", "default": 3, "minimum": 1, "maximum": 10},
            },
            "required": ["code_or_summary"],
        }
    )

    async def execute(self, code_or_summary: str, evidence_limit: int = 3) -> str:
        pattern_hits = self._match_patterns(code_or_summary)
        evidence = await self._fetch_evidence(code_or_summary, evidence_limit)

        lines = ["AUDIT PATTERN MATCH REPORT", "=" * 64]

        if not pattern_hits:
            lines.append("No deterministic pattern hit. Consider deeper manual review.")
        else:
            lines.append("Detected Patterns:")
            for idx, hit in enumerate(pattern_hits, start=1):
                lines.extend(
                    [
                        f"[{idx}] {hit['name']} ({hit['severity']})",
                        f"  Why it matters: {hit['rationale']}",
                        f"  Fix: {hit['remediation']}",
                    ]
                )

        lines.append("")
        lines.append("Related Solodit Evidence:")
        if not evidence:
            lines.append("- No similar Solodit findings returned.")
        else:
            for idx, item in enumerate(evidence, start=1):
                lines.extend(
                    [
                        f"[{idx}] {item['title']} ({item['severity']})",
                        f"  Category: {item['category']} | Project: {item['project']}",
                        f"  Summary: {item['summary']}",
                        f"  Source: {item['source_url'] or 'N/A'}",
                    ]
                )

        return "\n".join(lines)

    def _match_patterns(self, content: str) -> List[Dict[str, str]]:
        matches: List[Dict[str, str]] = []
        for rule in PATTERN_RULES:
            if re.search(rule.regex, content, flags=re.IGNORECASE | re.MULTILINE):
                matches.append(
                    {
                        "name": rule.name,
                        "severity": rule.severity,
                        "rationale": rule.rationale,
                        "remediation": rule.remediation,
                    }
                )
        return matches

    async def _fetch_evidence(self, content: str, limit: int) -> List[Dict[str, str]]:
        client = SoloditClient()
        try:
            return await client.similar_findings(text=content, limit=limit)
        except SoloditAPIError:
            return []


if __name__ == "__main__":
    import asyncio

    async def _demo() -> None:
        tool = AuditPatternMatcherTool()
        snippet = """
        function withdraw(uint256 amount) external {
            (bool ok,) = msg.sender.call{value: amount}("");
            balances[msg.sender] -= amount;
            require(ok, 'failed');
        }
        """
        print(await tool.execute(code_or_summary=snippet, evidence_limit=2))

    asyncio.run(_demo())
