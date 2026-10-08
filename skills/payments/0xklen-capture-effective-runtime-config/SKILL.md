---
name: capture-effective-runtime-config
description: Use when behaviour differs between two running instances of the same build. Prints the configuration each process actually resolved, including inherited defaults and overrides, rather than trusting the file on disk.
---

# Capture Effective Runtime Config

The config file is a request; the process's resolved config is a fact. When two identical builds behave differently, the divergence is in what each actually loaded — env, flags, defaults, or remote overrides.

## Procedure

1. Find the precedence order for the stack (e.g. defaults < file < env < CLI flags < remote). Overrides win, so a correct file can still be wrong.
2. Dump the resolved config from *inside* the running process, not from the deployment repo: add a startup log line that prints every non-secret setting and its source.
3. For live processes without a dump: read the environment directly — `tr '\0' '\n' < /proc/<pid>/environ`, `kubectl exec <pod> -- env | sort`, `docker inspect -f '{{json .Config.Env}}' <id>`.
4. Compare the two instances field by field: `diff <(env -i python3 -c '...dump...' ) <(ssh other '...dump...')`, sorted.
5. Redact secrets before sharing: replace known keys with `***`, keep their lengths and sources so a truncated token is still visible.
6. Confirm the process actually read the file you think it did: log the resolved absolute path and its mtime.
7. Watch for a second source silently winning: a `*.local` file, a systemd `EnvironmentFile`, a Kubernetes ConfigMap mount, or a `.env` picked up by the framework.
8. Record the resolved config in the bug note, so "works for me" becomes a diff.

## Pitfalls

- Reading the file in git and assuming the process loaded it; the running container may mount an older ConfigMap.
- Missing inherited env: a shell profile or CI job exporting `NODE_ENV=production` changes behaviour invisibly.
- Logging the config before the framework's own defaults are merged, so defaults look like unset values.
- Printing secret values verbatim into a bug report or ticket.
- Forgetting that some settings are read once at boot and never reloaded, so a "fixed" file changes nothing until restart.
- Comparing pretty-printed JSON in different key orders without sorting.

## Verification

    tr '\0' '\n' < /proc/"$(pgrep -f myservice | head -1)"/environ | sort > /tmp/live.env
    grep -E '^(DB_HOST|CACHE_TTL|FEATURE_)' /tmp/live.env
    # passes when the values shown match the failing behaviour's expectations, not the repo file

    diff <(jq -S . config.a.json) <(jq -S . config.b.json)
    # the single differing resolved field is the config-side cause

Report to the user: the resolved value and its source for each setting that differs, plus which of them the code reads at boot.
