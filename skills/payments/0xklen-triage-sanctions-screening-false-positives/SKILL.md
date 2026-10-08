---
name: triage-sanctions-screening-false-positives
description: Use when an automated screen returns matches that need clearing or escalating, and you must disambiguate by identity data rather than by name similarity alone.
---

# Triage a sanctions screening alert

An alert is a hypothesis, not a finding. The job is to accumulate enough independent identity data
to say "different person" or "cannot rule out", and to leave a disposition that a reviewer can
reproduce months later.

## Procedure

1. Pull the full listed record, not the name. Copy the whole row so you can compare field by
   field:

       grep -i "$SUBJECT" sdn_advanced.xml | head -40
       jq -r '.entities[]|select(.name|test("ACME";"i"))' consolidated.json

2. Compare on discriminating fields, in this order of weight: date of birth, unique ID / passport,
   country of residence, city, and known aliases. A match on name and country of birth with a
   different year is a different person more often than not; a match on name and passport number
   is a hit.

3. Score the overlap explicitly and put the number in the ticket so the reasoning is reviewable:

       python3 - <<'PY'
       weights = {"dob": 0.35, "passport": 0.40, "country": 0.10, "city": 0.15}
       overlap = {"dob": 0, "passport": 0, "country": 1, "city": 0}
       print(round(sum(weights[k]*v for k, v in overlap.items()), 2))  # 0.10
       PY

4. For wallet addresses there is no fuzzy tier. Either the normalised address equals the listed
   address or it does not; a hex string that differs in one character is not a near miss, it is a
   vanity-address lookalike and a red flag in its own right.

5. Record one disposition per alert: `true match`, `false positive`, `insufficient information`.
   Follow the same script for every alert of the same rule so decisions are consistent.

6. Escalate `true match` and `insufficient information` to the compliance owner. Clear
   `false positive` only with the disambiguating fields written down; a cleared alert with no
   evidence is worse than an open one.

## Pitfalls

- Clearing on name spelling alone. Transliteration variance (Mohamed / Muhammad) means a spelling
  difference neither proves nor disproves a match.
- Clearing because the amount is small. Sanctions are not threshold-based; a $5 transfer to a
  designated address is still a prohibited dealing.
- Auto-clearing on a vendor score below some cut-off without a human disposition. Regulators
  expect the reasoning, not the score.
- Letting alert backlog rot. An unworked alert queue is itself a finding in an examination;
  track ageing and escalate anything open beyond the internal SLA.
- Re-using another customer's disposition because the names look the same; each alert is a
  separate identity comparison.

## Verification

    grep -c "disposition=false_positive" alerts-closed.csv
    awk -F, '$3=="false_positive" && $5=="" {print "unjustified", $1}' alerts-closed.csv

The second command must print nothing — every cleared alert must carry the fields that
distinguished it from the listed party.

Report the count opened, closed by disposition, and the oldest open alert with its age. The
determination that a person is or is not designated is a compliance decision reserved to a
qualified officer and, where contested, counsel — not to the screening tool.
