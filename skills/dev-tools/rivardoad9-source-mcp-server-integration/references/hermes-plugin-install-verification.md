# Installing + verifying a batch of Hermes plugins (and the traps each one sets)

Follows `references/hermes-plugin-catalog-evaluation.md` (§3 ranks the candidates). This file is the
install-and-prove half: what to pass, how to tell "loaded" from "actually working", and the verified
traps of the four plugins that came out of the 11 Oct 2026 batch (skill-retrieval, toolaria,
memory-shield, memory-rewind).

## Install non-interactively

```bash
hermes plugins install <name> --enable --yes-deps    # --yes-deps answers the Python-dep consent prompt
```

One per plugin, echo a marker per loop so a failure names itself. `--enable` alone leaves the dep consent
question open and the install is refused on a non-interactive run. `hermes plugins show <name>` only works
for INSTALLED plugins (an uninstalled name returns "Plugin 'x' not found") — read `search --json` instead.

## "Enabled" is not "live" — check the three surfaces separately

The install banner lists what got wired: `hooks`, `gateway_commands`, `gateway_transforms`, `middleware`,
`tools: deferred (next session)`. A plugin can be enabled and still not be doing its job.

- **Enabled**: `hermes config get plugins.enabled` (or `hermes plugins list --json`).
- **Registered in the running process**: grep `~/.hermes/logs/agent.log` and `gateway.log` for
  `hermes_plugins.<name>` — e.g. `Skill retrieval plugin registered (top_k=6, compact=true)`. These logs
  are gitignored, so `search_files` skips them and reports 0 matches; use `rg` in `terminal`.
- **Producing its effect**: force the path and look at the artifact (§ below). Registration lines alone
  prove nothing about behaviour.

`hermes gateway status` prints the whole systemctl unit tree (hundreds of lines, kills your context) —
avoid it; the log lines above answer the same question.

## Per-plugin proof, cheapest first

**memory-rewind** — has a CLI, so it is the easiest to prove and it doubles as free undo:
`hermes memory-rewind snapshot` then `hermes memory-rewind log` → version list with file counts (1161
files on first snapshot). It hooks `on_session_start`/`post_tool_call`, so every `skill_manage` edit
automatically lands as its own version (`after skill_manage (4 files)` + the exact patches) — the cheapest
way to make a skill edit reversible. `restore` is user-run only.

**memory-shield** — the default policy is already safe, but set `trusted_users` or every direct chat is
treated as the owner:

```bash
hermes config set plugins.entries.memory-shield.settings.trusted_users '["telegram:<user_id>"]'
```

Settings are read through a `get_config` callable per evaluation, so no gateway restart is needed (the
install-time reload covers the hook). Prove it live with a deliberately refused write: a `memory`
`remove` on a nonexistent `old_text` returns the shield's refusal when it works and is harmless either
way. It also appends `plugin-data/memory-shield/audit.jsonl` with outcome/target/denied/chat_type/user_id.

**skill-retrieval** — verify the corpus is not empty and that ranking is sane, by driving its own module
(never by trusting the log line):

```python
# ~/.hermes/hermes-agent/venv/bin/python
spec = importlib.util.spec_from_file_location("m", "<plugins>/skill-retrieval/scripts/bm25_retriever.py")
# load_active_skills() → list of dicts; BM25Index().build([s['skill_id']], [s['text']]); .retrieve(q, 6)
```

Needs `pyyaml` **in the Hermes venv** (`~/.hermes/hermes-agent/venv/bin/python -c "import yaml"`) — the
system `python3` NOT having it is normal and not a failure.

**The trap that matters**: Phase 1 strips skill descriptions from the system prompt, so a BM25 miss means
the agent never sees that the skill exists. Lexical BM25 over English descriptions misses Indonesian
queries — measured 3 of 8 (`laporan mingguan kerja magang`, `pantau harga koin di portofolio`, `cari
lowongan magang akuntansi` all returned NO HIT while the matching skills existed).

Fix, and it lives in YOUR skills, not the plugin: add a `triggers:` list of natural user phrasings to the
frontmatter of the affected SKILL.md files (top-level key, str-list; `_frontmatter_keywords` accepts only
str lists, and the index text is `name: desc + triggers + tags`). The index rebuilds when Hermes clears
its skills prompt cache (`skill_manage` create/patch/delete). Re-run the probe and require the miss to be
gone — after adding Indonesian triggers, all 8 hit with the right skill on top.

**toolaria** — rescues only a fixed tool set: `web_extract`, `web_search`, `browser_*`, mail/social/webhook
senders, and any tool whose registry toolset starts with `mcp-`. `terminal`, `write_file`, `patch`,
`execute_code` are in `_UNCONDITIONAL_EXCLUDES` and are NEVER rescued.

So a 36 KB `terminal` output passing through untouched is EXPECTED, not a broken install. Prove it on the
right path: one `web_extract(urls=[...], char_limit=40000)` → the result comes back as a preview + handle
(`[Toolaria: tool result rescued. ... blob=<id>]`), and `~/.hermes/toolaria/blobs/<id>`, `sessions/`,
`sidecars/` appear on disk (blob bytes ≈ the reported size).

Two limits to report, not hide: `rescuer_fetch` is a deferred tool, so the handle is only fetchable next
session; and on a host without ambient-toolset support the plugin warns that in toolset-restricted
sessions (cron/profile) the handle cannot be redeemed — add `rescuer` to those sessions' enabled_toolsets
or accept the loss there.

## Report shape

Per plugin: enabled ✓ / registered ✓ / effect proven ✓ with the artifact (version hash, audit line, blob
id + bytes, probe output). Then the traps that survive, each with its concrete mitigation — a batch is not
"done" when the installs return 0.
