---
name: icp-deploy-check
description: Pre-deploy safety gate for an Internet Computer Rust canister (ic-cdk). A fast, read-only checklist for the five deploy-time footguns that brick a canister or let anyone drain it - anonymous-principal access, fetch_root_key in shipped code, unguarded admin methods, pre_upgrade traps, single controller - with grep signals, the tracing rules to confirm each hit, and a PASS/FAIL/REVIEW report. Use before `icp deploy -e ic` (or `dfx deploy --network ic`), in CI, or when asked whether a canister is ready or safe for mainnet. For the secure-coding patterns themselves, use canister-security.
license: Apache-2.0
compatibility: "a local Rust canister repo (ic-cdk >= 0.18); ripgrep; no network, no mainnet action"
metadata:
  title: ICP Deploy Check
  category: Security
---

# ICP deploy check

Run this static, read-only gate over a Rust canister repo **before** a mainnet
deploy. It reads source and reports; it never deploys, never calls mainnet, never
needs a key. The fix patterns behind each check live in the `canister-security`
skill — this skill is the checklist, that one is the reference.

Scope: every update entrypoint and the `init`/`pre_upgrade`/`post_upgrade` hooks
in the Rust `ic-cdk` canister(s), plus any frontend or agent code in the same repo
(check #2 only). Produce one row per check: `PASS` / `FAIL` / `REVIEW` / `N/A`
with `file:line` evidence.

## Enumerating update entrypoints

Checks #1 and #3 both start from the full list of update methods. Match the
attribute with or without arguments — `#[update(guard = "...")]`,
`#[update(name = "...")]` and `#[ic_cdk::update(manual_reply = true)]` are all
entrypoints:

```bash
rg -n -A4 '#\[(ic_cdk::)?update\b'
```

`\b` matches both `update]` and `update(`; a bare `'update\]'` pattern silently
skips every parameterized entrypoint. Record each method's name, its attribute
arguments (especially `guard = "..."`), and its body.

Callers are read with `ic_cdk::api::msg_caller()` (ic-cdk >= 0.18). Older code
uses `ic_cdk::caller()` / `ic_cdk::api::caller()` — treat them as equivalent when
tracing.

## The five checks

### 1. Anonymous principal reaches a state change — FAIL if reachable
Every state-changing update must reject `Principal::anonymous()` **before** its
first mutation.

- **Trace, don't pattern-match.** For each update that mutates state (writes a
  `thread_local!`/stable structure, credits/debits a balance, mints, sets
  config, makes a state-changing inter-canister call), confirm that on every path
  to the mutation the call is rejected (`trap`, `Err` return, or guard `Err`)
  when the caller is anonymous. Accept any of:
  - an explicit comparison against `Principal::anonymous()` (`==` with trap/return,
    or `!=` gating the mutation), on `msg_caller()` or a variable bound to it;
  - a `guard = "fn_name"` attribute — **open `fn_name`** and confirm its body
    returns `Err` for the anonymous principal;
  - a controller/owner/allowlist check that rejects the caller (anonymous can never
    be a controller). An owner-equality check counts only if the owner can never
    be anonymous — `RefCell::new(Principal::anonymous())` as the default owner
    with no `require_authenticated` first means anonymous **is** the owner until
    `init` runs.
- **Not authentication** — FAIL if these are the only "guard":
  - `CallerGuard` / per-caller locks / `PENDING` sets: these are reentrancy
    locks, they accept the anonymous principal like any other;
  - a guard identified only by its name (`require_caller`, `check_access`, ...)
    without reading its body;
  - `is_controller(...)` or a comparison whose result is computed but never acted
    on, or that runs after the mutation.
- An update that is deliberately open to anonymous callers (e.g. a public
  counter, an open sign-up whose cost is bounded) is `REVIEW`, not `FAIL` — state
  why it is intended. Query methods cannot persist state and are out of scope.

### 2. `fetch_root_key` in shipped code — FAIL if present
`fetch_root_key()` (Rust `ic-agent`) / `fetchRootKey()` (JS agent) fetches the
root public key **from the replica it is talking to** and trusts it. If that code
runs against mainnet, a man-in-the-middle can substitute its own key and forge
every certified response. This lives in frontend or agent/client code, not in
the canister, so scan the whole repo:

```bash
rg -n 'fetch_root_key|fetchRootKey|shouldFetchRootKey'
```

