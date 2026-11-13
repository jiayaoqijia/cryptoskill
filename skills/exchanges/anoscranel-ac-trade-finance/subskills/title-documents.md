---
name: title-documents
domain: investing/title-documents
trigger: "Reading a bill of lading or warehouse receipt as a document of title."
anti_trigger: "Not for legal advice, and not for freight operations."
scope: "Bills of lading and warehouse receipts as documents of title."
status: seedling
---

# Title documents

## Standard

A bill of lading does three things: it is a receipt for the goods, evidence of the contract of carriage, and — when issued to order — a document of title. That third function is what allows goods to be financed: the document stands in for the cargo, and whoever holds it can pledge it.

The warehouse receipt performs the same role for stored goods, and the same risk applies. A receipt issued by a warehouse that does not hold the goods, or that issues several receipts for one lot, is a document of title that entitles its holder to nothing. The verification of the issuer is therefore as important as the document's form.

Primary sources: <https://www.icc-ccs.org/> and <https://www.bis.org/>.

## Decision rules

- Record the bill's type: straight, order, or bearer, since only some are negotiable.
- Record the issuer and its standing, not only its name.
- Record the goods description and quantity against the inspection evidence.
- Record the discharge port and the consignee terms.
- Record whether the receipt is issued by the warehouse operator or by a third party.
- Record the independent verification available for the goods and the storage.

## Procedure

1. Record the document type and negotiability.
2. Record the issuer and its standing.
3. Record the goods and quantity.
4. Record the routing and consignee.
5. Record verification of storage where a receipt is used.
6. Write the title summary with the verification basis.

## Anti-patterns

- Assuming every bill of lading is negotiable.
- Accepting a receipt without verifying the warehouse.
- Ignoring a quantity that does not match the inspection.
- Treating the document's form as proof of the goods.
- Overlooking a consignee term that prevents endorsement.

## Done checklist

- [ ] Document type recorded.
- [ ] Issuer standing recorded.
- [ ] Goods and quantity recorded.
- [ ] Routing recorded.
- [ ] Verification recorded.
- [ ] Summary written.

The electronic equivalent deserves the same scrutiny as the paper: an electronic bill of lading is only a document of title if the platform's rules and the applicable law recognise it as one, and a system that records the transfer without conveying title leaves the financier holding a receipt rather than a claim on goods. Recording which legal regime the electronic document operates under is part of reading it.

## Sources

- Trade documentation standards: <https://www.icc-ccs.org/>
- Trade finance and collateral standards: <https://www.bis.org/>
- International trade guidance: <https://www.usa.gov/>
