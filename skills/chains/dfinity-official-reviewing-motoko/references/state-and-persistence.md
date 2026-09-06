# Reviewing state and persistence

Under enhanced migration (EM), every top-level `let`/`var` in an actor or mixin is **stable** unless prefixed `transient`, and stable fields are declared **type-only** — their values come from the migration chain.

```motoko
actor {
  let tasks : Map.Map<Nat, Types.Task>;                    // stable; value from the chain
  let state : { var nextId : Nat };                        // stable; mutable counter in a record
  transient var cache = Map.empty<Text, Types.TaskView>(); // rebuilt each start
  include TasksApi(tasks, state);
}
```

## Why EM is not optional

Pre-EM, stable fields carry inline initializers, so a stable field can be initialized from a transient one:

```motoko
transient let defaultQuota = 100;
let quota = defaultQuota;      // stable
```

The initializer runs **once, on first install**. Change `defaultQuota` to `250`, deploy, and `quota` is still `100` — forever, no warning, in code that reads as though the two are linked. The same shape appears with `Time.now()`, a config record, a computed limit: the transient side keeps moving and the stable side is frozen at whatever the first install saw.

EM makes it unwritable. A stable field has no initializer, so the only way to set or change one is a migration — explicit, reviewed, applied exactly once.

## The stable/transient question

For every actor and mixin field: **if this vanished on upgrade, would the app still be correct?**

- **Yes** → `transient`. Caches, derived indexes, memoized views, rate-limit windows, capability handles. Persisting them means migrating them forever and carrying stale entries across the upgrade meant to clear them.
- **No** → stable (no keyword). Anything a user expects to survive a deploy.

Both directions are findings. Constants are the third case: a bare `let X = ...` in an actor or mixin is stable state, so a static value (literals, tuples, immutable records, function values) belongs in a **module**, and a non-static one — anything involving a call, operator, or control flow — has to be `transient let`.

## Three ways mixin state silently decouples

`var` parameters pass **by value**; records pass by reference. Each of these compiles, and none of the writes reach the actor:

- `var nextId : Nat;` handed to a mixin — wrap it as `let state : { var nextId : Nat }` and pass the record.
- A record literal at the `include` site: `include TasksApi({ var nextId = state.nextId })` builds a fresh record. Pass the binding.
- A helper that reshapes the record: if the actor declares `{ var nextId : Nat }`, helpers must accept `{ var nextId : Nat }` and write `state.nextId`. Copying into `{ var counter = ... }` mutates only the copy.

Where two mixins need the same state, declare it once and pass the same binding to both.

A bare `let`/`var` at the top of a `mixin` is implicitly stable and traps at runtime with `IC0503`. It passes compilation and fails on the deployed canister, so it is always a blocker.

## Migration hygiene

| Finding                                                        | Level   | Why                                                                     |
| -------------------------------------------------------------- | ------- | ----------------------------------------------------------------------- |
| An import other than `mo:core/...`                             | Blocker | The chain replays forever; a project type that later changes breaks it. Caught by `caffeineai-lints`. |
| Two pending migrations in one build                            | Blocker | `check-limit = 1`. Fold the second into the first.                       |
| An edit to a migration that predates this build                | Blocker | Applied migrations are tracked by module name; the edit never runs.      |
| A stable field in `main.mo` no migration supplies              | Blocker | Surfaces as M0254 / M0267 and breaks later upgrades.                     |
| A feature-shaped filename (`AddPriority.mo`)                   | Warning | Invites a second file per change instead of editing the pending one. Use `YYYYMMDD_HHMMSS.mo`. |
| An identity migration body                                     | Warning | The change was stable-compatible; delete the file.                      |
| A magic constant in the body                                   | Warning | Derive defaults from the migration input or a domain default.            |
