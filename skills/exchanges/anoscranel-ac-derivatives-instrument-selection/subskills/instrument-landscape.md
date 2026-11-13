---
name: instrument-landscape
domain: crypto-trading/instrument-landscape
trigger: "what instrument should I trade; spot vs perp; difference between options and futures"
anti_trigger: "how to calculate funding; how to compute liquidation price"
scope: Taxonomy of spot, perpetual, dated future, option, and structured product with one-line tests.
status: seedling
---

## Standard

Instrument selection begins with a precise understanding of financial primitives. In digital asset markets, participants choose among spot assets, perpetual futures, dated futures, options, and structured products. Each instrument serves a distinct economic function, carries unique structural risks, and imposes specific holding costs. Mismatching an instrument to a trading thesis leads to unexpected cash drains, margin exhaustion, or forced liquidation.

Spot holdings provide unencumbered ownership of the underlying asset with zero liquidation risk, though capital efficiency is constrained by 1x leverage. Perpetual futures eliminate expiration dates via periodic funding payments, enabling continuous directional exposure but introducing ongoing funding cash flow friction and liquidation susceptibility. Dated futures introduce a fixed maturity date, decoupling long-term holding costs from funding payments while exposing the position to basis convergence and roll risk. Options grant asymmetric payoffs with defined premium costs, offering precise tail-risk protection or leverage without linear downside, though subject to volatility surfaces and time decay. Structured products bundle these primitives into packaged yield or principal-protected notes, trading liquidity and counterparty transparency for customized payoff profiles.

Primary sources for the claims here: <https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html> and <https://www.isda.org/book/isda-deriv-tracker](https://www.isda.org/book/isda-deriv-tracker>.

## Decision rules

1. Choose spot when holding duration is indefinite and liquidation risk must be entirely avoided.
2. Choose perpetual futures for tactical, multi-day directional trades where continuous funding payments are acceptable.
3. Choose dated futures when holding periods align with a specific expiry date and funding rate volatility must be locked out.
4. Choose options when asymmetric payoff profiles or defined-risk downside protection are required, provided implied volatility is fairly priced.
5. Apply the one-line test for every candidate: spot requires full capital; perpetuals require continuous funding vigilance; dated futures require roll discipline; options require volatility edge over premium decay.

## Procedure

1. Inventory the trading hypothesis, including directional bias, expected holding duration, and acceptable drawdown limits.
2. Evaluate capital allocation constraints: determine whether margin efficiency or unencumbered asset ownership takes precedence.
3. Assess cash flow implications: verify whether ongoing funding payments (perpetuals) or premium decay (options) will erode profitability over the target horizon.
4. Test instrument availability against venue liquidity and custody requirements before committing capital.
5. Record the selected instrument classification and its primary justification in the trade plan.

## Anti-patterns

- Defaulting to perpetual futures for multi-month horizon trades without factoring cumulative funding costs.
- Treating options as directional leverage without accounting for theta decay and implied volatility surface shifts.
- Deploying spot capital when leverage and capital efficiency are mandatory for the strategy.
- Ignoring expiration mechanics when trading dated futures near delivery dates.

## Done checklist

- [ ] Trading thesis aligned with instrument payoff profile.
- [ ] Holding duration matched to instrument expiration or settlement mechanics.
- [ ] Capital efficiency and leverage constraints verified.
- [ ] Funding or premium carry costs calculated and accepted.
- [ ] Instrument classification recorded in trade plan.

## Sources

- ISDA Financial Instrument Taxonomy and Derivatives Documentation: [https://www.isda.org/book/isda-deriv-tracker](https://www.isda.org/book/isda-deriv-tracker)
- Derivatives Risk Management and Settlement Standards: [https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html)
- Tail-risk calibration and hedging friction in crypto option surfaces: [https://arxiv.org/abs/2611.00958](https://arxiv.org/abs/2611.00958)
