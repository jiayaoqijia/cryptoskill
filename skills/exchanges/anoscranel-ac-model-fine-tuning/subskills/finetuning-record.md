---
name: finetuning-record
domain: software-engineering/finetuning-record
trigger: "Writing the record of a fine-tuning decision, run, and outcome."
anti_trigger: "Not for recommending a method, and not for the Serving-plan record alone."
scope: "The written record: data version, recipe, metrics, and what failed."
status: seedling
---

# Fine-tuning record

## Standard

The record reconstructs the run: the decision evidence (baseline prompting failures, data inventory), the exact recipe (recipe hyperparameters, library versions, base-model revision, adapter configuration), the full metric curves, the chosen checkpoint, the outcome on deployment probes, and the failed runs that did not ship. Every run is a layer with a date, and negative results are preserved with the same care as positive ones — a failed-rank experiment is the evidence that stops the next team from repeating it.

The record's second job is lineage: the deployed model traces to one adapter version, one data version, one base-model revision, one evaluation set per set version. Orphan artifacts — undeployed adapters, unreproducible runs — are the failure this record exists to prevent; when the base model updates next quarter, the record is what tells which fine-tunes are invalidated.

Primary sources: <https://osf.io/prereg/> and <https://huggingface.co/docs/transformers/training>.

## Decision rules

- Record the decision first: baseline failures, data inventory, and the evidence that met the stated threshold.
- Version the recipe fully: hyperparameters, library versions, base revision, adapter config.
- Preserve every run layer: metrics positive or negative, dated, no silent deletions.
- Tie the deployed artifact to its full lineage: adapter, data, base, eval sets.
- State the base-update policy and the canary protection watching for it.
- Amend, never rewrite: post-hoc findings append with the date.

## Procedure

1. Record the original decision evidence and data version.
2. Record the recipe, including versions at the time of run.
3. Append each run's metrics with its date and verdict.
4. Record the chosen artifact with full lineage.
5. Stare the failed runs into the record — they are the next session's savings.
6. After every base-model change, reconcile the registry with a dated line.

## Anti-patterns

- Keeping only the winning run and discarding the failed ones.
- Records without library versions — next quarter's repro fails silently.
- Deployed adapters with no data-version lineage.
- Rewriting history rather than appending amendments.
- No base-update policy: silent drift with no record of which fine-tunes broke.

## Done checklist

- [ ] Decision evidence and data version recorded.
- [ ] Recipe versioned with libraries.
- [ ] Run layers all present, positive and negative.
- [ ] Deployed artifact lineage complete.
- [ ] Failed runs preserved.
- [ ] Base-update reconciliation dated.

## Sources

- Pre-registration practice for stated decisions: <https://osf.io/prereg/>
- Training docs, reproducibility details: <https://huggingface.co/docs/transformers/training>
- TRL, versioned training routines: <https://huggingface.co/docs/trl/index>
