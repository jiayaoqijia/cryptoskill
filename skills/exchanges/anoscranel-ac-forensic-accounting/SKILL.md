---
name: ac-forensic-accounting
description: "Reading financial statements for what the structure conceals: related-party transactions and disclosure gaps, off-balance-sheet arrangements and variable interest entities, round-tripping and revenue that has no cash, capitalised costs and the expenses they hide, segment disclosure and what disappears between segments, cash conversion and the accounts that absorb it, and the written forensic record. It analyses disclosure forensically; it never accuses a company of fraud and never recommends a security. Use when asking \"related party\", \"off balance sheet\", \"variable interest entity\", \"VIE\", \"round tripping\", \"capitalised costs\", \"segment disclosure\", \"why is cash flow so different from earnings\", \"forensic accounting\", \"accounting red flags\". Not for accruals and non-GAAP bridges in reported results (ac-earnings-quality), not for the investment case (ac-equity-research), not for auditing or internal controls (ac-security-standards)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Forensic accounting

## Overview

Financial statements are a representation, prepared within rules that permit choices, and the choices are disclosed in notes that most readers skip. Forensic reading is the practice of following those choices: which entities are consolidated, which transactions are with parties the company controls, which costs are capitalised rather than expensed, and which segments are amalgamated so that a deteriorating business disappears inside a growing one.

This skill covers those readings and the evidence that supports them. It is deliberately framed as questions with document references rather than as conclusions: a related-party transaction is not a fraud, and a capitalised cost is not necessarily an overstatement, but each is a place where the reported result and the underlying economics can diverge, and the divergence is what a reader needs to see.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## When to use

- When reported earnings and cash flow diverge without an obvious explanation.
- When a company's structure includes entities whose consolidation is unclear.
- When related-party transactions or segment changes appear in the notes.
- When capitalised costs or unusual asset balances have grown materially.

## When NOT to use

- For accrual analysis and non-GAAP bridges in reported results (use ac-earnings-quality).
- For the investment case on a company (use ac-equity-research).
- For audit, control, or compliance programme design (use ac-security-standards).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/related-party-transactions.md` | `investing/related-party-transactions` | Disclosures, gaps, and the questions a transaction raises. |
| `subskills/off-balance-sheet-entities.md` | `investing/off-balance-sheet-entities` | Consolidation, variable interests, and what the boundary excludes. |
| `subskills/round-tripping-and-revenue-quality.md` | `investing/round-tripping-and-revenue-quality` | Revenue without cash, circular transactions, and the evidence trail. |
| `subskills/capitalised-costs.md` | `investing/capitalised-costs` | Capitalisation policy, its growth, and the expenses it defers. |
| `subskills/segment-disclosure.md` | `investing/segment-disclosure` | What changes when segments are redefined or amalgamated. |
| `subskills/cash-conversion-forensics.md` | `investing/cash-conversion-forensics` | Which accounts absorb the gap between earnings and cash. |
| `subskills/forensic-record.md` | `investing/forensic-record` | The written record: question, document reference, and finding. |

## Status and honest limits

Every practice described here has a legitimate business explanation, and most companies that use a permitted accounting choice are using it for a reason that is not concealment. The output of this analysis is a set of questions with references, not an allegation, and the difference matters both ethically and practically: an unfounded accusation is a serious harm, while a documented question is a legitimate part of reading a filing.
