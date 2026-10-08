---
name: restrict-agent-writes-to-an-allowlisted-path
description: Use when an agent writes files it chose the path for. Confine every write to a declared directory, reject path traversal, and log the resolved target.
---

# Restrict agent writes to an allowlisted path

An agent that picks its own filenames can overwrite a config, a credential file, or a sibling project. Resolve every write path, check it against an allowlist, and refuse anything outside.

## Procedure

1. Declare the writable roots once per run: `out/`, `notes/`, `tmp/`. Everything else is read-only.
2. Resolve the target to an absolute real path before checking: `os.path.realpath(p)`, which collapses `..` and symlinks.
3. Compare against the resolved roots with a boundary-safe check: `commonpath([root, target]) == root`, not a substring test.
4. Reject absolute paths supplied by the model unless they already sit inside a root.
5. Disallow symlink targets: a link inside `out/` pointing at `~/.ssh` must fail the realpath check.
6. Create parent directories only inside the root, and refuse to create a root that does not already exist.
7. Log the resolved path and the allowlist decision: `write=out/report.csv allowed=yes root=out`.
8. On rejection, return a clear error naming the attempted path so the model can retarget, not silently drop the write.

```python
import os
ROOTS = {os.path.realpath(r) for r in ("out", "notes", "tmp")}
def safe_write(p):
    real = os.path.realpath(p)
    if not any(os.path.commonpath([r, real]) == r for r in ROOTS):
        raise PermissionError(f"path outside allowlist: {real}")
    with open(real, "w") as fh:
        fh.write("...")
```

## Pitfalls

- Checking with `".." not in path` or a `startswith` prefix, both of which `out/../etc/x` and `outside/` slip past.
- Checking the path before resolving symlinks, so a link inside the root escapes it.
- Allowing the model to widen the allowlist itself in the same turn.
- Creating an allowlist root on demand, turning deny into allow-on-request.
- Dropping a rejected write silently, so the model believes it succeeded.
- Writing a temp file next to the target with a predictable name and racing another child.

## Verification

    python3 -c "import os;print(os.path.commonpath([os.path.realpath('out'), os.path.realpath('out/../out/x')]))"   # prints the root, not a parent

Report each write's resolved path, the allowlist decision, and any path refused.
