---
name: sequence-and-gaps
domain: software-engineering/sequence-and-gaps
trigger: "Making missing audit events visible as findings rather than silence."
anti_trigger: "Not for metric counters, and not for chain verification design alone."
scope: "Sequence numbers, visible gaps, and the silence they can indicate."
status: seedling
---

# Sequence and gaps

## Standard

A monotonic sequence number on each entry gives the trail two properties. It orders events without depending on timestamp precision, and it makes absence visible: a gap in the sequence is a detectable fact, while a missing event in an unordered log is indistinguishable from an event that never happened. An investigator's first question is often "what is missing", and only a sequence lets the question be asked.

The design decision is what a gap means. In a single-writer log a gap may indicate lost writes or an off-sequence insertion and is always an incident to explain; in a sharded log gaps are structural and the partition identity accompanies the sequence, so the invariant is per-partition continuity. The record states which scheme applies and what the verifier does when it finds a gap — report, halt, or annotate — decided before it ever fires.

Primary sources: <https://www.rfc-editor.org/rfc/rfc6962.html> and <https://csrc.nist.gov/pubs/sp/800/92/final>.

## Decision rules

- Assign a per-partition monotonic sequence to every entry.
- Record the partitioning scheme, if any, alongside each sequence.
- Define gap handling in verification: report, alert severity, and who is told.
- Treat an unexplained gap as an incident, not as logging noise.
- Keep the sequence independent of timestamp ordering — record both, trust the sequence for order.
- Verify continuity from the first entry of the retention window to the last.

## Procedure

1. Choose single-sequence or per-partition sequencing and record it.
2. Attach sequence and partition to every entry.
3. Implement verification that checks continuity across the window.
4. Define the gap response and alert routing.
5. Test with a deliberately removed entry and confirm the gap is detected and reported.
6. Record the scheme, the verifier, and the response policy.

## Anti-patterns

- Timestamps as the only ordering — clocks skew and gaps vanish.
- Gaps explained away as "sharding" without a partition scheme that accounts for them.
- Verification that stops at the head and never walks the tail.
- A sequence that resets on rotation, breaking continuity.
- No test that a removed entry actually raises the alarm.

## Done checklist

- [ ] Sequence scheme chosen and recorded.
- [ ] Partition identity present where sharded.
- [ ] Continuity verification implemented.
- [ ] Gap response defined and routed.
- [ ] Removal test passes.
- [ ] Scheme and policy in the audit record.

## Sources

- Certified-log sequence and continuity proofs: <https://www.rfc-editor.org/rfc/rfc6962.html>
- Log review and verification practice: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Identity and request context to pair with sequence: <https://w3.org/TR/trace-context>
