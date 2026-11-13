---
name: loop-composition
domain: prompt-engineering/loop-composition
trigger: "Ordering the RAG stages and choosing what each may depend on."
anti_trigger: "Not for index mechanics, and not for prompt writing."
scope: "Ordering the stages and choosing what each may depend on."
status: seedling
---

# Loop composition

## Standard

A RAG pipeline is an ordered set of stages — transform, retrieve, (sometimes) hop, generate, cite, verify, refuse or answer — and the order is a design with consequences. Retrieval before decomposition serves single-hop questions cheaply and multi-hop questions badly. Verification before citation rendering catches misbinding at the cost of a second pass. Every ordering makes some question classes cheap and others expensive, and the composition is honest when its chosen order is written down with the classes it favours.

The dependency question is the second half of composition: what may each stage see? The generator sees the passages and the identifiers; the verifier sees the answer and the same passages; the refusal threshold sees the retrieval scores, not the passages. Stating the inputs of each stage is stating its contract, and a stage whose inputs are implicit will quietly receive what it should not.

Primary sources: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> and <https://aws.amazon.com/what-is/retrieval-augmented-generation/>.

## Decision rules

- Publish the stage order with the question classes each order favours.
- State each stage's inputs and outputs; an implicit input becomes a silent coupling.
- Fast-path single-hop questions around expensive stages; the cost model, not hope, decides this.
- Every optional stage — verification, decomposition — has a stated routing condition.
- Latency budget is allocated per stage at design time and measured per stage in production.
- Composition changes are recorded with the question-class measurements that justified them.

## Procedure

1. List the stages and the candidate orders.
2. State each stage's inputs and outputs as a contract.
3. Choose routing conditions for optional stages per question class.
4. Allocate the latency budget per stage.
5. Measure per-stage latency and quality on real traffic.
6. Record the composition and every later change with its measurements.

## Anti-patterns

- A pipeline diagram nobody can match to the deployed order.
- Stage inputs taken from ambient context rather than a contract.
- Every question paying for every stage.
- An optional stage that always runs because its routing condition was never written.
- Composition changes justified by anecdotes rather than class measurements.

## Done checklist

- [ ] Order published with favoured classes.
- [ ] Stage contracts stated.
- [ ] Fast-path routing per class.
- [ ] Optional stages have routing conditions.
- [ ] Per-stage latency measured.
- [ ] Changes recorded with measurements.

## Sources

- RAG architecture overview: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- What-is RAG: <https://aws.amazon.com/what-is/retrieval-augmented-generation/>
- Original RAG paper: <https://arxiv.org/abs/2005.11401>
