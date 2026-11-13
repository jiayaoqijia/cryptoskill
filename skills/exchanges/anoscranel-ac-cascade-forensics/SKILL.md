---
name: ac-cascade-forensics
description: "Reconstructs after the fact what happened in a leveraged crypto liquidation crash: branching ratios, fill-log timelines, tape reconstruction, participation anomalies, and evidence standards. Analyses past cascades with rigorous data; it never predicts future liquidations or prices. Use when asking 'cascade forensics', 'analyse this liquidation event', 'what happened in this crash', 'branching ratio', 'reconstruct the timeline', 'was this a cascade'. Not for reading a live set-up (ac-liquidation-hunt-analysis), not for the trade record (ac-crypto-trading-discipline), not for generic research method (ac-deep-researcher)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Cascade Forensics

## Overview

- Market microstructures show liquidity crashes leave execution footprints on transparent order books (<https://epubs.siam.org/doi/abs/10.1137/120870932>).
- Risk analysis requires strict separation between historical fills and monitoring proxies (<https://press.princeton.edu/books/paperback/9780691118508/why-stock-markets-crash>).

Cascade forensics reconstructs leveraged liquidation events post-conclusion. It examines exchange fill logs, aggregated trade tapes, and order-book snapshots to establish the mechanical chain of forced liquidations, price impact, and backstop exhaustion. Forensics is strictly retrospective: it establishes what happened and why, but never predicts future prices or liquidation thresholds.

Mathematical models such as branching-ratio estimators show that market-wide liquidations operate in subcritical regimes where avalanches damp out rather than explode infinitely. Rigorous data analysis separates verified execution sequences from the myths of predictable liquidation heatmaps and non-existent whale tracking.

## When to use

- Reconstructing the timeline and mechanics of a major crypto derivative crash after settlement.
- Measuring the branching ratio and subcritical dynamics of forced liquidations from execution logs.
- Evaluating exchange fill logs, aggregated feeds, and reconstruction error bars.
- Auditing forensic reports for evidence standards, independent lineages, and sample boundaries.

## When NOT to use

- Evaluating a live trading set-up or looking for liquidation levels to trade against (use ac-liquidation-hunt-analysis).
- Managing position sizing, risk budgets, or recording trade execution journals (use ac-crypto-trading-discipline).
- Conducting general literature reviews or open-ended economic research without specific cascade focus (use ac-deep-researcher).

## Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| [subskills/fill-log-reading.md](subskills/fill-log-reading.md) | crypto-trading/fill-log-reading | Reconstructing a cascade timeline from a transparent venue's fill log: required fields, ordering, dedup, gaps; what a fill log proves vs what it merely suggests. |
| [subskills/branching-ratio.md](subskills/branching-ratio.md) | crypto-trading/branching-ratio | Measuring the branching ratio lambda from a cascade's fills; the subcritical reading; what subcriticality forbids. |
| [subskills/participation-and-anatomy.md](subskills/participation-and-anatomy.md) | crypto-trading/participation-and-anatomy | Who participated and at what size; what account-level transparency establishes vs the absent decomposition. |
| [subskills/proxies-and-tape.md](subskills/proxies-and-tape.md) | crypto-trading/proxies-and-tape | When no fill log exists: aggregated liquidation feeds, exchange endpoints, reconstruction error bars, and the collider problem. |
| [subskills/evidence-standards.md](subskills/evidence-standards.md) | crypto-trading/evidence-standards | What a forensic claim needs: two independent lineages, sample size, time window, the claim-card discipline, and the four absences. |
| [subskills/report-writing.md](subskills/report-writing.md) | crypto-trading/report-writing | The forensic report: timeline, mechanism, evidence table, limits section, reproducibility annex; stating what cannot be established. |
| [subskills/case-anatomy.md](subskills/case-anatomy.md) | crypto-trading/case-anatomy | The worked Oct 2025 case from the corpus: what was measured, what it showed, what it failed to predict; presented as a method demonstration. |

## Status and honest limits

Cascade forensics operates under strict epistemic boundaries. While transparent venues provide granular execution data, the broader market lacks universal account classification, making retail-versus-institutional distinctions speculative. Furthermore, branching-ratio measurements confirm that self-sustaining cascade models are mathematically impossible in subcritical markets. All conclusions must be bounded by explicit sample windows and verified against independent source lineages.

## Sources

- Cont, R., & de Larrard, A. (2013). Price dynamics in a Markovian limit order book. *SIAM Journal on Financial Mathematics*, 4(1), 1–25. <https://epubs.siam.org/doi/abs/10.1137/120870932>
- Sornette, D. (2004). *Why Stock Markets Crash: Critical Events in Complex Financial Systems*. Princeton University Press. <https://press.princeton.edu/books/paperback/9780691118508/why-stock-markets-crash>
- Lillo, F., & Farmer, J. D. (2004). The long memory of the efficient market. *Studies in Nonlinear Dynamics & Econometrics*, 8(3). <https://www.degruyter.com/document/doi/10.2202/1558-3708.1219/html>
- Central Bank of the Republic of Turkey (2025). Cryptoasset derivatives market structure and liquidation dynamics report. <https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Publications/Reports>
