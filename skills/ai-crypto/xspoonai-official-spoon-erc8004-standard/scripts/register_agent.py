#!/usr/bin/env python3
"""Register an agent on-chain using ERC-8004."""

import os
import json
from spoon_ai.identity.erc8004_client import ERC8004Client


# Contract addresses (NeoX Testnet)
CONTRACTS = {
    "agent_registry": "0xaB5623F3DD66f2a52027FA06007C78c7b0E63508",
    "identity_registry": "0x8bb086D12659D6e2c7220b07152255d10b2fB049",
    "reputation_registry": "0x18A9240c99c7283d9332B738f9C6972b5B59aEc2",
    "validation_registry": "0x..."
}


def register_agent(
    did: str,
    agent_card_uri: str,
    did_doc_uri: str
) -> str:
    """Register an agent on-chain.

    Args:
        did: Decentralized identifier (e.g., "did:spoon:my_agent")
        agent_card_uri: URI to agent card JSON
        did_doc_uri: URI to DID document JSON

    Returns:
        Transaction hash
    """
    client = ERC8004Client(
        rpc_url=os.getenv("RPC_URL", "https://testnet.rpc.banelabs.org"),
        agent_registry_address=CONTRACTS["agent_registry"],
        identity_registry_address=CONTRACTS["identity_registry"],
        reputation_registry_address=CONTRACTS["reputation_registry"],
        validation_registry_address=CONTRACTS["validation_registry"],
        private_key=os.getenv("PRIVATE_KEY")
    )

    tx_hash = client.register_agent(
        did=did,
        agent_card_uri=agent_card_uri,
        did_doc_uri=did_doc_uri
    )

    return tx_hash


def main():
    # Example registration
    did = "did:spoon:my_trading_agent"
    agent_card_uri = "ipfs://QmXyz.../agent_card.json"
    did_doc_uri = "ipfs://QmXyz.../did_document.json"

    try:
        tx_hash = register_agent(did, agent_card_uri, did_doc_uri)
        print(f"Agent registered successfully!")
        print(f"DID: {did}")
        print(f"Transaction: {tx_hash}")
    except Exception as e:
        print(f"Registration failed: {e}")


if __name__ == "__main__":
    main()
