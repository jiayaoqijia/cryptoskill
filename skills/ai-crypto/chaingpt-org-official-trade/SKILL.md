---
name: trade
description: "Execute live DEX trades on MAINNET via the ChainGPT plugin. EVM swaps via OpenOcean (default, no key, 10 mainnets), 1inch v6 (key-gated, better blue-chip routing), or CoW Protocol (MEV-protected intent-based for large trades). Solana swaps via Jupiter. Custody-free — the plugin builds unsigned tx / EIP-712 intent, the user signs externally. Mandatory pre-flight: chaingpt_risk_token on the buy token + a quote tool before any build/create tool. Triggers: swap, trade, buy, sell, exchange, dex, jupiter, openocean, 1inch, cow, cowswap, mev protection, 0x, paraswap, slippage, swap on ethereum, swap on base, swap on solana."
---

# ChainGPT Trade Skill

You execute real mainnet DEX trades on behalf of the user. **The plugin never holds keys.** Your job is to:

1. Run the pre-flight checks the user expects from a serious trading interface.
2. Build the unsigned transaction.
3. Hand it to the user's wallet to sign.

## The mandatory pipeline (EVM)

```
chaingpt_research_token        — confirm the user is buying the token they think
chaingpt_risk_token            — GoPlus + Honeypot check on the OUT token (MANDATORY)
chaingpt_dex_quote             — expected output, price impact, route
       │  (surface to user with USD-denominated cost and slippage)
       ▼
chaingpt_dex_approve_tx        — if inToken is ERC-20 and current allowance is insufficient (requires acknowledgeMainnet: true — approvals delegate spend authority)
       │  (user signs + broadcasts the approval)
       ▼
chaingpt_dex_build_swap_tx     — REFUSES mainnet unless acknowledgeMainnet=true
       │  (user signs + broadcasts the swap)
       ▼
chaingpt_onchain_tx hash=…     — confirm execution, surface received-amount
```

Pipeline for Solana is identical but two-step (no approval needed):

```
chaingpt_risk_token (on Solana outToken)
chaingpt_dex_jupiter_quote
chaingpt_dex_jupiter_build_swap_tx (requires acknowledgeMainnet)
```

## Hard rules for mainnet

1. **NEVER call `chaingpt_dex_build_swap_tx` with `acknowledgeMainnet: true`** unless the user has explicitly confirmed they want to swap on mainnet *with the specific amounts and tokens you echoed back*.
2. **ALWAYS surface the price impact and USD cost** from `chaingpt_dex_quote` before asking for confirmation.
3. **If `chaingpt_risk_token` raises a honeypot or cannot-sell-all flag, REFUSE the swap.** Surface the flag and require an explicit user override before re-running.
4. **For >$1,000 trades, also call `chaingpt_audit_contract`** on the outToken's contract if it's a freshly-deployed or unverified contract. The audit gate is the ChainGPT-native moat.
5. **For ERC-20 swaps, always insert the approval step.** Skipping approval is the single most common cause of failed swaps.

## What the build-tx response looks like

`chaingpt_dex_build_swap_tx` returns:

```json
{
  "chainId": 8453,
  "to": "0x6352a56caadc4f1e25cd6c75970fa768a3304e64",  // OpenOcean router on Base
  "data": "0x90411a32…",
  "value": "0x0",         // non-zero for native-in swaps
  "gas": "0x4c4b40",
  "gasPrice": "0x4a817c800"
}
```

The user pastes this into MetaMask's "send transaction" / Rabby's import-tx feature, or programmatically calls `wallet.sendTransaction(tx)` if they have a script.

## Network coverage

EVM: ethereum, base, arbitrum, optimism, polygon, bsc, avalanche, blast, linea, scroll.
Solana: mainnet only.

## What this skill does NOT do

- It does not custody funds. The plugin never sees the private key.
- It does not execute the trade autonomously. The user must sign in their wallet.
- It does not retry failed trades. If the swap reverts, the user is told what happened; the next attempt is a new call.

## Alternative aggregators (when OpenOcean isn't the right tool)

OpenOcean is the default because it's keyless and covers all 10 EVM chains. Two alternatives are wired in for specific use cases:

### 1inch v6 (`chaingpt_dex_1inch_quote` / `chaingpt_dex_1inch_swap_tx`)

- **When to use:** Better routing on Ethereum + L2s for large blue-chip pairs (USDC↔WETH, etc.) and when OpenOcean returns a worse quote.
- **Setup:** Requires `ONEINCH_API_KEY` (free tier at https://1inch.dev → Developer Portal). Without the key, the tool returns a setup hint and falls back to OpenOcean.
- **Networks:** ethereum, base, arbitrum, optimism, polygon, bsc, avalanche.
- **Approval target:** 1inch v6 router (returned in the quote response — use it as the `spender` for `chaingpt_dex_approve_tx`, with `acknowledgeMainnet: true`).

### CoW Protocol (`chaingpt_dex_cow_create_order` / `chaingpt_dex_cow_submit_signed_order`)

- **When to use:** Trades >$50k where MEV sandwich attacks would eat a meaningful slice of the trade. CoW uses an intent-based model — solvers compete to fill the order at the best price, and the executor pays gas.
- **Different signing flow:** The user signs an **EIP-712 order intent** (not a transaction). Then `chaingpt_dex_cow_submit_signed_order` POSTs it to the CoW API and returns an order UID trackable on https://explorer.cow.fi.
- **Approval target:** CoW **Vault Relayer** `0xC92E8bdf79f0507f65a392b0ab4667716BFE0110` (NOT the Settlement contract). One-time approval per token.
- **Networks:** ethereum, base, arbitrum_one. (No native ETH — wrap to WETH first.)
- **Hard rule:** Still gated on `acknowledgeMainnet=true`. Once signed and submitted, solvers WILL execute the order — there's no client-side broadcast step to cancel at.

## Credit accounting

Trading itself burns 0 ChainGPT credits — OpenOcean and Jupiter are free. The pre-flight `chaingpt_risk_token` is also free (GoPlus). The optional `chaingpt_audit_contract` step burns 1 credit. The credit funnel for this skill comes from upstream calls (research / news / signals) the user makes before deciding to trade.
