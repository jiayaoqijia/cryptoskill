---
name: set-incident-severity-levels
description: Use when an incident starts or changes and you must pick a severity. Maps user impact, data risk, and blast radius to SEV1-SEV4 so paging, cadence, and escalation follow from the number.
---

# Set Incident Severity Levels

Severity is a decision input, not a feeling. It sets who gets paged, how often stakeholders hear from you, and whether an executive is woken. Guessing either burns goodwill with over-paging or hides a real outage.

## Procedure

1. Measure user impact first: the fraction of users unable to complete a core action. Above `25%`, or any total outage of a revenue path, is at least SEV2; a full outage is SEV1.
2. Check data risk: any confirmed data loss, corruption, or exposure (PII leaving) forces SEV1 regardless of user count — data is not recoverable by rolling back.
3. Check blast radius: single region versus global, single tenant versus all tenants.
4. Map to a level:
   - `SEV1` — total outage or data loss/exposure; page IC + on-call + exec sponsor; comms every 15 min; public status page.
   - `SEV2` — major feature down or heavy degradation for many users; page on-call; comms every 30 min.
   - `SEV3` — degraded, workaround exists, or small subset; ticket plus on-call in hours; comms hourly.
   - `SEV4` — cosmetic or single-user; normal backlog.
5. When uncertainty spans two levels, take the higher until a metric disproves it. Downgrading with evidence is cheap; a missed SEV1 is not.
6. Announce every change with the evidence: `severity SEV2 -> SEV3, error rate 12% -> 0.4% after rollback`.
7. Record the level and the reason in the decision log, not just the number.
8. Re-check severity at each cadence tick; an incident that is worsening for two ticks is under-rated.
9. Publish the level in the channel topic so late joiners and other teams see it without asking.

## Pitfalls

- Letting the loudest affected team define severity, so a cosmetic bug on a managed plan outranks a silent data-loss bug on the free tier.
- Treating "no users complaining" as low severity when the affected path is internal or the outage is at 3am in the primary timezone.
- Leaving severity at SEV1 for hours after mitigation because no one owns the downgrade.
- Using SEV1 for every deployment hiccup, which trains people to ignore pages.
- Rating by cause ("it's only a config change") instead of by effect ("checkout is down").
- Forgetting that a security exposure stays SEV1 even if the surface looks quiet, because detection lag hides the blast radius.

## Verification

    grep -E 'SEV[1-4]' incident/SEV*-2026-*.md | head
    # passes when exactly one current level is set and each change cites the metric that justified it
