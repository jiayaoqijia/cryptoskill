# Case: adopting `morluto/rea` (reverse-engineering MCP toolkit)

Worked example of this skill end to end. Repo: https://github.com/morluto/rea · npm `rea-agents` · MIT ·
TypeScript · GitHub API: 11.994 ⭐ · 1.283 fork · created 2026-04-14 · 185 commits · 24 MB
(src 16 MB / tests 3,2 MB / docs 2 MB / scripts 1,3 MB / bridge 296 KB / skills 48 KB).
5 third-party submodules (binwalk, unblob, jadx-headless-mcp, ghidra-nativeaot, wakaru) — not vendored, so not
a copy-paste repo.

Supply-chain read: no telemetry/analytics (grepped `telemetry|analytics|sentry|posthog` — only internal
comments plus `DOTNET_CLI_TELEMETRY_OPTOUT=1` in its own test scripts), no `postinstall` (only a husky
`prepare`), outbound URLs in src limited to json-schema.org and www.hopperapp.com, and `install.sh` only
resolves a GitHub release while Hopper stays an explicitly consented optional download.

## What running it produced (v4 line)

- `--version` → `4.1.0`; `--help` → **~70 subcommands** (analyze / decompile / trace / inspect / compare /
  capture / evidence-export …).
- `doctor --json` → `healthy:false`, and the detail matters: node 26.7 ✓ · host ubuntu 24.04 ✓ · `hopper` ❌ ·
  `ghidra` ❌ (`GHIDRA_INSTALL_DIR` unset) · `ida-registration` ❌ · `skill:identity` ❌ (no agent registration
  yet — the v4 line had no setup command, Hermes registration was manual).
- `capabilities --json` → live providers `rea-artifact-graph`, `rea-dotnet-static`; dead ghidra/hopper/ida;
  `capture_native_ui_scenario` → `unsupported_host` ("Native macOS utilities require macOS").
- **Static JavaScript needs no engine** — the key to the whole verdict:
  `analyze-javascript-application /…/systray2 --json` (12 MB target, `NODE_OPTIONS=--max-old-space-size=1400`)
  → exit 0, **67 MB** evidence JSON: 50 relevant files · 42 JS files parsed · **17.424 AST nodes** · 308 findings
  · 0 parse failures · graph = 42 javascript-asset + 9 artifact + 6 electron-main + 1 electron-renderer + 1 endpoint.
  Its own stated limitation: *"JavaScript and HTML were parsed as inert text; bundle bootstrap code was never
  executed."* → findings are static, never runtime proof.
- 5 MB target (`gmgn-cli`, a big browser bundle) → **OOM crash** at the default 1 GB heap
  (`FATAL ERROR: Ineffective mark-compacts near heap limit`). Host at the time: 1,9 GB RAM, 875 MB swap used.
- **Web** — requires its own loopback CDP browser (`list-browser-targets <endpoint>` then
  `analyze-web-bundle <endpoint> <target_id>`):
  - `lynk.id/…` → target showed only `Just a moment...` plus a `challenges.cloudflare.com` iframe →
    **Cloudflare blocks plain headless** (target limitation, not tool breakage).
  - `zemizdigital.vercel.app` (our own site, chosen on purpose to ground-truth accuracy) → 1 script (8.208 B,
    sha256), 1.130 AST nodes, **0 endpoints**, completeness `complete`, confidence `observed` → matched reality.
- **APK**: `inspect-android-package app.apk` (real 12,5 MB F-Droid APK) →
  `{"code":"capability_unavailable","details":{"provider_id":"jadx","reason":"Set REA_JADX_MCP_JAR to the
  absolute path of a caller-supplied jadx-headless-mcp 0.7.1 JAR. REA does not download or install it."}}`.
- **MCP (v4)**: `npx -y rea-agents@4.1.0 mcp` → handshake OK, `serverInfo {name: rea, version: 4.1.0}`,
  protocolVersion `2024-11-05`, **125 tools at runtime** (catalog/README claimed 131). Registered by hand with
  `hermes mcp add rea --command npx --args -y rea-agents@4.1.0 mcp`.

