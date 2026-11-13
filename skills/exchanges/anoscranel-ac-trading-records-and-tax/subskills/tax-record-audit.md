---
name: tax-record-audit
domain: investing/tax-record-audit
trigger: "Auditing a tax pack before it goes to a professional."
anti_trigger: "Not for filing, and not for interpreting tax law."
scope: "Auditing the pack before submission: totals, gaps, and the errors that recur."
status: seedling
---

# Tax record audit

## Standard

The audit is the last cheap checkpoint. It checks the pack against itself: do the totals reconcile, does every statement have a matching record, does every record have a statement, are the open questions actually listed, and does the manifest match the files. These are mechanical checks, and mechanical checks catch the errors that cost the most time later.

The recurring errors are few and predictable: a missing month, a transfer counted twice, a fee not separated, a reward valued at the wrong date, an account omitted because it was closed. Each has a specific check, and a pack that passes all of them is a pack a professional can start work on immediately.

Primary sources: <https://www.irs.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Totals are reconciled across the pack: summary, detail, and statements must agree.
- Every statement is matched to a record and every record to a statement; unmatched items are listed.
- Month coverage is checked explicitly; a missing month is a finding.
- Closed accounts are checked separately, because they are the ones most often omitted.
- Open questions are counted and listed; an empty list is treated as a claim that must be justified.
- The manifest is checked against the files on disk, item by item.

## Procedure

1. Reconcile the totals across summary, detail, and statements.
2. Match statements to records in both directions.
3. Check month coverage across the period.
4. Check closed accounts and transfers.
5. Count and list the open questions.
6. Verify the manifest against the files.

## Anti-patterns

- Auditing the summary alone.
- Assuming a closed account needs no record.
- Leaving the open-questions list empty without justification.
- Trusting the manifest without checking it.
- Fixing an error in the pack without re-running the audit.

## Done checklist

- [ ] Totals reconciled across the pack.
- [ ] Statements and records matched both ways.
- [ ] Month coverage checked.
- [ ] Closed accounts and transfers checked.
- [ ] Open questions counted and listed.
- [ ] Manifest verified against files.

## Sources

- Tax administration guidance on records and audits: <https://www.irs.gov/>
- Transaction reporting context: <https://www.sec.gov/investor>
- Investor education on keeping records: <https://www.investor.gov/introduction-investing>

Run the audit twice: once when the pack is assembled, and once after any correction. Corrections have a way of introducing the next error, and the second pass costs minutes against a first-pass error that can cost a filing.
