---
name: compilation-targets
domain: software-engineering/compilation-targets
trigger: "Compiling code to the sandbox and choosing a toolchain."
anti_trigger: "Not for the host application's build, and not for cross-compilation of native binaries."
scope: "Compiling to the sandbox and the trade-offs each toolchain makes."
status: seedling
---

# Compilation targets

## Standard

Compiling to a sandbox target is a translation with choices: which source language, which toolchain, and which of the target's feature sets. The outputs differ in size, in what they assume about the host interface, and in the garbage-collection story — a language with a runtime brings that runtime's heap into linear memory, where the host sees it as one opaque allocation rather than as objects.

The honest comparison is per-workload, not per-marketing-claim. A compile target that produces small modules may assume particular host imports; one with broad language support may carry a large runtime. The measurement that decides is the end-to-end one the deployment cares about — instantiate, run the real workload, tear down — and the numbers belong in the record beside the choice, because toolchain versions move these results.

Primary sources: <https://webassembly.github.io/spec/> and <https://llvm.org/docs/>.

## Decision rules

- Record the toolchain and version per compiled guest, and per feature set used.
- Record the module's import set produced — the real capability ask, not the intended one.
- Measure module size, instantiation time, and steady-state memory for the real workload.
- Record the runtime story: what garbage collection or allocation model the guest brings.
- Prefer the smallest feature set that runs the workload; features extend the audit surface.
- Record what the compiled guest assumes about shared-structure layout.

## Procedure

1. Select candidate toolchains for the source language.
2. Compile the real workload to each candidate target.
3. Inspect each module's imports and size.
4. Measure instantiate-run-teardown end to end.
5. Choose and record toolchain, feature set, and measurements.
6. Pin the toolchain version in the record.

## Anti-patterns

- Choosing a toolchain from a benchmark of a different workload.
- Shipping a guest whose import set was never inspected.
- Enabling the full feature set by default.
- Comparing module sizes while ignoring instantiation cost.
- Unpinned toolchain versions in the record.

## Done checklist

- [ ] Toolchain and version recorded.
- [ ] Import set inspected and recorded.
- [ ] End-to-end measurements taken.
- [ ] Runtime story recorded.
- [ ] Minimal feature set chosen.
- [ ] Versions pinned.

The import set also reveals hidden assumptions a toolchain makes on its behalf: ahead-of-time workflows may expect runtime helpers the host never agreed to provide, and discovering that at the import inspection is cheap while discovering it at instantiation in production is not, so the inspection step is a gate, not documentation.

## Sources

- Target specification: <https://webassembly.github.io/spec/>
- LLVM target support: <https://llvm.org/docs/>
- Interface layout patterns: <https://capnproto.org/encoding.html>
