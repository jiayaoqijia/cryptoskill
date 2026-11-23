# False-alarm triage — before you mute anything (04 Okt 2026)

Directive, in full: **"ini offin dong alertnya"** (replying to a cron alert "⚠️ WEBHOOK LYNK.ID
BERMASALAH: URL tunnel tidak ditemukan di log"). It reads like a mute request. It was not: the daily
check had been firing that same line every morning for weeks while the receiver and the tunnel were both
healthy. **The alert was the bug.** Muting it would have deleted the coverage *and* left the real defect
(a monitor reading a rotated log) in place.

## Step 0 — is the alert WRONG, or is the channel merely noisy?

Four commands settle it, and they are cheaper than a mute:

```bash
pgrep -af "receiver.py|cloudflared"                                     # are both processes actually alive?
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8645/health   # 200 = the service is serving
curl -s -o /dev/null -w '%{http_code}\n' "$URL/health"                  # 200 = the public chain works
```

If the underlying thing is healthy while the alert keeps firing, the alert is the defect. Say that
plainly in the report — *"itu false alarm, webhook-nya sehat"* plus the evidence — then fix the source of
truth instead of silencing it. Muting is the right answer only when the user does not want the coverage at
all; offer that as a one-word follow-up, do not assume it.

## Step 0b — a fixed monitor must be proven on BOTH paths

- Healthy run: stdout **0 bytes** (with `no_agent`, empty stdout = no message).
- Forced failure: poke the state file (write a stale URL/flag), run again, confirm the alert text names the
  correct new value, then **restore the state file from a backup copy in the same command**.

Never report a monitor as fixed off code reading alone. If only the quiet path was exercised, say
"implemented, belum gw tes picu" — not "done".

## Reporting shape when this happens

State up front that it was a false alarm and why (rotating log as the source of truth), what was changed,
both test results, and then explicitly which alarms **remain** and what each one now means. The user's real
question was "stop waking me for nothing", not "remove my safety net" — and they will ask again if the
remaining alerts are not distinguishable from the noise.

Concrete instance: `webhook-receivers/references/cloudflared-tunnel-health.md` (cloudflared metrics
`/quicktunnel` as the live URL source, state-file diff for URL change, dual `/health` check).
