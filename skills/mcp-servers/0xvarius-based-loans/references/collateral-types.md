# How Based Loans prices collateral

Every loan is sized from the token's price at the moment the loan opens. The price is the lowest of the token's working price sources, and the loan is a share of that value (the max loan-to-value, usually 50%). Price sources are time-weighted averages from DEX pools (usually over 30 minutes) and, for some tokens, DIA price data. Tokens with two or more sources only open loans when the sources agree within a set range.

There are four kinds of collateral. The SDK and MCP server (get_market, get_risk_report) return which kind a token is as pricingType.

## 1. Regular tokens (market)
Priced straight from a DEX pool against USDC or WETH, sometimes with DIA as a second check.
Examples: WETH, cbBTC, cbETH, VIRTUAL, AERO.
What to know: the deeper the pool, the harder the price is to move. Tokens with only one pool and no second source have nothing double-checking their price.

## 2. Two-hop tokens (market_two_hop)
The token's main pool is against another token, so the price goes through that token first. For example MONSTRO trades against ALB, so MONSTRO is priced as MONSTRO in ALB, then ALB in WETH.
Examples: MONSTRO, PLAZM, DUB.
What to know: the price depends on both pools. A thin second pool matters as much as a thin first one. get_risk_report measures both.

## 3. Staked and share tokens (derived_live_ratio)
Tokens that represent a claim on another token, like a staked or liquid-staking token or a vault share. Priced as the base token's price times the exchange rate the token's own contract reports, read live.
Examples: xMONSTRO (priced from MONSTRO times its redemption rate), xl-LSTEAK (priced from LSTEAK times its exchange rate).
What to know: the risk is mostly the base token's risk, plus trust in the contract reporting the rate. If a lender ends up holding one, they may need to redeem it through its own contract, which can have fees or delays, before they have the base token.

## 4. Escrowed and locked tokens (derived_fixed_ratio)
Tokens that convert into a liquid token over time, like escrowed rewards that vest. Priced as the liquid token's price times a fixed discount set by governance.
Example: esALB is priced at 85% of ALB, because it has to vest before it becomes ALB.
What to know: the discount does not move with the market. If the real discount widens, the protocol's price stays the same until governance updates it. A lender who ends up holding an escrowed token may have to wait for it to vest before they can sell it.

## For borrowers
You never get liquidated. Whatever the token does during the loan, you can buy your collateral back for the fixed buyback cost before the due date, or walk away and keep the USDC.

## For lenders
You only lend against tokens you pick, up to the limits you set. If a borrower walks away, you receive your share of their collateral. Before adding a token, check get_risk_report: how many price sources it has, how deep its pools are, and what kind of collateral it is.
