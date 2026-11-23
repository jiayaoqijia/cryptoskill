# Worked example — muting @memescallsbot (30 Sep 2026)

Directive, in full: **"non aktif memebot"** — four words, no bot ID, no scope, no deadline.
This is what the procedure looked like end to end.

## 1. Alias → real channel

"memebot" was not a filename anywhere. It resolved through the credentials file:

```bash
python3 -c "import json;c=json.load(open('$HOME/.hermes/data/perf_bot.json'));print(c.get('bot'))"
# -> @memescallsbot   (token never printed)
```

## 2. Sender audit (which files actually push to it)

```bash
grep -rln "deliver(\|tg_push(" ~/.hermes/scripts/*.py
```

Result: **one shared helper plus five producers** — `lowcap_common.py` (the choke point),
`lowcap_collect.py` (P1), `lowcap_alert.py` (P2/P3), `early_watch.py`, `early_watch_track.py`,
`sm_lane.py`, plus `perf_report_send.py` (manual, on demand).

That is why the switch went into `lowcap_common.deliver()` and nowhere else: one edit covers
every lane, and an audit grep can prove coverage afterwards.

Deliberately **not** touched: the news bot (`@HermsNews_Bot`, different creds) and the engine
bot. The report said so explicitly — the user named one bot, not all of them.

## 3. Implementation shape

```python
# lowcap_common.py
MEMEBOT_FLAG = os.path.join(DATA, "memebot_off")      # flag file (survives restarts)

def meme_bot_off():
    """env MEMEBOT_PUSH=off  OR  file ~/.hermes/data/memebot_off"""
    if os.environ.get("MEMEBOT_PUSH", "").lower() in ("off", "0", "no"):
        return True
    return os.path.exists(MEMEBOT_FLAG)

def deliver(text, lane=""):
    if meme_bot_off():
        log_push(lane, False, len(text), "dimatikan (MEMEBOT_PUSH off)", status="MATI")
        return False, "dimatikan"        # <- payload DROPPED, stdout untouched
    ...                                   # unchanged: send, empty stdout on success
```

Two switches on purpose: the **file flag** works for crons that invoke the script directly
(no env plumbing through 7 jobs), the **env var** is for one-off runs.

## 4. The part that made it safe

The lane contract here is *silence-on-success*: a failed send **prints** the payload so cron
`deliver: origin` can deliver it as a safety net. So the mute could not be "skip the send" —
that would have printed every card into the main DM. The mute returns early **without
printing**, and records `MATI` in `~/.hermes/data/alert_push.log` so the suppression is
auditable rather than invisible.

Manual path kept working: `perf_report_send.py` (user explicitly asks for a performance
report) prints locally instead of sending. Muted = no unattended push, not "the user lost the
ability to ask".

Producers all kept running — scan, `call_ledger.jsonl`, `ew_features.jsonl`, +15m/30m/1j/4j/24j
checkpoints, heartbeats — so the measured record keeps accruing while the bot is quiet. That
tradeoff was stated in the report (GMGN quota and CPU still spent).

## 5. Proof (not "the code looks right")

```
$ ./lowcap_p3.sh
exit=0  stdout_bytes=0          <- cron stays silent, no flood
$ tail -4 ~/.hermes/data/alert_push.log
P3 | MATI | 8339 char | dimatikan (MEMEBOT_PUSH off)
P3 | KIRIM | 419 | 4321          <- pre-mute, message_id = Telegram receipt
P3 | KIRIM | 419 | 4319
P3 | KIRIM | 419 | 4317
```

`stdout = 0 bytes` + the `MATI` line + the contrast with the last real `KIRIM … <message_id>`
lines is the whole proof. One more lane (`early_watch_track.py`) was run too and stayed silent.

## 6. Test fix (the pitfall, in code)

Three pre-existing tests failed the moment the flag file existed in production, because they
read the module-level path:

```python
# selftest, delivery block
global BOT_CRED, PUSH_LOG, MEMEBOT_FLAG        # <- global belongs in the FUNCTION HEAD
oc, op, of2 = BOT_CRED, PUSH_LOG, MEMEBOT_FLAG
try:
    with tempfile.TemporaryDirectory() as td:
        MEMEBOT_FLAG = os.path.join(td, "memebot_off")   # non-existent path = bot ON
        ...                                               # existing send-path tests
        # kill-switch cases (7 new):
        open(MEMEBOT_FLAG, "w").close()                   # flag present
        assert deliver("teks")[0] is False
        assert captured_stdout == ""                      # NOT printed
        assert "MATI" in open(PUSH_LOG).read()
finally:
    MEMEBOT_FLAG = of2
```

A `global` inside the nested block raises
`SyntaxError: name assigned before global declaration` — hoist it to the function head.

Verification ritual: the suite must pass **39/39 with the flag present AND absent**:

```bash
mv ~/.hermes/data/memebot_off /tmp/mb.kill
python3 lowcap_common.py --selftest | tail -1
mv /tmp/mb.kill ~/.hermes/data/memebot_off      # always restore in the same command
```

## 7. Reversal

```bash
rm ~/.hermes/data/memebot_off      # normal sending resumes; flag file is the only switch
```

Left in place: the code, the log status, and the 7 tests — so re-muting later is one `touch`.
