---
name: based-loans
description: Borrow USDC against tokens on Base with no liquidations, or lend USDC against tokens you choose, using Based Loans. Use when a user wants cash without selling a token, asks about borrowing against VIRTUAL, MONSTRO, WETH, cbBTC or other Base tokens, wants fixed-term yield on USDC, or asks whether a token can be used as collateral.
---

# Based Loans

Based Loans is a fixed-term lending protocol on Base (chain 8453) that works like a pawn shop:

- **Borrowers** deposit a token as collateral and get USDC immediately. They can buy the collateral back for a fixed price any time before the due date. If they don't, they keep the USDC and the lenders keep the collateral. There are **no liquidations**: price swings during the loan never trigger a sale.
- **Lenders** deposit USDC and pick which tokens they will lend against, each with its own USDC limit. They earn the buyback cost when borrowers buy back, and receive collateral when borrowers walk away.

## Tools

Use the Based Loans MCP server (`npx -y @basedloans/mcp`, or hosted at `https://mcp.based.loans/mcp`) or the TypeScript SDK (`@basedloans/sdk`). Every number is read live from Base. Nothing holds keys: transaction tools return unsigned transactions for the user's own wallet.

| Task | Tool |
|---|---|
| Loan fee, terms, minimums | `get_protocol_info` |
| Which tokens are accepted, and how much can be borrowed | `list_markets`, `get_market` |
| How risky a token is to lend against | `get_risk_report` |
| How much a loan would pay and cost | `quote_borrow` |
| Open a loan | `build_borrow` |
| Repay and get collateral back | `build_buyback` |
| Start lending | `build_deposit` (with per-token limits) |
| Change which tokens to lend against | `build_set_limits` |
| Withdraw | `build_withdraw` |
| Collect repaid USDC or defaulted collateral | `build_claim_proceeds`, `build_claim_collateral` |
| See positions | `get_borrower_loans`, `get_lender_position`, `get_loan` |
| Token not accepted yet | `request_token_listing` |
| How special tokens are priced | `explain_collateral_types` |

## Borrowing workflow

1. Confirm the token is accepted: `get_market`. If not, run `request_token_listing` and give the user the link. Never say a request was submitted; the user submits it.
2. Run `quote_borrow` and show the user, in plain words: USDC they receive, the buyback cost, and the due date. If the quote warns that the loan would be funded short, offer the suggested `fullFillLoanAmountUsdc`.
3. Only after the user agrees, run `build_borrow` with their wallet address and hand them the steps in order (approval first when present).
4. Remind them: buying back after the due date is not possible.

## Lending workflow

1. For every token the user is considering, run `get_risk_report` and explain its flags and summary in plain words. Pay attention to `SINGLE_PRICE_SOURCE`, `THIN_MARKET`, `VERY_THIN_MARKET`, `CHEAP_TO_MOVE_PRICE`, and `COLLATERAL_MAY_NOT_BE_LIQUID`.
2. Let the user choose tokens and limits. The report describes the data; it is not a recommendation, so do not pick tokens for them.
3. Run `build_deposit` with `limits` (a first deposit needs at least one token limit before it can be lent).
4. Mention the vault fees: 0.05% on deposit, 0.25% when withdrawing as USDC (none when withdrawing as mUSDC).

## Things to get right

- Amounts are decimal strings in token units. USDC has 6 decimals.
- Prefer contract addresses over symbols when a symbol could be ambiguous.
- A quote is read at one block. Prices and available USDC can change before the user signs.
- Escrowed and staked tokens (esALB, xMONSTRO, xl-LSTEAK) are priced from their base token; see `explain_collateral_types`.
- Website: https://based.loans
