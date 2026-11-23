# A second agent with its own personality, on another chat bot

Use when the user asks for a "sub-agent" / separate personality they can CHAT with on their
second Telegram (or Discord/Slack) bot — e.g. "biar gw ga cuma chat sama lu doang di sini".

## Pick the right mechanism first

- `delegate_task` subagents are NOT this. They share the parent session, cannot talk to the user,
  and return one summary. Offering them here is answering the wrong question.
- A chat-able persona is a **profile** served by a gateway on that bot's OWN token. That is also
  what Bot Mode's roster is built on: the Bots tab (avatars, group chats, bot-to-bot DMs,
  `message_agent`) is a Desktop-app surface, so on a headless/Telegram-only install reach the same
  thing with profiles + per-profile bot tokens — do not send the user to install Desktop for it.

## Procedure

1. `hermes profile create <name> --clone`
   - `--clone` copies `config.yaml`, `.env` (provider API keys), `SOUL.md`, `skills/` and installed
     plugins — without it the profile has no credentials and cannot answer at all.
   - It deliberately does NOT copy messaging channels and strips `TELEGRAM_BOT_TOKEN` /
     `TELEGRAM_ALLOWED_USERS` from the cloned `.env`, because two gateways on one token fight over
     the same long-poll. Wiring the target bot is your job, not the clone's.
   - Any command can target the profile with `hermes -p <name> …`.
2. Wire the target bot into `~/.hermes/profiles/<name>/.env`: append `TELEGRAM_BOT_TOKEN=` and
   `TELEGRAM_ALLOWED_USERS=<user id>`, then `chmod 600`. Copy the token from its source `.env`
   inside a script so the value never lands on a command line or in the transcript, and assert the
   new token differs from the main profile's before restarting anything.
   When the user pastes a fresh BotFather token in chat instead, write it with a Python snippet that
   FIRST drops any existing `TELEGRAM_BOT_TOKEN=` / `TELEGRAM_ALLOWED_USERS=` lines, then appends the
   new pair — re-wiring a lane must be idempotent, and a duplicated token line makes the adapter read
   whichever one the loader hits first:
   ```python
   lines = [l for l in p.read_text().splitlines()
            if not l.startswith(("TELEGRAM_BOT_TOKEN=", "TELEGRAM_ALLOWED_USERS="))]
   lines += [f"TELEGRAM_BOT_TOKEN={tok}", f"TELEGRAM_ALLOWED_USERS={uid}"]
   ```
   `.env` is a protected store (`read_file` refuses it) — write through the script, chmod 600, and
   verify with a line count, never by printing the file. Then call `getMe` once and report the bot's
   `@username` + numeric id back to the user (that is how they know WHICH bot to open, and it proves
   the token is live before you claim anything); `getWebhookInfo` must show `url: ''` and
   `pending_update_count: 0`, otherwise a leftover webhook blocks long-polling and the bot looks dead.

   **When `getMe` answers 401, prove which side is broken before reporting.** Probe an ALREADY-WORKING
   bot token in the same snippet as a control: `401` on the new token plus `200` on the control means
   the request path and network are fine and Telegram itself rejects that token (revoked, regenerated
   in BotFather, bot deleted, or a copy that lost characters) — say that plainly instead of "gagal
   masang". A token pasted across two chat messages must be concatenated verbatim; never "repair" it.
   Pasting a token in chat does not invalidate it, so "he pasted it again" is not a fix — only a fresh
   BotFather value is.

   **Deactivating the bot again (user says "non aktif aja").** Strip every `TELEGRAM_*` line from
   `profiles/<name>/.env` (same filter-then-rewrite snippet, chmod 600) so the multiplexer cannot keep
   retrying a dead or unwanted token. Then prove it with
   `d['served_profiles']` / `d['platforms']` from `~/.hermes/gateway_state.json`: the profile may stay in
   `served_profiles` (dormant, no adapter) but `<name>:telegram` must be gone from `platforms`.
   Keep the profile itself — its `config.yaml`, `SOUL.md` and skills are the work that makes reviving it
   cheap once a valid token exists; deleting it buys nothing.
