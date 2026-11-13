---
name: containers
domain: security-hardening/containers
trigger: Building or running a container image — base image choice, user, scanning, runtime limits that cap what a compromise reaches.
anti_trigger: Cloud account, IAM, and IaC posture (subskills/cloud-iac.md); signing the build (subskills/supply-chain.md).
scope: Image minimisation, non-root, scanning, runtime limits
status: seedling
---

# Containers

## Standard

- **NSA/CISA Kubernetes Hardening Guidance v1.2** (2022-08-29): **run as non-root**; **immutable filesystems**; no privileged containers or `hostPID`/`hostIPC`/`hostNetwork`/`hostPath`; `--anonymous-auth=false`; RBAC least privilege; **encrypt etcd and Secrets**; default-deny NetworkPolicy; audit logging; TLS 1.2/1.3 everywhere (media.defense.gov, CTR_KUBERNETES_HARDENING_GUIDANCE_1.2).
- **NIST SP 800-190** *Application Container Security Guide* (Final, Sept 2017) remains current — the image/runtime/host layer split (https://csrc.nist.gov/pubs/sp/800/190/final).
- **CIS Docker Benchmark v1.8.0** is current (CIS August 2025 update) — the free configuration baseline (https://www.cisecurity.org/benchmark/docker).
- Measured risk is not raw CVE count: ~5.5% of running images carry critical/high vulnerabilities, while images with **known exploits dropped ~75% YoY** (Sysdig 2026 ⚠️ vendor). Exploitability in use is the metric.
- Most projects should not run Kubernetes: a managed PaaS (Fly.io, Render, Cloud Run, ECS Fargate) inherits control-plane hardening; the owner keeps pod-level rules only.

## Decision rules

1. Minimal base image — every package in the image is a package you patch; distroless or slim beats full Ubuntu.
2. Non-root always: add a `USER` directive; if the app "needs" root it needs a capability — grant the capability, not the user.
3. Read-only root filesystem where the app allows; writable paths as explicit mounts.
4. No secrets baked into layers — inject at runtime via env or secret mounts; anything in a layer is in the registry and `docker history` (`subskills/secrets.md`).
5. Pin image digests, not floating tags — a tag can be repointed, a digest cannot.
6. Scan in CI and block on high-severity findings (Trivy/Grype, free).

## Procedure

1. Write the image: `FROM` a slim or distroless base, `USER` non-root, no build tools in the final stage, `COPY` only artifact and runtime deps.
2. Multi-stage build so compilers never reach the shipped layer.
3. Add a CI scan (Trivy/Grype) gating on your severity floor plus the digest pin; wire it beside the other gates in `subskills/security-testing.md`.
4. Sign the image (cosign) if others pull it; publish the SBOM with it (`subskills/supply-chain.md`).
5. Run with limits: memory + CPU + PID caps, `no-new-privileges`, dropped capabilities, read-only rootfs — confirm non-root (`docker exec … id`).
6. On Kubernetes, apply the NSA/CISA items that survive a managed control plane: non-root, read-only rootfs, no privilege escalation, ResourceQuota/LimitRange, default-deny NetworkPolicy, namespaced RBAC, Secrets encryption, audit logging.
7. Never expose the Docker socket, `kubelet` API, or metadata endpoint to a container that does not need them — the socket is root on the host.

## Anti-patterns

- `FROM node:latest` with the whole toolchain in the shipped layer.
- Running as root because the port is "privileged" (use a high port or `NET_BIND_SERVICE`).
- Secrets as build args; mounting the Docker socket for convenience.

## Done checklist

- [ ] Base image slim/distroless; toolchain removed by a multi-stage build; non-root user verified in the running container.
- [ ] Read-only rootfs; writable paths as explicit mounts.
- [ ] No secrets in layers or build args; image digest pinned; CI scan gates on the severity floor.
- [ ] Memory/CPU/PID limits, `no-new-privileges`, capabilities dropped.
- [ ] K8s (if used): default-deny NetworkPolicy, namespaced RBAC, Secrets encryption, audit logging; no host-level mounts without a written exception.

## Sources

- Primary: NSA/CISA Kubernetes Hardening Guidance v1.2; NIST SP 800-190; CIS Docker Benchmark v1.8.0. Research: Sysdig 2026 Cloud-Native Security & Usage Report ⚠️ (vendor).
- <https://cheatsheetseries.owasp.org>
- <https://csrc.nist.gov/pubs/sp/800/190/final>
