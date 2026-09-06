---
name: spoon-erc8004-standard
description: Implement ERC-8004 trustless agent identity. Use when registering agents on-chain, managing reputation, handling validation, or generating DID documents.
---

# ERC-8004 Standard

Implement trustless on-chain agent identity with ERC-8004.

## Overview

ERC-8004 provides:
- On-chain agent registration
- Decentralized identity (DID)
- Reputation tracking
- Validation mechanisms

## Quick Start

```python
from spoon_ai.identity.erc8004_client import ERC8004Client

client = ERC8004Client(
    rpc_url="https://testnet.rpc.banelabs.org",
    agent_registry_address="0x...",
    identity_registry_address="0x...",
    reputation_registry_address="0x...",
    validation_registry_address="0x...",
    private_key=os.getenv("PRIVATE_KEY")
)

# Register agent
tx_hash = client.register_agent(
    did="did:spoon:agent123",
    agent_card_uri="https://storage.example.com/card.json",
    did_doc_uri="https://storage.example.com/did.json"
)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [register_agent.py](scripts/register_agent.py) | Agent registration |
| [resolve_agent.py](scripts/resolve_agent.py) | DID resolution |
| [update_reputation.py](scripts/update_reputation.py) | Reputation management |
| [generate_did.py](scripts/generate_did.py) | DID document generation |

## References

| Reference | Content |
|-----------|---------|
| [contracts.md](references/contracts.md) | Contract addresses |
| [did_format.md](references/did_format.md) | DID document format |

## Contract Addresses (NeoX Testnet)

| Contract | Address |
|----------|---------|
| AgentRegistry | `0xaB5623F3DD66f2a52027FA06007C78c7b0E63508` |
| IdentityRegistry | `0x8bb086D12659D6e2c7220b07152255d10b2fB049` |
| ReputationRegistry | `0x18A9240c99c7283d9332B738f9C6972b5B59aEc2` |

## Best Practices

1. Store agent cards on IPFS/Arweave
2. Use EIP-712 signatures for registration
3. Monitor reputation changes
4. Implement validation before transactions
