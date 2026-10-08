---
name: document-a-deprecated-feature
description: Use when a feature is being retired and callers must be moved off it. Records the replacement, the removal date, and the machine-readable warning that points users to the fix.
---

# Document a Deprecated Feature

Deprecation is a contract: tell users what is going away, when, and exactly what to use instead. A silent removal is a surprise break; a warning with no replacement is only half a deprecation.

## Procedure

1. Mark the feature in its own docs with a banner: deprecated since 2.7.0, removed in 3.0.0, use `new_thing()` instead.
2. Emit a runtime warning at call time that names the replacement and the removal version:
   `warnings.warn("old_fn is deprecated; use new_fn (removed in 3.0)", DeprecationWarning, stacklevel=2)`.
3. Keep the old name working until the stated removal version; do not remove early.
4. Document the replacement with a before/after example, not just a symbol name.
5. Add a dated deprecation entry to the changelog under the Deprecated bucket.
6. List the milestone or version that removes it in the roadmap, and link the tracking issue.
7. For an API, add a `Sunset` HTTP header with the RFC 8594 date: `Sunset: Sat, 31 Dec 2026 23:59:59 GMT`.
8. Give the exact migration path for the edge cases the replacement does not cover one-for-one.
9. After removal, replace the doc page with a pointer stub rather than deleting it, so old links do not 404.
10. Track usage so removal is data-driven: `grep -rc 'old_fn' src/` should reach zero before the removal ships.
11. Announce once at deprecation and once near removal; a single early warning gets ignored.

## Pitfalls

- A deprecation warning with no replacement named, so the reader knows only that they are wrong.
- Removing the feature before the documented date, which breaks the contract the warning made.
- Deleting the doc page at removal, so search results and links dead-end.
- A banner without the version, leaving users unsure whether the next upgrade removes it.
- Deprecating without telemetry, so you cannot tell if anyone still calls it.
- A warning that fires on every call, flooding logs until teams silence all warnings.
- Documenting the sunset date but never enforcing it, so the feature lives on forever by accident.

## Verification

    pytest -W error::DeprecationWarning tests/ -k old_fn
    # calling the deprecated path raises the warning with the replacement and removal version

Report the usage count of the deprecated symbol and the removal version, so the timeline is evidence-based.
