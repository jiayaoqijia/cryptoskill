---
name: screen-addresses-against-sanctions-lists
description: Use when a deposit address, withdrawal address or counterparty wallet must be checked against public sanctions lists before funds move, and you need the matched row and list version as evidence rather than a vendor score.
---

# Screen an address against public sanctions lists

Screening is exact-match against a dated list, not a similarity search. A miss on a designated
address is treated as strict liability in most regimes, so the output must be the matched row plus
the list digest and fetch time — never a bare "clear".

## Procedure

1. Fetch each list into a per-day directory and hash it. A screen against an undated cache is
   worthless because you cannot show which version you used.

       D=~/screening/$(date -u +%F); mkdir -p "$D" && cd "$D"
       curl -sSLo sdn.csv "https://www.treasury.gov/ofac/downloads/sdn.csv"
       curl -sSLo alt.csv "https://www.treasury.gov/ofac/downloads/alt.csv"
       curl -sSLo consolidated.xml \
         "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
       sha256sum sdn.csv alt.csv consolidated.xml | tee digests.txt

2. Normalise the subject: lowercase hex, no `0x` prefix, no ENS name. Lists store raw addresses
   only, so `alice.eth` must be resolved and both the name and the resolved address screened.

       A=8589427373d6d84e98730d7795d8f6f8731fda07   # strip 0x, lowercase
       grep -in "$A" sdn.csv alt.csv

3. Screen every hop, not just the endpoint: originator, beneficiary, and any intermediary or
   relayer address in the call path.

4. Record the outcome as one of `exact match`, `no match`, or `unresolved` (list unreachable,
   chain unsupported). Unresolved is not a pass — it is an open item that blocks the transfer.

5. Where a vendor API is also used, store its raw JSON response alongside the list screen so the
   two can be reconciled later:

       curl -s "https://public.chainalysis.com/api/v1/address/$ADDR" \
         -H "X-API-Key: $CHAINALYSIS_KEY" -o vendor.json

6. Freeze the decision: if there is a match, stop the transfer and route to the compliance owner.
   Do not attempt to re-route, split, or obfuscate the payment to make it clear.

## Pitfalls

- Screening the destination but not the source; inbound-only or outbound-only screens both leak.
- Treating a fuzzy name match as an address match. Addresses have no fuzzy tier — it is equal or
  it is not.
- Screening after broadcast. The screen must gate the send, not decorate a completed one.
- Assuming every sanctioned address is published. Some designations are name-based and have no
  on-chain artefact, so address screening alone is not a complete programme.
- Using one vendor's risk score as a substitute for the list check; a score of 0.1 is not a
  negative screen.

## Verification

    grep -ic "$A" sdn.csv alt.csv
    # 0 means no exact hit in these two files; confirm the same for consolidated.xml and any
    # additional regional lists before writing "no match".

Report the address normalised, every list screened with its `sha256` and UTC fetch time, the
result per list, and the disposition. This produces evidence for a compliance decision; a
qualified compliance officer or licensed counsel must make the final call on any match.
