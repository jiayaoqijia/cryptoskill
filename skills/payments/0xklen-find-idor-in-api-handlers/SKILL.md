---
name: find-idor-in-api-handlers
description: Use when an API accepts a user-supplied identifier and may fetch the object without an ownership check. Enumerates id-bearing routes, probes them with a second account, and proves or clears each IDOR.
---

# Find IDOR in API handlers

An insecure direct object reference is any handler that trusts a client-supplied identifier
without re-scoping it to the caller's tenant and role. Sequential integers leak enumeration; UUIDs
do not remove the bug, they only make it less convenient to guess.

## Procedure

1. Locate every id-bearing parameter across path, query, body, and headers:

       rg -n "/(:[a-z_]+|\{[a-z_]+\})|params\[|request\.args|req\.params|query\.get\(|pathParam" src/ \
         | rg -in "id|uuid|ref|key|token|owner" | sort -u

2. Classify identifiers: monotonic integers (`/orders/1042`) invite enumeration, UUIDv4 does not,
   but neither implies an authorization check exists.

3. Capture the two-account baseline. Authenticate as A and as B, then for each id path request B's
   resource with A's token:

       ffuf -u "https://app.example.com/api/orders/FUZZ" \
            -H "Authorization: Bearer $A_TOKEN" \
            -w <(seq 1000 1100) -mc 200 -o /tmp/idor.json -of json

   Any 200 for an id owned by B is a confirmed IDOR.

4. Fuzz the same ids with A's token but vary one header — some handlers honour `X-User-Id` or
   `X-Tenant` for routing and forget to bind it to the session.

5. Check the object's parent chain: a nested route `/users/{uid}/orders/{oid}` may validate `uid`
   but ignore whether `oid` belongs to `uid`.

6. Verify that create/update/delete take the same care as read. Mass-assignment of `owner_id` is a
   write-side IDOR (`detect-mass-assignment`).

7. For each finding, capture the exact request, the id space, and the leaked fields, then write a
   regression test that asserts 403/404 for a cross-tenant id.

## Pitfalls

- Switching the id in a path to a value the attacker owns and getting a 200 proves nothing; the
  request must target an id owned by a different account.
- IDs in JSON bodies and multipart fields are omitted when you only test the URL.
- Looking up by `username` or `email` is the same bug with a human-readable key.
- Batch endpoints (`?ids=1,2,3`) bypass per-request checks and return others' rows in one call.
- A 403 on GET but 200 on PUT is a partial fix; test every verb.
- Enumeration of an *unauthenticated* endpoint is information disclosure; still report it.

## Verification

    jq -r '.results[] | "\(.status) \(.url)"' /tmp/idor.json | rg '^200'

Pass: no line prints a 200 for an id owned by a second account. Report each confirmed IDOR with
verb, route, id type, and the fields leaked; list cleared routes separately.
