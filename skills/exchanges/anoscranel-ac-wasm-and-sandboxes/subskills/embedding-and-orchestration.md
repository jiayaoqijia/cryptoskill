---
name: embedding-and-orchestration
domain: software-engineering/embedding-and-orchestration
trigger: "Managing instantiation and lifetimes of many guests in one host."
anti_trigger: "Not for container orchestration, and not for workflow engines."
scope: "Instantiation, lifetimes, and managing many guests in one process."
status: seedling
---

# Embedding and orchestration

## Standard

A host that runs guest code manages instances: compile or fetch a module once, instantiate it per execution or per session, and destroy instances when their work ends. The lifecycle choices are cost and isolation decisions — instantiating per execution keeps guests from sharing any state and pays initialization each time, while pooling instances amortizes startup and requires the host to prove the pool resets all state between uses.

The failure modes are shared-state leaks and lifetime confusion. A host closure capturing a live instance outlives its task if the reference is not dropped; a pooled instance retaining a capability from its previous caller carries authority across a trust boundary. The orchestration rule that holds both away from the door is the single-responsibility instance: one instance does one task for one caller, and anything that outlives the task is a deliberate, recorded decision, never an accident of reference retention.

Primary sources: <https://webassembly.github.io/spec/> and <https://llvm.org/docs/>.

## Decision rules

- Record the instance model: per-execution, per-session, or pooled.
- For pooled instances, record the reset proof: what state and capabilities are cleared.
- Tie each instance's lifetime to its task; no instance outlives its caller's authority.
- Record the instantiation cost measured, since the model choice rests on it.
- Cap concurrent instances per host process and enforce the cap.
- Define what happens to in-flight work when an instance is destroyed or times out.

## Procedure

1. Choose the instance model from measured instantiation cost and isolation needs.
2. Implement lifetime tied to task or session.
3. If pooling, implement and test the reset of state and capabilities.
4. Set and enforce the concurrency cap.
5. Define destruction semantics for in-flight work.
6. Record the model, the cap, and the measured costs.

## Anti-patterns

- Pooling without a reset proof.
- Instances outliving their caller through a retained reference.
- Unbounded instance counts under load.
- Destroying an instance without defining in-flight behaviour.
- Choosing the model from ideology rather than measured cost.

## Done checklist

- [ ] Instance model chosen and recorded.
- [ ] Lifetime tied to task.
- [ ] Reset tested if pooled.
- [ ] Concurrency cap enforced.
- [ ] Destruction semantics defined.
- [ ] Costs measured and recorded.

Concurrency caps also protect the host from a cooperative failure: a guest that blocks indefinitely holding fuel can stall a worker, and the cap on concurrent instances bounds how many workers one misbehaving pattern can occupy, which is the difference between a degraded pool and an unavailable host.

## Sources

- Instantiation model: <https://webassembly.github.io/spec/>
- Runtime tooling: <https://llvm.org/docs/>
- Interface lifecycle patterns: <https://capnproto.org/encoding.html>
