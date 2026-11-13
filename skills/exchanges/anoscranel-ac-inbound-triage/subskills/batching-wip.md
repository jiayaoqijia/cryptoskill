---
name: batching-wip
domain: collaboration/batching-wip
trigger: "Grouping triaged work into batches; setting a work-in-progress limit; protecting time for deep work against interruptions"
anti_trigger: "Assigning a disposition or severity to an item; defining the queue or logging triage outcomes"
scope: "Batching by type and honest WIP limits: context-switch cost, protected blocks, batch windows"
status: "seedling"
---

# Batching and WIP Limits

## Standard

- **Anderson, _Kanban_ (2010)**: limiting work in progress shortens cycle time; when the limit is hit, new work waits, which forces a decision about what is actually most important. ⚠️ cited without URL.
- **Graham, "Maker's Schedule, Manager's Schedule" (2009)**: deep work needs long unbroken blocks; a schedule built from half-hour slots destroys it. <http://www.paulgraham.com/makersschedule.html>
- **American Psychological Association, "Multitasking"**: switching tasks carries a measurable cost; even brief switches slow the primary task. <https://www.apa.org/topics/research/multitasking>

## Decision rules

1. If work is deep, give it a protected block. If it is shallow, give it a batch window.
2. If the WIP limit is full, nothing new starts; the next item waits for a slot.
3. If an item would break the WIP limit, that forces the triage question: which open item matters least?
4. If tasks are the same type, batch them; if they differ, the switch cost is real.
5. If the WIP limit is never hit, it is too high; lower it until it occasionally binds.

## Procedure

1. Sort triaged work into types: deep (writing, designing, debugging) and shallow (replying, reviewing, filing).
2. Set a WIP limit: the number of items in flight at once. Start low, often three.
3. Block two or three long windows a day for deep work; nothing interrupts them.
4. Give shallow work one or two batch windows a day; do it all there.
5. When the WIP limit binds, do not start new work; pick the least important open item and finish or defer it.
6. Revisit the limit weekly; if the queue drains and quality holds, keep it, otherwise lower it.

## Anti-patterns

- **WIP limit set and ignored.** Work starts anyway and the limit is decoration. Fix: enforce the limit at the intake point.
- **No protected block.** Deep work is interrupted until nothing deep gets done. Fix: block the time and defend it.
- **Shallow work scattered.** Reply-by-reply all day costs a switch each time. Fix: batch it into a window.
- **Limit too high to bind.** A limit of ten that never fills is not a limit. Fix: lower it until it binds.
- **Limit used to avoid deciding.** New work waits forever instead of the least-important item being dropped. Fix: use the limit to force the choice, not defer it.

## Done checklist

- [ ] Work is sorted into deep and shallow types.
- [ ] A WIP limit is set and enforced at intake.
- [ ] Deep work has protected blocks.
- [ ] Shallow work has batch windows.
- [ ] A full WIP limit forces a drop or defer, not a wait.
- [ ] The limit is reviewed weekly.

## Sources

- Anderson, _Kanban: Successful Evolutionary Change for Your Technology Business_ (2010): ⚠️ cited without URL.
- Graham, "Maker's Schedule, Manager's Schedule" (2009): <http://www.paulgraham.com/makersschedule.html>
- American Psychological Association, "Multitasking": <https://www.apa.org/topics/research/multitasking>