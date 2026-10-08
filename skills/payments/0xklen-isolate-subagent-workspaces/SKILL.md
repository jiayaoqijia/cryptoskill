---
name: isolate-subagent-workspaces
description: Use when parallel children share a machine, repo, or environment. Gives each child a private workspace (worktree, directory, container) so one cannot corrupt another's files or state.
---

# Isolate Subagent Workspaces

Shared state is the root of most parallel bugs. Put each child in its own workspace — a git worktree, a copy, or a container — so its writes and environment changes stay local.

## Procedure

1. Pick the isolation level by the risk: a separate output directory for write-only children, `git worktree` for repo editors, a container for children that install packages.
2. For repo work, create a worktree per child: `git worktree add ../wt-<id> -b child-<id>`.
3. Give each child its own scratch root via the environment: `TMPDIR=$PWD/scratch/child-<id>` so temp files cannot collide.
4. Isolate environment variables and config paths per child (separate `$HOME` or config dir) so global settings do not race.
5. For containers, mount only the child's slice read-write; mount shared inputs read-only.
6. Prevent package collisions by giving each child its own virtualenv under its worktree.
7. Collect results by copying from each workspace into a wave directory at fan-in, not by having children write a shared path.
8. Tear down workspaces after fan-in: `git worktree remove ../wt-<id>` and delete the scratch directories.
9. Verify isolation: a child's writes should be invisible outside its workspace until copied out.
10. Record the workspace path per child in `notes/roster.json` so fan-in and teardown both know where to look.

## Pitfalls

- Running all children in one checkout "because it's simpler", so writes interleave and a green run is luck.
- Sharing a single virtualenv, so one child's `pip install` changes the version another depends on.
- Forgetting `git worktree remove` and leaking dozens of checkouts that confuse the next run's globs.
- Mounting a shared input read-write in a container and letting two children edit it concurrently.
- Isolating files but not env vars, so one child's exported variable leaks into the next through a shared parent shell.

## Verification

```bash
git worktree list; ls -d scratch/child-*/
# passes when each child has its own worktree/dir and no child writes outside them
```

Report to the user: the isolation level chosen per child, the workspace paths, and confirmation they were torn down.
