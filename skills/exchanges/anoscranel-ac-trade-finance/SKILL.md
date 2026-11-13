---
name: ac-trade-finance
description: "The financing layer beneath physical commodity trade: letters of credit and documentary collections, warehouse receipts and bills of lading as title documents, pre-payment and prepay structures, inventory and receivables finance, counterparty and performance risk in a documentary sale, the fraud patterns that recur, and the written trade-finance record. It explains the instruments and the risk; it never recommends a transaction and never gives legal advice. Use when asking \"letter of credit\", \"documentary collection\", \"bill of lading\", \"warehouse receipt\", \"prepayment\", \"trade finance\", \"inventory finance\", \"who bears the risk in this shipment\", \"double financing\". Not for commodity price and curve mechanics (ac-commodities-trading), not for borrower credit analysis (ac-bank-and-credit-analysis), not for shipping and freight operations (ac-institutional-operations)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Trade finance

## Overview

Physical commodity trade is financed at every step: the buyer's payment obligation, the seller's performance obligation, the goods in transit, and the inventory in a warehouse are each a claim that someone funds. The instruments that carry those claims — letters of credit, documentary collections, bills of lading, warehouse receipts — are what determine who bears the risk at each point.

This skill covers the instruments and the risks they allocate. A documentary sale is a sequence in which title, payment, and possession move at different times and through different parties, and the gaps between them are where losses occur. The recurring fraud patterns exploit exactly those gaps, which is why they are recorded here as mechanics rather than as anecdotes.

Primary sources: <https://www.icc-ccs.org/> and <https://www.bis.org/>.

## When to use

- When a physical trade's payment or performance risk needs allocating.
- When a letter of credit, collection, or receipt is part of a transaction.
- When inventory or receivables are being financed against goods.
- When a transaction's terms allow the same goods to secure more than one claim.

## When NOT to use

- For commodity prices, curves, and roll mechanics (use ac-commodities-trading).
- For assessing a borrower's ability to repay (use ac-bank-and-credit-analysis).
- For shipping operations and freight (use ac-institutional-operations).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/letters-of-credit.md` | `investing/letters-of-credit` | The instrument, its documents, and the discrepancies that stop payment. |
| `subskills/documentary-collections.md` | `investing/documentary-collections` | Collections, documents against payment, and the risk left with the seller. |
| `subskills/title-documents.md` | `investing/title-documents` | Bills of lading and warehouse receipts as documents of title. |
| `subskills/prepayment-structures.md` | `investing/prepayment-structures` | Prepay, offtake-backed advances, and the performance risk they carry. |
| `subskills/inventory-and-receivables-finance.md` | `investing/inventory-and-receivables-finance` | Borrowing against goods and invoices, and the control that makes it work. |
| `subskills/trade-finance-fraud.md` | `investing/trade-finance-fraud` | Double financing, fictitious cargo, and the patterns that recur. |
| `subskills/trade-finance-record.md` | `investing/trade-finance-record` | The written record: instruments, control, and residual exposure. |

## Status and honest limits

Trade finance relies on documents, and documents can be forged, duplicated, or issued against cargo that does not exist. Verification depends on parties whose incentives are not always aligned with the financier's, and the legal treatment of title varies by jurisdiction and by convention. Nothing here recommends a transaction, and a facility secured on goods without independent verification of those goods is a facility secured on a document.
