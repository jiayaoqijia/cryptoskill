---
name: static-site
description: "Deploy a frontend or any static site to the IC with the @dfinity/static-site recipe (the certified-assets canister). Covers icp.yaml recipe config, SPA routing with _redirects, custom headers/CSP with _headers, clean URLs, access protection for private apps, custom domains, and building against canister IDs. This is the recommended way to host frontends and static files on the IC. Also the entry point for the legacy @dfinity/asset-canister recipe and .ic-assets.json5 (see the legacy reference) and for migrating an existing asset canister to certified-assets. Use when hosting a frontend, deploying static files, an asset canister, or setting up SPA routing on the IC. Do NOT use for canister-level HTTP code patterns or custom domain DNS setup — use custom-domains for DNS."
license: Apache-2.0
compatibility: "icp-cli >= 1.0.0, Node.js >= 22"
metadata:
  title: Static Site (Certified Assets)
  category: Frontend
---

# Static Site (Certified Assets)

## What This Is

The **`@dfinity/static-site` recipe** deploys a static site — a built frontend, docs, or any folder of files — to the **certified-assets canister** on the Internet Computer, which serves it over HTTP with **response certification**. Every response carries a cryptographic proof, and the IC HTTP gateway verifies that proof before handing the response to the browser: visitors get content the canister provably committed to, not something a boundary node or gateway altered in transit.

**This is the recommended way to host a frontend on the IC going forward.** The recipe bundles a matched pair — the canister and its sync plugin — pinned together by one version. You point it at your build directory; `icp deploy` uploads, certifies, and serves.

> The older **`@dfinity/asset-canister` recipe** (the SDK asset canister, configured with `.ic-assets.json5`) is still supported for existing projects but is no longer the recommended path. It is a *different canister* with a different config format and API — see [`references/legacy-asset-canister.md`](references/legacy-asset-canister.md). To move an existing project over, see [`references/migrating-from-asset-canister.md`](references/migrating-from-asset-canister.md).

## Prerequisites

- `icp-cli` — `npm install -g @icp-sdk/icp-cli`. The recipe pins the canister + sync-plugin pair, both pre-built, so a plain `dir`/`build`/`presync` deploy needs nothing else.
- `ic-wasm` — `npm install -g @icp-sdk/ic-wasm`. A **separate** binary, not bundled with `icp-cli`. This recipe shells out to it *only* when you set the `metadata` field (the generated build guards on `command -v ic-wasm` and fails with "ic-wasm not found"); other official recipes need it unconditionally, so installing both up front is the safe default — see the `icp-cli` skill.
- Your frontend's build toolchain (e.g. Node.js >= 22 for a Vite/React app).

## Canister IDs and URLs

Static-site canisters are created per-project — there is no global canister ID. After deployment the canister ID is stored in `.icp/<cache|data>/mappings/<environment>.ids.json`. Managed networks (the local replica) are **cache** — `.icp/cache/mappings/local.ids.json`; connected networks (mainnet `ic`) are **data** — `.icp/data/mappings/ic.ids.json`.

| Environment | Browser URL |
|-------------|-------------|
| Local | `http://<canister-name>.<environment>.localhost:8000` — the middle label is the **environment name**, `local` by default, so `http://frontend.local.localhost:8000` (this is the URL `icp deploy` prints; `http://<canister-id>.localhost:8000` also works — `<canister-name>.localhost` with no environment label does not) |
| Mainnet | `https://<canister-id>.icp.net` |
| Custom domain | `https://yourdomain.com` (with DNS configuration) |

## icp.yaml Configuration

```yaml
canisters:
  - name: frontend
    recipe:
      type: "@dfinity/static-site@v0.3.3"
      configuration:
        build:
          - npm ci
          - npm run build
        dir: dist
```

