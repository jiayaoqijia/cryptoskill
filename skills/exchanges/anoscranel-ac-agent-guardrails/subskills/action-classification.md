---
name: action-classification
domain: software-engineering/action-classification
trigger: "Deciding which agent actions need a gate before they run."
anti_trigger: "Not for static tool permissions, and not for predicting agent behaviour."
scope: "Which actions need a gate, and the test that decides."
status: seedling
---

# Action classification

## Standard

The gate test is not "could this fail" but "could this be undone." An action is gated when reversal is impossible, expensive, or external: deleting records, sending messages to third parties, moving money, modifying shared infrastructure, publishing content. A read is never gated; a write to scratch may be logged only; a write to production is gated. The three-tier ladder — read, reversible write, irreversible write — decides the machinery applied, and it is written once in a table rather than re-argued per tool.

The classification is a design activity, not a runtime one; the runtime table is built from it. Every tool in the agent's manifest is classified before the agent runs, and a new tool arriving after deployment inherits a default class — by position, the strictest the agent has. Misclassification errors skew loud: classifying an irreversible action too low is the failure that makes the whole rest of the layer necessary.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://en.wikipedia.org/wiki/Idempotence>.

## Decision rules

- Write the action-class table once: tool, tier, rationale.
- Tier by reversibility, not by likelihood; likelihood is a guardrail-tuning number, reversibility is a class.
- Default for unclassified newcomers is the strictest tier the agent carries.
- Any action crossing a trust boundary — external user, payment network, infra API — is a gated tier regardless of local reversibility.
- Classify by the tool's actual effect, not the model's intended use of it.
- Review the table whenever the tool manifest changes.

## Procedure

1. List every tool in the agent's manifest.
2. For each, ask: what does it change, who can undo it, what does undoing cost.
3. Assign the tier: read, reversible write, irreversible write.
4. Add trust-boundary upgrades where the effect leaves the local context.
5. Record each row and its rationale in the design document.
6. Set the deploy-time default for newly arrived tools to the strictest tier.

## Anti-patterns

- Classifying by expected frequency of the action rather than irreversibility of it.
- One list of "safe tools" never revisited as the manifest evolves.
- Classifying based on the model's stated intent ("it only calls this to summarise").
- Reading the tool's marketing name as its effect.
- No tier for tools whose reversibility is unknown.

## Done checklist

- [ ] Every tool in the manifest has a tier assigned.
- [ ] The table carries rationale, not just labels.
- [ ] Trust-boundary upgrades applied for external effects.
- [ ] Newcomers default to the strictest tier.
- [ ] The table is dated and version-controlled with the manifest.
- [ ] Unknown reversibility produces a gated tier by default.

## Sources

- OWASP LLM Top 10, excessive-agency framing: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Idempotence and reversibility concepts: <https://en.wikipedia.org/wiki/Idempotence>
- AI risk framing: <https://www.nist.gov/itl/ai-risk-management-framework>
