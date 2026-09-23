# Package Release Metadata Must Match Contract Impact

The changelog entry and the semver bump match the contract impact, and a bump PR names the package version and the consumers it was checked against.

- **Public API/state change without changelog** — clients need migration context.
- **Breaking change released as minor/patch** — semver must match impact.
- **Controller package and client integration out of sync** — sync/bump PRs should state package version and consumer compatibility.
