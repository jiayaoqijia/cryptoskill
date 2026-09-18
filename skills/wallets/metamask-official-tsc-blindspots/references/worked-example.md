# Worked example — a JS→TS migration PR

[metamask-extension#44397](https://github.com/MetaMask/metamask-extension/pull/44397),
head `7fafda0`. 11 files converted, +153/−72, described as *"mostly mechanical
JS→TS with equivalent runtime logic"*, four files *"rename only"*. All CI green,
including `lint:tsc`.

Twelve hand-written types. Nine had an authoritative source. Five disagreed with it.

## Arm A

```
$ NODE_OPTIONS='--max-old-space-size=9216' npx tsc -p tsconfig.json --noEmit
$ echo $?
0
```

Silent — so every diagnostic below is attributable to the substitution.

## Arm B

Six probe files, each substituting the derived type and calling it as the real
code does:

```
probe-1-get-obj-structure.ts(19,47): error TS2345: Argument of type
  'MetaMaskStorageStructure | undefined' is not assignable to parameter of type
  'Record<string, unknown>'.
probe-2-set-current-popup-id.ts(22,21): error TS2345: Argument of type 'undefined'
  is not assignable to parameter of type 'number'.
probe-2-set-current-popup-id.ts(29,21): error TS2345: Argument of type
  'number | undefined' is not assignable to parameter of type 'number'.
probe-3-ens-provider.ts(27,32): error TS18048: 'provider' is possibly 'undefined'.
probe-3-ens-provider.ts(44,14): error TS2322: Type
  'SwappableProxy<ProxyWithAccessibleTarget<Provider>> | undefined' is not
  assignable to type 'HandWrittenEthProvider'.
probe-4-offscreen-message.ts(43,14): error TS2322: Types of property 'target' are
  incompatible. Type 'string' is not assignable to type 'OffscreenCommunicationTarget'.
probe-6-chain-id-widening.ts(31,50): error TS2322: Type '"1"' is not assignable to
  type '`0x${string}`'.
```

A seventh probe compiled the PR's *original* string literals with **zero** errors —
which is how the two unnecessary runtime changes below were established.

## Findings

| Hand-written | Authoritative source | Shape |
|---|---|---|
| `_setCurrentPopupId: ((id: number \| undefined) => void)` | `AppStateController['setCurrentPopupId']` → `(id: number) => void` | widening |
| `getCurrentChainId: () => string` | `ReturnType<typeof getCurrentChainId>` → `` `0x${string}` `` | widening |
| `target: string` on a received message | the sender, TypeScript in-repo → `OffscreenCommunicationTarget` | widening |
| `EthProvider` (written twice, unshared) | `ReturnType<NetworkController['getProviderAndBlockTracker']>['provider']` | duplication + dropped nullability |
| `obj: Record<string, unknown>` | already in a JSDoc `@type` on the argument at the call site: `MetaMaskStorageStructure \| undefined` | placeholder + dropped nullability |

Two of these had a consequence beyond tidiness:

- The widened setter is what let `setter?.(undefined)` compile. Deriving it fails —
  usefully, because it surfaces a genuine mismatch between a controller method's
  declared parameter and how its callers actually use it.
- The dropped nullability sat in the same edit that deleted a `= {}` default
  parameter, i.e. the guard that existed *for* the nullable case. (Traced: inert
  today, because a fallback upstream guarantees an object by the time the path runs.)

**Separately**, reading `@types/chrome` before trusting a type error found two
runtime changes the types never required: `contextTypes` and `reasons` are declared
as template-literal **string** types (`` `${ContextType}`[] ``, `` `${Reason}`[] ``),
so the original `['OFFSCREEN_DOCUMENT']` / `['IFRAME_SCRIPTING']` already compiled.
The PR replaced both with runtime enum lookups, and added a redundant cast.

## Clearances — and one that mattered

Five claims the probes **cleared**:

- `Promise<string>` as a provider `request` return looked unsound. It isn't: the
  real `request<Params, Result extends Json>` is generic in its result, so a call
  site may legitimately fix `Result = string`.
- Two `declare module` blocks: neither package ships types, and no `@types/*` is
  installed → no authoritative source exists, so hand-writing is correct.
- A hand-declared `clients?: { matchAll }`: the authoritative `Clients` lives in
  `lib.webworker.d.ts`, which is not in this repo's `tsconfig.lib` → out of scope.
- Two dependency callbacks (`() => string`, `() => boolean`) matched their sources
  exactly.
- A dropped argument (`_getPopup(id)` → `_getPopup()`) was a genuine no-op: the
  base function declared no parameters, so the argument was already discarded.

**The provider clearance is the reason Step 5 exists.** The first Arm B run
reported `TS18048: 'provider' is possibly 'undefined'` on that probe — an error on
the line the return-type claim lived on, which reads as confirmation if you count
exit codes. The nullability error fired one property *ahead* of the claim. Setting
it aside with `NonNullable<…>` and re-running showed the return type compiles
clean. Reported as a finding, it would have been wrong.
