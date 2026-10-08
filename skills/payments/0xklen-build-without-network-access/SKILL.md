---
name: build-without-network-access
description: Use when a build must run hermetically in a sandbox or air-gapped runner. Proves the build touches no network by running it with networking disabled.
---

# Build Without Network Access

A build that silently fetches at compile time is not hermetic — it fails during an outage and can be poisoned by a hijacked registry. Disabling the network turns hidden fetches into hard errors.

## Procedure

1. Warm every cache first, then run the build offline. Populate: pip wheels, npm cache, cargo registry, Maven `~/.m2`, Go module cache (`go mod download`).
2. Run in a container with networking off:
   `docker run --rm --network=none -v "$PWD:/src" -w /src build-image ./build.sh`
3. Force the package managers offline so a missing artifact fails loudly:
   `pip install --no-index --find-links vendor/` · `npm ci --offline` · `cargo build --offline` · `go build -mod=vendor` · `mvn -o` · `gradle --offline`.
4. Catch what the container misses with a syscall probe:
   `strace -f -e trace=network -o net.log ./build.sh; grep -c 'socket(' net.log`
   A count of 0 means no sockets opened.
5. Restrict DNS as a second net: run under a profile with no resolv.conf, or `unshare -rn ./build.sh` on Linux for a throwaway network namespace.
6. Commit the warm cache manifest (hashes of every downloaded blob) so the offline set is reproducible, not ad hoc.
7. Add the offline build as a required CI job on a runner with egress blocked, so a reintroduced fetch fails the PR.
8. Document which steps genuinely need the network (signing, publishing) and split them into a separate, networked stage.

## Pitfalls

- `--network=none` still allows Unix-domain sockets and localhost; a proxy on `127.0.0.1` will pass and mask the fetch.
- Some tools phone home for telemetry or version checks by default; disable with `DO_NOT_TRACK=1`, `NEXT_TELEMETRY_DISABLED=1`, `npm config set update-notifier false`.
- A warm cache with a per-machine key is not portable; key it by lockfile hash.
- GitHub-hosted runners cannot be truly air-gapped; emulate with a firewall that blocks egress except the artifact proxy.
- Clock skew breaks TLS in offline mirrors less often than expired tokens do — check tokens before blaming the cache.

## Verification

    docker run --rm --network=none -v "$PWD:/src" -w /src build-image ./build.sh && \
      grep -c 'socket(' net.log

Build exits 0 with no network and the strace probe reports zero network syscalls.

Report: "Build ran to completion under `--network=none`; strace logged 0 network syscalls, so no compile-time fetch remains."
