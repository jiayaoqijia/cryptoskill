---
name: rag-record
domain: prompt-engineering/rag-record
trigger: "Writing the record of a RAG system's design and measured failures."
anti_trigger: "Not for the pipeline itself, and not for index mechanics."
scope: "The written record: stage design, failure taxonomy, measured failures."
status: seedling
---

# RAG record

## Standard

The RAG record holds what a system needs to be judged and improved: the composition (stages, order, contracts), the failure taxonomy (misbinding, fabrication, conflation, retrieval failure, corpus silence), and the measured rates of each on dated samples. Without it, every incident becomes an argument about what the system was supposed to do; with it, the argument ends by pointing at a number and a stage.

Its second role is honest accounting of the trade-offs the design accepted: which question classes are fast-pathed, what verification coverage actually is (a sample rate is a coverage statement), and what the refusal threshold is this month. These are not constants of nature; they are decisions with dates, and the record keeps them visible so drift in the deployed system is detectable against the written one.

Primary sources: <https://osf.io/prereg/> and <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>.

The record also earns its place in incident review: when an answer fails publicly, the question is which stage failed and whether the class was known. A record that turns each incident into a lookup rather than a re-litigation is the difference between a system that improves and one that merely reboots.

## Decision rules

- The record contains composition, stage contracts, failure taxonomy, and measured rates, all dated.
- Failures are counted by class, not as one error rate; classes point at stages.
- Sampling and verification coverage are recorded as such: a sampled number that presents as total is a false claim.
- The refusal threshold and its change history are part of the record.
- Corpus coverage decisions — what was deliberately excluded — are recorded so silence is interpretable.
- Composition changes carry their measurements as amendments; the record is append-only.

## Procedure

1. Write the stage order and contracts at design time.
2. Define the failure taxonomy before the first measurement.
3. Measure each class on dated samples of real traffic.
4. Record sampling rates as coverage, never as totals.
5. Keep threshold changes with their grounds, dated.
6. Amend on composition or threshold changes; never overwrite.

## Anti-patterns

- One undifferentiated error number.
- A sampled measurement presented as total.
- No record of what the corpus deliberately excludes.
- Threshold history lost in the noise of redeploys.
- The record describing an older composition because changes were never written.

## Done checklist

- [ ] Composition and contracts recorded.
- [ ] Failure taxonomy dated before measurement.
- [ ] Class rates on dated samples.
- [ ] Coverage честly labelled.
- [ ] Threshold history kept.
- [ ] Append-only amendments.

## Sources

- Pre-registration practice for stated designs: <https://osf.io/prereg/>
- RAG architecture overview: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- What-is RAG: <https://aws.amazon.com/what-is/retrieval-augmented-generation/>
