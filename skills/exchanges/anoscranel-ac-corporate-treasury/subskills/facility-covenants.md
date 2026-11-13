---
name: facility-covenants
domain: investing/facility-covenants
trigger: "Reading a loan facility's covenant package and the headroom it leaves."
anti_trigger: "Not for legal advice, and not for predicting a breach."
scope: "Maintenance and incurrence tests, and the headroom they leave."
status: seedling
---

# Facility covenants

## Standard

Covenants come in two kinds and they constrain differently. A maintenance covenant is tested every period against a financial ratio, so a deterioration in the business can breach it without any action by the company. An incurrence covenant is tested only when the company wants to do something — raise debt, pay a dividend, make an acquisition — so it constrains behaviour rather than performance.

The headroom on the maintenance tests is the number that matters for credit. It is computed by taking the ratio's current level against its threshold and converting the gap into the amount of EBITDA decline or debt increase that would breach it. That conversion is what turns a covenant schedule into a statement about how much adversity the capital structure can absorb before the lender gains control.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## Decision rules

- Record each maintenance covenant with its definition, threshold, and test frequency.
- Record each incurrence covenant and the action it governs.
- Record the current level against each threshold and the headroom in the ratio's units.
- Convert the headroom into an EBITDA decline or a debt increase.
- Record equity cure rights, which allow a breach to be remedied by injection.
- Record cross-default provisions, which can accelerate one facility on another's breach.

## Procedure

1. Read the credit agreement's covenant section.
2. Record each covenant with its definition and threshold.
3. Record the current level and compute headroom.
4. Convert headroom into an EBITDA or debt change.
5. Record cure rights and their limits.
6. Record cross-default and write the assessment.

## Anti-patterns

- Reading the covenant threshold without its definition, which often adjusts EBITDA.
- Treating an incurrence covenant as a performance test.
- Ignoring equity cure rights, which change the breach path.
- Overlooking cross-default, which links facilities that look independent.
- Computing headroom without the definitional adjustments the agreement permits.

## Done checklist

- [ ] Maintenance covenants recorded with definitions.
- [ ] Incurrence covenants recorded.
- [ ] Headroom computed per covenant.
- [ ] Headroom converted into a business change.
- [ ] Cure rights recorded.
- [ ] Cross-default recorded.

The definition section deserves more attention than the threshold: a leverage covenant measured on adjusted EBITDA that permits add-backs for restructuring, acquisitions, and compensation can show comfortable headroom on a ratio that has drifted, and the add-backs themselves are a statement about how much the lender expected the number to be adjusted.


## Sources

- Facility and covenant disclosure: <https://www.sec.gov/investor>
- Credit market context: <https://www.federalreserve.gov/>
- Investor education on credit agreements: <https://www.investor.gov/introduction-investing>
