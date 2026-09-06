#!/usr/bin/env python3
"""Search Solodit findings and produce an audit-oriented report."""

from __future__ import annotations

from typing import List

from pydantic import Field
from spoon_ai.tools.base import BaseTool

from solodit_client import SoloditAPIError, SoloditClient


class SoloditSearchTool(BaseTool):
    """Search findings by vulnerability keyword."""

    name: str = "solodit_search_findings"
    description: str = "Search Solodit findings by keyword, severity and sort mode"
    parameters: dict = Field(
        default={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keyword or vulnerability phrase"},
                "severities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional severities, e.g. ['HIGH', 'MEDIUM']",
                },
                "limit": {"type": "integer", "default": 8, "minimum": 1, "maximum": 50},
                "sort_by": {
                    "type": "string",
                    "default": "recency",
                    "enum": ["recency", "severity", "relevance"],
                },
            },
            "required": ["query"],
        }
    )

    async def execute(
        self,
        query: str,
        severities: List[str] | None = None,
        limit: int = 8,
        sort_by: str = "recency",
    ) -> str:
        client = SoloditClient()
        try:
            findings = await client.search_findings(
                query=query,
                severities=severities,
                limit=limit,
                sort_by=sort_by,
            )
        except SoloditAPIError as exc:
            return f"Solodit search failed: {exc}"

        if not findings:
            return f"No Solodit findings found for query='{query}'."

        lines = [
            "SOLODIT SEARCH REPORT",
            "=" * 64,
            f"Query: {query}",
            f"Results: {len(findings)}",
            "",
        ]

        for idx, item in enumerate(findings, start=1):
            lines.extend(
                [
                    f"[{idx}] {item['title']}",
                    f"  Severity: {item['severity']} | Category: {item['category']} | Project: {item['project']}",
                    f"  Summary: {item['summary']}",
                    f"  Recommendation: {item['recommendation']}",
                    f"  Evidence: {item['source_url'] or 'N/A'}",
                    "",
                ]
            )

        return "\n".join(lines)


if __name__ == "__main__":
    import asyncio

    async def _demo() -> None:
        tool = SoloditSearchTool()
        print(await tool.execute(query="reentrancy", severities=["HIGH", "MEDIUM"], limit=5))

    asyncio.run(_demo())
