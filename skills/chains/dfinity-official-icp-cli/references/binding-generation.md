# Binding Generation

icp-cli does not have a built-in `dfx generate` command. Use `@icp-sdk/bindgen` (>= 0.4.0) to generate TypeScript bindings from `.did` files. The generated code imports `@icp-sdk/core`, which the project installs itself — `@icp-sdk/bindgen` does not depend on it.

## Vite plugin (recommended)

For Vite-based frontend projects:
```js
// vite.config.js
import { icpBindgen } from "@icp-sdk/bindgen/plugins/vite";

export default defineConfig({
  plugins: [
    // Add one icpBindgen() call per canister the frontend needs to access
    icpBindgen({
      didFile: "../backend/backend.did",
      outDir: "./src/bindings",
    }),
    icpBindgen({
      didFile: "../other/other.did",
      outDir: "./src/bindings",
    }),
  ],
});
```

Each `icpBindgen()` instance generates a `<canister-name>.ts` file (named after the `.did` file) in its `outDir` containing a `createActor` function. Add `**/src/bindings/` to `.gitignore`.

## Creating actors from bindings

Connect the generated bindings with the `ic_env` cookie. Pass `{ agentOptions }` and let the binding build the agent (for identity, pre-built agents and exceptions, see "Agent options" below).

```js
// src/actor.js
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";
import { createActor } from "./bindings/backend";
// For additional canisters: import { createActor as createOther } from "./bindings/other";

const canisterEnv = safeGetCanisterEnv();
// Do NOT set host. The agent's default host resolution already picks the right
// API endpoint everywhere: on known gateway origins (ic0.app, icp0.io,
// localhost, 127.0.0.1) it uses the page origin — so the local gateway and the
// Vite dev-server /api proxy keep working — and anywhere else, including custom
// domains and icp.net, it falls back to https://icp-api.io. Hardcoding
// host: window.location.origin breaks frontends served from a custom domain:
// the custom domain is only the HTTP gateway and does not serve /api/v2 (see
// the custom-domains skill).
const agentOptions = {
  rootKey: canisterEnv?.IC_ROOT_KEY,
};

// Let the binding build the agent from agentOptions
export const backend = createActor(
  canisterEnv?.["PUBLIC_CANISTER_ID:backend"],
  { agentOptions }
);
// Repeat for each canister: createOther(canisterEnv?.["PUBLIC_CANISTER_ID:other"], { agentOptions })
```

## Non-Vite frontends

Use the `@icp-sdk/bindgen` CLI to generate bindings manually:
```bash
npx @icp-sdk/bindgen --did-file ../backend/backend.did --out-dir ./src/bindings
```

## `opt T` is `T | null` in the wrapper, not `[] | [T]`

`@icp-sdk/bindgen` generates two layers: raw declarations under `src/bindings/` use the standard `@icp-sdk/core` Candid representation where `opt T` is `[] | [T]`, and a wrapper class that converts this to idiomatic `T | null`. Since `createActor` returns the wrapper, always use `T | null`:

```ts
// Wrong — raw Candid style (only applies if using declarations directly)
const result = await backend.getNickname();
if (result.length > 0) { name = result[0]; }

// Correct — wrapper returns T | null
const result = await backend.getNickname();
if (result !== null) { name = result; }
```

## Agent options

The example above is for browser code calling the network that serves the page.

- **Identity:** add `identity` to `agentOptions` for authenticated calls.
- **`rootKey`:** when calling the network that serves the page, set it from the cookie. Without it, the agent defaults to the mainnet root key, and every call against a local network fails verification. A page calling a different network must not pass it (see below).
- **A pre-built `{ agent }`** also works and is used as-is. Build it with `await HttpAgent.create({ identity, rootKey })` (plus `host` where the rules below require it), not the deprecated `new HttpAgent()`. `agentOptions` is ignored when you pass `agent` (passing both logs a console warning), so these options go into `create`. `create` returns a Promise, and passing it un-awaited fails at the first call with `agent.query is not a function` or `agent.update is not a function`. `{ agentOptions }` makes the binding call `HttpAgent.createSync(agentOptions)`.

Set `host` explicitly only when the default cannot know the target:

- **Outside the browser** (Node scripts, tests): there is no page origin and no `ic_env` cookie, so the agent defaults to `https://icp-api.io` and the mainnet root key. For a local network, read both from `icp network status --json`:
  ```js
  import { execFileSync } from "node:child_process";
  const { api_url, root_key } = JSON.parse(
    execFileSync("icp", ["network", "status", "--json"], { encoding: "utf8" })
  );
  const backend = createActor(canisterId, {
    agentOptions: { host: api_url, rootKey: Uint8Array.from(Buffer.from(root_key, "hex")) },
  });
  ```
- **A page calling a different network than the one serving it** (e.g. mainnet canisters from a local dev server): set `host: "https://icp-api.io"` and do not pass the local `IC_ROOT_KEY` (see the `wallet-integration` skill).

## Requirements

Install both packages in the frontend project (note the minimum versions):
```bash
npm install @icp-sdk/core@^6
npm install -D @icp-sdk/bindgen@^0.4.0
```

**Pin `@icp-sdk/core` to `^6`; do not take `latest`.** `@icp-sdk/auth`, `@icp-sdk/signer`, `@icp-sdk/canisters` (>= 4) and `@dfinity/utils` (>= 5) all peer `@icp-sdk/core@^6`, so a project that lands on a different major fails to install with `ERESOLVE`. Do not use `--legacy-peer-deps` to get past that — it skips the peer check and installs the mismatched pair anyway, so the incompatibility surfaces at runtime instead of at install time.

- The `.did` file must exist on disk before the frontend builds. The recommended workflow: generate the `.did` file once (see SKILL.md pitfall #16), commit it to the repo, and specify `candid:` in the recipe config. If `candid` is omitted, the recipe auto-generates the `.did` into the build cache at a non-deterministic path that bindgen cannot reference — so always commit the `.did` and set `candid:` when using bindgen.
- `@icp-sdk/bindgen` (>= 0.4.0) emits code that imports `@icp-sdk/core`; bindgen itself depends only on `commander`, so the project installs core separately (see the pin above). Projects using `@dfinity/agent` must upgrade to `@icp-sdk/core` + `@icp-sdk/bindgen`. This is not optional — there is no way to generate TypeScript bindings with icp-cli while staying on `@dfinity/agent`.