3. Personality lives in `profiles/<name>/SOUL.md` — a plain file, free to write. Read it with
   `read_file` first: a file you only printed with `cat` counts as unread and `write_file` refuses
   with `stale_write_blocked`. Write the persona as: who it is, who it is NOT (name the other bot
   and hand it the other bot's job), voice rules, how it works, hard lines (never invent a number or
   a source; never claim a trade happened).
4. **Memory needs a detour.** `--clone` copies your curated `memories/MEMORY.md` + `USER.md`, so the
   new agent starts as a copy of you. File/shell edits to those two files are BLOCKED by
   memory-shield ("changed only through the memory tool"), and the memory tool has no profile
   parameter, nor does `hermes memory` have an add subcommand. The working route is
   `hermes -p <name> memory reset --yes` (blanks the store; the profile then builds its own), and
   put the facts the persona must know from turn one — who the user is, how they want to be replied
   to — into `SOUL.md`.
5. Smoke-test before touching the gateway: `hermes -p <name> chat -q "kenalin diri lu singkat"`.
   It proves the cloned credentials work, `SOUL.md` loads, and the voice is right (~15s, and it
   sends a real intro the user can react to).
6. Confirm no routines came along: `profiles/<name>/cron/jobs.json` should not exist. A cloned
   profile carrying the source's jobs would double-post every lane into the new chat.
7. Serving it on its bot is a gateway step, not a profile step: see `hermes-gateway-ops` →
   "Serving a second profile on its own bot". A running standalone gateway never adopts a
   later-created profile — probe with the `rescan-profiles` control verb and hand the user the
   restart command instead of waiting for a rescan.

## Verify it is actually live

```bash
hermes gateway list                                   # "✓ <name> — served by the default multiplexer"
python3 -c "import json;d=json.load(open('/home/ubuntu/.hermes/gateway_state.json'));print(d['served_profiles'], d['platforms'])"
# platforms must contain a "<name>:telegram": {"state": "connected"} entry
```

The persona's own `state.db` (`profiles/<name>/state.db`, table `sessions`) also records what the
user typed and what it answered — reading the last row pair is the cleanest proof, and it shows
the cloned DB did NOT carry the main profile's history (`source` = `telegram`, `oneshot`, …).

## Google (Gmail / Calendar) for a profile bot

Profile sessions resolve `HERMES_HOME` to the profile dir, so the google-workspace scripts look for
`~/.hermes/profiles/<name>/google_token.json` — a fresh clone answers "Not authenticated" even though
`~/.hermes/google_token.json` exists. Fix: COPY both `google_token.json` and
`google_client_secret.json` into the profile dir and `chmod 600` them (the root token is often mode
644; tighten it too). Verify from inside the profile before promising it:

```bash
PY=/home/ubuntu/.hermes/hermes-agent/venv/bin/python
GAPI=/home/ubuntu/.hermes/skills/productivity/google-workspace/scripts/google_api.py
HERMES_HOME=~/.hermes/profiles/<name> $PY $GAPI calendar list        # expect real events, not "Not authenticated"
```

Write the exact `$PY $GAPI ...` incantation into the persona's SOUL.md — a persona told to "use Gmail"
without the working command guesses at it. Also copy the skill's hard rule (read freely, write only
after the user confirms in chat) into the SOUL.md, not just the skill.

## Seeding a persona's memory (the shield blocks direct writes)

`~/.hermes/profiles/<name>/memories/USER.md` cannot be written with file or shell tools — memory-shield
refuses every attempt ("Memory files are changed only through the memory tool"), even when the file is
empty. There is also no `hermes memory add`; that CLI only has setup/status/off/reset. The sanctioned
path is to RUN THE PROFILE'S OWN AGENT and have it call its own memory tool:

```bash
# write the ops to a prompt file first, then hand it to the profile's agent:
hermes -p <name> chat -q "$(cat ~/.hermes/cache/scratch/seed_<name>.txt)"
# prompt shape: "use the `memory` tool only; target=user add these 7 entries, target=memory add these 8;
#                write them VERBATIM, don't write files, don't merge entries"
```

