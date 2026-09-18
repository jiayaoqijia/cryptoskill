---
name: avoid-any
description: >-
  Handle `any` correctly — it is not a type but a directive that disables type
  checking. Substitute by position (assignee → `unknown`, assigned → `never`).
  Two narrow exceptions: a generic constraint, and a callback parameter caught
  in a bivariant position between two fixed, irresolvable function-type
  constraints — both declared with an inline eslint-disable. Also covers the
  `any` that is never written down: a precise signature fed `any` at every call
  site, which no lint rule and no compiler check can report.
maturity: experimental
---

# Avoid `any`

Deepens the TypeScript guidance in `mms-coding-guidelines` — which already says "avoid `any`, prefer `unknown`" and links `MetaMask/contributor-docs` `docs/typescript.md`. This is the reasoning layer beneath that bullet: why `any` is dangerous, and how to replace it by position. Grounded in `docs/typescript.md` (§ Avoid `any`).

## `any` is not a type — it is a directive that disables type checking

The mental model matters more than the ESLint rule, because `@typescript-eslint/no-explicit-any` (already `error` in extension CI) does not stop the reasoning that reaches for `any`:

- **`any` is not "the widest type" — that is `unknown`.** `any` is a compiler directive that _disables_ type checking for the value it annotates.
- **It suppresses every error about its assignee** — the equivalent of `@ts-ignore` on every use of that variable. The errors still affect the code; `any` only makes them invisible.
- **It subsumes what it touches.** Any type in a union, intersection, or property relationship with `any` becomes `any` — an unmitigated loss of type information.
- **It infects downstream code.** One `any` at a source (e.g. a library type that resolves to `any`) propagates silently through every consumer, converting compile-time errors into **silent runtime failures** — defeating the point of a statically-typed language.

## Substitute `any` by position — assignee vs assigned

Identify which side of an assignment the `any` sits on:

- **Assignee** (a variable, parameter, or return that _receives_ a value — "it could be anything"): **try `unknown` first**, then narrow. `unknown` is the true universal supertype: everything is assignable to it, but it forces a type guard before use. `any` ↔ `unknown` are interchangeable in this position, so it is almost always a safe swap.
  - 🚫 `type Fn = () => any; const xs: any[]`
  - ✅ `type Fn = () => unknown; const xs: unknown[]`
- **Assigned** (a value that _flows into_ a slot): **try `never` first**, then widen to a subtype of the assignee's type. `unknown` cannot substitute here (it is only assignable to `unknown`); `never` is the bottom type, assignable to everything.

## Acceptable exception 1 — generic *constraints*

`any` is acceptable in a generic **constraint**, and only there. It bounds a type parameter without being assigned to a value, so it neither pollutes nor infects.

```typescript
class BaseController<
  ControllerName extends string,
  ControllerState extends StateConstraint,
  ControllerMessenger extends Messenger<
    ControllerName,
    ActionConstraint,
    EventConstraint,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    any
  >,
> // ...
```

Three conditions attach:

- **Declare it explicitly.** `no-explicit-any` is `error`, so a constraint `any` needs an inline `// eslint-disable-next-line @typescript-eslint/no-explicit-any` at the site — a deliberate, visible exception.
- **Constraints only — never a generic _argument_.** Passing `any` as an argument (`ControllerMessenger<any, any>`) is 🚫 — that assigns `any` and infects. Constraint-vs-argument is the whole distinction.
- **Prefer a narrower constraint anyway.** Reach for `any` here only when the narrower bound is genuinely unavailable.

## Acceptable exception 2 — a callback parameter between two irresolvable function-type constraints

A callback's parameter may be `any` when all three hold:

1. **Bivariant position** — the callback is _assignable to_ a wider function type **and** an _assignee of_ a narrower one.
2. **Irresolvable** — no concrete type satisfies both directions, because the wider function type is not a supertype of the narrower (`WideParam extends T extends NarrowParam` has no solution).
3. **Fixed** — neither constraint can be redesigned without breaking callers or losing accuracy.

