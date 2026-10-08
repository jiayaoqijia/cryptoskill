---
name: make-a-build-reproducible
description: Use when two builds of the same commit produce different bytes. Pins inputs and strips nondeterminism so the same source yields byte-identical artifacts.
---

# Make a Build Reproducible

If two builds of the same commit differ, a checksum in a release note proves nothing and every cache hit is luck. Determinism must be shown, not assumed.

## Procedure

1. Measure the drift before fixing it. Build twice and diff the trees:
   `diffoscope build-a.tar.gz build-b.tar.gz | head -60`
   Build once locally and once in a clean container to expose environment leakage.
2. Pin every input. Use `FROM debian@sha256:<digest>`, not `debian:stable`. A floating `node:20` tag is not a pin.
3. Set `SOURCE_DATE_EPOCH` to the commit time so embedded dates are stable:
   `export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)`
4. Normalise the shell: `export LC_ALL=C TZ=UTC PYTHONHASHSEED=0`. Sort any generated file under `LC_ALL=C sort -u`.
5. Strip build paths. Go: `go build -trimpath -ldflags="-buildid=" -o out`. C: add `-ffile-prefix-map=$PWD=.`. Rust: set `remap-path-prefix` inside `RUSTFLAGS`.
6. Make archives deterministic — tar records mtime, owners and readdir order:
   `tar --sort=name --mtime=@$SOURCE_DATE_EPOCH --owner=0 --group=0 --numeric-owner -czf out.tgz dir/`
   For zip: `zip -X -r out.zip dir/` and reset each entry's mtime to the epoch.
7. Remove counters and host data. `git describe --dirty` embeds working-tree state; use `git rev-parse HEAD`. Drop build counters and hostnames.
8. Rebuild on a second machine and compare digests: `sha256sum a/out.tgz b/out.tgz`.

## Pitfalls

- Signing, SBOM and packaging steps re-add a timestamp. Hash and sign the built artifact in a separate pass, then never rebuild it.
- `apt-get install` in the Dockerfile pulls unpinned versions; pin via a committed lock or a hermetic mirror.
- Python `.pyc` files embed absolute source paths. Build with `PYTHONDONTWRITEBYTECODE=1`.
- Parallel linkers can reorder object files. Emit linker inputs as a sorted list.
- A cache that keys on branch name, not content, hides drift until release day.

## Verification

    ./build.sh && cp -r dist dist1 && rm -rf dist && ./build.sh && \
      diff -r dist dist1 && echo REPRODUCIBLE

`diff -r` prints nothing and exits 0 on a match. For a single binary, compare `sha256sum dist/app dist1/app` and assert equal.

Report: "Two builds of <commit> match byte-for-byte; after setting SOURCE_DATE_EPOCH and deterministic tar flags, diffoscope reports no differences."
