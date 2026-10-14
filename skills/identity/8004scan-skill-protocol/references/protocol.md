# ERC-8004: Trustless Agents — Protocol Overview

## Status

Draft EIP, deployed on Ethereum mainnet (January 29, 2026) and 30+ chains.

## Authors

Marco De Rossi (MetaMask), Davide Crapis (Ethereum Foundation), Jordan Ellis (Google), Erik Reppel (Coinbase).

## Abstract

ERC-8004 establishes a foundational trust and discovery layer for autonomous AI agents through three lightweight on-chain registries. It treats the blockchain as a neutral reference point while pushing most computation off-chain.

## Requires

EIP-155 (chain ID), EIP-712 (typed structured data signing), EIP-721 (NFT), EIP-1271 (smart contract signature verification).

## Three Registries

### 1. Identity Registry (ERC-721)

Every agent gets a portable, censorship-resistant identifier as an NFT. The token's `agentURI` resolves to a **registration file** — a JSON document describing the agent's name, description, endpoints, skills, and trust preferences.

- Mint creates a new agent identity
- Transfer changes ownership
- `agentURI` can point to IPFS, HTTP, or be stored on-chain
- Owners can update metadata at any time

### 2. Reputation Registry

A standard interface for posting and fetching feedback signals. Feedback includes:

- **value**: `int128` — signed integer allowing both positive and negative feedback
- **decimals**: `uint8` — decimal precision (e.g., 2 decimals: value 9977 → 99.77%)
- **tags**: Up to 2 string tags categorizing the feedback (e.g., "starred", "uptime")
- **endpoint**: The specific service endpoint being reviewed
- **payload**: Optional IPFS CID with extended off-chain feedback data

Key properties:
- Anyone can submit feedback for any agent
- Feedback is self-revocable by the submitter
- Agents can respond to feedback (on-chain reference to response)
- Scoring and aggregation happen both on-chain and off-chain

### 3. Validation Registry

Generic hooks for independent third-party checks:

- Agents **request** validation from validators
- Validators **respond** with proof and score (0-100)
- Supports TEE attestation, staking models, and custom proof types
- Validators have their own reputation within the system

## Agent Identifier

**Full form**: `eip155:{chainId}:{identityRegistry}:{tokenId}`
**Short form**: `{chainId}:{tokenId}` (when registry address is known)

Examples:
- `eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432:42`
- `1:42` (Ethereum mainnet, token 42)
- `11155111:7` (Sepolia testnet, token 7)

## Agent Lifecycle

1. **Register**: Mint identity NFT → publish registration file (IPFS/HTTP/on-chain)
2. **Discover**: Search by skills, domains, capabilities, name
3. **Interact**: Call agent endpoints (MCP, A2A, HTTP)
4. **Feedback**: Submit reputation signals after interaction
5. **Validate**: Request third-party attestation for trust
6. **Transfer**: Change ownership via ERC-721 transfer

## What ERC-8004 Does NOT Handle

- Payments/pricing — left to higher-level protocols (x402, etc.)
- Business models — no opinions on monetization
- Off-chain computation — only provides on-chain reference points
- Agent execution — no runtime, just identity and trust

## Glossary

| Term | Definition |
|------|-----------|
| **Agent** | An autonomous software entity with an on-chain identity NFT |
| **agentURI** | The token URI resolving to the agent's registration file |
| **Registration File** | JSON document describing agent capabilities and endpoints |
| **Feedback** | On-chain reputation signal (value + tags + optional payload) |
| **Validation** | Third-party attestation of agent properties |
| **Trust Signal** | Any data point (feedback, validation) that informs trust decisions |
| **OASF** | Open Agent Skill Framework — taxonomy for agent skills/domains |
| **MCP** | Model Context Protocol — agent communication standard |
| **A2A** | Agent-to-Agent protocol — direct agent communication |
