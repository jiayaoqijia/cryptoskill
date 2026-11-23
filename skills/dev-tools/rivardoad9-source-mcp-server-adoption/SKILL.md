---
name: mcp-server-adoption
description: "Use when adopting an external MCP server or agent CLI."
---

# Adopting an external MCP server / agent CLI into Hermes

Trigger: the user drops a repo or a tool and asks *"apakah ini bagus buat di-apply ke kita?"*, or wants an
external tool plugged into Hermes. This is a different class from general repo vetting (`external-repo-vetting`
covers library/strategy repos, upstream diffing, token/on-chain checks — read it too). Here the question is:
**does this thing actually run on our host, can it attach to Hermes, and what will it cost us per session?**

## 1. Run the binary before reading anything else

```bash
npx -y <pkg>@latest --version ; npx -y <pkg>@latest --help | head -80
```

Count the command surface. Agent-oriented repos usually ship a CLI **and** an MCP server; the MCP tools are
what our agent would actually use.

## 2. Readiness gate — which providers are ALIVE on this host

```bash
npx -y <pkg>@latest doctor --json       > /tmp/doctor.json
npx -y <pkg>@latest capabilities --json | head -c 1500
```

Never promise a capability before this. Typical findings: native engines (ghidra / hopper / ida) `not configured`,
macOS-only paths returning `unsupported_host`, some providers healthy with **zero** engines installed (static
analysis paths). An audit-wide `healthy:false` is often normal — read `scope_checks` / `capabilities` entries
instead of the headline flag, and report the dead providers explicitly rather than silently skipping them.

## 3. Probe the MCP handshake ourselves (evidence, not README)

```bash
python3 scripts/mcp_handshake_probe.py npx -y <pkg>@<exact-version> mcp
```

Prints `initialize ok`, `serverInfo`, protocolVersion and the **runtime** tool list. Marketing numbers drift
from reality (a repo advertising a 131-tool catalog advertised 125 at runtime) — quote the runtime number.
Pin one exact version for any persistent registration; `@latest` on every launch makes the tool a moving target.

## 4. Wire it into Hermes — and narrow it

```bash
hermes mcp list                                  # what's already attached
hermes mcp catalog | grep -i <name>              # is it one-click installable?
hermes mcp add <name> --command <cmd> --args <args...>
hermes mcp test <name>                           # verify the connection
hermes mcp configure <name>                      # toggle which tools are exposed
```

**Prefer the tool's own `setup` over hand-registering — but only after reading its plan.** Agent-oriented kits increasingly ship a setup command that registers the MCP server *and* installs its bundled skill; hand-editing `hermes mcp add` then leaves half the integration missing. The order is: plan, show it, then apply the narrowest scope.

```bash
npx -y <pkg>@latest setup --dry-run --all-detected --format json > /tmp/plan.json
echo $?                                        # non-zero output on exit 0 is a version-gate, not a plan
python3 -c "import json;d=json.load(open('/tmp/plan.json'));print(json.dumps(d['plannedActions'],indent=1))"
npx -y <pkg>@latest setup --client hermes --yes    # apply ONLY the client he named
```

A plan worth approving is a list of `plannedActions` with `kind` (`configure_client`, `install_skill`), the exact `target` path, and a `backupPath` for every file it rewrites. If the plan is empty but stdout shows `status: planned`-less output and a `remediation` about Node, read `remediation` first: it is an engine gate, not an empty plan. Packages pinned to `^22.23.4 || ^24.22.1 || >=26.12.1` reject a host sitting one patch below → `nvm install <required>` and run under that `PATH` rather than changing the host default (other services stay on their pinned Node).

**Do only the client he asked for.** "This coding agent" means Hermes; a plan that also offers Claude Code, Cursor and Grok gets applied with `--client hermes` and the rest reported as available-but-skipped. Show the plan before applying, then verify — never report "installed" from the setup command's own toast.

