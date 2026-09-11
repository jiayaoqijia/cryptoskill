---
name: dexe-setup
description: |
  Guided setup journey for dexe-mcp. Explains that reads work with ZERO config,
  then walks the user through only the keys that unlock more — signing, DAO/
  proposal creation (Pinata JWT), and optional reliability upgrades — telling
  them for each one exactly what breaks if they skip it. Drives from
  `dexe_doctor`, edits `.env` (NEVER `.claude.json`), and tells them to restart.
  Triggered by `/dexe-setup`, or proactively when a tool reports a missing key
  ("DEXE_PINATA_JWT is required…", "public RPC unstable", "shared public defaults").
---

# dexe-setup

## What this does

A guided onboarding journey for `dexe-mcp`. The plugin ships with sane public
defaults, so **reads work the moment it's installed** — no keys required. This
skill's job is to explain that reality and then help the user unlock the parts
that *do* need a key, one tier at a time, always saying what they lose by
skipping. It drives from the `dexe_doctor` tool — no guessing which file or key.

## The two-tier reality (say this first)

Open by orienting the user:

> **Reads already work** — DAO info, treasury, holders, proposals, subgraph
> queries, IPFS reads all run on shared public defaults with zero setup.
> You only need to configure something to **write** or to **create DAOs/
> proposals**. Want me to walk you through it, or are reads all you need?

If reads are all they need: confirm they're done, mention `dexe_doctor` is there
if anything misbehaves, and stop.

## When to invoke

- The user types `/dexe-setup`.
- The user says "set up dexe", "enable writes", "I want to create a DAO/
  proposal", "how do I configure dexe-mcp?".
- You see a tool result containing any of: `"DEXE_PINATA_JWT is required"`,
  `"Missing required env"`, `"public RPC unstable"`, `"public IPFS gateways
  are failing"`, `env.sharedDefaults` — invoke proactively.

## Hard rules (do not violate)

1. **Never write `DEXE_*` values to `.claude.json`.** The MCP host's env block
   SHADOWS `.env` silently. Write env to a `.env` file the server actually
   loads. For a **plugin / `npx` install** that is **`~/.dexe-mcp/.env`** (the
   cwd-independent home config — works from any folder on any OS; same dir as
   `state.json`). Only a **source checkout** uses the repo-root `.env`. Since
   0.23.1 the server loads `$DEXE_ENV_FILE` → `<cwd>/.env` → `~/.dexe-mcp/.env`
   → `<pkgdir>/.env`; the doctor/banner shows which file it loaded. Do NOT put
   config in a project `.env` for plugin use — the plugin's working directory is
   not your project, so it is silently missed.
2. **Never write `DEXE_PRIVATE_KEY` without explicit user opt-in.** Signing is
   available by default via WalletConnect (below) — reach for a hot key only if
   the user insists, and warn it lives in plaintext on disk.
3. **Always tell the user to restart Claude Code after editing `.env`.**
   `process.loadEnvFile()` runs once at startup; mid-session edits do nothing
   until restart.
4. **Cap the doctor loop at 3 iterations.** After three doctor → fix → restart
   cycles still failing, stop and present the full report for manual triage.

## The setup tiers (walk in order; for each, state what breaks if skipped)

### Tier 0 — Reads (nothing to do)
On-chain reads, subgraph reads, backend reads, IPFS reads all work on shared
public defaults. **Skip cost: none.** The only downside is the shared Graph API
key + public RPC/IPFS gateways are rate-limited and billable-shared — fine for
light use, upgrade under Tier 3 for heavy use.

### Tier 1 — Signing (to vote / execute / broadcast)
WalletConnect is **available by default** (shared project id). To sign: run
`dexe_wc_connect`, scan the QR with a wallet, approve each tx on your phone. No
key touches disk.
- **Skip cost:** you can build calldata and read, but can't broadcast.
- Optional: set your own `DEXE_WALLETCONNECT_PROJECT_ID` (free at
  cloud.reown.com) to stop sharing the default id.
- Only if the user *insists* on unattended/CI signing → hot key ladder below.

### Tier 2 — Creating DAOs / proposals (the one hard blocker)
Creating a DAO or proposal pins metadata to IPFS, which needs a **Pinata JWT**
(`DEXE_PINATA_JWT`). This is the only thing reads/signing can't default around.
- **Skip cost:** `dexe_dao_create`, `dexe_proposal_create`, and metadata uploads
  refuse up front (no on-chain tx is attempted).