## Later release: the kit self-registers

The v6 line replaced manual wiring with `setup`, and the shipped binary layout changed (a 66 MB `linux-x86_64`
tarball containing `bin/craft-style` GUI **and** `bin/rea-cli`-equivalent; only the CLI works headless).

```bash
npx -y rea-agents@latest setup --help      # options: --dry-run, --client <id>, --yes, --all-detected
npx -y rea-agents@latest setup --dry-run --all-detected --format json > /tmp/plan.json
npx -y rea-agents@latest setup --client hermes --yes
```

Plan shape that makes approval easy (four actions, both clients):

| kind | target | operation |
|---|---|---|
| `configure_client:hermes` | `/home/<user>/.hermes/config.yaml` | update, backs up to `config.yaml.rea.backup` |
| `install_skill:hermes` | `~/.hermes/skills/reverse-engineer-anything` | install |
| `configure_client:claude_code` | `~/.claude.json` | update, backs up to `.rea.backup` |
| `install_skill:claude_code` | `~/.claude/skills/reverse-engineer-anything` | install |

No provider env vars, no external downloads, no engine install unless `--install-hopper` is also passed.

Engine gate that bit: `npm warn EBADENGINE … required: ^22.23.4 || ^24.22.1 || >=26.12.1, current v22.23.2`,
and the dry-run then came back with an **empty `plannedActions`** plus a `remediation` sentence about Node.
Fix without touching the host default: `nvm install 22.23.4` and prepend `~/.nvm/versions/node/v22.23.4/bin`
to `PATH` for the run.

Verification after applying (`--client hermes`):

- `~/.hermes/config.yaml` gained `mcp_servers.rea` = `command: npx`, `args: [-y, rea-agents@6.8.0, mcp]`, `enabled: true`.
- `doctor --format json` → `identity.registrations` shows `('hermes','aligned')`, skill `installed_version 49`,
  `installed_tool_count 229`, no remediation. Claude Code stayed `missing` — proof the scope really was narrow.
- Live stdio handshake → `serverInfo {name: rea, version: 6.8.0}`, **229 tools** (`inspect_desktop_application`,
  `inspect_model_artifact`, `inspect_native_instruction`, `annotate_native_function`, …).
- 229 tool schemas is a real per-session context bill; the honest follow-up is to offer `enabled: false` and
  drive the CLI directly, or to expose a subset.

## Verdict delivered

Worth it, but only for one narrow job, stated explicitly: **"third-party artifacts before we trust them"** —
breaking open someone else's tool/app/web bundle instead of trusting their claims. Explicit NOT-use-cases: the
trading engine (Python + EVM on-chain, a different world), content/video, Threads. Do not install native
engines on the live box; do not run big-bundle analysis on the box that also serves the production engine.
Recommended cheapest reversible step: register the MCP server with only the JS/web tools enabled, plus its
bundled skill — with the per-session context cost stated.

## Transferable lessons

- Evidence payloads are huge (67 MB for a 12 MB target) → save to file, summarise with `jq`, use filter flags.
- `capabilities`/`doctor` first, before promising APK/native capability to the user.
- Raise the heap with `NODE_OPTIONS=--max-old-space-size=…` only after checking `free -m`.
- `pkill -f "chrome-headless"` kills its own shell (the pattern matches the shell command line) → use
  `pkill -f "chrome[-]headless"`.
- Driving a headless browser for CDP capture: `--headless=new --no-sandbox --disable-gpu
  --disable-dev-shm-usage --remote-debugging-port=… --user-data-dir=…` (Playwright chromium lives at
  `~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome`).
- Clean up afterwards and prove it: kill the browser/server you spawned, delete giant evidence files and temp
  profiles, then show `ps -eo pcpu,rss` + `free -m` — leave nothing hanging on a production host.
