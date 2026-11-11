---
name: ctf-web-devtools
description: Browser-native reconnaissance with chrome-devtools-mcp for CTF web targets. Use when the challenge is a JS-heavy page or SPA and you need the exact API requests the page makes, POST bodies, console errors with stack traces, computed CSS, localStorage/secrets, or screenshots — before moving to wire replay with curl/ffuf. Pairs with ctf-web (ops loop) and feeds har_map.py.
license: MIT
compatibility: Requires the chrome-devtools MCP server (chrome-devtools-mcp 1.12.0, Node + Chrome) configured in .agents/mcp.json.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "true"
  argument-hint: "[challenge URL]"
---

# CTF Web DevTools — browser-native recon

Talk to the page with `chrome-devtools-mcp` first. The page *shows* you which API requests matter; `har_map.py` *ranks* them; the wire lane (curl/ffuf/`api_fuzz.sh` from `ctf-web`) *exploits* them. Never fuzz blind when the browser will tell you the endpoints.

## 0. Preconditions and cost control

- Server: `chrome-devtools` in `.agents/mcp.json` (`--headless --isolated`, workspace=scoped, memory/perf categories off by default).
- `--isolated` gives a throwaway profile: CTF cookies never touch your real browser.
- Tool-call budget: each `get_network_request` returns full bodies — call it only on write/interesting requests, not on every static asset.
- If the server fails to launch Chrome, check `Google Chrome.app` exists and retry with `--channel=stable` (default). Do NOT attach to your real profile (`--browser-url`) with non-CTF tabs open.

## 1. The loop (in order)

```
1. navigate_page <URL>                 # land on the challenge
2. take_snapshot                        # accessibility tree: forms, buttons, inputs
3. list_network_requests                # filter mentally: fetch/XHR first, ignore static
4. get_network_request <id>             # bodies of the 3-5 most interesting requests
5. list_console_messages                 # leaked secrets, paths, stack traces, TODOs
6. evaluate_script <read storage>       # localStorage / sessionStorage / window.__config
7. export HAR -> scripts/har_map.py     # rank endpoints, see ctf-web §HAR mapper
8. move to wire: curl/ffuf/api_fuzz.sh  # clone cookies, mutate, fuzz (ctf-web lane)
```

### Step 2 — snapshot, not screenshot

`take_snapshot` (accessibility tree) is cheaper and more actionable than `take_screenshot`. Use the screenshot only for canvas/CAPTCHA/visual-puzzle challenges, or to confirm a UI state after an action.

### Step 3 — which requests matter

Priority: `POST/PUT/PATCH/DELETE` > `GET` with query strings > `GET` JSON > static assets (ignore `.js/.css/.png/.woff2` unless you suspect a secret in JS — then fetch the JS body; source maps `*.js.map` are gold).

Write requests that return **4xx with a detailed JSON error** are the best leads: they prove the parser reads your input and tell you the expected shape.

### Step 4 — bodies, the thing Playwright does not give you

`get_network_request` returns request + response headers and bodies. Capture for each interesting request:

- exact URL, method, headers (`Content-Type`, `Authorization`, custom `X-*`)
- request body bytes (replay these exactly with curl before mutating)
- response body and status — a `200` with `{"ok": false}` is a rendered-page lead, not a wire lead

### Step 5 — console is a secret scanner

`list_console_messages` then `get_console_message` on errors. Look for: API keys, internal hostnames, stack traces with file paths, `TODO`/`FIXME` with endpoints, React/Vue dev-mode warnings that name components, failed `fetch()` URLs the UI never shows.

### Step 6 — client-side storage

```js
// evaluate_script payloads (read-only; never write during recon)
Object.entries(localStorage)
Object.entries(sessionStorage)
document.cookie
Object.keys(window).filter(k => /config|flag|api|token|secret/i.test(k))
```

SPAs park JWTs, feature flags, and admin booleans here. If you find a token, jump to the wire lane immediately — do not keep clicking.

## 2. Manipulation (only after recon)

Input tools in cheapest-first order: `fill` (single field) → `fill_form` (whole form) → `click` → `press_key` (Enter/Escape) → `handle_dialog` (alert/confirm/prompt block automation — handle them or the page stalls). `upload_file` for file-upload challenges; pair with the `ctf-web` upload notes. `drag` for slider/drag-drop CAPTCHAs.

## 3. Emulation for environment-gated challenges

`emulate` (UA, geolocation, timezone, locale) then `resize_page` (mobile viewport) when the challenge branches on device, locale, or "mobile-only" features. Re-run `list_network_requests` after emulation — mobile builds often call *different* endpoints.

## 4. When to leave this skill

| Signal | Go to |
|---|---|
| You have ranked endpoints + cloned cookies | `ctf-web` API lane (replay/mutate/fuzz) |
| Login wall you cannot pass in-browser | `ctf-web` auth notes (JWT/OAuth sections) |
| Need request interception/modification in flight | mitmproxy/Caido/Burp (see reports/skills-plugins-research-2026-11.md §4.2) |
| No network tools available (server down) | `agent-browser` HAR capture, then `har_map.py` manually |
| Page is a game/canvas with no API | `take_screenshot` + manual play; this skill is done |

## 5. Failure branches

- **Empty network list:** the page may use WebSockets (`list_network_requests` may not show frames — check console + snapshot for `ws://`), or requests fired before you attached. `navigate_page` again (fresh load) and re-list.
- **Auth-gated API returns 401 in replay:** your cloned cookie jar is stale — re-export from the browser, do not hand-edit tokens.
- **`evaluate_script` blocked by CSP:** read storage via `take_snapshot` exposed values, or move to the wire lane; do not fight CSP during recon.
- **Memory category needed** (prototype-pollution/closure hunt): restart the server with `--categoryMemory` (14 heap tools) — off by default for context cost.

## 6. Verify the stack

```
npx -y chrome-devtools-mcp@1.12.0 --help | head -3
# smoke: navigate to a harmless page, list_network_requests returns ≥1 entry
```
