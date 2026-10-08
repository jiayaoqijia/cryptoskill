---
name: enforce-environment-parity-across-stages
description: Use when staging and production drift apart. Drives both from one module and variable schema so a change verified in staging behaves the same in prod.
---

# Enforce environment parity across stages

An environment that differs structurally from prod is a test that proves nothing. Parity means the same code with different inputs, not two hand-built clusters.

## Procedure

1. One module, one composition; vary only input variables per environment:
       module "app" {
         source         = "../../modules/app"
         instance_class = var.env == "prod" ? "m5.large" : "t3.small"
         min_size       = var.env == "prod" ? 3 : 1
       }
2. Keep a single `variables.tf` schema; each env supplies all inputs via `<env>.tfvars`. A variable present in one env and absent in another is drift.
3. Diff the composed resources of the two plans, ignoring expected size/count differences:
       terraform -chdir=envs/staging plan -out=s.plan && terraform -chdir=envs/prod plan -out=p.plan
       diff <(terraform show -json s.plan | jq -S '.planned_values.root_module.child_modules')
            <(terraform show -json p.plan | jq -S '.planned_values.root_module.child_modules')
4. Version-pin the module source (`?ref=v1.4.0`), never `main`; an unpinned ref means the two envs apply different code on different days.
5. Do not infer parity from "the same files exist"; verify the plan shapes match.
6. Track declared differences in a `parity.md`: instance sizes, replica counts, feature flags. Everything not listed must match.
7. Apply the same lint and policy gates to every env in CI, prod included.
8. Re-run the diff when the module changes; parity decays the moment someone patches one env.

## Pitfalls

- "Just this once" manual prod changes that never land in code, so the next apply reverts or duplicates them.
- Different provider versions pinned per env, so the same config produces different resources.
- A staging env built from a copy-paste that diverged six months ago and never matched.
- Comparing rendered names, which legitimately differ by env prefix, and calling real differences false positives.
- A feature flag enabled in staging but absent from prod config, so a "tested" path was never tested in prod shape.

## Verification

    diff <(tf_json staging) <(tf_json prod)   # only declared deltas remain
    grep -c 'variable "' envs/staging/variables.tf envs/prod/variables.tf   # counts match

Report: the module version both envs pin, the diff of composed resources, and the documented list of intentional differences.
