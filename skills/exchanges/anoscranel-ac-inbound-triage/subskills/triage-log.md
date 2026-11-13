---
name: triage-log
domain: collaboration/triage-log
trigger: "Recording triage decisions; reviewing the queue on a cadence; measuring how long items wait"
anti_trigger: "Assigning a disposition, severity, or batch in the first place; defining the queue or its service classes"
scope: "The log: one line per item, review cadence, the aging report, median and oldest age instead of raw count"
status: "seedling"
---

# Triage Log

## Standard

- **Anderson, _Kanban_ (2010)**: measure flow, not inventory; lead time, cycle time, and work-item age say more than a count of open items. ⚠️ cited without URL.
- **Little's Law**: wait time tracks queue length; the median and the oldest age reveal whether the queue drains or rots. <https://en.wikipedia.org/wiki/Little%27s_law>

## Decision rules

1. If an item is not in the log, it does not exist to the process; every item gets one line.
2. If a disposition changes, update the line; never add a second line for the same item.
3. If the oldest age keeps rising, the queue is not draining; act on that, not on the count.
4. If the log is not reviewed on its cadence, the cadence is wrong or the log is decorative; fix one.
5. If the log is read by no one, it is a second queue, not a tool; stop adding to it until someone reads it.

## Procedure

1. For each item, write one line: id, service class, disposition, owner, due date, date triaged.
2. Add the line the moment the item is triaged, not at the end of the day.
3. Review the log on a fixed cadence: daily for a fast queue, weekly for a slow one.
4. Each review, produce an aging report: the median age and the oldest age, and the items past their due date.
5. Act on the report: drop or escalate whatever has aged past its target.
6. Keep the log where the next reviewer will actually open it.

## Anti-patterns

- **Counting open items instead of age.** A flat count hides that three items have waited a month. Fix: report median and oldest age.
- **One item, many lines.** The same item is logged again each time it is touched. Fix: update the line, keep the id.
- **Log as a second queue.** Items are written and never read; the log becomes a quieter inbox. Fix: review on cadence or stop logging.
- **Review with no action.** The aging report is read and nothing is dropped or escalated. Fix: end each review with one change.
- **No due date.** An item without a due date can never be overdue. Fix: every scheduled item gets a date.

## Done checklist

- [ ] Every item has one line with id, class, disposition, owner, due, and date.
- [ ] Each item has exactly one line; changes update it, never duplicate it.
- [ ] The log is reviewed on a fixed cadence.
- [ ] Each review produces median age and oldest age, not a raw count.
- [ ] The review ends in at least one drop or escalation.
- [ ] Someone reads the log on the cadence; if not, logging is paused.

## Sources

- Anderson, _Kanban: Successful Evolutionary Change for Your Technology Business_ (2010): ⚠️ cited without URL.
- Little's Law: <https://en.wikipedia.org/wiki/Little%27s_law>