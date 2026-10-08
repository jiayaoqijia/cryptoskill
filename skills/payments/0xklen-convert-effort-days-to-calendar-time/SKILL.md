---
name: convert-effort-days-to-calendar-time
description: Use when a day-by-day work estimate is being read as elapsed days. Applies a focus factor for meetings, interruptions and on-call so the effort total becomes a realistic calendar duration.
---

# Convert effort days to calendar time

One "dev-day" of work is not one calendar day. Meetings, interruptions, reviews and on-call eat the clock, and a 20-effort-day plan quietly becomes six weeks. Convert explicitly, with a factor you can defend.

## Procedure

1. Start with raw effort: sum the task durations in person-days, e.g. 20 person-days.
2. Pick a focus factor — the fraction of a working day spent on the actual task, logged in `notes/capacity.md`. Realistic values run 0.5–0.8; a person juggling on-call or two projects sits near 0.5.
3. Divide effort by the available-fraction to get calendar days per person:

       python3 -c "effort=20; focus=0.7; print('calendar days', round(effort/focus,1))"
       calendar days 28.6

4. Subtract known non-work days in the window: public holidays, a team offsite, release freeze. Do not assume a five-day week.
5. Account for people, not just days. Two people on independent work nearly halve the time; two on the same small task do not (coordination cost) — model parallel work as a chain only when the pieces are truly independent.
6. If the window includes a person's holiday, reduce their availability rather than pretending they are full-time.

   Record each person's factor separately; a team average hides whoever is effectively part-time.
7. Recompute after any schedule change; the factor is a property of the environment, not a constant.

## Pitfalls

- Reporting effort days as calendar days, the single most common source of "but you said two weeks."
- Using focus factor 1.0 for a person who is on-call or pairing, which is never achievable.
- Assuming a 5-day week and 8 productive hours; realistically 6 or fewer hours are deep-work.
- Splitting one small task across three people to "compress" it, when coordination makes it slower.
- Forgetting that the estimate itself and code review consume the same hours, not extra ones.

## Verification

    python3 -c "print(round(20/0.7,1), 'vs', 20)"
    # 28.6 vs 20 — the calendar duration is longer than the effort; report both

Report effort days, the focus factor used and why, and the resulting calendar duration with holidays removed.
