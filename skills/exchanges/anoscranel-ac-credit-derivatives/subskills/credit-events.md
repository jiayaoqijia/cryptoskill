---
name: credit-events
domain: investing/credit-events
trigger: "Handling a credit event and the settlement that follows."
anti_trigger: "Not for legal advice, and not for predicting a default."
scope: "Default, restructuring, and the auction that settles protection."
status: seedling
---

# Credit events

## Standard

A credit default swap pays out when a defined credit event occurs, and the definition is in the documentation rather than in the news. Bankruptcy and failure to pay are the clearest events; restructuring is the contested one, because its inclusion and its terms determine whether a distressed exchange counts. A trader who has not read which restructuring clause applies does not know what the position protects against.

Settlement follows an event through a process rather than a single payment. The determination committee decides whether an event occurred, an auction establishes the recovery price, and protection settles against that price. The timing matters: a position held into the event has its economics fixed by the auction, and the difference between the auction price and the eventual workout value is not the protection buyer's to capture.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the credit events covered and the restructuring clause in force.
- Record the determination process and who sits on the committee.
- Record the settlement method: auction, cash, or physical.
- Record the deliverable obligations and any constraints on delivery.
- Record the position's exposure to the event in currency at a stated recovery.
- Record the timeline from event to settlement that comparable cases took.

## Procedure

1. Read the event definitions applicable to the contract.
2. Record the restructuring terms.
3. Record the settlement mechanics and the auction process.
4. Compute the position's payout at a range of recovery values.
5. Record the deliverable set and its constraints.
6. Write the event scenario with its timeline.

## Anti-patterns

- Assuming every default is an event under the contract.
- Ignoring the restructuring clause's effect.
- Treating the auction price as the ultimate recovery.
- Holding a position into an event without the deliverable obligation in hand.
- Sizing on an assumed recovery without a range.

## Done checklist

- [ ] Event definitions recorded.
- [ ] Restructuring terms recorded.
- [ ] Settlement mechanics recorded.
- [ ] Payout computed across recoveries.
- [ ] Deliverables and constraints recorded.
- [ ] Timeline written.

The determination process is also the reason two observers can disagree in good faith: a committee applying the standard definitions may reach a different conclusion from a market participant reading the news, and the record should distinguish the contractual question from the analytical one rather than merging them.

## Sources

- Credit event definitions and auction process: <https://www.isda.org/>
- Regulatory context for credit markets: <https://www.federalreserve.gov/>
- Investor education on credit risk: <https://www.investor.gov/introduction-investing>
