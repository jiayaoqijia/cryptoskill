---
name: key-and-permission-hygiene
domain: crypto-trading/key-and-permission-hygiene
trigger: "Reviewing API key scopes, permissions, allowlists, and rotation."
anti_trigger: "Not for handling key values, and not for venue selection."
scope: "Scopes, withdrawal permissions, IP allowlists, and rotation for API keys."
status: seedling
---

# Key and permission hygiene

## Standard

An API key is a credential with a scope, and the scope decides the damage it can do. The critical distinction is between reading and moving: a key that can read balances and place orders is dangerous if leaked, and a key that can also withdraw is catastrophic. Most venues let the key be restricted, and a key that needs no withdrawal permission should never have it.

The second control is the allowlist. A key bound to a fixed IP address cannot be used from elsewhere, which converts a stolen key into a useless string for an attacker without that address. The third is rotation: a key that has been exposed, even briefly, is a key that should be replaced, and rotation should be routine rather than exceptional.

Primary sources: <https://www.cisa.gov/> and <https://www.nist.gov/>.

## Decision rules

- Every key is recorded with its purpose, its scopes, its allowlist, and its creation date.
- Withdrawal permission is granted only where an automated process requires it, and is recorded as an exception.
- Keys are bound to an IP allowlist wherever the venue supports it.
- Trading keys and read-only keys are separate; one key never serves both.
- Rotation is scheduled and also triggered by any suspected exposure.
- Key values never appear in the record, in chat, or in a repository; only identifiers and storage locations.

## Procedure

1. List every key with its venue, purpose, and creation date.
2. Record the scopes actually granted and the scopes required.
3. Remove every permission the purpose does not need.
4. Apply the IP allowlist and record the addresses.
5. Set a rotation schedule and a rotation procedure.
6. Record the inventory with no secret values.

## Anti-patterns

- One key with full permissions for convenience.
- Leaving withdrawal permission on a key used for market data.
- An allowlist configured but never verified after a network change.
- Keys created for a test and never revoked.
- Storing the key value beside the inventory that describes it.

## Done checklist

- [ ] All keys inventoried with purposes.
- [ ] Scopes reduced to the minimum required.
- [ ] Allowlists applied and verified.
- [ ] Trading and read-only keys separated.
- [ ] Rotation schedule recorded.
- [ ] No secret values in the record.

## Sources

- Authentication and credential guidance: <https://www.cisa.gov/>
- Digital identity standards: <https://www.nist.gov/>
- Investor and market-participant guidance: <https://www.sec.gov/investor>
