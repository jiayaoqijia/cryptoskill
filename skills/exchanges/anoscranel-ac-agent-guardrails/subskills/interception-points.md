---
name: interception-points
domain: software-engineering/interception-points
trigger: "Choosing where a runtime check can actually enforce, not just observe."
anti_trigger: "Not for tool permissioning at build time, and not for logging design."
scope: "Where a check can actually block a call, and where it only watches."
status: seedling
---

# Interception points

## Standard

A guardrail only enforces at a point where the flow physically passes through the gate and cannot proceed without the gate yielding a verdict. The runtime tool bus — the single throat through which every tool call is dispatched — is the honest interception point: the agent proposes a call, the bus looks up the action class, routes gated calls to a hold, and only dispatches on a verdict. Points that merely observe (the prompt context, the model's log stream) can warn and record, but cannot block, and calling them guardrails overstates their power by exactly the dimensions that matter.

The second enforcing boundary is the emission bus: the single throat through which every agent output reaches a user or a system. An agent writing into a shell pipe, a PubSub topic, or a UI stream has three points — model output pre-render, rendered pre-send, and delivered after the fact — and only the first two can block. The design patterns matter: in-process function wrapping, a proxy broker, or an out-of-band veto daemon. Each carries different latency, bypass surface, and failure story; the choice is a design decision, not an accident of wherever the SDK offered a hook.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://en.wikipedia.org/wiki/Session_(computer_science)>.

## Decision rules

- Fix the two enforcing throats: the call-dispatch bus and the output-emission bus.
- Both run outside the model's context; checks in the prompt are advisory, never enforcing.
- The routing table (action class to check pipeline) lives beside the bus, versioned.
- The bus holds — and the call does not dispatch — until the pipeline yields a verdict.
- serviceName/label resolvers at the bus level; no calls direct to a tool bypass the bus.
- Record both what the bus blocked and what it waved through, and label each outgoing item with the check set that saw it.

## Procedure

1. Identify the single call-through point for all tool dispatch — make it a true throat.
2. Do the same for all output that reaches a destination — a write bus, a stream browser.
3. Bind the action-class table to the call bus routing.
4. Route gated calls to a hold queue and release on verdict.
5. Label each dispatched call and output item with the checks that passed.
6. Test enforcement by replaying an agent run — a blocked call must never arrive at the tool, and a held call must never dispatch without the verdict.

## Anti-patterns

- Calling a post-hoc detector on a log stream a guardrail — correlation, not causation.
- Checks that run in the prompt context are advisory by design; treating them as enforcement misleads.
- The model with direct network access — the bypass that renders the tool bus moot.
- Multiple dispatch paths; every path must run through the throat or an alternate becomes free.
- Blocking on the model's own output while it still has a direct shell or browser channel.

## Done checklist

- [ ] Single call throat identified and enforced by design.
- [ ] Single output throat identified; every destination reachable only through it.
- [ ] Gated calls actually held — verified by replay test.
- [ ] No dispatch path outside the bus.
- [ ] Every dispatched and blocked item labelled with its check set.
- [ ] The routing table is versioned with the tool manifest.

## Sources

- OWASP LLM Top 10, system-prompt and access-control framings: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- NIST AI RMF, manage/govern controls: <https://www.nist.gov/itl/ai-risk-management-framework>
- Session and boundary concepts: <https://en.wikipedia.org/wiki/Session_(computer_science)>
