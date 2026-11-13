---
name: context-selection
domain: collaboration/context-selection
trigger: "What should I pass on; how much context does the next reader need; trim this handoff; the summary is too long or too thin; what does the next agent get"
anti_trigger: "Copying constraints through compression (subskills/constraints-verbatim.md); verifying state on the receiving end (subskills/resumption-check.md); the artifact's section list (subskills/handoff-artifact.md)"
scope: "What to pass and what to leave: relevance filter, outcomes over transcripts, size budgets; the handoff tax and how it reverses with direction"
status: "seedling"
---

# Context Selection

## Standard

- **Ganz et al., "The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents" (2026), arXiv:2608.24358**: switching models mid-task costs quality. Full-trajectory escalation recovered less than half of the weak-to-strong quality gap while costing much more. The preferred transfer reverses with direction: passing less of the outgoing trajectory improved escalation quality, while removing the stronger model's trajectory reduced downshift quality. <https://arxiv.org/abs/2608.24358>
- **Sun et al., "When Must Becomes Maybe" (2026), arXiv:2608.24569**: intermediate records carry tasks forward but can erode established judgments; what compresses badly is risk, not volume. <https://arxiv.org/abs/2608.24569>
- **Google SRE Book, "Being On-Call"**: the on-call engineer passes a working summary of live items at shift change, not the shift's full log. <https://sre.google/sre-book/being-on-call/>
- House line: pass outcomes and decisions, not the road taken to reach them.

## Decision rules

1. Pass the answer, the state, and the constraints; leave the search path unless a dead end must not be repeated.
2. Escalating to a stronger receiver: pass less of the outgoing trajectory; outcomes, constraints, and pointers carry the weight.
3. Downshifting to a weaker receiver: pass more; keep the worked reasoning, because the receiver has less capacity to re-derive it.
4. One screen is the default budget for the capsule; anything larger goes behind a pointer.
5. Every passed claim must be checkable against some artifact; unverifiable narrative is noise.
6. When in doubt, pass the pointer, not the content; a pointer is cheap, a re-read is not.
7. Write what was deliberately left out; the receiver must tell a closed door from an unwritten one.

## Procedure

1. List the candidate items: files, transcripts, decisions, constraints, logs, dead ends.
2. Classify each: outcome (keep), constraint (keep verbatim), decision (keep one line), pointer (keep), noise (drop).
3. Cut each kept item to its smallest checkable form.
4. Set the budget: capsule within one screen; everything else behind a live pointer.
5. Read the direction of the handoff. Escalation: drop trajectory beyond outcomes and constraints. Downshift: keep the reasoning that produced them.
6. Write the omission note: what was dropped and why.
7. Test: can the receiver continue without asking for one more file? If not, add its pointer and retest.

## Anti-patterns

- **Transcript paste.** Buries the few lines that matter. Fix: capsule plus pointer.
- **Over-compression on escalation.** "Continue as before" and nothing else. Fix: outcomes and constraints travel on every hop.
- **Under-passing on downshift.** Assuming a weaker receiver will re-derive what was cut. Fix: more reasoning travels, not less.
- **Just-in-case hoarding.** Everything is passed so nobody had to decide. Fix: apply the filter; drop noise on purpose.
- **Silent omission.** The receiver cannot tell dropped from never-happened. Fix: the omission note.

## Done checklist

- [ ] Every candidate classified; kept items cut to smallest checkable form.
- [ ] Constraints travel verbatim.
- [ ] Direction applied: less on escalation, more on downshift.
- [ ] Capsule within budget; the rest behind live pointers.
- [ ] Omission note written.

## Sources

- Ganz et al., "The Handoff Tax" (2026), arXiv:2608.24358: <https://arxiv.org/abs/2608.24358>
- Sun et al., "When Must Becomes Maybe" (2026), arXiv:2608.24569: <https://arxiv.org/abs/2608.24569>
- Google SRE Book, "Being On-Call": <https://sre.google/sre-book/being-on-call/>

⚠️ The handoff-tax numbers come from coding-agent experiments with specific model pairs; treat them as evidence of direction and mechanism, not as universal constants.
