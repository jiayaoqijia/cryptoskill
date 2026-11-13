---
name: undo-and-history
domain: software-engineering/undo-and-history
trigger: "Making destructive actions reversible through a command history."
anti_trigger: "Not for optimistic network writes, and not for version control."
scope: "Command history, scopes, and what undo actually restores."
status: seedling
---

# Undo and history

## Standard

Undo works when actions are commands with inverses, recorded in a history. The command pattern pays for itself here: apply stores enough to reverse itself, undo applies the inverse, redo re-applies. The alternative — snapshots of whole state — is simpler and honest for small documents but pays storage proportional to state size times history length, and restores more than the user asked for: undoing a keystroke should not also undo a scroll or an unrelated edit.

The design questions are scope and granularity. Scope: does undo cross views (a deletion in one panel undoable in another), does it survive navigation, does it survive reload? Granularity: is one undo one keystroke, one word, or one semantic action — and is a dragged item one action or forty? A history depth stated in the record, a scope stated once, and semantic grouping chosen for the user's mental model ("delete row" is one undo) make the feature predictable. Predictable beats sophisticated: an undo that sometimes restores too little is worse than none, because the user trusted it.

Primary sources: <https://developer.chrome.com/docs/devtools/> and <https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API>.

## Decision rules

- Model actions as commands with apply and inverse, or snapshots when state is small.
- State the scope once: view, session, or persisted; undo surprises come from unstated scope.
- Group at semantic granularity: one user-intention per undo step.
- Bound and state the history depth; state the storage cost of that bound.
- Persist the history only if the persistence story survives reload, quota, and multiple tabs.
- Any irreversible action must confirm before executing; undo is not a substitute for asking.

## Procedure

1. Inventory destructive actions and classify: reversible, groupable, or genuinely irreversible.
2. Choose command-versus-snapshot per data size and edit pattern.
3. Define grouping and scope; write them down before implementing.
4. Implement apply, undo, redo with the same grouping.
5. Bound the history and state the bound.
6. Test cross-scope cases: undo after navigation, redo after a fresh edit, undo in a second tab.

## Anti-patterns

- Snapshotting the whole store per keystroke.
- Undo that restores unrelated state along with the intended edit.
- Unbounded history in memory.
- Undoing one drag event forty times because each mouse-move became a step.
- Irreversible actions with no confirmation because "undo exists".

## Done checklist

- [ ] Destructive actions inventoried.
- [ ] Command versus snapshot chosen.
- [ ] Scope and grouping stated.
- [ ] History bounded and stated.
- [ ] Persistence decided.
- [ ] Cross-scope cases tested.

## Sources

- Debugging client interactions: <https://developer.chrome.com/docs/devtools/>
- Persisting client history: <https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API>
- Statecharts for history interactions: <https://xstate.js.org/docs/>
