---
name: audit-boundary-conditions-in-diff
description: Use when a change touches indexing, ranges, or comparisons and off-by-one bugs hide at the edges. Reviews the zero, one, and last-element cases explicitly.
---

# Audit boundary conditions in the diff

Most logic bugs live at the edges of a range, not in its middle. Reviewing `[0,1,2]` and calling it done misses the empty list, the single element, and the last index.

## Procedure

1. List every new or changed comparison, index, and slice in the diff: `gh pr diff 482 | grep -nE '^\+.*(>=|<=|<|>|\[[^]]*:[^]]*\]|\.length|\.size|len\(|substring|slice\()'`.
2. For each, test the four edges by hand:
   - empty input (n = 0),
   - single element (n = 1),
   - exactly-at-threshold (n == limit),
   - one past the last index.
3. Check `<` versus `<=`. A `for i in range(len(x) - 1)` silently skips the final element; a `while i <= len(x)` reads one past the end.
4. Scrutinize slices: `x[1:]` drops the first item, `x[:-1]` drops the last, `x[a:a]` is empty even when `a` is valid. Confirm each is intentional.
5. Check pagination maths: `offset = page * size` with `count = len(items)` computes the next offset wrong when the last page is partial. Use a cursor or `has_more = offset + size < total`.
6. For date and time ranges, confirm the end is inclusive or exclusive as the caller expects — half-open `[start, end)` is the safe default and should be stated.
7. Add the edge cases as parametrized tests so the boundary is pinned: `@pytest.mark.parametrize("n", [0, 1, LIMIT - 1, LIMIT, LIMIT + 1])`.

## Pitfalls

- `range(1, n)` when the first index is 0, dropping element zero in every run.
- A slice `results[start:end]` where `end` is computed as `start + page_size + 1`, returning one extra row.
- Comparing float thresholds with `==`, so a value meant to be "at least 0.1" fails at 0.0999999.
- String length counted in bytes for a UTF-8 field, so a multibyte character crosses the boundary early.

## Verification

    pytest tests/ -q -k "boundary or edge"   # parametrized over 0, 1, LIMIT-1, LIMIT, LIMIT+1
    python -c "xs=[]; print(xs[len(xs)-1])"   # must raise cleanly, not fall through

Report each comparison and slice you inspected with its edge result, or state that the empty, single, and past-end inputs were all exercised by tests.

## Worked example

A loop reads batches with `for i in range(0, len(x), BATCH)`: empty `x` runs zero times, a single element runs once, both correct. The bug sits in a separate slice `x[1:]` meant to drop a header — when `x` has length 1 it drops the only real row. Parametrizing the test over `n in [0, 1, BATCH - 1, BATCH]` makes the length-1 case fail loudly instead of silently.
