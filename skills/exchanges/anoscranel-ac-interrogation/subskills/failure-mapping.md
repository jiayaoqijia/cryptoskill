---
name: failure-mapping
domain: critical-thinking/failure-mapping
trigger: "What kills this plan; run a pre-mortem on this; what is the fastest way this fails; poke holes in the risk list; why do similar projects always run late"
anti_trigger: "Listing what the plan assumes rather than how it breaks (subskills/assumption-audit.md); choosing among rival options (subskills/alternative-forcing.md); the close-out record (subskills/close-and-stop.md)"
scope: "Pre-mortem, inversion, weakest-link search, reference-class base rates, and naming the failure that actually ends the plan"
status: "seedling"
---

# Failure Mapping

## Standard

- **Klein, "Performing a Project Premortem"** (HBR, 2007): imagine the project has already failed and write the history of why; the exercise surfaces risks that hope-shaped meetings suppress. <https://hbr.org/2007/09/performing-a-project-premortem> ⚠️ paywalled.
- **Munger, _Poor Charlie's Almanack_**: invert — ask what would guarantee failure, then avoid it. ⚠️ cited without URL.
- **Flyvbjerg, "From Nobel Prize to Project Management"** (2006): reference-class forecasting — base rates from similar projects beat inside-view estimates. ⚠️ cited without URL.
- **Duke, _Quit_ (2022)**: set failure conditions in advance; deciding when to walk away is part of the plan, not a defeat. ⚠️ cited without URL.

## Decision rules

1. If no pre-mortem exists, run one before any other analysis; the failure history is written in the past tense.
2. If a listed failure is vague — "execution risk", "market risk" — push for a mechanism: who fails, at which step, observed how?
3. If the plan hangs on one dependency, name it the weakest link and check it first.
4. If similar plans exist in the world, pull their base rate before trusting an inside estimate.
5. If a failure ends the plan outright, it gets kill criteria; if the plan can absorb it, it gets a mitigation.
6. If the list passes ten items, rank by damage and work the top two; the rest go to the ledger.
7. If the author resists the pre-mortem, run inversion instead: "what is the fastest path to failure?"

## Procedure

1. Set the scene: "it is twelve months later. The plan failed."
2. Write the failure history in the past tense — first what happened, then what, then what. Ten minutes, silent, individually if a group.
3. Read the histories aloud; collect them without judging.
4. Invert: list what would guarantee failure — the fastest path down.
5. Find the weakest link: the single dependency whose failure cascades furthest.
6. Pull the reference class: find three similar plans, succeeded or failed; note their base rate and compare.
7. Classify every failure: fatal (ends the plan) or recoverable (costs time or money).
8. Name the one failure that actually ends the plan — the headline risk — and write its kill criteria: the observable signal that means stop.

## Anti-patterns

- **Risk-register theater.** Fifteen generic risks, none actionable. Fix: rank by damage; make each one a mechanism.
- **Premortem after commitment.** Runs as excuse collection for a done deal. Fix: run it while the plan can still change.
- **Base-rate denial.** "Our case is different", with no named difference. Fix: name the difference or accept the base rate.
- **Fatal and recoverable mingled.** A lost week and a lost company treated alike. Fix: classify first, plan second.
- **Hole-poking as sport.** An unbounded list of every conceivable failure. Fix: stop when new failures are variations of named ones.

## Done checklist

- [ ] Failure history written in the past tense.
- [ ] Inversion list created: the fastest path to failure.
- [ ] Weakest link named explicitly.
- [ ] Reference class pulled: three similar cases and their base rate.
- [ ] Headline failure named with kill criteria.

## Sources

- Klein, "Performing a Project Premortem", HBR 2007: <https://hbr.org/2007/09/performing-a-project-premortem>
- Flyvbjerg (2006). ⚠️ cited without URL.
- Duke, _Quit_ (2022). ⚠️ cited without URL.
- Munger, _Poor Charlie's Almanack_. ⚠️ cited without URL.