**Always recommend the subset.** Every advertised tool is schema the agent pays for in *every future session*;
125 tools for one occasional use case is a bad trade. Pick the handful tied to the actual use case.

## 4b. Verify a self-registering setup (three independent checks)

A setup that prints `warmed` is not evidence. Check the registration, the skill, and the live server separately:

```bash
grep -n -A6 "<pkg>" ~/.hermes/config.yaml        # registration landed under mcp_servers
grep -n "version" ~/.hermes/skills/<skill>/SKILL.md | head -3
npx -y <pkg>@<exact-version> doctor --format json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print([(r['client'],r['state']) for r in d['identity']['registrations']])"
python3 scripts/mcp_handshake_probe.py npx -y <pkg>@<exact-version> mcp   # runtime tool count
```

Pass condition: the client's registration state reads `aligned`, the skill reports a version and tool count, `doctor` has no `remediation`, and the handshake returns `serverInfo` plus a tool list. Quote the runtime count — a kit that reports 229 tools will cost that schema in **every** session until it is restarted, so state the per-session context price and offer `enabled: false` + CLI-only as the cheaper mode. Config edits do not take effect until the gateway/session restarts; say so instead of implying the tools are live.

## 4c. OAuth-only MCP servers on a headless host

The server answers `401 Missing or invalid Authorization header` until authorized, so a failed `add` proves nothing
about the endpoint. Sequence that works when the user, not the agent, owns the account:

```bash
printf '\ny\n' | hermes mcp add <name> --url <endpoint> --auth oauth   # saves the entry even though it can't connect
hermes config set mcp_servers.<name>.auth oauth                      # only if it saved auth as None
hermes mcp login <name> --flow browser                                # run with pty=true + background=true
```

- `mcp login` needs a TTY and blocks on input: start it as a background pty process and poll its log for the URL. Run it in the foreground and it dies with the turn.
- `--flow device` works only when the AS advertises RFC 8628; otherwise it exits with `Server does not advertise device authorization; use --flow browser`. Try it first (it is the only flow that needs no copy-paste), fall back without treating the failure as breakage.
- The browser flow prints the authorize URL **and** explicitly accepts a pasted redirect (`Or paste the redirect URL here`). The `redirect_uri` is loopback (`http://127.0.0.1:<port>/callback`), so the user opens the link on their own device, approves, the page fails to load — expected — and copies the address bar (`?code=…&state=…`) back to you. That handoff is the whole trick on a remote host.
- **Prefer `curl` over pasting into the waiting pty.** The CLI is already listening on that loopback port, so `curl "http://127.0.0.1:<port>/callback?code=…&state=…"` (quote it, the query has `&`) completes the exchange in one call and avoids the TUI swallowing or reflowing the long URL mid-paste. Confirm from the process log that it flipped to `Authenticated — N tool(s) available`.
- **Prove the server independently of the gateway.** Config changes only load on restart, so before promising anything: read `access_token` from `~/.hermes/mcp-tokens/<name>.json` and POST `initialize` then `tools/list` to the endpoint with `Accept: application/json, text/event-stream` and `MCP-Protocol-Version`. Then call one read-only tool — an empty list (`{"projects":[]}`) still proves auth and scope. Quote the runtime tool count and say the tools appear in chat only after `/restart`.
- **Cancelling is a clean op.** `hermes mcp remove <name>` drops the config entry *and* the stored OAuth tokens. Say that the vendor-side grant survives (account → connected apps) so the user can revoke it there too.
- Never log in for the user or type their password. You may load the consent URL read-only in the server browser to report what it will ask (Google vs email/password) and what scope it requests — loading it does not consume the code.
- State the vendor's price before they approve: a connector that needs a paid plan is a decision, not a step. Then verify with `hermes mcp test <name>` and narrow with `hermes mcp configure <name>`.

## 5. Run one real job end-to-end (smallest sensible target first)

The whole point is executed evidence. Order matters on a small host:

