---
name: navigate-a-monorepo-build-graph
description: Use when building or testing one package in a large monorepo. Uses the dependency graph to build only affected targets instead of the whole repo.
---

# Navigate a Monorepo Build Graph

In a monorepo, "run everything" wastes CI minutes and hides which package actually changed. Use the dependency graph to compute the affected set and build only that, plus its dependents.

## Procedure

1. Find the graph tool the repo already uses:
   - Nx: `nx show projects` and `nx graph --file=graph.json`.
   - Turborepo: `turbo run build --dry=json` and `package.json` `workspace` globs.
   - Bazel: `bazel query 'kind(".*rule", //...)'` and `bazel query 'rdeps(//..., //libs/x)'`.
   - pnpm workspaces: `pnpm -r list --depth -1`.
2. Compute changed files first: `git diff --name-only origin/main...HEAD`.
3. Map files to targets and expand to dependents:
   - Nx: `nx affected -t build test --base=origin/main --head=HEAD`.
   - Turborepo: `turbo run build --filter='...[origin/main]'` (the `...` means "and its dependents").
   - Bazel: `bazel build $(bazel query 'rdeps(//..., set(//libs/changed:all))')`.
4. Build leaves first. The graph's topological order is what the tool does for you; do not parallelise a target with its own dependencies.
5. Reason about `rdeps` vs `deps`: a change in a shared library affects everything that *depends on* it (reverse deps), which is usually the whole app, so scope the change tightly to avoid a full build.
6. Cache per target keyed on the target's inputs, not the repo commit, so unchanged targets rebuild from cache even in a fresh checkout (see the CI-cache skill).
7. Verify the affected set covers what you expect before trusting a fast run: an empty `affected` list when you edited a file means the project graph did not register that file.

## Pitfalls

- Glob changes to root configs (`tsconfig.base.json`, `WORKSPACE`, CI files) mark *every* target affected — expected, not a bug.
- A file the graph does not know about (a new script, an unregistered folder) is silently ignored and its target never builds.
- Remote caching without a content-addressed key can serve a stale artifact from another branch.
- `turbo --filter` needs the base ref to exist locally; a shallow clone without `origin/main` computes the wrong set.
- Circular package dependencies make topological order impossible; the tool will error or silently pick an order.

## Verification

    nx affected -t build --base=origin/main --head=HEAD --exclude='*e2e*' && \
      nx show projects --affected --base=origin/main | wc -l

The affected list is non-empty exactly when you changed a tracked file, and the build completes without building untouched projects (compare wall time to a full `nx run-many -t build`).

Report: "Changed <package>; graph selected <N> affected targets (<names>), built in <time> vs <full-time> for the whole repo."
