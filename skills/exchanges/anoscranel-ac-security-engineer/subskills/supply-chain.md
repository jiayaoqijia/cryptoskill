---
name: supply-chain
domain: security-hardening/supply-chain
trigger: Adding or vetting a dependency, setting up signing or provenance, deciding what to pin, lock, and attest before shipping.
anti_trigger: Prioritising which vulnerable dependency to fix first (subskills/cve-triage.md); storing and rotating credentials (subskills/secrets.md).
scope: SLSA levels, SBOM, provenance, signing, pinning
status: seedling
---

# Supply Chain

## Standard

- **SLSA v1.2** is the current spec: Build track **L0–L3**, Source track **L1–L4** (L4 = two-party review, per slsa.dev/spec/v1.2/source-requirements). GitHub Actions builders qualify for **SLSA 3** — jump straight to 3; minimal-effort publishers take **SLSA 1** (https://slsa.dev/how-to/get-started).
- **CISA 2026 Minimum Elements for an SBOM** (2026-07-29, v2.1) replaces the 2021 NTIA list: 17 required fields including author signature, component hash, license, generation context, tool version (https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom). Formats: SPDX and CycloneDX.
- **Sigstore** removes the signing-key problem: an ephemeral key, bound to an OIDC identity by a Fulcio short-lived certificate, signs, is destroyed, and the event lands in the append-only Rekor log (https://docs.sigstore.dev/cosign/signing/overview/).
- NIST SSDF SP 800-218's **PW.4** (reuse) and **RV** (respond) practices frame the process. ⚠️ US federal SSDF self-attestation (OMB M-22-18) was rescinded 23 Jan 2026 (M-26-05) — attestation now arrives via contract clauses, so its absence is not a safe harbour.
- The live exploit class is post-install code: Shai-Hulud compromised 500+ npm packages via `postinstall` scripts that harvested credentials with TruffleHog and self-propagated through stolen tokens (CISA 2025-09-23; VU#534320).

## Decision rules

1. Commit the lockfile — it pins the full transitive tree, not just direct deps.
2. Every AI-suggested dependency gets a registry-existence check plus a version pin: 4.62–6.10% of generated names do not exist; 127 names were invented identically by all five frontier models, (arXiv:2605.17062).
3. Automerge routine updates only after install scripts are disabled and the lockfile diff reviewed — an automerged bump executes the new package's lifecycle scripts (the Shai-Hulud vector). Security updates fire immediately.
4. Sign releases with Sigstore and take SLSA 3 free on GitHub Actions; deeper attestation chains are demand-driven.
5. If you publish a private package name, claim it publicly or scope it — dependency confusion picks whichever source has the higher version number (Birsan, 2021).

## Procedure

1. Audit install scripts: prefer `--ignore-scripts`; frozen lockfiles in CI.
2. Add to CI in order: lockfile-diff check → registry-existence + pin on every new dependency → SBOM generation (Syft/cdxgen) → SCA scan (OSV-Scanner).
3. Sign artifacts with `cosign` keyless (Sigstore) in the release job; publish the SBOM beside them.
4. Record provenance expectations: hosted builder for SLSA 3; Actions pinned by commit SHA; untrusted-PR jobs separate from release jobs.
5. Respond to a malicious-package event with the CISA pattern: pin to pre-compromise versions, audit with `--package-lock-only` without executing installs, rotate developer credentials, require phishing-resistant MFA.

## Anti-patterns

- Floating version ranges (`^`, `~`) in shipped artifacts; "the package looked popular" as verification.
- Automerge with install scripts enabled; an SBOM generated without a lockfile (some tools emit an empty SBOM ⚠️).
- Assuming upstream will fix it: the EU CRA reporting duty lands on the manufacturer placing the product on the market.

## Done checklist

- [ ] Lockfile committed; CI verifies it; registry-existence + pin gate on every dependency.
- [ ] SBOM per release with the 2026 minimum fields; artifacts signed (Sigstore); provenance at SLSA 3 where free.
- [ ] Install scripts disabled or justified; release jobs separated; incident runbook names pinning, rotation, audit-only installs.

## Sources

- Primary: SLSA spec v1.2 + getting-started (slsa.dev); CISA 2026 SBOM Minimum Elements; CISA Shai-Hulud alert; NIST SP 800-218; Sigstore docs; arXiv:2605.17062 (⚠️); OMB M-26-05 (secondary).
- <https://slsa.dev>
- <https://docs.sigstore.dev>
