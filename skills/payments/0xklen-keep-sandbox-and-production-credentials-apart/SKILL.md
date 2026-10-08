---
name: keep-sandbox-and-production-credentials-apart
description: Use when an integration touches both a test and a live environment. Separate hosts, keys, and clients so a bug cannot point test traffic at production or vice versa.
---

# Keep sandbox and production credentials apart

The classic integration accident is a test run that charges a real card because one generic
`API_KEY` pointed at production. Separate everything by environment and guard the boundary.

## Procedure

1. Name env vars by environment and never share one: `API_KEY_SANDBOX` and `API_KEY_PROD`, resolved by `APP_ENV`.
2. Keep two base URLs and refuse to start on a mismatch:
   ```python
   import os, re
   if os.environ.get("APP_ENV") == "prod" and re.search(
           r"sandbox|localhost|127\.0\.0\.1|\.test", os.environ["BASE_URL"]):
       raise SystemExit("prod pointing at a non-prod host")
   ```
3. Give credentials visually distinct prefixes; production keys must be revocable without touching test.
4. Store them at different secret paths (`/prod/app/api_key` vs `/dev/app/api_key`) with different policies.
5. Gate destructive test data: sandbox writes must never reference a production account id.
6. Print the environment in every log line and error so a misfire is obvious at a glance.
7. Default to sandbox when `APP_ENV` is unset — fail toward the safe environment.

## Pitfalls

- A single generic `API_KEY` copied between environments lets a test charge a real card.
- Providers sometimes share the auth host across environments and only the data host differs; check both hosts.
- Sandbox mirrors prod's model but with different limits and quirks; passing there is not proof for prod.
- Clients or connection pools built at import time can pin the wrong host if env is read late.
- `.env` files committed with prod keys leak live credentials; load from the secret store.

## Verification

    APP_ENV=prod BASE_URL=https://sandbox.api.example.com python -c 'import app.config'

Must exit non-zero with the guard message. Report: "Config guard rejected prod+sandbox host; sandbox key prefix sk_test_ distinct from sk_live_."
