---
name: compilation-phases
domain: software-engineering/compilation-phases
trigger: "Locating which compilation phase a diagnostic or failure comes from."
anti_trigger: "Not for build-system orchestration, and not for language design."
scope: "From preprocessing to linking, and which phase produces which diagnostic."
status: seedling
---

# Compilation phases

## Standard

Translation proceeds in stages: preprocessing expands directives, parsing builds a syntax tree, semantic analysis checks types and names, optimization transforms the program, code generation emits target instructions, and linking joins separately compiled units. Each phase has its own failure vocabulary — a preprocessing error is about textual expansion, a parse error about syntax, a semantic error about names and types, and a link error about missing or duplicate symbols across units.

The diagnostic location is evidence. An error that mentions a generated line number inside a macro or an expanded header is a preprocessing artefact; an error about an undeclared name is semantic; an undefined-reference error naming a mangled symbol is a link-stage disagreement between what one unit declared and what another provides. Reading the stage correctly directs the fix: a link error is never fixed by editing the failing call site, and a semantic error is not a compiler fault to be argued with.

Primary sources: <https://en.cppreference.com/w/c/language.html> and <https://gcc.gnu.org/onlinedocs/>.

## Decision rules

- Classify each diagnostic by phase before acting on it.
- For macro and header errors, inspect the expanded source, not the directive.
- For semantic errors, check declarations and types at the named location.
- For link errors, inspect the symbol name and its provenance, not the call site.
- Record the toolchain version alongside any genuinely surprising diagnostic.
- Separate the report of a diagnostic from any hypothesis about its cause.

## Procedure

1. Read the diagnostic and identify the phase it names or implies.
2. For preprocessing, expand and inspect the preprocessed output.
3. For parse or semantic errors, work on the source location directly.
4. For link errors, list the symbols and locate their definitions.
5. Form a hypothesis only after classification.
6. Record the diagnostic, phase, toolchain version, and resolution.

## Anti-patterns

- Editing a call site to fix a link error.
- Arguing that a semantic error is a compiler bug before reading the declaration.
- Debugging macros in their unexpanded form.
- Mixing a preprocessing hypothesis with a semantic diagnosis.
- No toolchain version recorded for a surprising diagnostic.

## Done checklist

- [ ] Phase classified.
- [ ] Expanded source inspected where relevant.
- [ ] Declarations checked for semantic errors.
- [ ] Symbols traced for link errors.
- [ ] Hypothesis formed after classification.
- [ ] Toolchain version recorded.

## Sources

- Language translation model: <https://en.cppreference.com/w/c/language.html>
- GCC documentation: <https://gcc.gnu.org/onlinedocs/>
- LLVM documentation: <https://llvm.org/docs/>
