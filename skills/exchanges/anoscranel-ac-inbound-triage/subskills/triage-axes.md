---
name: triage-axes
domain: collaboration/triage-axes
trigger: "Deciding which item in a queue comes first; two things are both claimed urgent; the order of attack is not obvious"
anti_trigger: "Assigning a disposition to an item once its order is settled; defining the queue itself or its service classes"
scope: "The axes that decide order: urgency, impact, reversibility, effort, dependency, ownership; the Eisenhower matrix as a frame"
status: "seedling"
---

# Triage Axes

## Standard

- **Eisenhower matrix**: sort items on two axes, urgent and important; do urgent-and-important, schedule important, delegate urgent, drop neither. ⚠️ The attribution to Eisenhower is disputed; no primary source shows he coined the two-by-two grid. It is a widely used frame, not a law.
- **Covey, _The 7 Habits of Highly Effective People_ (1989)**: urgency crowds out importance; the urgent-and-important quadrant is where people burn out. <https://www.franklincovey.com/the-7-habits/>
- **Bezos, 2015 shareholder letter**: classify decisions as one-way doors or two-way doors; reversible choices can be made fast with less analysis. <https://www.aboutamazon.com/news/company-news/2015-letter-to-shareholders>

## Decision rules

1. If a deadline is real and external, it raises urgency. If the deadline is only stated, urgency does not change.
2. If a blocked item blocks others, it outranks a blocked item that blocks no one.
3. If an action is reversible, decide fast. If it is a one-way door, slow down.
4. If effort is tiny and impact is real, do it before anything bigger; effort breaks ties, not the ranking.
5. If an item is not yours at all, stop scoring it; route it to its owner.
6. If two items tie on every axis, pick one and move on; the tie itself is not information.

## Procedure

1. For each waiting item, write one line: what is it, who is blocked, what breaks if it waits.
2. Score urgency against a real deadline, not a stated one. Ask whose deadline it is.
3. Score impact by who is blocked and what breaks; count people and blast radius.
4. Ask whether the action can be undone. Two-way doors rank lower in caution, higher in speed.
5. Estimate effort in rough units: minutes, hours, days. Use it to break ties only.
6. Ask whether the item is yours. If not, route it before scoring further.
7. Rank by urgency, then impact, then reversibility; use effort and dependency as tiebreakers.

## Anti-patterns

- **Stated deadline treated as real.** "Need it Friday" with no consequence is a wish, not a deadline. Fix: verify the consequence of missing it.
- **Loudest voice wins.** The most recent or most anxious requester jumps the queue. Fix: score on the axes, not on volume.
- **Effort drives ranking.** Small easy items run first while the blocking one rots. Fix: impact first, effort last.
- **Scoring what is not yours.** Time spent triaging someone else's item is wasted. Fix: route on ownership before scoring.
- **Tie broken by more analysis.** Two equal items get researched into the ground. Fix: pick one, note the other, move on.

## Done checklist

- [ ] Each item has a one-line note: what it is, who is blocked, what breaks.
- [ ] Urgency is tied to a real deadline, not a stated one.
- [ ] Impact counts people blocked and blast radius.
- [ ] Reversibility is marked for each action.
- [ ] Effort and dependency are used only as tiebreakers.
- [ ] Items not owned by me are routed before scoring.

## Sources

- Eisenhower matrix, attribution note: <https://en.wikipedia.org/wiki/Time_management#The_Eisenhower_Method>
- Covey, _The 7 Habits of Highly Effective People_ (1989): <https://www.franklincovey.com/the-7-habits/>
- Bezos, 2015 shareholder letter: <https://www.aboutamazon.com/news/company-news/2015-letter-to-shareholders>