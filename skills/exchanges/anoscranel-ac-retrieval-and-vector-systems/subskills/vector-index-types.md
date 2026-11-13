---
name: vector-index-types
domain: software-engineering/vector-index-types
trigger: "Choosing a vector index and the recall it trades away."
anti_trigger: "Not for database B-tree design, and not for embedding model choice."
scope: "Flat, IVF, HNSW, and the recall-latency-memory trade each makes."
status: seedling
---

# Vector index types

## Standard

Exact nearest-neighbour search compares the query against every vector, which is perfectly accurate and linear in corpus size. Approximate indexes give up a little accuracy to gain a great deal of speed, and each family gives it up differently: a partitioned index narrows the search to a few clusters and misses results in the clusters it skipped, while a graph index walks a neighbourhood and can miss results the graph does not connect.

The parameter that matters is recall at the operating point. Every approximate index has knobs that trade recall for latency, and the honest approach is to measure recall against exact search on a sample, then choose the parameters that meet a stated recall target at an acceptable latency. Recording only the latency is recording half the trade.

Primary sources: <https://nlp.stanford.edu/IR-book/> and <https://www.nist.gov/>.

## Decision rules

- Record the index type and the parameters in use.
- Record the measured recall against exact search on a fixed sample.
- Record the latency at the operating point, at a stated percentile.
- Record the memory footprint, which differs by orders of magnitude between types.
- Record the rebuild and update behaviour, since some indexes degrade with inserts.
- Record the recall target and who set it, since it is a product decision.

## Procedure

1. Record the index type and its parameter values.
2. Build a fixed sample of queries with known exact results.
3. Measure recall at the operating parameters.
4. Record latency at a stated percentile.
5. Record memory and update behaviour.
6. Write the choice with its recall target and measured result.

## Anti-patterns

- Reporting latency without recall.
- Tuning parameters on the production index and calling the result a measurement.
- Assuming recall measured on one corpus transfers to another.
- Ignoring memory, which often binds before latency does.
- Choosing an index that degrades badly under continuous inserts.

## Done checklist

- [ ] Index type and parameters recorded.
- [ ] Recall measured against exact search.
- [ ] Latency recorded at a percentile.
- [ ] Memory recorded.
- [ ] Update behaviour recorded.
- [ ] Recall target recorded.

The comparison should be made on the deployed corpus rather than a public benchmark: recall at a given parameter setting depends on the data's clustering and dimensionality, so a configuration that achieves the target on a standard set can miss it on a corpus with different structure, and the measurement has to be local to be meaningful.


## Sources

- Information retrieval foundations: <https://nlp.stanford.edu/IR-book/>
- Benchmark and measurement guidance: <https://www.nist.gov/>
- Vector search documentation: <https://huggingface.co/docs/transformers/>
