---
name: alert-triage-and-soc
domain: security-hardening/alert-triage-and-soc
trigger: "Running or assessing an alert queue and its triage."
anti_trigger: "Not for writing the detections, and not for incident comms."
scope: "The queue, its fatigue, and the triage that keeps signal above noise."
status: seedling
---

# Alert triage and the SOC

## Standard

The SOC queue is a resource-allocation problem wearing a security costume. Alerts arrive faster than analysts can close them; the queue lengthens; the analyst buys speed with shallow closes; shallow closes generate re-alerts; the queue lengthens. Alert fatigue is not an attitude problem but a budget problem, and its fix begins upstream — in the detections that generate unactionable volume — not downstream in the analysts.

The triage system is what keeps signal above noise: every alert gets an explicit disposition path, criteria for escalate, close-as-benign, or merge, and a feedback loop that reaches the detection engineer. Closed-without-investigation is the metric that reveals the system's honesty, because it is the path by which a real alert becomes a missed one under volume pressure.

Primary sources: <https://www.cisa.gov/> and <https://www.nist.gov/>.

## Decision rules

- Record each alert class with its volume, its true-positive rate, and its actionability.
- Define the disposition criteria — escalate, benign-close, merge — in writing.
- Track time-to-first-look and queue depth per shift, not only as averages.
- Count closed-without-investigation and treat a rise as an upstream signal.
- Route the benign-close reasons back to detection engineering weekly.
- Cap the queue: define when volume exceeds capacity and triggers tuning, not endurance.

## Procedure

1. Classify the alert types and measure each volume and precision.
2. Write disposition criteria for each class.
3. Instrument the queue: depth, first-look time, close reasons.
4. Review benign-close reasons with the detection owners.
5. Set the volume threshold that forces rule tuning.
6. Record the metrics with dates in the ops record.

## Anti-patterns

- Measuring closure speed while ignoring closure quality.
- Treating analyst burnout as a hiring metric rather than a noise metric.
- No written disposition criteria, so triage differs by shift.
- Feedback from closes never reaching the rule authors.
- The queue as badge of honor instead of a defect signal.

## Done checklist

- [ ] Alert classes measured for volume and precision.
- [ ] Disposition criteria written.
- [ ] Queue instrumented per shift.
- [ ] Close-reason feedback loop running.
- [ ] Volume threshold defined.
- [ ] Metrics recorded with dates.

The queue also has a shift-invariance test worth running: compare dispositions for the same alert class across shifts, since unwritten criteria drift by who is on duty. Where the same alert is escalated by one shift and benign-closed by another, the criteria are not actually written down, whatever the wiki says.

## Sources

- Security operations guidance: <https://www.cisa.gov/>
- Incident-handling reference: <https://www.nist.gov/>
- SOC process context: <https://www.sans.org/>
