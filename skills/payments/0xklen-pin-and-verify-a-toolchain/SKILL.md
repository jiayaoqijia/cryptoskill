---
name: pin-and-verify-a-toolchain
description: Use when a build depends on a specific compiler, interpreter or CLI version. Pins the toolchain in-repo and verifies installer checksums so every machine builds with the same tools.
---

# Pin and Verify a Toolchain

"Works on my machine" is usually "works with my compiler". Pin the exact toolchain in the repo so CI, laptops and release builders agree, and verify what you download.

## Procedure

1. Pin per language in the file its manager reads on checkout:
   - Node: `.nvmrc` (or `engines` + `packageManager` with `corepack`), commit the exact version `20.11.1`.
   - Python: `.python-version` for pyenv, or a `python_requires` plus a locked interpreter in the CI image.
   - Rust: `rust-toolchain.toml` with `channel = "1.78.0"` and the components you need.
   - Go: the `toolchain go1.22.3` directive in `go.mod`.
   - Multi-tool repos: `.tool-versions` for `mise`/`asdf`, one line per tool.
2. Enable corepack so Node package managers are pinned too: `corepack enable && corepack prepare pnpm@9.1.0 --activate`.
3. Do not trust a `curl | bash` installer. Download the artifact, then verify its checksum or signature:
   `curl -fsSLO https://example.org/tool-1.2.3.tar.gz && \
    echo "<sha256>  tool-1.2.3.tar.gz" | sha256sum -c -`
4. Fetch the expected checksum from a signed source, not a URL on the same CDN that served the binary.
5. Re-pin in a dedicated PR; treat a toolchain bump as a dependency change requiring a full CI run, not a drive-by edit.
6. Make CI install from the pin: `mise install` respects `.tool-versions`; `rustup` respects `rust-toolchain.toml`; `setup-node` reads `.nvmrc`.
7. Record the installed versions as a build artifact so a failure can be attributed: `node -v && rustc -Vv && go version | tee toolchain.txt`.

## Pitfalls

- Pinning `latest` or a major-only `node@20` defeats the purpose; patch versions change behaviour.
- `rust-toolchain.toml` without `channel =` set exactly lets rustup pull the current stable on each machine.
- A checksum file fetched over the same connection it is meant to authenticate adds no security.
- Pinning in CI but not for developers means CI catches a version skew only after a push.
- A `packageManager` field without `corepack enable` is advisory; CI will still use whatever npm happens to be installed.

## Verification

    test "$(node -v)" = "v$(cat .nvmrc)" && rustup show active-toolchain | grep -q 1.78.0 && \
      cat toolchain.txt

Each tool's runtime version equals its pin file on a fresh checkout, and the recorded `toolchain.txt` for the release matches the CI job's.

Report: "Toolchain pinned (node $(cat .nvmrc), rust 1.78.0, go 1.22.3); installer checksum verified; fresh CI and local installs report identical versions."
