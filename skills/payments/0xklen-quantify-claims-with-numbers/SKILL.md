---
name: quantify-claims-with-numbers
description: Use when a report leans on adjectives like fast, many, or significant. Replace each vague quantity with a measured number, a unit, and a comparison baseline.
---

# Quantify claims with numbers

"Much faster" is a marketing claim; "180ms p95, down from 240ms" is a finding. Numbers with units and a baseline let the reader check you instead of trusting you.

## Procedure

1. Flag every scale adjective in the draft: fast, slow, large, many, most, significant, rarely.

2. Replace each with a number and a unit: `p95 latency 180ms`, not `fast`.

3. Give a baseline: "180ms versus 240ms before". A number alone tells the reader nothing.

4. State the measurement method so the number is reproducible: `hyperfine --runs 10 './before' './after'`.

5. Round honestly: "about 180ms" unless the difference itself is the finding.

6. Convert vague fractions to counts: "9 of 10 requests" rather than "most".

7. If you have no measurement, write `unmeasured` rather than implying one.

## Pitfalls

- "Significantly faster" with no test is a slogan, not a report.
- A number with no baseline invites the reader to invent one.
- A percentage without its denominator misleads; always show both.
- Precision you never measured ("cut by 37.2%") is fabricated confidence.
- Mixing MB with MiB, or ms with µs, inflates or deflates silently.

## Verification

    hyperfine --runs 10 './before' './after'   # both numbers, same harness, same machine

Give every scale claim a number, a unit, and a baseline; drop adjectives you cannot measure.
