---
name: ctf-api-hunt
description: Deterministic API endpoint and parameter discovery for CTF web/API targets. Use when you know the host but not the routes — JS crawling with katana, live XHR capture, har_map.py scoring, hidden-parameter discovery with arjun, then method/path fuzzing with api_fuzz.sh. Run the ladder in order; every step has an explicit empty-result branch.
license: MIT
compatibility: Requires katana, arjun, and the existing scripts/har_map.py plus scripts/api_fuzz.sh. No MCP server needed.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "true"
  argument-hint: "[base URL | host]"
---

# CTF API Hunt — endpoint discovery ladder

Fuzzing a 404 catch-all is the most common way to waste an API challenge. This ladder finds the *real* routes first, then fuzzes. Run steps 1–4 in order; each step names where to go when it returns nothing.

Scope rule: authorized CTF target only. Bounded concurrency, no aggressive recursion (`-d 3` max), respect any rate hints in the challenge.

## Step 1 — crawl the JS (katana)

The HTML lies; the JavaScript tells the truth about endpoints.

```bash
katana -u https://TARGET/ -d 3 -jc -duc -kf all -jsonl -o crawl.jsonl
```

`-duc` disables the version/update check, which hangs in sandboxed or proxied networks (verified: without it katana stalls before the first request). Keep it in every invocation.

Flags: `-d 3` depth cap, `-jc` parse JavaScript, `-kf all` known-files (robots.txt, sitemap, .git, swagger). Then extract what matters:

```bash
# endpoints + JS files that reference /api
grep -oE '"/[a-zA-Z0-9/_\.\-]+\"' crawl.jsonl | sort -u | head -50
```

**If empty:** target may be a pure API with no site — skip to step 4 with the base path. Or the crawl was blocked (WAF/JS challenge) — fall back to `ctf-web-devtools` network capture of a real browser load.

## Step 2 — what the page really calls (live capture)

Static JS contains dead routes. The live page shows live ones. Either:

- `ctf-web-devtools` loop (`list_network_requests` → `get_network_request` on XHR/fetch), or
- `agent-browser` HAR capture → export.

Normalize both into one input for the scorer. katana JSONL and HAR are both accepted reasoning inputs; when in doubt, HAR wins (it is ground truth).

## Step 3 — score and rank (har_map.py)

```bash
python3 scripts/har_map.py capture.har        # or crawl.jsonl
```

Take the top 3 endpoints by score. For each, record: method, full URL, auth requirement (cookie/bearer/none), parameter names seen, error-verbosity (detailed 4xx JSON = high value).

**If the scorer returns only static assets:** your capture missed the API — the app may call the API only after login or after an in-page action. Drive the action in the browser (login, submit the form, click the feature) *then* re-capture. Do not proceed to fuzzing on static assets.

## Step 4 — hidden parameters (arjun)

Run on each top-3 endpoint, one at a time (arjun is slow and noisy — that is normal):

```bash
arjun -u 'https://TARGET/api/endpoint' -m GET,POST --stable -oT arjun-endpoint.txt
```

`--stable` reduces false positives on flaky challenge servers. Timing: arjun spends ~1–2 min on heuristic baseline *before* testing your wordlist, even for 5 words — always run it as a background job and poll the output file, never in a blocking call. Note the found URL ships with a random fuzz value (`?debug=6002`) — replace it with your own value when verifying. A parameter "found" only counts if adding it **changes response length or status** — verify each hit manually with curl before believing it:

```bash
curl -s -o /dev/null -w '%{http_code} %{size_download}\n' 'https://TARGET/api/endpoint'
curl -s -o /dev/null -w '%{http_code} %{size_download}\n' 'https://TARGET/api/endpoint?debug=1'
```

Classic CTF params to also try by hand if arjun is slow: `debug`, `admin`, `test`, `dev`, `show`, `all`, `raw`, `format`, `callback`, `id`, `role`, `preview`.

**If arjun finds nothing:** proceed to step 5 anyway — the route may take JSON-body or header params instead. Try `Content-Type: application/json` with `{}` vs `{"debug":true}`, and custom headers (`X-Debug`, `X-Original-URL`, `X-Forwarded-For: 127.0.0.1`).

## Step 5 — fuzz methods, paths, values (api_fuzz.sh)

Now, and only now, fuzz — with cloned auth state:

```bash
# 1. export cookies from the browser (agent-browser cookie JSON is authoritative)
# 2. baseline first: exact bytes of a known-good request
# 3. then:
bash scripts/api_fuzz.sh -u https://TARGET -c cookies.json --methods --params
```

See `scripts/api_fuzz.sh --help` and `ctf-web` §Fuzzing for wordlists (`scripts/wordlists/api-endpoints.txt`). Baseline → single mutation → diff. Never change two things at once; never trust a 200 without reading the body.

## Step 6 — route corpus (optional, kiterunner)

If steps 1–5 show an `/api/` surface but no flag path, and kiterunner is installed:

```bash
kiterunner scan https://TARGET -w routes.kite -A=apiroutes-210328:20000
```

API-aware corpus beats generic wordlists on `/api/v1/...` shapes. Skip this step if you already have a working primitive — more routes is not progress.

## Decision summary

```
crawl empty + no browser API   -> pure-API target: start at step 4/5 on /api/, /, /v1/, /graphql
scorer shows only static       -> drive the in-page action, re-capture (step 2)
arjun empty                    -> JSON-body params + X-Original-URL / X-Forwarded-* headers
fuzzing 404 on everything      -> wrong base path: check katana -kf hits (swagger, /.git, robots)
detailed 4xx JSON anywhere     -> STOP laddering; read the error, it names the expected shape
```

## Verify the stack

```bash
katana -version && arjun --help >/dev/null && echo ARJUN_OK
python3 scripts/api_fuzz.sh --help >/dev/null 2>&1 || bash scripts/api_fuzz.sh --help | head -5
```
