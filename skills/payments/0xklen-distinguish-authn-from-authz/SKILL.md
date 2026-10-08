---
name: distinguish-authn-from-authz
description: Use when reviewing whether an endpoint checks who the caller is versus what they are allowed to touch. Separates authentication from object- and function-level authorisation and tests each axis on its own.
---

# Distinguish authentication from authorization

Authentication answers "who is this caller?"; authorization answers "may this identity touch this
object or invoke this function?". A route that correctly returns 401 when anonymous can still be a
full IDOR once authenticated, so the two checks are reviewed and tested as separate axes.

## Procedure

1. Inventory the authentication checks:

       rg -n "requiresAuth|@login_required|authenticate|get_current_user|requireAuth" src/ | tee /tmp/authn_hits.txt

2. Inventory the authorization checks — anything that scopes by owner, tenant, or role:

       rg -n "authorize|isOwner|owns\(|hasPermission|@roles|require_role|can\(" src/ | tee /tmp/authz_hits.txt

   Any route in the first list but not the second is the suspect set.

3. For every route that accepts an object id, read the fetch and decide whether it is scoped by the
   caller or by the raw id:

       # suspect: no owner scope
       obj = db.get(Order, order_id)
       # safe: scoped to the authenticated principal
       obj = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()

4. Function-level authorization: confirm admin routes are gated by role, not merely by login.
   `rg -n "is_staff|is_superuser|ROLE_ADMIN|scope==" src/`.

5. Build two accounts of the *same* privilege level (A and B). Capture an object id owned by B,
   then replay it as A:

       curl -s -H "Authorization: Bearer $A_TOKEN" \
         https://app.example.com/api/orders/$B_ORDER_ID -o /dev/null -w '%{http_code}\n'

   Expect 403 or 404 — never 200.

6. Vertical axis: call an admin-only route with a normal-user token and expect 403.

7. Confirm the posture is deny-by-default: an allowlist middleware beats per-handler
   `if not user.is_admin: abort(403)` checks scattered through the codebase.

8. Record a matrix of route, authn check, authz check, object scope, and the two-token result.

## Pitfalls

- Returning 200 on your own object masks a missing check; the test must use another account's id.
- A frontend that hides the admin button is presentation, not authorization — the API must reject.
- GraphQL resolvers often skip re-checks because the schema "looks" typed; test each resolver.
- Middleware matching `/api/admin/*` misses `/api/admin` on routers that do not normalise the path.
- A role carried in a client-supplied JWT claim is only as trustworthy as signature verification.
- "Authenticated == authorised" passes every test where every account happens to own its own data.

## Verification

    for id in $B_IDS; do \
      code=$(curl -s -H "Authorization: Bearer $A_TOKEN" https://app.example.com/api/orders/$id -o /dev/null -w '%{http_code}'); \
      printf '%s %s\n' "$id" "$code"; \
    done

Pass: every id owned by B returns 403 or 404 for A's token. Report the route→check matrix and any
route that carried authentication but no authorization check.
