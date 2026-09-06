# Legacy: the `@dfinity/asset-canister` recipe

This reference documents the **legacy SDK asset canister** (`@dfinity/asset-canister` recipe, the `dfinity/sdk` `ic-asset` canister). It is **still supported** for existing projects but is **no longer the recommended path** — new frontends should use the `@dfinity/static-site` recipe (certified-assets canister) described in the main SKILL.md. Use this reference to understand and maintain a project that is already on the asset canister, or to read its behavior before [migrating](migrating-from-asset-canister.md).

The legacy asset canister is a **different canister** from certified-assets: different config file (`.ic-assets.json5` vs `_headers`/`_redirects`), different upload API (`store`/`create_batch`/`commit_batch` vs `upload_chunks`/`execute_operations`), and a different permission model (`grant_permission` roles vs `authorize`). Config and code are not interchangeable between the two.

## icp.yaml Configuration

```yaml
canisters:
  - name: frontend
    recipe:
      type: "@dfinity/asset-canister@v2.2.1"
      configuration:
        dir: dist
        build:
          - npm install
          - npm run build
```

- `recipe.type: "@dfinity/asset-canister@..."` — tells `icp` this is the legacy asset canister.
- `dir` — directory to upload (contents, not the directory itself).
- `build` — commands `icp deploy` runs before uploading.
- `version` — optionally pins the asset canister **Wasm** version (independent of the recipe version). Omit to get the latest.

**Pin `v2.2.1` or later.** icp-cli 0.3.0 removes the built-in `type: assets` sync step; recipe versions ≤ `v2.1.0` generate the old step and break on 0.3.0. `v2.2.1` generates a `plugin`-based sync step. If writing a sync step by hand, use `type: plugin` (pointing at the certified-assets `sync_plugin.wasm` release artifact with its `sha256`) or `type: script`:

```yaml
sync:
  steps:
    - type: plugin
      url: https://github.com/dfinity/certified-assets/releases/download/migration-v2.2.1-6b48585/sync_plugin.wasm
      sha256: ca7cb5666c30d2875f8d5e10535f8a53f97a86c79c263f7d5bdac2fdd1bbf83c
      dirs:
        - dist
```

## SPA Routing and Default Headers: `.ic-assets.json5`

The legacy canister is configured with a `.ic-assets.json5` file (JSON5, glob `match` rules). It must end up in the `dir` directory at deploy time — place it in `public/`/`static/` so the build copies it into `dist/`.

```json5
[
  {
    // Default headers for all paths: caching, security, and raw access policy
    "match": "**/*",
    "security_policy": "standard",
    "headers": {
      "Cache-Control": "public, max-age=0, must-revalidate"
    },
    // Disable raw (uncertified) access by default
    "allow_raw_access": false
  },
  {
    // Cache static assets aggressively (they have content hashes in filenames)
    "match": "assets/**/*",
    "headers": {
      "Cache-Control": "public, max-age=31536000, immutable"
    }
  },
  {
    // SPA fallback: serve index.html for any unmatched route
    "match": "**/*",
    "enable_aliasing": true
  }
]
```

The critical SPA setting is `"enable_aliasing": true` — it serves `index.html` when a requested path has no matching file. (In certified-assets this is instead a `/*  /index.html  200` rule in `_redirects`.)

If the standard security policy blocks the app, override the default security headers with custom values after `Cache-Control`. Make them as strict as the app allows. The standard policy headers are defined at https://github.com/dfinity/sdk/blob/master/src/canisters/frontend/ic-asset/src/security_policy.rs

### Legacy pitfalls

1. **Wrong `dir` path.** `configuration.dir` must point to the build output (Vite → `dist`, Next.js export → `out`). A missing path deploys an empty canister.
2. **Missing `.ic-assets.json5` for SPAs.** Without `enable_aliasing`, refreshing on `/about` returns 404.
3. **Missing `build` step.** If `configuration.build` is omitted, run the build manually before deploying or `dir` is stale/empty.
4. **Pinning Wasm below `0.30.2`.** The `ic_env` cookie (read by `safeGetCanisterEnv()`) is only served by asset-canister Wasm ≥ `0.30.2`. Omit `configuration.version` or pin ≥ `0.30.2`.
5. **`allow_raw_access` left enabled.** By default assets are also served on the uncertified `raw.icp.net` domain, where content can be tampered with undetected. Set `"allow_raw_access": false` for sensitive assets.
6. **Downgrading the Wasm version.** The legacy asset canister serializes its state across upgrades, so upgrading *down* to an older Wasm can trap on boot when the older deserializer cannot read a newer stable-memory format. Prefer the recipe (loads latest) over `type: pre-built` with a manual Wasm URL. For an intentional downgrade use `icp deploy --mode reinstall` (wipes state).
7. **Removed `type: assets` sync step.** icp-cli 0.3.0 rejects it: *"icp-cli no longer supports the `assets` sync step type."* Use the `@dfinity/asset-canister@v2.2.1` recipe (plugin sync) — see above.

