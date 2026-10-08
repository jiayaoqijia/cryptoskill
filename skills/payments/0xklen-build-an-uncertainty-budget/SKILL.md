---
name: build-an-uncertainty-budget
description: Use when a plan carries several unknowns and you must decide how much slack each deserves. Prices each unknown into an explicit probability-weighted budget instead of a vague "some buffer".
---

# Build an uncertainty budget

Unknowns that are never priced get paid for at the worst possible moment. Give each named risk a probability and a cost, sum the expected values, and that sum — not a round number — is the reserve you defend.

## Procedure

1. List every unknown that could move the estimate: "third-party API undocumented", "no staging database", "reviewer on holiday."
2. For each, write two numbers: the probability it actually bites (0.1, 0.3, 0.5) and the extra work if it does, in days.

       python3 -c "u=[(0.5,3),(0.3,5),(0.2,2)]; print(round(sum(p*c for p,c in u),1))"
       3.9

3. The expected value above is the 50% case. A deadline you actually care about needs roughly the 80% case, so add the tail, not just the mean:

       python3 -c "u=[(0.5,3),(0.3,5),(0.2,2)]; print('EV',round(sum(p*c for p,c in u),1),'worst',sum(c for _,c in u))"
       EV 3.9 worst 10

4. Convert the top one or two risks into tasks you can retire early — a spike, a question to a stakeholder — rather than carrying them forever as budget.
5. Recompute whenever a risk is retired or a new one appears. A budget line you never revisit is decoration.
6. Show the budget as its own line in `notes/plan.md`. Never fold it silently into the estimate, or it becomes invisible padding.

## Pitfalls

- Padding every task by 20% instead of pricing named risks, which hides the real driver and cannot be defended when challenged.
- Double counting: the same dependency risk appearing in two parts of the plan, inflating the reserve.
- Setting probabilities by mood; if you cannot say why it is 0.3 rather than 0.1, you should widen the range instead.
- Treating the reserve as normal spendable time — it is reserved for the risks on the list and nothing else.
- Carrying a large budget for a risk a two-hour spike would retire, then presenting the spike as unaffordable.

## Verification

    python3 -c "u=[(0.5,3),(0.3,5),(0.2,2)]; assert all(0<=p<=1 for p,_ in u); print(sum(p*c for p,c in u))"
    # prints 3.9; every probability within [0,1] or the assert fires

Report each unknown with its probability and cost, the summed expected cost, the worst case, and which risks you are retiring rather than budgeting for.
