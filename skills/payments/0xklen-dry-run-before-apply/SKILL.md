---
name: dry-run-before-apply
description: Use when a tool supports a planning or no-op mode and the change touches shared or hard-to-reverse state. Runs the plan, reads it against intent, then applies only what was previewed.
---

# Dry Run Before Apply

A preview is cheaper than a mistake. Run the tool's no-op mode, read the plan against what you intended, and apply only the diff you actually approved.

## Procedure

1. Find the dry-run flag before assuming there is one: `man <tool>` / `<tool> --help | grep -i -e dry -e plan -e check`.
2. Use the flag for the common tools:
   - shell/io: `rsync -avn src/ dst/`, `rm -i` or `find ... -print`.
   - git: `git apply --check patch.diff`, `git push --dry-run`, `git clean -nd`.
   - terraform/tofu: `terraform plan -out=tfplan` then `terraform apply tfplan`.
   - containers: `kubectl apply --dry-run=server -f k8s/`, `docker compose config`.
   - packages: `npm publish --dry-run`, `pip install --dry-run --report /tmp/pip.json`.
3. Read the preview and diff it against your intent: every added line is intended, every removed line is intended, and nothing else appears. An unexpected deletion is a stop condition.
4. For infrastructure, capture the plan to a file and apply that exact artefact (`-out=tfplan`), not a fresh plan, so what you reviewed is what runs.
5. If the tool has no dry-run, simulate: copy to a scratch dir and run there (`cp -a src /tmp/probe && cd /tmp/probe && ./migrate.sh`).
6. Note when a "dry run" still has side effects — some deploy tools validate against production and can warm caches or consume rate limits.
7. Apply, then compare the actual change to the previewed one; a mismatch means stop and investigate.
8. Keep the plan file with the change record so the applied diff is auditable.

## Pitfalls

- Assuming a flag is a dry run because it contains "check" — `--check` may only lint, not preview the transform.
- Previewing one change and applying a freshly generated, different one.
- Reading the plan's summary line instead of the full diff, missing an unintended resource.
- Running a dry-run mode that actually writes metadata to a live system.
- Applying to a copy with different config than the real target, so the probe does not predict reality.

## Verification

    diff <(terraform show -no-color tfplan) notes/applied-diff.txt
    # passes when the applied change matches the previewed plan line for line

Report to the user: the dry-run command, the key lines of the preview, and confirmation that the applied change matched it.
