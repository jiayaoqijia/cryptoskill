---
name: subscriptions-and-sse
domain: software-engineering/subscriptions-and-sse
trigger: "Choosing a push transport and defining what it guarantees."
anti_trigger: "Not for message queues between services, and not for socket protocol design."
scope: "Push transport choice, delivery guarantees, and reconnection."
status: seedling
---

# Subscriptions and SSE

## Standard

Push interfaces differ in what they guarantee and what they cost. A GraphQL subscription typically rides a WebSocket, carries a query-shaped payload, and can be filtered per client. Server-sent events ride ordinary HTTP, flow one way, reconnect automatically, and are simpler to operate through proxies and load balancers. Both deliver at most once in practice unless the client tracks position and the server retains history.

Reconnection is where the guarantee lives or dies. A client that reconnects without a resume point has missed whatever arrived during the gap; a client that reconnects with the last event id can ask the server to replay from there, but only if the server retained that history and exposes it. The record should state which of those two exists, because the difference is invisible until a disconnect happens in production.

Primary sources: <https://html.spec.whatwg.org/multipage/server-sent-events.html> and <https://graphql.org/>.

## Decision rules

- Record the transport and the reason for choosing it over the alternative.
- Record the direction of flow: one-way push or bidirectional.
- Record the delivery guarantee: what happens to events emitted during a disconnect.
- Record whether the server retains history and for how long.
- Record the reconnect behaviour and any resume token.
- Record the fan-out limit, since one connection per client becomes a capacity problem at scale.

## Procedure

1. Record the transport choice and its rationale.
2. Record the delivery guarantee and the gap behaviour.
3. Record history retention and the resume token format.
4. Record reconnect and backoff behaviour.
5. Record the connection count and its capacity implication.
6. Write the contract with the guarantee stated plainly.

## Anti-patterns

- Claiming exactly-once delivery over a push channel.
- Reconnecting without a resume point and calling the stream reliable.
- Choosing WebSockets for a one-way feed that SSE would serve.
- Ignoring connection count when the client base grows.
- Assuming a load balancer will preserve a long-lived connection without configuration.

## Done checklist

- [ ] Transport and rationale recorded.
- [ ] Flow direction recorded.
- [ ] Delivery guarantee recorded.
- [ ] History retention recorded.
- [ ] Resume token recorded.
- [ ] Connection capacity recorded.

The capacity implication deserves its own line: a subscription holds a connection open per client, and a thousand clients means a thousand sockets across the load balancer, which is a different resource profile from request-response traffic. Recording the expected connection count and the per-connection memory makes the cost visible before it is a surprise.


## Sources

- Server-sent events specification: <https://html.spec.whatwg.org/multipage/server-sent-events.html>
- GraphQL subscription guidance: <https://graphql.org/>
- WebSocket protocol: <https://www.rfc-editor.org/rfc/rfc6455>
