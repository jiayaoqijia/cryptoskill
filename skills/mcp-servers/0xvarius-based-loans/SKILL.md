---
name: based-loans
description: Borrow USDC against crypto tokens on Base with no liquidations, or lend USDC for fixed-term returns, using Based Loans. Quotes, token risk checks, loan and lender positions, and ready-to-sign transactions for borrowing, partial or full buybacks, lending, withdrawals and claims. Use when a user wants USDC without selling a token, asks about collateral-backed or fixed-term crypto loans on Base, asks whether a token (WETH, cbBTC, VIRTUAL, AERO and others) can be borrowed against, wants to check or repay a Based Loans loan, or wants to earn on USDC by lending against tokens they choose.
license: MIT
compatibility: Needs network access to the Based Loans MCP server (https://mcp.based.loans/mcp) or HTTP API (https://mcp.based.loans/v1). Transactions are signed by the user's own Base wallet.
metadata:
  website: https://based.loans
  docs: https://docs.based.loans/ai-agents
  source: https://github.com/0xVarius/basedloans-agents
---

# Based Loans

Based Loans is a fixed-term lending protocol on **Base mainnet** (chain ID 8453) that works like a pawn shop:

- **Borrowers** deposit a token as collateral and receive USDC right away. They can buy the collateral back at a fixed price any time before the due date. If they don't, they keep the USDC and the lenders receive the collateral. There are **no liquidations**: price moves during the loan never sell the collateral early, and there are no margin calls.
- **Lenders** deposit USDC and choose which tokens they lend against, each with its own USDC limit. They never fund loans against tokens they did not choose.

## Terms at a glance

Values as of November 2026. **Always read the live values with `get_protocol_info` before quoting them to a user**; they can change.

| | Value |
|---|---|
| Network | Base mainnet only |
| Max loan-to-value | 50% of the collateral's value on every current market |
| Loan fee | 2.49%, taken out of the loan amount (borrow 100, receive 97.51) |
| Terms | short 15 days, medium 30 days, long 45 days |
| Buyback cost | loan amount + 2.5% (short), 5% (medium) or 7.5% (long), fixed when the loan opens |
| Minimum loan | 50 USDC |
| Minimum partial buyback | 1 USDC |
| Minimum lender deposit | 200 USDC |
| Per-token lending limit | 50 to 1,000,000 USDC |

**If the borrower does not buy back by the due date (default):** the borrower keeps the USDC, cannot buy back any more, and the lenders who funded the loan claim the collateral, split by how much each one funded. Nothing else is owed. Price moves never trigger anything during the loan.

## How to connect

Prefer the MCP server. It exposes every tool named below and never holds keys.

- Hosted (no install): `https://mcp.based.loans/mcp` (Streamable HTTP, no login)
- Local: `npx -y @basedloans/mcp`
- No MCP support: use the HTTP API at `https://mcp.based.loans/v1`, mapped in [references/http-api.md](references/http-api.md)

## Read-only vs. transactions

**Read-only (safe to run any time, nothing is signed):**

| Task | Tool |
|---|---|
| Fees, terms, minimums, contract addresses, paused state | `get_protocol_info` |
| Accepted collateral, price, max LTV, USDC available | `list_markets` (`only_with_funds: true` for markets lenders are backing), `get_market` |
| Exact loan quote | `quote_borrow` |
| A token's risk data | `get_risk_report` |
| Loans and positions | `get_borrower_loans`, `get_lender_position`, `get_loan` |
| How special tokens are priced | `explain_collateral_types` |
| Token not accepted yet | `request_token_listing` (returns a link; the user submits it) |
| Dry-run a prepared transaction | `simulate_transaction` |

**Transactions (the user's wallet must approve each one):** `build_borrow`, `build_buyback`, `build_deposit`, `build_set_limits`, `build_withdraw`, `build_claim_proceeds`, `build_claim_collateral`, `build_set_auto_redeploy`.

These tools **do not send anything**. They return unsigned transactions in order (an approval first, only when needed). The user signs and sends each step with their own wallet. Never ask for a seed phrase or private key, and never accept one if offered: tell the user to keep it private. If the agent itself controls a wallet, confirm the exact amounts with the user before sending.

## Borrowing

1. **Check the token.** `get_market` (or `list_markets`). If it is not accepted, run `request_token_listing` and give the user the link. Never claim a request was submitted.
2. **Quote.** `quote_borrow` with the token, collateral amount and term. Show in plain words: USDC received, buyback cost, due date and collateral used. Only the collateral the loan needs is taken.
3. **Handle short funding.** If the quote warns that lenders can only fund part of it, offer the suggested `fullFillLoanAmountUsdc`. If `wouldFail` is set, explain why and don't build the loan.
4. **Confirm, then build.** After the user agrees, run `build_borrow` with their wallet address. Hand over the steps in order.
5. **Remind them:** buy back before the due date or the collateral goes to the lenders. Buying back after the due date is not possible.

Details and edge cases: [references/borrowing.md](references/borrowing.md).

## Buying back (full or partial)

1. `get_borrower_loans` (or `get_loan`) to find the loan, its remaining buyback amount and due date.
2. `build_buyback` with the loan ID. Omit `payment_usdc` to pay in full and get all the collateral back. A partial payment (at least 1 USDC) returns a proportional share of the collateral, and the rest stays in the loan until the due date.

## Lending

1. **Check risk for every token** the user is considering with `get_risk_report`. Explain the summary and each flag in plain words. Pay special attention to `SINGLE_PRICE_SOURCE`, `THIN_MARKET`, `VERY_THIN_MARKET`, `CHEAP_TO_MOVE_PRICE` and `COLLATERAL_MAY_NOT_BE_LIQUID`. See [references/lending.md](references/lending.md).
2. **Let the user choose** tokens and limits. The report describes data; it is not a recommendation, so don't pick tokens for them.
3. **Deposit** with `build_deposit` and `limits`. A first deposit needs at least one token limit before it can be lent.
4. **Manage:** `get_lender_position` to see deposits, USDC in active loans and anything ready to claim. Use `build_set_limits` to change tokens, `build_claim_proceeds` for repaid USDC (or `mode: "redeploy"` to re-lend it), `build_claim_collateral` after a default, and `build_withdraw` for USDC not in active loans.

## Things to get right

- Amounts are decimal strings in token units (`"0.5"` WETH, `"500"` USDC).
- Prefer contract addresses over symbols when a symbol could be ambiguous.
- A quote is read at one block. Prices and available USDC can change before the user signs, so re-quote if time has passed.
- Staked and escrowed tokens (for example xl-LSTEAK, esALB) are priced from their base token. See [references/collateral-types.md](references/collateral-types.md).
- If `get_protocol_info` shows `paused: true`, tell the user nothing can be opened or repaid until it is unpaused.
- Website: https://based.loans. Docs: https://docs.based.loans
