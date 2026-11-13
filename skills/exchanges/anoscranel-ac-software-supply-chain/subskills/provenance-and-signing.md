---
name: provenance-and-signing
domain: software-engineering/provenance-and-signing
trigger: "Verifying where an artifact came from."
anti_trigger: "Not for runtime security controls, and not for code review."
scope: "Verifying where an artifact came from."
status: seedling
---

# Provenance and signing

## Standard

A signature says an artifact has not changed since someone signed it. Provenance says more: a signed statement of how the artifact was built — from which source, at which commit, by which build process. A signature without provenance tells you the bytes are intact; it does not tell you the bytes were built from the source you read, in the process you trusted, without a step you would not have approved.

The practical distinction is what each stops. Signing stops substitution in transit and tampering after the build. Provenance stops the substitution that happens earlier: a build machine that pulled from a different source, or a process that injected something the source never contained. Verification is therefore two checks — verify the signature against the identity, and verify the provenance against the expectation you hold for how this artifact should have been made.

Primary source: <https://slsa.dev/>.

## Decision rules

- Record which artifacts in the pipeline are signed and by what key or identity.
- Record the provenance expectation: the source repository and the build process each artifact should come from.
- Verify provenance against the expectation, not merely the signature against the identity.
- Record who holds the signing identity and how a rotation would proceed.
- Verify at consumption time, not only at publication time — the check belongs where trust is relied on.
- Record the failure mode: what happens when a verification fails, and who responds.

## Procedure

1. Inventory artifacts and their signing status.
2. Record the provenance expectation per artifact type.
3. Wire verification at the point of consumption.
4. Test a deliberate failure: a mismatched provenance must be refused.
5. Document key custody and the rotation procedure.
6. Record the escalation for a failed verification.

## Anti-patterns

- Verifying signatures and calling it provenance.
- Trusting the build machine because it is internal — internal is where substitution happens too.
- Verification at publish only, then consumption trusts transit.
- No defined response when verification fails.
- Provenance expectations kept in nobody's memory.

## Done checklist

- [ ] Artifact signing inventory recorded.
- [ ] Provenance expectation per artifact recorded.
- [ ] Verification at consumption wired.
- [ ] Failure case tested.
- [ ] Key custody and rotation documented.
- [ ] Escalation defined.

The identity behind the signature deserves as much attention as the signature itself: an automated publisher key that anyone with repository write access can invoke proves only that someone with write access ran the build, and a verification that passes against a broad identity is weaker than it appears. Recording which identities are trusted, and how narrowly, is part of the verification rather than an aside.

## Sources

- Supply-chain integrity levels: <https://slsa.dev/>
- In-toto provenance framework: <https://in-toto.io/>
- Sigstore signing and identity: <https://www.sigstore.dev/>
