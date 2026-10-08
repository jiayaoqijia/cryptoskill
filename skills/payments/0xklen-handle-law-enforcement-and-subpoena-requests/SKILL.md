---
name: handle-law-enforcement-and-subpoena-requests
description: Use when law enforcement, a regulator or a private party demands records covering customer data or an account, and you must preserve and route the request without over-disclosing.
---

# Handle a law-enforcement or subpoena request

An inbound legal demand is a preservation and routing problem before it is a disclosure problem.
The organisation's job is to stop the relevant evidence degrading, verify who is asking, and hand
the question to counsel — not to decide scope on the spot.

## Procedure

1. Log the request on arrival with the receiving channel, the requester, and the exact identifier
   of what was asked for. This timestamp starts every later clock.

```
       printf '%s,%s,%s,%s\n' "$(date -u +%FT%TZ)" "$REQUESTER" "$CASE_REF" "$SCOPE" \
         >> legal-requests.log
```

2. Preserve immediately and broadly, then narrow later. Snapshot the accounts, transaction
   records, and any linked identifiers named, and record what was preserved:

       aws s3api put-object --bucket compliance-archive --key "hold/$CASE_REF/manifest.json" \
         --body hold-manifest.json --metadata legal-hold=true

   Preservation is cheap and reversible; deletion is not. Never let a routine retention job expire
   data under a hold.

3. Verify the legal instrument before producing anything: who issued it, under what authority, in
   which jurisdiction, whether it is an order or a voluntary request, and whether it is valid on
   its face. A screenshot of a document in an email is a request to be verified, not an order.

4. Route to counsel and, where required, to the designated law-enforcement response team.
   Technical staff should not assess scope alone.

5. Apply the tipping-off rule: do not notify the customer, a colleague without a need to know, or
   a third-party service that a request exists unless counsel directs otherwise.

6. Produce only what counsel approves, in the format they specify, with a transmittal that records
   exactly what was disclosed and to whom.

7. Close the request with a record: instrument verified, counsel advice reference, what was
   preserved, what was produced, and the date each step happened.

## Pitfalls

- Deleting or letting retention expire data after receiving a request, which converts a
  disclosure request into a spoliation problem.
- Producing records to whoever asks first, including a plausible-looking emailed demand or a
  private party's civil subpoena with no legal basis for the data sought.
- Over-disclosing: answering a request for one account with a bundle that covers hundreds,
  including data outside the instrument's scope.
- Letting an engineer answer a request directly to be helpful, bypassing counsel and the log.
- Failing to preserve metadata: a transfer list without timestamps, IPs and counterparties is not
  the record that was asked for.

## Verification

    tail -n 3 legal-requests.log
    aws s3api head-object --bucket compliance-archive --key "hold/$CASE_REF/manifest.json" \
      | jq -r '.Metadata."legal-hold"'

A pass shows the request logged with a timestamp and a hold object present with the hold metadata
set, before any production.

Report the requester, the instrument and its verification status, the scope preserved, and what
counsel directed. Validating an instrument and deciding what may lawfully be disclosed is a legal
determination that only qualified counsel can make.
