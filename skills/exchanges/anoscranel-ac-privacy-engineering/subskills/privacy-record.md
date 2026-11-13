---
name: privacy-record
domain: software-engineering/privacy-record
trigger: "Writing the record of what personal data the system holds and how it is governed."
anti_trigger: "Not for legal advice, and not for security posture."
scope: "The written record: inventory, retention, subprocessors, and gaps."
status: seedling
---

# Privacy record

## Standard

The privacy record gathers the inventory, the retention schedule, the subprocessor list, and the open gaps into one place with dates. It is the document that answers, without a project, the questions that arrive with a deadline: where is this data, who else has it, how long is it kept, and what is not yet handled.

Its second function is to keep the gaps visible. Every system has them — a store not yet covered by the deletion job, a subprocessor whose agreement lags, a field whose purpose has lapsed — and a record that names them with an owner and a date is a record that can be acted on, while a record that lists only what is complete is a record that flatters.

Primary sources: <https://ico.org.uk/> and <https://osf.io/prereg/>.

## Decision rules

- The record contains the field inventory, the retention schedule, and the subprocessor list.
- Every gap carries an owner and a target date.
- The legal determinations are recorded as questions answered by counsel, with the date.
- The record names the systems not yet in scope and why.
- Review triggers are dated: new system, new subprocessor, retention change, request volume shift.
- The record is append-only; corrections are dated amendments.

## Procedure

1. Assemble the inventory, retention schedule, and subprocessor list.
2. Record each open gap with an owner and a date.
3. Record legal determinations with their date and source.
4. Record out-of-scope systems and the reason.
5. Set review triggers.
6. Amend at each trigger and record what changed.

## Anti-patterns

- A record that lists only completed work.
- Gaps without owners, which never close.
- Recording a legal conclusion without its date and source.
- Omitting systems that are known to be out of scope.
- No triggers, so the record describes a state that has passed.

## Done checklist

- [ ] Inventory, retention, subprocessors recorded.
- [ ] Gaps recorded with owners and dates.
- [ ] Legal determinations dated.
- [ ] Out-of-scope systems recorded.
- [ ] Triggers dated.
- [ ] Amendments dated.

The record should also state its own age: a privacy record without a visible date is read as current even when it is a year old, and the single most useful line in it is the date of the last review against the systems that exist now.


## Sources

- Data protection guidance: <https://ico.org.uk/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- NIST privacy framework: <https://www.nist.gov/privacy-framework>
