---
name: recipe-pretty-pr
description: Create a Pretty PR from strong recipe evidence. Use after Cook retains recipe proof to verify proof quality, select reviewer-useful media, preserve the repository template, and package or upload PR evidence. Does not invent proof.
disable-model-invocation: true
maturity: experimental
---

# Pretty PR

Turn a completed recipe run into a PR that is fast and pleasant to review. Evidence quality comes first; formatting cannot rescue weak proof. Infer the adapter from the checkout.

Refs: `references/examples.md`. Repo overlay on install.

## Inputs

Whatever exists under the task dir: the root `recipe.json`, `recipe-resolution.json`, `resolved-recipes/`, `summary.json`, `trace.json`, artifact manifest, screenshots/videos/logs, and ACs. Runtime claims need harness verify artifacts.

## Evidence gate

Before packaging:

1. Run the task's locked `mm-harness help --json` and apply its quality bar.
2. Map every PR claim to executed recipe nodes and manifest-indexed evidence.
3. Open and inspect every selected screenshot or video. Keep only settled, legible, reviewer-useful media that visibly proves its claim.
4. Reject stale, contradictory, blank, obscured, duplicated, or merely decorative evidence.
5. If a material claim lacks proof, stop and name the recipe node or evidence capture that must be rerun. Do not package around the gap or rewrite the claim as proven. Captured visual proof awaiting a person's review may be packaged as a local draft with `awaiting-review` stated explicitly; leave the criterion and task unapproved.

## Rules

- Lead with what changed and why it matters. Link each artifact to the claim and separate proved behavior from gaps.
- Prefer a small ordered evidence set that tells the user journey over an exhaustive screenshot dump.
- The local packager does not host `before_after_pairs` yet. If the manifest contains comparisons, retain their run-qualified paths and covered claims, report that packaging gap and stop before packaging; do not infer pairs from filenames or claim the comparison images were packaged. Follow the manifest schema in `.agents/skills/mms-recipe-cook/references/dev-fix-bug.md#coverage-and-finish`.
- Runtime claim needs the complete Recipe v1 provenance set (`recipe.json`, resolution graph, resolved dependencies, `summary.json`, `trace.json`, and manifest); visual claims need screenshot/video paths or an explicit unproven gap.
- Blank/black PNG = missing visual proof unless alternate proof + gap called out. Label DOM-raster fallbacks.
- No long logs. No secrets. Never claim pass if the run did not complete.
- Never claim mobile/extension runtime proof without passing `mm-harness verify`.
- Local packaging requires retained recipe proof, its quality report, and a request for PR evidence or a PR description. It may precede Cook completion, including no-change or pending human review. Keep pending review explicit; a draft does not authorize publication.
- Creating a PR or changing its body requires Cook `mark complete` or `mark no-change`, any required human reviews, separate consent, and the generated `pr-package/pr-desc.md`. That file preserves the repository template. Never bypass it with a hand-written `gh pr create` or `gh pr edit` body.

## Package

```bash
.agents/skills/mms-recipe-pretty-pr/scripts/package-pr-evidence.js --task <task-dir>
```

- Requires nonempty `artifacts/pr-description.md` for dev/fixbug, or QA's `artifacts/report.html` and `artifacts/report-data.json`; legacy `artifacts/report.md` is still accepted.
- Requires a `pass` or `warn` verdict in `artifacts/recipe-quality.json` and at least one complete run validated through the task's locked harness, `mm-harness recipe-validate`. Packaging verifies the task's frozen harness receipt and never uses an `mm-harness` found on `PATH`.
- Missing proof or failed quality stops packaging with a named gap and no `pr-desc.md`. Rerunning removes the previous generated package so it cannot be mistaken for current proof. Comment targets may package failed quality with `--allow-fail`.
- Packaging does not replace claim review or visual inspection.

Writes `pr-package/`: `pr-desc.md`, manifest-indexed `runs/`, `images/`, `evidence.md` (QA instead keeps `report.html` and `report-data.json`), `recipe-quality.json`, optional checklist copy, `package-manifest.json`, `final-report.md`. Core is headless: screenshots are N/A and summary/trace/report/log/test artifacts carry proof.

For dev/fix-bug, packaging renders `artifacts/pr-body.md` with the task's locked harness, `mm-harness pr-body render <task> --out <task>/artifacts/pr-body.md --json`, then adds the evidence images and artifact index. It resolves that harness through Recipe Cook's `resolve-harness`, never a binary discovered on `PATH`. This requires mm-harness 0.92.21 or newer. Renderer failure, a status other than `ok`, invalid JSON or missing output stops packaging; never substitute authored prose. Keep the task's harness receipt and markers frozen. The renderer also accepts `--command <invocation>` to label the retained run log.

Repository identity must be an exact `github.com` MetaMask canonical remote or a GitHub fork with that canonical `upstream`. For a same-name GitHub fork without `upstream`, pass explicit `--adapter extension|mobile|core`; local paths and lookalike hosts are rejected.

Print: task path, `pr-package/`, `pr-desc.md`, images folder.

```md
### Recipe validation
Verdict: warn
Proved: ...
Artifacts: summary.json, trace.json, screenshots/...
Gaps: ...
```

## Upload / PR (opt-in)

Artifacts owner = `gh api user`. Images and QA HTML reports go to public `<owner>/mm-<adapter>-artifacts` at `evidence/<branch>/`; recordings stay in retained evidence. Headless Markdown-only tasks skip that public repo. **Ask before every outward step.** State that the repo is public and reports can embed screenshots containing wallet state.

```bash
S=.agents/skills/mms-recipe-pretty-pr/scripts/upload-pr-evidence.js
node "$S" --task <task-dir> --dry-run
node "$S" --task <task-dir> [--ensure-repo] --confirm-public-upload --create-pr [--pr <n>]
```

`--confirm-public-upload` is required for image and HTML uploads; `--create-pr` is required for PR body writes. `gh` writes with `GH_TOKEN` unset. Never ask the human to paste a token or secret.

## Evidence comment (QA, review-pr)

A PR-scoped QA or review task reports on someone else's PR through one comment, refreshed in place on reruns. QA uses `report-data.json` for a short verdict/summary and links the uploaded `report.html`; do not author a Markdown duplicate. Download the HTML to view its text and embedded screenshots; recordings remain in the retained evidence store. Legacy tasks still use `artifacts/report.md`, and `--body <markdown-file>` explicitly overrides the comment text. A failed verdict is the point of the comment, so package with `--allow-fail`. Same evidence gate: every cited claim maps to retained evidence, and standalone screenshots must be manifest-indexed. The HTML and its embedded screenshots are public uploads covered by the same consent flag. Release/daily reports remain local unless separately authorized for publication.

```bash
node .agents/skills/mms-recipe-pretty-pr/scripts/package-pr-evidence.js --task <task-dir> --allow-fail
node "$S" --task <task-dir> --target new-comment --pr <n> --dry-run
node "$S" --task <task-dir> --target new-comment --pr <n> --confirm-public-upload      # first post
node "$S" --task <task-dir> --target comment --comment <id> --confirm-public-upload   # refresh that comment
```