Verify on disk, not from the agent's reply: `wc -c profiles/<name>/memories/*.md` and
`grep -c '§' profiles/<name>/memories/USER.md` (entries are separated by `§`; 7 adds → 6 separators).
Ceilings live in that profile's `config.yaml`: `memory.user_char_limit` (1375) and
`memory.memory_char_limit` (2200). A seeded USER.md right at the ceiling still loads but rejects later
adds, so leave slack. The SAME seven user entries work for every persona; the memory entries must
differ per lane — bot handle, its own scripts/paths, its hard limits.

## Give a persona skill AWARENESS, not more skills

A `--clone`d profile inherits the ENTIRE global skills tree (`find profiles/<n>/skills -name SKILL.md`
= the same count as `~/.hermes/skills`), so "this agent needs skills" is usually the wrong diagnosis —
it needs to know WHICH ones are its own. Write a numbered skill map into its SOUL.md (lane → skill
names, grouped), with the rule "never guess how a skill works, open it with skill_view first".

Only add a skill when a real gap is demonstrated. Hub search (`hermes skills search`) returns plenty of
overlapping candidates; installing a third URL-to-markdown tool next to a working fetch path is tool
hoarding, and a weekly evidence ledger will call it out later.

## Shared toolbox venv (tools several personas shell out to)

Keep such tools in ONE venv outside every profile so the path written into each SOUL.md is identical:
`~/.hermes/tools/toolbox/venv/bin/<tool>`. A verified pair for a capture/research desk:

- `markitdown` (MIT, 0.1.8) — PDF/DOCX/XLSX/PPTX/image → markdown. Caveat found while testing: PDF text
  often comes back with the spaces squeezed out (`Providedproperattribution…`), so tell the persona to
  fall back to the `pdf` skill and to mention the bad stretch in the note.
- `trafilatura` (Apache-2.0, 2.3.1) — `trafilatura -u "<url>" --no-comments` for clean article text when
  the built-in fetch returns nothing/paywalled. Local, no API key.

Test each on a REAL input before documenting it (an actual multi-page PDF, an actual article URL), and
report the caveat you hit instead of claiming it works for every format.

## Wiring a token does NOT need a restart (verified)

After appending `TELEGRAM_BOT_TOKEN` to `~/.hermes/profiles/<name>/.env`, the RUNNING multiplexed
gateway picked it up on its own — measured ~50 seconds from profile creation to connected, with no
restart and no manual rescan. The signature in `~/.hermes/logs/gateway.log`:
`[MULTIPLEX] Now serving profile '<name>' (0 adapter(s) connected)` → later
`✓ telegram connected (profile: <name>)` + `[MULTIPLEX] Re-scanned profile '<name>' after config/.env
change (1 adapter(s) connected)`. Poll `gateway_state.json` for `platforms["<name>:telegram"].state ==
"connected"` BEFORE asking the user to restart — a restart is usually unnecessary work.

`hermes gateway list` printing `✓ <name> — served by the default multiplexer` is NOT the same proof:
the profile can be served with zero adapters while the bot is still dead. Only the
`platforms["<name>:telegram"]` entry (or a real message from the user) settles it.

This auto-adopt only applies when the gateway booted in multiplex mode. If the boot-time probe
(`rescan_gateway_profiles`) returns `multiplex: False`, writing the `.env` changes nothing and the
restart is mandatory — see `hermes-gateway-ops`.

Verify the DELIVERY path, not just connectivity: create a one-shot job ~2 minutes out with the
persona's own deliver target, then read the result rather than trusting the chat window.

```bash
hermes -p <name> cron create "<MM> <HH> <DD> <MM> *" "Balas satu baris: jalur kirim jalan." \
  --name tes_delivery --repeat 1 --deliver telegram
# past the scheduled minute:
python3 -c "import sqlite3;print(sqlite3.connect('file:/home/ubuntu/.hermes/profiles/<name>/cron/executions.db?mode=ro',uri=True).execute('select job_id,status,delivery_outcome,error from executions order by started_at desc limit 3').fetchall())"
```

`delivery_outcome='delivered'` is the proof; `status='completed'` alone is not. Delete the test job after.

## Reminders (one-shot)

The schedule accepts a 5-field cron expression, so a one-shot reminder is
`sched="MM HH DD MM *"` plus `--repeat 1` — verify in `cron/jobs.json` that `repeat.times == 1` and
`next_run_at` is the intended minute. Profile cron scripts must be real files in the profile's own
`scripts/` dir (see below), but ordinary reminder jobs need no script at all.

