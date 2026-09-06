---
name: web3-dao-tooling
description: Build DAO governance agents with SpoonOS. Use when monitoring proposals, automating voting, managing delegations, or analyzing governance patterns.
---

# DAO Tooling

Automate DAO governance participation with SpoonOS agents.

## Supported Platforms

| Platform | Type | Chains |
|----------|------|--------|
| Snapshot | Off-chain voting | All EVM |
| Tally | On-chain Governor | ETH, Polygon, Arbitrum, Optimism |
| Compound Governor | On-chain | ETH |
| Aragon | On-chain DAO | ETH, Polygon |

## Snapshot Integration

### API Configuration

```python
SNAPSHOT_API = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORE_API = "https://score.snapshot.org"
```

### Proposal Monitor

```python
# scripts/snapshot_monitor.py
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field
from datetime import datetime

class SnapshotMonitorTool(BaseTool):
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

            report += f"""
{p['title']}
ID: {p['id'][:20]}...
State: {p['state'].upper()}
Votes: {p['votes']:,}
"""

            # Show choices with scores
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
```

### Snapshot Voting

```python
# scripts/snapshot_vote.py
import aiohttp
from eth_account import Account
from eth_account.messages import encode_defunct
import json
import time

class SnapshotVoteTool(BaseTool):
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
            async with session.post(
                "https://seq.snapshot.org",
                json=payload
            ) as resp:
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
```

## Tally Integration

### Tally API

```python
TALLY_API = "https://api.tally.xyz/query"

class TallyMonitorTool(BaseTool):
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

        report = f"TALLY GOVERNANCE: {governor}\n{'='*50}\n\n"

        for p in proposals:
            votes = p.get("votes", {})

            report += f"""
{p['title']}
Status: {p['status']}
Proposer: {p['proposer']['name'] or p['proposer']['address'][:10]}...

Votes:
  For: {int(votes.get('for', 0)):,}
  Against: {int(votes.get('against', 0)):,}
  Abstain: {int(votes.get('abstain', 0)):,}

"""

        return report
```

## On-Chain Voting

### Governor Contract Integration

```python
# scripts/governor_vote.py
from web3 import Web3
from spoon_ai.tools.base import BaseTool
from pydantic import Field

# Standard Governor ABI functions
GOVERNOR_ABI = [
    {
        "name": "castVote",
        "inputs": [
            {"name": "proposalId", "type": "uint256"},
            {"name": "support", "type": "uint8"}
        ],
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "name": "castVoteWithReason",
        "inputs": [
            {"name": "proposalId", "type": "uint256"},
            {"name": "support", "type": "uint8"},
            {"name": "reason", "type": "string"}
        ],
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "name": "state",
        "inputs": [{"name": "proposalId", "type": "uint256"}],
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
        "stateMutability": "view"
    }
]

# Vote support values
VOTE_AGAINST = 0
VOTE_FOR = 1
VOTE_ABSTAIN = 2

class GovernorVoteTool(BaseTool):
    name: str = "governor_vote"
    description: str = "Cast on-chain vote on Governor proposal"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "governor_address": {"type": "string"},
            "proposal_id": {"type": "string"},
            "support": {"type": "string", "enum": ["for", "against", "abstain"]},
            "reason": {"type": "string", "default": ""},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["governor_address", "proposal_id", "support"]
    })

    async def execute(self, governor_address: str, proposal_id: str,
                      support: str, reason: str = "", chain: str = "ethereum") -> str:
        w3 = Web3(Web3.HTTPProvider(RPC_URLS[chain]))
        account = Account.from_key(os.getenv("PRIVATE_KEY"))

        contract = w3.eth.contract(
            address=Web3.to_checksum_address(governor_address),
            abi=GOVERNOR_ABI
        )

        # Map support string to uint8
        support_value = {
            "for": VOTE_FOR,
            "against": VOTE_AGAINST,
            "abstain": VOTE_ABSTAIN
        }[support]

        # Check proposal state
        state = contract.functions.state(int(proposal_id)).call()
        if state != 1:  # 1 = Active
            states = ["Pending", "Active", "Canceled", "Defeated",
                     "Succeeded", "Queued", "Expired", "Executed"]
            return f"Cannot vote: Proposal is {states[state]}"

        # Build transaction
        if reason:
            tx_func = contract.functions.castVoteWithReason(
                int(proposal_id),
                support_value,
                reason
            )
        else:
            tx_func = contract.functions.castVote(
                int(proposal_id),
                support_value
            )

        tx = tx_func.build_transaction({
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 200000,
            "maxFeePerGas": w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": w3.to_wei(2, "gwei")
        })

        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            return f"""
ON-CHAIN VOTE SUBMITTED
{'='*40}
Governor: {governor_address}
Proposal: {proposal_id}
Vote: {support.upper()}
Tx: {tx_hash.hex()}
Gas Used: {receipt.gasUsed:,}
"""
        else:
            return f"Vote transaction failed: {tx_hash.hex()}"
```

