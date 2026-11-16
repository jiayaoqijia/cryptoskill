---
name: guardrail-incidents
domain: software-engineering/guardrail-incidents
trigger: "Handling a guardrail firing: capture, review, and the fix loop."
anti_trigger: "Not for content adjudication policy, and not for SLO alerting."
scope: "What firing a guardrail triggers: capture, review, and the fix loop."
status: seedling
---

# Guardrail incidents

## Standard

A firing is an operational event, not a metric. When a guardrail blocks or holds, three things happen: capture (the full context of the attempted action is preserved — task context, model reasoning, proposed call, verdict, decision), review (the firing is classified within a fixed vocabulary: true-positive catch, near-miss, screen false-positive, wiring defect), and feed-forward (the finding routes to where it is fixed: the action-class table, the screen threshold, the tool manifest, or the actual task).

The fire vocabulary distinguishes two loud failure syndromes that kill agent deployments: the noisy guardrail (false positives erode trust until someone disables the layer) and the silent death (zero firings over time is treated as success when it can equally mean the wiring broke). Both are monitored by firing-rate trends with per-class labels, and zero-firing/zero-audit intervals are treated as signals, not blessings.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://casp-uk.net/casp-tools-checklists/>.

## Decision rules

- Every firing captures the full context automatically — task, reasoning, proposed call, verdict, and disposition.
- Classify each firing in a small fixed vocabulary: catch, near-miss, false-positive, wiring defect.
- Firing-rate trends are monitored per class; zero-firing periods trigger a wiring audit.
- False-positive classification feeds back into threshold tuning as a recorded, dated decision.
- True-positive catches feed into a taxonomy of what the agent actually tried — informing future action-class rows.
- Repeated firings on the same run escalate disposition (hold rising to kill) rather than repeating the same hold.

## Procedure

1. Capture the firing automatically with full replayable context.
2. Classify it in the fixed vocabulary within the review SLA.
3. Route the finding to its fix: table row, threshold, manifest entry, or monitored task class.
4. Log the fix consumed, with dates, like a postmortem action item.
5. Track weekly: firing counts by class, disposition distribution, review SLA adherence.
6. Audit any interval of zero firings with zero reviews for wiring defects.

## Anti-patterns

- Firings that are counted as metrics and never reviewed individually.
- A single-catch binary (all catches where near-misses and wiring defects silently collapse.
- Firing spikes triggering immediate threshold loosening rather than trend analysis.
- No escalation for repeat offenders within a run.
- Treating a zero-firing month as confirmed success rather than a signal to audit the wiring.

## Done checklist

- [ ] Firing capture automatic, replayable.
- [ ] Classification vocabulary fixed and small.
- [ ] Routing to a named fix surface for each class.
- [ ] Weekly trend tracking in place.
- [ ] Escalation rule for repeats.
- [ ] Zero-firing audits scheduled.

## Sources

- OWASP LLM Top 10, monitoring and response framings: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Review-instrument practice: <https://casp-uk.net/casp-tools-checklists/>
- AI incident framing: <https://www.nist.gov/itl/ai-risk-management-framework>
