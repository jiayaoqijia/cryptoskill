---
name: derive-types
description: Derive types from authoritative sources (indexed access, `typeof`, `ReturnType`/`Parameters`, `Pick`/`Omit`, `Infer<typeof struct>`) instead of hand-writing ad-hoc types that duplicate, run too wide or too narrow, and drift.
maturity: experimental
---

# Derive Types From Authoritative Sources

Deepens the TypeScript guidance in `mms-coding-guidelines`, and is the structural counterpart to the contributor-docs rule *Prefer type inference over annotations and assertions* (`MetaMask/contributor-docs` `docs/typescript.md`). Where inference handles values, derivation handles types that reference other types.

## Derive, don't re-declare

When a type already exists at an authoritative source — a controller's state type, a function's return, a library's exported type, a schema/struct — **derive from it** rather than restating it. Derive with indexed access (`State['field']`), `typeof`, `ReturnType` / `Parameters` / `Awaited`, utility types (`Pick` / `Omit` / `Partial`), and `Infer<typeof struct>`; let inference carry the rest. Inference covers an omitted return annotation, `as const` on a literal, and `satisfies` where a `:` annotation would widen the inferred type. How narrow the result should be, including literal lookup tables and built keys, is `avoid-widening`. Inferred and derived types stay "responsive to changes in code," while hand-written declarations "rely on hard-coding, making them brittle against code drift."

Over a union, `Pick` and `Omit` work on `keyof` the whole union, which is only the keys every member shares, so `Omit<A | B, 'k'>` loses each member's own keys. Branch first with a distributive conditional type: `T extends unknown ? Omit<T, K> : never` applies `Omit` to each member.

An ad-hoc type — one hand-defined to describe a value an authoritative type already describes — carries three dangers:

- **Duplication.** The same shape is stated twice; every reader reconciles them and every change touches both.
- **Incorrect in either direction.** A hand-written type is a _guess_ at the source's shape, and the guess can miss either way. Too wide, it admits values the authoritative type would reject, so invalid data still type-checks. Too narrow, it drops a case the source allows, such as a `| undefined`, and erases the compiler's record of why a runtime guard exists (see the five divergence shapes in `tsc-blindspots`).
- **Drift.** The source evolves; the copy does not. Because it is hand-written rather than derived, the compiler cannot flag the divergence — the bug surfaces at runtime, not at build.

## A grounded example (`metamask-extension` #42583)

A `wallet-services` module hand-rolled a messenger type, re-declaring each controller action's signature and **hand-copying its return shape** inline.

🚫 Reinvents the controller's messenger and re-states its action returns:

```typescript
type TokenResolutionMessenger = {
  call(
    action: 'AssetsContractController:getTokenStandardAndDetails',
    address: string,
    // …
  ): Promise<
    | {
        balance?: string | number | bigint | { toString(radix?: number): string };
        decimals?: string | number | bigint | { toString(radix?: number): string };
        standard?: string;
        symbol?: string;
      }
    | undefined
  >;
  // the other action's return is discarded entirely:
  call(action: 'AssetsContractController:getBalancesInSingleCall' /* … */): Promise<unknown>;
};
```

✅ Derive each return from the controller's exported action type; don't hand-copy it:

```typescript
import type { AssetsContractControllerGetTokenStandardAndDetailsAction } from '@metamask/assets-controllers';

// the action already types its own return — derive it
type TokenDetails = ReturnType<
  AssetsContractControllerGetTokenStandardAndDetailsAction['handler']
>;
```

The messenger itself should be a `Messenger` from `@metamask/messenger` parameterized with those exported action types, so every `call` signature comes from the controller rather than a hand-rolled overload. The hand-rolled version is worse than a plain duplicate: one return is hand-copied (already looser than the controller's real type), the other (`Promise<unknown>`) discards the type entirely.

The same PR also typed a dependency `getMetaMaskState: () => Record<string, unknown>`, which forced every consumer to re-cast the shape by hand — including a `{ metamask: getMetaMaskState() } as never` double-cast. That downstream cast tax is what a too-wide type always imposes; deriving the dependency from the authoritative state type deletes it. Notably the same file _did_ derive one type correctly (`type Action = (typeof ACTIONS)[number]`), so the pattern was already in hand — the discipline is extending it to every referenced type.

## Rule

Before writing a type, ask where the value comes from and whether that source already types it. If it does, derive. Define a fresh type only when no authoritative source exists — a genuinely new shape at a boundary you own. Before defining, exhaust deriving: search the internal `@metamask/*` packages and the consuming repo for the authoritative source first.
