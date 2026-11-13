---
name: environments-config
domain: software-engineering/environments-config
trigger: "\"containerize this\", \"write the Terraform\", \"set up staging\", \"move config out of the code\", \"works on my machine only\"."
anti_trigger: "Pushing to production hosts (subskills/deployment.md); pipeline gates and runners (subskills/ci-pipeline.md); where security checks sit; live schema changes."
scope: "IaC, containers, config and environment parity for running the app"
status: "seedling"
---

# Environments & Config

## Standard

- **12-factor config** (https://12factor.net/config): config lives in the environment, never in the code.
- **Two IaC classes**: a declarative DSL (Terraform HCL, OpenTofu, Pulumi) or a general-purpose language. State discipline is the law: remote locked state, no hand edits, `plan` before `apply`.
- **Drift detection** runs on a schedule, not only in CI.
- **Multi-stage builds**: each `FROM` starts a fresh filesystem, and only copied artifacts reach the last stage, so compilers and source never ship.
- **Slim bases and non-root**: distroless `:nonroot` (UID 65532) has no shell or package manager, so the CVE surface is near zero.
- **Parity**: dev, CI and production differ in config and scale, not in shape.

## Decision rules

1. Use IaC at two or more environments, two or more people, or a resource set rebuilt more than once. Below that a runbook is cheaper.
2. Commit the lockfile. Pin base images by digest for release builds.
3. Compose on one host fits under about eight services. Adopt Kubernetes for multi-node failover or autoscaling, never "to be ready to scale".
4. Build-time credentials use BuildKit `RUN --mount=type=secret`; runtime secrets go in the environment or a mounted file.
5. `.env` never enters an image or the repository.
6. Applying to production is **human-gated**: the agent runs `plan`, a human runs `apply`.
7. Read an agent-written infra change for policy intent — IAM scope, public exposure, encryption — not for a clean plan. ⚠️ A plan-clean agent fix once passed automated checks while leaving the defect in place (arXiv 2606.26590): direction reliable, rate single-lab.

## Procedure

1. List the environments and what differs between them.
2. Move every varying value out of the code into the environment.
3. Write a multi-stage image ending at a non-root base, and add `.dockerignore` with `.git`, `.env`, `node_modules` and build output.
4. Put the stack definition in the repo as versioned text.
5. Configure a remote, locked state backend before the first apply.
6. Read the diff line by line: `terraform plan -out=tfplan`.
7. Roll to dev, staging, then production, comparing one request at each hop.
8. Schedule drift detection: `plan -refresh-only` nightly; route any diff to a human.
9. Scan the image on every build. A finding in a new layer fails the build.
10. Record the runbook: how to rebuild each environment from nothing.

## Anti-patterns

- Secrets in `ENV` or `ARG`, or a committed `.env`.
- Unpinned base images, so a new CVE breaks the build daily.
- Kubernetes adopted for scale that does not exist.
- A rootful Docker socket open to untrusted build steps.
- An IaC repo whose plan nobody reads, so drift goes unnoticed.

## Done checklist

- [ ] Config comes from the environment everywhere.
- [ ] State is remote and locked; drift is checked on a schedule.
- [ ] Image is multi-stage, slim and non-root.
- [ ] A rebuild-from-scratch run exists and has been run.
- [ ] Secret handling documented, rotation owned by a human.

## Sources

- <https://github.com/hashicorp/terraform/blob/main/LICENSE>
- <https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321670229>
- https://12factor.net/config
