---
name: react-render-delta
description: Prove a React rendering or memoization change actually reduced work, with a delivery gate and a reported band. Covers re-render counts (why-did-you-render), selector recomputes (reselect's real `.recomputations()` API), and A/B arms toggled at a FIXED commit rather than across a merge boundary. The falsifier is an arm whose treatment never reached the built bundle — a null from undelivered treatment is indistinguishable from a null from a small effect and reports as the second. Triggers on /mms-react-render-delta, or when asked to prove a component stopped over-rendering, measure selector recomputation, validate a memoization/React Compiler change, run a render-count A/B, or interpret a re-render benchmark. Callable by `evidence` as its React render & selector proof engine.
maturity: experimental
---

# /react-render-delta

A render-count number is worthless until two things are true: the **treatment reached the
artifact the browser executes**, and the number is reported as a **band** rather than a point.
Most of this skill is those two checks. The measurement itself is easy; the failure mode is
reporting a difference between arms that never differed.

> **Falsifier.** An arm whose manipulation cannot be observed in the built bundle. If you
> cannot point at output that differs *in kind* between arms — a symbol present in one and
> absent in the other, a flag line in a log — the A/B is not designed yet, and any delta it
> produces is noise with a story attached.

## Method

1. **Name the delivery check before building arms, and verify it emits.** State how the run
   itself will show the arms differ, then confirm that output exists on one real build before
   scaling to N repeats. This ordering is the whole skill. A measurement launched before the
   instrument is proven emits a null that reads exactly like "no effect".

2. **Derive the needle from output at the stage you will grep, not one stage upstream.**
   Compiler and bundler output are not the same text. Worked failures, both real:
   - React Compiler at `target: '17'` emits `react-compiler-runtime`; at `target: '19'` it
     emits `react/compiler-runtime`. Grepping for the wrong one returns 0 in *both* arms and
     fails the arm that actually got the treatment.
   - `_c(` is the form **babel** emits. Metro transforms it further — in a real 119 MB React
     Native bundle it scored 13 hits, every one a minified vendor identifier
     (`function _c(e,t){return e|t}`), while the true compiler output went uncounted. The form
     that survived metro was `memo_cache_sentinel` (4681 in the treated arm vs 166 in the
     control). Same needle, two bundlers, two different answers.

   Compile one real file through the project's own config and read the output. Ten minutes
   here saves a whole run.

3. **A name is not a witness — count what only exists when the module is included.** A bare
   module specifier appears in bundled `package.json` dependency lists whether or not the
   module was ever pulled in; a clean control arm scored exactly 1 that way and was wrongly
   failed. Gate on artifacts that cannot appear otherwise (a runtime sentinel, a compiled call
   site). Keep the specifier count as a diagnostic — 3081-vs-1 is informative, it just isn't a
   boolean.

4. **Use the library's real counter before injecting your own.** `reselect` exposes
   **`.recomputations()`** on memoized selectors — a genuine API, not a patch. Read it (sample
   on an interval if the count should visibly climb). An injected `console.log` you added to a
   selector body is an authored claim, not an observation; reach for it only when no real API
   exists, and say so when you do. *(Note: the evidence catalog's render-and-selector entry long claimed there
   was "no built-in selector-call counter". There is.)*

5. **Toggle at a fixed commit, not across a merge boundary.** Same tree in both arms, one
   thing different. A commit boundary drags in unrelated change you will then be unable to
   exclude. When the real commit bundles two changes (a scope change *and* a version bump),
   reproduce only the one under test — moving both reintroduces the confound the fixed-commit
   design exists to remove, and can silently flip your delivery needle mid-experiment.

6. **Repeat the capture, not the build; report the band.** Counts vary run to run — one
   baseline measured 153/164/224 across three runs. The build dominates cost (~6 min vs ~90 s
   per capture), so repeats are nearly free. Publish one artifact; report every repeat's count.

7. **When the delta is under the spread, say "not resolvable at this n" and give the MDE.**
   Not "no effect". State the smallest detectable effect and what n would resolve the observed
   difference. A real worked result: 112–128 vs 115–133, delta 4.6%, t=1.33 — with delivery
   proven (1244 compiled sites vs 0), so the null was about effect size, not plumbing.

8. **A check that finds nothing needs a positive control.** Before believing a zero, confirm
   the same check finds something it should. A search that returned "0 references" looked like
   confirmation until searching for a string known to be present *also* returned 0 — the index
   didn't reach that content and the zero meant nothing.

## Gates, in order

| gate | asserts | on failure |
|---|---|---|
| source manipulation | the intended edit applied, and *only* it | abort the arm |
| **delivery** | the change reached the built bundle | abort **before any capture** |
| metric | the instrument emitted a non-zero count on capture 1 | abort before spending repeats |

Each catches what the previous cannot. Source changing is not delivery; delivery is not the
instrument working. Wire them as script-level aborts so a broken arm cannot report a number —
"refusing to emit a render count from an arm whose treatment is unproven" is the correct
output, and it is not a failure of the run.

**Never relax a gate to make an arm pass.** When a gate fires, go read the artifact and find
the mechanism first. Loosening is the work-reducing direction, which is exactly where scrutiny
collapses. Demoting a needle from gate to diagnostic *after* proving it fires for an unrelated
reason is legitimate; doing it because the arm failed is not.

## What the count does and does not mean

WDYR counts **every** re-render in the measured window, including boot settling — not only the
cascade a given fix targeted. So an RCA predicting "→ 0 re-renders" for a specific cascade is
not refuted by a non-zero WDYR total. Say which quantity you measured, and don't let a global
counter stand in for a scoped claim.

Global application does not imply a large effect: 1244 auto-memoized call sites moved one
interaction's re-render count under 5%. Reach for a flow the change plausibly dominates, and
treat a single flow as a lower bound on reach, not a summary of it.

## Caveats to publish with the number

Fixture parity (structurally matched vs byte-identical), arm ordering (randomized or not),
what window the counter covers, and how many flows were measured. State them; they are cheap
and their absence is what makes a number unfalsifiable.

## Related

- `evidence` — packages this skill's output as its [React render & selector proof category](https://github.com/MetaMask/skills/blob/main/domains/pr-workflow/skills/evidence/references/evidence-catalog.md).
- `memory-leak`, `supply-chain-audit` — sibling engines behind other categories.
