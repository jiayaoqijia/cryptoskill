---
maturity: experimental
name: effect-antipattern-scan
description: Review PR diffs that add or modify `useEffect` for the systemic React effect antipatterns
---

# Effect Anti-Pattern Review

**Scope:** Pre-merge review of PRs that add or modify `useEffect` calls. The workflow is a grep-driven checklist against the patterns catalogued in the **`effect-antipatterns`** knowledge file, which is the single source for their definitions and fixes (installed alongside this skill under `knowledge/`).

Applies to both `metamask-extension` and `metamask-mobile`. See overlays for repo-specific paths.

## When To Use

- Reviewing a PR that adds or modifies a `useEffect` call
- Reviewing a PR that adds `setInterval`, `setTimeout`, `fetch`, or `addEventListener` inside a component
- Investigating a "Can't perform a React state update on an unmounted component" warning

## Do Not Use When

- Reviewing selector or render-cascade issues (use [`selector-antipattern-scan`](../selector-antipattern-scan/skill.md))
- Reviewing non-React code (background scripts, workers, test utilities)
- Reviewing an effect that is intentionally one-shot with no async work or timers (check patterns below anyway, but most do not apply)

## Workflow

1. **List changed files with `useEffect`.** `git diff --name-only origin/main...HEAD | xargs grep -l 'useEffect'`
2. **Run the [grep checklist](#grep-checklist)** against the changed files.
3. **For each hit, map to a pattern** in `effect-antipatterns` and apply the fix from the knowledge file.
4. **Block on unstable dependency identity**, unless it is a `JSON.stringify` on a cold path with a small object. Do not merge otherwise.
5. **Block on a timer without cleanup.** Any `setInterval` / `setTimeout` without a matching `clearInterval` / `clearTimeout` in the cleanup function is blocking.
6. **Require cancellation for async effects.** Any `fetch` / network call inside `useEffect` must guard against a stale response, with a cancelled flag or `AbortController`.

## Grep Checklist

| Pattern (`effect-antipatterns` §) | Detection |
|---|---|
| §1 Unstable dependency identity | `grep -rnE 'useEffect.*\[.*JSON\.stringify' <source-dir>`, plus inline `{`/`[` literals in the dep position |
| §2 Wrong dependencies | Hand review — empty deps that read state (stale closure), deps that read nothing, or an effect dependency the effect never reads |
| §3 Derived state via effect + setState | Hand review — `useEffect` that calls `setX` from other state/props; §3a for chains of them |
| §4 Missing timer cleanup | `grep -rnE 'setInterval\|setTimeout' <source-dir>` then check each effect returns a cleanup |
| §5 Uncancelled async work | `grep -rnB2 -A10 'fetch\(' <source-dir>` within `useEffect` blocks |

See the repo overlay for the concrete `<source-dir>` path.

## Common Pitfalls

| Mistake | Correct approach |
|---|---|
| Accept `JSON.stringify` in deps because "the effect needs to rerun when X changes" | Destructure to primitives or `useMemo` the object on a hot path. A cold path with a small object can stringify |
| Accept a state-mirror effect because "the computation is expensive" | Use `useMemo` for expensive derivations. Effects are for side effects, not state derivation |
| Let `setInterval` ship without cleanup because "the component rarely unmounts" | Cleanup is non-negotiable — unmount frequency doesn't matter, correctness does |
| Treat "can't perform state update on unmounted component" as a cosmetic warning | It is a data race. An old response can overwrite a new one |
| Add a lint rule disable on `react-hooks/exhaustive-deps` | Almost always wrong. Destructure or memoize instead |
| Refactor toward `useEffect` + `setState` because it "feels like state" | You probably do not need an effect. See [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) |
