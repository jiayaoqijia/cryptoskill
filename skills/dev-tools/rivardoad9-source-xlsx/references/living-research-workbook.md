# Living research workbook

Blueprint for a market-research workbook that gets updated over days, plus the Drive sync that keeps one stable link.

## Sheet blueprint

| Sheet | Content |
|---|---|
| Ringkasan | The 5 research questions with one-line answers, 6 KPI cells driven by formulas, and a "cara pakai" note |
| Riset Studio / Riset Target | One row per target: name, area, contact, date, status, mandatory?, sells on site?, brands, price min, price max, own label?, source, note |
| Benchmark Harga | One row per SKU with price, price tier, source. Statistics (MIN/MEDIAN/AVERAGE/MAX/COUNT) plus a bar chart |
| Supply | Factory quote inputs in highlighted cells — unit price, MOQ, sample fee, tooling/screen cost, lead time, payment terms — then a `<b>total keluar sebelum ada barang jadi</b>` formula, then a margin scenario table (wholesale / retail / D2C) with laba kotor and margin % formulas |
| Vendor Pabrik | Aspect-by-aspect comparison (legalitas, berdiri, kapasitas, MOQ, harga, bahan, bukti sosial, risiko) plus a pre-transfer checklist |
| Pasar | Supply and demand context, clearly labelled as external data, not target data |
| Rencana Aksi | Ordered steps with a status dropdown (Belum mulai / Jalan / Selesai / Dibatalkan) and conditional colouring |
| Template & Skrip | Every outreach and follow-up script actually used, plus the rules of engagement |

Rules that keep it compounding:

- Raw observation goes in the row; anything inferred goes in as `perlu konfirmasi`.
- Formulas reference wide ranges (e.g. `D6:D40`) so rows can be appended without editing formulas.
- Statistics and charts must be regenerated from the actual row count at build time, not a hardcoded range, or appended rows silently drop out of the chart.
- Numbers stay numeric with a `"Rp"#,##0` format; never pre-format prices as text.
- A quote sheet must answer "how much cash leaves before anything is sellable", not just "unit price": sample fee, tooling/screen, shipping and packaging, summed by formula. A sample fee credited against the down payment later is still cash out now and is forfeited on cancellation, so show it as money already spent.
- Keep the break-even quantity as a formula (fixed costs ÷ margin per unit), so it moves the moment a supplier changes the price.

## Stable-link Drive sync

Rebuilding the file is fine. Recreating the Drive file is not: every `files().create()` returns a new id and the link the user saved breaks.

- Convert on write so the user can edit from the phone: create with `body={"mimeType": "application/vnd.google-apps.spreadsheet"}` and the xlsx as media.
- On later runs use `files().update(fileId=PINNED_ID, media_body=media)`.
- Pin the id in the script as a constant, with a fallback `create` only inside an exception handler that prints a loud warning with the new id.
- Never `delete`-then-`create` "to avoid duplicates" - that is exactly what changes the link.
- Verify after every sync: read back a range through the Sheets API and assert the headline numbers, not just that the call returned 200.
