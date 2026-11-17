# Lending on Based Loans

## How lending works

- A lender deposits USDC (minimum 200 USDC) and sets a USDC limit for each token they are willing to lend against (50 to 1,000,000 USDC per token, up to 50 tokens).
- New loans are funded from a queue of lenders who chose that token. One loan can be split across up to 25 lenders.
- When a borrower buys back, the lender gets their share of the buyback cost: principal plus 2.5%, 5% or 7.5% depending on the term. Claim it with `build_claim_proceeds`, either to the wallet or straight back into lending (`mode: "redeploy"`). `build_set_auto_redeploy` turns automatic re-lending on or off.
- When a borrower defaults, the lender receives their share of the collateral instead. Claim it with `build_claim_collateral`. Its value may be more or less than the USDC lent.

## Fees

The lending vault charges 0.05% on deposits and 0.25% when withdrawing as USDC. Withdrawing as mUSDC vault shares (`as_musdc: true`) has no withdrawal fee.

## Reading a risk report

`get_risk_report` returns data, not advice. Explain the summary and each flag in plain words, then let the user decide.

| Flag | What it means for a lender |
|---|---|
| `SINGLE_PRICE_SOURCE` | Only one price source; there is no second source to catch a bad price. |
| `THIN_MARKET` / `VERY_THIN_MARKET` | Little trading depth. Collateral received after a default may be hard to sell near the quoted price. |
| `CHEAP_TO_MOVE_PRICE` | A relatively small trade moves the pool price a lot. The report shows the USDC needed to move it 2x and 10x. |
| `COLLATERAL_MAY_NOT_BE_LIQUID` | The token may need vesting, unstaking or redeeming before it can be sold. |

Other fields worth showing: the number of price sources and whether they agree, how far back pool price history goes, USDC available against the token, and its active loan cap.

## Managing a position

- `get_lender_position`: deposit, USDC in active loans, USDC available to withdraw, per-token limits, and claimable proceeds or collateral, with loan IDs.
- `build_set_limits`: add, change or remove token limits. A limit of 0 removes the token, once nothing is in active loans against it.
- `build_withdraw`: withdraw USDC not in active loans (`"max"` for all of it). USDC in active loans comes back as borrowers buy back.
