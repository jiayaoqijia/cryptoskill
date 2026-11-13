---
name: ac-derivatives-instrument-selection
description: Select derivative and spot instruments by payoff structure, funding and expiry risk, margin mechanics, and liquidity depth. Use when asking "which instrument", "perp or future", "should I use options", "hedge with options", "dated future vs perpetual". Not for funding arithmetic (ac-funding-and-basis), not for liquidation geometry (ac-liquidation-risk-management), not for venue evaluation (ac-perp-venue-diligence).
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Derivatives Instrument Selection

Selecting the correct crypto market instrument requires aligning the trading thesis, holding horizon, and risk tolerance with the specific mechanical profile of spot assets, perpetual futures, dated futures, options, or structured products. Instrument choice is not merely a preference for directional leverage; it is a structural decision governed by funding cash flows, expiry convergence, margin modes, and market liquidity depth across centralized and decentralized exchanges.

## Overview and Purpose

Market participants frequently default to perpetual futures without assessing whether continuous funding rates, liquidation mechanics, or order book depth match their operational horizon. This skill provides a rigorous, standardized framework for evaluating instrument trade-offs across six core operational dimensions: payoff geometry, funding versus roll risk, option convexity and premium friction, horizon matching, collateral fit, and execution liquidity. By formalizing instrument selection into a structured decision process, traders eliminate unhedged carry liabilities, prevent margin contagion, and avoid execution friction in fragmented order books. Furthermore, establishing rigorous selection criteria ensures that capital is deployed into the exact instrument primitive that maximizes risk-adjusted return without introducing unintended structural liabilities or unmonitored cash drain risks. Operating across digital asset markets demands continuous verification of instrument appropriateness against evolving market volatility and liquidity regimes. Effective risk management depends upon selecting primitives that match both strategic intent and venue mechanics across all trading cycles. Moreover, maintaining clear operational guardrails ensures structural alignment between execution venues and portfolio risk limits.

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/instrument-landscape.md` | `crypto-trading/instrument-landscape` | Taxonomy of spot, perpetual, dated future, option, and structured product with one-line tests. |
| `subskills/perp-versus-dated.md` | `crypto-trading/perp-versus-dated` | Funding risk versus expiry/roll risk, basis convergence, and instrument selection trade-offs. |
| `subskills/options-as-hedges.md` | `crypto-trading/options-as-hedges` | Convexity, premium cost as insurance friction, and buying versus selling protection. |
| `subskills/horizon-matching.md` | `crypto-trading/horizon-matching` | Aligning holding periods with instrument settlement profiles and avoiding horizon mismatch failure modes. |
| `subskills/collateral-and-margin-fit.md` | `crypto-trading/collateral-and-margin-fit` | Collateral types, margin modes (cross vs isolated), and leverage constraints across instruments. |
| `subskills/liquidity-and-execution-fit.md` | `crypto-trading/liquidity-and-execution-fit` | Order book depth, turnover ratios, depth-to-turnover test, and execution friction elimination. |
| `subskills/selection-record.md` | `crypto-trading/selection-record` | Documenting instrument selection criteria, weights, rejections, review triggers, and decision artifact rules. |

## External References and Industry Standards

- Financial instrument taxonomy and derivatives clearing frameworks: [https://www.isda.org/book/isda-deriv-tracker](https://www.isda.org/book/isda-deriv-tracker)
- Derivatives risk management and margin methodologies: [https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html)
- Tail-risk calibration and hedging friction in crypto option surfaces: [https://arxiv.org/abs/2611.00958](https://arxiv.org/abs/2611.00958)
- Regulatory standards for derivatives market integrity: [https://www.iosco.org/library/pubdocs/pdf/IOSCOPD603.pdf](https://www.iosco.org/library/pubdocs/pdf/IOSCOPD603.pdf)
- CFTC educational resources on futures and options markets: [https://www.cftc.gov/LearnAndProtect/EducationCenter/index.htm](https://www.cftc.gov/LearnAndProtect/EducationCenter/index.htm)
