---
name: queue-definition
domain: collaboration/queue-definition
trigger: "The inbox has no single intake point; items arrive through many channels; scope is unclear; no response-time target exists"
anti_trigger: "Deciding the order of a queue that is already defined; choosing act-now versus schedule versus drop for a specific item"
scope: "Define the queue before triaging it: one intake point, in scope versus deflected, service classes with response targets, queue versus backlog"
status: "seedling"
---

# Queue Definition

## Standard

- **Scrum Guide (2020)**: a backlog is an ordered list of work to be done, not a promise to do all of it. <https://scrumguides.org/scrum-guide.html>
- **Anderson, _Kanban_ (2010)**: make work visible and limit work in progress; a queue is work waiting, a backlog is work accepted but not yet scheduled. ⚠️ cited without URL.
- **Little's Law**: average wait time scales with the number of items in a queue, so an unbounded queue grows wait time without bound. <https://en.wikipedia.org/wiki/Little%27s_law>

## Decision rules

1. If items arrive through more than one channel, name one intake point and redirect every other channel to it.
2. If an item is outside scope, deflect it before triage; it costs no triage time.
3. If a class of work has no response target, do not triage it yet; set the target first.
4. If work is waiting to be worked, it is a queue. If work is accepted but not yet scheduled, it is a backlog.
5. If a service class has no owner, it will not be met; assign one before relying on the target.

## Procedure

1. List every channel work arrives through: email, chat, tickets, walk-ups, voice.
2. Pick the single intake point; post a routing rule that sends every other channel there.
3. Write the scope: what the queue accepts, and what it deflects without reading.
4. Name the service classes and one response target each. A target is "first response within X", not "done within X".
5. Split the queue from the backlog: the queue is waiting to be triaged; the backlog is triaged and scheduled.
6. Record the intake point, scope, classes, and targets in one place the team can see.

## Anti-patterns

- **Many intake points.** Work hides in direct messages and side channels. Fix: one intake point and a redirect for the rest.
- **Triage before scope.** Reading every item wastes time on out-of-scope noise. Fix: deflect first.
- **No response target.** "ASAP" is not a target; nothing can be measured against it. Fix: a stated time per class.
- **Queue and backlog conflated.** Un-triaged work mixed with scheduled work looks bigger than it is. Fix: two named lists.
- **Targets without owners.** A class with a target but no owner is a wish. Fix: name the owner.

## Done checklist

- [ ] One intake point exists and every other channel redirects to it.
- [ ] Scope is written: in-scope and deflected items are named.
- [ ] Each service class has a stated response target and an owner.
- [ ] The queue and the backlog are two separate lists.
- [ ] The definitions are written down where the team can see them.

## Sources

- Scrum Guide (2020): <https://scrumguides.org/scrum-guide.html>
- Anderson, _Kanban: Successful Evolutionary Change for Your Technology Business_ (2010): ⚠️ cited without URL.
- Little's Law: <https://en.wikipedia.org/wiki/Little%27s_law>