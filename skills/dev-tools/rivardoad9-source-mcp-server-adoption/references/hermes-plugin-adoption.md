# Native Hermes plugin adoption — worked case: TinyFish (10 Oct 2026)

Class: the user drops `hermes-agent.nousresearch.com/docs/plugins/<name>` and asks *"cek ini, solid ga
buat lu instal?"*. That is a **native Hermes plugin** (declared tools + hooks + web/browser providers
in a `plugin.yaml`), not an MCP server and not a skill bundle — same verdict shape as SKILL.md §8.

## 1. The docs page gives you three things worth having

- the declared surface: tools, hooks (`pre_llm_call`, `pre_tool_call`, `on_session_finalize`, …),
  required env vars
- the **reviewed commit** of the author's repo — that SHA is your audit target
- per-plugin README (install paths, config keys, credit policy)

Catalog review does not mean audit the latest HEAD: pin the reviewed SHA, and diff later if HEAD
moved (TinyFish: docs pinned `e868225…`, repo HEAD was `df5734f8` — read HEAD, cite the pin).

## 2. Pull the module into /tmp and audit there

```bash
gh api repos/<owner>/<repo>/contents/<subdir> --jq '.[] | "\(.type) \(.path) \(.size)"'
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<subdir>/plugin.yaml"
# then curl each module file into /tmp/<name>/ and audit with search_files
```

Never audit or extract inside the Hermes tree; `/tmp` keeps the live install untouched.

## 3. Manifest first — the declared surface IS the risk surface

`plugin.yaml` fields that decide the verdict: `provides_tools`, `provides_hooks`,
`provides_web_providers`, `provides_browser_providers`, `requires_env` (+ `secret: true`),
`python_runtime`, `requires_hermes`, `version`, `kind: backend`.

Hooks are the part to read line by line — a `pre_llm_call` / `pre_tool_call` hook sees every turn of
every conversation. In the TinyFish case all three hooks were local and benign:

| hook | what the body actually does |
|---|---|
| `pre_llm_call` | returns one static guidance string, deduped by an in-context marker (`<tinyfish-routing-context version="1">`) |
| `pre_tool_call` | approve/block only its own credit-consuming calls, via Hermes' `tools.approval.request_tool_approval` |
| `on_session_finalize` | closes leftover vendor browser sessions |

## 4. Greps that answer "does it phone home or touch my box?"

```bash
search_files pattern "https?://"                 # expect only the vendor's own domains
search_files pattern "analytics|posthog|sentry|segment|amplitude|statsig|telemetry"
search_files pattern "os\.environ|getenv|\.env|write_text|chmod|open\("
search_files pattern "subprocess|os\.system|popen|eval\(|exec\("
```

TinyFish result: endpoints only `api.search.tinyfish.ai`, `api.fetch.tinyfish.ai`,
`api.browser.tinyfish.ai`, `agent.tinyfish.ai`; no analytics SDK; `subprocess` only inside the setup
CLI (it shells back into `hermes config set`); `httpx` is the sole dependency. Report that list as
evidence, not as "looks fine".

## 5. Does it fit this host (before promising anything)

- dependency already present in the Hermes venv:
  `hermes-agent/venv/bin/python -c "import httpx;print(httpx.__version__)"` → 0.28.1 ⇒ zero install
  step (matters because a non-TTY install would otherwise stall on a dep prompt).
- `requires_hermes` vs `hermes --version` (needs >=0.19, host had 0.20.4).
- **`hermes plugins search <name>` only searches the local seed index**: it answered
  `No plugins matched 'tinyfish' (index source: seed)` for a plugin that IS in the official catalog.
  Absence there proves nothing; install by `owner/repo/subdir` taken from the docs page.

## 6. Install inert, then verify — do not wire backends in the same step

```bash
hermes plugins install <owner>/<repo>/<subdir> --enable
hermes plugins list                       # status enabled, source user
hermes plugins capabilities <name>        # declared vs granted
hermes <name> status                      # api_key_configured, backends, ok
hermes <name> doctor                      # same report + "Recommended next step"
```

A backend plugin with **no API key** changes nothing: its tool is registered with a `check_fn` that
is false, and `web.search_backend` / `web.extract_backend` / `browser.cloud_provider` stay empty. So
install-then-verify is safe and reversible (`hermes plugins remove <name>`), and the honest line to
the user is "installed, currently inert, nothing routed".

The running gateway only loads a new plugin after `hermes gateway restart` — do NOT restart a live
gateway (alert lanes ride on it) without asking; say "restart needed to go live" and let the user
choose the moment.

## 7. Cost gate — put the number in the verdict

Read the vendor pricing page and separate free from metered before recommending any routing.
TinyFish (10 Oct 2026): Search free 30 req/min, Fetch free 150 urls/min; Agent $0.016/step and
Browser $0.002/min, both metered against a prepaid wallet. Check the plugin's own defaults too
(`tinyfish.credit_policy.browser` / `.agent` shipped as `request` = approval gate per feature).

Recommendation shape: use the free lane, leave metered lanes at `request`/`deny`, and never route the
credit-consuming cloud browser while local browser tooling already works.

## 8. What the user must supply, and the rollback

End with the one input that is theirs, not ours: their own vendor API key
(`agent.tinyfish.ai/api-keys` for TinyFish), then `hermes <name> setup`, one live query, and an A/B
against the current backend **before** switching daily work onto it. Rollback in one line:
`hermes plugins remove <name>` or reset `web.search_backend` / `web.extract_backend`.

Also state the trade-offs plainly, not just the features: routed queries and URLs leave through the
vendor (privacy), and any backend switch changes where our research traffic goes.
