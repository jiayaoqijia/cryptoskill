---
name: batching-sub-questions
domain: prompt-engineering/batching-sub-questions
trigger: "Asking in one packed request what would otherwise be many separate calls."
anti_trigger: "Not for prompt style alone, and not for batching-as-an-API-feature."
scope: "Asking in one packed request what would otherwise be ten calls."
status: seedling
---

# Batching sub-questions

## Standard

Most real questions arrive as clusters: a document raises five doubts, a plan needs three risks and two counter-examples, a comparison has four dimensions. The default habit asks each sub-question as its own request — one call per doubt — which under a request cap multiplies cost linearly and, worse, forfeits the shared context: the answer to sub-question three depends on what sub-question one established, and separate calls cannot see each other.

Batching puts the sub-questions and their context into a single numbered request and asks for a numbered set of answers. One request replaces ten; the sequence runs at the speed of one round trip; and the answers are consistent because one context produced them. The craft is in the decomposition before the call: sub-questions must be genuinely distinct, stated crisply, and ordered so the responder can hold them all.

Primary sources: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering> and <https://12factor.net/>.

## Decision rules

- Decompose first on paper, then batch: distinct sub-questions, one line each, numbered.
- Cap the batch at what one response can deliver well; split only on that evidence, not habit.
- State the shared context once at the top rather than repeating it per sub-question.
- Ask for answers keyed to the numbering, so the output is checkably complete.
- Mark each sub-question with its acceptable answer form: a fact, a list, a judgement.
- Keep the dependency order inside the batch: a sub-question that needs another's answer sits after it.

## Procedure

1. List every sub-question the task actually needs, without trimming for request count yet.
2. Remove duplicates and merge near-variants into single sharper sub-questions.
3. Order them so independent ones come first and dependent ones follow.
4. Write the shared context block once, above the numbered list.
5. Add the output contract: numbered answers, the form of each, and no omissions.
6. Send as one request; store the batch with its answers in the ledger.

## Anti-patterns

- Batching questions that each need different context into one call.
- A batch so large that answers thin out and completeness cannot be checked.
- Trimming decomposition to fit a comfortable request length rather than the task's real shape.
- Unnumbered free-form prompts that make missing answers invisible.
- Re-sending a batch because one sub-answer was weak instead of a targeted follow-up.

## Done checklist

- [ ] Sub-questions distinct, numbered, one line each.
- [ ] Duplicates merged before batching.
- [ ] Shared context stated once.
- [ ] Dependency order respected.
- [ ] Output contract with numbered answers stated.
- [ ] Batch and answers stored in the ledger.

## Sources

- Prompt engineering guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>
- Batch processing guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/batch-processing>
- The twelve-factor app: <https://12factor.net/>