## Delegation Management

```python
# scripts/delegation.py
class DelegationTool(BaseTool):
    name: str = "manage_delegation"
    description: str = "Delegate voting power to another address"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token_address": {"type": "string", "description": "Governance token address"},
            "delegate_to": {"type": "string", "description": "Address to delegate to"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["token_address", "delegate_to"]
    })

    async def execute(self, token_address: str, delegate_to: str,
                      chain: str = "ethereum") -> str:
        w3 = Web3(Web3.HTTPProvider(RPC_URLS[chain]))
        account = Account.from_key(os.getenv("PRIVATE_KEY"))

        # ERC20Votes delegate function
        delegate_abi = [{
            "name": "delegate",
            "inputs": [{"name": "delegatee", "type": "address"}],
            "outputs": [],
            "type": "function"
        }]

        contract = w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=delegate_abi
        )

        tx = contract.functions.delegate(
            Web3.to_checksum_address(delegate_to)
        ).build_transaction({
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 100000,
            "maxFeePerGas": w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": w3.to_wei(2, "gwei")
        })

        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            return f"""
DELEGATION SUCCESSFUL
{'='*40}
Token: {token_address}
Delegated to: {delegate_to}
Tx: {tx_hash.hex()}
"""
        else:
            return f"Delegation failed: {tx_hash.hex()}"
```

## DAO Agent Example

```python
# scripts/dao_agent.py
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

class DAOGovernanceAgent(SpoonReactMCP):
    name = "dao_governance_agent"
    description = "Automated DAO governance participation"

    system_prompt = """You are a DAO governance assistant.

CAPABILITIES:
- Monitor proposals on Snapshot and Tally
- Analyze proposal impact and voting patterns
- Execute votes (with user confirmation)
- Manage delegation settings

GOVERNANCE RULES:
- Always explain proposal implications before voting
- Require explicit confirmation for on-chain votes
- Track voting history and reasoning
- Consider quorum requirements

SUPPORTED PLATFORMS:
- Snapshot (off-chain, gasless)
- Tally (on-chain Governor contracts)
- Compound Governor
"""

    def __init__(self):
        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([
                SnapshotMonitorTool(),
                SnapshotVoteTool(),
                TallyMonitorTool(),
                GovernorVoteTool(),
                DelegationTool()
            ]),
            max_steps=10
        )
```

## Environment Variables

```bash
# API Keys
TALLY_API_KEY=...

# Wallet
PRIVATE_KEY=0x...

# RPC
ETHEREUM_RPC=https://eth.llamarpc.com
```

## Best Practices

1. **Review Before Voting** - Always analyze proposal impact
2. **Gas Optimization** - Use Snapshot for non-critical votes
3. **Delegation Strategy** - Delegate to active, aligned delegates
4. **Track Participation** - Monitor voting power and history
5. **Quorum Awareness** - Check quorum before voting
