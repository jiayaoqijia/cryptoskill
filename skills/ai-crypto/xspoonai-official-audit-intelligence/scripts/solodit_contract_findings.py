#!/usr/bin/env python3
"""Fetch and summarize findings by project/contract from Solodit."""

from __future__ import annotations

from collections import Counter

from pydantic import Field
from spoon_ai.tools.base import BaseTool

from solodit_client import SoloditAPIError, SoloditClient


class SoloditProjectFindingsTool(BaseTool):
    """Aggregate findings for a specific project/address."""

    name: str = "solodit_project_findings"
    description: str = "Retrieve and aggregate findings for a project or contract address"
    parameters: dict = Field(
        default={
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "Project name, protocol slug, or contract address",
                },
                "limit": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
            },
            "required": ["project"],
        }
    )

    async def execute(self, project: str, limit: int = 20) -> str:
        client = SoloditClient()
        try:
            findings = await client.get_project_findings(project=project, limit=limit)
        except SoloditAPIError as exc:
            return f"Solodit project lookup failed: {exc}"

        if not findings:
            return f"No findings associated with '{project}'."

        sev_counter = Counter(item["severity"] for item in findings)
        cat_counter = Counter(item["category"] for item in findings)

        lines = [
            "PROJECT AUDIT FINDINGS REPORT",
            "=" * 64,
            f"Target: {project}",
            f"Total Findings: {len(findings)}",
            f"Severity Breakdown: {dict(sev_counter)}",
            f"Top Categories: {cat_counter.most_common(5)}",
            "",
            "Top Findings:",
        ]

        for idx, item in enumerate(findings[:10], start=1):
            lines.extend(
                [
                    f"[{idx}] {item['title']} ({item['severity']})",
                    f"  Category: {item['category']} | Date: {item['published_at']}",
                    f"  Recommendation: {item['recommendation']}",
                    f"  Source: {item['source_url'] or 'N/A'}",
                ]
            )

        return "\n".join(lines)


if __name__ == "__main__":
    import asyncio

    async def _demo() -> None:
        tool = SoloditProjectFindingsTool()
        print(await tool.execute(project="uniswap", limit=10))

    asyncio.run(_demo())
