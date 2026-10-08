---
name: implement-travel-rule-data-transfer
description: Use when a transfer between two virtual-asset service providers must carry originator and beneficiary data, and you are wiring the IVMS 101 payload, the counterparty handshake, or the fallback when the peer has no endpoint.
---

# Implement travel-rule data transfer between VASPs

When one regulated provider sends value to another, the originator and beneficiary information
must travel with it. The engineering problem is provenance and reliability: the payload must be
reconstructable at audit, and a peer that cannot receive it must not silently drop the data.

## Procedure

1. Assemble the payload in IVMS 101 shape — one `originator` block, one `beneficiary` block, and
   the `originatingVASP` / `beneficiaryVASP` stanzas. The legal name, the account identifier
   (that is the chain address), and the country are the fields most often omitted.

2. Validate the payload locally before sending; a malformed name or a missing country is a
   rejection, not a warning.

       python3 -c '
       import json,sys
       d=json.load(open("ivms101.json"))
       o=d["originator"]["originatorPersons"][0]["naturalPerson"]["name"][0]
       assert o.get("nameIdentifier"), "originator name missing"
       print("originator ok:", o["nameIdentifier"][0]["primaryIdentifier"])'

3. Prefer an open transport (TRP / TRISA) to a bespoke API per peer. If you must support a
   proprietary endpoint, put the peer's scheme name, endpoint, and a test-vector response under
   version control so a peer-side change is a reviewable diff.

4. Handle the handshake explicitly: confirm the beneficiary address before release, and store the
   peer's confirmation receipt keyed by your internal transfer id.

       curl -sS -X POST https://api.trp.example/v1/transfers \
         -H "Content-Type: application/json" -H "Authorization: Bearer $TRP_KEY" \
         -d @ivms101.json -o receipt.json
       jq -r '.status, .transferId' receipt.json

5. For peers with no receiving endpoint, apply the documented fallback — typically collect and
   hold the counterparty data with the sending institution and transmit on request within 24
   hours — and log which fallback path was used per transfer.

6. Emit a per-transfer record: internal id, chain, tx hash, payload hash, peer, method, and
   timestamp. The payload itself is stored encrypted; the hash is what you retain in queryable
   form.

## Pitfalls

- Sending the data only when the amount is above a threshold you guessed; thresholds differ by
  jurisdiction and the EU regime applies to CASP-to-CASP transfers with no amount floor.
- Treating the chain address as sufficient beneficiary data. It is the account identifier, not the
  name; both are required.
- Storing the full payload in plaintext application logs, which turns the compliance feature into
  a personal-data breach.
- Assuming the peer validated anything. A `200 OK` from a proprietary endpoint frequently means
  "acknowledged", not "accepted".
- Dropping the transfer when the peer is unreachable instead of holding it for the mandated
  follow-up window.

## Verification

    jq -e '.originator and .beneficiary and .originatingVASP' ivms101.json >/dev/null && echo structure-ok
    sha256sum ivms101.json | tee -a transfer-payloads.log

A pass means the three required blocks are present and the payload hash is logged against the
transfer id; a missing block or an unlogged hash fails the check.

Report the transport used, the peer, the payload hash, and the fallback path taken. Whether the
transfer is legally complete is a question for the compliance officer and counsel, who own the
final determination.