## Programmatic Uploads with `@icp-sdk/canisters` (legacy only)

`AssetManager` works **only** against the legacy asset canister — it uses the `store`/`create_batch`/`commit_batch` API. It does **not** work against the certified-assets (static-site) canister. Requires `@icp-sdk/canisters` (>= 3.5.0) and `@icp-sdk/core` (>= 5.0.0).

```javascript
import { AssetManager } from "@icp-sdk/canisters/assets";
import { HttpAgent } from "@icp-sdk/core/agent";
import { readFileSync, readdirSync } from "fs";

// SECURITY: shouldFetchRootKey fetches the root public key from the replica at
// runtime. In production the root key is hardcoded and trusted. Fetching it at
// runtime lets a man-in-the-middle supply a fake key and forge certified responses.
// NEVER set shouldFetchRootKey to true when host points to mainnet.
const LOCAL_REPLICA = "http://localhost:8000";
const MAINNET = "https://icp-api.io";
const host = LOCAL_REPLICA; // Change to MAINNET for production

async function manageAssets() {
  const agent = await HttpAgent.create({
    host,
    // Only fetch the root key when talking to a local replica.
    shouldFetchRootKey: host === LOCAL_REPLICA,
  });

  const assetManager = new AssetManager({
    canisterId: "your-asset-canister-id",
    agent,
  });

  // Upload a single file. Files >1.9MB are automatically chunked.
  const fileBuffer = readFileSync("./photo.jpg");
  const key = await assetManager.store(fileBuffer, {
    fileName: "photo.jpg",
    contentType: "image/jpeg",
    path: "/uploads",
  });

  const assets = await assetManager.list(); // list all assets
  await assetManager.delete("/uploads/old-photo.jpg");

  const files = readdirSync("./dist");
  for (const file of files) {
    const content = readFileSync(`./dist/${file}`);
    await assetManager.store(content, { fileName: file, path: "/" });
  }
}

manageAssets();
```

## Authorization for Uploads (legacy: three roles)

The legacy asset canister has a built-in permission system with three roles (least → most privileged):

- **Prepare** — upload chunks and propose batches, but cannot commit them live.
- **Commit** — upload and commit assets (make them live). Standard role for deploy pipelines.
- **ManagePermissions** — grant and revoke permissions to other principals.

```bash
# Grant "prepare" (upload but not commit) — preview/staging
icp canister call frontend grant_permission '(record { to_principal = principal "<principal-id>"; permission = variant { Prepare } })'

# Grant commit (publish assets) — deploy pipelines
icp canister call frontend grant_permission '(record { to_principal = principal "<principal-id>"; permission = variant { Commit } })'

# Grant permission management
icp canister call frontend grant_permission '(record { to_principal = principal "<principal-id>"; permission = variant { ManagePermissions } })'

# List / revoke
icp canister call frontend list_permitted '(record { permission = variant { Commit } })'
icp canister call frontend revoke_permission '(record { of_principal = principal "<principal-id>"; permission = variant { Commit } })'
```

(In certified-assets this collapses to a single `authorize(principal)` set plus controllers — see the main SKILL.md.)

> **Security Warning:** `icp canister settings update frontend --add-controller <principal-id>` grants full canister control — not just upload permission. Only add controllers when you genuinely need full administrative access.

## Content Encoding & Verify (legacy)

The legacy canister compresses assets with gzip and brotli automatically. To inspect, and to verify a deploy:

```bash
# List uploaded assets
icp canister call frontend list '(record {})'
# → [{ key = "/index.html"; content_type = "text/html"; ... }, ...]

# Fetch the index page (certified)
icp canister call frontend http_request '(record {
  url = "/"; method = "GET"; body = vec {}; headers = vec {};
  certificate_version = opt 2;
})'
```

(Note `list` is a legacy method; the certified-assets canister does not expose it — verify a static-site deploy with `http_request` instead.)
