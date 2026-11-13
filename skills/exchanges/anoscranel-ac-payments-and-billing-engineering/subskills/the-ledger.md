---
name: the-ledger
domain: software-engineering/ledger-double-entry
trigger: "Building the ledger behind balances, invoices, and payouts."
anti_trigger: "Not for accounting standards, and not for processor product choice."
scope: "Double entry as the invariant; balances as aggregates, never updates-in-place."
status: seedling
---

# The ledger

## Standard

The ledger is the system of record for money, and its minimal honest form is double entry: every movement of value is represented as two or more entries that always sum to zero across the affected accounts. This is not office decoration; the zero-sum property is an invariant that can be machine-checked, and it is what makes a money system self-auditing. When the sum of all entries over all accounts is not zero, something has already gone wrong, and the ledger says so without anyone having to look.

From the invariant follows the most important implementation rule: balances are never stored as a mutable number that code increments. Balances are aggregates — sums over entry ranges — and their correctness is protected because they cannot drift from their inputs; if payment code updates a balance field directly, the ledger becomes a suggestion rather than a record. The projection that shows a customer their balance computes it from entries, and an entry is immutable once written; correction is a new transaction whose reason is part of its identity.

Primary sources: <https://www.pcisecuritystandards.org/document_library/> and <https://docs.stripe.com/billing/subscriptions/overview>.

## Decision rules

- Every money movement is a transaction with two or more entries summing to zero.
- Entries are immutable; corrections are new transactions that reference what they correct with a reason.
- Balances are computed aggregates, never directly written fields.
- Accounts are named for role and owner, not for the system that wrote to them; account names are a cohesive taxonomy.
- Assigned accounts: customer funds, processor funds (a pending settlement), revenue, refunds — each its own account; operations between them are what the entry pair shows.
- The zero-sum check runs on every transaction at write time and periodically across history.

## Procedure

1. Identify the accounts needed for the money movements in the domain.
2. Define the transaction template for each type of movement; write its entry pairs explicitly.
3. Enforce the zero-sum validation at the write boundary.
4. Implement balances as cached aggregates computed from entries, and define when the cache refreshes.
5. Write corrections as referencing transactions with reasons; never edit an entry.
6. Periodically re-run the zero-sum check across history; report any anomaly as an incident, not a fix.

## Anti-patterns

- A balance column updated by payment code; the ledger becomes advisory.
- Single-entry records; invariants vanish and errors float silently.
- Anonymous accounts that blend the customer's money with the merchant's pending settlement.
- Corrections that overwrite the original entry; history becomes a fiction.
- Zero-sum checked only at audit time, when drift has already become loss or its illusion.

## Done checklist

- [ ] Entry pairs written explicitly per transaction type.
- [ ] Sum-to-zero validated at write time.
- [ ] Balances as aggregates, never direct writes.
- [ ] Accounts named by role and owner with a taxonomy.
- [ ] Corrections are referencing transactions.
- [ ] Historical zero-sum check scheduled.

## Sources

- PCI security standards library: <https://www.pcisecuritystandards.org/document_library/>
- Billing lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- Disputes: <https://stripe.com/docs/disputes>
