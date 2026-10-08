---
name: pin-transitive-dependencies-with-a-lockfile
description: Use when reproducible installs matter across environments. Commits a lockfile that pins every transitive version by hash so installs are byte-identical and verifiable.
---

# Pin Transitive Dependencies with a Lockfile

Direct ranges in a manifest say what you tolerate; a lockfile says what you built. Without a committed, hash-pinned lock, two machines install different transitive versions and only one of them is tested.

## Procedure

1. Generate the lock from a clean resolve once: `npm install --package-lock-only`, `pip-compile --generate-hashes requirements.in`, `cargo generate-lockfile`, `go mod tidy`.
2. Commit it and keep it tracked: `git add package-lock.json go.sum Cargo.lock requirements.txt`. Remove any `.gitignore` entry that excludes it.
3. Install in the strict mode that refuses to drift:
   `npm ci` · `pip install --require-hashes -r requirements.txt` · `cargo build --locked` · `go build -mod=mod` with a verified `go.sum` · `bundle install --frozen`.
4. Add hashes so a tampered package fails install: `pip-compile --generate-hashes`; for npm the lockfile already records `integrity` shasums.
5. Fail CI on drift: run the resolver with `--locked`/`--frozen` and assert `git diff --exit-code` on the lock afterward.
6. Separate direct from transitive: only bump a direct dependency in a deliberate PR; transitive moves happen as a consequence, never by hand-editing the lock.
7. For a targeted transitive bump (usually a CVE fix), address it explicitly: `cargo update -p rustls`, `npm dedupe`, or an `overrides`/`resolutions` entry.

## Pitfalls

- Editing the lockfile by hand corrupts the `integrity` fields and installs an unverified tarball.
- `go.sum` records hashes but `go build` without `-mod=mod`/verified checksum DB may pull from a proxy you did not intend; run `GOFLAGS=-mod=readonly`.
- `pip install -r requirements.txt` ignores hashes unless `--require-hashes` is passed.
- Running `npm install` in CI instead of `npm ci` silently rewrites the lock and skips the `--prefer-offline` fast path.
- A lock generated on macOS can include platform-specific optional deps that break a fresh Linux install; generate in the target platform's container.
- Two lockfiles for the same project (`pnpm-lock.yaml` and a stray `package-lock.json`) mean CI and developers pin different graphs.
- Not pinning build-time tools in the lock leaves them free to change the artifact even when the app deps are frozen.

## Verification

    npm ci && git diff --exit-code package-lock.json && \
      git log -1 --format=%h -- package-lock.json

The install succeeds, the lock is unchanged after install, and the lock's last-modified commit is the one you intended (not an incidental CI rewrite).

Report: "Lock pinned <N> packages with integrity hashes; `npm ci` (or `--require-hashes`) leaves the lock unchanged and `git diff --exit-code` is clean."
