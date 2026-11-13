---
name: settlement-and-clearing
domain: investing/settlement-and-clearing
trigger: "Understanding when a trade becomes final and who stands in the middle."
anti_trigger: "Not for cash management advice, and not for tax timing."
scope: "Settlement cycles, clearing, fails to deliver, and the counterparty in the middle."
status: seedling
---

# Settlement and clearing

## Standard

A trade is an agreement; settlement is when the securities and cash actually move. In between stands a clearinghouse that becomes the buyer to every seller and the seller to every buyer, which is what makes the market's counterparty risk manageable. The settlement cycle sets when the cash arrives and when the shares are truly yours.

Fails to deliver happen when the seller does not deliver on time. They are recorded, published, and usually resolved, but they matter to anyone whose plan assumes shares or cash are available on a specific date. The mechanics are mundane and the consequences are not: a plan that assumes same-day availability of proceeds is built on a rule that does not exist.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the settlement cycle applicable to the instrument and venue.
- Record the clearinghouse and the margin the broker requires in between.
- Any plan that depends on proceeds records the settlement date, not the trade date.
- Fails to deliver are recorded where they affect an obligation.
- The counterparty chain — broker, clearing member, clearinghouse — is recorded for large exposures.
- Settlement changes are treated as rule changes and verified before relying on them.

## Procedure

1. Identify the settlement cycle for the instrument.
2. Record the trade date and the settlement date.
3. Record the broker's settlement-related margin or hold.
4. Track any fail to deliver against obligations.
5. Record the counterparty chain for material exposures.
6. Verify current rules before relying on a date.

## Anti-patterns

- Assuming proceeds are available on trade date.
- Ignoring the broker's hold on unsettled proceeds.
- Treating a fail to deliver as the buyer's problem alone.
- Assuming the settlement cycle from memory after a rule change.
- Ignoring the clearing member in the counterparty chain.

## Done checklist

- [ ] Settlement cycle recorded.
- [ ] Trade and settlement dates recorded.
- [ ] Broker holds recorded.
- [ ] Fails tracked against obligations.
- [ ] Counterparty chain recorded for material exposures.
- [ ] Current rules verified.

## Sources

- Regulatory context for settlement and clearing: <https://www.sec.gov/investor>
- Investor education on trade settlement: <https://www.investor.gov/introduction-investing>
- Rule context for clearing requirements: <https://www.finra.org/rules-guidance>

The gap between trade date and settlement date is where cash-flow plans break. Any obligation that assumes the proceeds of a sale are available before settlement is an obligation built on a timing assumption, and the record should carry the date rather than the assumption.
