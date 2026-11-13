---
name: preparation-and-caching
domain: prompt-engineering/preparation-and-caching
trigger: "Doing free local work before spending a metered request."
anti_trigger: "Not for infrastructure caching tiers, and not for retrieval systems."
scope: "Reading local and computing cheaply before spending a request."
status: seedling
---

# Preparation and caching

## Standard

Under a request cap, every operation that happens off the API is free, and the set of such operations is larger than habit suggests. Local reads — files, notes, earlier responses in the ledger — answer many would-be questions without any request. Local computation — arithmetic, dates, string manipulation, deduplication — prepares the request so it arrives already distilled. Local decisions — which sub-questions are genuinely distinct, which material is load-bearing — prevent the wasted request that a vague one would have made.

Caching in this context is the ledger itself: yesterday's responses stored with their questions, so a repeated or near-repeated question is served from disk instead of re-asked. The reuse test is similarity of need, not literal string match: if the earlier answer covered the ground, pointing the new task at it costs nothing, and a small local restatement replaces a new round trip.

Primary sources: <https://12factor.net/> and <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>.

## Decision rules

- Before any request, check the ledger for an answer covering the same ground.
- Read local files and notes first; ask only what they cannot supply.
- Compute locally what can be computed: arithmetic, dates, sorting, deduplication.
- Distill the request material locally so the request carries conclusions, not raw volume where conclusions suffice.
- Record each response in the ledger with the question and the pack list for future reuse.
- Track how many would-be requests were served from ledger or files; that count is the preparation dividend.

## Procedure

1. Write the task down and search the ledger and files before composing anything.
2. Extract what local reads and prior responses already answer.
3. Compute locally every part that is mechanical.
4. Compose the request from the residue only.
5. On response, store question, pack list, and answer in the ledger.
6. At session end, count ledger-served versus request-served needs.

## Anti-patterns

- Asking a question that a stored earlier answer already covers.
- Sending raw material for the model to sort when local tools sort it.
- Spending a request on arithmetic the requester could do.
- A ledger that stores responses without the questions that got them.
- Rebuilding a context that already exists on the desk.

## Done checklist

- [ ] Ledger and local files checked first.
- [ ] Local answers extracted before composing.
- [ ] Mechanical computation done locally.
- [ ] Request carries only the residue.
- [ ] Response + question + pack logged.
- [ ] Preparation dividend counted at session end.

## Sources

- The twelve-factor app: <https://12factor.net/>
- Prompt engineering guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>
- Batch processing guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/batch-processing>
