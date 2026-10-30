# Human HTML report

Use [report-example.html](report-example.html) for layout and [report-example.json](report-example.json) for renderer input. Both are illustrative, not proof. Render one human `report.html` from structured evidence. Do not author `qa-report.md` or `report.md` duplicates. Keep machine proof, raw harness execution artifacts and historical reports intact.

Save `artifacts/report-data.json`, then render:

```sh
node <installed-recipe-qa>/scripts/render-report.mjs --input <task>/artifacts/report-data.json --out <task>/artifacts/report.html --assets <task>/artifacts
```

The renderer rewrites `artifacts/pr-verdicts.json`; never edit it. Update `report-data.json` and re-render. Read rollups only when `generatedFrom` matches the current input digest.

For an authorized PR comment, Recipe Pretty PR packages this HTML and uses the same `report-data.json` to generate a short comment with the recorded verdict and summary. Its explicit public-upload step hosts the full HTML with embedded screenshots and links it from the comment. Do not create `report.md` for publishing; recordings remain in retained evidence. Daily and release reports stay local unless separately authorized.

- `testedBuild: {name, version, branch, commit}` identifies the actual tested checkout in the header. Capture `name` and `version` from its `package.json`, branch from `git branch --show-current` and full HEAD from `git rev-parse HEAD` after setup and before proof. Label a detached checkout `detached HEAD`; never infer identity from a directory, requested ref or report title. Retain the readback with runtime evidence and verify the running app matches that source or official artifact. Historical reports without this record show an explicit missing-identity caption.
- `sources` maps a stable `id` to a human title, label and source URL. Use PR titles and canonical PR links for authored changes; name domain smoke and derived integration checks separately. Do not make readers decode criterion IDs to find a PR.
- `criteria` keeps each frozen `text`, `id`, `sourceId`, recorded `verdict` (`PASS`, `FAIL`, `UNTESTABLE`) and `detail` describing the proved boundary or missing proof. For new `UNTESTABLE` rows, set `coverageState` to `not-run`, `incomplete-evidence` or `blocked`; blocked rows also require `blockerEvidence` entries pointing to the observed prerequisite/capability failure. Historical rows with no recorded cause may omit `coverageState` and display as Not proved. `title` may provide a short readable label without replacing the full text. Evidence entries have a readable `label`, optional `url` (an `https` or `http` link, or a plain, unencoded path relative to the artifact directory; such a path resolves only beside the exported HTML, not in a hosted copy of the HTML alone) and observation-limit `note`.
- Expand criteria by default. Show each source's status and proved/total count in both the contents and its section: fully validated only when all listed criteria pass; partially validated when some pass; not validated when none are proved; failure found when any criterion fails. Color accompanies these labels, never replaces them.
- Do not use “untestable” as shorthand for “not attempted.” For each unproved criterion distinguish not run, incomplete evidence, and a concrete blocker. Record the failed prerequisite or attempted operation for a blocker. Missing recipe coverage alone does not make a basic interaction impossible to test. Legacy `UNTESTABLE` records display as “Not proved” with their original value preserved in the details; do not invent a cause after the run.

An allowed, obtainable prerequisite belongs in execution setup. For example, a duplicate-submit criterion may need a task-owned test position and two input events close together. Under existing testnet authority, attempt the bounded setup and discover the supported input primitive. Prove the temporal input and the single resulting submission with executable evidence; a recording of the final state alone is insufficient. If the primitive, fixture or observation is unavailable, record the actual check and failure. “Needs a position” is a test plan, not an observed blocker. If the run stops for time or scope budget before attempting it, report that as not run.
- `images` contains retained PNG/JPEG `path`s relative to the artifact directory, a precise `caption`, and `criterionIds`. The renderer embeds images beside their criteria. Captions say what the image proves and what still needs a trace or recording. Never fabricate or substitute an image from another attempt.
- `videos` contains retained media `path`, `caption`, and `criterionIds`. Reference the runtime's `timelinePath` and selected `markers: [{traceIndex, label, criterionIds}]` to derive proof links without hand-authoring timestamps. The renderer uses the locked protocol from `harness-provenance.json` and verifies the video/trace digests. Export the relative media files beside the HTML for offline playback; the HTML alone retains its text and embedded screenshots, not the video bytes. A marker identifies action time, not guaranteed captured pixels; retain proof screenshots and state/log evidence separately.
- Include findings, next steps, frozen scope/build metadata and source artifact digests in provenance. For a report rendered after execution, identify it as a presentation export; do not imply another validation ran.

Reuse node intent and proof IDs already sent to the recipe HUD. The runtime derives
video markers; the agent selects useful evidence references rather than narrating
every action or estimating timestamps. Prefer capture-helper's concurrent recording
and snapshot support when the selected target supports it. Declare fallback recorder
identity and gaps. A snapshot without confirmed encoded-frame correspondence remains
independent screenshot evidence.

The renderer derives counts from the recorded criterion verdicts. It does not run QA, finalize proof or change a verdict. Unknown causes remain unknown. Do not turn missing evidence into a product failure or PASS.

`plan` optionally records `level`, `evidence: {label, url?}`, `selectedCriterionIds`, and `exclusions: [{criterionId, reason}]` from the retained pre-execution plan. Every inventoried criterion must appear exactly once across selection and exclusions. Omit `plan` for historical runs without recorded selection; never reconstruct it from passing cases. Selected checks expand by default; excluded detail stays accessible in collapsed sections. Show selected-plan results separately from full acceptance coverage. A smart daily/release smoke can finish its chosen checks without re-proving every detailed AC. Mark deliberately omitted detail “Outside this run's plan” with its pre-execution selection rationale. Keep “Not run” for a selected check that was not attempted and “Blocked” for an observed unavailable prerequisite. Never retroactively rename abandoned planned checks as intentional exclusions to improve the result. Prior PR proof may justify prioritization but does not become current-build proof.

Keep scripts and external dependencies out of the HTML. Native details and CSS filters provide contents navigation, collapsible proof sections and verdict filtering in the exported report. Embed report text and screenshots. Identify any unbundled videos/traces, and state when links require the recipient's own access. A self-contained report is not automatically a complete portable evidence bundle.

End with an explicit handoff: review findings, close completed execution with its recorded result, or schedule fresh proof for gaps. Closing or reviewing a PARTIAL report is not release approval. Describe only controls actually available in the caller; do not claim a run was closed or an issue published without confirmation.

Keep the quick navigation visible at the top while scrolling, with Summary, Findings, Contents, a change jump list and Next steps. This belongs in the exported report; maximize/restore belongs to the host artifact viewer and applies to all artifact types.
