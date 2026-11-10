---
name: recipe-library-audit
description: "Run every recipe of a team recipe library on one client with mm-harness, classify each result with the failing node and exact error, and review naming and composability. Produces a per-client table; changes nothing."
disable-model-invocation: true
maturity: experimental
---

# Audit a recipe library on one client

Use only when explicitly named. Input: the library alias (for example `perps`), the client checkout (Extension, Mobile, Core or Terminal) and its device, and the network (testnet unless the user names mainnet). Use `mm-harness` only. The audit never edits a recipe, the library, the harness or the product; it reports, and proposes library edits.

## 1. Preflight, before the first recipe

- Node from the checkout's `.nvmrc`; run every command on it.
- Pin the harness by path for the whole audit: resolve `mm-harness` once (`command -v mm-harness`, or the slot's `MM_HARNESS_BIN`) and call that path. A harness replaced mid-audit kills the run.
- `mm-harness doctor --fix`, then follow its next command until it passes: `launch --verify`, then `fixtures set` (pass the device for Mobile). Continue only when `mm-harness status` reports the runtime ready and the wallet fixture applied.
- Note the harness version and the library revision (`mm-harness run --list --json` reports both).

## 2. Run each recipe once

List with `mm-harness run --list --json` and keep the recipes of the named library that list this client. For each: `--describe`, then `--plan`, then one run with its defaults on the chosen network. When a required parameter has no default, use the smallest valid value and record it.

- Shared test accounts (dev1 is public): touch only the recipe's target market. A recipe that would close or cancel state it did not open, or needs an exclusive market, keys or a receipt it can't get, is `not-runnable`, with the reason; don't run it.
- Mainnet only when the user named it; otherwise a recipe that needs it is `needs-mainnet`.
- No retries to get a pass. One retry for a clear infrastructure flake, with both attempts recorded.
- A modal or prompt that blocks a recipe is dismissed once outside the recipe and the row says so; never add dismiss steps to a recipe during an audit.
- A child recipe that assumes a page or form is already open (a `select-*` or `set-*` step) runs through its parent journey, or is `not-runnable: child`; run alone it fails on a missing selector that isn't drift.

## 3. Classify from the run's own evidence

Read the failing node and the exact error from the run's `trace.json` and `summary.json`, not the harness summary line.

| Result | When |
|---|---|
| `pass` | Trace passed |
| `stale` | Recipe drift: a selector, testID, route, action or parameter contract that the current product or harness no longer matches (search the product source, including template-literal testIDs, before calling one gone), or a plan that doesn't validate |
| `fail-product` | The error shows the product disagrees with the recipe's claim, checked against the product source |
| `blocked-env` | Fixture, funds, device, runtime or a hidden precondition the recipe doesn't establish |
| `not-runnable` / `needs-mainnet` | Not run, with the reason |
| `unclear` | The cause isn't proven; keep the error |

## 4. Quality pass, one line per recipe

- Naming: one journey has one recipe name; client variants share it.
- Composability: calls library children (`ensure-*`, `close-*`, shared order steps) instead of inline copies. A selector repeated across many recipes means a missing shared child.
- Parameters: market, side, size and provider are parameters with the same names and meaning on every client.
- Preconditions: checks are scoped to the target market, never "account must be empty".

## 5. Output

Write `temp/library-audit/<library>-<client>.md` and `.json` in the checkout: one row per recipe (`recipe | result | failing node | error | quality`), the counts, the harness version and library revision. End with the causes grouped by fix owner (library, harness, product, environment) and the library edits worth proposing. Rerun the same audit after a library change and put both tables in the PR.