- How to get one (say this to non-technical users): sign up free at
  https://app.pinata.cloud → API Keys → New Key → enable `pinJSONToIPFS` and
  `pinFileToIPFS` → copy the JWT.
- Validate it before saving: `GET https://api.pinata.cloud/data/testAuthentication`
  with header `Authorization: Bearer <jwt>` should return `{"message":
  "Congratulations! ..."}`. (The `npx dexe-mcp init` wizard does this check for you.)

### Tier 3 — Reliability upgrades (optional, offer when errors appear)
- **Private RPC** — if a read fails with *"public RPC unstable"*: set
  `DEXE_RPC_URL_MAINNET` (chain 56) / `DEXE_RPC_URL_TESTNET` (chain 97) to an
  Alchemy / QuickNode / Ankr URL. **Skip cost:** occasional rate-limit flakiness.
- **Dedicated IPFS gateway** — if a read fails with *"public IPFS gateways are
  failing"*: set `DEXE_IPFS_GATEWAY` (a free Pinata dedicated gateway comes with
  your JWT — `https://<subdomain>.mypinata.cloud`). **Skip cost:** slower/flaky
  metadata reads.
- **Own Graph key** — if `dexe_doctor` shows `env.sharedDefaults`: set your own
  `DEXE_SUBGRAPH_*_URL` (with your Graph key embedded, or `DEXE_GRAPH_API_KEY`).
  **Skip cost:** you share a rate-limited, billable key.

## Algorithm

1. Call `dexe_doctor` (no input).
2. Read `summary` and `checks` from the structured response.
   - `summary.status === "pass"` (only warnings) → reads are healthy. Ask which
     tier (if any) the user wants; don't block on warnings.
   - Treat `warn` checks (`chain.publicRpcFallback`, `env.sharedDefaults`) as
     *offers*, not problems.
3. For each `fail` or the user's chosen tier, collect the env key(s). Use the
   check's `remediation` verbatim for network failures.
4. Batch questions by tier/category with `AskUserQuestion` — one question per
   tier, not one per key. Only ask for what the chosen tier needs.
5. Locate the `.env` the server loads (the doctor/banner shows the path). For a
   plugin/`npx` install use `~/.dexe-mcp/.env` (create the `.dexe-mcp` dir if
   absent); for a source checkout use the repo-root `.env` (where `package.json`
   lives). When unsure, prefer `~/.dexe-mcp/.env` — it loads on every OS from any
   folder.
6. Edit that `.env` with the Edit tool: replace the key's line if present, else
   append `KEY=value` (preserve the trailing newline).
7. Tell the user, verbatim:
   > Edits saved to `.env`. **Restart Claude Code** so the new values load
   > (quit and relaunch). Then I'll re-run `dexe_doctor` to confirm.
8. After restart, re-run `dexe_doctor`. If still failing, go to step 3. Iterate
   at most 3 times.
9. After 3 iterations still failing, present the full `checks` array — remaining
   issues need manual triage (bad credentials, suspended account, paid-plan
   required, corporate proxy).

## Signer mode escalation

If the user wants signing beyond phone-approval WalletConnect, walk this ladder
(top = safest):

1. **WalletConnect (default).** `dexe_wc_connect` → approve on phone. No key on
   disk. This is already available; prefer it.
2. **Safe multisig (`DEXE_SAFE_TX_SERVICE_URL`).** Proposes tx to a Safe; owners
   co-sign separately.
3. **Hot key (`DEXE_PRIVATE_KEY`).** Plaintext on disk. Convenient for CI bots,
   dangerous for humans. Show this before writing:
   > Setting `DEXE_PRIVATE_KEY` stores your key in plaintext at `.env`. Anyone
   > who reads the file can drain that wallet. Are you sure you don't want
   > WalletConnect (already available) or a Safe multisig instead?
4. Refuse to proceed to a hot key without an explicit "yes" confirming the
   trade-off.

## .env precedence trap

If `dexe_doctor` returns a check named `env.<KEY>` with "shadowed by host env
block", the same key is defined in BOTH `.env` and `.claude.json`. The host
wins. Tell them to keep it in one place (prefer `.env`) and restart.

## Useful tools (reference)

- `dexe_doctor` — diagnostic (read-only, safe to call repeatedly).
- `dexe_context` — signer/mode + env readiness + `usingSharedDefaults` list.
- `npx dexe-mcp doctor` — CLI form; useful when the MCP server failed to start.
- `npx dexe-mcp init` — fresh-start wizard (prompts + live-validates Pinata JWT).
  Overwrites `.env`; use for new installs, not for fixing an existing setup.
