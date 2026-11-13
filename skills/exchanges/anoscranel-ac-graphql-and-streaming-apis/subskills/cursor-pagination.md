---
name: cursor-pagination
domain: software-engineering/cursor-pagination
trigger: "Paginating a GraphQL or streaming connection without losing rows."
anti_trigger: "Not for offset pagination in reports, and not for database indexing."
scope: "Stable cursors, ordering, and why offset pagination breaks."
status: seedling
---

# Cursor pagination

## Standard

Offset pagination asks for a page by its position, which is stable only if nothing is inserted or deleted between requests. In a live dataset it is not: a row inserted before the current offset shifts everything, so the next page repeats an item that was already shown or skips one that was not. A cursor encodes a position in the ordered sequence instead, so the next page begins after the last item seen regardless of what changed.

The cursor must be built from a stable, unique ordering. A timestamp alone is not enough if two records share it, because the tie makes the position ambiguous and the page boundary moves. The ordering should therefore be the sort key plus a unique tiebreaker, and the cursor should encode both so the server can resume exactly.

Primary sources: <https://relay.dev/graphql/connections.htm> and <https://graphql.org/>.

## Decision rules

- Record the sort key and the unique tiebreaker used to build the cursor.
- Record the cursor's encoding and whether it is opaque to clients.
- Record the direction of traversal supported and whether both are offered.
- Record the page size default and maximum.
- Record how total counts, if offered, are computed, since counting can be expensive.
- Record the behaviour when a record referenced by a cursor is deleted.

## Procedure

1. Choose the ordering: sort key plus unique tiebreaker.
2. Define the cursor as an encoding of both values.
3. Implement forward traversal and record the query it produces.
4. Set page size default and maximum.
5. Record deleted-record behaviour and the count strategy.
6. Write the pagination contract with its ordering stated.

## Anti-patterns

- Using a timestamp alone as a cursor, which breaks on ties.
- Exposing the cursor as a raw primary key that clients can guess.
- Implementing offsets behind a cursor-shaped API.
- Offering a total count on every page when the count is expensive.
- Changing the sort order without versioning the connection.

## Done checklist

- [ ] Sort key and tiebreaker recorded.
- [ ] Cursor encoding recorded.
- [ ] Traversal directions recorded.
- [ ] Page size limits recorded.
- [ ] Count strategy recorded.
- [ ] Deleted-record behaviour recorded.

The ordering also has to be stable across writes, which usually means an immutable column: a cursor built on a mutable field like a status or a name can point at a position that no longer exists after an update reorders the set, and the page boundary then silently moves. Recording which columns may change under a live cursor is the check that prevents it.


## Sources

- Relay connection specification: <https://relay.dev/graphql/connections.htm>
- GraphQL pagination guidance: <https://graphql.org/>
- GraphQL specification: <https://spec.graphql.org/>
