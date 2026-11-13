---
name: accessibility
domain: software-engineering/accessibility
trigger: "\"Is this accessible\", \"meet WCAG 2.2 AA\", \"keyboard users can't reach this\", \"fix contrast\", \"add ARIA\", \"screen reader test\"."
anti_trigger: "Building the component itself (subskills/frontend-ui.md); writing inclusive prose for readers is out of scope for this tree; legal conformance sign-off is a human decision."
scope: "Building and checking to WCAG 2.2 AA: semantics, keyboard, contrast, screen reader"
status: "seedling"
---

# Accessibility

## Standard

- **WCAG 2.2**: W3C Recommendation, first published 5 October 2023; current dated version 12 December 2024 (https://www.w3.org/TR/WCAG22/). Level AA is the usual legal target.
- **WCAG 3.0** is a Working Draft (10 September 2026). Do not cite it as a requirement.
- **EU**: European Accessibility Act, Directive (EU) 2019/882, applies from 28 June 2025. EN 301 549 V3.2.1 (WCAG 2.1 AA based) gives presumption of conformity today. V4.1.1 (WCAG 2.2 AA) was published 2 September 2026 but is not yet cited in the Official Journal. ⚠️ EUR-Lex and ETSI texts not read directly.
- **Core checks**: semantics, landmarks, headings, labels, error identification, alt text, keyboard and visible focus, contrast 4.5:1 (3:1 large text), live regions, page `lang`.
- **Automation ceiling**: best automated tools detect about 18–20% of issues. ⚠️ Inherited figure. A clean scan is a floor.

## Decision rules

1. Native HTML first. ARIA only when no native element fits. Wrong ARIA is worse than none.
2. Every interactive element works with the keyboard alone, in a logical order, with a visible focus indicator.
3. Focus must not be fully hidden by sticky headers or overlays (WCAG 2.2 SC 2.4.11).
4. Pointer targets at least 24 × 24 CSS px or with enough spacing (SC 2.5.8). (https://www.w3.org/TR/WCAG22/#target-size-minimum)
5. No cognitive test for login unless an alternative exists (SC 3.3.8).
6. Every form field has a programmatic label. Errors name the field and say how to fix it.
7. Never use colour as the only signal.
8. CI gate: zero new automated violations against a baseline.
9. Each release: a manual keyboard pass and a screen-reader pass on the top three flows.
10. A conformance claim (VPAT, accessibility statement) is **human-gated**.

## Procedure

1. Automated scan in CI:
   ```ts
   import AxeBuilder from '@axe-core/playwright';
   const r = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag22aa']).analyze();
   expect(r.violations).toEqual([]);
   ```
2. Lint components (`eslint-plugin-jsx-a11y` or your framework's equivalent). Check token pairs for contrast.
3. Keyboard pass: no mouse. Tab through each flow. Check order, visible focus, no traps, Escape closes dialogs.
4. Screen-reader pass: NVDA or JAWS (Windows), VoiceOver (macOS, iOS), TalkBack (Android). Check names, roles, states, headings, dynamic announcements.
5. Zoom to 200%; reflow at 320 CSS px. Nothing clipped; no horizontal text scroll.
6. Log each issue with success criterion, severity and fix.
7. Fix components, not pages.
8. Re-run all checks. Record results per release.

## Anti-patterns

- `div` with `onClick` and no role or key handler.
- `outline: none` with no replacement.
- Placeholder as the only label.
- A clean axe scan treated as conformance.

## Done checklist

- [ ] Automated scan clean against baseline, in CI.
- [ ] Keyboard pass done on all changed flows.
- [ ] Screen-reader pass on top three flows.
- [ ] Contrast, target size, focus visibility checked.
- [ ] Issues logged by success criterion; conformance claim left to a human.

## Sources

- https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/standards-guidelines/wcag/
- <https://unicode-org.github.io/icu/userguide/format_parse/messages/>
- <https://www.w3.org/TR/WCAG22>
