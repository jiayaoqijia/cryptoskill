---
name: never-mount-the-docker-socket
description: Use when a container is asked to build or manage other containers by mounting /var/run/docker.sock. Treats that mount as root-on-the-host and replaces it with a scoped alternative.
---

# Never Mount the Docker Socket

Mounting `/var/run/docker.sock` into a container hands it the Docker API, which is equivalent to host root: it can start a privileged container that mounts the host filesystem and reads any secret. CI runners, agents and "docker-in-docker" builders do this casually and it is a full escape.

## Procedure

1. Detect it before deploy: `docker inspect <container> | jq '.[].HostConfig.Binds, .[].Mounts'` and flag any source ending `/docker.sock`. In Compose, grep the file: `yq '.services[].volumes[]' compose.yml | grep docker.sock`.
2. Block it at admission. Kyverno: `validate.deny.conditions.any[].key: "{{ request.object.spec.volumes[].hostPath.path }}"` matching `/var/run/docker.sock`; or a Pod Security `restricted` profile with a policy forbidding hostPath.
3. Replace the need, not just the mount:
   - Build images out of the container: run `docker buildx`/`kaniko`/`buildah` in a dedicated, unprivileged builder (rootless BuildKit, `podman --remote`).
   - If a tool must orchestrate, give it a scoped API: a socket proxy such as `docker-socket-proxy` with `CONTAINERS=1, POST=0` so it can read but not create or exec.
   - Kubernetes: use the API with a `ServiceAccount` and RBAC limited to the objects it manages.
4. If a proxy is unavoidable, mount the proxy's socket, not the daemon's, and run the proxy container with the daemon socket read-only and a wildcard-denied default.
5. Never combine the socket mount with `--privileged` or `network_mode: host`.
6. Treat any container that ever had the socket mounted as trusted with host root — rotate host credentials it could have read.
7. For CI, prefer an ephemeral builder node over mounting the runner's socket into every job.

## Pitfalls

- A read-only socket mount (`:ro`) is not safe: the API can still create and start privileged containers; the mount flag does not restrict API semantics.
- `docker-socket-proxy` defaults to denying all; enabling `POST=1` to allow builds re-opens container creation and is only marginally better than the raw socket.
- `docker compose` mounts the socket for a `watch`/build feature without flagging it, so it can slip in during a refactor.
- DinD (`docker:dind`) as `--privileged` is also a host-root path; rootless BuildKit is the safe substitute.
- The socket is often mounted alongside `user: root` in the container, compounding the exposure, and the container then controls the daemon.
- A compromised sidecar with the socket reaches every other container's env and volume, not just its own.
- gVisor/Kata is not a defence here: the mount is a host path, not a syscall boundary.

## Verification

    docker inspect <container> --format '{{range .Mounts}}{{.Source}}{{"\n"}}{{end}}' | grep -c docker.sock
    # 0
    kubectl get pod <p> -o jsonpath='{.spec.volumes[*].hostPath.path}' | grep -c docker.sock
    # 0

No container in the workload references the daemon socket, and the build path uses rootless BuildKit or a proxy with POST disabled. Report the mount audit result per container.
