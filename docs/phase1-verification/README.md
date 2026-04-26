# Phase 1 Verification

This directory holds the hand-labeled verification material for the
capability extractor (`scripts/extract-capabilities.py`). The protocol is
defined in `docs/TRUST.md` §"Phase 1 verification protocol".

## Files

- `holdout-v0.yaml` — The frozen 200-skill stratified holdout for
  extractor major version `0.x`. Each entry has the human label set
  (filled blind to the extractor output) and the reviewer's Sigstore
  identity. Precision/recall are computed against this holdout.
- `precision-recall.md` — Latest per-capability precision and Wilson
  95% lower-bound recall; regenerated each time the extractor changes.
- `compute-precision-recall.py` — Computes the table in
  `precision-recall.md` from `holdout-v0.yaml` and the current
  `docs/capabilities.json`.

## Holdout policy (TRUST.md §Verification)

The holdout is **frozen at the start of each extractor major version**.
The same set is reused across patch releases so the recall measurement
is comparable across runs. A new holdout is generated only when the
extractor's major version increments (e.g., 0.x → 1.x). Reviewers sign
their forms with Sigstore keyless.

The 200-skill sample is stratified by category × predicted execution
mode. The 20-skill stratified sample described in TRUST.md is a subset
used for the precision pass; the full 200 is used to compute Wilson
95% lower-bound recall on the critical-subset capabilities.

## Status

- [ ] holdout-v0.yaml hand-labelled (currently a template; reviewers
      assigned)
- [ ] At least one polymorphic skill (Heurist Mesh) included in the
      stratified sample
- [ ] Reviewer signatures attached
