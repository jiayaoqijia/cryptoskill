---
name: signatures-versus-macs
domain: software-engineering/signatures-versus-macs
trigger: "Deciding how Byzantine replicas authenticate their messages."
anti_trigger: "Not for TLS configuration, and not for key management policy in general."
scope: "Authentication cost, message counts, and the recovery post-surgery."
status: seedling
---

# Signatures versus MACs

## Standard

Byzantine messages must be authenticated: a replica must prove a purported message came from the named sender and was not forged. Two mechanisms serve. A digital signature lets anyone verify — one signature is checkable by every recipient and by outside auditors — but costs computation per message. A MAC (message authentication code) is cheaper but pairwise: each sender must compute a separate authenticator for each recipient, which multiplies the work as the replica count grows.

The choice behind the choice is recovery. With MACs, a compromised replica's key material exists on every other replica, so evicting it requires the whole membership to redistribute keys. With signatures, revocation replaces one public key and the recovered party can be re-admitted with a fresh keypair without surgery elsewhere. The record should name which recovery the deployment can afford, because the authenticator decision is usually made for performance and paid for during the worst week of the system's life.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://en.wikipedia.org/wiki/Message_authentication_code>.

## Decision rules

- Record the authentication mechanism: signatures, MACs, or a hybrid by message class.
- Record the per-message cost at the deployment's replica count.
- Record the message classes that carry signatures versus MACs.
- Record the eviction procedure for a compromised replica under each mechanism.
- Record how a recovered replica rejoins and with what key material.
- Record the replay protection: sequence numbers, nonces, and their windows.

## Procedure

1. State the mechanism per message class.
2. Compute the authentication cost at full replica count.
3. Compare signature and MAC totals for the deployment's realistic load.
4. Trace an eviction under the chosen mechanism.
5. Trace a recovered replica's rejoin.
6. Write the authentication policy with the recovery path stated.

## Anti-patterns

- Choosing by benchmark while ignoring recovery cost.
- Using MACs in a large membership where the multiplication exceeds signatures.
- Sharing long-lived keys without replay protection.
- Evicting a replica without re-keying those who shared material with it.
- Signing everything, including messages no outside party will verify.

## Done checklist

- [ ] Mechanism per class stated.
- [ ] Cost computed at replica count.
- [ ] Class split recorded.
- [ ] Eviction traced.
- [ ] Rejoin traced.
- [ ] Replay protection recorded.

The hybrid deserves its own line: many deployments sign only the messages an outside party must verify and MAC the rest, and the record should name the boundary, because a message class silently moved across it inherits the wrong recovery path.

## Sources

- PBFT authentication discussion: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
- MAC reference: <https://en.wikipedia.org/wiki/Message_authentication_code>
- Digital signature reference: <https://en.wikipedia.org/wiki/Digital_signature>
