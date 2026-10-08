---
name: run-untrusted-code-with-network-disabled
description: Use when you must execute code, dependencies, or scripts you did not write. Run them with no network, a read-only mount, and a hard resource ceiling so a malicious payload has nowhere to send data.
---

# Run untrusted code with network disabled

The cheapest defence against code that phones home is to have no phone. This skill runs unknown scripts in a disposable, network-less, resource-capped sandbox and treats any attempt to reach out as a finding.

## Procedure

1. Prefer a container with networking off and a read-only root:

       docker run --rm --network none --read-only \
         --tmpfs /tmp:rw,noexec,nosuid,size=64m \
         --memory 512m --cpus 1 --pids-limit 128 \
         -v "$PWD/src:/src:ro" -w /src debian:12-slim sh -c 'bash ./run.sh'

2. On Linux without Docker, use a network namespace: `unshare -rn --map-root-user bash -c 'ip link set lo up; bash ./run.sh'`.

3. On macOS, use a disposable VM or a `sandbox-exec` profile that denies network; do not run unknown code on the bare host.

4. Mount inputs read-only and outputs to a fresh empty directory, so the code can write findings but cannot alter your tree or read your secrets.

5. Drop the environment to the minimum: `env -i PATH=/usr/bin:/bin HOME=/tmp bash ./run.sh`. Do not pass `$HOME`, tokens, or `AWS_*` variables in.

6. Cap time as well as memory: wrap with `timeout -s KILL 60` so a fork bomb or infinite loop cannot run out the clock.

7. Watch for network syscalls even with the namespace up: a `connect` to `169.254.169.254` or an external IP is exfiltration intent; capture it as evidence.

## Pitfalls

- `--network none` is not the default; omitting it gives the payload a live route out.
- Binding a directory read-write so the script "can save results" lets it overwrite your files or plant a payload.
- Inheriting the parent environment leaks API keys into code that will happily POST them.
- A container without `--read-only` can still be escaped via a mounted Docker socket; never mount `docker.sock`.

## Verification

    docker run --rm --network none alpine ip route   # empty routing table = isolation confirmed

Report: "ran <script> in <sandbox>, network none, mem 512m, cpu 1, timeout 60s; attempt-to-connect none|<n> recorded."
