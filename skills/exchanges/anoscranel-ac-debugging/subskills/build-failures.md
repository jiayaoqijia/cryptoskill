---
name: build-failures
domain: software-engineering/build-failures
trigger: "\"CI is red\", \"the build is broken\", \"main is broken\", \"works on my machine but not in CI\", \"the pipeline started failing overnight\", \"dependency install fails\"."
anti_trigger: "A product bug that tests catch correctly (subskills/debugging.md); one test failing at random; designing the pipeline itself."
scope: "Triage of a broken build or red pipeline: classify, isolate, restore green"
status: "seedling"
---

# Build Failures

## Standard

- **Main stays releasable**: every commit should leave the pipeline releasable (Humble & Farley, *Continuous Delivery*, 2010).
- **Restore first, investigate second**.
- **Not every red is the product**: 26% of non-flaky CI failures were wrong or obsolete tests; 19.3% of failed builds were fixed by editing the test (Hilton et al., FSE 2017).
- **Merge queues** stop "green alone, red together" breaks by testing the merged result.

## Decision rules

1. Main red → restore green within the hour. ⚠️ House target. Revert the offending commit first; fix forward only if the fix is one small obvious change.
2. Classify before you dig. Five classes:
 - **code**: a test or compile error caused by the change;
 - **test**: the test is wrong or obsolete;
 - **flake**: passes on rerun of the same commit (out of scope for this leaf: the flake triage loop);
 - **environment**: runner image, toolchain, service, network, quota, secret expiry;
 - **dependency**: a new upstream version, a yanked package, a registry outage.
3. One rerun is allowed to test the flake class. A second rerun without new information is forbidden.
4. "Passes locally, fails in CI" → diff versions, env vars, OS, timezone, locale, CPU count, file-system case.
5. Every branch fails at once with no code change → environment or dependency.
6. Suspect unpinned dependencies and mutable action tags first.
7. Disabling a check or skipping a test needs a ticket, an owner and a human decision.
8. After restore, add a guard against the class.

## Procedure

1. Read the first error in the log, not the last. Note the job, step and command.
2. Scope it: main too? Other branches? Last green run?
3. Rerun once. Passes → flaky class; quarantine path.
4. Reproduce locally with CI's exact command and versions:
   ```bash
   docker run --rm -it -v "$PWD":/w -w /w <ci-image> bash -lc '<ci command>'
   ```
5. Diff the last green and first red run: commits, lockfile, runner image, tool versions, cache key.
   ```bash
   git log --oneline <last-green>..<first-red>
   git diff <last-green> <first-red> -- package-lock.json poetry.lock go.sum
   ```
6. Act by class. Code → revert or fix. Test → repair it, reason in the commit. Dependency → pin the last good version; open an upgrade ticket. Environment → pin the image or tool; credential renewal is **human-gated**.
7. Re-key the cache if it may be corrupt.
8. Confirm main green. Note cause class, fix and guard.
9. Add the guard: pin, lockfile check, merge queue, required check, image digest.

## Anti-patterns

- Rerunning until green.
- Large fix-forward while main stays red.
- Commenting out the failing test.
- `latest` tags and floating dependency ranges.

## Done checklist

- [ ] Failure classified into one of five classes.
- [ ] Main green again; revert used if the fix was not trivial.
- [ ] Cause and fix noted.
- [ ] Guard added against the class.
- [ ] No check disabled without a ticket and human approval.

## Sources

- <https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321670229>
- <https://docs.github.com/en/actions/administering-github-actions/usage-limits-billing-and-administration>
- <https://2025.msrconf.org/details/msr-2025-technical-papers/24/Understanding-Test-Deletion-in-Java-Applications>
- <https://codeclaritylab.com/glossary/bus_factor>
