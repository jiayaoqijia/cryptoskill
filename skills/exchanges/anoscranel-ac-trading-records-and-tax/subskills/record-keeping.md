---
name: record-keeping
domain: investing/record-keeping
trigger: "Recording each trade with the fields that make it usable at tax time."
anti_trigger: "Not for computing tax, and not for trading decisions."
scope: "What to record per trade, and the fields that make a record usable a year later."
status: seedling
---

# Record keeping

## Standard

A trade record is usable if a stranger can reconstruct the transaction from it without asking a question. That requires more fields than most traders keep: the venue, the instrument identifier, the side, the quantity, the price, the fees separately, the timestamp with timezone, the order identifier, and the settlement or transfer reference where one exists.

The test is temporal. A record written for today's dashboard is not a record; it is a view. The record must survive the venue's interface changing, the position closing, and the account being closed. Export the raw data at the time of the trade, store it outside the venue, and keep the export format documented so a later reader can parse it.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Every trade record carries the ten fields: venue, instrument, side, quantity, price, fee, timestamp with timezone, currency, order identifier, and transfer reference where applicable.
- Fees are recorded separately from price, never netted silently.
- Raw exports are stored outside the venue, with the export date and format version.
- Transfers between accounts are recorded as transfers, not as sales.
- A record is immutable once written; corrections are appended with a reason and a date.
- Records are backed up to a second medium on a stated schedule.

## Procedure

1. Configure the export before the first trade; do not rely on interfaces.
2. Store the raw export with a date-stamped filename and a checksum.
3. Normalise into a table with the ten fields, keeping the raw file untouched.
4. Record transfers separately, with both sides identified.
5. Append corrections rather than editing.
6. Test the record by reconstructing one trade from scratch.

## Anti-patterns

- Screenshotting a dashboard as the record.
- Netting fees into price and losing the fee line.
- Keeping the only copy inside the venue's interface.
- Recording transfers as sales.
- Editing a record after a reconciliation.

## Done checklist

- [ ] Export configured before the first trade.
- [ ] Raw files stored with dates and checksums.
- [ ] Normalised table with the ten fields.
- [ ] Transfers recorded separately with both sides.
- [ ] Corrections appended, not edited.
- [ ] One trade reconstructed as a test.

## Sources

- Tax administration guidance on record keeping: <https://www.irs.gov/>
- Investor education on records and disclosure: <https://www.investor.gov/introduction-investing>
- Regulatory context for transaction reporting: <https://www.sec.gov/investor>
