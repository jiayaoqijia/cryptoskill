---
name: run-an-airgapped-key-ceremony
description: Use when generating a root signing key or key shares that will control funds. Runs the generation on an offline machine with witnessed entropy, recorded attestations, and no key material on any online host.
---

# Run an air-gapped key ceremony

A ceremony exists so that no single person or machine can quietly produce the key alone, and so the provenance of every share is recorded. This skill generates key material offline, in front of witnesses, and never lets a seed or private key touch an online command line.

## Procedure

1. Prepare a machine that has never been online for the generation, plus two independent cold signers if the scheme is threshold. Verify media hashes from a second source before use.
2. Write the ceremony script and print it beforehand. Everyone signs off on the exact steps before any key exists.
3. Generate entropy from at least two independent sources — a hardware RNG plus physical dice or coin flips — and mix it, so a backdoored RNG cannot alone determine the key.
4. Generate the key or shares offline:
   ```bash
   # on the Airgapped host, no network interface up
   cast wallet new --keystore-key
   ```
   For SPDZ/GG20-style MPC, run each party's instance on a separate offline host so no single host sees the full key.
5. Record each participant, each device serial, each entropy source, and the time, on paper. Have two witnesses countersign the transcript.
6. Move only the encrypted keystore or public key material to the online host; the raw seed or share stays on paper or an HSM, never in an environment variable that ends up in a log.
7. Seal backups: split the seed or each share with Shamir into `k` of `n` pieces, distribute geographically, and destroy the single-source copy only after all backups are verified.
8. Destroy the air-gapped machine's temporary files and, if it was single-use, the machine.

## Pitfalls

- A "cold" machine that was ever connected to Wi-Fi or has a camera/microphone is not air-gapped; a photo of a seed on a phone is a compromise.
- Never paste a seed phrase or private key into a chat, a shell command, or a log — keys come from the offline device or a restricted file, and every participant should be able to say where their share lives.
- Printing the seed on a network printer leaves it in the printer's spool; use a dedicated offline printer or hand transcription.
- Reusing one entropy source across two shares correlates them and can defeat the threshold entirely.
- Skipping the transcript makes a disputed ceremony unresolvable; the paper record is the point.

## Verification

    sha256sum ceremony-transcript.pdf && grep -Ri "seed\|mnemonic" ./ceremony-notes || echo "no plaintext key material in notes"
    # expect a recorded transcript hash and no matches for key words

Report the participants, the threshold, where each share lives, and the transcript hash, quoting the checks.