## Profile-scoped cron (gotchas, verified)

- `hermes -p <name> cron create <schedule> "<prompt>"` — the prompt is a POSITIONAL argument;
  there is no `--prompt` flag (it errors `unrecognized arguments: --prompt`).
- A `--script` for a profile job must be a REAL FILE inside `~/.hermes/profiles/<name>/scripts/`.
  A symlink to the canonical script in `~/.hermes/scripts/` is refused with "Script path escapes the
  scripts directory via traversal", and a plain path under the shared scripts dir is refused with
  "Script file not found: ~/.hermes/profiles/<name>/scripts/<script>". Keep the logic canonical and
  drop a real shim in the profile:
  ```python
  import runpy
  runpy.run_path("/home/ubuntu/.hermes/scripts/<script>.py", run_name="__main__")
  ```
- `--deliver telegram` on a profile job delivers on THAT profile's own Telegram bot (deliver targets
  are profile-scoped), so no `lane_send.py` detour is needed once its token is wired.
  `--failure-deliver local` stops a not-yet-wired token from spamming failure notices.

## The evidence-collector pattern (a "what did I actually do" bot)

A weekly agent reading `~/.hermes/cron/executions.db` directly reports FALSE ZEROS: that DB keeps
only ~1000 rolling rows (~8 hours). Ingest incrementally into the profile's own DB instead — a
`--no-agent` script every few hours that `INSERT OR IGNORE`s on the source primary key — then let
the weekly agent read the accumulated tables and compare week over week. Things that bit:

- `executions.status` is `completed` | `failed`. Testing `status != 'success'` marks every healthy
  run as a failure (995 of 1000 reads as failures).
- `cron_incidents.id` is TEXT (e.g. `81878b_fd8f0decdd8e`); declaring it `INTEGER PRIMARY KEY`
  raises `sqlite3.IntegrityError: datatype mismatch`.
- Count new rows with `INSERT OR IGNORE` plus a separate `UPDATE` for the mutable fields; an upsert's
  rowcount is always 1, which makes "new rows" meaningless.
- Always run the collector twice in a row before trusting it: the second run must report zero new
  rows, otherwise the dedupe key is wrong.

## Feeding a capture persona links (economics)

A capture lane is the cheapest place to throw a URL, and that is a design property, not luck: its
reply is SHORT (title + 3-5 points + the note path), which measured ~330 output tokens per call
against ~1.270 on the main analysis lane, and the run happens in its own session so the main chat's
context never grows. Measured end to end: one X link = ~16 calls / 9,7k fresh input / 7,9k output /
100 s, one long article = ~10 calls / 9,5k fresh input / 3,9k output / 85 s.

- **One link per message.** A five-link dump makes the persona fetch, read and write everything in a
  single turn and answer long — that is where both the latency and the tokens are.
- **X/Twitter links are the expensive path** (~1,6x the calls and 2x the output of an article): the
  fetch fights a login wall — syndication CDN first, a safety filter blocks the shell attempt, then
  it writes a throwaway script to extract the text. If the lane will receive X links regularly, wire
  it to the authenticated X API path (`xurl`) instead of HTML scraping, and ask before using the
  user's token.
- **Verify the capture from the lane's OWN ledger**, `profiles/<n>/captures.jsonl`
  (`ts`, `src`, `title`, `path`, `status`), then stat the `path` it names. Do NOT infer success from
  a filename glob you built out of the URL — a guessed pattern reports "no note" for a link that was
  filed correctly, and that false negative then gets reported to the user.
- A persona told to "explain the article" graduates to main-lane cost. Keep the instruction as
  capture + note; the artefact lives in the vault on disk, so it never has to be re-read into
  anyone's context again.

## After it is live

- The bot becomes bidirectional: script pushes into that same bot do NOT enter the persona's
  session, so it cannot comment on an alert it never saw — the user must quote or paste it. Say
  that plainly instead of implying the persona has the alert in context.
- Report the residual limits (draft persona, no own memory yet, no routines) as things the user can
  change, and offer the cheap levers: edit `SOUL.md`, add routines later.
