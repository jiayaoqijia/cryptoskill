---
name: purple-teaming
domain: security-hardening/purple-teaming
trigger: "Closing the loop between attack technique and detection coverage."
anti_trigger: "Not for unbounded pentesting, and not for red-team scorekeeping."
scope: "Attack, detect, and feed the gap back into the detections."
status: seedling
---

# Purple teaming

## Standard

Purple teaming is the deliberate pairing of an attack exercise with the defenders watching it: the attacker performs a named technique in the live estate, the defenders attempt to see it with current telemetry and detections, and the gap between the two — performed but unseen, or seen but too late — becomes a backlog item. The exercise's product is not a report card but a measurable change in coverage.

This is where it differs from a pentest. A pentest answers whether the environment can be compromised; a purple exercise answers whether the compromise would have been noticed, and then re-answers it after the fix. The loop is the point: technique, telemetry, detection, test, re-test. Coverage improved without the re-test is asserted; coverage improved with it is shown.

Primary sources: <https://attack.mitre.org/> and <https://www.cisa.gov/>.

## Decision rules

- Scope each exercise to named techniques with their adversary mapping.
- Confirm the telemetry for each technique exists before running it.
- Run the technique live and record what fired, what saw-but-did-not-alert, and what saw nothing.
- Convert every gap into a detection or collection backlog item with an owner.
- Re-run the technique after the fix; the second run is the deliverable.
- Record end-to-end time from technique execution to detection visibility.

## Procedure

1. Choose techniques and confirm their relevance to the estate.
2. Verify telemetry coverage for the techniques' evidence.
3. Execute and observe; record the three outcomes per technique.
4. Write the gap list with owners and dates.
5. Fix the detections or collections.
6. Re-execute and record the measured improvement.

## Anti-patterns

- Running attacks nobody watches, which is a pentest, not purple.
- Fixing detections but never re-running the technique.
- Exercise reports as trophies rather than backlog change.
- Techniques chosen for spectacle rather than estate relevance.
- The defenders unable to distinguish the exercise from a real event because it was not coordinated.

## Done checklist

- [ ] Techniques named and mapped.
- [ ] Telemetry verified pre-run.
- [ ] Three outcomes recorded per technique.
- [ ] Gap list with owners and dates.
- [ ] Fixes deployed.
- [ ] Re-run results recorded as the deliverable.

The cadence is also a finding source: coverage decays as the estate changes, so a technique detected at the last exercise may go quiet after a logging change nobody connected to security. A standing re-run of a fixed technique set catches the decay that one-off exercises miss.

## Sources

- Technique reference framework: <https://attack.mitre.org/>
- Exercise methodologies: <https://www.cisa.gov/>
- Detection context: <https://csrc.nist.gov/>
