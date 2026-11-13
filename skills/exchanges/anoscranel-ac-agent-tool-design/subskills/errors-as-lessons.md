---
name: errors-as-lessons
domain: prompt-engineering/errors-as-lessons
trigger: "Designing tool error returns that teach recovery."
anti_trigger: "Not for HTTP error handling, and not for the client loop."
scope: "Error returns that tell the model what to do next."
status: seedling
---

# Errors as lessons

## Standard

An error return is a message to a model that has just tried something and is deciding what to do next. "Error: invalid input" gives it nothing to act on but a retry; "Error: date must be in YYYY-MM-DD; received 'March 3'" lets it fix the call in one step. The difference compounds across the loop: an agent that can fix its own errors in one pass converges; one that cannot spins until its iteration guard kills the run.

The good error names the class (validation, not-found, auth, transient, capacity), the exact constraint violated with the received value, and where sensible, the corrected form. It also holds discipline: a distinct error class for "you are not permitted" instead of a generic failure, so the model stops retrying what was never allowed, and a rate-limit message that states when to retry instead of leaving the model to guess. The error payload is the cheapest place to buy agent reliability, because it is the only channel that speaks at exactly the moment of confusion.

Primary sources: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use> and <https://platform.openai.com/docs/guides/function-calling>.

## Decision rules

- Every error carries: class, the constraint violated, the received value, and the corrected form where known.
- Distinguish permanent from transient in the error class itself, not in prose tone.
- Permanent errors (permissions, validation) state "do not retry" in words the model reads.
- Rate limits return the wait interval so the model's retry is timed, not guessed.
- No stack traces, internal identifiers, or dumps a model cannot use.
- Log the full internal detail server-side; return to the model only what informs its next action.

## Procedure

1. Enumerate the failure modes of the tool: validation, not-found, auth, transient, capacity.
2. Give each a structured error class with its triggered constraint as data.
3. Write messages with received values and corrected forms.
4. Test each error against a fresh model pass: can it fix the call in one step?
5. Strip anything internal the model cannot act on.
6. Record the error contract in the tool-surface record.

## Anti-patterns

- "Something went wrong" — a message that produces a wasted retry.
- Retrying permission failures because the error class never said stop.
- Raw exceptions passed through unchanged, leaking internals.
- Different prose for the same class across sibling tools.
- Missing received value, forcing the model to reconstruct its own mistake from context.

## Done checklist

- [ ] Failure modes enumerated.
- [ ] Structured error classes defined.
- [ ] Received values and corrections included.
- [ ] Permanent-transient distinction is machine-readable or plain-stated.
- [ ] One-step recovery verified per error class.
- [ ] Internals stripped from the returned message.

## Sources

- Tool error handling guidance: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
- Function calling errors: <https://platform.openai.com/docs/guides/function-calling>
- Tool layer architecture: <https://modelcontextprotocol.io/docs/concepts/architecture>
