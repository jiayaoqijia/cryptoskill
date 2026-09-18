---
repo: metamask-mobile
parent: derive-types
---

# Deriving in `metamask-mobile`

Read via the GitHub API against `MetaMask/metamask-mobile` `main` on 2026-08-31, not from a local
checkout. Every path, line number and count below was re-verified against `main` at that date;
confirm before quoting a line number in review, and never verify one against a working tree.

As in the extension, most authoritative types are upstream: `package.json` carries 132
`@metamask/*` dependencies at caret ranges. Mobile and the extension sit on **different versions of
the same packages**, so a shape copied by hand here diverges from the same shape copied by hand
there, and neither repo can see the other drift. Deriving is what keeps both pinned to whatever
`core` actually says.

## Where the authoritative source lives

`app/core/Engine/types.ts` is the hub. Two hand-maintained maps sit at the top, and everything else
in the file is derived from them:

- `MessengerClients` (line 854) — controller name to controller **class**, one row each.
- `EngineState` (line 979) — controller name to the upstream `*State` type, one row each.

The rows are written by hand; the values are imported, not restated. So the shapes are already
authoritative — what is hand-maintained is the *membership* of the maps.

Everything downstream derives:

| Derived type | Line | Form |
| --- | --- | --- |
| `MessengerClientName` | 1060 | `keyof MessengerClients` |
| `MessengerClient` | 1065 | `MessengerClients[MessengerClientName]` |
| `MessengerClientsByName` | 1068 | mapped over `MessengerClientName` |
| `RequiredControllers` | 560 | `Omit<MessengerClients, …services>` |
| `OptionalControllers` | 576 | `Pick<MessengerClients, …services>` |
| `EngineContext` | 971 | `RequiredControllers & Partial<OptionalControllers>` |
| `MessengerClientPersistedState` | 1188 | mapped, `MessengerClientsByName[Name]['state']` |
| `MessengerClientMessengersByName` | 1198 | `typeof MESSENGER_FACTORIES` |
| `Permissions` | 589-590 | `ReturnType<typeof getPermissionSpecifications>[keyof …]` |

`MESSENGER_FACTORIES` itself is at `app/core/Engine/messengers/index.ts`.

## No completeness guard on the engine maps

The extension asserts its two constructions of background state agree, and collapses the type to
`never` when they do not. Mobile has no equivalent: a GitHub code search for `IsEquivalent` across
this repo returns 0 hits (positive control — `MessengerClientsByName` returns 4 — so the search is
reaching the code).

Consequence for derivation work here: adding a controller and forgetting its `EngineState` row
typechecks. Nothing fails. Derive *from* `EngineState` freely; do not assume `EngineState` is
complete because the build is green.

## Redux runs the opposite direction from the extension

`app/reducers/index.ts:66` declares `export interface RootState` by hand, with
`engine: { backgroundState: EngineState }` at line 71, and passes it *into*
`combineReducers<RootState, any>` at line 193. The extension derives its root state out of the
configured store; mobile supplies its root state to the store.

So when deriving a UI type here, `RootState['engine']['backgroundState'][…]` does reach the upstream
controller state types and is the right path. The rest of `RootState` — the ~24 non-engine slices
under `app/reducers/` — is a hand-written boundary, and a derivation that bottoms out there has
reached a declaration rather than a source.

## The strongest derivation in the repo

`app/messengers/ui-messenger.ts` derives the entire UI-facing action and event surface from
`GlobalActions` / `GlobalEvents` by transformation rather than by restatement — asynchronizing every
handler with `infer`, filtering to JSON-serializable actions with a conditional on
`Parameters<Action['handler']>`, and deriving the exclusion list off a const array
(`(typeof MESSENGERS_WITH_EXCLUSIONS)[number]['EXCLUDED_CAPABILITIES']['actions'][number]`). It is
also the only file across the three repos that uses `ExtractActionResponse` from
`@metamask/messenger`. Copy its shape when a consumer needs a *modified* view of an upstream union;
the alternative is re-declaring the union with the modification baked in.

## `moduleResolution` is `node`, and that hides exported types

`tsconfig.json` sets `"moduleResolution": "node"`, not `Node16`. Package `exports` subpaths
therefore do not resolve, and the repo shims each one it needs with an explicit `paths` entry into
`node_modules/@metamask/<pkg>/dist/**/*.d.cts` — `@metamask/keyring-api/v2`,
`@metamask/perps-controller/types`, `@metamask/delegation-controller/types` and others, under a
`// TODO: Remove these once we use Node16 module resolution.` comment.

**Before concluding an authoritative type is not exported, check `paths`.** A type that lives behind
a subpath will not resolve until an entry exists, and the failure looks like the type not existing.
Adding the `paths` entry is the fix; hand-writing the shape because the import "doesn't work" is the
failure this skill is about.

## Other config that bears on derivation

- `strict: true` set explicitly; `noUncheckedIndexedAccess` **not** set, so an element type derived
  out of a `Record` is the value type, not `value | undefined`.
- `lib: ["es2022"]` with **no `DOM`**. A derived type that transitively references a DOM type will
  not resolve here even though the same derivation compiles in the extension, whose `lib` includes
  `DOM`. This is the most common way a type that works upstream fails to land in mobile.
- `skipLibCheck: true` — errors inside upstream `.d.cts` files are not reported. The derived type is
  still checked where you use it, so this suppresses noise rather than the signal you want.
- `isolatedModules: true` — re-export derived types with `export type { … }`.
- `target: esnext`, `module: commonjs`, `jsx: react-native`, `allowJs: true`. As in the extension,
  `allowJs` means a `typeof` derivation can land on an untyped JS module and widen silently.
- `@typescript-eslint/no-explicit-any` is `error` (`.eslintrc.js:170`); a too-wide hand-written type
  passes it.

## The generated action types come from the same binary as `core`'s

Generated `*-method-action-types.ts` files exist here (imported by
`app/core/Engine/controllers/rewards-controller/` and
`app/components/UI/Predict/controllers/PredictController.ts`, and recognized in `.eslintrc.js` and
`.eslintignore`), and they are enforced: `yarn messenger-action-types:check` is the second half of
this repo's `lint` script, running the `messenger-action-types` binary from
`@metamask/messenger-cli ^0.2.0` — the same tool, from `core`'s `packages/messenger-cli`, that
`core` and the extension run. Regenerate with `yarn messenger-action-types:generate`.

So all three repos derive their action handlers from the same class methods with one shared
generator. A hand-written handler signature is the only thing that can put them out of step.

## Open

- The selector layer was not surveyed. Whether mobile's selectors derive from
  `RootState['engine']['backgroundState']` or re-import controller state types directly is unknown,
  and it decides which path this skill should point at for UI work. Settled by a sweep of
  `app/selectors/`.
