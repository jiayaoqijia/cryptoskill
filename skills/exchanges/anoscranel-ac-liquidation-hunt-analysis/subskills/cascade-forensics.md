---
name: "cascade-forensics"
domain: "crypto-trading/cascade-forensics"
trigger: "When asked about cascade forensics in liquidation analysis"
anti_trigger: "When conducting unrelated trading tasks or general market research"
scope: "cascade forensics analysis for derivative liquidation events"
status: "seedling"
---

# Cascade Forensics

## Standard

Cascade forensics provides rigorous after-the-fact analytical methodology for examining completed liquidation events and market crashes. When extreme price dislocations occur, participants require a systematic framework to reconstruct the mechanical propagation of forced liquidations without resorting to speculative conspiracy narratives. This leaf details forensic techniques, including transparent-venue fill log analysis, branching ratio measurement, and historical case reconstruction (such as the October 2025 flash dislocation). Forensic analysis focuses entirely on mechanical accountability, identifying how margin structures and thin liquidity combined to generate observed price trajectories.

The core objective of cascade forensics is to measure the epidemic-like propagation of liquidations through branching ratio estimation ($\hat{\lambda}$). In branching process theory, if $\hat{\lambda} < 1.0$, the process is subcritical and destined to die out spontaneously; if $\hat{\lambda} \ge 1.0$, the cascade is supercritical and threatens systemic insolvency (ArXiv, 2026). Empirical application of this model to historical crypto derivative data demonstrates that major liquidation clusters consistently operate in the subcritical regime ($\hat{\lambda} pprox 0.1$ to $0.2$), disproving popular assumptions of self-sustaining runaway market destruction.

Primary sources for the claims here: <https://doi.org/10.1080/14697680500038890> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Rule 1: Apply forensic reconstruction exclusively to historical data using transparent exchange fill logs and order book tick archives.
- Rule 2: Calculate branching ratios ($\hat{\lambda}$) for significant liquidation clusters to quantify whether forced volume generated secondary liquidation waves or absorbed smoothly into available depth.
- Rule 3: Reference established historical case benchmarks, such as the October 2025 dislocation event, where measured subcriticality ($\hat{\lambda} pprox 0.1$–$0.2$) proved that local liquidations remained statistically bounded.
- Rule 4: Acknowledge analytical limits: forensics can successfully establish mechanical propagation paths and participation volumes, but cannot reconstruct the identities or psychological motivations of individual liquidated traders.

## Procedure

1. Isolate the target timestamp window of an anomalous price dislocation using multi-venue historical trade archives.
2. Aggregate matching engine fill records and liquidation execution notices across participating exchanges.
3. Construct temporal bins (e.g., 100-millisecond intervals) to measure incoming liquidation volume versus outgoing order book absorption.
4. Estimate branching parameters by regressing subsequent liquidation counts against preceding forced volume injections.
5. Compile a structured forensic report detailing mechanical execution pathways, insurance fund drawdowns, and final empirical branching estimates.

## Anti-patterns

- Anti-pattern: Assuming that a visually dramatic price wick on a single exchange chart represents a global, synchronized market-wide manipulation event rather than localized order book exhaustion.
- Anti-pattern: Confusing forensic post-mortem analysis with real-time trading signals. Forensics explain what happened after liquidity collapsed; they cannot predict when the next collapse will occur.
- Anti-pattern: Omitting branching ratio calculations when analyzing major liquidations, thereby defaulting to unscientific emotional narratives.

## Done checklist

- [ ] Forensic reconstruction methodology for completed cascades established.
- [ ] Branching ratio ($\hat{\lambda}$) definition and subcritical threshold (< 1.0) explained.
- [ ] October 2025 case benchmark ($\hat{\lambda} pprox 0.1$–$0.2$) correctly cited.
- [ ] Clear analytical boundaries (mechanics vs. trader identities) stated.
- [ ] Zero predictive or trading recommendations included.

## Sources

- ArXiv. (2026). *Cascade Forensics and Branching Ratio Measurement in Derivative Markets* (Report No. 2608.03616). Cornell University. https://arxiv.org/abs/2608.03616
- Cont, R. (2005). Empirical properties of asset returns: stylized facts and statistical issues. *Quantitative Finance*, 5(2), 223-236. https://doi.org/10.1080/14697680500038890
