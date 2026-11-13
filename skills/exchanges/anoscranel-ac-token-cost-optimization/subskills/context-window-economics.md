---
name: context-window-economics
domain: prompt-engineering/context-window-economics
trigger: "Deciding what earns a place in the context window."
anti_trigger: "Not for packing techniques, and not for retrieval mechanics."
scope: "Input-token dominance: what context earns its place."
status: seedling
---

# Context window economics

## Standard

Input tokens are the quiet majority of most real workloads. A large instruction block, a reference document, and a conversation history all bill on every single request unless cached — and even the cached rate is nonzero. The context decision is therefore an economic one: every candidate piece of context must earn its recurring cost by changing outcomes, and the unit of judgment is dollars per task, not tokens per request.

The recurring framing is what makes this different from a single-request view. A 20-thousand-token reference appended to every request is not a one-time cost; it is a subscription, billed at the input or cached rate on every call that carries it. The test is whether the subscription pays: does the document measurably change the answers, and could a cheaper mechanism — retrieval, caching, selection — deliver the same change for fewer billed tokens.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/pricing> and <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>.

## Decision rules

- Inventory context components and classify each as static, semi-static, or per-request.
- Multiplying a component's token count by the number of requests carrying it.
- Charge static bulk to the cache — that is what the prefix arrangement is for.
- Question any per-request inclusion: does it change the outcome measurably?
- Prefer a smaller always-present core plus selective context over a maximal fixed prompt.
- Re-audit the prompt periodically; context accretes quietly and bills silently.

## Procedure

1. Decompose the prompt into its billed components.
2. Classify by stability: static, semi-static, volatile.
3. Multiply each component's tokens by the request volume carrying it.
4. Position stable bulk for the prefix cache.
5. A/B the volatile candidates: with and without, and measure the difference.
6. Cut the context whose removal does not change outcomes; record the cut.

## Anti-patterns

- "More context is better" as a policy — every token bills on every call.
- Appending wads of raw output without extract/select first.
- Counting tokens per request while ignoring request volume.
- The maximal prompt as a copy-paste default for new tasks.
- Auditing context once and never re-auditing.

## Done checklist

- [ ] Components inventoried with stability classes.
- [ ] Recurring cost computed for each.
- [ ] Static bulk on the cached prefix.
- [ ] Outcomes compared with and without borderline candidates.
- [ ] Zero-effect context cut and recorded.
- [ ] Prompt re-audit scheduled.

## Sources

- Pricing basis: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- Cache arrangements: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>
- Cache discounting: <https://platform.openai.com/docs/guides/prompt-caching>
