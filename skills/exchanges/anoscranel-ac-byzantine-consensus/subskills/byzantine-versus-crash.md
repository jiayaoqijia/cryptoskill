---
name: byzantine-versus-crash
domain: software-engineering/byzantine-versus-crash
trigger: "Deciding which failure model a system actually faces."
anti_trigger: "Not for choosing a protocol, and not for security hardening of hosts."
scope: "The failure model: what a Byzantine node may do that a crashed one cannot."
status: seedling
---

# Byzantine versus crash

## Standard

A crash fault is honest: the node stops, sends nothing, and its silence is the failure. A Byzantine fault may say anything: the node can send conflicting values to different peers, replay old messages, misquote a third party, or selectively refuse to answer. Crash consensus detects absence; Byzantine consensus must detect contradiction, and contradiction requires testimony from enough independent witnesses to outvote the liar.

The model choice is a claim about the adversary. Crash tolerance suffices when failures are mechanical — power, disk, network. Byzantine tolerance earns its cost when a participant may act against the protocol: a compromised machine, a buggy implementation that diverges from the spec, or jurisdictions and companies that benefit from equivocation. The record should name the adversary, because "we might be attacked" is not the same threat as "our hardware fails", and they buy different systems.

Primary sources: <https://en.wikipedia.org/wiki/Byzantine_fault> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## Decision rules

- Record the failure model the deployment claims, and the adversary it names.
- Record what a faulty node may do: stop only, or equivocate and lie.
- Record whether a node's software is trusted-shared or independently implemented.
- Record the consequence of a minority of nodes being controlled by one actor.
- Record the cost the chosen model pays in replicas, rounds, and cryptography.
- Record the downgrade danger: a Byzantine claim weakened to crash tolerance by configuration.

## Procedure

1. Write the adversary statement in one sentence.
2. Classify each failure cause the system has observed: mechanical or adversarial.
3. Record whether any single actor can control more than one replica's messages.
4. Compare the replica and message costs of each model.
5. Check the deployed configuration against the claimed model.
6. Write the model statement with the adversary named.

## Anti-patterns

- Claiming Byzantine tolerance while running a crash-fault protocol.
- Paying Byzantine costs with a trust assumption that never needed them.
- Naming no adversary, leaving the threat model decorative.
- Treating independently-written clients as needing no tolerance.
- Forgetting that shared bugs defeat the model: identical faulty nodes are not independent faults.

## Done checklist

- [ ] Adversary statement written.
- [ ] Failure causes classified.
- [ ] Single-actor control bound recorded.
- [ ] Costs of each model compared.
- [ ] Deployment configuration checked against the claim.
- [ ] Model recorded with the adversary named.

## Sources

- Byzantine fault reference: <https://en.wikipedia.org/wiki/Byzantine_fault>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Original problem framing: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
