#!/usr/bin/env python3
"""Snapshot Voting Integration."""

import os
import json
import aiohttp
from eth_account import Account
from eth_account.messages import encode_defunct
from spoon_ai.tools.base import BaseTool
from pydantic import Field

SNAPSHOT_API = "https://hub.snapshot.org/graphql"
SNAPSHOT_SEQ = "https://seq.snapshot.org"


class SnapshotVoteTool(BaseTool):
    """Cast votes on Snapshot proposals."""

    name: str = "snapshot_vote"
    description: str = "Cast vote on Snapshot proposal"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "proposal_id": {"type": "string"},
            "choice": {"type": "integer", "description": "Choice index (1-based)"},
            "reason": {"type": "string", "default": ""}
        },
        "required": ["proposal_id", "choice"]
    })

    async def execute(self, proposal_id: str, choice: int, reason: str = "") -> str:
        # Get proposal details first
        proposal = await self._get_proposal(proposal_id)
        if not proposal:
            return f"Proposal {proposal_id} not found"

        space = proposal["space"]["id"]

        # Prepare vote message
        account = Account.from_key(os.getenv("PRIVATE_KEY"))

        vote_data = {
            "space": space,
            "proposal": proposal_id,
            "type": "single-choice",
            "choice": choice,
            "reason": reason,
            "app": "spoonos-agent",
            "metadata": "{}"
        }

        # Sign the vote
        message = json.dumps(vote_data, separators=(',', ':'))
        signable = encode_defunct(text=message)
        signature = account.sign_message(signable)

        # Submit vote
        payload = {
            "address": account.address,
            "sig": signature.signature.hex(),
            "data": vote_data
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(SNAPSHOT_SEQ, json=payload) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    return f"Vote failed: {error}"

                result = await resp.json()

        choice_text = proposal["choices"][choice - 1]

        return f"""
VOTE SUBMITTED
{'='*40}
Proposal: {proposal['title']}
Choice: {choice_text}
Voter: {account.address}
Receipt: {result.get('id', 'N/A')}
"""

    async def _get_proposal(self, proposal_id: str) -> dict:
        query = """
        query Proposal($id: String!) {
            proposal(id: $id) {
                id
                title
                choices
                space {
                    id
                    name
                }
            }
        }
        """

        async with aiohttp.ClientSession() as session:
            async with session.post(
                SNAPSHOT_API,
                json={"query": query, "variables": {"id": proposal_id}}
            ) as resp:
                data = await resp.json()
                return data.get("data", {}).get("proposal")


async def main():
    tool = SnapshotVoteTool()
    print("SnapshotVoteTool ready - requires PRIVATE_KEY env var")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
