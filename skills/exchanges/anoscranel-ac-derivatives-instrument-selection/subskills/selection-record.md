---
name: selection-record
domain: crypto-trading/selection-record
trigger: "record instrument selection criteria; document why instrument was chosen; review triggers for instruments"
anti_trigger: "how to trade this instrument; recommend a specific coin or contract"
scope: Documenting instrument selection criteria, weights, rejections, review triggers, and decision artifact rules.
status: seedling
---

## Standard

Instrument selection must be formalized as a rigorous written record rather than treated as an ad-hoc tactical preference. A complete selection record documents the decision criteria, weighted trade-offs between instruments, explicit justifications for rejected alternatives, and defined review triggers for position adjustment. This documentation enforces operational discipline and prevents emotional drift during volatile market conditions.

Crucially, the selection record is a decision artifact, not a trade recommendation. It captures the objective constraints and market conditions prevailing at the time of choice without predicting future price direction or guaranteeing returns. Maintaining this audit trail ensures that subsequent reviews can isolate whether performance failures stemmed from flawed instrument mechanics or unexpected macroeconomic shocks.

Primary sources for the claims here: <https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html> and <https://www.iosco.org/library/pubdocs/pdf/IOSCOPD603.pdf](https://www.iosco.org/library/pubdocs/pdf/IOSCOPD603.pdf>.

## Decision rules

1. Create a written selection record for every trading strategy before committing capital to spot, futures, or options.
2. Document explicit selection criteria and weights assigned to funding cost, liquidity depth, margin fit, and horizon alignment.
3. Record all alternative instruments considered and provide concrete reasons for their rejection.
4. Establish clear review triggers based on funding rate shifts, basis widening, or liquidity degradation to mandate instrument reassessment.
5. Apply the one-line test: the selection record documents objective structural trade-offs, never directional price predictions or return promises.

## Procedure

1. Compile all analytical findings from landscape evaluation, carry comparison, margin fit, and liquidity screening.
2. Draft the selection summary detailing the chosen instrument class and rejecting unviable alternatives.
3. Define quantitative review thresholds (e.g., funding rate exceeding 0.1% per 8 hours, bid-ask spread widening beyond 0.2%).
4. Archive the selection record in the trading desk repository as an immutable decision artifact.
5. Audit the selection record periodically against actual execution outcomes during post-trade reviews.

## Anti-patterns

- Making verbal or undocumented instrument selections based on intuition without evaluating structural trade-offs.
- Omitting rejected alternatives from the record, masking the decision process from subsequent audit.
- Failing to establish review triggers, leaving positions vulnerable to unmonitored structural regime shifts.
- Treating the selection record as a promotional justification for a directional trade rather than a risk management artifact.

## Done checklist

- [ ] Written selection record created prior to capital deployment.
- [ ] Criteria weights and structural trade-offs documented.
- [ ] Rejected instrument alternatives explicitly justified.
- [ ] Quantitative review triggers established for ongoing monitoring.
- [ ] Selection record archived as immutable decision artifact.

## Sources

- IOSCO Compliance and Operational Risk Recordkeeping Standards: [https://www.iosco.org/library/pubdocs/pdf/IOSCOPD603.pdf](https://www.iosco.org/library/pubdocs/pdf/IOSCOPD603.pdf)
- Derivatives Risk Management and Margin Methodologies: [https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html)
- Tail-risk calibration and hedging friction in crypto option surfaces: [https://arxiv.org/abs/2611.00958](https://arxiv.org/abs/2611.00958)
