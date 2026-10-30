# Optional recipe advice

Use the task's recorded harness throughout. The harness owns settings, precedence, provider selection and credential detection. Do not read configuration or secrets yourself, call a provider directly, or install a newer harness for this optional feature.

1. Run `mm-harness recipe-quality advisor-status --json`, forwarding the caller's explicit advisor options. Save its output as `<task>/artifacts/advisor-policy.json`. Recheck policy on resume so a current opt-out takes effect, but reuse existing assessments instead of making another request. Preserve a prior policy record when it changes. An unsupported command, disabled policy, missing key or configuration error leaves ordinary authoring available; record the reason and do not retry.
2. When status is `ready`, use only its listed `stages`. The default is `plan`. Copy the recorded acceptance criteria into `<task>/artifacts/advisor-task.json` using the installed command's task schema. Preserve supplied wording and any labels for assumptions or derived criteria.
3. Before drafting, if `plan` is enabled, call `recipe-quality plan --task <advisor-task.json> --adapter <adapter> --output <task>/artifacts/advisor-plan.json --json`. Pass the resolved policy back as `--advisor <provider> --advisor-model <model> --advisor-stages <comma-separated-stages>`. Redirect command stdout to a task-local file instead of loading the duplicate full artifact into context. Inspect a compact summary first, then read only the selected candidate contracts needed for authoring. Record accepted or rejected suggestions briefly in the recipe coverage notes; a suggested match does not establish a postcondition.
4. If explicitly enabled in the policy, `draft` permits one `recipe-quality advise` call on the statically valid recipe; `evidence` permits one such call with focused execution observations through `--evidence`. Keep outputs at `recipe-advice.json` and `evidence-advice.json` under task artifacts. Forward the same frozen policy and actual root parameters. Supply observed results for every claimed case; image filenames are not pixel proof.

Limit each enabled stage to one request per materialized task. Reuse existing results on resume. A materially revised task needs an explicit new assessment decision, not an automatic retry. Retain provider status, model, input/question hashes, usage and duration from the output, including skips or unavailability. Treat all suggestions as advice; validate and execute revised recipes normally. Advice cannot waive a gate, authorize app actions, supply missing evidence or replace canonical quality.

The execution environment can supply overrides. The same status command resolves them; the skill does not implement separate policy. `--advisor off` disables advice for this task even when the saved profile is enabled.

A compact planning summary preserves the outcome and accounting without repeating the catalog:

```bash
jq '{status, reason, provider, model, usage, durationMs, assessments: [.assessments[]? | {id, classification, ref: .candidate.ref, confidence}]}' <task>/artifacts/advisor-plan.json
```
