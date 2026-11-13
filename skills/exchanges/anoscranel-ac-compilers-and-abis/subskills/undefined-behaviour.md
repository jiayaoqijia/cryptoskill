---
name: undefined-behaviour
domain: software-engineering/undefined-behaviour
trigger: "Recognizing undefined behaviour and what the optimizer may do with it."
anti_trigger: "Not for target-specific behaviour that is documented, and not for linting in general."
scope: "What UB licenses the optimizer to do, and how to detect reliance on it."
status: seedling
---

# Undefined behaviour

## Standard

Undefined behaviour is not a crash promise; it is the absence of a promise. When a program executes an operation the standard left undefined — a read past the end, a signed overflow, a use of a moved-from value in some languages — the whole execution ceases to have specified meaning, which licenses the optimizer to assume the case never occurs and to reason backwards from that assumption. The resulting program can do anything, including exactly what the author hoped, on Tuesdays.

The optimizer's licence is the part that misleads. Code that "works in debug" often works because an unoptimized build happened to produce the hoped-for effect; the optimized build leaned on the assumption that UB never runs, hoisting or deleting code in ways that change observable behaviour arbitrarily far from the offending line. The discipline is detection-first: sanitizer and diagnostic tooling can find undefined behaviour reliably where reading code cannot, and the fix is to remove the reliance, never to reason around the observed outcome.

Primary sources: <https://en.cppreference.com/w/c/language.html> and <https://gcc.gnu.org/onlinedocs/>.

## Decision rules

- Treat any UB diagnosis as a fault to remove, not an effect to tolerate.
- Run sanitizer instrumentation in CI for code where UB class risk matters.
- Never accept "but it printed the right answer" as evidence about UB.
- When a release-only misbehaviour appears, suspect UB-first and instrument before hypothesizing.
- Record the UB class, the fixing change, and the tool that found it.
- Treat compiler warnings for UB-adjacent constructs as findings, not noise to suppress.

## Procedure

1. Enable the toolchain's UB diagnostics and sanitizers on the suspect path.
2. Reproduce with instrumentation and capture the reported event.
3. Identify the UB class from the tool's report.
4. Replace the reliance with a defined construct.
5. Re-run instrumented to confirm the event is gone.
6. Record the class, the fix, and the detecting tool.

## Anti-patterns

- Reasoning from observed behaviour of an UB execution.
- Removing the sanitizer after a clean run instead of keeping it in CI.
- Suppressing the warning that names the reliance.
- Assuming UB crashes; it usually cooperates until it doesn't.
- Fixing the optimizer's output rather than the source licence.

## Done checklist

- [ ] Sanitizer run on the suspect path.
- [ ] UB class identified from the report.
- [ ] Reliance replaced with defined behaviour.
- [ ] Re-run clean under instrumentation.
- [ ] Sanitizer retained in CI where warranted.
- [ ] Class, fix, and tool recorded.

## Sources

- Language definition and UB catalog: <https://en.cppreference.com/w/c/language.html>
- GCC diagnostics and sanitizers: <https://gcc.gnu.org/onlinedocs/>
- LLVM sanitizer documentation: <https://llvm.org/docs/>
