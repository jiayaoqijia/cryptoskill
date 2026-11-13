---
name: trace-sampling
domain: software-engineering/trace-sampling
trigger: "Choosing what to capture in full and what to record in outline."
anti_trigger: "Not for provider rate limits, and not for eval suites."
scope: "What to capture in full; what to record in outline."
status: seedling
---

# Trace sampling

## Standard

Full-fidelity capture of every span of every run costs storage and, more delicately, attention: a thousand traces a day is a corpus no one reads. Sampling is the stated policy for which runs are captured at full fidelity, which at outline (counts and timings, no payloads), and which at totals only. The choice is data-driven: error runs are always captured in full, a stated fraction of successful runs is kept for calibration, and everything else aggregates.

The critical asymmetry: failures are never sampled down. A run that ended wrong, retried, or exceeded a threshold is captured whole — those traces are the debugging corpus. Sampling applies to the successes, where the question is not "what happened here" but "what does normal look like", and outline-plus-totals answers that. The policy is written, versioned, and measured for sampling bias: if the captured fraction is unrepresentative, calibration days drift.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://langfuse.com/docs>.

## Decision rules

- Failed, retried, and threshold-exceeded runs: always full capture.
- Successful runs: a stated fraction at full fidelity, the rest at outline or totals.
- The fraction and its rationale are recorded; sampling without a written policy is drift.
- Measure the captured fraction for bias against the full population's error and step counts.
- Retain full traces long enough for debugging cycles; outlines last longer but carry less.
- Revisit the fractions when the run volume changes by an order of magnitude.

## Procedure

1. Write the policy: always-capture conditions, success fraction, outline fields.
2. Route runs at capture time by their end status into tiers.
3. Aggregate un-captured runs into daily totals for the population view.
4. Monthly, measure the captured sample against those totals for bias.
5. Adjust the fraction on written evidence, not intuition.
6. Version the policy; each change dated with the reason.

## Anti-patterns

- Uniform capture of everything; storage and attention both collapse.
- Sampling the failures as if they were successes; the debugging corpus shrinks.
- Sampling decided per day by whim; a written policy does the deciding.
- No bias measurement; the calibration fraction quietly unrepresentative.
- Fractions untouched across a tenfold volume change.

## Done checklist

- [ ] Policy written: tiers, fraction, fields.
- [ ] Failures always captured in full.
- [ ] Totals kept for the un-captured population.
- [ ] Bias measured against population totals.
- [ ] Fractions adjusted on evidence.
- [ ] Policy versioned with dated changes.

## Sources

- GenAI conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Tracing docs: <https://langfuse.com/docs>
- Semantic conventions source: <https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/README.md>
