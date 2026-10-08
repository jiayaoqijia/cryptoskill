---
name: assess-chain-analytics-risk-scores
description: Use when a blockchain analytics vendor returns a risk score or exposure figure for an address, and you must decide what the number actually supports before acting on it.
---

# Read a chain-analytics risk score honestly

Vendor scores are heuristic labels, not determinations of fact. A "high risk" flag is a prompt to
do work; a "sanctioned" flag is a different kind of claim altogether, and conflating the two
produces both false freezes and missed designations.

## Procedure

1. Separate the claim types in the vendor response before reading the number:

       curl -s "https://public.chainalysis.com/api/v1/address/$ADDR" \
         -H "X-API-Key: $KEY" | jq '{identifications, risk, cluster}'

   `identifications` naming an actual sanctions programme is a designation claim; a bare
   categorical band is a heuristic. Only the first is a hard stop.

2. Measure exposure two ways: direct (the address transacted with a labelled entity) and indirect
   (value reached it through N hops). Indirect exposure falls off with hops and is the weakest
   signal; a 0.1% indirect exposure via five hops is noise.

       jq -r '.exposure[] | select(.category=="sanctions") | "\(.direct) direct / \(.indirect) indirect"'

3. Check the attribution behind the label. A cluster is often defined by a single deposit or a
   shared nonce; one analyst's guess becomes an "exchange" label propagated across the industry.

4. Look for hysteresis. If a score moved from 0.9 to 0.2 with no new on-chain facts, the vendor
   changed its model, not the world. Record which of the two happened.

5. Set thresholds in policy, not per case: what score triggers enhanced due diligence, what
   triggers a freeze, and what is documented-and-cleared. Write each with the reason.

6. When a score drives a file-blocking decision, capture the raw JSON, the model version if the
   vendor exposes one, and the retrieval timestamp — a score with no artefact is not evidence.

## Pitfalls

- Treating an exchange cluster as authoritative KYC. Clusters mislabel, and a mislabelled deposit
  can make an innocent address look like a mixer user.
- Reading a low score as a clearance. Absence of a flag is not a negative screen; it means the
  vendor has no label, which is not the same as nothing to declare.
- Screaming "sanctioned" when the output said "high risk". One is a legal status, the other a
  business judgement, and the misreport damages trust with the customer and the examiner.
- Comparing scores from two vendors as if they share a scale. They do not; scores are ordinal
  within a vendor and are not portable.
- Forgetting coverage. A score is only meaningful for chains the vendor indexes; a green result
  on an unsupported chain is meaningless.

## Verification

    jq -r '.identifications[]?.category' vendor.json | sort -u

If this prints nothing, the vendor made no designation claim for the address and the finding can
only be reported as heuristic risk.

Report the raw score, the exposure split with hop counts, the vendor and retrieval time, and the
policy band it falls into. A "high risk" label is an input to review; confirming it as a
sanctions or enforcement matter is a decision for a qualified compliance officer.
