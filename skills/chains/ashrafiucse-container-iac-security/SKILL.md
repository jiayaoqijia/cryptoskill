---
name: container-iac-security
description: Audits container and infrastructure-as-code security — Dockerfiles, docker-compose, Kubernetes manifests/helm charts, Terraform, CloudFormation, Pulumi. Finds root containers, untagged images, secrets baked into layers, privileged containers, host mounts, overly open security groups, unencrypted storage, and IAM over-privilege. Use when auditing Docker, Kubernetes, Terraform, or cloud infrastructure definitions.
license: MIT
---

# Container & IaC Security

## Dockerfile

```bash
rg --files -g 'Dockerfile*' -g '*.dockerfile'
```

Check each Dockerfile:
- **No `USER` directive** → runs as root → HIGH (add `USER app` + `COPY --chown`)
- `FROM ...:latest` or untagged base → MEDIUM (unreproducible, silent breaking changes)
- Secrets in build: `ARG`/`ENV` with keys, `COPY .env`, private keys copied in → CRITICAL (they persist in layers even if later deleted — check multi-stage usage)
- `ADD http://...` (remote fetch) instead of `COPY` → MEDIUM; `ADD url | sh` patterns → HIGH
- `curl ... | sh` in RUN → HIGH
- Package caches not cleaned, `apt-get upgrade` in build (non-deterministic) → LOW hygiene
- Missing `HEALTHCHECK` where orchestrator relies on it → LOW
- sudo/setuid bits installed in image → MEDIUM

## docker-compose / docker run scripts

- `privileged: true` → CRITICAL unless strongly justified (enumerating what it grants: all caps, host devices)
- `volumes: /var/run/docker.sock` mounted → CRITICAL (container escape = host root)
- `network_mode: host` → HIGH (bypasses network isolation)
- `cap_add: SYS_ADMIN|NET_ADMIN|...` → flag each with justification check
- Host paths mounted writable (`/:/host`) → CRITICAL
- Default/weak service passwords (`POSTGRES_PASSWORD: postgres`) with published ports (`ports:` mapping to host) → HIGH

## Kubernetes

```bash
rg --files -g '*.yaml' -g '*.yml' | xargs grep -ln "kind: Deployment\|kind: Pod\|SecurityContext" 2>/dev/null
```

