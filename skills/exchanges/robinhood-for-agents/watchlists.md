# Watchlists — Lists, Curated Lists & Options Watchlist

**CRITICAL: Always confirm the exact list + symbols with the user before any write below — these mutate the user's account.**

Watchlists are identified by **list_id (UUID)** — there is no "default list" shortcut, by design (so a write can never hit the wrong list).

`restoreSession()` loads tokens but does not validate them. A `TokenExpiredError` on a write means the write did **not** land — re-authenticate via [setup.md](setup.md), re-read the list to confirm its actual state, then redo only the missing operation. This matters most for the two-call move (remove then add): if the second call dies on auth, the symbol is off the source list and not yet on the target.

## Step 1: Look Up the List

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

const lists = await rh.getWatchlists();          // your own lists (metadata + ids)
const curated = await rh.getPopularWatchlists();  // Robinhood-curated lists to follow
console.log(JSON.stringify({ lists, curated }, null, 2));
'
```
Pick the list; note its `id` and `owner_type`.

## Step 2: Read Items

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const items = await rh.getWatchlistItems("LIST_ID");  // enriched with symbol/name
console.log(JSON.stringify(items, null, 2));
'
```
For the options watchlist, use `getOptionWatchlistContracts()` instead — it returns the actual single-leg option **contracts** (each with `option_id`, `position_type`, `chain_symbol`, `strategy`), not just list metadata:
```typescript
const contracts = await rh.getOptionWatchlistContracts();
```

## Step 3: Write Items (confirm with the user first)

`updateWatchlistItems(listId, operation, items)` is a single-list, single-operation primitive — it builds the underlying bulk wire-map internally, so multi-list or mixed create/delete writes are never expressible.

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

// Add AAPL: resolve the exact instrument first (never findInstruments()[0] — a fuzzy search).
const inst = await rh.resolveInstrumentBySymbol("AAPL");
const added = await rh.updateWatchlistItems("LIST_ID", "create", [
  { object_type: "instrument", object_id: inst.id },
]);
console.log(JSON.stringify(added, null, 2));
'
```

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

// Remove: match against the list's actual members so you delete the listed
// object_id (dodging stale-instrument ids), then delete only what's present.
const present = await rh.getWatchlistItems("LIST_ID");
const hit = present.find((p) => p.symbol?.toUpperCase() === "AAPL");
if (hit?.object_id) {
  const removed = await rh.updateWatchlistItems("LIST_ID", "delete", [
    { object_type: "instrument", object_id: hit.object_id },
  ]);
  console.log(JSON.stringify(removed, null, 2));
} else {
  console.log("not_present");
}
'
```
`object_type` is `"instrument"` (stocks/ETFs), `"index"`, or `"currency_pair"`. For indexes/crypto the `object_id` is the UUID directly (from `getIndexInstruments()` / `getCurrencyPairs()`).

Adds/removes are **idempotent** — already-present / not-present items are no-ops, reported declaratively ("ensured present" / "removed" vs "not_present"), never an error.

Writes are single-list, single-operation only. **To move a symbol between lists, that's a remove then an add — two confirmed calls.**

## Create / Rename a List (confirm with the user first)

```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();

const list = await rh.createWatchlist("Tech Longs", { displayDescription: "high-conviction" });
console.log(JSON.stringify(list, null, 2)); // list.id -> populate with updateWatchlistItems
'
```
```typescript
await rh.updateWatchlist(list.id, { displayName: "Tech Longs (2026)" }); // rename/re-describe; items untouched
```

There is **no** delete-watchlist tool (by design — the official MCP has none).

## Follow / Unfollow a Curated List (confirm with the user first)

Make a Robinhood-**curated** list (id from `getPopularWatchlists()`) appear in / disappear from the user's watchlists. Both return `void`; the API echoes the request, not the new state — treat success declaratively.

```typescript
const curated = await rh.getPopularWatchlists();
await rh.followWatchlist(curated[0].id);    // now shows in the user's watchlists
await rh.unfollowWatchlist(curated[0].id);  // removed again
```

## Options Watchlist — Add / Remove Contracts (confirm with the user first)

Add a single-leg option contract to the options watchlist. **Long only** — `quickAddOption` mints one single-leg **long** contract; short-leg entries return an error directing to the Robinhood app, and **multi-leg** strategies aren't modifiable here (they surface in `getOptionWatchlistContracts()` with a null `option_id` and a pointer to the app). Already-present contracts are no-ops (deduped).

```typescript
const inst = await rh.getOptionInstrumentById(optionId); // validate the id (throws if unknown)
await rh.quickAddOption(inst.id, "long");                 // add as a single-leg long contract
```

To remove, match by `option_id` against the contracts actually on the list, then delete their `object_id` via the same `updateWatchlistItems` primitive used for equities:
```typescript
const list = await rh.getOptionWatchlist();               // options watchlist metadata ({ id, ... } | null)
const contracts = await rh.getOptionWatchlistContracts();
const hit = contracts.find((c) => c.option_id === optionId);
if (list?.id && hit?.object_id) {
  await rh.updateWatchlistItems(list.id, "delete", [
    { object_type: "option_strategy", object_id: hit.object_id },
  ]);
}
```

Use the Robinhood app for short legs and multi-leg strategies.

## MCP Users

If using the MCP server instead of the client, the equivalent tools are:

| Client Method | MCP Tool |
|---|---|
| `getWatchlists()` | `robinhood_get_watchlists` |
| `getPopularWatchlists()` | `robinhood_get_popular_watchlists` |
| `getWatchlistItems(listId)` | `robinhood_get_watchlist_items` |
| `getOptionWatchlistContracts()` | `robinhood_get_option_watchlist` |
| `resolveInstrumentBySymbol` + `updateWatchlistItems(listId, "create", …)` | `robinhood_add_to_watchlist` |
| `getWatchlistItems` + `updateWatchlistItems(listId, "delete", …)` | `robinhood_remove_from_watchlist` |
| `createWatchlist(name, opts?)` | `robinhood_create_watchlist` |
| `updateWatchlist(listId, updates)` | `robinhood_update_watchlist` |
| `followWatchlist(listId)` | `robinhood_follow_watchlist` |
| `unfollowWatchlist(listId)` | `robinhood_unfollow_watchlist` |
| `getOptionInstrumentById` + `quickAddOption(optionId, "long")` | `robinhood_add_option_to_watchlist` |
| `getOptionWatchlist` + `getOptionWatchlistContracts` + `updateWatchlistItems(listId, "delete", …)` | `robinhood_remove_option_from_watchlist` |

All MCP watchlist tools **confirm with the user first**, are single-list/single-operation per call, and report results declaratively. See [reference.md](reference.md) for full parameters.

For all client methods, see [client-api.md](client-api.md).
