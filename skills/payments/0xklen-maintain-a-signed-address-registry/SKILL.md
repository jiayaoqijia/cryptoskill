---
name: maintain-a-signed-address-registry
description: Use when teammates must know which address is legitimately yours. Publishes a signed, versioned address registry so nobody trusts an address from a chat message, email, or a hasty paste.
---

# Maintain a signed address registry

Every address that arrives over chat is a phishing candidate; the fix is a single signed source of truth. This skill publishes your addresses in a signed, versioned document and makes verifying against it the path of least resistance.

## Procedure

1. Keep one registry file mapping each role to an address, with currency and chain:
   ```json
   { "treasury": "0x…", "opsHot": "0x…", "deployer": "0x…", "version": 7 }
   ```
2. Sign the registry with a well-known key whose address is itself published widely (on a site, in a repo, in prior signing sessions), so the signature can be verified:
   `cast wallet sign "registry-v7:$(sha256sum registry.json | cut -d' ' -f1)" --account registry`
3. Commit the signed registry plus a detached signature. Every release bumps the version and includes a changelog of which address changed.
4. Verify any address a counterparty sends against the registry before using it, comparing all 40 hex characters. A mismatch is a stop.
5. Sign the address out-of-band too when it matters: confirm a receive address by a signed message from the counterparty's own key, not just the registry.
6. Rotate on a schedule and on any compromise: bump the version, re-sign, and announce the change through a second channel.
7. Never place a private key or seed in the registry; it holds only public addresses.

## Pitfalls

- A registry with no signature is a wiki; anyone can edit it, so the signature and the published signer address are the whole value.
- Announcing a new address only in the same channel that was compromised defeats the out-of-band check.
- Address-poisoning dust: attackers send tiny amounts from look-alike addresses so the fake shows in history; never copy an address from a wallet's history — use the registry only.
- A vanity address sharing the first and last characters of yours passes a glance; compare the full string, not the ends.
- Stale registries get trusted longer than they should; put an expiry or version in every message that cites one.
- Signing the registry with a key that also signs transactions couples the two; use a dedicated, low-value registry key.
- If the registry signer is a multisig, publish the Safe address and the collected signatures, not a single ECDSA signature.
- A checksum-less address in the registry invites a mistype; store EIP-55 checksummed addresses and validate them.
- Do not substitute an ENS name for the address unless the resolved address is also listed.

## Verification

    cast wallet verify --address $REGISTRY_SIGNER "registry-v7:$(sha256sum registry.json | cut -d' ' -f1)" "0x<sig>"
    # expect 'valid' and the signer to match the widely published registry signer address

Report the registry version, the signer address, and the verification result, quoting the command.
