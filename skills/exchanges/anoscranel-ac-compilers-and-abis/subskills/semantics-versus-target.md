---
name: semantics-versus-target
domain: software-engineering/semantics-versus-target
trigger: "Separating what the language guarantees from what the target does."
anti_trigger: "Not for performance profiling, and not for memory-layout tuning."
scope: "What the language guarantees versus what the target makes fast or slow."
status: seedling
---

# Semantics versus target

## Standard

A language definition specifies what a program may observe: sequencing constraints, value ranges, conversion rules. Everything the definition leaves unspecified — struct field order, stack direction, the numeric result of an overflow it does not define — is delegated to the implementation and the target, and code that depends on the delegated parts is code that works by local convention rather than by language guarantee.

The distinction decides what is portable in fact. A program relying only on guarantees behaves identically everywhere the language is implemented; a program relying on target behaviour — a packing pragma's layout, an overflow wrapping result — is testing a property of one compiler on one target. The practical skill is to read questionable code and ask which class it relies on, and to record the answer, because "it works here" is evidence about the target, and nothing more.

Primary sources: <https://en.cppreference.com/w/c/language.html> and <https://gcc.gnu.org/onlinedocs/>.

## Decision rules

- For each dependence in question, classify it as guaranteed, implementation-defined, or undefined.
- Record the classification source: the standard clause or the implementation's documentation.
- Treat implementation-defined behaviour as a porting surface, documented per target.
- Never let undefined behaviour carry a load-bearing result, even one observed to work.
- For a result deliberately relying on target behaviour, record the target and the intent.
- Test dependence classifications by disturbing the conditions that hide them.

## Procedure

1. Read the questionable construct and its intended outcome.
2. Classify the reliance: guaranteed, implementation-defined, undefined.
3. Cite the clause or document that supports the classification.
4. Replace undefined reliance with a defined alternative where one exists.
5. Document implementation-defined reliance per target.
6. Record the classification with the code that relies on it.

## Anti-patterns

- Citing observed behaviour as a guarantee.
- Generalizing one target's layout or overflow result to all.
- Leaving an implementation-defined reliance undocumented.
- Arguing over intent instead of consulting the definition.
- Testing once and calling the reliance safe.

## Done checklist

- [ ] Reliance classified.
- [ ] Classification source cited.
- [ ] Undefined reliance replaced.
- [ ] Implementation-defined reliance documented per target.
- [ ] Deliberate target reliance recorded.
- [ ] Classification stored with the code.

The distinction also disciplines benchmarks: a measurement that depends on implementation-defined layout or timing is a measurement of one target, and generalizing it to the language or the algorithm claims a portability the experiment never tested, which is why the record of any performance claim belongs beside the record of what the code relied on.

## Sources

- Language definition: <https://en.cppreference.com/w/c/language.html>
- Implementation documentation: <https://gcc.gnu.org/onlinedocs/>
- Compiler infrastructure docs: <https://llvm.org/docs/>
