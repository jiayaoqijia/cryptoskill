---
name: log-assumptions-before-acting
description: Use when a task requires decisions the request did not specify. Write each assumption to a file before executing, tag its reversal cost, and confirm the costly ones first.
---

# Log assumptions before acting

Unstated assumptions are the cheapest thing to fix at minute one and the most expensive at minute sixty. This skill makes you write each one down and price it before you build on it.

## Procedure

1. Create `ASSUMPTIONS.md` in the working directory at the start of the task, before the first write or API call.

2. For each gap in the request, add a numbered row with four fields: `N | assumption | impact if wrong | how to confirm`.

3. Keep each assumption falsifiable. "Uses PostgreSQL 15" is testable; "the database is fine" is not, and must be split into testable parts.

4. Tag every row `reversible` or `costly`. A `costly` row changes data, spends money, or is hard to undo.

5. Confirm every `costly` row with the user before proceeding. Proceed unconfirmed only on `reversible` rows, and mention them in your next message.

6. Timestamp each row at creation (`date -u +%FT%TZ`) so a later reviewer can see the ordering of belief.

7. When evidence settles a row, edit it in place to `CONFIRMED` or `WRONG`. If `WRONG`, stop dependent work and re-plan rather than patching around it.

8. At task end, `grep -vc "^#" ASSUMPTIONS.md` should equal the number of rows, and none may still be blank — every row ends `CONFIRMED` or `WRONG`.

## Pitfalls

- Writing assumptions after acting is rationalisation; the timestamp must precede the dependent step.
- A vague assumption cannot be confirmed or refuted, so it provides no protection.
- Three 90% assumptions stack to 73%; log the chain so the compounded risk is visible.
- Deleting a wrong assumption erases the audit trail; mark it wrong and keep the row.
- Silently widening an assumption mid-task ("well, it's close enough") defeats the whole log.

## Verification

    grep -c "CONFIRMED\|WRONG" ASSUMPTIONS.md; grep -c "^[0-9]" ASSUMPTIONS.md   # counts must match

Report each `costly` assumption to the user before touching data, one line each.
