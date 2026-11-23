# Evaluating Hermes plugin-catalog entries (verifying the hype, ranking power)

Trigger: "Hermes added 20+ new plugins in a single day / 88 PRs merged on <date> / 5 additions worth
knowing about — mana yang powerful?" (or a single name: "govee bagus nggak?"). Also fires when the user
pastes a tweet/thread listing agent frameworks or tool repos and asks whether it would make the agent
stronger (§2b). Same class as judging an MCP server: verdict first, evidence measured, then the cheapest
reversible step.

## 1. Verify the viral claim before repeating it

```bash
# merged PRs on a date
gh api "search/issues?q=repo:NousResearch/hermes-agent+is:pr+is:merged+merged:2026-10-08&per_page=1" --jq '.total_count'
# how many of them are catalog work
gh api "search/issues?q=repo:NousResearch/hermes-agent+is:pr+is:merged+merged:2026-10-08&per_page=100" \
  --jq '[.items[] | select(.title | test("catalog";"i"))] | length'
gh api "search/issues?q=repo:NousResearch/hermes-agent+is:pr+is:merged+merged:<date>&per_page=100" \
  --jq '.items[] | select(.title | test("catalog";"i")) | "\(.number) \(.title)"'
```

10 Oct 2026 result: claim TRUE — 88 PRs merged 2026-10-08, 55 plugin-related, 19 of them new catalog
entries. (`gh api repos/.../pulls` misses these: the newest 100 closed PRs don't reach back a day. Use
`search/issues`.)

## 2. Read the catalog as data, not as a page

```bash
curl -sL --compressed https://hermes-agent.nousresearch.com/docs/api/plugin-catalog.json -o /tmp/cat.json
```

**`-L` is mandatory**: without it you get `{"redirect": "...nousresearch.github.io/..."}` and zero entries.
540 entries at the time of writing. Fields that decide the verdict, per entry:

| field | why it matters |
| --- | --- |
| `requires_hermes` | GATING. Compare against `hermes --version` FIRST — an entry needing `>=0.21.5` cannot be installed on 0.20.4, so 4 of 5 candidates were blocked before any evaluation |
| `tier` | `official` (NousResearch) vs `community` — all five candidates were community |
| `category` | shelf: memory / desktop / tools / web / platform / voice / models |
| `capabilities` | `provides_tools`, `provides_hooks`, `provides_middleware`, `requires_env` → the blast radius and whether a key/Desktop/appliance is needed |
| `repo` + `sha` | catalog installs pin the reviewed commit; a bare-name install is refused if absent from the catalog |

Per-plugin detail page: `https://hermes-agent.nousresearch.com/docs/plugins/<name>` (the README, the
capability chips, the exact install + enable commands). `llms.txt` only indexes the catalog page itself,
so go straight to `/docs/plugins/<name>`.

### CLI route (no network, and the only parseable one)

```bash
hermes plugins search --json > /tmp/cat.json      # OMIT the term → the WHOLE curated catalog
hermes plugins list --json                        # installed plugins incl. bundled, names only
```

`search --json` returns `{query, results: [...]}` with `name, repo, sha, description, maintainer, tier,
category` per entry — the same decision fields as the HTTP JSON, in one call, with no redirect trap.
Counts drift between routes (550 via CLI vs 540 via HTTP on the same day) — normal; the fields that gate
a verdict agree.

**Never parse `hermes plugins browse`.** It is a rich table that wraps and truncates every cell (names
come back as `agent-bat…`, descriptions end in `…`), and it takes no `--json` flag — `COLUMNS=400` only
widens it. Also, `hermes plugin list` is not a command; the subcommand is `plugins` (`list`/`ls`).

Discard whole shelves by the surface the user actually talks over, before ranking anything:

| shelf | drop when |
| --- | --- |
| `desktop` (133 of 550) | the user is on a gateway/Telegram/CLI install — they never see the pane |
| `memory` (63) | any memory provider is already installed |
| `models` (46) | the provider/model is already chosen |
| `voice` (16), `platform` (31) | the user does not use that surface |

The surviving `tools` / `automation` / `general` / `web` entries are the only candidates. Rank those with §3.

## 2b. A framework list is not an upgrade path

When the input is a list of agent frameworks/repos (OpenHands, Browser Use, LangGraph, CrewAI, PydanticAI,
Agno, AutoGen, Semantic Kernel, Mastra, Dify …) and the question is "would installing this make you
stronger?" — that is not an install question. Frameworks build a NEW agent; they add nothing to a running
one. Answer as a mapping, one line each: the capability it covers and where the running install already
has it. Checks that settle it: `hermes plugins list --json` for the bundled `browser-browser-use` plugin
behind the `browser_exec` helpers, the coding-delegation skills (claude-code / codex / opencode), and
`delegate_task` for multi-agent fan-out.

State plainly that installing them changes nothing, then pivot to the levers that do — plugins/MCP, skills,
memory — and use §3 for what is actually on offer.

## 3. Rank by what changes, not by novelty

Order the candidates with these four questions (this is what "powerful" means for this user):

1. **Does it change how the agent works, or add a peripheral tool?** Memory/context providers change
   everything; a lamp switch changes nothing.
2. **Does it hit a live pain point right now?** Check the real bottlenecks: flat memory at 99 % capacity
   (a retrieval-based memory provider removes the char ceiling), pages that block the keyless scraper,
   API spend the user is actually paying for.
3. **Install cost** — a separate server binary (~160 MB Go binary + embedding model + LLM endpoint),
   Desktop-app-only UI, a hardware appliance, an extra API key, or "stdlib only, no key, no network".
4. **Version gate** from step 2.

Report shape: rank them, name the #1 and say WHY in one line, then per candidate: what it does, what it
needs, and for whom it is worthless. Close with the honest note when none of them earn money or change
the user's outcomes — this user's agent must not oversell a plugin as leverage.

Worked 10 Oct 2026 verdict: **1)** HyAtlas memory (only one that changes the agent: 7-layer local memory,
vector store, cited graph; cost = separate Go server + LLM endpoint + `>=0.21.4`) **2)** TinyFish (already
installed, free search 30/min + fetch 150/min, cloud browser for blocked pages) **3)** Approval Ledger
(observer-only audit of approval prompts; stdlib, no key, no network; `>=0.21.5`) **4)** OpenRouter Spend
(good only if OpenRouter is the provider — this user runs DeepSeek, so near-zero value; also Desktop-only)
**5)** Govee (lights only, no plugs/heaters → zero unless the user owns the hardware).
