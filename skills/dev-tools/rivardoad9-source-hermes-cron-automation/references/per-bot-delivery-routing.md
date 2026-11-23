# Routing a cron job's output to a SECOND Telegram bot (not the main one)

Verified 14 Oct 2026, moving risk-porto / rotasi-narasi / thesis-AI off the main DM onto @HermsNews_Bot.

## The constraint

`deliver` only routes through the platform connector, i.e. the MAIN bot (@your_gateway_bot here).
There is NO `deliver` value that posts via another bot. Splitting per bot therefore means the job
(or its script) pushes the text itself with the TARGET bot's token, and the job's `deliver` is set so
the engine does not ALSO post to the origin chat.

`deliver` DOES accept `bot-chat[:profile]` — do not reach for it here. That form injects the text into
the named profile's Bot Chat as a message the bot then answers: it burns a whole extra agent turn on
the target profile (cost it does not need) and the DM receives the bot's REWRITE of your text instead
of the artifact. Pushing with the target bot's token is what delivers the report verbatim.

## Known lanes in this stack

- `~/.hermes/scripts/news_send.py` → @HermsNews_Bot (token from `~/NewsAgent/.env`)
- `~/.hermes/scripts/perf_report_send.py` → @memescallsbot (token from `~/.hermes/data/perf_bot.json`)
- `~/.hermes/scripts/clip_send.py` → @clippersz_bot (CLIPPING lane; token from `~/.hermes/data/clip_bot.json`, mode 600)
- main bot → `TELEGRAM_BOT_TOKEN` in `~/.hermes/.env`

When the user pastes a NEW bot token in chat: write it straight into a fresh
`~/.hermes/data/<lane>_bot.json`, `chmod 600`, verify with `getMe` (confirms the real bot
username) and send one real test message — a bot can only DM a user who has started it, and
`getMe` alone does not prove the chat is reachable. `chat_id` is almost always the user's own
Telegram id.

**4096-char cap:** a feed dump (e.g. a campaign list) can exceed Telegram's limit and the send
fails silently with `ok:false` — chunk on line boundaries (~3900) and append `(i/n)`. Check the
real payload size (`--all` mode) before trusting one-shot sends.

DM chat_id is the user's own Telegram id (<telegram-user-id>) for ALL of these bots — the bot differs, not
the chat_id, so "different chat_id" is never the way to tell the lanes apart.

## Procedure

1. `news_send.py` takes `--file <path> [--kind news|card|report|alert|signal|info|warn]`.
   **Always pass `--kind card` or `--kind report` for data-dense text**: the default `news` kind
   truncates at `MAX_LINES=8` (msgstyle.py) whenever the text is ≤18 lines → a risk card loses half
   its rows silently. `card`/`signal`/`report` are exempt from the cap.
2. For a **no_agent script job**: replace the final `printf` with the push and keep stdout EMPTY so the
   engine has nothing to deliver. **Propagate the sender's exit code** — never `|| echo …; exit 0`:
   ```bash
   TMP="$(mktemp)"; printf '%s\n' "$OUT" > "$TMP"
   python3 "$HOME/.hermes/scripts/news_send.py" --file "$TMP" --kind card
   RC=$?; rm -f "$TMP"
   [ "$RC" -ne 0 ] && echo "<job>: gagal kirim ke <lane> (rc=$RC)" >&2
   exit "$RC"
   ```
   A wrapper that prints the error but still exits 0 is indistinguishable from a healthy run: `no_agent`
   delivers stdout only, so stderr is invisible to the user and a non-zero exit is the ONLY thing that fires
   `failure_deliver`. Left at `exit 0`, the lane can be dead for weeks while every run records success.
3. For an **LLM job**: append a final step to the job's own prompt, with `terminal` in
   `enabled_toolsets`. Replace a long prompt from a file — `hermes cron edit <job_id> --prompt
   "$(cat /tmp/prompt.txt)"` takes the whole multi-line text and avoids shell-quoting a 6k-char
   prompt by hand. Prompt shape that works:
   ```
   LANGKAH TERAKHIR: tulis laporan final persis format di atas ke /tmp/<lane>_out.txt,
   lalu jalankan: python3 ~/.hermes/scripts/news_send.py --file /tmp/<lane>_out.txt --kind report
   --kind wajib report: kind news memotong teks di 8 baris. Kalau exit-nya gagal, ulangi sekali;
   kalau masih gagal, tulis laporan penuh itu sebagai respons akhir lu dan sebut di baris pertama
   bahwa kirim gagal. Respons akhir lu sendiri cukup SATU BARIS status — jangan ulangi laporannya.
   ```
   `--kind report`, NEVER the default `news`: a daily report is 20-26 lines, and `news` hard-truncates
   anything under 18 lines to 8, silently dropping half the card (verified: 26 lines in → 28 lines out
   under `report`, which only adds the style header). The fallback-to-final-response matters because
   step 4's `failure_deliver` only fires on JOB failure — a failed send inside a successful run has no
   other way to surface, and the local cron output keeps the text.
