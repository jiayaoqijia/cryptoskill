---
name: proration-and-metering
domain: software-engineering/proration-and-metering
trigger: "Changes mid-period and usage-priced charges computed as shown arithmetic."
anti_trigger: "Not for pricing strategy, and not for tax computation."
scope: "Prorate as arithmetic you can show; metering as an aggregation pipeline."
status: seedling
---

# Proration and metering

## Standard

Proration is charging for a fraction of a period, and its honesty lives in showing the arithmetic. A mid-period upgrade, a downgrade, a cancellation with refund of unused time: each produces credit and debit amounts that the customer should be able to reconstruct from presented facts — period length, fraction remaining, the two rates — and a merchant who cannot produce the arithmetic has a support burden, not an engineering feature. The discipline is: proration results are records of a computed decision, stored with their inputs, not just their outputs.

Metered billing is the same honesty under aggregation. Everything hangs on the ingestion pipeline that turns raw usage events into billable quantities: the events are recorded with identity and time, aggregation is defined over a window and a key, late events have a declared policy, and the invoice line item is derived data that can be traced back to the events that composed it. Without that traceability, bills become unverifiable assertions that the customer disputes product by product rather than as a matter of total.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://docs.stripe.com/payments/3d-secure>.

## Decision rules

- Store proration decisions with their inputs (period, fraction, rates), not just the resulting amount.
- Rate changes take effect at boundaries defined in advance; applying a new rate to a past window without a recorded rate version is forbidden.
- Metering events: each has a stable identity; ingestion is idempotent; late arrival has a declared policy with a cutoff.
- Aggregation window and key are explicit data; any exception is a new explicit rule, not a case-bycase improvisation.
- Invoice lines derived from metering are traceable to their aggregate and its underlying events.
- Unit rounding policy is stated and consistent with the money-representation rules elsewhere in the system.

## Procedure

1. Model the proration decision as data: period boundaries, change date, old and new plans, computed credits and debits.
2. Present the raw arithmetic on the invoice line as facts; state how the fraction is derived.
3. Record rate versions with their effective windows; never compute a bill against a rate you cannot name as of the billing moment.
4. Pipeline the usage events through idempotent ingestion with event identity.
5. Aggregate by window and key, and make the invoice line show the aggregate it derived from.
6. Test the paths: late event, tampered event, changed plan mid-window.

## Anti-patterns

- A prorated amount decoded months later from a single number with its inputs discarded.
- Rates without effective windows; past periods re-rated silently.
- Metering aggregation that silently swallows late events without a recorded exception.
- Invoice lines with no derivation path to the events they tax.
- Rounding rules that differ between the proration computation and the invoice line.

## Done checklist

- [ ] Proration records stored with inputs.
- [ ] Fraction derivation shown on the invoice.
- [ ] Rate versions with effective windows.
- [ ] Idempotent usage-event ingestion.
- [ ] Invoice lines traceable to their aggregates and events.
- [ ] Late-arrival policy declared and tested.

## Sources

- Billing subscriptions overview: <https://docs.stripe.com/billing/subscriptions/overview>
- 3-D Secure authentication: <https://docs.stripe.com/payments/3d-secure>
- PCI standards library: <https://www.pcisecuritystandards.org/document_library/>
