---
name: verify-provenance-of-a-prompt-template
description: Use when you pull a prompt, agent config, or template from a repo, gist, or registry. Verify who signed it and that the bytes match before it runs, because a prompt is executable text.
---

# Verify provenance of a prompt template

A prompt template is code that runs inside a model, so it deserves the same supply-chain scrutiny as a downloaded binary. This skill checks origin, integrity, and diff before a template ever reaches context.

## Procedure

1. Pin to a commit, never a branch: `git clone --depth 1 https://host/prompts.git && cd prompts && git rev-parse HEAD`. Record the SHA.

2. Prefer a signed tag or a published digest. Verify with what the source offers: `git tag -v v1.4.0` (GPG), `cosign verify-blob --signature tpl.sig tpl.md` (Sigstore), or a checksum in a release you already trust.

3. Recomputed integrity must match the advertised value: `shasum -a 256 prompts/agent.md`.

4. Read the diff of exactly what changed since your last known-good pin: `git diff <old_sha>..<new_sha> -- prompts/agent.md`. A template that gained network calls or a "send data to" line is a red flag.

5. Inspect for embedded exfiltration and instruction-smuggling: URLs, `curl`/`wget`, base64 blobs, and zero-width characters.

       grep -nE "(https?://|curl|wget|base64|eval)" prompts/agent.md
       python3 -c "print([hex(ord(c)) for c in open('prompts/agent.md').read() if ord(c)>0x2000])"

6. Confirm the author is a source you decided to trust before reading the content, not after — a convincing template does not validate its own origin.

7. Store the approved bytes read-only with the digest beside them: `chmod 0444 agent.md && echo "$SHA  agent.md" > agent.md.sha256`.

## Pitfalls

- A hash from the same page as the download proves only internal consistency; an attacker controls both.
- Cloning a branch and reading HEAD silently accepts whatever landed since your last review.
- Prompt packs with install hooks execute before you read them; inspect `setup.py`/`postinstall` first.
- Trusting a famous username without verifying the signature invites account-takeover supply-chain attacks.

## Verification

    shasum -a 256 -c agent.md.sha256   # must print: agent.md: OK

Report: "template <path> from <origin>@<sha>, signature verified|absent, digest matches pinned value yes|no, reviewed diff N lines."
