#!/usr/bin/env python3
"""Snapshot Proposal Monitoring."""

import aiohttp
from datetime import datetime
from spoon_ai.tools.base import BaseTool
from pydantic import Field

SNAPSHOT_API = "https://hub.snapshot.org/graphql"


class SnapshotMonitorTool(BaseTool):
    """Monitor Snapshot governance proposals."""

    name: str = "snapshot_proposals"
    description: str = "Monitor Snapshot governance proposals"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "space": {"type": "string", "description": "Snapshot space ID (e.g., 'uniswap.eth')"},
            "state": {"type": "string", "enum": ["active", "pending", "closed", "all"], "default": "active"},
            "limit": {"type": "integer", "default": 10}
        },
        "required": ["space"]
    })

    async def execute(self, space: str, state: str = "active", limit: int = 10) -> str:
        query = """
        query Proposals($space: String!, $state: String!, $limit: Int!) {
            proposals(
                first: $limit,
                where: { space: $space, state: $state },
                orderBy: "created",
                orderDirection: desc
            ) {
                id
                title
                body
                choices
                start
                end
                state
                scores
                scores_total
                votes
                author
                space {
                    id
                    name
                }
            }
        }
        """

        variables = {
            "space": space,
            "state": state if state != "all" else None,
            "limit": limit
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                SNAPSHOT_API,
                json={"query": query, "variables": variables}
            ) as resp:
                if resp.status != 200:
                    return f"Error: {resp.status}"
                data = await resp.json()

        proposals = data.get("data", {}).get("proposals", [])

        if not proposals:
            return f"No {state} proposals found for {space}"

        report = f"SNAPSHOT PROPOSALS: {space}\n{'='*50}\n\n"

        for p in proposals:
            end_time = datetime.fromtimestamp(p["end"])
            time_left = end_time - datetime.now()

            report += f"{p['title']}\n"
            report += f"ID: {p['id'][:20]}...\n"
            report += f"State: {p['state'].upper()}\n"
            report += f"Votes: {p['votes']:,}\n"

            if p['choices'] and p['scores']:
                report += "Results:\n"
                for i, choice in enumerate(p['choices']):
                    score = p['scores'][i] if i < len(p['scores']) else 0
                    total = p['scores_total'] or 1
                    pct = (score / total) * 100
                    report += f"  - {choice}: {pct:.1f}%\n"

            if p['state'] == 'active':
                report += f"Ends: {end_time.strftime('%Y-%m-%d %H:%M')} ({time_left.days}d {time_left.seconds//3600}h left)\n"

            report += "\n"

        return report


async def main():
    tool = SnapshotMonitorTool()
    result = await tool.execute(space="uniswap.eth", state="active", limit=5)
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
