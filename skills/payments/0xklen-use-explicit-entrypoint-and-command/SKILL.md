---
name: use-explicit-entrypoint-and-command
description: Use when a container's start command is ambiguous or overridden at deploy time. Splits ENTRYPOINT (the fixed binary) from CMD (default args) so operators can pass args without replacing the whole invocation.
---

# Use Explicit ENTRYPOINT and CMD

`ENTRYPOINT` is the executable that must run; `CMD` supplies its default arguments and is trivially overridden at runtime. Conflating them, or using shell form, makes the container start a shell, hide signals, and ignore `docker run ... <args>`.

## Procedure

1. Use exec (JSON) form so no shell wraps the process and signals reach it:
   ```dockerfile
   ENTRYPOINT ["/usr/local/bin/app"]
   CMD ["serve", "--addr=:8080"]
   ```
2. With this split, `docker run app:x migrate` replaces only `CMD`, giving `app migrate`; the entrypoint stays.
3. Put real shell logic in a script you `COPY` and exec, not inline in `ENTRYPOINT []`:
   ```dockerfile
   COPY entrypoint.sh /usr/local/bin/
   ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
   ```
   End the script with `exec "$@"` so PID 1 becomes the app and receives signals.
4. Never use `ENTRYPOINT /app start` (shell form): it runs `/bin/sh -c "/app start"` and the shell eats SIGTERM.
5. Keep arguments that are truly fixed in `ENTRYPOINT`; put anything an operator would reasonably change (config path, port, log level, subcommand) in `CMD`.
6. In Kubernetes, `command:` maps to `ENTRYPOINT` and `args:` maps to `CMD`; if you set only `args:`, the image's `ENTRYPOINT` still applies.
7. Validate the resolved command: `docker inspect -f '{{.Config.Entrypoint}} {{.Config.Cmd}}' app:x`.

## Pitfalls

- `CMD ["app"]` alone (no ENTRYPOINT) is overridden entirely by any `docker run` args, so `docker run app migrate` tries to execute `migrate` as a binary and fails with "executable file not found".
- Setting both `ENTRYPOINT` and `CMD` as the app, e.g. `ENTRYPOINT ["app","serve"] CMD ["app","serve"]`, appends args and runs `app serve app serve`.
- A shell-form `ENTRYPOINT` makes PID 1 the shell, so SIGTERM is not forwarded and graceful shutdown never runs — the container is SIGKILLed.
- A `RUN chmod +x` on a script is lost if a later `COPY` overwrites it without `--chmod=755`; the entrypoint fails with permission denied at start.
- Overriding Kubernetes `command:` without also overriding `args:` keeps the image's default args, producing an unexpected invocation.
- `ENTRYPOINT ["app.json"]`-style typos or bad JSON quoting silently fall back to shell parsing and reintroduce the signal problem.
- Relative paths in `ENTRYPOINT` depend on `WORKDIR`; a missing `WORKDIR` resolves against `/` and the binary is not found.

## Verification

    docker inspect -f '{{.Config.Entrypoint}} {{.Config.Cmd}}' app:x
    docker run --rm app:x --help        # CMD replaced, entrypoint kept

The entrypoint is the app binary and overriding args changes only the arguments. Report the resolved entrypoint/cmd pair.
