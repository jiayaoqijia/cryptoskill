---
name: cover-empty-loading-and-error-states
description: Use when shipping a list or data view. Designs the empty, loading, error and partial states before the happy path, so a blank screen is never the fallback.
---

# Cover empty, loading and error states

A feature demo usually shows a table full of rows. Real users first see a table with none, then a spinner, then a 500. Design all four states or the product ships looking broken.

## Procedure

1. Enumerate the states for every data surface: `loading`, `empty (first run)`, `empty (after filtering)`, `error`, `partial/stale`, and `loaded`. Write them down before styling.
2. Make the two empties different. First-run empty teaches and offers the primary action; filtered empty offers a way to clear the filter:
       <EmptyState title="No projects yet" cta="Create your first project" />
       <EmptyState title="No results for 'billing'" cta="Clear filters" />
3. Prefer skeletons to spinners for known-shape content — a wireframe of the coming layout reduces perceived wait and prevents layout shift when data arrives. Use a spinner only when the shape is unknown.
4. Give loading a shape, not a vague ellipse: match the skeleton row count to the expected content (3–5 rows), and cap skeleton time with a timeout so a hung request does not shimmer forever.
5. Write an error message that names the failure and the next step, and keep the raw error behind a details toggle: "Couldn't load projects. Retry" above `Request failed: 503`.
6. Preserve the user's input on error. A form that clears itself on submit failure is the most-complained-about bug in the family.
7. Distinguish empty from error in code — do not render `[]` and a network failure with the same component, or users cannot tell "nothing here" from "something broke".
8. Render the empty state as the default in the component and let data replace it, so a slow fetch shows the intended message rather than `undefined`.

## Pitfalls

- One shared "No data" string for empty and error, so a broken backend looks like an empty account.
- Skeletons with a different height than the loaded rows, causing a jump when data lands — the shift is worse than the spinner it replaced.
- Error text exposing a stack trace or an internal hostname to end users.
- A spinner with no timeout: when the request never returns, users stare at motion forever with no retry.
- Filtered-empty that offers "Create new" instead of "Clear filters", sending users to make a duplicate of what they were searching for.

## Verification

    # Force each state and capture a screenshot:
    #   1. intercept the API and return []          -> first-run empty
    #   2. set a filter that matches nothing         -> filtered empty
    #   3. intercept and return 503, delay 10s       -> error, then loading
    grep -rn "EmptyState\|Skeleton\|ErrorState" src/components/ | wc -l

Every data view must reference at least one empty and one error branch. Report the state matrix, the copy for each, and any state that fell through to a bare `null`.
