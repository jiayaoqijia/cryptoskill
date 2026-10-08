---
name: map-licensing-exposure-by-jurisdiction
description: Use when a crypto product must ship in a new country or a feature change may move it into a regulated activity, and you need to chart which licences or registrations the activity actually triggers.
---

# Map licensing exposure by jurisdiction

Licensing follows the activity and the customer's location, not the entity's incorporation. A
feature that looks like software can be money transmission in one country and unregulated in the
next, so the mapping has to be done per activity, per country, on paper.

## Procedure

1. Decompose the product into activities before touching jurisdictions. Typical axes: custody of
   customer keys, fiat on/off ramp, spot exchange between two assets, lending, staking-as-a-
   service, and order routing. Each maps to a different regulatory hook.

2. For each activity, list the countries where the customer (not the server) sits, and mark the
   trigger:

```
       cat > exposure.csv <<'CSV'
       activity,country,regime,hook,needed
       custody,US,BSA/MSB,state money transmission,register+MTL
       spot_exchange,EU,MiCA,crypto-asset service provider,CASP licence
       fiat_ramp,UK,FCA MLR,registered cryptoasset business,MLR registration
       custody,SG,PSA 2019,digital payment token service,DPT licence
       CSV
```

3. Apply the activity test rather than the label. Ask the blunt questions: do we ever hold or
   control customer funds or keys, do we ever take one side of a trade, do we have discretion
   over a customer's assets? A yes to any of these is a licensing trigger somewhere.

4. Check the offering restriction separately from the licence. Some countries allow the activity
   only with a licence, others prohibit it for retail regardless, and a few permit it for
   professionals only.

5. Record the effective date and the source for every row. Regimes change: a row without a
   citation and an as-of date is a guess dressed as a fact.

       grep -n ",," exposure.csv   # any empty field is an unresolved row

6. Route the sheet to counsel per jurisdiction. Keep the engineering work — the activity list and
   the country list — scoped to facts you can evidence.

## Pitfalls

- Assuming incorporation in a permissive jurisdiction covers the customers. Many regimes reach
  the activity where the customer is, or where the marketing is aimed.
- Treating non-custodial software as automatically outside all regimes; some regimes reach
  "arranging" or "making arrangements" without custody.
- Missing registration-only regimes because they lack the word "licence". A registration is still
  a permission to operate.
- Copying a competitor's posture as your answer; their licence scope, entity and customer base
  are not yours.
- Forgetting the marketing rule: an app in the local app store, a local-language site or local
  ads can establish the jurisdictional hook even with no local entity.

## Verification

    awk -F, 'NR>1 && NF!=5 {print "malformed row", FNR}' exposure.csv
    awk -F, 'NR>1 && ($4==""||$5=="") {print "unresolved", $2, $1}' exposure.csv

Both commands must print nothing for the sheet to be usable.

Report the activity-by-country grid with the regime, hook, required permission, and as-of date.
Interpreting whether a licence applies is a legal question: the final call must be made by
qualified local counsel, not by this mapping.
