---
name: OpenOcean
description: OpenOcean-skills is a skill package for interacting with the OpenOcean Aggregator API. Use it to get swap quotes, build swap transactions, execute swaps, and troubleshoot OpenOcean workflows across 40+ chains, including EVM, Solana, and Sui.
metadata:
  tags:
    - openocean-skills
    - openocean
    - defi
    - dex-aggregator
    - swap
    - quote
    - transaction-build
    - swap-execution
    - evm
    - solana
    - sui
  provider: OpenOcean
  homepage: https://openocean.finance
---

# OpenOcean Skills

Skills for interacting with the [OpenOcean Aggregator API](https://apis.openocean.finance/). Fetch swap quotes, build transaction calldata, and execute swaps across 40+ chains (EVM, Solana, Sui).

## Entry Point and Sub-Skills

This skill package is the **entry point**. Detailed workflows live in the following files under `skills/`:

| User intent | Skill file | When to use |
|-------------|------------|-------------|
| Get quote / check price | `skills/quote/SKILL.md` | "get a swap quote", "check swap price", "how much would I get for" |
| Build transaction | `skills/swap-build/SKILL.md` | "build a swap", "prepare swap transaction", "get swap calldata" |
| Execute (with confirmation) | `skills/swap-execute/SKILL.md` | "execute swap", "broadcast swap", "send transaction" |
| Execute fast (no confirmation) | `skills/swap-execute-fast/SKILL.md` | "swap fast", "execute immediately" — use with extreme caution |
| Errors and troubleshooting | `skills/error-handling/SKILL.md` | API errors, token resolution failures, execution failures |

**Reference files** (read before calling APIs):

- `references/token-registry.md` — Token addresses and decimals per chain
- `references/api-reference.md` — OpenOcean API specification

All paths above are relative to the **workspace root** (the directory that contains this `SKILL.md`).

Path resolution rule (strict, to avoid noisy "file not found" errors):
1. **Always run glob discovery first**:
   - `**/token-registry.md`
   - `**/api-reference.md`
2. If a unique match is found, read that matched path directly.
3. Do not attempt to read hardcoded `references/...` paths before glob.
4. Only report an error if no match is found (or multiple ambiguous matches are found).

## Prerequisites

- **Quote / Build**: Only need GET request capability (e.g. `mcp_web_fetch`).
- **Execute**: Require [Foundry](https://getfoundry.sh/) (`cast`), RPC URL, and wallet (env, Ledger, Trezor, or keystore).

## Quick Examples

```
/quote 1 ETH to USDC on ethereum
/swap-build 100 USDC to ETH on arbitrum from 0xYourAddress
/swap-execute
```

For full workflows, confirmation prompts, and error handling, follow the corresponding `skills/*/SKILL.md` file.
