---
name: openclaw_kraken
description: Use a Bash CLI to query Kraken Spot and Futures APIs, inspect account state, run guarded trading and funding actions, and work with Kraken websocket payloads using OpenClaw-managed secrets.
homepage: https://github.com/oscraters/kraken-skill.git
metadata: {"openclaw":{"homepage":"https://github.com/oscraters/kraken-skill.git","requires":{"bins":["bash","curl","openssl"],"env":["KRAKEN_API_BASE_URL"]},"primaryEnv":"KRAKEN_API_KEY"}}
---

# OpenClaw Kraken

Use `{baseDir}/bin/openclaw-kraken` for Kraken Spot REST tasks.

## Use when

- The user wants Kraken market data.
- The user wants Kraken account state from private REST endpoints.
- The user wants guarded order placement, funding, earn, futures, subaccount, or websocket actions through a local Bash tool instead of ad hoc curl commands.

## Rules

- Never print API secrets, signatures, or raw auth headers.
- Read secrets from the environment only. In OpenClaw, inject them via secret refs rather than plaintext config.
- Refuse to run if required config is missing or malformed.
- Use configured base URLs only. Do not accept arbitrary destination URLs.
- Preserve stdout for API results; use `--jq` or `--compact` when structured formatting is needed.
- Prefer read-only endpoints unless the user clearly asked for a state-changing action.
- For state-changing aliases such as trading, withdrawal, earn allocation, or subaccount transfer operations, require `--confirm`.

## Commands

- `market time`
- `market ticker --pair XBTUSD`
- `account balance`
- `funding deposit-methods --asset ETH`
- `earn strategies --ascending true`
- `futures call market.tickers`
- `ws spot-public --message-json '{"method":"ping"}'`
- `orders add --pair XBTUSD --side buy --type limit --volume 0.01 --price 25000 --time-in-force GTC --post-only true --confirm`
- `call funding.withdraw-info --asset ETH --key MyWallet --amount 0.5`

## Configuration

- Non-secret config is read from environment or `OPENCLAW_KRAKEN_CONFIG`.
- Secrets must be provided via environment variables that OpenClaw resolves from secret refs.
- See `{baseDir}/README.md` for examples.
