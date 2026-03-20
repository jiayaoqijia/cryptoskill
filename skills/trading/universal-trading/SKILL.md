---
name: universal-trading
description: Execute cross-chain token trading on EVM and Solana with Particle Network Universal Account SDK. Use when users ask to set up universal-account-example, buy or sell tokens, run convert/swap flows, transfer assets, call custom transactions, query balances/history, or monitor transaction status via WebSocket.
metadata: {"openclaw":{"os":["darwin","linux"],"requires":{"bins":["node","npm"]},"install":[{"id":"brew-node","label":"Install Node.js and npm (Homebrew)","kind":"brew","formula":"node","bins":["node","npm"]}]}}
---

# Universal Trading

Execute cross-chain trades with the official Particle Network `universal-account-example` project.

## First-Use Auto Initialization (Default)

When users install this skill and start using it for the first time, auto-run initialization by default.

Use this decision flow:

1. If `universal-account-example/.env` already exists, treat environment as initialized and continue to trading tasks.
2. If not initialized, run from any directory:

```bash
bash {baseDir}/scripts/init.sh new
```

3. If user explicitly wants to import an existing wallet, run:

```bash
bash {baseDir}/scripts/init.sh import <YOUR_PRIVATE_KEY>
```

After initialization, explicitly tell users:
- private key is stored at `universal-account-example/.env` under `PRIVATE_KEY`
- they can use this wallet in the UniversalX frontend:
  `https://universalx.app` -> `创建钱包` -> `导入现有钱包`

By default, setup auto-binds invite code `666666` after `.env` is created.
It also patches `examples/buy-evm.ts` to remove `usePrimaryTokens` restriction.

Optional flags:

```bash
# Use existing repo path
bash {baseDir}/scripts/init.sh new --target /path/to/universal-account-example

# Skip smoke test
bash {baseDir}/scripts/init.sh new --skip-smoke

# Disable invite auto-bind
DISABLE_AUTO_INVITE_BIND=1 bash {baseDir}/scripts/init.sh new
```

## Available Operations

Use scripts inside `universal-account-example/examples`:

- Buy token: `buy-solana.ts`, `buy-evm.ts`
- Sell token: `sell-solana.ts`, `sell-evm.ts`
- Convert (swap): `convert-solana.ts`, `convert-evm.ts`, `7702-convert-evm.ts`
- Transfer: `transfer-solana.ts`, `transfer-evm.ts`
- Custom transaction calls: `custom-transaction-*`
- Balance and history: `get-primary-asset.ts`, `get-transactions.ts`
- Real-time monitoring: `transaction-status-wss.ts`, `user-assets-wss.ts`

For buy operations that need explicit slippage control, use:
- `scripts/buy-with-slippage.sh` (fixed slippage or dynamic retry)

## Trade Status Follow-Up (Required)

After any `sendTransaction`, do not stop at "transaction submitted".
Always return final outcome to user:

1. Capture and show `transactionId`.
2. Poll status until success or failure:

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/check-transaction.sh <TRANSACTION_ID> --max-attempts 30 --interval-sec 2
```

3. Reply with one of:
- `SUCCESS` (confirmed)
- `FAILED` (failed on-chain/executor)
- `PENDING` (not finalized before timeout, include explorer link)

## Trade Configuration

| Option | Description | Example |
|--------|-------------|---------|
| `slippageBps` | Slippage tolerance (100 = 1%) | `100` |
| `universalGas` | Use PARTI token for gas | `true` |
| `usePrimaryTokens` | Restrict source/fee primary tokens. Default: do not set (auto select). | `[SUPPORTED_TOKEN_TYPE.USDT, SUPPORTED_TOKEN_TYPE.USDC]` |
| `solanaMEVTipAmount` | Jito tip for MEV protection (SOL) | `0.01` |

## Slippage Controls (Required for Volatile Tokens)

Allow users to choose one of these modes before buy:

1. Fixed slippage only:
```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300
```

2. Dynamic slippage + auto retry:
```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200
```

3. Solana custom tip (anti-MEV) + retry tips:
```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain solana \
  --token-address 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200 \
  --solana-mev-tip-amount 0.001 \
  --retry-mev-tips 0.001,0.003,0.005
```

Reply with:
- chosen slippage mode and values
- chosen Solana tip settings (if Solana)
- final status (`SUCCESS` / `FAILED` / `PENDING`)
- `transactionId` and explorer URL when available

## Supported Chains

- Solana: `CHAIN_ID.SOLANA_MAINNET`
- EVM: `CHAIN_ID.POLYGON`, `CHAIN_ID.ARBITRUM`, `CHAIN_ID.OPTIMISM`, `CHAIN_ID.BSC`, `CHAIN_ID.ETHEREUM`

## Common Token Addresses

- SOL (native): `0x0000000000000000000000000000000000000000`
- USDC (Solana): `EPjFWdd5AufqSSFqM7BcEHw3BXmQ9Ce3pq27dUGL7C24`
- USDT (Solana): `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`

## Safety Checklist

1. Validate chain, token address, and amount before creating transactions.
2. Use small size for first live trade.
3. Wrap `sendTransaction` in try-catch and log `transactionId`.
4. Prefer your own Particle credentials for production workloads.

## Reference Files

- [Environment Setup](references/env-setup.md)
- [API Reference](references/api.md)
- [Examples](references/examples.md)
