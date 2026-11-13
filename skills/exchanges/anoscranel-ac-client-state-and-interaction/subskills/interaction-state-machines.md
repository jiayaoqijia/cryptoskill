---
name: interaction-state-machines
domain: software-engineering/interaction-state-machines
trigger: "Modelling interaction logic as finite states and explicit transitions."
anti_trigger: "Not for styling states, and not for animation state."
scope: "Finite states and explicit transitions instead of booleans."
status: seedling
---

# Interaction state machines

## Standard

An interaction modelled in booleans — loading, succeeded, failed, retrying — produces impossible states by multiplication: loading and failed at once, succeeded and retrying together. A finite state machine makes the states the source of truth and the transitions the only way between them. The four-state fetch is the entry example: idle, loading, success, failure — each reachable only from the right predecessor. A form flows draft → submitting → saved / retryable. A dialog is open or closed, never both. The machine's value is not the library but the invariant: states that cannot co-occur cannot co-occur.

Machines earn their keep on compound interactions: a multi-step checkout with an edit-any-step requirement, a drag-and-drop with validation gates, a media player with buffering and error recovery. These collapse in boolean soup and become inspectable in a state chart: every path visible, every guard named, every impossible combination simply absent from the model. Storing the machine in the component tree or in the URL both work; what matters is that one representation is authoritative and every other view derives from it.

Primary sources: <https://xstate.js.org/docs/> and <https://www.w3.org/TR/wai-aria-1.2/>.

## Decision rules

- Reach for a machine when boolean combinations can conflict; keep plain flags when they cannot.
- Name the states as user-visible conditions, not flags: "submitting", not "loading && !done".
- Define the transitions and their guards explicitly; an undesigned transition is a bug's home.
- Derive boolean presentation values from the state, never the reverse.
- Persistence in the URL makes deep-linkable states; persistence in a store makes the machine global — choose one and state it.
- Add to the chart when a bug reveals an unhandled transition rather than patching with a flag.

## Procedure

1. List the states as user-visible conditions.
2. Draw or write the transitions with their guards and events.
3. Remove unreachable states and impossible edges.
4. Implement the states as the single source of truth; derive presentation booleans.
5. Decide persistence: URL, store, or component.
6. Test by event sequences, including the invalid events the machine should ignore.

## Anti-patterns

- Six booleans standing in for a four-state machine.
- States named after implementation, not after what the user sees.
- Fixing an unhandled transition by adding another flag.
- Two representations of the state kept in sync by hand.
- Modelling styling or animation conditions as machine states.

## Done checklist

- [ ] States named as conditions.
- [ ] Transitions and guards explicit.
- [ ] Impossible states removed from the model.
- [ ] Presentation derived, not mirrored.
- [ ] Persistence decided.
- [ ] Invalid-event sequences tested.

## Sources

- Statecharts documentation: <https://xstate.js.org/docs/>
- Accessibility semantics for state disclosure: <https://www.w3.org/TR/wai-aria-1.2/>
- Browser tooling for interaction debugging: <https://developer.chrome.com/docs/devtools/>
