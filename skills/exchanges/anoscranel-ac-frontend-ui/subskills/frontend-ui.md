---
name: frontend-ui
domain: software-engineering/frontend-ui
trigger: "\"Build this UI\", \"make this component\", \"where should this state live\", \"make it responsive\", \"use our design tokens\", \"this component is a mess\"."
anti_trigger: "WCAG conformance checks (subskills/accessibility.md); Core Web Vitals and bundle cost; browser tests; native mobile UI craft is out of scope for this tree."
scope: "Component structure, state, responsive layout, design-system use"
status: "seedling"
---

# Frontend UI

## Standard

- ⚠️ **No vendor-neutral standard** exists for component or state architecture. The authorities are framework docs.
- **React, "Choosing the State Structure"**: group related state; avoid contradictions; avoid redundant state; avoid duplication; avoid deep nesting (https://react.dev/learn/choosing-the-state-structure).
- **Vue**: Pinia for shared app state (https://vuejs.org/guide/scaling-up/state-management).
- **Design tokens**: DTCG Format 2025.10, a stable W3C Community Group report, not a W3C Standard (https://www.designtokens.org/TR/2025.10/format/).
- **Design system** = components + tokens + documented rules (Nielsen Norman Group).
- **Usability lens**: Nielsen's 10 heuristics — a review rubric, not a gate.
- **Layout regressions**: visual regression tests per viewport against an approved baseline.

## Decision rules

1. State lives in the lowest component that needs it. Lift it only when siblings must share it.
2. Derive, do not store: anything computable from props or state is computed at render.
3. Classify state: server cache (a data-fetching library), URL (filters, page, tab), form, local UI, global app. Global store only for the last.
4. Components: presentational ones take props and emit events; containers fetch and own state. Keep each under one screen of code. ⚠️ House heuristic.
5. Every colour, space, radius and font size comes from a token. A raw hex or pixel value in a component is a defect.
6. Mobile-first CSS. Breakpoints come from tokens. Use flexbox and grid; no fixed widths on containers.
7. Every data view handles four states: loading, empty, error, success.
8. Use native elements (`button`, `a`, `input`, `select`) before custom widgets.
9. Agent-generated UI follows the written design system; the agent cannot hold it in memory across sessions.

## Procedure

1. List the screen's states and user actions. Sketch the component tree.
2. Mark each piece of state with its class (rule 3) and its owner component.
3. Pick existing design-system components first. Build new ones only for gaps.
4. Write the component:
   ```tsx
   type Props = { items: Item[]; onSelect(id: string): void };
   export function ItemList({ items, onSelect }: Props) {
     if (items.length === 0) return <EmptyState text="No items yet" />;
     return (
       <ul className="stack-md">
         {items.map(i => (
           <li key={i.id}><button onClick={() => onSelect(i.id)}>{i.name}</button></li>
         ))}
       </ul>
     );
   }
   ```
5. Style with tokens only:
   ```css
   .stack-md { display: grid; gap: var(--space-md); }
   ```
6. Check at three widths: 360 px, 768 px, 1280 px. ⚠️ House viewport set.
7. Add component tests for behaviour and visual snapshots per viewport.
8. Heuristic pass: status visible, errors explained, undo possible, labels consistent.

## Anti-patterns

- Copying props into state, then syncing them.
- One global store for everything.
- Hard-coded colours and pixel values.
- Clickable `div` instead of `button`.
- Only the happy-path state rendered.
- Huge components.

## Done checklist

- [ ] Each state has one owner; derived values not stored.
- [ ] Loading, empty, error and success states built.
- [ ] Only tokens used for visual values.
- [ ] Layout checked at three widths; visual snapshots added.
- [ ] Native elements used where they exist.

## Sources

- https://react.dev/learn/choosing-the-state-structure · https://www.designtokens.org/TR/2025.10/format/
- <https://www.nngroup.com/articles/design-systems-101/>
