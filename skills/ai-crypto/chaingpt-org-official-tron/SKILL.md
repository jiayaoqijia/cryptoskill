---
name: tron
description: "Tron (TVM) support via the ChainGPT plugin — at parity with the EVM + Solana surfaces. Read balances/resources/tx, research (DexScreener), risk (GoPlus), build UNSIGNED native TRX + TRC-20 transfers (custody-free), SunSwap quotes, JustLend lending, and autonomous agent-wallet signing behind a deterministic policy gate. The agent's Tron account uses the SAME key as the EVM agent wallet. Triggers: tron, TRX, TRC-20, USDT on tron, sun swap, sunswap, justlend, tronscan, send TRX, tron balance, tron wallet."
---

# ChainGPT Tron Skill

You operate on **Tron**, a non-EVM chain (TVM). It is bytecode-compatible with the EVM but the account, address, fee, and transaction layers differ. Key facts:

- **Addresses** are base58 `T…` (34 chars). The same secp256k1 key controls both an ETH EOA and a Tron account; only the encoding differs (`0x41` + Base58Check). So the agent's Tron address is derived from its existing EVM agent wallet — there is no separate `_init`.
- **Units:** 1 TRX = 1,000,000 SUN (6 decimals). Contract calls burn **Energy** (capped by `fee_limit`); transactions burn **Bandwidth**. Sending to a never-activated address costs ~1.1 TRX.
- **No OpenOcean/1inch on Tron** — DEX routing uses **SunSwap**; lending uses **JustLend**.
- **Custody-free by default:** builders return an UNSIGNED tx (sign in TronLink or via the agent wallet). Mainnet builders require `acknowledgeMainnet: true`.

## Tools

| Tool | Purpose |
|---|---|
| `chaingpt_tron_validate_address` | Validate + show hex/EVM forms (offline) |
| `chaingpt_tron_balances` | TRX + resources + TRC-20 balances |
| `chaingpt_tron_token_balance` | One TRC-20 balance (resolves decimals on-chain) |
| `chaingpt_tron_account_resources` | Bandwidth + energy |
| `chaingpt_tron_tx_info` | Receipt by txid |
| `chaingpt_tron_research_token` | DexScreener price/liquidity/volume |
| `chaingpt_tron_risk_token` | GoPlus security scan |
| `chaingpt_tron_build_transfer_tx` | Unsigned native TRX transfer |
| `chaingpt_tron_build_trc20_transfer_tx` | Unsigned TRC-20 transfer |
| `chaingpt_tron_dex_sunswap_quote` | SunSwap swap quote (read) |
| `chaingpt_tron_lend_justlend_account` | JustLend liquidity + per-market balances |
| `chaingpt_tron_lend_justlend_build_tx` | Unsigned JustLend approve/supply/withdraw/borrow/repay |
| `chaingpt_agent_wallet_tron_address` | Agent's Tron address + TRX balance |
| `chaingpt_agent_wallet_tron_sign_and_send` | Build + sign + broadcast under the `tron` policy |

## Pipelines

**Send a token (custody-free):**
```text
chaingpt_tron_risk_token (optional gate) → chaingpt_tron_build_trc20_transfer_tx (acknowledgeMainnet:true) → sign in TronLink
```

**Autonomous send (agent wallet):**
```text
chaingpt_agent_wallet_tron_address (fund it) → chaingpt_agent_wallet_tron_sign_and_send { kind:"trc20_transfer", token:"USDT", to, amount, memo }
```
The deterministic `tron` policy gate enforces the destination allowlist, per-tx + rolling-24h SUN caps, the `fee_limit` cap, and a memo before signing. Tron signing requires `"tron": { "enabled": true }` in the policy (fail-closed for policy files that predate Tron). No MCP tool can relax the policy.

**Lend on JustLend:**
```text
chaingpt_tron_lend_justlend_account → build approve (TRC-20 markets) → build supply → sign
```

## Environment

- `TRON_PRO_API_KEY` — TronGrid key (mainnet keyless is throttled).
- `TRON_RPC_URL` — override the node host. Agent-wallet signing refuses a non-TronGrid host.

## Rules

- ALWAYS confirm an address with `chaingpt_tron_validate_address` if unsure — a bad checksum is rejected, but a valid-but-wrong address is not.
- NEVER use a poisoned address (USDDOLD, old SUN); the registry blocks them.
- Set a slippage-protected `minAmountOut` before executing any swap; SunSwap V2 quotes are indicative.
- TRC-20 supply/repay on JustLend need a prior `approve`.
