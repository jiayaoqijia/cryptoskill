---
name: test-mpc-share-backup-restoration
description: Use when an MPC wallet holds funds and its share backups have never been restored. Reconstructs the signing key from backed-up shares in an isolated environment and proves the derived public key matches.
---

# Test MPC share backup restoration

An MPC backup is only real if the shares reconstruct the same public key; a corrupted or mismatched backup is discovered at the worst moment otherwise. This skill restores shares in isolation and checks the derived key against the live wallet's public key.

## Procedure

1. Gather the documented restore procedure from the vendor and the share backups. A vendor that cannot describe offline recovery is telling you recovery requires the vendor.
2. Restore on a host that is not a live signing party and has no network access, so a bad restore cannot corrupt the running key.
3. Reconstruct with at least `t` shares but fewer than all, exactly as a disaster would. Confirm the group public key:
   ```bash
   # vendor CLI example; the exact binary differs per scheme
   mpc-cli recover --shares backup-1.share,backup-2.share --derive-secp256k1
   ```
4. Compare the derived public key byte-for-byte with the funded wallet's public key:
   `cast wallet address --public-key <derived>` vs the address that holds the funds.
5. Restore again with a different `t`-subset to prove the shares are interchangeable, not position-locked to one combination.
6. Confirm each share carries the scheme metadata it needs: key id, party id, threshold, and curve. A share without its key id cannot be matched.
7. Wipe the restore host and any temporary share files after the drill.

## Pitfalls

- Backups that require the vendor's live service to decrypt are not offline backups; read the recovery contract before trusting them.
- A restore that yields the right public key but a share marked for a different key id means two wallets' backups were mixed — verify metadata, not just the curve.
- Never paste a share or seed into a chat, a shell command line, or a log; move shares over their own encrypted channel into a restricted 0600 file.
- Testing restore using all `n` shares proves reconstruction but not that losing one share is survivable; test the `t` case.
- A restore drill that runs on your production signing host risks overwriting a live share.

## Verification

    mpc-cli recover --shares backup-1.share,backup-2.share --derive-secp256k1
    # expect the derived address to equal the funded wallet address; any mismatch fails the drill

Report the shares used, the derived address, and the wipe confirmation, quoting the recovery output.
