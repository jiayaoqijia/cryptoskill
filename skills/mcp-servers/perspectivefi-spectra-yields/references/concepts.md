# Spectra concepts and edge cases

| Term | Meaning |
| --- | --- |
| IBT | Interest-bearing token being tokenized (an ERC-4626 vault share: lending deposit, LST, savings token). |
| Underlying | Asset the IBT is denominated in (USDC, WETH, FXRP…). PTs redeem for it at maturity. |
| PT | Principal Token. Trades below 1 underlying before maturity; redeemable 1:1 at maturity unless the yield source had negative yield. |
| YT | Yield Token. Receives all IBT yield until maturity, then worth zero. Spectra keeps 3% of YT yield (including points). |
| Fixed APY (`fixed_apy_pct`) | Rate locked by buying PT now and holding to maturity. Headline value is for a small trade; quote for size. |
| Implied APY | Rate the market prices into PT. |
| Variable APY | Current yield of the IBT. |
| LP APY | Variable: swap fees + PT accretion + IBT yield + incentives (see `lp_apy_breakdown`). |
| YT leverage | Yield exposure per unit of capital when buying YT. |
| Maturity | Date PT becomes redeemable and YT stops accruing. |
| MetaVault | Curated vault. Live APY and 30-day average are both variable. Withdrawals can wait for the next settlement. |

## Edge cases

- **Matured markets** (`expired`): do not suggest buying. PT holders should redeem; LPs should exit.
- **Negative fixed APY**: PT trades above par; buying locks a loss. Flagged `negative_fixed_apy`.
- **Thin pools**: the quote's fixed APY can be far below the headline; mention price impact.
- **Stellar markets**: order-book based (no AMM pool). Data and links work; transaction building is EVM-only.
- **Missing USD price** (`missing_usd_price`): TVL in USD is unknown; do not rank by TVL.
- **Exit-only markets** (`exit_only`): users can only leave.

Docs: https://docs.spectra.finance (llms.txt: https://docs.spectra.finance/llms.txt)