Under `--strictFunctionTypes` parameters are contravariant, so the callback's parameter must be a _supertype_ of the outer slot's (outward: `unknown` ✓, `never` ✗) **and** a _subtype_ of the incoming value's (inward: `never` ✓, `unknown` ✗). `any` is the only inhabitant of both the top and bottom of the assignability lattice, so it is the only escape. (Return types stay covariant — keep `unknown`.)

🚫 If the constraints are **redesignable**, the contravariance error is a real design smell — fix it (usually by parametrizing with a generic), don't suppress:

```typescript
declare const acceptGeneric: <E>(handler: (event: E) => void) => void;
acceptGeneric(onA); // no `any` needed
```

✅ Only when the constraints are **fixed and irresolvable**:

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- Bivariant position with irresolvable, fixed constraints
let bridge: (x: any) => void;
```

Like the generic-constraint case, this `any` is **not infectious** — it is scoped to one parameter position, and both constraint types re-impose their signatures at each use site. Annotate the `eslint-disable` with the criteria so a reviewer can check them. Caveat: the safety claim holds only if the constraint types are accurate — a fixed constraint that is itself imprecise (a library type that is `any` internally) still forces the bridge `any` but no longer preserves safety at the use sites.

Canonical instance: a messenger `registerActionHandler` slot typed `(...args: any[]) => any` — strongly-typed handlers flow inward at registration, strongly-typed argument tuples outward at dispatch; `unknown[]` fails registration, `never[]` fails dispatch. It encodes rank-N polymorphism (`∀α. (α) => R`) that TypeScript cannot express directly.

When `any` still seems unavoidable, prefer the narrower, greppable escape hatches: `as unknown as` as a documented last resort, or `@ts-expect-error` with a comment saying why (a TODO where a fix is planned), never `@ts-ignore`. An unneeded `@ts-expect-error` fails `tsc` with `Unused '@ts-expect-error' directive` while an unneeded `@ts-ignore` stays silent, and `@typescript-eslint/ban-ts-comment` bans `@ts-ignore` and requires a description on `@ts-expect-error`. To replace a member, assert the replacement instead of erasing the target: `target.method = stub as typeof target.method`, not `(target as any).method = stub`, so `tsc` still rejects a stub whose type does not overlap the original's. Never reach for `any` to unblock feature work "to fix later."

## Declared `any` beats absorbed `any` — and only one of them is countable

The two exceptions above are both *declared*: the `any` is written down, an inline disable sits next to it, and a reviewer can find it with `grep`. The dangerous case is the one where **no `any` appears anywhere** and the value is `any` regardless:

- 🚫 **Absorbed.** A precise annotation on a parameter or return that receives `any` at every call site — `hexValueIsEmpty(value: string | null | undefined)` fed ethers dynamic-method results. `no-explicit-any` never fires, because no `any` was written. `tsc` never fires, because `any` satisfies every annotation. The file reads as checked and none of it is.
- ✅ **Declared.** `): Promise<any>` with an inline disable and a linked issue, as `shared/lib/token-util.ts` does for the same ethers API. Nothing is safer at runtime, but the claim is now honest, greppable, and countable by CI.

The absorbed form is strictly worse than the declared one, and it is what a JS→TS conversion produces by default: the writer annotates what the value *ought* to be, and `any` accepts the annotation without comment.

**A conversion is where the boundary's type is chosen, so an absorbed `any` is a decision, not an inheritance.** With `checkJs` off the predecessor asserted nothing; the precise signature is new. "The `any` is pre-existing" is true of the library and false of the annotation next to it.

Detect it with `IsAny<T>` at the call sites rather than by reading the signature — the probe, its controls, and the `declare module` composition that turns an `any` into a confident `string` are in the `tsc-blindspots` skill. The fix is to type or validate the value where it enters, so the precise annotations downstream are earned.
