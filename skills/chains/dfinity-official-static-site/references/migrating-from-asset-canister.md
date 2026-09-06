# Migrating from `@dfinity/asset-canister` to `@dfinity/static-site`

This guide moves an existing project from the **legacy SDK asset canister** (`@dfinity/asset-canister`, `.ic-assets.json5`) to the **certified-assets canister** (`@dfinity/static-site`, `_headers`/`_redirects`). Reference migration: [dfinity/icp-cli#682](https://github.com/dfinity/icp-cli/pull/682) migrated the icp-cli docs canister this way.

## Why migrate

The certified-assets canister adds **response certification** and **automatic clean-URL canonicalization** (e.g. `/about` ↔ `/about/` resolve to one canonical URL via `307`), which fixes a class of broken relative-link bugs the legacy canister had (it served both slash variants with identical status codes). It also adds built-in access protection for private apps.

## The core caveat: you cannot upgrade in place

The two are **unrelated canisters with unrelated Candid interfaces**, so a plain `icp deploy` (which attempts an in-place *upgrade*) **fails before anything is installed**: icp-cli's pre-install compatibility check aborts with `Candid interface compatibility check failed: '<canister>' … You are making a BREAKING change`. Nothing is installed and the running asset canister is untouched — a safe failure, not a corrupted canister. (This is *not* a stable-memory "Cannot parse header" panic; the check stops the deploy before any wasm is installed.) You have two options:

1. **New canister (simplest, changes the canister ID).** Remove the old canister from `icp.yaml`, add a new `frontend` entry with the static-site recipe, and `icp deploy`. You get a fresh canister ID. Update any custom-domain registration and any hardcoded references to the old ID.
2. **Reinstall in place (keeps the canister ID, wipes state).** Point the existing canister's recipe at static-site and deploy with reinstall mode:
   ```bash
   icp deploy --mode reinstall frontend
   ```
   Reinstall replaces the wasm and **wipes all canister state**, then the sync plugin re-uploads every file. Because `--mode reinstall` is not an upgrade, it **skips the Candid check entirely**. The canister ID (and thus its URL / custom domain) is preserved. This is what PR #682 used, exposed as a `mode` input on its deploy workflow.

> Always deploy with the intended mode explicitly during migration. Do **not** silence the check with `--yes`: that forces the in-place upgrade onto stable memory the certified-assets canister cannot interpret (it keeps its state in `ic-stable-structures` with no deserialize-on-boot step, so it reinitializes to empty rather than rejecting the foreign layout), leaving a live canister that serves nothing. Use `--mode reinstall` or a new canister instead.

## Config mapping

### 1. Recipe in `icp.yaml`

```diff
 canisters:
   - name: frontend
     recipe:
-      type: "@dfinity/asset-canister@v2.2.1"
+      type: "@dfinity/static-site@v0.3.3"
       configuration:
         dir: dist
         build:
           - npm install
           - npm run build
```

Pin the latest [static-site release](https://github.com/dfinity/icp-cli-recipes/releases?q=static-site). Drop any `configuration.version` field — the static-site recipe version *is* the canister version.

### 2. `.ic-assets.json5` → `_headers` + `_redirects`

Delete `.ic-assets.json5` and split its concerns into two Netlify/Cloudflare-style files at the root of your `dir`:

| Legacy `.ic-assets.json5` | certified-assets |
|---------------------------|------------------|
| `"match": "**/*"` + `"enable_aliasing": true` (SPA fallback) | `/*  /index.html  200` in `_redirects` |
| `"headers": { "Cache-Control": ... }` | a block in `_headers` (pattern matches the **file/asset key**, e.g. `/*.html`, `/assets/*`) |
| `"security_policy": "standard"` | **no default** — write the security headers yourself in `_headers` (CSP, `X-Frame-Options`, etc.) |
| `"allow_raw_access": false` | not applicable — certified-assets has no raw-access mode |
| `{ "match": ".well-known", "ignore": false }` | not needed — `.well-known/` is uploaded automatically |
| glob `**/*`, `?`, arbitrary depth | single `*` wildcard only; `/*` is a trailing-subtree match; no `**`/`?` |

Example: an `.ic-assets.json5` with a standard security policy, aggressive asset caching, revalidated HTML, and SPA aliasing becomes —

`_redirects`:
```
/*  /index.html  200
```

`_headers`:
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
```

Remember `_headers` patterns match the **asset key** (the file path), not the visitor URL: use `/index.html` / `/*.html`, not `/`. See the main SKILL.md's `_headers` section for the reserved-header list the sync plugin rejects.

### 3. CI / deploy workflow

Publish `_headers` and `_redirects` (instead of `.ic-assets.json5`) into `dir`, and add a `mode` input so the migration deploy can use `reinstall` (PR #682 did both). After the one-time migration deploy, subsequent deploys are ordinary `icp deploy` (in-place upgrade — safe within the same canister type; a **breaking** certified-assets release will itself require a reinstall + re-sync).

### 4. Programmatic uploads

If your project used `AssetManager` from `@icp-sdk/canisters/assets`, that code **stops working** — the certified-assets canister does not expose the SDK asset canister's `store`/`create_batch`/`commit_batch` API. Uploads now go exclusively through the recipe's sync plugin on `icp deploy`. There is no drop-in `AssetManager` replacement; remove the programmatic-upload path and rely on `icp deploy` (with a `presync` build step if you need canister IDs baked in).

### 5. Upload authorization

`grant_permission`'s three roles (`Prepare`/`Commit`/`ManagePermissions`) collapse to certified-assets' flat model: controllers plus an `authorize(principal)` set of syncers. Re-grant any CI principal with:

```bash
icp canister call frontend authorize '(principal "<ci-principal-id>")'
```

## What stays the same

- The **`ic_env` cookie** is served on every HTML response by both canisters, so frontend code reading canister IDs / the root key via `safeGetCanisterEnv()` needs no change.
- The `build` / `presync` / `metadata` recipe configuration fields behave the same way.
- The mainnet browser URL is still `https://<canister-id>.icp.net` (a new ID if you took the new-canister route).

## Checklist

- [ ] `icp.yaml` recipe → `@dfinity/static-site@<latest>`, `configuration.version` removed
- [ ] `.ic-assets.json5` deleted; `_redirects` (SPA rule) and `_headers` (security + caching) added to `dir`
- [ ] Security headers rewritten explicitly (no `security_policy: "standard"` default)
- [ ] `AssetManager` / programmatic-upload code removed
- [ ] CI publishes `_headers`/`_redirects`; migration deploy uses `--mode reinstall` (or a new canister)
- [ ] CI principal re-authorized with `authorize`
- [ ] Custom domain / hardcoded canister-ID references updated if the ID changed
- [ ] Verified with `http_request` that `/` returns 200 and SPA deep links return the shell, not 404
