---
name: cardano-transactions
description: "Sign and submit Cardano transactions with explicit user confirmation."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "📤"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---

# Cardano Transactions

Sign and submit Cardano transactions with explicit user confirmation.

## Prerequisites

- `@indigoprotocol/cardano-mcp` server running

## MCP Tools

- `submit_transaction` — Sign and submit a Cardano transaction CBOR

## When to use

Use this skill when the user asks to:

- Submit or send a Cardano transaction
- Sign a transaction with their wallet
- Broadcast a pre-built transaction

## Safety model

**This tool is dangerous.** Before calling `submit_transaction`:

1. Summarize the transaction in plain English.
2. Ask the user to explicitly confirm.
3. Only proceed if the user says yes.
4. **Never submit a transaction automatically.**

## Data interpretation

- Input requires unsigned transaction CBOR (hex string).
- Output includes `transactionHash` and `timestamp` on success.
- The transaction is signed by the connected wallet's keys.