- **FAIL** on any occurrence in a shipped frontend or client path — **even behind
  an environment check** (`if network === "local"`, `process.env.DFX_NETWORK`,
  `#[cfg(feature = "local")]`): environment branching is how the call leaks into
  production builds. The fix is to stop fetching it: pass the root key from the
  `ic_env` cookie (`IC_ROOT_KEY`, via `safeGetCanisterEnv()`) as `rootKey` to
  `HttpAgent.create()`. See `canister-security` for the full pattern.
- **Not a finding:** test-only code (`#[cfg(test)]`, `tests/`, PocketIC
  harnesses, scripts that only ever target a local replica) — mark `PASS` with a
  note.

### 3. Unguarded admin / privileged method — FAIL if not privileged-guarded
Mint / burn / migrate / upgrade / config / `set_*` / withdraw updates must be
restricted to a controller, owner or admin — not merely to authenticated users.

- **Candidates:** from the enumerated update list (not a separate grep), take every
  method whose name contains — anywhere, not only as a prefix —
  `(?i)(mint|burn|admin|migrate|upgrade|config|set_|withdraw|transfer_from|owner|controller|pause|allowlist|whitelist)`.
  Name matching only finds candidates: an update whose visible body changes fees,
  ownership, other users' balances, or canister-wide settings is privileged
  regardless of its name. A user-facing method acting on the caller's own account
  (`deposit`, `transfer`, `claim`) is not privileged — it belongs to check #1. Do
  not speculate about helpers whose bodies you cannot see (`credit(...)`): judge
  the code shown and note what is out of view.
- **PASS only if** the method (or the body of its `guard = "..."` function) rejects
  the call unless the caller is a controller (`is_controller(&caller)` acted on),
  the owner, or a member of an admin set.
- **FAIL if** the only protection is anonymous rejection. `guard =
  "require_authenticated"`, or a body that only checks `!= Principal::anonymous()`,
  still lets **any** signed-in principal call `set_config`. A `guard =` attribute
  is evidence of nothing until you have read the guard function.

### 4. `pre_upgrade` trap risk — REVIEW
A `pre_upgrade` that serializes a large or unbounded heap can exceed the
instruction limit and **trap**, making the canister permanently un-upgradeable.

- **Detect:** `rg -n '#\[(ic_cdk::)?pre_upgrade\b' -A10`. `REVIEW` any `pre_upgrade`
  that serializes (`stable_save`, `candid::encode_*`, `serde`) a collection
  (`Vec`/`HashMap`/`BTreeMap`/`String`) whose size users can grow. `PASS`/`N/A`
  when state lives in `ic-stable-structures` and there is no manual copy.
- Recommend bounding the data or moving it into `ic-stable-structures`.

### 5. Single controller / no backup — REVIEW (operator, deploy-time)
A canister controlled by one principal — especially a plaintext dev identity — is
one lost or compromised key from being unrecoverable or silently re-coded.

- **Detect:** this is not visible in source. Ask for, or have the operator run,
  `icp canister status <name> -e ic` (legacy: `dfx canister info <id> --network
  ic`) and read the controller list. Require a threshold/multisig controller
  (e.g. an orbit station or SNS) or a documented backup controller principal held
  offline. A single controller is `REVIEW`, not an automatic `FAIL`.

## Report format

```
Target: <crate> (Rust ic-cdk canister) — N update methods
[FAIL  ] #1 src/lib.rs:42 claim_bonus — credits balance, no anonymous rejection
[FAIL  ] #3 src/lib.rs:57 set_config — guard require_authenticated rejects only anonymous; needs controller/owner check
[PASS  ] #2 no fetch_root_key / fetchRootKey in shipped code
[N/A   ] #4 no pre_upgrade; state in ic-stable-structures
[REVIEW] #5 controller set — operator to confirm a backup/multisig controller
Verdict: NOT ready to deploy (2 FAIL)
```

A grep hit is a **candidate**: open the `file:line`, trace the guard, and only
then mark `FAIL`. A `PASS` must also be traced — a guard attribute or a guard-like
name proves nothing on its own. When no source is available, say so and list what
you would check rather than inventing `file:line` evidence.

## Boundaries

This is a fast pre-deploy gate, not a full audit. It does not cover TOCTOU across
`await`, callback-trap ordering, cycle-drain economics, or unbounded storage
growth — see the `canister-security` skill for those. It performs **no** network
or mainnet action.
