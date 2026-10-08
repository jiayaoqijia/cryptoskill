---
name: tool-selection-economics
description: Use when a step could be done by several tools (shell, script, API, browser, subagent) and the choice affects cost. Picks the cheapest tool that actually satisfies the step, and says why.
---

# Tool-Selection Economics

Each tool has a price in tokens, latency, and failure modes. Choosing the wrong one multiplies the cost of a task that was cheap to do. Pick by matching the tool to the shape of the work.

## Procedure

1. Classify the step: `read-one-thing`, `read-many`, `compute/transform`, `act-on-a-page`, `delegate a big subtask`.
2. Match:
   - Does an existing connection/tool already do exactly this? Use it before shelling out.
   - `read-one-thing` (a file, a field) → the direct read tool, not a shell pipeline.
   - `read-many` or filter → search/grep first, then read only the hits.
   - `compute/transform` over many items → one script in a single code call, not N tool calls.
   - `act-on-a-page` (click, login, JS-rendered) → a real browser; static fetch when the page is static.
   - `delegate a big subtask` → a subagent, and only when the subtask is separable and self-contained.
3. Estimate the cost before running: number of calls × per-call token overhead. If you are about to make 20 similar calls, that is one script.
4. Prefer a batch call over a loop of single calls when results do not depend on each other; issue independent calls together, not serially.
5. Prefer the tool whose failure mode you can detect. A silent default (a fetch that returns an error page with HTTP 200) is worse than a loud one.
6. State the choice when it is non-obvious, in one line: "One Python pass over 4k rows instead of 4k tool calls."
7. Re-evaluate if the chosen tool starts failing in a new way (a paywall, a rate limit). Switching tools is cheaper than fighting a walled one; see `retry-vs-switch`.
8. Price a subagent by its handoff: if the subtask needs hours of shared context to hand off, it is not separable and should stay local.
9. Prefer the tool that returns structured data (JSON) over one you must scrape, when both can do the step.
10. When two tools are close in cost, pick the one whose output you can verify.

## Pitfalls

- Driving a full browser for a page that a plain GET returns, paying render cost for nothing.
- A loop of 30 single-file reads when one script could read and reduce the set.
- Spawning a subagent for a subtask that is three quick calls, adding handoff overhead for no gain.
- Re-fetching a page already fetched this turn because the result was not saved to the workspace.
- Choosing the tool you used last time rather than the one that fits this step's shape.
- Running browser automation to read content a plain `curl` would return, paying render cost for a static page.
- Choosing a heavyweight tool because it is more capable, when the step only needs a substring search.

## Verification

    # Count tool calls for a completed bulk step in the transcript
    # passes when a many-item step used <= 2 calls (navigate+extract, or one script)

Report to the user: the step class, the tool chosen, the reason in one line, and the call count it took.
