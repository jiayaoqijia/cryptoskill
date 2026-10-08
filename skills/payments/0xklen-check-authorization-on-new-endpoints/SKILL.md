---
name: check-authorization-on-new-endpoints
description: Use when a diff adds a route, handler, or API method and authentication may be present but authorization is not. Requires an explicit access check per new endpoint before merge.
---

# Check authorization on new endpoints

Authenticated is not authorized. A new endpoint behind a valid session that never checks ownership lets any logged-in user read or mutate another user's record — the classic IDOR.

## Procedure

1. Enumerate every new entrypoint in the diff: `gh pr diff 482 | grep -nE '^\+.*(@(app|router)\.(get|post|put|patch|delete)|func .*Handler|public .*Response)'`.
2. For each, find the authorization check, not just the auth middleware. Authentication answers "who"; you need "is this who allowed to touch this object".
3. Require an object-level check that binds the resource to the caller:
       order = Order.objects.get(pk=order_id, user=request.user)   # scoped query
       if order.user_id != current_user.id:
           raise HTTPException(status_code=403)
   A lookup by id alone, followed by no owner comparison, is a blocking finding.
4. Test it adversarially: as user B, request user A's resource id and confirm a 403 or 404, never a 200 with A's data.
5. Check role and scope claims are read from the verified token, not from a request body field or query parameter the caller controls.
6. Confirm list endpoints filter by the caller, not just detail endpoints — an unfiltered list leaks the same data in bulk.
7. Verify admin or internal endpoints are gated by role, not merely hidden from the router.

## Pitfalls

- Auth middleware applied to a router prefix but one new route registered outside it.
- An IDOR in a nested path (`/users/{id}/invoices/{invoice_id}`) where only the outer id is checked.
- A check that compares a numeric id parsed as a string, so `"1" != 1` always passes.
- Returning 403 vs 404 leaking existence; for private records prefer 404.

## Verification

    # As user B, attempt user A's resource:
    curl -s -o /dev/null -w '%{http_code}\n' \
      -H "Authorization: Bearer $USER_B_TOKEN" \
      https://api.example.com/users/$USER_A_ID/invoices/$INVOICE_ID
    # Expect 403 or 404, never 200.

Report each new endpoint, the check that protects it, and the adversarial request you ran. Any endpoint with authentication but no object-level check is blocking.
