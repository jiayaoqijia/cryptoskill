---
name: resolve-conflicting-memories
description: Use when two memory entries contradict each other. Breaks the tie by source authority, recency, and a live check, then keeps exactly one entry.
---

# Resolve Conflicting Memories

Two stored values for one fact is worse than none: every reader picks a different one. A conflict is resolved by evidence, not by which entry you happened to see first.

## Procedure

1. Surface the conflict: `grep -rn "prod-db-host" ~/.hermes/memories/` to find every entry for the same key.
2. Write both candidate values with their dates and sources side by side.
3. Prefer the more authoritative source, ranked: a live system query > a generated file > a hand-written note.
4. If authority ties, prefer the more recent entry — but only after step 5.
5. Break a remaining tie with a live check: query the system and take the value it returns now.
6. Keep the winner, delete the loser, and append the resolution: `resolved 2026-10-08: host = prod-2 (live dns lookup)`.
7. If the live check contradicts both, the memory is wrong, not just stale — record the correct value and note the error.
8. Fix the writing habit that caused it; the conflict usually traces to append-instead-of-edit.
9. Re-read the store after editing to confirm only one entry remains for the key.
10. If other tasks cached the losing value, note where so they can be corrected.

## Pitfalls

- Taking the first match from grep instead of enumerating all entries for the key.
- Choosing by recency when an older entry came from a more authoritative source.
- "Resolving" by keeping both and adding a note to prefer one — readers still see two.
- Assuming the newer entry is right because it was edited more recently, when the edit was the error.
- Skipping the live check when the system is reachable, and guessing between two values.

- Resolving the pair but not searching for a third entry under a variant key.
- Recording the resolution in a separate note instead of in the entry, so the store stays ambiguous.
- Declaring a winner without writing why, so the next conflict re-opens the same argument.

## Verification

    grep -rc "prod-db-host" ~/.hermes/memories/ | awk -F: '{s+=$2} END {print s}'
    # passes when the count for the key is 1, not 2

Report to the user: the key in conflict, both candidate values, the evidence that decided it, and the single value left.
