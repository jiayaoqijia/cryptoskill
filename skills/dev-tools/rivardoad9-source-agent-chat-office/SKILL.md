---
name: agent-chat-office
description: Use when building a web office for agent personas.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-ui, multi-agent, profiles, telegram, tunnel, chat]
    related_skills: [localhost-dashboard-serving, hermes-agent, hermes-cron-automation]
---

# Web "office" for several agent personas

## When to Use

The user has 2+ persona bots (Hermes profiles) and wants one place to see them: "bikin kayak kantor", "satu
halaman buat semua agent", "ui web nya kayak gini" — usually with a reference screenshot.

Read the reference for WHAT it is, not just how it looks. A pixel-art isometric office, a building cutaway,
labelled rooms with tiny workers = the user wants a VISUAL office (who the agents are, what each one's job
is, who is working right now). A bare chat composer = a chat UI. Building the chat when they meant the
visualization misses the whole delivery, so when the reference is ambiguous build the visual map as the
landing page and keep chat as the second tab — that satisfies both readings.

Telegram itself cannot be re-skinned — say that plainly and deliver the web page; the Telegram half is a
GROUP with the bots in it (below).

## Architecture that works

One stdlib `ThreadingHTTPServer` on 127.0.0.1 (never 0.0.0.0) + cloudflared quick tunnel + the keeper cron
from `localhost-dashboard-serving`. Working example: `~/.hermes/office/` (server.py, office.html,
start.sh) on port 8795, watchdog `~/.hermes/scripts/kantor_up.sh` (cron `kantor_up`, `*/10 * * * *`,
`--no-agent --deliver origin`).

Routes: `/` + `/kantor` (page), `/manifest.json` + `/icon*.png` (PWA), `/healthz`, `/api/agents` (list +
status), `/api/thread/<id>` (history), `/api/send` (POST).

### Per-agent status, cheap

- online/offline: `gateway_state.json` → `platforms` map. Key is `telegram` for the DEFAULT profile and
  `<profile>:telegram` for the rest; test `["state"] == "connected"`. A naive substring search over the
  whole file reports every bot online.
- last activity: newest row of that profile's `state.db` `messages`.
- "job jalan 24 jam": `cron/executions.db` (default profile: `~/.hermes/cron/executions.db`, others
  `profiles/<p>/cron/executions.db`), column `status` is `completed`/`failed` (never `success`).
- Open every DB read-only: `sqlite3.connect("file:<path>?mode=ro", uri=True)`.

### Sending a message to a persona (the core)

```python
cmd = ["hermes"] + (["-p", profile] if profile else []) + [
    "chat", "-q", text, "--format", "stream-json", "--pass-session-id"]
if saved_sid: cmd += ["--resume", saved_sid]
```

- `--format stream-json` is the only parseable mode: the last line is
  `{"type":"result","session_id":...,"text":"...","duration_ms":...}`. Text mode wraps the answer in a
  `╭─ ☤ Hermes ─╮` box plus a "Resume this session with:" footer — do not regex that.
- Persist `session_id` per agent in `office/sessions.json` and `--resume` it next time, or every message
  spawns a brand-new session and the chat has no continuity. Write the file atomically (`os.replace`).
- Pass the text as an argv element (no shell) so quotes/backticks survive; `-q "$(cat file)"` in a shell
  is where the quoting bugs live.
- One `threading.Lock` per agent, `acquire(blocking=False)` → 429 "masih ngerjain pesan sebelumnya".
  A run takes 10-40 s, so the UI needs a typing indicator; also give the subprocess a hard timeout.

### The visual office (map view) — make it the landing page

One room per agent, drawn in code (inline SVG, no image assets), each labelled by the agent's JOB —
TRADING, ON AIR, BACK OFFICE, MAIL ROOM — and furnished with what that agent actually does (three monitors
and a safe for the trading desk, a mic and a lit red ON AIR sign for the news desk, a filing cabinet and a
wall calendar for the admin desk, sorting racks and parcels for the inbox desk). Each room carries a live
status chip, the room owner's job line, last activity and 24h job count, and clicking a room opens that
agent's desk. The room's figure animates while the agent is `busy` — that animation is what makes it a
dashboard instead of a picture. Geometry, props, painter order and the poster export:
`references/isometric-office-scene.md`. The same tab row carries a `⬇️ Pasang app` button: it fires
`beforeinstallprompt` on Chrome/Android and falls back to the iOS steps (Share → Add to Home Screen)
otherwise, and hides itself under `display-mode: standalone`.

Label consistency: the room chip and the roster/sidebar must use the SAME vocabulary (`siap` / `lagi
kerja` / `offline`). A room reading "standby" while the roster shows an online dot looks like a bug to the
user even when both are technically true.

