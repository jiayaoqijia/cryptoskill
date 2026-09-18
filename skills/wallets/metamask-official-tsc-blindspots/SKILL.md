---
name: tsc-blindspots
description: >-
  Find the type defects `tsc` is structurally unable to report — a green build is
  not evidence the types are correct. Covers the two classes: (1) hand-written
  types that restate an authoritative source and disagree with it, caught by
  substituting the derived type at a fixed commit and diffing `tsc` output; and
  (2) the standing blind spots in the language and config — unchecked array/record
  indexing, bivariant method parameters, covariant arrays, `any` absorption at
  untyped boundaries, precise signatures fed `any` at every call site, ambient
  `declare module` assertions that launder an `any` into a confident type,
  excess-property checks that only fire on fresh literals, and external data
  asserted rather than validated. Also audits typing edits that quietly change
  runtime behavior:
  stripped `| undefined`, deleted default parameters, literals swapped for runtime
  enum lookups, calls made optional so a throw becomes a silent no-op. Use when
  reviewing a JS→TS migration, a PR that hand-writes types for values that already
  have them, a "rename-only" refactor, or any PR claiming a change is mechanical.
  Triggers on /mms-tsc-blindspots, or on phrases like "validate this TypeScript
  migration", "is this type right", "does this type match the real shape",
  "why didn't CI catch this type", "derive vs define", and "what can tsc not
  check".
maturity: experimental
---

# TypeScript compiler blind spots

A hand-written type is a **claim about a value's shape**, and it compiles whether
or not the claim is true. `tsc` checks declarations for internal **consistency** —
never for **correspondence** to the source they restate. Across a JavaScript
boundary (`checkJs` off) it checks nothing at all.

Those are the blind spots. This skill finds what is hiding in them.

Two classes, two methods:

| Class | What it is | Method |
|---|---|---|
| **Restated types** | A type hand-written to describe a value that already has an authoritative type | **Substitution A/B** — swap in the derived type, diff `tsc` output |
| **Standing blind spots** | Defects the language and config cannot report at all, in any codebase | **Targeted audit** — [references/false-negatives.md](references/false-negatives.md) |

The second class is the one that surprises people: a file of genuinely broken
code can typecheck clean. The reference includes exactly that — a demonstration
file where every block is wrong and `tsc` reports zero errors.

