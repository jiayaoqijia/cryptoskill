---
name: scan-container-images-for-vulnerabilities
description: Use when a container image ships with unknown OS and library CVEs. Scans the built image with Trivy or Grype, fails the build on fixable high/critical findings, and records a baseline.
---

# Scan Container Images for Vulnerabilities

Base images and language packages carry CVEs that a `npm audit` never sees; the OS layer alone can be hundreds of packages. Scanning the built image — not the source tree — is the only way to know what the runtime actually ships.

## Procedure

1. Scan the built image, not the Dockerfile: `trivy image --severity HIGH,CRITICAL ghcr.io/acme/app:1.4`.
2. Fail the build only on findings that are fixable and reachable, to avoid a permanently red pipeline:
   `trivy image --exit-code 1 --ignore-unfixed --severity CRITICAL app:x`.
3. As an alternative scanner with a different DB for cross-checking: `grype ghcr.io/acme/app:1.4 -o table`.
4. Pin the vulnerability DB and scanner version in CI so results are reproducible:
   `TRIVY_VERSION=0.55.0` and `--cache-dir .trivy-cache`.
5. Emit a machine-readable report as an artifact: `trivy image -f json -o trivy.json app:x`, then archive it with the release.
6. Create a `.trivyignore` for accepted findings, each line citing the CVE, the reason, and an expiry date so the exception is revisited.
7. Reduce the surface before ignoring: switch to a slim/distroless base, `apt-get upgrade` only what is needed, and remove build tooling from the final stage — most findings are in packages the app never imports.
8. Scan on a schedule too, not only at build: an unchanged image gains CVEs as the DB updates. Run `trivy image` nightly against the deployed digests.

## Pitfalls

- Scanning only the final stage misses CVEs in the build stage only if that stage is a separate pushed image; multi-stage junk dropped from the final image is correctly not reported.
- `--ignore-unfixed` hides real risk: an unfixed critical with no patch may still be exploitable, so track those separately rather than dropping them.
- Trivy's default DB lags the upstream advisory by hours; a "clean" scan means clean as of the DB timestamp, so record it.
- Ignoring by CVE id globally hides new instances in other packages; scope ignores to the package path.
- A distroless image reports few OS CVEs because there is no package manager metadata to read — the count is not comparable to a Debian-based image.
- An image that `COPY`s a static binary still inherits base OS layers built for the scanner's detection; verify what is actually in the final `FROM`.
- Failing CI on LOW/MEDIUM makes developers disable the gate; gate on CRITICAL+fixable and report the rest.

## Verification

    trivy image --exit-code 1 --ignore-unfixed --severity CRITICAL app:x
    echo "exit=$?  db=$(trivy --version | head -1)"

Exit code 0 with the DB version printed, and the JSON report archived. Report the finding counts by severity and the DB date, not "image is clean".
