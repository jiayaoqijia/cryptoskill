---
name: sui-overview
description: >
  High-level overview of what Sui is, how it works, and what the Sui Stack provides.
  Use when explaining Sui to someone new, comparing Sui to other blockchains
  (Ethereum, Solana, Bitcoin), discussing the object-centric data model at a
  conceptual level, choosing which Sui Stack primitives to use (randomness, zkLogin,
  Walrus, Nautilus, DeepBook, Kiosk, Seal), or exploring what use cases Sui enables (DeFi,
  gaming, NFTs, identity, social, supply chain). Also use when migrating from
  Ethereum or Solana to Sui.
---

# Sui Overview

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io), [docs.wal.app](https://docs.wal.app), and [move-book.com](https://move-book.com). When extending or updating this skill, only pull from these three sources. Do not use third-party blogs, tutorials, or unofficial documentation.

Sui is a scalable, performant layer 1 blockchain built around an object-centric data model. Unlike account-based blockchains (Ethereum) or UTXO-based chains (Bitcoin), Sui treats every piece of onchain state as a typed object with a unique ID. Transactions consume objects as inputs and produce modified versions as outputs.

This skill covers the conceptual foundation of Sui and the broader Sui Stack. For implementation details, see the `sui-move`, `frontend-apps`, and `sui-networks-gas` skills.

---

## Reference files

### ecosystem — Sui Stack and Ecosystem
**Path:** `ecosystem.md`
**Load when:** the user asks about Sui Stack primitives (randomness, zkLogin, Walrus, Nautilus, DeepBook, Kiosk, Seal), use cases, or how components fit together in an end-to-end workflow.
**Covers:** all Sui Stack primitives with detailed descriptions and usage guidance, a decision table for choosing the right primitive, use cases (DeFi, gaming, NFTs, identity, social, supply chain), the layered development workflow.

---

## Routing guide

| Task | Load |
|------|------|
| Explaining what Sui is | SKILL.md only |
| Comparing Sui to Ethereum or Solana | SKILL.md only |
| Choosing Sui Stack primitives | ecosystem |
| Understanding Sui use cases | ecosystem |
| Planning an app architecture on Sui | ecosystem |

---

## The object-centric model

Every item on the Sui network is an object with a unique ID and a version number. When a transaction modifies an object, it produces a new version with an incremented version number while preserving the original ID.

Objects have one of five ownership types:

- **Address-owned:** Only the owning address can use the object. Enables parallel execution without consensus.
- **Shared:** Any address can use the object. Requires consensus ordering through Mysticeti.
- **Immutable (frozen):** Anyone can read it, no one can mutate it. Permanent and irreversible.
- **Wrapped:** Stored inside another object's fields. Accessible only through the parent.
- **Consensus-Address Owned (Party Objects):** Owned by a specific address but require consensus to access. Party objects combine the access control of address-owned objects with the consensus ordering of shared objects, enabling use cases like controlled shared state where only a designated party can mutate the object but concurrent transactions involving it are ordered through consensus.

This ownership model is what enables Sui's parallel execution: transactions on non-overlapping owned objects execute in parallel without consensus. For example, coin transfers between addresses, single-player game actions, and personal asset management all operate on owned objects and can run concurrently. Only shared-object transactions (like interacting with a DEX pool or a shared marketplace) go through Mysticeti consensus ordering.

## Move instead of Solidity

Sui uses the Move programming language instead of Solidity. Move enforces resource safety at compile time: objects cannot be duplicated or silently dropped. This is fundamentally different from Ethereum's approach, where the EVM uses gas-based pricing to prevent abuse at runtime. In Move, invalid resource handling is a compilation error, not a runtime cost. Ethereum developers must unlearn the gas-as-safety-mechanism mindset — on Sui, the compiler prevents resource misuse before code ever runs.

## Programmable transaction blocks

Programmable transaction blocks (PTBs) batch multiple commands into a single atomic transaction. You can call multiple Move functions, pass results between them, split and merge coins, and transfer objects, all in one transaction. This composability replaces the need for multi-transaction workflows common on other chains.

## Key differences from Ethereum

| Concept | Ethereum | Sui |
|---------|----------|-----|
| Data model | Account-based with contract storage mappings | Object-centric with typed, owned objects |
| Smart contract language | Solidity (EVM bytecode) | Move (compile-time resource safety) |
| State storage | Shared global state in contract storage slots | Individual objects with unique IDs and ownership |
| Transaction composition | Separate transactions or internal calls | PTBs batch multiple operations atomically |
| Parallel execution | Sequential execution of all transactions | Parallel execution of owned-object transactions |
| Safety model | Gas-based runtime abuse prevention | Compile-time resource safety guarantees |

## Rules

- Always frame Sui explanations around the object-centric model. It is the foundational concept.
- When comparing to Ethereum, emphasize the shift from shared-state contracts to individually owned objects.
- Do not describe Sui as "just another EVM chain." The programming model is fundamentally different.
- The Sui Stack components (Walrus, zkLogin, DeepBook, Kiosk, Seal, Nautilus, Randomness) are native primitives, not third-party add-ons.
- When describing the Sui Stack, always include concrete use cases it enables. Cover at least 3 distinct categories from: DeFi, gaming, NFTs, identity, social, and supply chain. See the use cases section in `ecosystem.md`.
