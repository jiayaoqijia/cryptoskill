---
name: tokenise-values-into-semantic-names
description: Use when components hard-code colours and radii. Replaces literals with two token tiers — raw palette and semantic alias — so a rebrand or theme touches one file.
---

# Tokenise values into semantic names

`color: #2563eb` sprinkled across 40 components means a rebrand is a find-and-replace with collateral damage. Tokens give a value one name and that name one meaning.

## Procedure

1. Create two tiers. Tier one is the raw palette (`--blue-600: #2563eb`); tier two is semantic and points at palette values (`--accent: var(--blue-600)`). Components consume only tier two.
2. Never let a component reference a `-50`…`-900` raw stop directly. If `--blue-600` appears in a `.tsx`, the token layer has been bypassed.
3. Name semantics by role and state, not appearance: `--surface`, `--surface-hover`, `--text-secondary`, `--border-strong`, `--accent-pressed`, `--danger`.
4. Include non-colour values in the same system: `--radius-card: 12px`, `--radius-control: 8px`, `--shadow-overlay: 0 8px 24px rgb(0 0 0 / .12)`, `--z-modal: 1000`.
5. Define once on `:root`, and override per theme or per brand scope:
       :root { --accent: var(--blue-600); }
       [data-brand="acme"] { --accent: var(--green-700); }
6. Keep the token count small enough to hold in your head — often 40–80 semantics. A 300-token system is re-named CSS variables, not a design system.
7. Export tokens to the formats consumers need from one source (JSON → CSS + TS types + iOS/Android) so the numbers cannot drift between platforms.
8. Deprecate rather than delete: mark an old token `--old-name: var(--new-name)` with a comment, migrate call sites, then remove it in a following change.
9. Version the token file so a consumer can see a breaking rename coming; a token contract with a `v1`/`v2` prefix lets an app migrate on its own schedule.
10. Add a lint rule or a code-review checklist item that rejects raw hex and raw radii in component files, because the token layer only survives if bypasses are caught automatically.

## Worked example

Rebranding from blue to green touches one line — `--accent: var(--green-700)` on `:root` — and every button, link and focus ring updates. Without tokens the same change is a repository-wide search for `#2563eb` that also hits a chart palette, an email template and a favicon definition, none of which should move together.

## Pitfalls

- Semantic names that describe appearance (`--light-blue-button`), which forbids dark mode and locks the palette to one look.
- A component reaching for `var(--blue-600, #2563eb)` with a literal fallback, so the raw value leaks back in and drifts from the token.
- Tokens defined in the app but the design file on a separate palette, so the "source of truth" is neither.
- Aliasing a token to a token to a token, producing a chain that a reader must trace three files to resolve.

## Verification

    # Raw hex and px radii outside the token file are bypasses:
    grep -rnE '#[0-9a-fA-F]{3,6}\b' src/ --include=*.tsx --include=*.css | grep -v tokens
    grep -rnE 'border-radius:\s*[0-9]+px' src/ | grep -v tokens

Both searches should return only intentional exceptions (e.g. an SVG fill). Report the token tiers, the semantic list, and each remaining literal with the token it should use.
