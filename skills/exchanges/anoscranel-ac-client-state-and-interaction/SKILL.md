---
name: ac-client-state-and-interaction
description: "Client-side state as its own engineering problem: server cache versus UI state and the data layer that separates them, optimistic updates and rollback on failure, finite state machines for interaction logic, undo and redo as a command history, list virtualization for long lists, offline reads and writes on the web with background sync, and the written client-state record. It explains the client data layer and interaction mechanics; it never recommends a framework and never promises an offline app. Use when asking \"server state versus client state\", \"optimistic update\", \"state machine UI\", \"undo redo implementation\", \"virtualized list\", \"offline first web\", \"background sync\", \"stale while revalidate\", \"undo history\", \"when to refetch\". Not for component structure and state placement basics (ac-frontend-ui), not for mobile offline sync (ac-mobile-client-engineering), not for WCAG conformance (ac-frontend-ui)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Client state and interaction

## Overview

The client holds two different things called state. Server state is a local copy of data the server owns — its truth is remote, it can be refetched, and it goes stale. UI state is local and ephemeral: which tab is open, what the user typed, what an animation is doing. Confusing the two produces the classic pathologies — refetch loops, optimistic writes that never reconcile, form input erased by a background refresh. The first discipline of this skill is keeping the two apart, usually with a data layer that owns the server copy and invalidation, while UI state stays in components.

The second discipline is interaction honesty: an optimistic update is a promise the client makes to the user and must keep or visibly retract. A state machine makes interaction logic inspectable where booleans produce impossible combinations. Undo turns destructive actions from irreversible commits into navigable history. Virtualization keeps a million-row list responsive, offline keeps the web app usable without a network, and background sync reconciles writes made while disconnected.

Primary sources: <https://tanstack.com/query/latest/docs/framework/react/overview> and <https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API>.

## When to use

- When client state, caches, and data-layer design go wrong or are being designed.
- When optimistic updates, undo, or interaction state machines are being built.
- When lists, feeds, or tables outgrow the DOM.
- When the web app must read or write while offline.

## When NOT to use

- For component structure, state placement basics, and design tokens (use ac-frontend-ui).
- For WCAG conformance and accessibility mechanics (use ac-frontend-ui).
- For mobile-device offline sync and conflict resolution (use ac-mobile-client-engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/server-versus-ui-state.md` | `software-engineering/server-versus-ui-state` | The two kinds of client state, the data layer, and invalidation. |
| `subskills/optimistic-updates.md` | `software-engineering/optimistic-updates` | Instant writes, rollback on failure, and reconciliation. |
| `subskills/interaction-state-machines.md` | `software-engineering/interaction-state-machines` | Finite states and explicit transitions instead of booleans. |
| `subskills/undo-and-history.md` | `software-engineering/undo-and-history` | Command history, scopes, and what undo actually restores. |
| `subskills/list-virtualization.md` | `software-engineering/list-virtualization` | Windowing long lists without losing scroll anchors. |
| `subskills/offline-and-sync.md` | `software-engineering/offline-and-sync` | Reads and writes without a network, and the sync that follows. |
| `subskills/client-state-record.md` | `software-engineering/client-state-record` | The written record: layer choices, promises made, failure paths. |

## Status and honest limits

A data layer and a state machine catch whole classes of bugs, but they cannot make an unreliable backend reliable, and an optimistic UI lies confidently if the server's eventual response is the one that matters most. Offline-first on the web is bounded by storage quotas, cache lifetimes, and platform removal of stored data — the record should state those limits rather than promise availability. Nothing here recommends a library; patterns are described so they can be implemented anywhere.
