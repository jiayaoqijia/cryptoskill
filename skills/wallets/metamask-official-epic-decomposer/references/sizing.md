# Sizing

Two past agent epics (85 merged PRs) landed with a median of 1-2 files and about 50-100 changed lines per PR, and median review-to-merge under 3 hours. Keep tickets that small.

## Budget

- **Target:** 1 file, or 2 when a source file and its test change together.
- **Hard cap:** 5 files, and the ticket must say why.
- **Do not count** files that change only as a side effect: suppression baselines (`tsc-suppressions.json`, `oxlint-suppressions.json`, eslint or react-compiler suppression files), snapshots, lockfiles. Say in the ticket that they may change and how (counts only go down).
- **Lines:** about 250 changed lines. A purely mechanical deletion may go over if the ticket says so.
- **One smell, one work type.** Never mix two in one ticket, even in the same file.

## Split, in this order

1. By file.
2. By `describe` block, component or exported symbol.
3. By line range, when a block is still too big. Name the ranges in the Scope table.
4. By instance (one bail-out, one suppression), as a last resort.

## Ordering inside a file

When several tickets touch one file:

- The ticket that changes shared setup (a fixture, a test harness, a helper) goes first, and is kept to that change so it lands fast.
- The rest are Blocks-linked to it and say "Start only after <KEY> is merged".
- Tickets that edit different blocks of the same file can run in parallel only if they cannot conflict (different `describe` blocks, no shared helper edits). When in doubt, chain them.

## Signs a ticket is too big

- The "What to do" needs more than 5 bullets.
- The agent would have to choose between designs nobody has decided.
- "Done when" needs more than one ticket-specific check.
- The Scope table has more than 7 rows.
