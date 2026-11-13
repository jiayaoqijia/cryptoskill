---
name: name-mangling-and-symbols
domain: software-engineering/name-mangling-and-symbols
trigger: "Understanding how language names become linker symbols."
anti_trigger: "Not for API naming conventions, and not for DNS or service naming."
scope: "How overloaded names become symbols, and how resolution finds them."
status: seedling
---

# Name mangling and symbols

## Standard

A linker resolves symbols, and a language allows names that cannot be symbols directly: overloads with the same spelling, names in namespaces, operators. The toolchain therefore encodes the language-level identity into a symbol name — the mangled name — carrying scope, parameter types, and linkage class inside the string. Two functions that share a source name produce different symbols, and the same function built by two different mangling schemes produces symbols that cannot meet.

The observable consequences are link-time and runtime. A link error naming a long decorated symbol is naming the exact overload it could not find, and reading the decoration is faster than guessing; an unresolved symbol in a dlopen message is a mangling or linkage-class mismatch, not necessarily a missing function. The linkage class matters as much as the encoding — a name declared with C linkage from two sides must agree, and a missing extern declaration produces the classic undefined-reference on a plain, unmangled name.

Primary sources: <https://sourceware.org/binutils/docs/ld/> and <https://gcc.gnu.org/onlinedocs/>.

## Decision rules

- Read the decorated name in a link error before hypothesizing.
- Record the mangling scheme in use when mixing toolchains or languages.
- Declare cross-language boundaries with the matching linkage class on both sides.
- Inspect the symbol table of a library before declaring an export missing.
- Record the visibility of every symbol intended to cross a shared-object boundary.
- Treat a changed decoration as an ABI break even when the source name is unchanged.

## Procedure

1. Capture the exact symbol name from the diagnostic.
2. Decode it with the toolchain's demangler.
3. Compare the decoded identity against the declared one.
4. Inspect the providing object's symbol table.
5. Check linkage class and visibility on both sides.
6. Record the mismatch and the fix.

## Anti-patterns

- Guessing at an overload from its mangled form without decoding.
- Declaring an extern function with the wrong linkage class.
- Treating an unresolved symbol as a missing implementation.
- Exporting by accident; visibility is a decision.
- Comparing source names when the diagnostic is about symbols.

## Done checklist

- [ ] Symbol captured and decoded.
- [ ] Identity compared with the declaration.
- [ ] Provider's symbol table inspected.
- [ ] Linkage class verified on both sides.
- [ ] Visibility recorded for boundary symbols.
- [ ] Mismatch and fix recorded.

## Sources

- Linker and symbol resolution: <https://sourceware.org/binutils/docs/ld/>
- GCC linkage and naming: <https://gcc.gnu.org/onlinedocs/>
- LLVM symbol handling: <https://llvm.org/docs/>
