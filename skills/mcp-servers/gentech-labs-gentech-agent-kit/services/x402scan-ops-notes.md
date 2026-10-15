# x402scan Listing — Ops Notes (2026-08-02)

**Status:** REGISTERED ✅ — merchant page: `https://tryponcho.com/m/api.gentechlabs.net`

**What it is:** x402scan.com (www.x402scan.com) — the x402 block explorer / marketplace (12.21M txns, $717K volume, 86K sellers). "Add your API" flow.

**How to register / re-verify:**
1. Go to https://www.x402scan.com → "Add your API"
2. Enter `api.gentechlabs.net`
3. It probes endpoints from our openapi.json — expects x402-paid endpoints to return HTTP 402 (payment challenge), free endpoints to be marked `security: []`

**The fix that cleared "7 endpoints with errors":**
- The gateway's `/openapi.json` was being shadowed by FastAPI's auto-generated spec (registered at app creation, wins over custom route).
- Fix: `app = FastAPI(..., openapi_url=None, docs_url=None, redoc_url=None)` so our custom spec is the only one.
- Custom spec marks free endpoints (`/`, `/health`, `/status`, `/openapi.json`, `/.well-known/*`) with `"security": []`, and `/v1/{service}/{path}` carries the x402 security scheme.
- Added `info.contact.email` (jordanjones0902@gmail.com) for ownership verification.

**Verify live:**
```bash
curl -s https://api.gentechlabs.net/openapi.json | python3 -m json.tool
# title: GenTech Labs x402 Gateway, version: 9.0.0, contact present
```

**Gotcha:** `/openapi.json` is ALSO served as a static file at `/var/www/gentechlabs/openapi.json` (June 25, stale, "5 live x402-protected APIs") on the `gentechlabs.net` domain. The `api.gentechlabs.net` domain proxies to the live gateway (port 8090). If the static copy shows up somewhere, update or delete it — it's not the live spec.
