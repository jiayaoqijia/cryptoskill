---
name: toolchain-record
domain: software-engineering/toolchain-record
trigger: "Recording toolchain versions, flags, and ABI decisions."
anti_trigger: "Not for dependency manifests, and not for CI configuration notes."
scope: "The written record: toolchain versions, flags, and ABI decisions."
status: seedling
---

# Toolchain record

## Standard

The toolchain record captures the compiler version, the optimization and diagnostic flags, the ABI-relevant settings, and the linker model for each binary the project ships. Its justification is reproducibility under the specific respect that matters here: a binary's behaviour depends on the exact toolchain that built it, so a bug report or a performance claim is only interpretable with those facts attached.

The record's second function is drift detection. Optimization levels and diagnostic flags silently change between build configurations, and a release built with different flags than the tested one has a different licence surface. Recording flags as-built — not as-configured — means the record says what happened, and a later discrepancy between the configured and built states is a finding, not a mystery.

Primary sources: <https://gcc.gnu.org/onlinedocs/> and <https://llvm.org/docs/>.

## Decision rules

- Record the exact toolchain version string and target triple per binary.
- Record optimization, diagnostic, and ABI-relevant flags as built.
- Record the linkage model and dependency versions the loader must resolve.
- Keep the record beside the release artefact, not in a wiki page separated from it.
- Diff the record between releases; unexplained flag changes are findings.
- Record sanitizer and hardening instrumentation when enabled for shipped builds.

## Procedure

1. Capture the compiler version and target for each build.
2. Capture the flags as the compiler received them.
3. Capture the linkage model and dynamic dependencies.
4. Store the record with the artefact it describes.
5. Diff the record against the previous release.
6. Investigate unexplained differences before shipping.

## Anti-patterns

- Recording intended flags instead of actual flags.
- Storing build details far from the binary they describe.
- Missing the diagnostic change when optimization levels change.
- No diff reviewed between releases.
- Treating a local build as representative of CI without comparing records.

## Done checklist

- [ ] Version and target per binary recorded.
- [ ] Actual flags captured.
- [ ] Linkage and dependencies recorded.
- [ ] Record stored with the artefact.
- [ ] Record diffed against the previous release.
- [ ] Diffs explained before shipping.

The record should also capture the diagnostics that were enabled when the binary shipped: a build with warnings suppressed or sanitizers absent has a different evidence value than one built loudly, and a bug report arriving against a quietly-built binary deserves the honest note that the toolchain was not asked to look.

## Sources

- GCC options and reporting: <https://gcc.gnu.org/onlinedocs/>
- LLVM toolchain documentation: <https://llvm.org/docs/>
- Linker invocation records: <https://sourceware.org/binutils/docs/ld/>
