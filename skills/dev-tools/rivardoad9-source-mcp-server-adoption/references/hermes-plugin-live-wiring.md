# Wiring a plugin/provider LIVE — the half after the verdict

Companion to `references/hermes-plugin-adoption.md` (which covers the verdict: docs page → source audit →
inert install → cost gate). This file covers what happens **after** the user says *"set it up for yourself"*
and hands over their own key. Worked case: TinyFish, 10 Oct 2026.

## 1. Let the vendor CLI do the multi-harness work

```bash
npx -y @<vendor>/cli@latest connect --all --api-key <KEY> --skip-launch --url "<mcp url>"
npx -y @<vendor>/cli@latest doctor --pretty      # human summary, ✓ / ⚠ per harness
npx -y @<vendor>/cli@latest doctor               # JSON: checks[] + repairs[]
```

- `connect --all` detects every coding agent on the box, registers the MCP server for each, installs the
  vendor skill, and **writes the key into `~/.hermes/.env` itself** (vendor-prefixed name,
  e.g. `MCP_TINYFISH_API_KEY`; the plugin resolves `TINYFISH_API_KEY` first, then that one). No need to
  re-paste the key anywhere, and never echo it back to the user or into a file we author.
- **With `--api-key` supplied there is no browser sign-in** — the CLI printed "Using your stored … API key,
  no browser sign-in needed". Warn about the sign-in pause only when no key is given.
- Its summary marks each harness ✓ or ⚠; report those literally, plus which harnesses were `skip` because
  they are not installed (that list is long and uninteresting — one line).

## 2. Two failure modes that look like failures and are not

- **`plugin_install` finishing step fails on a seed-only index:**
  `Plugin '<name>' was not found in the community index (seed)`. The CLI installs by *index name*, so this
  fires even when the plugin is already installed by `owner/repo/subdir`. Ignore its suggested
  `hermes plugins install <name> --enable`.
- **`doctor` JSON says `"repairs": []` while a `checks[]` entry is still `warn`** ("plugin installed but the
  web backends do not point at tinyfish"). An empty repairs list is **not** "all clear" — the fix is the
  plugin's own `hermes <name> setup --yes`, then re-run doctor until every line is ✓. Repairs that DO come
  with `unattended_safe: false` are the user's to run: show the command, don't run it.

## 3. The ordering trap: routing a backend the running process cannot serve

`hermes <name> setup --yes` writes `web.search_backend` / `web.extract_backend` = `<name>`. The live gateway
loaded its plugin set at **startup**, so the agent's very next tool call dies:

```
web is configured to use 'tinyfish' (set via hermes tools), but no registered web search provider has that name
```

That is the agent cutting off its own web access mid-conversation. Either wire the backends **last**, or route
and restart immediately. Never leave config pointing at a provider the running gateway has not loaded.

## 4. Prove it before the restart lands

`hermes <name> doctor --live` runs the plugin's own provider code with the stored key and answers
`live_search_ok: yes` / `live_fetch_ok: yes`. The vendor CLI proves the same from outside
(`search query "…" --pretty`, `fetch content get <url>`). The MCP tools only appear in a session started
after the install — say that plainly instead of reinstalling.

Pitfall: `fetch content get <url> --pretty` prints only the summary (`Results: 1 / Errors: 0 / Title: …`),
never the body. Fetch **without** `--pretty` into a file and read `results[0].text`.

Worked proof of the whole chain (top HN story, 10 Oct 2026): `fetch content get https://news.ycombinator.com`
→ TinyFish Fetch, 367 ms, markdown body; top item parsed as rank 1 and corroborated with a TinyFish Search
query on the same headline. Two independent vendor paths = good evidence; a single "it works" is not.

## 5. Restart on this host: timed, detached, self-verifying

`hermes-gateway-ops` has the base recipe (the inline restart command is blocked; system scope here, so
`systemctl --user` fails with "Failed to connect to bus: No medium found"). Two refinements that paid off:

- **Check `hermes cron list` first** and set `--on-active` so the bounce lands *after* the next scheduled
  tick. A 5-minute no-agent job would otherwise be clipped mid-run.
- **Make the detached script write its own verification file.** The agent has no turn while the gateway is
  down, so that file is the only way the next session can confirm the restart landed.

```bash
# /tmp/restart_gw.sh
systemctl restart hermes-gateway
sleep 14
{ date; systemctl is-active hermes-gateway
  systemctl show -p MainPID --value hermes-gateway
  journalctl -u hermes-gateway --since "-2 min" --no-pager | tail -25; } > /tmp/<name>_restart_check.txt 2>&1
```

```bash
chmod +x /tmp/restart_gw.sh && sudo systemd-run --on-active=150 /bin/bash /tmp/restart_gw.sh
```

Tell the user the exact minute of the bounce and that a message sent during it may be dropped — then read
`/tmp/<name>_restart_check.txt` on their next message instead of assuming.

## 6. Reporting shape when the user is watching a checklist

When the request arrives as numbered steps ("1. run this, 2. check it, 3. prove it, 4. report"), answer in
that same numbering and put the unfinished items in the open: which harnesses connected, which need the user
to sign in (often: none), what is deliberately still off (metered lanes left at `request`/`deny`, nothing
funded), and anything that must happen after the restart. State the confirmation the user must supply next
(a single message after the bounce), so no one is left wondering whether it worked.