Check the [static-site releases](https://github.com/dfinity/icp-cli-recipes/releases?q=static-site) for the latest version and pin it in the `type` field. Because the recipe pins a matched canister + plugin pair, there is **no separate canister version to choose** — the recipe version *is* the canister version.

The recipe takes four configuration fields:

| Field | Required | Description |
|-------|----------|-------------|
| `dir` | **Yes** | The single directory of built files to serve. The canister owns its whole URL space, so this is one directory, not a list. Vite → `dist`, Next.js export → `out`. |
| `build` | No | Shell commands run *before the canister exists* to produce `dir` (e.g. `npm run build`). No canister IDs are available yet. |
| `presync` | No | Shell commands run *at sync time, after the canister exists*, with deployed canister IDs exported as env vars. Use this to bake a canister ID into a frontend build (see [below](#building-against-canister-ids-presync-vs-build)). |
| `metadata` | No | `name`/`value`/`visibility` entries baked into the canister wasm via `ic-wasm`. `visibility` is optional, `public` or `private`; omitted means `private` (ic-wasm's default), and only `public` sections are readable by anyone via `icp canister metadata`. Values are interpolated in a shell at build time, so `$(…)` works. |

## Pitfalls

1. **Using `.ic-assets.json5` with the static-site recipe.** `.ic-assets.json5` is the **legacy asset canister's** config file. The certified-assets canister does not read it — and because the plugin skips every dotfile and dot-directory (only `.well-known/` is exempt, Pitfall 12), a `.ic-assets.json5` in your `dir` is not even uploaded. It is silently absent, so SPA fallback, headers, and security policy do nothing. Configure this canister with `_redirects` and `_headers` instead (below).

2. **Wrong SPA fallback rule.** For client-side routing, the fallback is a **rewrite** in `_redirects`: `/*  /index.html  200`. The `200` status is what makes it a rewrite (serve the shell's contents at the requested URL, no visible redirect) so deep links work on fresh load and reload. Do **not** use a `301`/`302` redirect, and do **not** reach for `enable_aliasing` — that is a legacy asset-canister setting and has no effect here.

3. **Relative asset paths in a SPA.** Link assets with **absolute** paths (`/assets/app.js`), never relative (`assets/app.js`). Under a `/*` rewrite, a relative URL resolves against the *client route*: at `/dashboard/settings` the browser requests `/dashboard/settings/assets/app.js`, which `/*` answers with the HTML shell — producing a confusing MIME-type error instead of loading your script.

4. **Expecting `AssetManager` / `@icp-sdk/canisters` to work.** The certified-assets canister's upload API is `upload_chunks` + `execute_operations`, **not** the SDK asset canister's `store`/`create_batch`/`commit_batch`. `AssetManager` from `@icp-sdk/canisters/assets` targets the *legacy* canister and does **not** work against static-site. Uploads happen through the recipe's sync plugin on `icp deploy`; there is no drop-in JS `AssetManager` equivalent for this canister. (If you need programmatic uploads, you are almost certainly on the legacy canister — see the legacy reference.)

5. **`_headers` / `_redirects` in the wrong place.** These two files must sit at the **root of your `dir`** (e.g. `dist/_redirects`). They are read as configuration and never served as assets. Put them in your `public/` (Vite) or `static/` folder so the build copies them into `dir` automatically — a file left at the project root but not copied into `dir` is simply absent at deploy time.

6. **Setting a reserved header in `_headers`.** The sync plugin **rejects** these at deploy time with an explanatory error: `Content-Length`, `Content-Encoding`, `ETag`, `Transfer-Encoding`, `Accept-Ranges`, `Content-Range`, `IC-Certificate`, `IC-CertificateExpression`, `Location`. To set an asset's media type use the bare `Content-Type:` form (it routes to asset metadata, not a response header). To redirect, use `_redirects` — a `Location` header in `_headers` would not redirect (status stays `200`).

7. **Assuming default security headers.** Unlike the legacy canister's `security_policy: "standard"`, the certified-assets canister adds **no default headers** — no `Cache-Control`, no CSP, no `X-Frame-Options`. If you want them, declare them in `_headers` (baseline below). The only headers it manages itself are the certification/serving ones and its `ic_env` cookie.

8. **A `404`/`410` rule pointing at a large file.** An error-page target must be a **small, single-chunk file** (under ~1.9 MB). Large files are served as certified `206` range responses that can't carry a 4xx status, so the plugin rejects such a rule at deploy time, naming it. (A `200` rewrite to a large file is fine.)

9. **Expecting dynamic redirect captures.** There is no `:splat` or `:placeholder` — you can't forward a captured segment (`/old/:rest → /new/:rest`). Every certifiable response must be enumerable ahead of time, so `_redirects`/`_headers` support only exact paths, a trailing `/*` subtree wildcard, and fixed destinations.

10. **Switching an existing project from the legacy asset canister to static-site.** Repointing `recipe:` at `@dfinity/static-site` and running a plain `icp deploy` **fails before anything is installed**: these are two unrelated canisters with unrelated Candid interfaces, so icp-cli's pre-install check aborts with `Candid interface compatibility check failed: '<canister>' … You are making a BREAKING change`. Run **`icp deploy --mode reinstall`** instead. That replaces the wasm with the certified-assets canister, **discards the old stable memory** — every legacy asset, permission, and `.ic-assets.json5`-derived setting is gone — and leaves the canister with empty state, after which the sync plugin uploads your whole `dir` from scratch. Deploying static-site as a brand-new canister avoids the question entirely. Do **not** silence the check with `--yes`: that pushes the in-place upgrade through onto stable memory certified-assets cannot read, leaving a live canister that serves nothing. See the migration reference.

11. **Assuming a recipe version bump re-installs itself.** Moving between certified-assets' **own** releases is gentler than the legacy switch above — the Candid interface is stable across a release series, so nothing blocks the deploy — but a breaking bump still needs a reinstall **you run yourself**. The canister and plugin are version-locked, so after bumping the recipe `icp deploy` upgrades in place and the sync plugin then refuses, reporting `assets canister version mismatch: canister is X, this plugin is Y` plus the fix: `icp canister install --mode upgrade` for a **patch** bump (state preserved) or `icp canister install --mode reinstall` for a **breaking** (pre-1.0 minor, post-1.0 major) bump, which wipes state so the next sync re-uploads every asset and redirect rule. A failed sync right after a version bump is this, not a bug.

12. **`.well-known/` is uploaded automatically — no config needed.** The plugin skips dotfiles and dot-directories *except* `.well-known/`, which it traverses normally. So `dir/.well-known/ic-domains` is served at `/.well-known/ic-domains` with no extra setting. (This is the opposite of the legacy canister, which needed an explicit `.ic-assets.json5` un-ignore rule.)

13. **Access protection ordering.** The recipe's `icp deploy` installs the canister **and** syncs assets together, so a plain deploy-then-`enable_protection` briefly serves your content publicly. For a brand-new *private* app, enable protection **before your real assets are synced** — deploy a `dir` containing only `login.html`, `enable_protection`, then deploy the full site — so assets are never world-readable. The login page must be **fully self-contained** (inline CSS/JS, `data:` URIs) — it is the only gate-exempt path, and any external subresource it references would itself be gated. See [Access protection](#access-protection-private-apps).

## SPA Routing and Redirects: `_redirects`

Add a `_redirects` file to the root of your `dir`. Syntax follows [Netlify's `_redirects`](https://docs.netlify.com/manage/routing/redirects/overview/) — one rule per line, three whitespace-separated fields (`from`, `to`, `status`); blank lines and `#` comments are ignored.

```
# Single-page-app fallback: serve the shell for any unmatched path (a rewrite, status 200)
/*               /index.html      200

# Permanent redirect to a new internal path
/old-blog        /blog            301

# Redirect to an external site
/discord         https://discord.gg/example   302

# Rewrite: serve /content/article.html at a pretty URL, no visible redirect
/article         /content/article.html         200

# Subtree redirect: everything under /docs/v1/ moves to /docs/v2/
/docs/v1/*       /docs/v2/        301

# Custom error pages (target must be a small single-chunk file)
/secret          /403.html        404
/retired-feature /sunset.html     410
```

Status codes: `301`/`302`/`307`/`308` redirect; `200` is a **rewrite**; `404`/`410` serve an error page. `from` is always absolute and its only wildcard is a trailing `/*`. Precedence, first match wins: **real files** > automatic **clean-URL** rules > your `_redirects` (in file order) > the 404 fallback. Because a real file always wins, a `/*` SPA rule only catches paths nothing else claimed.

**SPA caveat — missing assets return HTML.** With `/*  /index.html  200`, a typo'd `/assets/app-old.js` also matches `/*` and serves the shell as `text/html`. To give real 404s under a build-output folder, scope a narrower rule *above* the catch-all (rules match in file order):

```
/assets/*  /404.html    404
/*         /index.html  200
```

This needs a `404.html` in your `dir`; declaring `/*` means the built-in default 404 is not added.

## Custom Headers: `_headers`

Add a `_headers` file to the root of your `dir`. Syntax follows [Netlify's `_headers`](https://docs.netlify.com/manage/routing/headers/): a path pattern on its own line, followed by indented `Name: value` lines; a blank line or `#` ends a block. Patterns are absolute paths with an optional single `*` wildcard (which matches `/` too; there is no `**` or `?`).

A useful baseline — act like a senior security engineer and tighten the CSP for your app:

```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'

# Fingerprinted build assets never change — cache them hard
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# HTML should revalidate so deploys are picked up
/*.html
  Cache-Control: public, max-age=0, must-revalidate
```

Key rules:
- **Patterns match the file (asset key), not the visitor's URL.** Write `/index.html`, not `/`. For a SPA, a `Cache-Control` on `/index.html` (or `/*.html`) is what every `/*`-rewritten client route gets; a block written against a route like `/dashboard/*` matches no file and does nothing.
- **All matching blocks contribute** — a file matching several blocks gets every block's headers (same-name values are combined comma-separated; `Set-Cookie` stays separate).
- **`Content-Type` is special** — the bare `Content-Type: <type>` form overrides the stored media type of the matching file (use it for extension-less files like `/llms.txt`); it is single-valued, first-match-wins, and is *not* emitted as an ordinary header.
- Reserved headers are rejected at deploy time — see Pitfall 6.

## Clean URLs and the 404 Page

You don't link to `.html` files — the canister maps each HTML file to a clean, extension-less canonical URL and `307`-redirects the other forms to it:

| Your file | Canonical URL | Also handled (→ `307`) |
|-----------|---------------|------------------------|
| `dist/index.html` | `/` | `/index` |
| `dist/about.html` | `/about` | `/about/`, `/about/index` |
| `dist/blog/index.html` | `/blog/` | `/blog`, `/blog/index` |

Requesting the underlying `/about.html` directly currently serves it `200` (a file always beats a routing rule). For a custom 404, put a `404.html` at the root of your `dir`; otherwise a certified default is served. A SPA `/*` rule takes over the whole path space, so it replaces the default 404 with your shell.

## Custom Domains

To serve from your own domain, add a `.well-known/ic-domains` file to your `dir`, one domain per line:

```
example.com
www.example.com
```

`.well-known/` is uploaded automatically (Pitfall 12), so the file is served where the IC boundary nodes look. Registering the domain itself (DNS records, ACME challenge, TLS provisioning) is a separate IC platform step — see the `custom-domains` skill.

## Access Protection (private apps)

Put a login gate in front of an in-progress or preview app. Unauthenticated visitors get a certified `307 → <login_page>` (HTML) or `401` (other assets). Configure it through controller-only canister methods:

```sh
# 1. Add a self-contained /login.html to your dir and deploy.
icp deploy

# 2. Turn the gate on, naming your login page.
icp canister call frontend enable_protection '("/login.html")'

# 3. Mint a credential (here: a chosen passphrase valid ~1 year). Pass value = null for a random token.
#    issue_token takes a record (IssueTokenArgs), not positional args.
icp canister call frontend issue_token '(record { label = "owner"; ttl_secs = 31536000 : nat32; value = opt "my-passphrase" })'
```

> **Ordering & the public window.** The `static-site` recipe's `icp deploy` **installs the canister and syncs your assets in one step**, so the sequence above serves your content publicly for the brief window between that first deploy and `enable_protection` — fine when gating an existing or preview app. To avoid *any* public exposure for a **brand-new private app**, enable protection **before your real assets are synced**: run the first `icp deploy` with a `dir` containing only `login.html`, then `enable_protection '("/login.html")'`, then `icp deploy` again with the full site. The login page is gate-exempt, so nothing private is ever served unauthenticated (Pitfall 13). (Enabling on a truly empty canister also works — the canister reports `EnabledLoginPageMissing` and self-heals to `Enabled` once `login.html` is synced.)

| Method | Effect |
|--------|--------|
| `issue_token '(record { label = "<label>"; ttl_secs = <secs> : nat32; value = opt "<value>" })'` | Mints a token, returns its value. `value = null` → high-entropy random token. |
| `revoke_token '("<label>")'` | Removes every token with that label, live. |
| `list_tokens '()'` | Live tokens `{ label; expires_at }` (controller-only). |
| `check_protection_status '()'` | `Disabled`, `Enabled`, or `EnabledLoginPageMissing`. |
| `disable_protection '()'` | Gate off, drops all tokens. |

Always pass the argument explicitly — `'()'` for the methods that take none. Called with no argument, `icp canister call` opens an interactive prompt instead of sending an empty one.

This is **access gating, not confidentiality**: node operators can read asset bytes and the token store, there is no rate-limiting, and it relies on the honest-replica/honest-gateway assumption. Use high-entropy random tokens for share links; enable *before* the first sync for a new private app (Pitfall 13). Full details in the [certified-assets access-protection docs](https://github.com/dfinity/certified-assets/blob/v0.3.3/docs/access-protection.md).

## Authorizing Uploaders

Uploads (sync) are performed by canister **controllers** and by a separate set of **authorized syncer principals**. To let a CI/deploy principal sync without giving it full canister control, `authorize` it — do **not** `--add-controller`, which grants upgrade/settings/delete power far beyond uploading.

```bash
# Allow a principal to sync assets (upload), without making it a controller
icp canister call frontend authorize '(principal "<principal-id>")'

# List authorized syncers
icp canister call frontend list_authorized '()'

# Revoke
icp canister call frontend deauthorize '(principal "<principal-id>")'
```

> **Security Warning:** `icp canister settings update frontend --add-controller <principal-id>` grants full canister control (upgrade wasm, change settings, delete, drain cycles) — not just upload access. Prefer `authorize` for deploy pipelines.

## Building Against Canister IDs (`presync` vs `build`)

`build` runs before the canister exists, so it can't know any canister IDs. When a client-side app must bake in the ID of a canister it calls, build it in `presync` — that runs at sync time, once IDs exist, and exports them:

```yaml
canisters:
  - name: frontend
    recipe:
      type: "@dfinity/static-site@v0.3.3"
      configuration:
        dir: dist
        presync:
          - npm ci
          # $ICP_CLI_CID_BACKEND is the `backend` canister's principal.
          - VITE_CANISTER_ID_BACKEND=$ICP_CLI_CID_BACKEND npm run build
```

Variables available to `presync`: `ICP_CLI_CID` (this canister), `ICP_CLI_CID_<NAME>` (each project canister — name upper-cased, non-alphanumerics → `_`, e.g. `backend` → `ICP_CLI_CID_BACKEND`), `ICP_CLI_NETWORK`, `ICP_CLI_ENVIRONMENT`.

Alternatively, read canister IDs at **runtime** in the browser from the `ic_env` cookie the canister sets on every HTML response (works both locally and on mainnet with no environment branching) — see the `internet-identity` and `icp-cli` skills for the `safeGetCanisterEnv()` pattern. Prefer the cookie over `fetchRootKey()`.

## What You Get Automatically

No configuration needed — on by default:

- **Response certification** — every response is certified and gateway-verified.
- **Clean URLs** — `307` canonicalization (above).
- **Compression** — compressible assets are stored gzip + Brotli alongside the original and negotiated per request via `Accept-Encoding`. Compressible means: any `text/*`; any `+json` or `+xml` suffix (so `image/svg+xml`, `application/xhtml+xml`); `application/javascript`, `application/json`, `application/xml`, `application/wasm`; and `font/*` **except** `woff`/`woff2` (already compressed). An encoding is kept only if it actually came out smaller than the original.
- **ETag / `304 Not Modified`** — content-hash ETag; unchanged files aren't re-downloaded.
- **A default certified `404`** — replaceable with your own `/404.html`.
- **The `ic_env` cookie** — on HTML responses, carrying canister IDs and the root key for the frontend.

## Deploy & Verify

```bash
# Start the local network
icp network start -d

# Build + deploy everything (or just the frontend)
icp deploy
icp deploy frontend

# Mainnet (needs cycles)
icp deploy -e ic frontend
```

Re-running `icp deploy` re-syncs: the plugin diffs your directory against the canister and uploads only what changed.

```bash
# Canister is running
icp canister status frontend            # Status: Running, non-zero memory

# Get the canister ID (there is no `icp canister id`; use status --id-only)
icp canister status frontend --id-only

# Fetch the index page (certified)
icp canister call frontend http_request '(record {
  url = "/"; method = "GET"; body = vec {}; headers = vec {};
  certificate_version = opt 2;
})'                                       # → status_code = 200

# SPA fallback returns the shell, not 404
icp canister call frontend http_request '(record {
  url = "/dashboard/settings"; method = "GET"; body = vec {}; headers = vec {};
  certificate_version = opt 2;
})'                                       # → 200 (index.html), NOT 404

# Open in a browser (this is the URL `icp deploy` prints)
# Local:   http://frontend.local.localhost:8000
# Mainnet: https://<frontend-canister-id>.icp.net
```

## Legacy Asset Canister and Migration

- **Maintaining an existing `@dfinity/asset-canister` project** (`.ic-assets.json5`, `AssetManager` uploads, `grant_permission` roles, `allow_raw_access`): see [`references/legacy-asset-canister.md`](references/legacy-asset-canister.md).
- **Moving an existing asset-canister project to certified-assets / static-site**: see [`references/migrating-from-asset-canister.md`](references/migrating-from-asset-canister.md) for the config mapping and the reinstall-mode caveat.

## Additional References

- Load `icp-cli` for the recipe system, `icp.yaml` structure, canister-ID injection, and the `ic_env` cookie / `safeGetCanisterEnv()` pattern.
- Load `custom-domains` for DNS records, ACME challenge, and TLS provisioning of a custom domain.
- Load `internet-identity` for reading the root key and canister IDs from `ic_env` in a frontend.
- Full upstream user docs: [certified-assets docs](https://github.com/dfinity/certified-assets/blob/v0.3.3/docs/overview.md).