```bash
free -m                                     # headroom BEFORE anything heavy
TARGET=<smallest interesting target>         # 12 MB target worked; a 5 MB target OOM'd at a 1 GB heap
NODE_OPTIONS=--max-old-space-size=1400 <cmd> --json > /tmp/out.json 2>/tmp/out.err
jq -r 'keys_unsorted' /tmp/out.json; jq -r '.normalized_result.statistics' /tmp/out.json
```

Analysis tools emit enormous evidence payloads (67 MB JSON for a 12 MB target) — always to a file, always
summarise with `jq`, and prefer the tool's own `--filter-output key.path` / `--token-limit` when an agent
consumes the result. Never pipe a long analysis through `head`/`tail` (it masks the exit code) and don't rely
on piped output for progress — poll the process instead.

## 6. Ground-truth the accuracy before trusting it on an unknown target

Run it against something whose contents you already know (your own site, your own artifact) and compare its
findings with reality. "0 endpoints" on a page you know has none, reported alongside limitations instead of
guesses, is a *positive* accuracy signal — say so. If findings contradict known reality, that is the headline
finding of the whole evaluation.

## 7. Host safety (this box also serves live systems)

Heavy analyses must not run on the box that runs the production engine/gateway: a 5 MB target OOM-crashed at
the default 1 GB heap on a 1.9 GB host. Check `free -m` and swap first, start with the smallest target, raise
the heap only with real headroom, and prefer running the tool on the user's own machine with Hermes attached
over MCP if the workload is big. Clean up afterwards (kill the browser/server you spawned, delete the giant
evidence files, remove temp profiles) and **show** the box is clean (`ps -eo pcpu,rss`, `free -m`) — never
leave processes hanging on a production host.

## 8. Verdict shape (Indonesian, casual, decision-ready)

1. **Verdict first** — worth it / worth it only for one narrow job / skip.
2. What it IS (one line + license, stars, activity, who maintains it).
3. **What we proved by running it** — every claim with a real number.
4. What is **blocked or missing** (engines, runtimes, host limits) — as `capability_unavailable`-style facts
   plus the exact remediation, never as "the tool is broken".
5. Use cases **and explicit NOT-use-cases** for our lanes.
6. Supply-chain read: license, telemetry/analytics greps, install hooks, outbound URLs, optional downloads.
7. Cheapest reversible next step (register MCP with a subset / install the skill) with its cost stated
   (context per session) — then let the user decide. End with the decision, not with "mau gw buatkan?".

## Pitfalls

- Don't judge from the README, and don't let the README's tool count stand in for the runtime count.
- `capability_unavailable` + `remediation` is a *quality* signal: report it as the boundary plus what to
  install. Do not install JREs, engines, or system packages on the live box without asking.
- `pkill -f "chrome-headless"` also kills the shell running it (the pattern matches its own command line) —
  use `pkill -f "chrome[-]headless"`.
- Cloudflare-protected sites ("Just a moment…") cannot be captured by a plain headless browser; that is a
  target limitation, not tool breakage.
- If the user already owns a repo-vetting skill, put the *repo* learnings there and keep this skill focused on
  adoption mechanics (readiness, wiring, subset, cost).
- Support files: `references/rea-adoption-case.md` (worked case: readiness, MCP wiring, payload sizes) and `references/hermes-plugin-adoption.md` / `references/hermes-plugin-live-wiring.md` (plugin lane).
- Direct edits to `~/.hermes/config.yaml` are refused for the agent (security-sensitive); use `hermes config set <dotted.key> <value>` for scalar fields such as `mcp_servers.<name>.auth`.
- A GUI-first kit ships two binaries: launching the desktop one on a headless host fails with `neither WAYLAND_DISPLAY nor DISPLAY is set` — that is not a broken install. Test the CLI binary in `bin/` instead, and say which surface (GUI vs CLI) the user gets on his own machine.
