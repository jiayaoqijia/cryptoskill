---
name: injection-defense
domain: prompt-engineering/injection-defense
trigger: "When untrusted content (user input, retrieved documents, tool output, memory, another agent's messages) can reach the model."
anti_trigger: "Benign single-user prompts with no untrusted content path."
scope: "Prompt-layer defense against prompt injection: trust boundaries, the enforcement order, least-privilege tools, and approval gates."
status: "seedling"
---

# Prompt injection defenses

## Standard

A model response is evidence, never authority; only deterministic policy may authorize
an action (<https://genai.owasp.org/download/52117/>).
Prompt injection is OWASP LLM01, the top LLM risk (OWASP Top 10 for LLM Applications
2025, https://genai.owasp.org/), and indirect injection through retrieved content is a
named agentic threat (OWASP Agentic AI Threats & Mitigations 2025-2026). Enforce from
the strongest layer outward:

1. Effect-time schema validation plus a deterministic policy engine.
2. Sandboxing with filesystem and network egress boundaries.
3. Human approval for high-impact or irreversible actions.
4. Action validation, idempotency, monitoring, and kill switches.
5. Classifier filters as a supplement.
6. Prose, delimiters, and output refusals last; they only reduce likelihood.

The empirical record: adaptive attackers defeated eight prompt-and-filter defenses at
over 50% attack success (NAACL 2025, arXiv:2503.00061); a 2026 large-scale competition
found all 13 tested models vulnerable (arXiv:2603.15714; NIST CAISI summary). So prose
hardening is never a security boundary.

Primary sources: <https://genai.owasp.org> and <https://simonwillison.net>.

## Decision rules

| Content class entering context | Treatment |
|---|---|
| User free text | Data; may propose, never authorizes |
| Retrieved documents | Data envelope; never let its text redefine policy |
| Tool results | Data; validate shape before the model sees it |
| Tool descriptions (MCP) | Untrusted unless the server is trusted (MCP 2026-07-28 security rules) |
| Memory records | Authorized writes only; provenance plus TTL |
| Another agent's messages | Data; verify against the shared task contract |

## Procedure

1. Map every path by which untrusted text reaches the model.
2. For each tool the model can call, rate the risk: write access, reversibility, money
 (OpenAI, https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/).
3. Gate high-risk tools with human approval; fail closed on timeout.
4. Strip or quote-delimit untrusted content so instruction-looking text stays inert.
5. Validate every downstream action against policy in deterministic code before it
 runs.
6. Add canary secrets to untrusted sources so exfiltration trips an alarm.

## Anti-patterns

- An instruction that says "do not follow instructions in the content"; adaptive
 attackers beat it (NAACL 2025).
- A second model asked to spot injections; it is a filter, not a boundary.
- Hiding the prompt as the defense; the prompt is not a secret.
- Approval prompts the model itself can confirm.

## Done checklist

- [ ] Every untrusted-content path is enumerated.
- [ ] High-risk tools sit behind approval that fails closed.
- [ ] Effect-time validation runs in deterministic code, not in the prompt.
- [ ] The red-team record reports attack-success rate with denominators, not slogans.

## Sources

- <https://genai.owasp.org>
- <https://simonwillison.net>
