# QA report presentation

Produce one human `report.html` using [rendering instructions](html-report.md), [example data](report-example.json) and the [HTML reference](report-example.html). These examples are illustrative, not proof. Keep Cook's recorded verdicts and machine artifacts authoritative; do not author a Markdown duplicate.

Lead with a short PM summary, selected-plan results, product findings and next actions. Show full-AC coverage separately. Keep readable source titles, reproduction steps and proof beside each selected check. Tool diagnostics belong in the retrospective unless they affect confidence in a result. Preserve failed attempts and unexplained failures even when a rerun passes.

## Adapt the report to its scope and audience

| Scope | Adaptation | Output destination |
|---|---|---|
| PR | Identify the PR and frozen head. Preserve the team's proposed-reply format and Cook's review recommendation. Keep source-review findings separate from runtime verdicts | Local report and proposed reply; publish a comment only when authorized |
| Daily / time range | State explicit boundaries, timezone, selection semantics, shared dependencies and exclusions. Make interaction checks distinguishable from individual feature checks | Local report and retained evidence |
| Release | State release identifier, baseline and target SHAs, and actual artifact identity. Say whether the tested app is a branch build or the release ZIP; branch proof does not certify the ZIP | Local report and retained evidence |
| Single ref / regression | Identify the exact build and domain-plan criteria without inventing a change inventory | Local report and retained evidence |

The report uses the same evidence for PM and engineering readers. Collapse unselected detail and diagnostics without hiding failures or selected-plan gaps. The scope/build section identifies source-dev versus release artifact, platform, fixture and library/harness revisions. Video and screenshots need clear target attribution and observation limits.

Sharing must preserve provenance and state which media require access to retained artifacts. Report completion, execution closure and release approval are separate. Do not claim publication or a completed handoff without confirmation.
