---
name: export-controls
domain: investing/export-controls
trigger: "Tracing how an export control reaches a company's revenue or cost."
anti_trigger: "Not for legal advice, and not for predicting control decisions."
scope: "Control lists, licence requirements, and the supplier chain they reach."
status: seedling
---

# Export controls

## Standard

Export controls restrict the transfer of specified items, software, and technology to specified destinations or users. They operate through lists: a list of controlled items, classified by technical parameters, and lists of restricted end users and destinations. A licence is required when an item meets a parameter and the destination or user is restricted, and the absence of a licence makes the sale unlawful rather than merely unprofitable.

For an investor the reach is often second-order. A company may not export to a restricted party at all, but its customer may, and its supplier may be unable to supply the component that the company's product depends on. Tracing the chain means asking which inputs are controlled, which suppliers are exposed to a restriction, and whether the company's own products meet a controlled parameter.

Primary sources: <https://www.bis.org/> and <https://www.wto.org/>.

## Decision rules

- Record the control regime and the list version in force.
- Record which of the company's inputs or products meet a listed parameter.
- Record which destinations and end users are restricted for those items.
- Record the revenue exposed to a licence requirement, if disclosed.
- Record the supplier concentration on controlled components.
- Record the compliance programme and whether it is described in filings.

## Procedure

1. Identify the applicable regimes and list versions.
2. Map the product range against controlled parameters.
3. Record the destinations and users affected.
4. Estimate revenue or cost exposed.
5. Record supplier dependence on controlled inputs.
6. Write the control summary with the chain traced.

## Anti-patterns

- Treating controls as a sales restriction rather than an input restriction.
- Ignoring the technical parameters and reasoning from the product's name.
- Assuming a licence will be granted because one was granted before.
- Overlooking the supplier's exposure as a separate risk.
- Reading the list version at a date other than the transaction's.

## Done checklist

- [ ] Regime and list version recorded.
- [ ] Products mapped to parameters.
- [ ] Destinations and users recorded.
- [ ] Revenue exposure estimated.
- [ ] Supplier dependence recorded.
- [ ] Chain traced in the summary.

The practical distinction is between an item that is listed and an item that is not yet listed: controls are updated as technology develops, and a product that sits just below a technical parameter today can be brought inside the list by a revision, which means the exposure should be assessed against the direction of the parameters rather than only their current values.

## Sources

- Export control and security standards: <https://www.bis.org/>
- Trade policy information: <https://www.wto.org/>
- Company disclosure of compliance matters: <https://www.sec.gov/investor>
