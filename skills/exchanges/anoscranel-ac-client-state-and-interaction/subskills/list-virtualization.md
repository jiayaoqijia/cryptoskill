---
name: list-virtualization
domain: software-engineering/list-virtualization
trigger: "Rendering long lists by windowing instead of mounting everything."
anti_trigger: "Not for pagination design, and not for feed ranking."
scope: "Windowing long lists without losing scroll anchors."
status: seedling
---

# List virtualization

## Standard

A list of ten thousand rows does not need ten thousand elements in the DOM. Virtualization renders the visible window plus an overscan margin, positions it within a spacer sized to the full content, and recycles elements as the user scrolls. The DOM stays flat and the compositor stops drowning — the interaction cost of a huge list is a DOM-size cost, and virtualization is how a long list stays responsive.

The correctness risks are the edges. Variable heights break the offset arithmetic: the window needs measured or estimated item heights, and estimates must correct themselves as items render or the scrollbar lies and the anchor drifts. Scroll anchoring — the browser's own mechanism that keeps the visible content stable when content above changes — must be understood before being defeated by a virtualizer that repositions the container. Keyboard focus and find-in-page only reach rendered items; a focus jump beyond the window must scroll to render the target first, and search should query the data, not the DOM.

Primary sources: <https://web.dev/learn/performance> and <https://developer.chrome.com/docs/devtools/>.

## Decision rules

- Virtualize past a stated row threshold and say the threshold in the record.
- Measure or estimate item heights; correct estimated offsets as items render.
- Keep overscan small enough to stay lazy and large enough to stop flashing.
- Test keyboard navigation to unrendered rows: focus scrolls first, then lands.
- Search and find-in-page query the backing data, never the mounted window alone.
- State the resize and reordering rules: what happens to the anchor when the data changes above it.

## Procedure

1. State the row threshold that triggers virtualization and the overscan margin.
2. Choose the height strategy: fixed, measured, or estimated-with-correction.
3. Implement the spacer, window, and recycling.
4. Wire focus management to scroll-then-render for off-window targets.
5. Point search and selection at the data, not the DOM.
6. Test variable heights, fast scroll, data mutation above the anchor, and window resize.

## Anti-patterns

- Virtualizing a fifty-row list for library reasons.
- Fixed-height math on a list with variable-height rows.
- Losing the scroll position because the spacer recalculated on every render.
- Focus disappearing when the focused row leaves the window.
- Sorting the data without preserving or resetting the anchor by an explicit rule.

## Done checklist

- [ ] Threshold and overscan stated.
- [ ] Height strategy chosen and correction implemented.
- [ ] Focus navigation scrolls to targets.
- [ ] Search queries the data.
- [ ] Anchor behaviour on mutation stated.
- [ ] Resize and reorder tested.

## Sources

- Rendering performance: <https://web.dev/learn/performance>
- DOM inspection during scroll: <https://developer.chrome.com/docs/devtools/>
- ARIA semantics for windowed lists: <https://www.w3.org/TR/wai-aria-1.2/>
