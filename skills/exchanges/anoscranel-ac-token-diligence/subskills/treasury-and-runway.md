---
name: treasury-and-runway
domain: crypto-trading/treasury-and-runway
trigger: "Reading a protocol treasury and computing how long it survives without new buyers."
anti_trigger: "Not for valuing the token, and not for predicting revenue."
scope: "Protocol treasury, burn rate, fee revenue, and the runway arithmetic that says whether the thing survives without new buyers."
status: seedling
---

# Treasury and runway

## Standard

A protocol that pays its costs from a treasury is a business with a clock. The clock is runway: treasury value divided by net burn. Runway matters to a token holder because the treasury is usually denominated in the token itself, so the numerator falls when the token falls, and the spending accelerates the fall when it is sold. That feedback loop is the honest frame for treasury analysis.

Reported treasury figures are self-reported unless the holdings are verifiable on-chain. A treasury statement is evidence of what the issuer says it holds; a set of addresses is evidence of what it actually holds. Diligence records both and states which one the runway calculation used.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## Decision rules

- Record treasury composition by asset class, not as one number; a treasury that is ninety percent its own token is a different object from one that is stablecoins.
- Compute runway in months at current burn, and again with the token price down fifty percent. The second number is the one that matters.
- Separate protocol revenue from token emissions used to pay contributors; the first is income, the second is dilution.
- If treasury holdings are not verifiable on-chain, record the runway as self-reported and mark confidence low.
- A treasury that funds itself by selling the token is structurally short the token; state this plainly.
- Recompute after any material price move or spend announcement.

## Procedure

1. Collect treasury addresses and reported balances; reconcile the two where both exist.
2. Classify holdings: own token, stablecoins, other assets, illiquid positions.
3. Establish monthly burn from published spending or, failing that, from contributor payments visible on-chain.
4. Compute runway in months, twice: at current price and at half price, with arithmetic shown.
5. Identify revenue sources and whether they are denominated in the token or in other assets.
6. Record sources, dates, and which figures are self-reported.

## Anti-patterns

- Treating a treasury's headline dollar figure as available capital when most of it is the token itself.
- Counting token emissions as revenue.
- Assuming a treasury means solvency without checking the burn rate.
- Ignoring that treasury sales are themselves a supply event.
- Using a price from a different date than the holdings snapshot.

## Done checklist

- [ ] Treasury addresses and reported balances reconciled or discrepancies recorded.
- [ ] Composition by asset class stated with percentages.
- [ ] Monthly burn established with its basis.
- [ ] Runway computed at current and half price, arithmetic shown.
- [ ] Revenue versus emissions separated.
- [ ] Self-reported figures marked as such, with confidence.

## Sources

- Investor education on disclosure and financial statements: <https://www.investor.gov/introduction-investing>
- Securities regulation context for issuer disclosures: <https://www.sec.gov/investor>
- Ethereum token standards documentation: <https://ethereum.org/en/developers/docs/standards/tokens/>
