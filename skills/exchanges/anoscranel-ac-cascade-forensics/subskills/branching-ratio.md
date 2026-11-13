---
name: branching-ratio
domain: crypto-trading/branching-ratio
trigger: "Measuring the branching ratio lambda from a cascade's fills; the subcritical reading (lambda 0.1-0.2, measured in flight, Oct 2025); what subcriticality forbids."
anti_trigger: "Assuming self-sustaining explosive avalanches (subskills/proxies-and-tape.md); forecasting future price paths from historical branching ratios."
scope: "Measuring the branching ratio lambda from a cascade's fills; the subcritical reading; what subcriticality forbids."
status: seedling
---

# Branching Ratio

## Standard

- **Sornette, D. (2004)**: *Why Stock Markets Crash: Critical Events in Complex Financial Systems*. Princeton University Press. Defines self-exciting point processes and branching ratio estimation. <https://press.princeton.edu/books/paperback/9780691118508/why-stock-markets-crash>
- **Hardiman, S. J., Bercot, N., & Bouchaud, J.-P. (2013)**: Critical reflexivity in financial markets: a Hawkes process analysis. *Physical Review E*, 88(2), 022814. Details empirical measurements of branching ratios in financial order flows. <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.88.022814>
- **arXiv:2608.03616**: Quantitative measurement of liquidation cascades and branching ratios in crypto perpetual futures during extreme volatility events (measured lambda hat 0.1–0.2 in flight, Oct 2025 case). <https://arxiv.org/abs/2608.03616>

## Decision rules

- **Rule 1 (Subcritical regime)**: The measured branching ratio lambda hat must fall strictly below 1.0 (typically 0.1–0.2 in crypto liquidation clusters), confirming a subcritical system.
- **Rule 2 (No explosive avalanches)**: Subcriticality forbids any model of self-sustaining, infinite cascade avalanches; every cluster eventually dampens out.
- **Rule 3 (Estimation window)**: Branching ratios must be calculated over rolling temporal bins (e.g., 1-second intervals) to capture burst dynamics without smoothing out micro-shocks.
- **Rule 4 (Descriptive only)**: Measured branching ratios describe past cascade dampening rates; they must never be used to forecast future market crashes or price bottoms.

## Procedure

1. Take the validated fill-log timeline from fill-log analysis and bin execution sizes into fixed time intervals (delta t = 1 second).
2. Fit a Hawkes process or branching-process estimator to the point process of liquidation arrivals to compute the expected offspring number (branching ratio lambda hat).
3. Verify that the estimated lambda hat remains significantly below unity (confirming the empirical 0.1–0.2 subcritical range).
4. Plot the cluster size distribution against theoretical subcritical branching curves to test goodness-of-fit.
5. Document the damping coefficient and recovery half-life for the liquidation cluster.
6. Verify that no predictive claims are derived from the subcritical measurement.

## Anti-patterns

- Assuming that a large liquidation cluster implies a critical branching ratio (lambda hat >= 1.0).
- Building automated trading bots that treat branching ratios as directional entry signals.
- Ignoring binning sensitivity when estimating Hawkes process parameters over sparse transaction data.
- Concluding that market makers caused a cascade simply because the branching ratio was measured.

## Done checklist

- [ ] Fill events binned into consistent temporal intervals.
- [ ] Branching ratio lambda hat estimated via point-process methods.
- [ ] Subcritical regime (lambda hat < 1.0) confirmed and documented.
- [ ] Cluster size distribution compared against theoretical curves.
- [ ] Predictive statements strictly excluded from the analysis output.
- [ ] Word count (450-650) and URL counts verified.

## Sources

- Sornette, D. (2004). *Why Stock Markets Crash*. Princeton University Press. <https://press.princeton.edu/books/paperback/9780691118508/why-stock-markets-crash>
- Hardiman, S. J., et al. (2013). Critical reflexivity in financial markets. *Physical Review E*, 88(2), 022814. <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.88.022814>
- arXiv:2608.03616. Quantitative measurement of liquidation cascades in crypto perps. <https://arxiv.org/abs/2608.03616>
- Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. *Biometrika*, 58(1), 83–90. <https://academic.oup.com/biomet/article-abstract/58/1/83/259178>
