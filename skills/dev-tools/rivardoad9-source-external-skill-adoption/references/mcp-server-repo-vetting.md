# Vetting an agent-tooling repo (CLI + MCP server) before adopting it

Some repos aren't apps, they're *tools for agents* — a CLI that also ships an MCP server. The
question changes from "is this code safe" to "does it start, what does it really expose, and what
does it cost me to run it and to register it".

## Steps

1. **Run it through npx, don't build it.** `npx -y <pkg>@latest --version` then `--help`. Grep the
   help — an analysis toolkit can expose 70+ subcommands and pasting them all into context is waste.
2. **Ask the tool about its own environment**: `doctor --json`, `capabilities --json`. They report
   which engines are installed and which capability families are live *on this OS*, instead of you
   guessing from the README's feature list (e.g. on Linux a macOS-only capability set is dead weight,
   while static JS/.NET/artifact analysis needs no engine at all).
3. **Check the host's platform (Hermes) side**: `hermes mcp list` / `hermes mcp catalog` — if the
   server isn't in the catalog it's a manual `hermes mcp add`, and worth knowing before promising an
   easy install.
4. **Prove the MCP handshake BEFORE offering to wire it in.** Docs advertise more tools than the
   published build ships (observed: docs/catalog 131 vs the running server's **125**). Run
   `scripts/mcp_stdio_probe.py -- <server cmd...>` — it performs initialize + tools/list over stdio
   and prints serverInfo, protocolVersion and the real tool count.
5. **Supply-chain pass** (JS flavour): install hooks
   (`jq '.scripts | to_entries[] | select(.key|test("postinstall|preinstall|prepare"))' package.json`),
   outbound URLs in `src/`, telemetry/analytics identifiers, submodule list, and what the installer
   downloads (`grep -nE 'https?://|curl|wget|rpm|apt-get' install.sh`). A `prepare` hook that only
   sets up git hooks is fine; an installer that pulls native engines (Ghidra/Hopper/IDA, firmware
   toolchains) is a decision, not a side effect.
6. **Budget the output before you run anything real.** Analysis toolkits emit evidence bundles, not
   summaries: one 12 MB app produced a **67 MB** JSON (with 17k AST nodes, 308 findings, and an
   explicit `limitations` list). Always `> /tmp/out.json` and query with `jq`; never load it into
   context or `json.load` it on a small-RAM host.
7. **Check the host before running heavy analysis.** Bundlers/decompilers are RAM-hungry and the
   "medium" probe artifact is often a multi-MB minified bundle: a 5 MB package OOM'd node at the
   default ~1 GB heap on a 1.9 GB box, while a 12 MB package needed
   `NODE_OPTIONS=--max-old-space-size=1400`. Cap the heap, shrink the target, or run the tool on
   another machine and point the agent at it over MCP. Never discover this by swapping out the
   services that share the box.
8. **Wiring decision**: register only the tool subset that matches a named, recurring job (each MCP
   tool costs context in *every* future session), and say plainly what is *not* your lane — a RE
   toolkit is not a substitute for on-chain/EVM analysis or a content pipeline.

## Worked example (7 Oct 2026, `morluto/rea`)

12k★ MIT TypeScript RE toolkit; CLI `rea-agents@4.1.0` + MCP server. Verified by running: node 26.7
accepted; `doctor` healthy=false only for missing native engines (no Hopper/Ghidra/IDA) and no agent
registrations; static JS analysis of a 12 MB Node app succeeded (50 relevant files, 42 JS parsed,
17,424 AST nodes, 308 findings, graph of artifact/electron-main/electron-renderer/endpoint nodes);
MCP handshake OK, `serverInfo rea 4.1.0`, protocol 2024-11-05, 125 tools. Supply chain clean (no
telemetry identifiers, no postinstall). Genuine fit for this user = auditing third-party
apps/tools/dashboards; no fit for trading-engine or content work.

## Browser/CDP-based analysis (when the target is a live web app)

The web-bundle path needs a **loopback CDP endpoint plus a target id** — you launch the browser, the
tool attaches: `chrome --headless --remote-debugging-port=9333 <url>`, then
`list-browser-targets <endpoint>` → `analyze-web-bundle <endpoint> <targetId>`. A Playwright cache
install puts the binary at `~/.cache/ms-playwright/chromium-<v>/chrome-linux64/chrome` (note
`chrome-linux64`, not `chrome-linux`). Sites behind Cloudflare answer `curl` with an interstitial
("Just a moment…"), which is a reason to use the browser path — not a reason to give up on the site.
Watch RAM: a headless browser plus the analysis pass on the same small box is where an unrelated
service gets OOM-killed; free the browser process when the run is done.