Companion to the authoring rule it enforces — *derive types from authoritative
sources instead of re-declaring them* in
[contributor-docs `docs/typescript.md`](https://github.com/MetaMask/contributor-docs/blob/main/docs/typescript.md).
This skill is the review-side proof; that document is the write-side guidance.

## When to use

- A **JS→TS migration** PR, or one whose body says *mechanical*, *rename-only*, or *no behavior change*.
- A PR that **hand-writes a type for a value that already has one** — a controller method's parameters, a selector's return, a message payload, a package's exported shape.
- A reviewer asks "is this type actually right?" and the answer so far is "it compiles."

Out of scope: code correctness (use a normal review), runtime behavior (use e2e /
visual proof), and lint/format (CI owns those).

## Prerequisites

- The repo checked out at the PR head, dependencies installed, `tsc` runnable.
- Enough heap for a full typecheck on large repos (see Troubleshooting).
- A scratch directory inside the `tsconfig` `include` paths for probe files.

## The core idea: two arms, one commit

Both arms sit at the **same commit**. They differ by a *substitution*, not by a
ref — so there is no build, no rebase, and no merge boundary to confound.

| | What it is | What it must show |
|---|---|---|
| **Arm A** | The PR exactly as written | **Silent.** Zero diagnostics |
| **Arm B** | Same tree + probes that use the *derived* type, exercised as the real code exercises it | Each new diagnostic = a disagreement the hand-written type concealed |

**Arm A must be silent or the run is inconclusive.** If the untouched tree
already emits diagnostics, nothing in Arm B is attributable to the substitution —
"N errors in Arm B" is then a count, not a finding. Publish Arm A's result
verbatim as the delivery check.

## Instructions

### Step 1: Inventory every type the PR hand-wrote

```bash
gh pr diff <pr> | grep -nE '^\+.*(type [A-Z]|interface [A-Z]|: (Record<|string|number|boolean|unknown|any)\b)'
```

List them. Each one is a claim you are about to test.

**First, check each converted module is still referenced:**

```bash
grep -rn "moduleName" --include=*.ts --include=*.js . | grep -v node_modules | grep -v '\.test\.'
```

If the only hits are the module's own definition and its test, the file is dead —
every type on it is unfalsifiable, because nothing constrains it and no divergence
can ever surface. This is the highest value-per-second check in a migration, and
it reorders the work: a dead module's conversion is a deletion candidate, not a
typing exercise.

### Step 2: Find the authoritative source for each

Work down this list — the first hit wins. In the worked example 9 of the 12
hand-written types had a source, each found in under a minute:

1. **The call site.** What is actually passed? In a JS caller, check for a JSDoc
   `@type {import('…').Foo}` annotation on the variable — the answer is sometimes
   literally already written down there.
2. **The class or method being wrapped** → `MyController['someMethod']`.
3. **A package already imported in the same file** — e.g. `webextension-polyfill`
   defines every listener payload; if the file calls the API, the type is in reach.
4. **The sender**, for a message or event payload. If the sender is TypeScript, the
   shape is derivable, not guessable.
5. **A selector's return** → `ReturnType<typeof mySelector>`.
6. **`@types/*` for a platform API.** Read the actual declaration before "fixing"
   a type error — many are template-literal *string* types (`` `${SomeEnum}`[] ``),
   which already accept a plain string literal.
7. **No source exists** — an untyped dependency, a lib absent from `tsconfig.lib`,
   a genuinely new boundary the repo owns. Hand-writing is then **correct**. Record
   it as a cleared falsifier with the reason; do not report it as a finding.

### Step 3: Write one probe per claim

One file per claim, in a scratch dir inside the `include` paths. Each probe names
its authoritative source in a header comment and calls the derived type **the way
the real call site calls it**:

```ts
// PROBE — src/thing.ts hand-wrote `setFoo: (id: number | undefined) => void`.
// Authoritative: FooController['setFoo'] (foo-controller.ts:120) — param is `number`.
// The real code calls it as below.
import type { FooController } from '../controllers/foo-controller';

declare const setFoo: FooController['setFoo'];

export function asCalledByTheRealCode() {
  setFoo(undefined); // thing.ts:105
}
```

### Step 4: Run both arms

```bash
./scripts/substitution-ab.sh <repo-path> <probe-dir>
```

Or by hand — Arm A first, and stop if it is not silent.

### Step 5: Isolate diagnostics that fire for the wrong reason

A checker reports the *first* failure it reaches, so an unrelated earlier cause
can short-circuit the claim under test — and an exit-code read scores that as a
confirmation. **Assert on the specific diagnostic** (code + message + line), and
where an earlier cause intervenes, neutralise it and re-probe:

```ts
const defined = value as NonNullable<Derived>; // set nullability aside
// …now the return-type claim is the only thing left to fail
```

This is not hypothetical — see the worked example, where a claim that a return
type was unsound turned out **sound** once the nullability error ahead of it was
isolated.

### Step 6: Report findings *and* clearances

Give each claim a verdict, and say which ones the probes **cleared**. A
substitution sweep that only ever confirms is indistinguishable from one that
never isolated anything.

### Severity: "pre-existing" is about the upstream `any`, not about the annotation

A conversion PR invites two reflexes that both understate a false-precision
finding, and the underlying `any` is what makes each of them sound reasonable:

- **"It's pre-existing."** Split the claim. The library's `any` is genuinely
  inherited — ethers has returned `any` from dynamic contract methods since long
  before this diff. The *annotation beside it* was written here: check `git log
  --diff-filter=A -- <path>` and, for a `declare module`, whether the block itself
  is added by this PR. If the file is new, nothing in it is pre-existing, because
  with `checkJs` off the predecessor asserted nothing at all. A conversion is the
  moment the boundary's type is **chosen**.
- **"It's a nit."** A nit is a finding that is minor *in itself*. A value crossing
  a boundary unchecked, under a signature that says it was checked, is a type-safety
  defect — the class this whole skill exists to surface. Scope and severity are
  separate axes: a substantive finding a PR need not fix is still substantive, and
  saying so costs one sentence.

The remedy follows from which one it is. Annotating the hole and filing a TODO is
right for the inherited `any`; it is not a fix for false precision, because the
misleading signature stays exactly as it was. Type or validate the value where it
enters, so the precise annotations downstream are earned.

## The five divergence shapes

Five shapes to check for. Treat the list as a starting checklist, not a partition —
the first four each account for at least one divergence in the worked example, and
the fifth was found on a later pass over the same PR:

1. **Widening** — `string` for a `Hex`/template-literal type, `string` for an enum,
   `number | undefined` for `number`. Admits values the real type rejects; worst
   when a guard downstream depends on the narrower form. A union ending in
   `string & Record<never, never>` reads as a narrowing and is not one: its last
   member accepts every string, typos included.
2. **Dropped nullability** — the source says `| undefined`, the hand-written type
   doesn't. Erases the compiler's record of why a runtime guard exists.
3. **Duplication** — the same shape written out in two files, unshared. Both copies
   now need every future change.
4. **Placeholder** — `Record<string, unknown>`, `any`, or `unknown` standing in for
   a shape that is known. Pushes a cast to every use site. A circular import does
   not justify one: `import type` the real type, which is erased from the emitted
   JavaScript and adds no runtime edge to the module graph.
5. **False precision** — the inverse of a placeholder: the annotation is *narrower*
   than what actually arrives. `hexValueIsEmpty(value: string | null | undefined)`
   on a parameter fed `any` at every call site. `tsc` cannot report it, because
   `any` satisfies every annotation, and `no-explicit-any` cannot either, because
   no `any` was written. The narrower the type, the more confident the file reads
   and the less any of it is checked. Find it with `IsAny` at the call sites, not
   by reading the signature — see
   [references/false-negatives.md](references/false-negatives.md) §7.

## Escape hatches are the tell

When a diff adds a hand-written type *and* an `as`, a `!`, a new `?.`, or an
`eslint-disable` in the same region, check whether the escape hatch exists to service
the type rather than the runtime. Count them — a cluster marks where to probe first.
Ask of each suppression what would fire on that exact line without it. `tsc` reports
an unused `@ts-expect-error` (TS2578) but not an unused `@ts-ignore`, and whether an
unused `eslint-disable` is reported depends on the repo's `reportUnusedDisableDirectives`
setting (`'error'` in extension and core, unset in mobile).

## A typing change should not change runtime behavior

The second axis, and the one whose defects reach runtime rather than staying in
the type layer. A migration PR is
allowed to add annotations; it is not allowed to change what the program *does*.
Four patterns to grep the diff for, all of which look like typing work:

1. **A literal replaced by a runtime lookup.** `['IFRAME_SCRIPTING']` becoming
   `[SomeApi.Reason.IFRAME_SCRIPTING]` adds a dependency on that object existing at
   runtime. **Read the declaration first** — if the parameter is a template-literal
   string type (`` `${SomeEnum}`[] ``), the literal already type-checked and the
   swap bought nothing.
2. **A default parameter or fallback deleted.** `function f(x = {})` → `function f(x: T)`
   removes a guard. Ask what the guard was *for*: a `| undefined` the new type just
   dropped is the first candidate. Then check reachability rather than assuming either way.
3. **A call made optional.** `obj.method()` → `obj.method?.()`, added to satisfy a
   hand-written `| undefined`, converts a **throw into a silent no-op**. The loud
   failure was load-bearing; now the same state produces no signal at all.
4. **A widened local to keep a check alive.** `let name: string | undefined` on a
   value the authoritative type calls `string`, so that an `=== undefined` branch
   still compiles. If the runtime check is genuinely needed, the *input* type is
   wrong — fix that instead of widening downstream.

For each hit: state whether it is reachable, and say so plainly either way. "I
traced it and it is inert today" is a useful review finding. "This might be a bug"
is not.

### Silent failure modes deserve their own pass

Ask where a newly-introduced failure would *surface*. A change inside a
`try { … } catch { captureException(e); return; }` degrades a feature without
crashing — nothing goes red, no test fails, and the only signal is an error-tracker
entry nobody is watching. The same edit in a hot path would be caught in minutes.
Weight findings by observability, not just by likelihood: **an unlikely failure in a
swallowed path can outrank a likely one in a loud path.**

## Why the build stays green regardless

- The hand-written type **compiles by construction** — that is why it was written.
- With `checkJs` off, a type written for a function whose callers are still `.js`
  is checked against **nothing** and can drift indefinitely.
- A value that arrives as `any` silently satisfies any annotation.

So cite the green build as the *premise* of the finding, never as counter-evidence.

## Examples

**Worked example** — 12 hand-written types across a JS→TS migration PR, 5 confirmed
divergences and 5 cleared falsifiers, with the verbatim two-arm output:
[references/worked-example.md](references/worked-example.md).

**Repo notes** for MetaMask Extension (heap, probe location, `checkJs` status):
[references/metamask-extension.md](references/metamask-extension.md).

```
User: "Validate this TS migration PR — is it really mechanical?"
Agent: inventories the 12 new types → finds the authoritative source for 9 →
       writes 6 probes → Arm A silent, Arm B reports 6 diagnostics → isolates
       one that fired for the wrong reason → reports 5 findings, 5 clearances.
```

## Troubleshooting

### Arm A is not silent

**Problem:** the untouched tree already emits diagnostics, so Arm B is unattributable.
**Fix:** pin the toolchain, install against the PR's own lockfile, raise the heap, or
narrow the project. If it cannot be made silent, the lane is **inconclusive** — say
so; do not report Arm B's count as findings.

### `tsc` runs out of memory

**Problem:** `FATAL ERROR: Ineffective mark-compacts near heap limit`.
**Fix:** raise the heap — `NODE_OPTIONS='--max-old-space-size=9216'`. Note the OOM
exits non-zero *without* type diagnostics, so a naive exit-code check reads it as
"errors found." Always look at the output, not just the status.

### A probe errors, but not for the claimed reason

**Problem:** the diagnostic is about an earlier property, not the claim.
**Fix:** neutralise the earlier cause (`NonNullable<…>`, a narrow assertion) and
re-run. If the claim then compiles clean, the claim was **wrong** — report it as cleared.

### There is no authoritative source

Not a failure. Hand-writing is correct where nothing defines the shape; record the
reason (package ships no types, lib not in `tsconfig.lib`, new boundary) so the next
reviewer doesn't re-litigate it.

## Related

- [contributor-docs `docs/typescript.md`](https://github.com/MetaMask/contributor-docs/blob/main/docs/typescript.md) — the write-side rule this proves.
- `unit-testing`, `integration-test` — for behavior claims; this skill proves *types*.
