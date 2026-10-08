---
name: run-a-blameless-postmortem
description: Use when an incident has ended and a write-up is required — produces a postmortem with contributing factors and action items that each carry an owner, a date and a measurable outcome.
---

# Run a blameless postmortem

Blameless does not mean no accountability; it means the system failed and the system gets fixed. Name the conditions that made failure likely, and name humans only for actions they owned, described in terms of what was knowable at the time.

## Procedure

1. Start within 48 hours while memory is fresh, and build from the incident timeline, not recollection. Facts before story.

2. Use a fixed structure: Impact (who, how many, how long), Timeline (T0→resolved), Detection (what noticed it and how long that took), Contributing factors, What went well, Action items.

3. Quantify impact with real numbers: affected request count, distinct users, duration in minutes, and revenue if tracked. "Some users were briefly affected" is not impact.

4. Write contributing factors as conditions, not causes: "the canary compared against the previous day's baseline, which masked a global regression" rather than "Bob skipped the check".

5. Cap contributing factors at five and rank by leverage — which single change most reduces recurrence. A postmortem with fifteen factors fixes none.

6. Give every action item a verb, a verifiable outcome, a named owner and a due date. "Improve monitoring" fails; "add alert `error_ratio>1% for 5m` on checkout, owner @sre, due 2026-10-20" passes. File each as a ticket before the meeting ends.

7. Separate preventive actions from detection and mitigation actions. Most teams over-invest in prevention and under-invest in shortening detection — the latter is usually the bigger MTTR lever.

8. Publish to a searchable location and link prior incidents with the same factor. Three incidents sharing a factor means the earlier action items were not real.

## Pitfalls

- A single "root cause": complex failures have several necessary conditions, and forcing one hides the rest.
- Action items with no owner or date, which then rot. Review open items monthly and re-date or drop them explicitly.
- Blame laundered into passive voice ("the button was pressed"), implying fault while sounding blameless — state the timeline fact instead.
- Fixing only prevention, so the class recurs because detection still takes 20 minutes.

## Verification

    grep -c 'Owner:' postmortem.md                       # >= number of action items
    grep -Ec 'due 20[0-9]{2}-[0-9]{2}-[0-9]{2}' postmortem.md
    # every action item has an owner and a date; none say 'improve' without a metric

Report: impact numbers, the top contributing factor and its leverage, N action items each with owner and date filed as tickets, and how many address detection versus prevention.
