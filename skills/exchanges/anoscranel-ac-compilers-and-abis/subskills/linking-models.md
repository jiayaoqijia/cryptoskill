---
name: linking-models
domain: software-engineering/linking-models
trigger: "Choosing static versus dynamic linkage and controlling symbol visibility."
anti_trigger: "Not for package management, and not for service deployment."
scope: "Static and dynamic linkage, visibility, and what breaks at load time."
status: seedling
---

# Linking models

## Standard

Static linkage copies a library's code into the program at build time: the result is self-contained, its binary grows with each inclusion, and updates require a rebuild. Dynamic linkage records a dependency resolved at load time: the binary stays small, updates apply without rebuilding, and the program inherits a runtime failure class — a missing or incompatible library version at load time — that static programs do not have.

Visibility is the boundary decision inside a dynamic library. By default many toolchains export every symbol, which couples the library's internal names to every consumer and creates accidental ABI surface; explicit visibility restricts the exported set to the intended interface, shrinks the symbol table, and makes the intended contract the only one load-time resolution can see. A load error naming a symbol that was never intended to be public is a visibility failure, not a missing implementation.

Primary sources: <https://sourceware.org/binutils/docs/ld/> and <https://llvm.org/docs/>.

## Decision rules

- Record which libraries are linked statically and which dynamically, and why each.
- Record the version constraint each dynamic dependency imposes, and where it is declared.
- Set explicit visibility on shared-library builds; defaults export too much.
- Record the intended exported interface as the load-time contract.
- Treat a missing-library or symbol failure as a deployment contract question, not a code bug.
- Verify with a clean load in the deployment environment, not only in the build environment.

## Procedure

1. List each dependency and its linkage model with the reason.
2. Record version constraints and where the loader finds each library.
3. Configure visibility so only the intended symbols export.
4. Inspect the exported symbol table against the intended interface.
5. Load-test in an environment matching deployment.
6. Record the models, constraints, and exported interface.

## Anti-patterns

- Default visibility shipping every internal symbol.
- Testing loads only where the build ran.
- Treating a load-time version miss as a code defect.
- Mixing linkage models for the same library across modules.
- Unrecorded version constraints.

## Done checklist

- [ ] Linkage model per dependency recorded.
- [ ] Version constraints declared and recorded.
- [ ] Explicit visibility configured.
- [ ] Exported table inspected against the interface.
- [ ] Deployment-like load test done.
- [ ] Models and interface recorded.

Static and dynamic also differ in their security-update path: a dynamically linked library receives a fix when the system library is updated, while a statically linked copy carries the old code until the program is rebuilt, so the linkage model is a statement about how vulnerabilities reach the running program and how quickly they can be withdrawn.

## Sources

- Linker models and options: <https://sourceware.org/binutils/docs/ld/>
- Visibility mechanisms: <https://llvm.org/docs/>
- Compiler driver options: <https://gcc.gnu.org/onlinedocs/>
