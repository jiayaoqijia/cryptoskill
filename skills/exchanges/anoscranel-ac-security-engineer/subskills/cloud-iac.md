---
name: cloud-iac
domain: security-hardening/cloud-iac
trigger: Setting up or auditing a cloud account, IAM, storage exposure, or IaC.
anti_trigger: Containers (subskills/containers.md); credential storage and rotation (subskills/secrets.md).
scope: IAM, storage exposure, IaC scanning, CIS baselines
status: seedling
---

# Cloud & IaC

## Standard

- **Zero trust, NIST SP 800-207** (Aug 2020): no implicit trust from network location; per-session dynamic policy — the network edge is not an authorization boundary (https://csrc.nist.gov/pubs/sp/800/207/final).
- AWS root-user guidance is the baseline: root holds complete access — **never create access keys for it**, put **MFA** on root sign-in (required within 35 days), and do not use root unless a task needs it (https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
- **CIS Benchmarks** are the free consensus baselines: AWS Foundations v7.1.0, Azure Foundations v6.0.0, GCP Foundation v5.0.0 (https://www.cisecurity.org/cis-benchmarks). Vendor compliance maps restate concrete items: block public buckets, restrict public SQL, rotate service-account keys.
- HashiCorp is unambiguous: **state and plan files contain secrets in plaintext**, and the `sensitive` flag only redacts CLI output (https://developer.hashicorp.com/terraform/language/manage-sensitive-data).

## Decision rules

1. One admin identity for daily work; root locked away with hardware MFA and a group recovery email. No root access keys, ever.
2. Short-lived role credentials and OIDC federation over long-lived keys; one least-privilege role per service.
3. Storage private by default: public-access blocks, databases in private subnets, no `0.0.0.0/0` on SSH/db/admin ports, HTTPS on buckets and CDNs.
4. Terraform state is a credential file: never commit `terraform.tfstate`; use remote state with encryption and locking; prefer ephemeral values / write-only arguments so generated passwords never persist.
5. Enable the platform's free posture checker (Security Hub / SCC / Defender) and drift detection — a console click that reopens a hole must be visible.6. Misconfiguration, not exotic exploits, dominates cloud risk: weak IAM and missing logging hit 80–98% of hyperscaler accounts (Intruder 2026 ⚠️ single vendor).
7. ⚠️ Applying an IaC plan to production is **human-gated** — plan output reviewed, a human applies.
## Procedure

1. Lock the root account: hardware MFA, group recovery, no access keys; in an Organization, strip member-account root credentials and deny root actions by SCP.
2. Create one daily admin identity; delete every unused IAM user and access key — the audit finds them.
3. Replace static cloud keys in CI with OIDC federation — the workflow requests a short-lived token, so no long-lived credential exists to leak (`subskills/secrets.md`).
4. Storage audit: list every bucket and database; set private-by-default; a reflected CORS origin with `Allow-Credentials` is a common hole.
5. Network: default-deny security groups; restrict egress so a compromised app cannot reach the metadata service (`169.254.169.254`) or exfiltrate freely (`subskills/ssrf.md`).
6. IaC hygiene: gitignore state, remote encrypted state with locking, ephemeral values for generated secrets, policy scanner (tfsec/Checkov) in the same CI as `subskills/security-testing.md`, and CIS findings from native tools with drift alerts on IAM policies, public-access blocks, and security groups.

## Anti-patterns

- Root access keys "for the CLI".
- `terraform.tfstate` in git, or an IAM user with `*:*` "temporarily".
- Unrestricted egress, so SSRF reaches metadata and the internet.

## Done checklist

- [ ] Root: no access keys, MFA on, group recovery; member accounts stripped.
- [ ] One daily admin identity; unused users/keys deleted.
- [ ] Long-lived cloud keys replaced by OIDC federation.
- [ ] Storage private-by-default verified across buckets and databases.
- [ ] Non-HTTP ports closed to `0.0.0.0/0`; egress restricted.
- [ ] State never committed; remote encrypted state; IaC scanner gates CI; drift alerts armed.

## Sources

- Primary: NIST SP 800-207; AWS root-user best practices; CIS Benchmarks; HashiCorp Terraform state docs; CISA BOD 26-04.
- <https://developer.hashicorp.com>
- <https://csrc.nist.gov/pubs/sp/800/218/final>
