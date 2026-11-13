---
name: reps-warranties-indemnities
domain: investing/reps-warranties-indemnities
trigger: "Reading the representations, warranties, and indemnification architecture of a deal."
anti_trigger: "Not for legal advice, and not for the deal negotiation itself."
scope: "Allocating risk backwards in time with contractual statements."
status: seedling
---

# Representations, warranties, and indemnities

## Standard

Representations and warranties are the seller's statements about the state of the company as of signing and again at closing — about its financials, assets, litigation, contracts, tax, employees, and compliance. Their function is risk allocation backwards in time: the buyer pays the agreed price on the strength of those statements, and if a statement is untrue, the indemnification provisions decide who pays for the discrepancy.

The architecture has three dials. Scope decides what must be true. Qualification decides how true it must be — knowledge qualifiers and materiality thresholds narrow broad statements. Remedies decide what happens when a statement fails: who indemnifies whom, up to what cap, after what deductible, surviving for how long, and under what procedure. Reading a deal's risk transfer means reading all three dials together, because a broad-sounding warranty heavily qualified by knowledge qualifiers transfers far less risk than its words suggest.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.law.cornell.edu/>.

## Decision rules

- Inventory the representation categories and note which are qualified by knowledge, materiality, or both.
- Record the indemnification structure: cap, deductible (de minimis and basket), survival period, and any special carve-outs outside the cap.
- Identify fundamental representations to which the general cap and survival do not apply.
- Note the indemnification procedure, including claim deadlines and third-party claim conduct.
- Record any representation and warranty insurance and what it shifts.
- Flag vague qualifiers ("to the knowledge of the seller") without identifying whose knowledge and how it was formed.

## Procedure

1. Read the representation sections and classify each by category and qualification.
2. Record the indemnity terms: cap, baskets, survival, procedure.
3. Identify fundamental reps and their separate treatment.
4. Note rep and warranty insurance if present and its exclusions.
5. Map each major risk area to the rep covering it and to its remedy.
6. Write the risk-allocation summary with the three dials stated per area.

## Anti-patterns

- Reading warranty words without their qualifiers.
- Assuming the cap applies to fundamental representations.
- Accepting "knowledge" qualifiers without asking whose knowledge.
- Treating survival periods as uniform across reps.
- Overlooking insurance exclusions that return risk to the seller.

## Done checklist

- [ ] Rep categories and qualifiers inventoried.
- [ ] Indemnity cap, baskets, and survival recorded.
- [ ] Fundamental reps identified with separate treatment.
- [ ] Indemnification procedure recorded.
- [ ] Insurance terms and exclusions noted.
- [ ] Risk map written with the three dials visible.

## Sources

- Merger agreement disclosure with rep schedules: <https://www.sec.gov/edgar/search/>
- Statutory and case reference: <https://www.law.cornell.edu/>
- Investor education on deal documents: <https://www.investor.gov/introduction-investing>
