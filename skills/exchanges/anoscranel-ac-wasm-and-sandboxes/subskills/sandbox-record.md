---
name: sandbox-record
domain: software-engineering/sandbox-record
trigger: "Writing the record of a sandbox deployment and its surface."
anti_trigger: "Not for security audit reports in general, and not for the toolchain record."
scope: "The written record: surface, capabilities, and the audits behind them."
status: seedling
---

# Sandbox record

## Standard

The sandbox record states, per guest class: the import set it is provisioned with, the resource caps applied, the shared layouts it speaks, the instance lifecycle model, and the audits that reviewed each. Its function is to make the trust posture legible — a reader can see exactly what a guest can reach without reading the host's source — and to make drift visible when a new import or a looser cap appears.

Its second function is honest comparison over time. The record carries what was audited, when, and by which tool or review, so the difference between "no known issues" and "never checked" is never lost. A sandbox posture that is never re-audited is decaying silently, because imports accrete in development, and the record is the artefact that makes the accretion a reviewable event.

Primary sources: <https://webassembly.github.io/spec/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each guest class with its import set, resource caps, and lifecycle model.
- Shared layouts are recorded with versions, matching the linear-memory record.
- Every entry carries the date and the audit or review that covered it.
- Import-set and cap changes are appended, not edited; the history is the audit trail.
- The record names the side-channel posture: placement policy and shape-constant decisions.
- A re-audit is scheduled on every import-set change, not on the calendar alone.

## Procedure

1. Write the per-guest-class import sets and caps.
2. Attach the shared layouts and their versions.
3. Record the lifecycle model and the measured costs.
4. Record the side-channel posture.
5. Attach the audit history for each entry.
6. Append every change with its date and re-audit note.

## Anti-patterns

- Describing the posture as "sandboxed" without the import list.
- Editing history instead of appending.
- No audit note on an entry.
- Calendar-only audits while imports change weekly.
- Caps recorded in a different place from the imports they bound.

## Done checklist

- [ ] Guest classes with imports and caps listed.
- [ ] Layouts and versions recorded.
- [ ] Lifecycle and costs recorded.
- [ ] Side-channel posture recorded.
- [ ] Audit history attached per entry.
- [ ] Changes appended with dates.

The record should also name what the sandbox is trust-boundary against: a posture scoped to untrusted third-party plugins differs from one scoped to trusted-but-buggy internal code, and the same import set can be generous for the second and unacceptable for the first, so the class's threat statement belongs at the head of its entry.

## Sources

- Provisioning model: <https://webassembly.github.io/spec/>
- Pre-registration practice: <https://osf.io/prereg/>
- Runtime concepts: <https://webassembly.org/specs/>
