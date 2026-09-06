#!/usr/bin/env python3
"""DAO Assistant Agent Template."""

import os
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool
from pydantic import Field


class ProposalMonitorTool(BaseTool):
    """Monitor DAO proposals on Snapshot/Tally."""

    name: str = "proposal_monitor"
    description: str = "Get active proposals from DAOs"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "dao": {"type": "string", "description": "DAO name or ENS"},
            "status": {"type": "string", "enum": ["active", "pending", "closed"], "default": "active"}
        },
        "required": ["dao"]
    })

    async def execute(self, dao: str, status: str = "active") -> str:
        import aiohttp

        # Snapshot GraphQL API
        url = "https://hub.snapshot.org/graphql"
        query = """
        query Proposals($space: String!, $state: String!) {
            proposals(
                where: { space: $space, state: $state }
                first: 5
                orderBy: "created"
                orderDirection: desc
            ) {
                id
                title
                state
                scores_total
                end
            }
        }
        """

        variables = {"space": dao, "state": status}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"query": query, "variables": variables}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    proposals = data.get("data", {}).get("proposals", [])

                    result = f"Active proposals for {dao}:\n"
                    for p in proposals:
                        result += f"- {p['title']} (votes: {p['scores_total']:.0f})\n"
                    return result

                return f"Error fetching proposals: {await resp.text()}"


class VotingTool(BaseTool):
    """Execute votes on DAO proposals."""

    name: str = "vote"
    description: str = "Cast vote on a proposal"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "proposal_id": {"type": "string"},
            "choice": {"type": "integer", "description": "Choice index (1-based)"},
            "reason": {"type": "string"}
        },
        "required": ["proposal_id", "choice"]
    })

    async def execute(self, proposal_id: str, choice: int, reason: str = None) -> str:
        # Implementation would sign and submit vote
        return f"Vote cast: choice {choice} on proposal {proposal_id}"


class DelegationTool(BaseTool):
    """Manage voting power delegation."""

    name: str = "delegation"
    description: str = "Delegate or check voting power"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["check", "delegate", "undelegate"]},
            "dao": {"type": "string"},
            "delegate_to": {"type": "string"}
        },
        "required": ["action", "dao"]
    })

    async def execute(self, action: str, dao: str, delegate_to: str = None) -> str:
        if action == "check":
            return f"Your voting power in {dao}: 1000 tokens"
        elif action == "delegate":
            return f"Delegated voting power to {delegate_to}"
        return "Delegation revoked"


class DAOAssistantAgent(SpoonReactMCP):
    """DAO governance participation agent."""

    name = "dao_assistant"
    description = "DAO governance participation agent"

    system_prompt = """You are a DAO governance assistant.

    CAPABILITIES:
    - Monitor active proposals on Snapshot/Tally
    - Analyze proposal impact and voting patterns
    - Execute votes based on configured preferences
    - Manage delegation settings

    GOVERNANCE PROTOCOLS:
    - Snapshot (off-chain): gasless voting
    - Tally (on-chain): Governor contracts
    - Compound Governor: timelock execution
    """

    def __init__(self):
        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([
                ProposalMonitorTool(),
                VotingTool(),
                DelegationTool()
            ])
        )


async def main():
    agent = DAOAssistantAgent()
    result = await agent.run("Show me active Uniswap proposals")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
