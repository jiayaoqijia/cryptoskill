---
name: module-resolution
domain: software-engineering/module-resolution
trigger: "Diagnosing why an import resolves to the wrong or unexpected file."
anti_trigger: "Not for choosing a package manager, and not for runtime rendering."
scope: "How an import becomes a file, and the graph it implies."
status: seedling
---

# Module resolution

## Standard

An import statement names a module; resolution decides which file that name means. The algorithm walks a sequence of candidate locations — the importing file's directory, then upward through node_modules folders, then alias substitutions — and the first match wins. Every resolver shares that shape, but the details differ: extension lists, directory-index defaults, export maps in packages, and case sensitivity can each change the file an import binds to.

Resolution is the build's first semantic act. A bundle is a traversal of the graph that resolution produces, so a resolution surprise becomes a shipped surprise: an import that picks a different file in the build than in the editor ships different code than the author ran. The graph the bundler actually walked, not the graph the author imagined, is what ships.

Primary source: <https://web.dev/learn>.

## Decision rules

- Record the resolver's extension list and index defaults for the project.
- Record every alias and each one's substitution, in one place.
- Verify that an import used in a bundle resolves to the file the author intended, not the first match.
- Check for case-mismatched imports on case-sensitive file systems.
- Watch for re-exports that silently broaden what a barrel file pulls in.
- Prefer explicit file paths in application code; reserve ambiguity for configured aliases.

## Procedure

1. Print the resolver configuration: extensions, aliases, index names.
2. Trace one representative import end to end to the file it binds.
3. Search for case-variant imports across the project.
4. List barrel files and count the modules each re-exports.
5. Export the module graph and confirm the file set against expectations.
6. Record the resolution rules and any divergence found.

## Anti-patterns

- Assuming the bundler resolves the way the editor's language server does.
- Adding an alias to fix one import and changing the meaning of fifty.
- Deep-importing a package bypassing its export map.
- Mixing case-variant imports of the same module.
- Importing a barrel for one symbol and shipping the whole barrel.

## Done checklist

- [ ] Resolver configuration recorded.
- [ ] Representative import traced to its file.
- [ ] Case variants searched and fixed.
- [ ] Barrel re-export sizes measured.
- [ ] Module graph exported and inspected.
- [ ] Resolution rules documented.

## Sources

- Web platform module and bundling guide: <https://web.dev/learn>
- Node.js package resolution documentation: <https://nodejs.org/api/modules.html>
- ES modules specification: <https://tc39.es/ecma262/>
