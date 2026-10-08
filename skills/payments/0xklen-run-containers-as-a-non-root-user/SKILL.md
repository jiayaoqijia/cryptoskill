---
name: run-containers-as-a-non-root-user
description: Use when a container should not have root inside it even if the host is safe. Creates and switches to an unprivileged UID pinned in the image so a process compromise is not a root compromise.
---

# Run Containers as a Non-Root User

By default a container runs as UID 0, and without a user namespace that is host root for many escape and volume paths. The fix is a numeric, explicit UID baked into the image plus a runtime refusal to run as root.

## Procedure

1. Create the user in the image with a fixed numeric UID (names are resolved in the image, so a bare `USER app` fails on a base that lacks the passwd entry):
   ```dockerfile
   RUN groupadd -g 10001 app && useradd -u 10001 -g 10001 -m -s /sbin/nologin app
   USER 10001:10001
   ```
2. `chown` the working dir and any writable paths before switching, since root-only writes after `USER` fail:
   `RUN chown -R 10001:10001 /app && chmod -R u+rwX /app`.
3. At runtime, make the intent explicit and defensive:
   `docker run --user 10001:10001 --read-only --tmpfs /tmp app:x`.
4. In Kubernetes set `runAsNonRoot: true` and a numeric `runAsUser`, which the kubelet refuses to violate:
   ```yaml
   securityContext:
     runAsNonRoot: true
     runAsUser: 10001
     allowPrivilegeEscalation: false
     capabilities: { drop: ["ALL"] }
   ```
5. Enforce cluster-wide with the Pod Security Standard `restricted` profile, or a Kyverno rule requiring `runAsNonRoot: true` on every pod.
6. Check what a process can do: `docker run --rm app:x id` must print `uid=10001`. For ports, bind to `>1024` — non-root cannot bind `80`/`443`, so publish with `-p 8080:8080` and let the proxy handle the low port.
7. If a supervisor needs a low port, do not grant `CAP_NET_BIND_SERVICE` broadly; drop ALL and add back only that one capability.

## Pitfalls

- Setting `USER` in the Dockerfile does not stop `docker run --user 0`; only `runAsNonRoot: true` in the orchestrator enforces it.
- A base image's `USER 1000` is often overridden by a later `RUN` that escalates to `USER root` and never switches back — the image ships as root and nobody notices.
- `chown -R` in a huge layer doubles image size; prefer creating files as the target user or `--chown=10001:10001` on `COPY`.
- Volume mounts from the host arrive owned by the host's UID; a container non-root user then cannot write them. Set `fsGroup` (K8s) or `--user` matching the host, or use an init container to chown.
- Random UIDs from `runAsUser` ranges break images whose entrypoint reads `/etc/passwd` for a home directory; mount a writable `HOME` or an emptyDir instead.
- `allowPrivilegeEscalation: false` still permits a setuid binary already in the image — remove setuid bits in the Dockerfile (`RUN find / -perm -4000 -exec chmod u-s {} +`).

## Verification

    docker run --rm app:x id
    # uid=10001(app) gid=10001(app) groups=10001(app)

The command prints a non-zero UID and the container runs its healthcheck without permission errors. Report the observed UID/GID and the policy that enforced it.
