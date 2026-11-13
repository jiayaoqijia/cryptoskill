---
name: order-lifecycle
domain: investing/order-lifecycle
trigger: "Tracing an institutional order from execution to affirmation."
anti_trigger: "Not for order placement tactics, and not for legal advice."
scope: "Execution, allocation, confirmation, affirmation, and where the chain breaks."
status: seedling
---

# Order lifecycle

## Standard

An execution becomes a settled position through a sequence. The order is executed by a broker, then allocated: the single execution is split across the accounts that will hold it, with quantities and average prices assigned. Each allocation is confirmed by the broker and affirmed by the client, and only then does it become a settlement obligation. A break at any of those stages delays everything downstream.

The stages that most often break are allocation and affirmation. An allocation that does not match the executing broker's record produces a mismatch that has to be resolved before settlement, and an affirmation that misses its deadline moves the trade to a different settlement date. Both are administrative, and both consume the time that settlement needs, which is why operations teams treat them as risk rather than paperwork.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the execution details: venue, time, quantity, price, and counterparty.
- Record the allocation: accounts, quantities, and average price method.
- Record confirmation and affirmation deadlines with the timezone stated.
- Record which entity is responsible for each stage.
- Record the break resolution path and who owns it.
- Record the resulting settlement date and any change caused by a break.

## Procedure

1. Record the execution and its identifiers.
2. Record the allocation instructions and method.
3. Record confirmation and affirmation status with times.
4. Assign ownership for each stage.
5. Record any break, its cause, and its resolution.
6. Record the resulting settlement date.

## Anti-patterns

- Treating an allocation as a formality.
- Missing an affirmation deadline without escalating.
- Assuming the executing broker's record matches the client's.
- Losing the link between the execution and its allocations.
- Allowing a break to sit without an owner.

## Done checklist

- [ ] Execution details recorded.
- [ ] Allocation recorded.
- [ ] Confirmation and affirmation times recorded.
- [ ] Ownership assigned per stage.
- [ ] Breaks recorded with cause.
- [ ] Settlement date recorded.

The identifier discipline is what makes the rest possible: a unique reference that persists from execution through allocation, confirmation, and settlement is the only way to trace a break backwards to its cause, and a chain that relies on matching by quantity and price will produce ambiguities whenever two trades share both.


## Sources

- Settlement and market infrastructure standards: <https://www.bis.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on trade settlement: <https://www.investor.gov/introduction-investing>
