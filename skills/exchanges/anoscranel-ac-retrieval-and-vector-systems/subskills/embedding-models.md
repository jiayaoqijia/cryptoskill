---
name: embedding-models
domain: software-engineering/embedding-models
trigger: "Choosing an embedding model and understanding what it commits you to."
anti_trigger: "Not for prompt design, and not for model training from scratch."
scope: "Dimensions, training domain, multilingual coverage, and re-embedding cost."
status: seedling
---

# Embedding models

## Standard

An embedding model maps text to a vector, and its choices are constraints rather than preferences. Dimensionality determines index size and query cost; the training domain determines what it represents well, so a model trained on general prose may perform poorly on code or on clinical text; and the tokenizer's maximum length determines how much of a chunk it actually sees, which can silently truncate.

The commitment that is easiest to overlook is the re-embedding cost. Changing the model means re-embedding the entire corpus, because vectors from two models are not comparable, and that cost scales with corpus size and with the rate limits of the embedding provider. The decision to change a model is therefore a migration project, and the record should state the corpus size and the estimated re-embed time before the change is proposed.

Primary sources: <https://huggingface.co/docs/transformers/> and <https://www.nist.gov/>.

## Decision rules

- Record the model, its version, and its dimensionality.
- Record the maximum input tokens and confirm chunks fit within it.
- Record the training domain and why it matches the corpus.
- Record the multilingual coverage where the corpus is not monolingual.
- Record the corpus size and the estimated re-embedding time and cost.
- Record whether the model is hosted or local, and the latency that implies.

## Procedure

1. Record the candidate models and their dimensions.
2. Compare maximum input length with the chunk size in use.
3. Assess domain fit against the corpus's actual content.
4. Estimate re-embedding cost at the current corpus size.
5. Record hosting choice and query latency.
6. Write the model decision with its migration cost.

## Anti-patterns

- Changing the model without re-embedding the corpus.
- Using a model whose input limit is shorter than the chunks.
- Choosing by benchmark score without testing on the actual corpus.
- Ignoring tokenizer differences when comparing models on token counts.
- Treating the model choice as reversible without cost.

## Done checklist

- [ ] Model and version recorded.
- [ ] Dimensionality recorded.
- [ ] Input limit compared with chunk size.
- [ ] Domain fit assessed.
- [ ] Re-embedding cost estimated.
- [ ] Hosting and latency recorded.

The tokenizer deserves a note of its own: two models can report the same chunk size in tokens while seeing different text, because their tokenizers segment differently, and a chunk that fits one model's limit can be truncated by another. Recording the tokenizer used to measure chunk length, rather than the count alone, is what makes the fit check meaningful.


## Sources

- Open model documentation: <https://huggingface.co/docs/transformers/>
- Evaluation methodology: <https://www.nist.gov/>
- Vector search guidance: <https://nlp.stanford.edu/IR-book/>
