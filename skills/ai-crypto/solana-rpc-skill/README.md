# Solana JSON-RPC — AI-agent skill

> **Generated distribution mirror.** The canonical source, issues, and releases live in [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills). Do not hand-edit generated files in this repository.

Provider-neutral Solana JSON-RPC skill and Python examples for batching, transaction retrieval, and enhanced APIs.

- Canonical skill: [https://github.com/Vo1ganin/crypto-claude-skills/tree/main/skills/solana-rpc](https://github.com/Vo1ganin/crypto-claude-skills/tree/main/skills/solana-rpc)
- Collection: [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills)
- Provenance: [`.source.json`](.source.json)

## Skill documentation

Universal Solana JSON-RPC skill for Claude Code — works with [Helius](https://www.helius.dev), [QuickNode](https://www.quicknode.com), [Triton](https://triton.one), [Ankr](https://www.ankr.com), [Chainstack](https://chainstack.com), or public endpoints.

Standard Solana RPC methods are identical across providers; only the URL differs. Provider-specific extensions (Helius DAS, QuickNode addons, etc.) covered in separate reference files.

## What it does

- Standard Solana JSON-RPC operations: accounts, blocks, transactions, signatures, tokens, fees
- Helius-specific APIs: DAS (NFTs + tokens), Enhanced Transactions, Priority Fee, Sender, Webhooks, LaserStream
- QuickNode-specific addons: `qn_estimatePriorityFees`, Metaplex DAS, Jito (Lil JIT), Yellowstone Geyser
- JSON-RPC batch requests (array-of-methods in one HTTP call)
- Multi-provider fallback

## When it triggers

Any request involving direct Solana node access: fetch raw tx, read account state, get block data, query program accounts, submit transactions, estimate priority fees, stream real-time data.

Also triggers on explicit mentions of Helius / QuickNode or their specific features.

## Files

| File | Purpose |
|------|---------|
| [`SKILL.md`](SKILL.md) | Three hard rules, provider setup, workflow |
| [`references/core-methods.md`](references/core-methods.md) | Standard Solana JSON-RPC: accounts, blocks, tx, fees |
| [`references/helius-extensions.md`](references/helius-extensions.md) | DAS API, Enhanced Tx, Priority Fee, Sender, Webhooks, LaserStream |
| [`references/quicknode-extensions.md`](references/quicknode-extensions.md) | `qn_estimatePriorityFees`, DAS addon, Lil JIT, Metis, Yellowstone |
| [`references/patterns.md`](references/patterns.md) | JSON-RPC batching, semaphore tuning, fallback, cost heuristics |
| [`references/examples/fetch_tx_batch.py`](references/examples/fetch_tx_batch.py) | Batch `getTransaction` via JSON-RPC arrays — any provider |
| [`references/examples/wallet_full_history.py`](references/examples/wallet_full_history.py) | Helius `getTransactionsForAddress` with pagination + resume |
| [`references/examples/wallet_holdings_das.py`](references/examples/wallet_holdings_das.py) | DAS `getAssetsByOwner` with `showFungible` + `showNativeBalance` |

## Key rules

1. **Prefer parsed/enhanced APIs** — Helius Enhanced Tx beats raw `getSignaturesForAddress` + N × `getTransaction`; DAS beats `getTokenAccountsByOwner` + metadata lookups
2. **JSON-RPC batching** — send up to 100 methods per HTTP request via array body
3. **Never `getProgramAccounts` without `dataSize` and `memcmp` filters** — otherwise scans all program accounts, times out
4. **Always include `maxSupportedTransactionVersion: 0`** in tx-method configs (v0 transactions fail otherwise)
5. **Default commitment: `confirmed`** for reads, `finalized` for financial history, never `processed` for production

## Provider cheat-sheet

| Use case | Provider |
|----------|----------|
| NFTs & cNFTs | Helius (DAS polished) |
| Parsed tx for analytics | Helius (Enhanced Tx) |
| Real-time streams | Helius LaserStream or QuickNode Yellowstone |
| MEV / Jito bundles | QuickNode Lil JIT |
| Raw high-throughput RPC | Either — pick based on pricing |

## Quick example

```
> "Fetch full wallet history for 5EMW...R on Helius"

Skill:
  → Detects SOLANA_RPC_URL is Helius
  → Uses getTransactionsForAddress (Enhanced) with pagination
  → Parsed output includes NFT sales, swaps, transfers labeled
  → Resume-safe JSONL to wallet_history.jsonl
```

## Setup

Set `SOLANA_RPC_URL` in `.env` with your provider's endpoint. For fallback support, add `SOLANA_RPC_URL_PRIMARY` and `SOLANA_RPC_URL_FALLBACK`.

See [`INSTALL.md`](INSTALL.md) for details.
