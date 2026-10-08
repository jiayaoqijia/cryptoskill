---
name: sandbox-agent-shell-commands
description: Use when an agent runs shell commands it generated itself. Execute them in a sandbox with no network, a read-only host, and a disposable filesystem so a bad command cannot reach the host.
---

# Sandbox agent shell commands

An agent writing its own shell is one typo from `rm -rf` in the wrong directory. Run generated commands in a throwaway sandbox with the host mounted read-only and egress blocked.

## Procedure

1. Never run a generated command in the working repo directly. Start a container: `docker run --rm -v "$PWD/out:/work:rw" -w /work alpine:3.20 sh -c "<cmd>"`.
2. Mount only the paths the step needs, and mount them read-only unless the step writes there: `-v "$PWD/src:/src:ro"`.
3. Block network by default: `--network none`. Add a named network only when the step genuinely fetches.
4. Drop capabilities and run non-root: `--cap-drop ALL --security-opt no-new-privileges --user 65534`.
5. Bound the run: `--memory 512m --pids-limit 128 --cpus 1` and a `timeout 60s` outside the container.
6. Capture stdout, stderr, and exit code separately so a non-zero exit is not swallowed by a pipe.
7. Use `--rm` so each step starts clean; a sandbox that accumulates state stops being disposable.
8. For commands that only inspect, prefer running them read-only twice: once to see, once to confirm, before any writable variant.

```bash
docker run --rm --network none --cap-drop ALL --user 65534 \
  -v "$PWD/src:/src:ro" -m 512m --pids-limit 128 alpine:3.20 \
  timeout 60 sh -c "$CMD"
echo "exit=$?"
```

## Pitfalls

- Running generated shell in the live repo "just this once" to save a container start.
- Mounting the home directory read-write, which hands the agent every credential on the machine.
- Leaving `--network host` on from an earlier step that needed it.
- Piping output through `tail` and reading the pipe's exit code instead of the command's.
- Reusing a long-lived sandbox container, so state from a failed run leaks into the next.
- Forgetting `timeout`, letting a hung command hold the agent's whole step budget.

## Verification

    docker run --rm --network none alpine:3.20 sh -c 'wget -T2 -qO- https://example.com'; echo "egress_blocked_exit=$? (nonzero = good)"

Report the command run, the sandbox flags used, and the captured exit code.
