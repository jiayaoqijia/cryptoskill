---
name: cardano-staking
description: "Check stake delegation and available ADA rewards for the connected wallet."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "🥩"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---

# Cardano Staking

Check stake delegation and available ADA rewards for the connected wallet.

## Prerequisites

- `@indigoprotocol/cardano-mcp` server running

## MCP Tools

- `get_stake_delegation` — Retrieve the staked pool ID and available ADA rewards

## When to use

Use this skill when the user asks about:

- Staking status or delegation
- Which stake pool they are delegated to
- Available staking rewards
- ADA rewards they can claim

## Data interpretation

- `poolId` is the bech32 pool identifier (e.g. `pool1...`).
- `availableAdaRewards` is already in ADA (not lovelace).