### Key the page, always

The page can read the user's Gmail/calendar and write to their vault through the personas, so never hand
out a bare quick-tunnel URL. `OFFICE_TOKEN` env → require `?k=<token>` or a `k=<token>` cookie: set the
cookie on the first `?k=` hit (`Set-Cookie: k=…; Path=/; Max-Age=31536000; SameSite=Lax`; same-origin
`fetch` then carries it), 401 page/JSON otherwise. Keep `/healthz` UNauthenticated or the keeper
(pgrep/curl healthz) turns into a restart loop. Token file `office/token.txt`, mode 600, generated with
`head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n'`; the keeper prints the link as `$URL/?k=$TOKEN`. The install assets are the deliberate exception: the
browser fetches them itself, so `server.py` keeps a `PUBLIC` set (`/manifest.json`,
`/manifest.webmanifest`, `/sw.js`, `/icon*.png`) that bypasses the 401 while the page and `/api/*` stay
gated. `start_url: /?k=<token>` is injected into the manifest ONLY for an authed request, and the
page's `<head>` remembers the key in `localStorage.kk` + self-redirects when opened without it, so the
installed icon never lands on the 401 page. Recipe, SW rules and pitfalls: the `localhost-dashboard-serving` skill's PWA installability reference
(`references/pwa-installability.md` di skill itu, bukan di sini).

## The Telegram half

Telegram's look cannot be changed, but a **group containing all the persona bots** is the closest thing to
an office: bots keep privacy mode ON, so each one only sees messages that @mention it, and there is no
bot-to-bot loop. The user must create the group and add the bots (an agent cannot do it). The bots'
`TELEGRAM_ALLOWED_USERS` allowlist still matches the human sender, so no re-config is needed.

## Verify before reporting

1. API truth: `/api/agents` per-desk status, `/api/thread/<id>`.
2. One REAL send end-to-end (`POST /api/send`) and quote the reply + `ms` — that is the proof the office
   talks to the personas, not just that the page renders.
3. Browser pass at 390x844 and 1280x900 (`localhost-dashboard-serving` scripts) + `vision_analyze` on the
   screenshots; `scrollWidth == clientWidth` for no sideways scroll. Send the screenshots to the user.
4. Through the TUNNEL, not just localhost: `/` without key → 401, `/?k=` → 200, `/healthz` → 200.
5. Art QA for the visual office: render the 2x poster and `vision_analyze` THAT, not a phone screenshot —
   the inspector only sees room detail at 2x. Fix the mechanical findings (no contact shadow, sprite too
   small to read, a label contradicting the roster) and ignore the perspective impressions ("this panel
   feels tilted, not flush") — they are not actionable at pixel-art scale and chasing them burns rounds.
6. Installability (when the user asked for an app): load the KEYED url, then `cdp('Page.getAppManifest')`
   → `errors: []`, exactly one SW registration, `caches.keys()` non-empty, and
   `navigator.serviceWorker.controller` non-null after a reload. Then load the BARE url with no `?k=`:
   it must bounce to the keyed URL and render the rooms. Bare `/manifest.json` must not carry the token.

## Pitfalls

- The keeper's `pkill -f` pattern must not match its own command line (`[o]ffice/server.py`), and the
  restarted server must keep the SAME port or the tunnel points at nothing.
- `js()` in the browser harness runs in an ISOLATED world: page `var`s (`AGENTS`) read as 0 while the DOM
  reads fine. Assert on the DOM (`document.querySelectorAll('.desk').length`) and click elements with
  `document.querySelector('[data-id="x"]').click()` instead of calling page functions.
- Chips/desks render only after the first `/api/agents` fetch resolves; poll for `.desk`/`.chip` before
  asserting or screenshotting, or the shot shows "memuat…".
- Match the composer the user sent: blue pill on the left (agent switcher), emoji, `Message` field,
  paperclip, round blue send. Pure CSS, no CDN — the box has no internet-facing assets.
- Figures in an SVG diorama must be legible at card size: ~40px in a 176-unit-tall viewBox reads as a
  person, ~25px reads as a head peeking over a desk. Put the figure on clear floor at the FRONT of the
  room and give it `shade(agentAccent, 1.15)` as the shirt so it does not blend into props of a similar
  colour (a green worker among green parcels disappears).
- Exporting a clean poster: hide tabs/header/sidebar and capture with CDP `Page.captureScreenshot`
  (`clip` = the map element's bounding box, `scale: 2`). Hiding the sidebar is not enough in a CSS-grid
  layout — the empty track survives and the poster comes out a narrow vertical strip; set
  `gridTemplateColumns='1fr'` first.