4. `hermes cron edit <job_id> --deliver local --failure-deliver origin`
   `local` stops the origin post; `failure-deliver origin` keeps breakage visible in the DM (plain
   `local` would suppress failure notices entirely, which turns a broken job invisible).

## Half-done move: `deliver=local` with no route

Flipping `deliver` to `local` without wiring a sender is the most common way a lane move fails, and it
fails SILENTLY: the job keeps reporting success, the text lands in `~/.hermes/cron/output/<run_id>/`,
and the user never sees it — until he asks "bukannya ini udah gw suruh lempar ke bot lain?". A prompt
can even SAY the right thing ("Kirim via bot @HermsNews_Bot") while no mechanism exists, so grepping
the bot's name is not evidence; only a concrete send call is.

Audit rule: grep for the SENDER in the job's script or prompt, never trust the words.

```bash
grep -n "news_send\|lane_send\|perf_report_send\|clip_send" ~/.hermes/scripts/<script>.sh
```

`deliver=local` + no sender = broken by design → wire it or put it back to `origin`. `failure_deliver=origin`
masks this on the failure path only; successful runs stay invisible, which is exactly the state that looks fine.

Claim-checking the user's recollection: `session_search` the original request, then grep the current jobs,
before agreeing or denying. The honest answer is usually split ("2 dari 3 jalan") — name which ones are wired,
with file + line as evidence, and name plainly the one that is not.

**Sweep the whole batch, not just the job he named.** A lane move requested for several jobs at once is
usually half-wired in MORE than one place, and the second broken job is only found by looking: grep the sender
across every `jobs.json` (default profile plus each `profiles/*/cron/jobs.json`) and across the scripts of
every job that was aimed at that lane. Reporting the tally and fixing the unnamed ones in the same turn is
cheaper than being asked again later — he audits by asking, and "you told me about one of three" costs more
trust than the extra edit.

## Adding the route to an EXISTING LLM job's prompt

`hermes cron edit <job_id> --prompt "<text>"` REPLACES the whole prompt. Build the new text programmatically
instead of retyping 6k chars by hand: read `prompt` from `jobs.json`, append the route block, pass it as one
argv element (`subprocess.run(["hermes", "cron", "edit", jid, "--prompt", new])` — no shell quoting), then
read `jobs.json` back and assert both the new length and a marker (`'RUTE BALASAN' in prompt`).

Route block to append (needs `terminal` in `enabled_toolsets`):

```
RUTE BALASAN (WAJIB, jangan dilewat): job ini deliver=local, jadi balasanmu TIDAK masuk ke chat
mana pun kalau nggak lu kirim sendiri.
1. tulis hasilnya ke /tmp/<job>_out.txt lewat terminal (printf atau python3 -c, JANGAN echo -e).
2. jalankan: python3 /home/ubuntu/.hermes/scripts/news_send.py --file /tmp/<job>_out.txt --kind card
Kalau exit-nya bukan 0, tulis baris terakhir balasanmu: "<job>: gagal kirim ke <lane>".
Kalau sukses, diam (jangan kirim dobel ke chat utama).
```

A run already in flight keeps the OLD prompt (loaded at start), so the correct wording is "rute barunya
kepakai di run berikutnya", never "udah live".

## Verification

- **Verify a wired route from the job's own run artifact, not from the absence of complaints.** After the
  next real fire, read `~/.hermes/cron/output/<job_id>/<timestamp>.md`. A job that used to emit a warning
  line and now reads `Status: silent (empty output)` is evidence the defect is gone: a warning makes the run
  non-silent (it gets delivered), so silence after the fix is meaningful, not just "nothing happened".
  Pair it with the deterministic side effect the job advances (its state file's block/marker moving forward).
- `bash -n <script>` after editing.
- Test the send block by hand with a synthetic temp file BEFORE waiting for a real trigger; a
  delta-gated script prints nothing on a no-change run, so "ran with no output" does NOT prove the
  new send path works.
- Read `jobs.json` back and confirm `deliver` / `failure_deliver` / prompt survived (the ticker
  rewrites jobs.json every minute).
