---
name: surface-hidden-assumptions-in-a-request
description: Use when a request rests on unstated premises about data, load, or environment. Enumerate the assumptions in writing and confirm the risky ones before building.
---

# Surface hidden assumptions in a request

Every brief smuggles in facts nobody said out loud: the row count, the environment, who runs it. An unstated assumption that turns out false forces a rewrite the moment it surfaces.

## Procedure

1. Read the request and list every factual claim it depends on: input size, data shape, environment, operator, schedule.

2. Mark each assumption `stated` (the requester said it) or `silent` (you supplied it).

3. Rank the silent ones by cost-if-wrong: data volume off by 100x, "the table has a unique id", "this only runs weekly".

4. State the top three silent assumptions in your reply with the behaviour that changes if each is false: `assuming <= 10k rows; at 10M this needs an index and a batch job`.

5. Confirm only the assumptions where being wrong forces a rewrite or an irreversible action (deploy, delete, pay).

6. Write the confirmed set to `ASSUMPTIONS.md` with a date and an owner, so drift is detectable later.

7. Re-check the assumptions when any input changes; a new data sample invalidates the old size assumption.

## Pitfalls

- Treating "obviously this runs on prod" as safe when the requester meant their laptop.

- Confirming every trivial assumption, which turns a build into an interrogation.

- An assumption written nowhere gets re-guessed differently in the next session.

- Reading an empty query result as "no data" rather than as a broken filter.

- Letting a size assumption age past a data refresh without re-testing it.

## Verification

```
    grep -c '^SILENT' ASSUMPTIONS.md   # silent assumptions recorded, each with a consequence
```

Report each confirmed assumption and the one behaviour that changes if it proves false.
