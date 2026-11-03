---
name: spectra-transactions
description: Safely prepare Spectra transactions (buy a Principal Token to lock a fixed rate, sell PT before maturity, redeem matured PT) as unsigned transactions for the user to sign in their own wallet. Use when the user wants to act on a Spectra market, not just read data.
---

# Spectra transactions

You never sign or broadcast. You prepare unsigned transactions, explain them, and the user signs in their wallet.

## Tools

- `spectra_prepare_pt_trade` (`side`: `buy` | `sell`; `amount` in token units; `token`: `underlying` | `ibt` | address; `slippage_pct`, default 0.5; `receiver`; optional `sender`).
- `spectra_prepare_redeem` for PTs past maturity.
- Both are on the Spectra MCP server's trade endpoint, `https://mcp.spectra.finance/mcp/trade`. If they are not available, send the user to the market's app link instead; never build calldata by hand.

## Required flow

1. **Identify the market** with `spectra_find_yields` / `spectra_get_market`. Confirm network, PT symbol, maturity and flags with the user. Do not proceed on `apy_outlier`, `expired` (for buys) or `exit_only` markets.
2. **Quote first** (no `receiver`). Show: amount in, expected and minimum out, fixed APY for this size, maturity, fee, warnings.
3. **Get explicit confirmation** of amount, market, slippage and the receiving wallet.
4. **Prepare** with `receiver` (and `sender` if the signer differs). Present transactions in order:
   - step 1 (if present): ERC-20 `approve` of exactly the amount to the Spectra router;
   - step 2: the router call.
   Show `chain_id`, `to`, and that `value` is 0. The router is checked against pinned Spectra routers by the tool.
5. The user signs each step in order. If more than a couple of minutes pass, quote again: prices move.

## Guardrails

- Never ask for or accept a private key or seed phrase.
- Keep the default slippage (0.5%) unless the user asks; explain the trade-off if they raise it.
- If the tool refuses (sanity check failed, unknown router, preview error), stop and send the user to the app link it returns. Do not retry with a hand-built transaction.
- Approvals are for the exact amount; do not suggest unlimited approvals.
- Selling before maturity realises the market price; the fixed rate only holds to maturity.
- Tokenized-equity markets are not available to persons in US, UK, Canada, Australia, Singapore.
- Stellar markets: send the user to the app (no transaction building).
