---
name: review-null-and-empty-input-paths
description: Use when new code assumes values are present and non-empty. Traces every new field and parameter through the null, empty-string, and empty-collection cases before approving.
---

# Review null and empty input paths

Code written against the happy record in the developer's head crashes on the real database, where that column is `NULL` and that relation is an empty list.

## Procedure

1. List new dereferences and iterations in the diff: `gh pr diff 482 | grep -nE '^\+.*(\.[a-z_]+\.|for .* in |\.map\(|\.forEach\(|\[0\]|\.get\(\))'`.
2. For every field touched, ask whether the source can be null: nullable DB columns, optional JSON, map lookups that miss, `find`/`querySelector` that can return nothing.
3. Trace the three empties separately — they fail differently:
   - `null`/`None`/`undefined` — dereference throws,
   - `""` — passes a `!= null` check but fails truthiness and length,
   - `[]` / `{}` — `.first()` or `[0]` is an index error.
4. Check optional chaining and its silent half: `a?.b.c` still throws if `b` is undefined; you need `a?.b?.c`. An `??` default does not apply when the value is `""` or `0`.
5. Verify the empty case has defined behaviour: return an empty result, skip, or raise a typed error — not an unhandled crash.
6. In SQL, confirm `NOT IN` against a subquery that can yield `NULL` is not silently returning zero rows.
7. Add a test per empty kind, with the field literally set to `None`, `""`, and `[]`.

## Pitfalls

- Guarding with `if x:` so a legitimate `0` or `""` is treated as missing.
- Optional chaining on the outer object but not the inner property, moving the crash one level down.
- A default of `[]` created in an argument list (`def f(items=[])`) shared across calls and mutated.
- An empty collection passed to a `min`/`max`/`.reduce` that raises instead of returning a sentinel.

## Verification

    pytest tests/ -q -k "none or empty or null"
    # Also exercise the live type: assert the field is Optional in the schema.
    gh pr diff 482 | grep -nE '^\+.*\?\?|is None|!= null|Optional'

Report each new field and the empty inputs you traced, or state that null, empty-string, and empty-collection inputs are each covered by a test.

## Worked example

A change adds `return user.profile.avatar.url`. `profile` is a nullable one-to-one, so a user without one raises `AttributeError`. The fix:
    return user.profile.avatar.url if user.profile else DEFAULT_AVATAR
The tests set `profile=None`, then `avatar=""`, then `url=""`, and assert the default avatar is returned for each — three distinct empties, three assertions.
