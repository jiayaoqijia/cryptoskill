# Encoding invariants in Motoko types

Motoko has variants, options, records, and generics — no refinement types, no non-empty list, no zero-cost newtype. So the goal is not "no invalid value can exist", it is **no invalid value can be written by accident**. Variants and options buy that almost everywhere.

## The cost

Everything reachable from a stable actor field is persisted, so changing such a type needs a migration, and the chain is one-way. Two consequences: get types right early, and batch the fixes (`check-limit = 1` allows one pending migration per build). Before proposing a type change, check whether the type is stable-reachable — if it is, the proposal includes the migration.

## T1. Closed set held as `Text`

**Spot it:** permitted values listed in a comment, compared with `==` against literals, or `switch`ed with a `case _` fallback. Statuses, roles, kinds, tiers, categories.

`{ var status : Text }` fails three ways, none a compile error: a capitalisation mismatch, a comparison against a spelling that is never produced, and a new state falling silently into `case _`.

Encode it as a variant, and move data that only exists in one state *inside* that state — so there is no `claimedBy : ?Principal` that can be `null` while the status says claimed:

```motoko
public type TaskStatus = { #open; #claimed : Principal; #done : { at : Time.Time } };
```

**Keep `Text`** when the set is genuinely open (display names, notes, search terms) or an external system owns the string. In the second case parse it into a variant once at the boundary and never `switch` on the raw string again.

**Migration.** Map each known string to a tag. The value of writing it out is that it forces the decision about unrecognized strings; make that decision rather than adding an `#unknown` tag nobody removes.

```motoko project=text-to-variant filepath=src/backend/migrations/20260101_000000.mo
import Map "mo:core/Map";
import Nat "mo:core/Nat";

module {
  type OldTask = { id : Nat; var status : Text };

  // Payload-free: a raw Text source cannot populate a Principal or Time
  // payload, so this step only lifts the tags. The payloaded form above
  // is the end state, reached only when the source data carries the value.
  type NewStatus = { #open; #claimed; #done };
  type NewTask = { id : Nat; var status : NewStatus };

  type OldActor = { tasks : Map.Map<Nat, OldTask> };
  type NewActor = { tasks : Map.Map<Nat, NewTask> };

  public func migration(old : OldActor) : NewActor {
    let tasks = old.tasks.map<Nat, OldTask, NewTask>(
      func(_id, task) {
        {
          id = task.id;
          // Unrecognized strings become #open — still actionable, and no record
          // is silently dropped. Decide this explicitly per domain.
          var status = switch (task.status) {
            case ("claimed") { #claimed };
            case ("done") { #done };
            case _ { #open };
          };
        };
      }
    );
    { tasks };
  };
};
```

## T2. Correlated fields

A `Bool` beside an optional payload has four representable combinations and two meaningful ones. `{ isPaid : Bool; paidAt : ?Time.Time }` becomes `{ payment : { #unpaid; #paid : Time.Time } }`.

Do not over-apply: where a plain `?T` already carries the invariant, use `?T`. The recipe is for two or more correlated fields, or when a tag needs a name an option cannot give it.

## T3. Cardinality

Exactly one → `T`. None or one → `?T`. Any number → `[T]`. A `[T]` that is always empty-or-one makes every caller loop or check `size() == 1`.

Motoko has no non-empty array. `(T, [T])` encodes "at least one" at a real readability cost — use it only where an empty collection is a bug callers keep guarding against.

## T4. Error types

`Result<Ok, Text>` is T1 wearing a different hat: every caller, frontend included, has to string-match to tell failures apart. Make `Err` a variant whose tags carry what a caller needs to react. A `Text` payload *inside* a tag is fine as a human-readable message, never as the discriminator.

See the `Result` section of `writing-motoko` for choosing between `Result`, `?T`, and a trap.

## T5. Internal vs shared views

Internal records carry `var` fields and `Map`/`Set`/`List` values, so they cannot cross a public signature and projects keep a second shared type per entity.

Review the **narrowing**, not just that the split exists. A view mirroring every internal field is a leak that compiles: flag re-exported principal lists, audit trails, internal flags, and other users' data. Keep one `toView` per type — duplicated mappers drift.

## T6. `case _` on variants

A catch-all converts "adding a tag breaks every site that needs updating" into "adding a tag silently does the wrong thing", which is most of the value of the variant. Remove it where a new tag would need new behaviour; keep it where the arms are genuinely uniform and the set is expected to grow.

## T7. Identifier types

`type UserId = Principal` is a transparent alias — any `Principal` type-checks in its place. It documents intent and costs nothing, so do not flag it by default. Flag it only when two id types are actually being crossed at call sites; a one-field record or a variant tag enforces the distinction, at the cost of the Candid shape and a migration if the id is stable state.
