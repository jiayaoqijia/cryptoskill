---
name: shadow-and-verification
domain: software-engineering/shadow-and-verification
trigger: "Proving the new store answers correctly before traffic trusts it."
anti_trigger: "Not for load testing, and not for recommending a comparison tool."
scope: "Serving the new store silently and comparing results before trusting it."
status: seedling
---

# Shadow and verification

## Standard

Shadow traffic sends a copy of real reads to the new store, discards its answers, and compares them against the old store's answers. The comparison is the evidence for cutover, and its quality is decided by coverage — which paths are shadowed, which endpoints, which tenants — and by the comparison rule itself: exact equality is right for deterministic reads, and tolerance or equivalence rules are needed for anything ranked, sampled, or time-dependent.

Two traps recur. Silent coverage gaps: the shadow exercises only the traffic it was pointed at, and a rarely-taken branch ships unverified, then becomes the first thing production hits after the switch. And metric ambiguity: a comparison that reports "99.5 percent match" hides which half-percent differs, and a mismatch concentrated in one shape of query is a defect while the same total spread thin across noise is a judgement call. The record must hold the mismatch taxonomy, not only its rate.

Primary sources: <https://martinfowler.com/> and <https://sre.google/>.

## Decision rules

- Record the shadowed share of traffic and how it is selected.
- Record the coverage map: endpoints, tenants, and rarely-taken paths deliberately included.
- Record the comparison rule per output: exact, tolerance, or equivalence-shaped.
- Record the mismatch taxonomy: by endpoint, error class, and example rows.
- Set the cutover gate on the taxonomy being understood, not on a bare percentage.
- Record how long the shadow must stay quiet before the switch is scheduled.

## Procedure

1. Select the traffic share and its sampling rule.
2. Build the coverage map including rare paths.
3. Write the comparison rules per output kind.
4. Run the shadow and collect mismatches into a taxonomy.
5. Investigate each mismatch class to defect, tolerance, or equivalence.
6. Set the quiet-period gate and hold the switch until it passes.

## Anti-patterns

- A bare match percentage with no breakdown.
- Shadowing only the easy endpoints and shipping the rest unverified.
- Exact comparison on outputs that are legitimately nondeterministic.
- Mismatches attributed to "timing" without any evidence, repeatedly.
- The quiet period shortened because a deadline is closer than the gate.

## Done checklist

- [ ] Traffic share and sampling recorded.
- [ ] Coverage map with rare paths included.
- [ ] Comparison rule per output.
- [ ] Mismatch taxonomy assembled.
- [ ] Each class dispositioned.
- [ ] Quiet-period gate held.

## Sources

- Migration and parallel-run patterns: <https://martinfowler.com/>
- Verification practice: <https://sre.google/>
- Data engineering references: <https://www.distributed-systems.net/>
