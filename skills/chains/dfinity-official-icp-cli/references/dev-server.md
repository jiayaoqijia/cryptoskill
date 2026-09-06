# Dev Server Configuration (Vite)

In development, the Vite dev server must simulate the `ic_env` cookie that the frontend canister (static-site or asset canister) provides in production.

## Prerequisites

The dev server configuration queries the local network for backend canister IDs and the root key. Before running `vite dev`:

1. Start the local network: `icp network start -d`
2. Deploy the backend: `icp deploy backend`

Without a running network and deployed backend canisters, `getDevServerConfig()` will fail because `icp network status` and `icp canister status` have nothing to query. The frontend canister does not need to be deployed for local development — Vite serves it directly.

## Configuration

```js
// vite.config.js
import { execSync } from "child_process";

const environment = process.env.ICP_ENVIRONMENT || "local";
// List all backend canisters the frontend needs to access
const CANISTER_NAMES = ["backend", "other"];

function getCanisterId(name) {
  // `--id-only` makes the command print just the canister ID
  return execSync(`icp canister status ${name} -e ${environment} --id-only`, {
    encoding: "utf-8", stdio: "pipe",
  }).trim();
}

function getDevServerConfig() {
  const networkStatus = JSON.parse(
    execSync(`icp network status -e ${environment} --json`, {
      encoding: "utf-8",
    })
  );
  const canisterParams = CANISTER_NAMES
    .map((name) => `PUBLIC_CANISTER_ID:${name}=${getCanisterId(name)}`)
    .join("&");
  return {
    headers: {
      "Set-Cookie": `ic_env=${encodeURIComponent(
        `${canisterParams}&ic_root_key=${networkStatus.root_key}`
      )}; SameSite=Lax;`,
    },
    proxy: {
      "/api": { target: networkStatus.api_url, changeOrigin: true },
    },
  };
}
```

## Mode guard

Only invoke `getDevServerConfig()` when running the dev server, not during production builds. The `command` parameter is `"serve"` for `vite dev` and `"build"` for `vite build`:

```js
export default defineConfig(({ command }) => ({
  plugins: [
    react(),
    icpBindgen({
      didFile: "../../src/backend/backend.did",
      outDir: "./src/bindings",
    }),
  ],
  ...(command === "serve" ? { server: getDevServerConfig() } : {}),
}));
```

Without this guard, `vite build` will execute `icp network status` and `icp canister status` at import time, producing confusing errors or warnings even though the dev server config is irrelevant for production builds.

## Key differences from dfx

- The proxy target and root key come from `icp network status --json` (no hardcoded ports)
- Canister IDs come from `icp canister status <name> -e <env> --id-only` (no `.env` file)
- The `ic_env` cookie replaces dfx's `CANISTER_ID_*` environment variables
- `ICP_ENVIRONMENT` lets the dev server target any environment (local, staging, ic)
