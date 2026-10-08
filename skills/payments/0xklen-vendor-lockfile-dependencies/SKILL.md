---
name: vendor-lockfile-dependencies
description: Use when a build must not reach a package registry or must survive a registry outage. Copies resolved dependencies into the repo and makes the build read only from there.
---

# Vendor Lockfile Dependencies

Vendoring moves the dependency set from "whatever the registry serves today" to "these exact files in this commit". It makes builds offline-capable and audits reviewable.

## Procedure

1. Commit the lockfile and prove it is tracked: `git ls-files --error-unmatch package-lock.json`. If it is in `.gitignore`, remove that line — an untracked lockfile is not a lock.
2. Install strictly from the lock, never resolving fresh: `npm ci` (not `npm install`), `yarn install --immutable`, `pnpm install --frozen-lockfile`.
3. Go: `go mod vendor` writes `vendor/`; builds then use `-mod=vendor` automatically when `vendor/modules.txt` exists.
4. Python: `pip download -r requirements.txt -d vendor/` (add `--only-binary=:all: --platform manylinux2014_x86_64 --python-version 3.11` to vendor wheels for a target platform). Install with `pip install --no-index --find-links vendor/ -r requirements.txt`.
5. Rust: `cargo vendor > .cargo/config.toml` and commit `.cargo/config.toml` so cargo uses the vendored source replacement.
6. Node without a registry: add `.npmrc` with `offline=true` or point `registry` at a local `verdaccio` cache.
7. Add a CI step that fails on drift: run the manager again and `git diff --exit-code` the lockfile and vendor tree.
8. Record the size cost — vendored trees bloat a clone. Check `du -sh vendor/ node_modules/`.

## Pitfalls

- Vendoring without committing the lock still lets versions drift on the next resolve; the two must move together.
- Platform-specific wheels vendored on macOS do not install on Linux CI. Vendor for the build target's platform tags.
- `go mod vendor` prunes packages only reachable from tests you do not run; keep a `tools.go` importing build-time tools so they stay in.
- A vendored tree hides license headers from scanners that read manifests; keep `LICENSES/` alongside.
- `npm ci` deletes `node_modules` first — never run it on a path with hand-edited local modules.
- Vendoring a package that post-installs a native binary from the network is not really offline; check for `postinstall` hooks that fetch.
- A vendor directory committed but stale relative to an unreviewed lock turns a routine `npm ci` into a surprise; treat the pair as atomically changed.
- Vendoring inflates clone size for every developer; a shallow vendored tree still costs CI minutes to check out.

## Verification

    go build -mod=vendor ./... && git status --porcelain vendor/ | wc -l

A clean `go build` and zero changed files under `vendor/` after a rebuild means the tree is complete and in sync with the lock.

Report: "Dependencies vendored (<N> modules, `du -sh vendor/` = <size>); build succeeds with `--no-index`/`-mod=vendor` and `git diff --exit-code` on the lockfile is clean."
