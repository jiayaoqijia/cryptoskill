---
name: slo-reliability
domain: software-engineering/slo-reliability
trigger: "\"set an SLO\", \"how much downtime is allowed\", \"write the alert rule\", \"backup and DR plan\"."
anti_trigger: "Adding telemetry (subskills/observability.md); running the outage and postmortem (subskills/incident-response.md); rollback and ramp mechanics; load testing a latency budget."
scope: "SLIs, SLOs, error budgets, alert rules, backup and DR targets"
status: "seedling"
---

# SLO & Reliability

## Standard

- **SLI then SLO** (https://sre.google/workbook/implementing-slos): an SLI is good events over valid events on a 0–100 % scale; an SLO is its target over a stated window.
- **Error budget** = 100 % minus the SLO (SRE Book ch3). 99.9 % over 30 days allows about 43 minutes of downtime (about 40 over 28 days); 99.99 % allows about 4.3 minutes over 30 days. Each extra nine costs roughly an order of magnitude.
- **Multi-window burn-rate alerting** (Workbook ch5, table 5-8): page on 14.4× burn over 1 h + 5 min, 6× over 6 h + 30 min; ticket on 1× over 3 d + 6 h.
- **RTO and RPO** per service tier, with a ladder from backup-restore to hot standby.
- **Budget policy** (SRE Book ch3): when the budget is exhausted, feature launches gate or freeze until reliability recovers.

## Decision rules

1. An SLO covers one path that matters: signup, checkout or the paid API.
2. Two SLIs are enough: availability and a latency percentile.
3. Alert on budget burn, never on a raw error rate.
4. Every SLO record names an owner, an approver, a review date and a consumption rule.
5. Backups are untested until a restore has run: restore-test monthly, failover drill twice a year, tabletop quarterly.
6. DR targets are per tier: tier 1 gets warm standby, tier 3 gets scheduled backup-restore.
7. Dependency targets belong here too: every outbound call has a timeout, retries use jittered backoff, and a breaker stops retries into a dead dependency.
8. ⚠️ The restore-test cadence is practitioner convention.

## Procedure

1. Name the path and its window (30 days is the default).
2. Define the SLI in the telemetry you have (subskills/observability.md).
3. Write the SLO record: target, window, owner, approver, review date, consumption rule.
4. Compute the budget in time: 99.9 % over 30 days ≈ 43 minutes.
5. Write the burn-rate rules with paired windows:
   ```
   page   burn(1h) > 14.4 and burn(5m) > 14.4
   page   burn(6h) > 6    and burn(30m) > 6
   ticket burn(3d) > 1    and burn(6h) > 1
   ```
6. Route pages to a human, tickets to the queue.
7. Set RTO and RPO per tier, then pick the DR row that meets them.
8. Write the restore runbook. Run it once, timed, against a real backup.
9. Keep the drill on schedule.
10. Review the SLO record quarterly.

## Anti-patterns

- An SLO per service, so nothing has one owner.
- Alerts on raw error rate, waking people for a bad minute.
- A budget with no consumption rule.
- A backup job that has never been restored.
- Active-active claimed while the data sync is unsolved.
- A 99.99 % target on a two-person team.

## Done checklist

- [ ] One path, two SLIs, one written SLO record.
- [ ] Burn-rate rules with paired windows.
- [ ] Budget stated in minutes.
- [ ] RTO and RPO recorded per tier.
- [ ] A timed restore has been run.
- [ ] Review date set.

## Sources

- <https://stackpractices.com/guides/disaster-recovery-guide>
- <https://sre.google/workbook/alerting-on-slos/>
- https://sre.google/workbook/alerting-on-slos/