- Missing/broken `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, dropped capabilities (`drop: ["ALL"]`) → MEDIUM per gap, HIGH combined on internet-facing services
- `privileged: true` in containers → CRITICAL
- `hostPath` volumes, especially writable → HIGH/CRITICAL
- `automountServiceAccountToken: true` (default) on pods that don't talk to the K8s API → MEDIUM (default creds for lateral movement)
- Wildcard RBAC (`verbs: ["*"]`, `resources: ["*"]`), cluster-admin bindings to services → HIGH. **RBAC escalation verbs**: any Role/ClusterRole granting `escalate` (self-boost any role), `bind` (bind higher-priv roles to self), or `impersonate` (become any user/SA) → **Critical** even scoped; `verbs: ["get","list"]` on `secrets` at cluster scope → Critical (reads every credential)
```bash
rg -n "escalate|impersonate" -g '*.yaml' -g '*.yml' | rg "verbs|resources"   # census: every verb row dispositioned
rg -n "resources:.*secrets" -g '*.yaml' -g '*.yml' | rg -v "namespace"   # census: every secret-reading role dispositioned
```
- `imagePullPolicy: Always` with `:latest` tags / images from unknown registries → MEDIUM
- Resource limits absent (DoS surface) → LOW
- Exposed `type: LoadBalancer` on admin/debug services → HIGH
- Secrets as plain `ConfigMap`/env instead of Secret objects/external secrets → MEDIUM
- **Ingress (nginx-ingress) annotations**:
```bash
rg -n "nginx\.ingress\.kubernetes\.io/(configuration-snippet|server-snippet|auth-url|rewrite-target|proxy-ssl)" -g '*.yaml' -g '*.yml'
```
  - `configuration-snippet`/`server-snippet` in user-editable Ingress objects → config injection by anyone who can create Ingresses (CVE-2021-25742 family); controller must have snippets disabled → HIGH if reachable
  - `rewrite-target` with attacker-influenced capture groups → open redirect/proxy (CVE-2021-25741 family — check controller version)
  - `auth-url` with broad skip/bypass paths (`*-snippets` overriding auth) → HIGH
- **Egress**: no `NetworkPolicy` with `Egress` policyType for pods that fetch URLs / call external APIs → MEDIUM alone, raise the paired SSRF finding (see `../injection-flaws/SKILL.md`) — the fetcher can reach cloud metadata (169.254.169.254) and internal services
```bash
rg -n "policyTypes:" -g '*.yaml' -g '*.yml'     # any Egress policy at all?
```

## Terraform / CloudFormation / Pulumi

```bash
rg -n -i "0\.0\.0\.0/0|::/0" -g '*.tf' -g '*.yaml' -g '*.json'
rg -n -i "ingress|cidr_blocks|security_group" -g '*.tf'
rg -n -i "hardcoded|access_key|secret_key|aws_secret" -g '*.tf'
```

- Security groups / firewall rules: `0.0.0.0/0` ingress on ports 22/3389/5432/6379/27017/etc. → CRITICAL/HIGH (port 80/443 on load balancers is fine — judge by port)
- Databases/storage unencrypted at rest (`encrypt_at_rest`, `storage_encrypted` false/omitted) → HIGH
- Public S3/GCS buckets (`public_access_block` absent, `acl: public-read`) → HIGH if data is non-static
- IAM: `Action: "*"` / `resources: ["*"]` policies attached to broad principals → HIGH; wildcard trust policies → CRITICAL. **Full escalation-path analysis (PassRole+compute, self-modification, broken trust, ExternalId)**: `references/aws-iam-escalation.md` — load it whenever IAM policies or trust relationships exist in the repo.
- Hardcoded cloud keys in state files/code → CRITICAL (also check `.tfstate` committed to git)
- Cloud: metadata with v1 tokens allowed → raises SSRF severity
```bash
rg -n -i "metadata_options|http_tokens|hop_limit|imdsv2" -g '*.tf' -g '*.yaml'
```
- `http_tokens = "optional"` / IMDSv1 allowed on internet-facing workloads → HIGH (metadata credential theft pairs with any SSRF)
- No `hop_limit = 1` on containers/instances fetching user URLs → MEDIUM
- Disabled logging (no `aws_flow_log`, `enable_audit` variants) → MEDIUM
- Snapshot/backup configs absent → LOW

## Serverless / FaaS (Lambda & friends)

```bash
rg --files -g 'serverless.yml' -g 'template.yaml' -g '*.tf' | head
rg -n -i "handler|runtime|iam|role" -g 'serverless.yml' -g 'template.yaml' | head -10
```
- **Wildcard IAM on functions** (`Resource: "*"` + `Action: "*"`/s3:*/dynamodb:* in the execution role) → HIGH; pair with `aws-iam-escalation.md` paths for chains
- **Trusted event payloads**: SQS/Kinesis/SNS handlers treating message bodies as trusted (second-order pattern — producers are not trust boundaries; validate + scope per tenant) → Medium/High
- **API Gateway without authorizer** (or `NONE`/open access on non-public routes; `authorizationType: NONE` on state-changing routes) → Critical
- Function URLs / public invokes without auth → Critical
- Secrets in env vars of function defs (`environment:` blocks in serverless.yml/template.yaml) → Critical (same rules as `secrets-detection`)
- Layers/containers pulled from public registries unpinned → Medium

## Reporting

**Optional bridge:** if `checkov`/`kube-linter`/`tfsec` is installed (probe: `../security-audit/scripts/probe_tools.sh`), run it and map its findings onto the categories above — tools catch rule-library items greps miss (e.g. new CIS checks); you add the context triage they can't.

Group by layer (image → runtime → cluster → cloud). For each finding: the exact resource + file:line, blast radius sentence, and the hardened config snippet (e.g. the corrected `securityContext` block). Cross-reference CRITICAL secrets findings with `../secrets-detection/SKILL.md`.
