---
name: generate-an-sbom
description: Use when a release or compliance process needs a machine-readable inventory of shipped components. Emits an SPDX or CycloneDX SBOM from the resolved graph and attaches it to the release.
---

# Generate an SBOM

An SBOM is the bill of materials for a build: every component and version that shipped. It answers "are we affected?" in seconds after the next Log4Shell, but only if it reflects the actual resolved graph and lives beside the artifact.

## Procedure

1. Pick a format by consumer: **CycloneDX** (`bom.json`) for security tooling and VEX, **SPDX** (`sbom.spdx.json`) for license/compliance review. Emit both if unsure — they are cheap.
2. Generate from the resolved graph, not the manifest. With Syft:
   `syft dir:. -o cyclonedx-json > sbom.cdx.json` and `syft packages docker:app:1.4.0 -o spdx-json > sbom.spdx.json`.
3. Language-native tools give more accurate output for one ecosystem: `cyclonedx-npm --output-file bom.json`, `cdxgen -o bom.json`, `cyclonedx-py`, `bazel run //:sbom`.
4. Include the top-level artifact's own name, version and its PURL in the SBOM so the deliverable is identified, and record the build commit in the document metadata.
5. Attach the SBOM to the release together with the artifact and signature: `cosign attest --predicate bom.json --type cyclonedx dist/app`.
6. Validate the document before publishing: `sbom-tool validate -b sbom.cdx.json` or a JSON-schema check against the CycloneDX 1.5 schema.
7. Regenerate on every release — a stale SBOM is worse than none because it gives false assurance.
8. Wire it into incident response: to answer "which services use `openssl 3.0.1`", grep the stored SBOMs, e.g. `jq '.components[] | select(.name=="openssl")' sbom.cdx.json`.

## Pitfalls

- Scanning the source tree misses vendored or compiled-in libraries; scan the built image or the binary where the real components live.
- A lockfile-based SBOM includes dev dependencies that never ship, inflating the list and the CVE noise.
- Omitting versions or PURLs makes the SBOM un-queryable; a component without a version cannot be matched to an advisory.
- SPDX license identifiers must use the official list; a free-text "BSD-ish" field breaks automated compliance.
- Storing SBOMs only in CI artifacts that expire in 90 days loses the historical record you will need next year.
- One SBOM per release is not enough for a monorepo that ships several images; emit one per published artifact.

## Verification

    syft dir:. -o cyclonedx-json | jq '.components | length' && \
      jq -e '.components[] | select(.purl != null)' sbom.cdx.json > /dev/null && echo VALID

The component count is non-zero, every component has a `purl`, and the document validates against the declared CycloneDX schema version.

Report: "SBOM (<N> components, CycloneDX 1.5) for <artifact>@<version> at commit <sha>, validated and attached to the release."
