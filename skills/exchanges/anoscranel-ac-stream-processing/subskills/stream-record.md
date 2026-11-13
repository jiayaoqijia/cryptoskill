---
name: stream-record
domain: software-engineering/stream-record
trigger: "Writing down the time semantics a stream answers by."
anti_trigger: "Not for recommending a framework, and not for a pipeline log."
scope: "The written record: time semantics, windows, lateness policy, and state bounds."
status: seedling
---

# Stream record

## Standard

The stream record states the contract a stream's outputs obey: which clock each is correct in, the watermark or trigger that closes each computation, the lateness policy with its side-output and correction behaviour, and the state bounds the deployment must live within. It exists because stream correctness is invisible: a dashboard that undercounts by discarding late events still draws a line, and only the written policy tells anyone what the line means.

Its most useful entry is the inconsistency ledger. Every consumer wants a slightly different clock, a slightly different lateness, a slightly different window, and the record names the divergences rather than letting them accumulate silently in configuration. Two outputs that differ by policy are two honest numbers; two outputs that differ by accident are an argument waiting for its first meeting.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://osf.io/prereg/>.

## Decision rules

- The record states, per output, the clock it is correct in.
- Per output: window type, size, alignment, and trigger.
- Per output: allowed lateness, side-output routing, and correction behaviour downstream.
- Per stateful operator: key, per-key size, retention, and worst-case total.
- Divergences between outputs are listed as deliberate, with the reason.
- Every policy change is an amendment with a date, never a silent edit.

## Procedure

1. Record the clock per output.
2. Record windows and triggers per output.
3. Record lateness and correction policies.
4. Record state bounds per operator.
5. Write the divergence ledger.
6. Amend with dates; never edit history.

## Anti-patterns

- A record of pipeline topology with no time semantics.
- Lateness policy implied by framework defaults.
- Divergences undocumented, surfacing first as a number dispute.
- State bounds absent until a failure finds them.
- Policies edited silently, so no one can say when the number changed meaning.

## Done checklist

- [ ] Clock per output recorded.
- [ ] Windows and triggers per output recorded.
- [ ] Lateness and correction policies recorded.
- [ ] State bounds recorded.
- [ ] Divergence ledger written.
- [ ] Amendments dated.

The record's divergence ledger deserves a worked example: when a revenue dashboard counts by event time and an alert counts by processing time, both are right in their own clock, and the ledger is the only place the two-second nightly discrepancy is explained before it becomes a data-quality incident.

## Sources

- Stream semantics documentation: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Stream processing references: <https://dataintensive.net/>
