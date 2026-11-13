---
name: media-pipeline-record
domain: software-engineering/media-pipeline-record
trigger: "Writing the record of a media pipeline and its derivative recipes."
anti_trigger: "Not for capacity reports, and not for delivery monitoring."
scope: "The written record: source→derivative inventory, transcode parameters, errors and retries, cold-storage and retention policy."
status: seedling
---

# Media pipeline record

## Standard

The media pipeline record is the single place where each pipeline's design and history are inspectable: the media families and their derivative recipes (with versions and the browser-support snapshot dates that justified their format choices), the storage and retention policies for sources and derivatives, the queue and processing SLAs, and the error taxonomy for failed jobs. Media pipelines are slow to build and slower to change, and without the record the pipeline becomes folklore — knowledge that lives in the encoder flags of a departed engineer.

The record earns its existence when something regresses. A video that used to transcode in four minutes now takes twenty — the record's per-rung cost history answers whether the source mix changed, the encoder was silently re-versioned, or the ladder grew. A derivative set that used to fit in cold storage now does not — the recipe versions and their measured sizes answer whether AVIF was added, whether retention was silently extended, or whether orphaned derivatives from a dead feature still exist. Without the record, the investigation begins with guesswork about a pipeline that may no longer be reproducible.

## Decision rules

- The record holds: media families, derivative recipes with version history, storage and retention policy, queue SLAs, and the error taxonomy.
- Each recipe version carries its support-matrix snapshot date and its reason for existence.
- Per-rung cost (transcode time, storage) is recorded per recipe, so regressions are attributable.
- Error taxonomy covers verification, transcode, and packaging failures with their failure classes.
- Retention policy distinguishes source lifecycle (hot, cold, archived) from derivative lifecycle.
- The record is append-only; changes to recipes bump versions and add entries, not overwrite.


## Procedure

1. Write the record when the pipeline is designed, before the first production source flows through it.
2. Capture per-family recipes, versions, format rationale, and support-matrix snapshot dates.
3. Record measured per-rung costs (transcode time, storage) per recipe version.
4. Define the error taxonomy (verification/transcode/packaging) and map observed failures to it.
5. State the retention policy: source hot/cold/archival tiers, derivative expiry rules.
6. Review on schedule and on regressions: the record is the first diagnostic input.

## Anti-patterns

- No record: recipes live in tooling code and are reconstructed from the git history of a config file.
- Recording only successes; failures are where the pipeline's actual failure modes live.
- Overwriting recipe history so regressions cannot be attributed to a change.
- Retention kept as implicit practice rather than stated policy.

## Done checklist

- [ ] Record written at design time, before first production flow.
- [ ] Recipes versioned with support-matrix snapshot dates.
- [ ] Per-rung costs measured and recorded per version.
- [ ] Error taxonomy defined; failures mapped to classes.
- [ ] Retention policy stated for sources and derivatives separately.
- [ ] Append-only; changes bump versions.

## Sources

- MDN web video codec guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs>
- MDN image file type and format guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types>
