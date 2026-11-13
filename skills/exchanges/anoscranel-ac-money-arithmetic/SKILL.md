---
name: ac-money-arithmetic
description: "Representing and computing money without losing cents: integer minor units versus binary floating point, decimal semantics and precision, rounding modes and where each is appropriate, allocation that distributes remainders, currency conversion and its rounding sequence, day-count and accrual arithmetic, reconciliation tolerance, and the written money-policy record. Use when asking \"floating point money\", \"decimal places\", \"rounding mode\", \"banker's rounding\", \"split an amount\", \"allocate a remainder\", \"penny discrepancy\", \"currency conversion rounding\", \"why is there a cent missing\", \"money type\". Not for pricing strategy, not for tax computation, and not for test technique in general (ac-testing)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Money arithmetic

## Overview

Most floating-point discussions in engineering are about precision; money arithmetic is about policy. A binary floating-point type cannot represent a decimal fraction exactly, so a cent vanishes or appears depending on the order of operations, but the deeper issue is that rounding a monetary amount requires a decision — which mode, applied at which step, with the remainder going where.

This skill covers the representation and the policy together, because they are one decision. Integer minor units and a decimal type both avoid binary error and both still need a rounding rule for division, allocation, conversion, and accrual. The record states the representation, the rounding mode per operation, and the tolerance at which a reconciliation difference is accepted rather than investigated.

Primary sources: <https://www.iso.org/> and <https://www.bis.org/>.

## When to use

- When choosing a representation for monetary amounts.
- When an operation requires rounding, allocation, or conversion.
- When reconciling two systems that disagree by small amounts.
- When accrual or interest arithmetic must match a stated convention.

## When NOT to use

- For pricing and commercial strategy (outside engineering).
- For tax computation, which depends on jurisdiction (consult a professional).
- For general numeric testing technique (use ac-testing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/representation-and-types.md` | `software-engineering/representation-and-types` | Minor units, decimal types, and why binary floating point fails. |
| `subskills/rounding-modes.md` | `software-engineering/rounding-modes` | Half-up, half-even, and truncation, and where each belongs. |
| `subskills/allocation-and-remainders.md` | `software-engineering/allocation-and-remainders` | Splitting an amount so the parts sum to the whole. |
| `subskills/conversion-and-precision.md` | `software-engineering/conversion-and-precision` | Currency conversion, the rounding sequence, and display precision. |
| `subskills/accrual-and-daycount.md` | `software-engineering/accrual-and-daycount` | Day-count conventions, compounding, and period arithmetic. |
| `subskills/reconciliation-tolerance.md` | `software-engineering/reconciliation-tolerance` | The difference at which a discrepancy is a defect. |
| `subskills/money-record.md` | `software-engineering/money-record` | The written policy: representation, rounding, and tolerance. |

## Status and honest limits

Currency, day-count, and rounding conventions are regulated in places and conventional elsewhere, and the correct choice depends on the instrument and the jurisdiction rather than on engineering preference. Nothing here constitutes accounting or tax advice. A money policy also cannot be inferred from a codebase once it has drifted, which is why the record is written before the first ambiguous operation rather than after the first discrepancy.
