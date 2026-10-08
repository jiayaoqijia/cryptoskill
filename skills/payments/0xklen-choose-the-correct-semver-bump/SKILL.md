---
name: choose-the-correct-semver-bump
description: Use when deciding whether a release is a major, minor or patch. Diffs the public surface against the previous release and maps the change class to semver, including 0.x rules.
---

# Choose the Correct Semver Bump

The version number is a contract with consumers. Guessing "patch" for a breaking change breaks everyone who trusted the number. Decide from the actual API diff, not from the size of the commit.

## Procedure

1. Generate the public-surface diff between the last release and HEAD:
   - Rust: `cargo public-api diff <prev>` or `cargo semver-checks check-release`.
   - Go: `go-apidiff v1.2.0 HEAD` or `apidiff -w` with `golang.org/x/exp/apidiff`.
   - TypeScript: `api-extractor run --local` then diff the `.api.md` report.
   - Java: `japicmp -o old.jar -n new.jar` prints added/removed/changed members.
2. Classify each change:
   - Removing or renaming an exported symbol, tightening a parameter type, or adding a required argument → **MAJOR**.
   - Adding an exported symbol, an optional parameter with a default, or a new enum member consumers may match on → **MINOR**.
   - Fixing behaviour that did not match docs, perf work, internal refactor → **PATCH**.
3. Read the changelog for behavioural breaks the API diff cannot see: changed default values, stricter validation, a different error type. These are MAJOR even though signatures are unchanged.
4. Apply the 0.x rule: while `major == 0`, a MINOR bump may break compatibility. Still bump MINOR for additions and PATCH for fixes; document breaks in the changelog.
5. If both a break and an addition landed, the bump is MAJOR — the highest class wins.
6. Record the decision in the PR: "MAJOR because `parseConfig` gained a required `opts` argument."
7. Use `cargo semver-checks`/`japicmp` in CI as a gate; let a tool catch the missed bump.

## Pitfalls

- Adding a method to an interface others implement is a break for implementers, even though it is "additive" for callers.
- Changing an error message that tests assert on is a break for those consumers; keep messages stable or gate them.
- Pre-release identifiers order oddly: `1.0.0-rc.2` precedes `1.0.0`, and `1.0.0-alpha` < `1.0.0-beta`.
- Build metadata (`+build.5`) is ignored in precedence, so it can never carry a compatibility signal.
- Bumping two of three numbers (`1.2` → `1.3.0` vs `1.2.0` → `1.3.0`) signals the wrong thing; always three.

## Verification

    cargo semver-checks check-release   # or: japicmp -o prev.jar -n new.jar --only-modified

The tool reports the required bump as MAJOR/MINOR/PATCH; confirm it matches the version you wrote in the manifest.

Report: "Choosing <major|minor|patch> <old>→<new>: `<tool>` reports <N> breaking and <M> additive changes, breaks are <list>."
