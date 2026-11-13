---
name: phishing-readiness
domain: security-hardening/phishing-readiness
trigger: "Measuring and improving how an organization handles phishing."
anti_trigger: "Not for blaming clickers, and not for building the mail filters."
scope: "Simulations, reporting culture, and what a click rate measures."
status: seedling
---

# Phishing readiness

## Standard

A phishing simulation measures one thing directly — the click rate on that simulation — and several things indirectly: whether reporting is easy, whether reports reach someone who acts, and whether the response to a real phish is practiced. The click rate itself is the weakest of these signals, because a campaign that is too easy to spot shows nothing, and one that is too hard shows only that a convincing phish deceives. The useful metrics are behind the click: how fast did reports arrive, and what happened after.

The failure mode of the practice is cultural. Naming clickers converts a readiness program into a punishment program, reports drop, and the single genuine defense — people willing to say "I think this is bad" — is suppressed. A program with a rising click rate and a rising report rate is healthier than one with a falling click rate and silence, because the second has stopped seeing itself.

Primary sources: <https://www.cisa.gov/> and <https://www.ftc.gov/>.

## Decision rules

- Record the simulation's difficulty and target audience with each campaign's results.
- Track clicks, reports, and report-to-click ratio; publish all three, not one.
- Measure the time from send to first report as the readiness metric.
- Make reporting one action from any client, and confirm receipt to the reporter.
- Deliver training to clickers privately, never in league tables.
- Test the response path itself: does a reported phish reach containment quickly?

## Procedure

1. Design the campaign with a stated difficulty and audience.
2. Send and instrument clicks, reports, and timings.
3. Record all three metrics by campaign, never names.
4. Confirm receipt to reporters and route to response.
5. Train the audience shown by the data, privately.
6. Exercise the response path end to end per campaign.

## Anti-patterns

- Publishing clicker lists, which suppresses the reporting the program needs.
- Chasing a low click rate with obvious fakes.
- Reporting the click rate without the report rate beside it.
- No feedback to reporters, so reports stop feeling useful.
- Never testing what happens after the report arrives.

## Done checklist

- [ ] Campaign difficulty and audience recorded.
- [ ] Clicks, reports, and ratio tracked.
- [ ] Time-to-first-report measured.
- [ ] One-action reporting confirmed working.
- [ ] Training delivered privately.
- [ ] Response path exercised.

## Sources

- Phishing guidance and reporting: <https://www.cisa.gov/>
- Consumer fraud context: <https://www.ftc.gov/>
- Awareness standards context: <https://csrc.nist.gov/>
