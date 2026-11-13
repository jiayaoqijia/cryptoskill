---
name: tree-shaking-and-side-effects
domain: software-engineering/tree-shaking-and-side-effects
trigger: "Working out why unused code survives the build."
anti_trigger: "Not for general dead-code removal in compiled languages."
scope: "Dead-code removal and the patterns that defeat it."
status: seedling
---

# Tree shaking and side effects

## Standard

Tree shaking drops modules and exports that the bundle provably never uses. The proof is structural: if an import binds a named export and nothing reads it, and if removing that export cannot change anything the program observes, the bundler removes it. The catch is the second clause — side effects. A module that assigns to a global, patches a prototype, or registers itself on import is observable, and a bundler that cannot prove otherwise must keep it.

That is why the side-effects field in a package manifest exists: a package that declares its modules free of side effects gives the bundler permission to drop unread exports, and a package that does not — or that declares a wildcard — ships everything a barrel re-exports, whether or not any of it is used. Most tree-shaking failures are a missing or wrong declaration, a barrel import, or code that genuinely has an import-time effect.

Primary source: <https://web.dev/learn>.

## Decision rules

- Record which packages declare themselves side-effect free and which do not.
- Prefer named imports over namespace imports; a namespace import defeats most shaking.
- Import from the specific module, not the barrel that re-exports the whole library.
- Verify shaking by measuring: the same feature, imported two ways, compared by output size.
- Watch for polyfills and prototype patches applied at import time — they anchor whole modules.
- Record the tool's assumptions: pure annotations, production mode, and minification both enabled.

## Procedure

1. List the heaviest packages in the bundle and their side-effects declarations.
2. Rewrite barrel imports to direct module imports for the heaviest symbols.
3. Measure output size before and after each rewrite.
4. Inspect modules that survived despite appearing unused, and find the effect that anchors them.
5. Confirm pure annotations are present where the code allows them.
6. Record what shaking cannot remove and why.

## Anti-patterns

- Importing a namespace to use one function.
- Expecting shaking to remove code with an import-time effect.
- Disabling side-effects declarations to shrink output; the shrink is a lie the runtime pays for.
- Mixing default exports and named exports in ways the tool cannot analyse.
- Measuring before minification and calling the result a win.

## Done checklist

- [ ] Package side-effects declarations recorded.
- [ ] Barrel imports rewritten for heavy symbols.
- [ ] Output measured before and after.
- [ ] Surviving modules explained.
- [ ] Pure annotations confirmed.
- [ ] Unremovable code documented with its anchor.

## Sources

- Module bundling and tree shaking guide: <https://web.dev/learn>
- Package.json side-effects field: <https://nodejs.org/api/packages.html>
- Rollup side-effects documentation: <https://rollupjs.org/introduction/>
