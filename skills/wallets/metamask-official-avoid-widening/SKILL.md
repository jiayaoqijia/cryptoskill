---
name: avoid-widening
description: >-
  Keep a type as narrow as the value it describes. An annotation wider than
  what inference already knows throws information away, so annotate only to
  add information. Keep immutable lookup tables literal with `as const
  satisfies`, type built keys with template literal types and build them
  `as const`, and widen on purpose only at a boundary where inference is
  unsound.
maturity: experimental
---

# Avoid Widening

Deepens `MetaMask/contributor-docs` [`docs/typescript.md`](https://github.com/MetaMask/contributor-docs/blob/0c297e8a01be7482cc3ff0d047e5e51069adc442/docs/typescript.md#L40-L42), *Avoid unintentionally widening an inferred type with a type annotation*: "Enforcing a wider type defeats the purpose of adding an explicit type declaration, as it _loses_ type information instead of adding it." `derive-types` covers where a type should come from. This skill covers how wide it should be, and `avoid-any` covers the annotation that turns checking off.

## When To Use

- Writing or reviewing a type annotation, a `satisfies` clause or an `as const`.
- A lookup table maps one set of names to another, such as trace names or action types.
- A collection is keyed by strings built from known parts, such as `` `${name}:${id}` ``.
- Proposing a type change in review, where a widening suggestion reads as a tightening.

## Annotate to add information, never to repeat or lose it

Compare the annotation with the type inference already produces. Equal adds nothing, and wider loses information. Only a narrower annotation, or a deliberate widening at a boundary (below), is worth writing.

| declaration | resulting type |
|---|---|
| `const name = 'foo'` | `"foo"` |
| `const name: string = 'foo'` | `string`, widened |
| `const ids = [1, 2] as const` | `readonly [1, 2]` |
| `const ids: number[] = [1, 2]` | `number[]`, widened |

To check a value against a type without widening it, use `satisfies` ([`docs/typescript.md` L134-L136](https://github.com/MetaMask/contributor-docs/blob/0c297e8a01be7482cc3ff0d047e5e51069adc442/docs/typescript.md#L134-L136)). The exception is a mutable object, array or class that code adds to later. There the narrowest type excludes the additions, so annotate with `:` unless the value is meant to be immutable ([L201-L205](https://github.com/MetaMask/contributor-docs/blob/0c297e8a01be7482cc3ff0d047e5e51069adc442/docs/typescript.md#L201-L205)).

## Keep immutable lookup tables literal

```typescript
// 🚫 The annotation widens every value to `TraceName`, so `NAMES[name]` no longer says which member it is.
const NAMES: Record<FeatureTraceName, TraceName> = {
  'Feature Open': TraceName.FeatureOpen,
  'Feature Close': TraceName.FeatureClose,
};

// ✅ Checks every key and value, keeps each value's member type, and makes the table read-only.
const NAMES = {
  'Feature Open': TraceName.FeatureOpen,
  'Feature Close': TraceName.FeatureClose,
} as const satisfies Record<FeatureTraceName, TraceName>;
```

- A plain object literal with neither widens its values to `TraceName`.
- `satisfies` alone already keeps each value's member type when the checked type is a union of literals, as an enum is. What `as const` adds is `readonly`, plus literal types for nested arrays and objects. It also marks the table as immutable, which is the condition under which the extensible-type exception above does not apply.

## Type a built key by how it is built, and build it `as const`

```typescript
// ✅ The map accepts only keys of this shape, so a key built from the wrong name does not compile.
const pending = new Map<`${FeatureTraceName}:${string}`, PendingSpan>();

const key = `${params.name}:${params.id}` as const;
pending.get(key);
```

- A template literal expression infers as `string` unless it is marked `as const` or contextually typed. So narrowing a collection's key type fails with TS2345 at each `get`, `set` and `delete` that passes an unmarked key. Change the key type and every expression that builds a key together.
- Measured with TypeScript 5.6.3 on [metamask-extension#46123 (preload Perps markets on unlock)](https://github.com/MetaMask/metamask-extension/pull/46123) at [`0118bcc256`](https://github.com/MetaMask/metamask-extension/blob/0118bcc25610de7238243c47d8ba37924251e017/app/scripts/controllers/perps/infrastructure.ts#L274-L306). Narrowing only the span map's key type produced five TS2345 errors, and adding `as const` to its two key expressions cleared them.

## Widen on purpose only where inference is unsound, and only at a boundary

When a library's types claim more than its runtime guarantees, the correct annotation is wider. luxon types `plus(duration)` as returning `this`, so a valid `DateTime<true>` stays `DateTime<true>` after `plus()`, although the result is invalid past year 275760. Declaring the return as `DateTimeMaybeValid` restores the distinction the library erased.

That widening works only where the compiler has to use it:

| form | forces the check? |
|---|---|
| `const x: DateTimeMaybeValid = start.plus(d)` | no, because control-flow analysis re-narrows `x` to its initializer |
| `start.plus(d) satisfies DateTimeMaybeValid` | no, because it checks assignability and keeps the inferred type |
| `start.plus(d) as DateTimeMaybeValid` | yes |
| a parameter or return typed `DateTimeMaybeValid` | yes |

So the test is whether an annotation adds information inference lacks. Narrowing usually does. Widening does only where inference is wrong about the runtime.

## Workflow

1. Before writing `:`, hover or `tsc --noEmit` to see the inferred type, and write the annotation only if it is narrower, or a boundary widening of an unsound type.
2. For a table that code never adds to, use `as const satisfies <Constraint>`. For one that grows, annotate with `:`.
3. For a collection keyed by built strings, type the key as the template literal it is, and add `as const` to every expression that builds one. Typecheck before proposing the change, since the key type and the builders have to change together.
4. In review, run the proposed suggestion through `tsc` before posting it. A narrowing that leaves the builders unmarked fails the build.

## Related

- `derive-types` — take a type from its authoritative source instead of restating it.
- `avoid-any` — the annotation that disables checking.
- `tsc-blindspots` — divergence shapes the compiler cannot report, including a widened local.
