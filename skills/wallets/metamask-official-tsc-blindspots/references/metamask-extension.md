# Repo notes — metamask-extension

Specifics for running the two-arm proof in `MetaMask/metamask-extension`. The
split against `repos/metamask-extension.md` is by kind rather than by repo: which
blind spots bite this repo, and where they live, go in the overlay; run mechanics
— heap size, probe placement, timings — stay here.

## Typecheck invocation

```bash
NODE_OPTIONS='--max-old-space-size=9216' npx tsc -p tsconfig.json --noEmit
```

`package.json`'s `lint:tsc` uses `--max-old-space-size=6144`, and CI's `Test lint`
job ran it over the full project at that heap and exited 0 (`main` at
`0269fae48a`, 2026-09-14). A local full run can still **OOM**, and the OOM exits
non-zero with no type diagnostics, so a naive exit-code check reads it as "errors
found." If it does, raise the heap and read the output. A full run takes roughly
3–5 minutes.

## Where to put probes

Anywhere under the `include` list — `app`, `development`, `shared`, `test`,
`types`, `ui`. `app/scripts/derive-probe/` works. Delete it afterwards; it is
inside the build's include paths.

## What the compiler is *not* checking

- **`checkJs` is unset** and there is no `// @ts-check` in `app/scripts/background.js`.
  `background.js` is the sole caller of much of `app/scripts/lib/**`, so a type
  written for those functions is validated against **nothing**. This is where
  migration PRs accumulate silent divergence, and where this skill pays.
- `tsconfig.json` sets `lib: ["DOM", "es2023"]`, overriding the base. **`webworker`
  is absent**, so service-worker globals (`clients`, `Clients`, `Client`) have no
  authoritative type in scope — hand-declaring them is legitimate here.
- Strictness comes from `@tsconfig/node22` (`strict: true`), so `strictNullChecks`
  is on and nullability divergences do surface in a probe.

## Authoritative sources worth knowing

| Looking for | Derive from |
|---|---|
| current chain id | `ReturnType<typeof getCurrentChainId>` (`shared/lib/selectors/networks.ts`) → `Hex`, not `string` |
| the EIP-1193 provider | `ReturnType<NetworkController['getProviderAndBlockTracker']>['provider']` — note the `\| undefined` |
| a controller method's params | `SomeController['methodName']` |
| persisted state root | `MetaMaskStorageStructure` (`shared/lib/stores/base-store.ts`) |
| a `browser.*` listener payload | `browser.WebRequest.OnErrorOccurredDetailsType` and siblings, from `webextension-polyfill` |
| offscreen message targets/events | the enums in `shared/constants/offscreen-communication.ts` |

## Before "fixing" a `chrome.*` type error

Read the declaration in `node_modules/@types/chrome/index.d.ts` first. Several
parameters are template-literal **string** types, not the enums they mirror — e.g.
`ContextFilter.contextTypes?: ` `` `${ContextType}`[] `` and
`CreateParameters.reasons: ` `` `${Reason}`[] ``. A plain string literal already
satisfies them, so swapping in `chrome.offscreen.Reason.X` is an unnecessary
runtime change, not a type fix.
