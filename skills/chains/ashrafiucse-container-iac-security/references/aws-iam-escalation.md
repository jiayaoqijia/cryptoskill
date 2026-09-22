# AWS IAM Privilege-Escalation Pack

IAM policies whose actions combine into privilege escalation (grounded in
the publicly documented escalation matrix — primed principals, role
chains, credential exfiltration). Load when the repo contains IAM
policies, trust policies, or Terraform/CloudFormation IAM resources.

```bash
rg -n -i "iam:|sts:|lambda:CreateFunction|ec2:RunInstances|glue:Create|cloudformation:Create|datapipeline:" -g '*.json' -g '*.tf' -g '*.yml' | head -25
rg -n -i "PassRole|AssumeRole|iam:Create(AccessKey|LoginProfile|User|Role|Policy)|iam:(Attach|Put|Update)(Role|User)Policy|sts:AssumeRole" -g '*.json' -g '*.tf' | head -20
```

## Escalation paths to check (action + what it needs)

| Path | Signal | Severity |
|---|---|---|
| **PassRole + service create** | `iam:PassRole` (with broad `Resource: "*"` or a privileged role ARN) + `ec2:RunInstances` / `lambda:CreateFunction` / `glue:CreateDevEndpoint` / `cloudformation:CreateStack` / `sagemaker:CreateNotebookInstance` | attach privileged role to a compute resource the principal controls → Critical |
| **Direct permission grants** | `iam:CreateAccessKey` or `iam:UpdateLoginProfile` on other users | create creds for a privileged user → Critical |
| **Policy self-modification** | `iam:PutUserPolicy`/`AttachUserPolicy`/`PutRolePolicy` on own principal (or `iam:*`) | grant self anything → Critical |
| **Role-chain assumption** | trust policy `Principal: "*"` or `AWS: "*"` (broken trust) / `sts:AssumeRole` reachable broadly with no external condition | anyone/any account assumes the role → Critical |
| **Confused-deputy** | trust policy allowing root of another account without `sts:ExternalId` (for 3rd-party access) | session hijack via the trusted third party → High |
| **Credential exfil** | any principal with BOTH read access to secrets (SSM/SecretsManager) the repo manages AND `iam:PassRole`-adjacent compute | chain material — note in chains |

## Judgment rules

- A single scary action with a narrow `Resource` (one specific role the
  principal legitimately passes) is normal — check what the ROLE grants.
- `iam:*` / `AdministratorAccess` on anything user-reachable: Critical, no
  further chaining needed.
- Trust-policy wildcards are findings even when the account looks internal
  — org accounts get compromised too.
- Cross-reference found paths with `container-iac-security` Terraform
  checks (wildcards there) and report as IAM layer findings with the
  exact policy document + file:line.

## Fix patterns

- Scope `iam:PassRole` to specific role ARNs the workload needs.
- Enforce permissions boundaries on roles users can create.
- Trust policies: explicit account root + `sts:ExternalId` for third
  parties; condition on `aws:PrincipalOrgID` for org-wide.
- Deny `iam:CreateAccessKey`/`UpdateLoginProfile` outside break-glass.
