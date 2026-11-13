---
name: policy-compliance-monitoring
domain: investing/policy-compliance-monitoring
trigger: "Testing whether a portfolio is inside its mandate, and handling breaches."
anti_trigger: "Not for setting the limits, and not for legal advice."
scope: "Testing compliance, pre-trade versus post-trade, and breach handling."
status: seedling
---

# Policy compliance monitoring

## Standard

Compliance can be tested before a trade or after it. Pre-trade testing prevents a breach; post-trade testing detects one. Most mandates require both, and the difference matters when a breach occurs, because a post-trade system produces breaches that were avoidable and a pre-trade system alone misses the drift that no single trade caused.

Drift is the failure mode that post-trade-only and pre-trade-only systems share. A portfolio can move outside its limits through market movement, through a series of individually compliant trades, or through a corporate action that changes a holding's characteristics. Monitoring therefore needs a periodic full-portfolio test in addition to the trade-level checks, and the record should state which tests run, how often, and who reviews the exceptions.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record which tests are pre-trade and which are post-trade.
- Record the frequency of full-portfolio testing.
- Record the tolerance or threshold at which an exception is raised.
- Record the breach-handling procedure and its deadlines.
- Record who is notified and who decides the remedy.
- Record every breach with its cause, its remedy, and its closure date.

## Procedure

1. Record the test inventory and their timing.
2. Record tolerances and exception thresholds.
3. Record the breach procedure and deadlines.
4. Record notification and decision authority.
5. Log breaches with cause and remedy.
6. Review the log for patterns rather than incidents.

## Anti-patterns

- Testing only at trade time and missing drift.
- Testing only periodically and missing avoidable breaches.
- Logging breaches without a closure date.
- Treating a breach as closed when it is merely reported.
- Reviewing individual breaches without looking for a pattern.

## Done checklist

- [ ] Test inventory recorded.
- [ ] Tolerances recorded.
- [ ] Breach procedure recorded.
- [ ] Notification recorded.
- [ ] Breach log maintained with closure.
- [ ] Pattern review performed.

The pattern that review should look for is a breach that recurs at the same point in the cycle: a limit that is breached every quarter by market movement rather than by trading is telling you that the limit is set too tight for the portfolio's own volatility, which is a mandate design problem rather than a compliance failure, and treating it as the latter produces a log of exceptions that nobody acts on.

## Sources

- Investment management standards: <https://www.cfainstitute.org/>
- Regulatory compliance context: <https://www.sec.gov/investor>
- Investor protection guidance: <https://www.investor.gov/introduction-investing>
