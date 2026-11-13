---
name: events-versus-commands
domain: software-engineering/events-versus-commands
trigger: "Deciding whether a message should be an event or a command."
anti_trigger: "Not for transport selection, and not for API design."
scope: "A fact versus an instruction, and the coupling each creates."
status: seedling
---

# Events versus commands

## Standard

A command names an action and expects it to be performed, possibly rejected. An event names something that already happened and expects nothing. The producer of a command knows its recipient and depends on its behaviour; the producer of an event knows nothing about its consumers and is free of them.

That asymmetry decides the coupling. A command is a remote procedure call in message form and inherits the recipient's availability as the sender's problem, unless the sender is willing to fire and forget. An event inverts the dependency: the producer publishes and moves on, and any consumer that is down is simply behind. The price is that no one can tell the producer's team what the event must contain, so the schema becomes a negotiated contract.

Primary sources: <https://www.enterpriseintegrationpatterns.com/> and <https://www.cncf.io/>.

## Decision rules

- Record for each message whether it is a fact or an instruction, and the naming that shows it.
- Record the expected recipient count for a command, which should be one.
- Record whether the sender waits for a result, since that reintroduces synchronous coupling.
- Record the events that are business facts, and their owners.
- Record any message whose name describes an instruction but is broadcast, which is the ambiguous case.
- Record the failure semantics the sender expects when the message is not processed.

## Procedure

1. List the messages and classify each as fact or instruction.
2. Rename instructions as imperatives and facts as past-tense statements.
3. Identify broadcast instructions and split them into a fact plus consumers.
4. Record which senders wait for a result and why.
5. Record the failure semantics per message.
6. Review the classification with the consumers' owners.

## Anti-patterns

- Broadcasting an instruction and calling it an event.
- Naming an event as a command and having consumers act as if commanded.
- Sending a command to many recipients and expecting one effect.
- Hiding a synchronous dependency behind a message broker.
- Publishing facts the producer does not own.

## Done checklist

- [ ] Each message classified with naming that matches.
- [ ] Recipient counts recorded for commands.
- [ ] Sender waiting recorded.
- [ ] Business facts and their owners recorded.
- [ ] Ambiguous messages split or resolved.
- [ ] Failure semantics recorded.

## Sources

- Enterprise integration patterns reference: <https://www.enterpriseintegrationpatterns.com/>
- Cloud native messaging guidance: <https://www.cncf.io/>
- Distributed systems practice reference: <https://martinfowler.com/>
