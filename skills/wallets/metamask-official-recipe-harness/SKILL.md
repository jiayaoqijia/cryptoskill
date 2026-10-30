---
name: recipe-harness
description: Operate mm-harness in one isolated MetaMask checkout. Use for runtime preparation, action or recipe execution, diagnostics, and evidence collection; the installed CLI owns version-specific recipe authoring guidance.
disable-model-invocation: true
maturity: experimental
---

# Recipe Harness

Use only `mm-harness`. Recipe Cook owns task routing and checklist policy. This skill adds the MetaMask checkout and runtime boundary.

## Read the installed contract

From the target checkout, run:

```bash
mm-harness help --json
```

The returned harness version, Recipe Protocol version, adapter, authoring method, quality bar, drift recovery, and discovery commands are authoritative for that installed binary. Follow them instead of recalling recipe fields, copying skill prose, or inventing commands. The canonical protocol remains Recipe Protocol v1: https://farmslot.io/docs/reference/recipe-protocol-v1/.

## Prepare one sandbox

1. Run `mm-harness doctor --fix --json` in this checkout. It may repair harness-owned runtime state, but it must not choose credentials, a wallet, or another checkout.
2. If doctor reports a wallet-fixture choice, relay its exact numbered options and end the turn. Never request or pass an SRP, private key, or password in chat or CLI arguments.
3. After the operator chooses, run only the printed fixture command, rerun doctor, then follow `status` into launch or reuse. Use `launch --verify`; add `--build` only when doctor requires it. Core is headless and uses `verify`.
4. Require the final result to identify only this checkout's device or browser profile, ports, fixture, runtime owner, and artifact directory. Never borrow another checkout.

Run one checkout operation at a time. If a job is backgrounded, wait for that job. If its handle is lost, wait for the PID recorded in `temp/recipe/runtime/sandbox.lock`; do not probe with a competing harness command. A bounded failure stops the loop.

## Execution boundaries

- Use the task's provenance-locked harness when Recipe Cook or Release QA created one. Do not replace it with a PATH binary mid-task.
- When no catalog action can observe an AC, write a task action under a new name, modeled on a library action (`actions --action <name> --json` shows its `sourceManifest`) but self-contained (node built-ins, plus any helper copied next to it): keep its manifest in `<task>/artifacts/task-actions/manifests/` and its script in the sibling `<task>/artifacts/task-actions/actions/`, pass `--action-manifest <manifest>` to every harness `actions`, `run --plan`, `run` and `call`, and flag it in the report as a library candidate. A missing fixture or runtime capability is still a named blocker, never a hidden state mutation.
- Final evidence comes from the run's printed artifact directory. Require the root recipe, resolution graph and dependency recipes, summary, trace, artifact manifest, and claimed evidence.
- Review `sideFindings` and `diagnostics.json` as non-blocking leads. They do not establish a product failure or its cause.
- Keep secrets out of recipes, commands, reports, and evidence.

Read `references/evidence-package.md` only when a task needs the optional evidence-package layout.
