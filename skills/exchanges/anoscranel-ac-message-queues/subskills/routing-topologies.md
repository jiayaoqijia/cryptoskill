---
name: routing-topologies
domain: software-engineering/routing-topologies
trigger: "Choosing or reading how messages route from producer to queue."
anti_trigger: "Not for delivery guarantees, and not for recommending a broker."
scope: "Direct, fanout, topic, and headers exchanges, and what each route matches."
status: seedling
---

# Routing topologies

## Standard

A routing topology answers one question: which queues receive a given message? The direct match sends a message to queues bound with the same key; the fanout sends it to every bound queue regardless of key; the topic matches a routing key against a pattern with wildcards; the headers match on arbitrary header fields instead of one key. Each is a different declaration of what the producer is allowed to know about its consumers.

The design consequence is coupling. A producer publishing to a fanout is asserting that every current binding matters, including ones added later without its knowledge. A producer using a topic pattern is encoding a naming convention that every future consumer must follow or silently miss messages. The topology is a contract, and the miss mode is silent: a mis-bound queue does not error, it just receives nothing, and the first symptom is a consumer that starves.

Primary sources: <https://www.rabbitmq.com/tutorials/tutorial-one-python> and <https://kafka.apache.org/documentation/>.

## Decision rules

- Record the exchange type and what a producer must supply to route correctly.
- Record the binding rules and who is permitted to create or change them.
- Record the wildcard grammar for topic patterns and one valid and one invalid key.
- Record what a message does when no binding matches — dropped, returned, or errored.
- Record whether bindings are code, configuration, or an operator's manual act.
- Record the silent-miss test: how a dropped binding is detected before a consumer starves.

## Procedure

1. Write the exchange type and the producer's obligations under it.
2. List current bindings and their owners.
3. State the no-match behaviour explicitly.
4. Record the pattern grammar if topics are used.
5. Derive the silent-miss detector — what watches the starved consumer.
6. Write the topology with the coupling named.

## Anti-patterns

- Treating a topic pattern as match-anywhere; wildcards match segments, not substrings.
- Assuming a mis-binding fails loudly; it produces silence.
- Letting anything rebind a queue without recording the change.
- Publishing to fanout when only some consumers care, and filtering downstream.
- Encoding operational meaning into routing keys without writing the convention down.

## Done checklist

- [ ] Exchange type and producer obligations recorded.
- [ ] Bindings listed with owners.
- [ ] No-match behaviour stated.
- [ ] Pattern grammar recorded.
- [ ] Binding change control recorded.
- [ ] Silent-miss detector named.

## Sources

- Broker routing tutorials: <https://www.rabbitmq.com/tutorials/tutorial-one-python>
- Kafka topic and partition model: <https://kafka.apache.org/documentation/>
- Enterprise messaging patterns background: <https://www.enterpriseintegrationpatterns.com/>
