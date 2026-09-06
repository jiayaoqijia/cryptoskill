#!/usr/bin/env python3
"""On-Chain Governor Voting."""

import os
from web3 import Web3
from eth_account import Account
from spoon_ai.tools.base import BaseTool
from pydantic import Field

# Vote support values
VOTE_AGAINST = 0
VOTE_FOR = 1
VOTE_ABSTAIN = 2

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

RPC_URLS = {
    "ethereum": "https://eth.llamarpc.com",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io"
}


class GovernorVoteTool(BaseTool):
    """Cast on-chain votes on Governor proposals."""

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
        w3 = Web3(Web3.HTTPProvider(RPC_URLS.get(chain, RPC_URLS["ethereum"])))
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


async def main():
    tool = GovernorVoteTool()
    print("GovernorVoteTool ready - requires PRIVATE_KEY env var")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
