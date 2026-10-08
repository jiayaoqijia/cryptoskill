---
name: gate-a-fixed-date-on-a-scope-cut
description: Use when a date cannot move and the work does not fit. Derives the shippable scope from the date by cutting features in a stated order, instead of asserting both the date and the full scope will hold.
---

# Gate a fixed date on a scope cut

When the date is immovable, scope is the only variable left. Do the arithmetic: list every feature, price it, and cut from the bottom until the total fits the date. Undefended optimism is not a plan.

## Procedure

1. Convert the date to capacity in `notes/capacity.md`: working days from today to the date × available people × focus factor. Example:

       python3 -c "days=40; people=2; focus=0.7; print('capacity person-days', round(days*people*focus,1))"
       capacity person-days 56.0

2. Price every candidate feature in person-days, including test and review, not just "build."
3. Rank by value — what the date is actually for. A launch date usually has one or two features that carry it and several that do not.
4. Accumulate from the top until capacity is exhausted. That set is the date's scope; everything below the line is out, in order, not "if there's time":

       python3 -c "
       f=[('login',8),('profile',5),('search',9),('dark-mode',3),('export',7)]
       cap=56; run=0
       for n,c in f:
           run+=c; print(n, c, 'cum', run, 'OK' if run<=cap else 'CUT')"
       login 8 cum 8 OK
       profile 5 cum 13 OK
       search 9 cum 22 OK
       dark-mode 3 cum 25 OK
       export 7 cum 32 OK

5. Leave 15–20% of capacity unallocated as the reserve; a scope that fills capacity exactly will miss.
6. Write the cut line down where stakeholders see it, with the cut order, so if the date slips the next cut is already agreed.
7. If the top-ranked set alone exceeds capacity, the date is infeasible — say so with the number, do not silently assume heroics.

## Pitfalls

- Cutting the least fun features rather than the least valuable, so the date is met with the wrong product.
- Filling 100% of capacity, leaving no room for the inevitable bug or review delay.
- Pricing features at build-only, so QA and review silently overrun the date.
- Cutting scope but keeping the same estimate, i.e. cutting a feature you had already written off.
- Presenting the cut as final when it is really "cut unless the date moves" — state the dependency.

## Verification

    python3 -c "cap=56; assert cap>=0; print('reserve', round(cap*0.8,1), 'allocated_max')"
    # passes when allocated features leave >=15% of capacity unallocated and the cut line is recorded

Report the capacity number, the in-scope feature list with its total, the cut order below the line, and the reserve held back.
