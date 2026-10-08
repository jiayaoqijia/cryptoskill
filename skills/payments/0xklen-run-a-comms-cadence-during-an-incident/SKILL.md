---
name: run-a-comms-cadence-during-an-incident
description: Use when an incident is open and stakeholders keep asking for updates. Sets a fixed update interval with one template, so silence never becomes the story and no one cold-calls the IC.
---

# Run a Comms Cadence During an Incident

During an outage the absence of updates is read as incompetence or concealment. A fixed cadence — including updates that say "no change" — keeps stakeholders off the IC's back and puts every team on the same facts.

## Procedure

1. Pick the interval from severity: SEV1 every 15 min, SEV2 every 30 min, SEV3 hourly. Write the next-due time in the channel header.
2. Use one template every time, so readers scan instead of parse:

       [SEV2 14:05] Impact: 40% of checkouts 500. Theory: DB connection pool exhausted.
       Action: draining and resizing pool. Next update: 14:20. Owner: @comms-lead.

3. Post on time even with no change: `[SEV2 14:20] No change; pool resize at 80%, watching error rate. Next 14:35.` A no-change post is a valid update.
4. Keep the raw stream in the incident channel and the summary in the stakeholder channel; do not CC the whole company on every tick.
5. When a new fact changes impact, lead with it and prefix `CHANGE:` so skimmers see it without reading the paragraph.
6. Hand the cadence to a named backup before the comms lead goes offline — the interval must not lapse during a shift gap.
7. At 3x the interval with no post, treat it as a process incident: ping the comms lead and post a fallback status yourself.
8. Keep the message under ~120 words; the impact line and next-update time are the only mandatory fields.
9. Timestamp every post in UTC so the thread merges cleanly with server logs.
10. When resolution lands, post a final update with the end time rather than just going quiet.

## Pitfalls

- The comms lead waits for a real update before posting, so 40 minutes of silence reads as a cover-up.
- Posting a wall of raw terminal output instead of a two-line summary with impact and the next time.
- Broadcasting to all of #general so every update summons twenty unrelated questions back at the IC.
- Letting the cadence drift to "when the IC has a free moment", which never happens during an incident.
- Using local time in one update and UTC in another, so stakeholders misread the window.
- Skipping the final resolved update, so readers assume the incident is still running.

## Verification

    grep -oE '^\[SEV[1-4] [0-9]{2}:[0-9]{2}\]' incident/SEV*-2026-*.md | awk -F'[ :]' '{print $2*60+$3}' | awk 'NR>1 && $1-p>20 {print "gap " $1-p "min"} {p=$1}'
    # passes when no gap exceeds the interval and the last update is younger than the interval
