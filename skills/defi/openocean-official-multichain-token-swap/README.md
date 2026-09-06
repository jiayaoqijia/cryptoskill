# OpenOcean Skills

Skills for interacting with the [OpenOcean Aggregator API](https://apis.openocean.finance/). Use them to fetch swap quotes and build transaction calldata across 40+ chains, including both EVM and non-EVM networks such as Solana and Sui. They can be used by any AI coding assistant or agent that supports skill- or plugin-style instructions, such as Cursor, Claude Code, or custom runners.

## Prerequisites & Availability

- **Reference files**: Skills read `references/token-registry.md` and `references/api-reference.md` from the workspace root. Ensure these files are present.
- **Quote / Build**: `quote` and `swap-build` only require the ability to send GET requests, such as `mcp_web_fetch` or `curl`; no local installation is needed.
- **Execute**: `swap-execute` and `swap-execute-fast` require [Foundry](https://getfoundry.sh/) (`cast`) plus RPC and wallet configuration.

If something goes wrong, check: 1) Correct workspace with `references/`; 2) API requests use integer-string `amountDecimals` (no decimal point); 3) User-facing `slippage 100` means 100 bps = 1%, while the API parameter uses percent (`1` = 1%); 4) Foundry is installed and `ETH_RPC_URL` plus any required wallet settings are configured for on-chain execution.

## Project Structure

Skills live under `skills/`, while shared API docs and token data live under `references/`.

```
openocean-skills/
├── skills/
│   ├── quote/              # Get a swap quote
│   │   └── SKILL.md
│   ├── swap-build/         # Build swap calldata (with confirmation)
│   │   └── SKILL.md
│   ├── swap-execute/       # Execute a swap via Foundry cast (with confirmation)
│   │   └── SKILL.md
│   ├── swap-execute-fast/  # Build and execute in one step (no confirmation)
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── fast-swap.sh      # Token resolution and route building
│   │       └── execute-swap.sh   # Calls fast-swap.sh and then broadcasts
│   └── error-handling/     # Troubleshooting and error codes
│       └── SKILL.md
├── references/             # Shared docs
│   ├── api-reference.md
│   └── token-registry.md
├── test/                   # Prompt test cases
│   └── agent-test-cases.md # English test prompts
└── README.md
```

## Installation

This repo works with Cursor, Claude Code, OpenClaw, and other mainstream tools.

Download the repo, either as a ZIP archive or via `git clone`, and place it in your tool's skills directory.

After extraction, make sure the project root still contains the `references/` folder, since the skills read `token-registry.md` and `api-reference.md` from there.

## Skills Overview

### quote

Get the best swap route and price for a token pair.

```
/quote 1 ETH to USDC on ethereum
/quote 100 USDC to WBTC on arbitrum
/quote 0.5 WBTC to DAI on polygon
```

Returns: expected output amount, USD value, exchange rate, estimated gas, and route path (DEXes used).

### swap-build

Build a full swap transaction, including the route and encoded calldata. Requires a sender address. Shows quote details such as rate, minimum output, and gas, then asks for confirmation before building.

```
/swap-build 100 USDC to ETH on arbitrum from 0xYourAddress
/swap-build 1 ETH to USDC on ethereum from 0xYourAddress slippage 100
```

Returns: encoded calldata, router address, transaction value, gas estimate, minimum output after slippage. **Does not** submit on-chain.

### swap-execute

Execute a previously built swap on-chain using Foundry's `cast send`. Consumes `swap-build` output and broadcasts it.

```
/swap-execute
```

Requires Foundry (`cast`). Supports multiple wallet options, including environment variables, Ledger, Trezor, or a keystore. Asks for confirmation before execution because the transaction is irreversible.

### swap-execute-fast

Build and execute a swap in one step, with no confirmation prompt.

```
/swap-execute-fast 1 ETH to USDC on base from 0xYourAddress
/swap-execute-fast 100 USDC to ETH on arbitrum from 0xYourAddress keystore mykey
/swap-execute-fast 0.5 WBTC to DAI on polygon from 0xYourAddress ledger
```

Requires `cast`, `curl`, and `jq`. **Extremely dangerous**: builds and executes immediately with no confirmation. Use only when you fully trust the parameters and understand the risks.
