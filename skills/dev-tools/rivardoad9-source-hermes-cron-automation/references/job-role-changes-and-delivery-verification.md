# Changing an existing cron job's ROLE (and verifying what it actually delivered)

Proven 4 Okt 2026 when the narrative-screening lane was demoted from "signal" to "performance tracker".

## 1. Demoting a lane: stop the alerts, keep the recording

A lane whose edge came out unproven should stop shipping alerts — but its state files usually still feed
other jobs (deep dives, dashboards, audits). **Do not pause the cron**: pausing stops the data collection
too, and the audit that produced the verdict then has no fresh input.

Put the switch inside the wrapper script instead. Empty stdout is silent for `no_agent` jobs, so delivery
stops while state/history/ledger writes keep happening:

```bash
OUT=$(python3 detector.py all 2>&1)
if [ -f /home/<user>/.hermes/data/<lane>_alert_on ]; then
    echo "$OUT"
else
    { echo "[$(date '+%F %T %Z')] <lane> (performance-only, alert OFF)"; echo "$OUT"; } \
        >> /home/<user>/.hermes/logs/<lane>.log; exit 0
fi
```

- The flag file **is** the toggle (`touch` to re-enable, `rm` to mute) — the user can flip it without an
  agent edit. Put the toggle commands plus the mute date/reason in the script header and repeat the toggle
  in the reply.
- Verify the mute yourself before claiming it: `OUT=$(bash script.sh); echo ${#OUT}` must print `0`, and the
  log must contain the header line.
- Then re-frame the **reporting** job with the same `job_id` (updated `name` + `prompt`) instead of leaving
  a job called "signal X" that no longer ships signals — otherwise the chat keeps implying the edge you just
  said is unproven.
- After muting, check the daily job still gets fresh data: a cache that used to be refreshed by the silent
  2-hourly recorder now needs its own freshness check (`if cache last bar < expected last closed bar: refresh`).

## 2. Verify the DELIVERED report, not the job status

`last_status: ok` means the run finished, nothing more. To confirm what the user actually received:

```
~/.hermes/cron/output/<job_id>/<YYYY-MM-DD_HH-MM-SS>.md
```

Read the `## Response` section (the agent's final text) and compare its numbers against the script's
stdout in the same file. A child/agent claiming success is a self-report; the numbers are the evidence.
Do this before telling the user a scheduled report "works", and it doubles as the check that the agent
did not invent a figure.

## 3. Hybrid jobs: deterministic script + agent judgement

For audit/scorecard jobs, pass the heavy computation as `script=` (its stdout is injected as context) and
keep the agent for judgement only. Give each number exactly one source of truth:

- the script computes every metric (accuracy, significance, calibration, forward-test);
- the prompt **forbids** the agent from computing or estimating numbers ("semua angka wajib dari output
  script") and forbids raw table dumps (cap the report at ~18 lines);
- the prompt says explicitly what NOT to do when nothing changed, so a quiet day does not produce invented work.

## 4. Correction to the SKILL.md scheduling note

The SKILL.md line "this user: server UTC+8, user WIB UTC+7" is stale — this stack currently runs
WIB-native cron (memory: "Server TZ = WIB; cron native WIB"; a `20 7 * * *` job reports
`next_run_at ...+07:00`). Lesson to keep either way: **verify the mapping before scheduling** with
`date` and the job's `next_run_at`; never carry a TZ assumption forward from an older note.

## 5. Job prompts that must not over-patch

When a cron job is authorised to modify its own strategy script, gate it: patch only on an explicit
"ready to promote" signal from the deterministic data (e.g. live-sample gate passed), and require the job
to re-run the detector's own smoke command afterwards (`python3 detector.py scan --force`) and report a
one-line before → after diff. Without the gate, an "improvement loop" job will rewrite thresholds on noise.
