---
name: backup-and-recovery-drills
domain: security-hardening/backup-and-recovery-drills
trigger: "Verifying that backups restore and recovery plans work."
anti_trigger: "Not for backup product selection, and not for DR plan writing alone."
scope: "A backup is a restore test; a plan is a drill that ran."
status: seedling
---

# Backup and recovery drills

## Standard

A backup that has never been restored is a hypothesis. The verification that matters is the restore test: select a copy, restore it to a clean environment, and compare the result against the source of record. A plan that has never been run is equally a hypothesis, and its verification is the drill: simulate the loss, walk the actual recovery steps with the actual people, and measure how long the service took to return.

Two dimensions decide whether either verification is honest. The first is fidelity: a restore into the same infrastructure with the same people who built it proves less than a restore into a clean environment by whoever would actually be on shift. The second is scope: recovering the files is not recovering the service, and the drill that stops at the data has not tested the part the business cares about, which is the application accepting work again.

Primary sources: <https://www.cisa.gov/> and <https://www.nist.gov/>.

## Decision rules

- Restore-test each backup class on a stated cadence and record results with dates.
- Drill the recovery plan end to end, including the people who would be on shift.
- Measure and record the actual recovery time, not the estimate.
- Include the failure modes a real incident adds: lost credentials, absent staff, blocked egress.
- Test the restore of the most recent copy, not a convenient old one.
- Record the gap list from every drill with owners, and verify fixes at the next drill.

## Procedure

1. Inventory backup classes and their restore owners.
2. Schedule restore tests per class and execute them.
3. Run the recovery drill with shift-accurate staffing.
4. Inject one realistic complication per drill.
5. Measure elapsed time to service-accepting-work.
6. Record gaps and verify fixes next cycle.

## Anti-patterns

- Verifying that backups exist rather than that they restore.
- Drills run by the architecture team rather than the on-call staff.
- Measuring the restore of old copies instead of the latest.
- A plan updated after a drill but never re-run.
- Excluding the credential and access recovery steps because they are inconvenient.

## Done checklist

- [ ] Restore tests per class, dated.
- [ ] Drill executed with shift-accurate staffing.
- [ ] Actual recovery time measured.
- [ ] Complication injected and handled.
- [ ] Latest copy tested.
- [ ] Gap fixes verified next cycle.

## Sources

- Resilience and exercises guidance: <https://www.cisa.gov/>
- Contingency planning standards: <https://www.nist.gov/>
- Ransomware recovery context: <https://www.cisa.gov/>
