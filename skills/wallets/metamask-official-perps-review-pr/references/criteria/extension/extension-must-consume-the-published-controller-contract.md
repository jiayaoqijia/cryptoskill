# Extension Must Consume the Published Controller Contract

A controller bump or a `perps-events.ts` merge is proven against the shipped `@metamask/perps-controller` bundle and its `.d.cts`, not against manifests or Mobile assumptions.

- **Client patch compensates for controller state gap** — fix the shared controller contract or use explicit client-owned state.
- **Assumes Mobile-only initialization semantics** — Extension background/controller init may differ.
- **Package bump without compatibility check** — controller version changes need state/method/event compatibility validation.
- **Package bump proved only from manifests or `node_modules`** — those checks can pass while `dist` is stale. After building, verify a symbol introduced by the target controller version is present in the shipped bundle.
- **New constant accepted from main without contract check** — when resolving a merge conflict in `perps-events.ts` or similar, verify every constant added by main against `@metamask/perps-controller`'s `.d.cts` before accepting. Some constants are already supplied by the controller spread with identical string values (no-op to add); others are Extension-only aliases that must stay in the local alias layer. A constant that exists on neither side but has live consumers will cause a compile break if it is accidentally dropped.
- **Extension-only alias keys added as inline snake_case** — Extension-only analytics property keys (e.g. `query_count`, `time_in_search_ms`) must go in the alias layer of `shared/constants/perps-events.ts`, not as inline snake_case object keys. Inline snake_case keys trip `@typescript-eslint/naming-convention`.
