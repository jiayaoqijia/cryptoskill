#!/usr/bin/env python3
"""Tally On-Chain Governance Monitoring."""

import os
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

TALLY_API = "https://api.tally.xyz/query"


class TallyMonitorTool(BaseTool):
    """Monitor on-chain governance proposals via Tally."""

    name: str = "tally_proposals"
    description: str = "Monitor on-chain governance via Tally"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "governor": {"type": "string", "description": "Governor contract or organization slug"},
            "status": {"type": "string", "enum": ["active", "pending", "executed", "all"], "default": "active"}
        },
        "required": ["governor"]
    })

    async def execute(self, governor: str, status: str = "active") -> str:
        query = """
        query Proposals($governor: Address!, $status: ProposalStatusType) {
            proposals(
                chainId: "eip155:1"
                governors: [$governor]
                statuses: [$status]
                first: 10
            ) {
                nodes {
                    id
                    title
                    description
                    status
                    votes {
                        for
                        against
                        abstain
                    }
                    proposer {
                        address
                        name
                    }
                    voteStats {
                        percent
                        type
                    }
                }
            }
        }
        """

        headers = {
            "Api-Key": os.getenv("TALLY_API_KEY"),
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                TALLY_API,
                headers=headers,
                json={"query": query, "variables": {"governor": governor, "status": status.upper()}}
            ) as resp:
                if resp.status != 200:
                    return f"Error: {resp.status}"

                data = await resp.json()

        proposals = data.get("data", {}).get("proposals", {}).get("nodes", [])

        if not proposals:
            return f"No {status} proposals found for {governor}"

        report = f"TALLY GOVERNANCE: {governor}\n{'='*50}\n\n"

        for p in proposals:
            votes = p.get("votes", {})

            report += f"{p['title']}\n"
            report += f"Status: {p['status']}\n"
            proposer = p.get('proposer', {})
            proposer_name = proposer.get('name') or proposer.get('address', 'Unknown')[:10] + '...'
            report += f"Proposer: {proposer_name}\n"
            report += "\nVotes:\n"
            report += f"  For: {int(votes.get('for', 0)):,}\n"
            report += f"  Against: {int(votes.get('against', 0)):,}\n"
            report += f"  Abstain: {int(votes.get('abstain', 0)):,}\n"
            report += "\n"

        return report


async def main():
    tool = TallyMonitorTool()
    print("TallyMonitorTool ready - requires TALLY_API_KEY env var")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
