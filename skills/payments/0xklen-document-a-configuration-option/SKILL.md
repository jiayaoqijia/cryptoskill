---
name: document-a-configuration-option
description: Use when documenting a config flag or environment variable so operators set it correctly. States type, default, valid range, effect, and what breaks when it is wrong.
---

# Document a Configuration Option

A config option is an interface; document it like an API. The reader needs the type, the default, the valid range, and the failure mode of a wrong value.

## Procedure

1. One entry per option, with the canonical name exactly as the code reads it: `MAX_CONCURRENCY`.
2. State the type and the environment: `integer, environment variable`. Note any config-file equivalent and its key path, such as `server.max_concurrency`.
3. Give the default and mark whether it is safe to omit: `default: 8`.
4. Give the valid range and units, with both bounds: `1-64, jobs per worker`. An open upper bound invites an OOM.
5. Explain the effect in one sentence a non-author can act on: "number of jobs each worker runs in parallel; higher raises throughput and memory".
6. Note the failure mode of an invalid value: "values over 64 are rejected at startup; 0 disables the queue".
7. State required vs optional and whether a restart is needed to apply.
8. Give an interaction: options that must move together, such as `MAX_CONCURRENCY <= DB_POOL_SIZE`.
9. Show a correct example line: `MAX_CONCURRENCY=16 ./server`.
10. Add a security note when the value affects exposure, such as `CORS_ORIGINS`.
11. Keep the single source in the code comment and generate the doc page from it where possible, so the two cannot drift.
12. Note the precedence when the same value is set in a file and an environment variable.

## Pitfalls

- Listing the default wrong because it changed in code and the doc did not.
- "String" for an enum, missing the allowed values, so the reader guesses and gets a startup crash.
- Documenting only the flag but not the config-file path users of the file actually set.
- Silent clamping: the doc says up to 64 but the code allows 128, or vice versa.
- No units, so an operator writes `30` meaning seconds when the code reads milliseconds.
- An example value that would be dangerous in production, copied verbatim.
- Forgetting to say whether a bad value fails fast or is ignored, which decides how loudly to test.

## Verification

    ./server --print-config | grep -w MAX_CONCURRENCY
    # the printed default and type match the documented values exactly

Diff each documented default against the code's default and report any mismatch as drift.
