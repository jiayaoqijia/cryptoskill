---
name: set-travel-rule-thresholds-by-jurisdiction
description: Use when configuring an amount threshold for when counterparty data must be collected and transmitted, because the trigger differs by jurisdiction and the sender and receiver regimes are often different.
---

# Set travel-rule thresholds per jurisdiction

The amount at which originator and beneficiary data must accompany a transfer is not global. A
single product-wide threshold will either break a stricter regime or collect data you have no
lawful basis for in a looser one. Configure per corridor, and record the basis for each number.

## Procedure

1. Enumerate the regimes that actually touch the flow: the sender's regulator, the receiver's
   regulator, and any intermediary VASP's. The applicable rule is the strictest one in the path.

2. Map each corridor to its trigger and encode it as data, not as an `if` scattered through the
   transfer code:

       cat > thresholds.yaml <<'YAML'
       default: { amount_floor_usd: 0, data_required: true }
       corridors:
         EU_TO_EU:      { amount_floor_usd: 0,    basis: "TFR 2023/1113, CASP-to-CASP" }
         US_TO_US:      { amount_floor_usd: 3000, basis: "BSA 31 CFR 1010.410(e)" }
         CH_DOMESTIC:   { amount_floor_usd: 1000, basis: "AMLO-FINMA, CHF equivalent" }
         FATF_BASELINE:{ amount_floor_usd: 1000, basis: "FATF R.16 interpretive note" }
       YAML

3. Convert the fiat floor to the chain's native unit at the rate used for the ledger entry, and
   store the rate and its timestamp next to the trigger decision. A $3,000 floor evaluated with
   yesterday's ETH price is an arbitrary threshold.

       python3 -c 'p=3000; eth=3420.15; print(f"{p/eth:.6f} ETH")'

4. Decide the fail-safe direction. When the corridor is unknown or the peer's jurisdiction cannot
   be resolved, apply the zero floor (collect and transmit). Under-collecting is a reporting
   failure; over-collecting is a privacy cost, and the asymmetry favours collecting.

5. Version the file and gate deploys on it. A corridor rule change is a compliance change and
   should be reviewed like one, with the effective date recorded.

6. Re-derive thresholds when a corridor's rules change; keep the previous file so a historical
   transfer can be judged against the rules in force on its date.

## Pitfalls

- Hard-coding one number from a blog summary. The FATF baseline figure and the EU's zero floor
  are both real and both commonly confused.
- Applying the floor to the aggregate rather than to each transfer, letting many sub-threshold
  sends slip under it — structuring is a red flag regardless of the threshold.
- Ignoring the OCR/aggregation rule that some regimes apply: linked transfers that together
  exceed the floor can pull in the earlier ones.
- Treating the threshold as the point at which KYC starts. Customer due diligence applies at
  onboarding, not at the travel-rule amount.
- Forgetting that the receiving VASP's regime governs what it must accept; a compliant sender can
  still be sending to a peer that is breaching its own rules.

## Verification

    python3 -c 'import yaml;d=yaml.safe_load(open("thresholds.yaml"));
    assert all(c.get("basis") for c in d["corridors"].values());print("bases present")'
    grep -n "amount_floor_usd" thresholds.yaml

Every corridor must carry a written `basis`; a corridor with a number and no citation fails
review.

Report the corridor, the floor applied, the basis citation, and the conversion used. Choosing the
governing rule for a given flow is a legal determination — a qualified compliance officer or
counsel makes that call.
