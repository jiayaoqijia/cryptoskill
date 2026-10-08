---
name: test-code-blocks-in-docs
description: Use when documentation contains code samples that must keep working. Extracts every fenced block and executes it in CI against the release version the docs claim.
---

# Test Code Blocks in Docs

A code sample that does not run is worse than none: it teaches the wrong API and burns the reader's first ten minutes. Execute every block in CI.

## Procedure

1. Tag fenced blocks so an extractor knows which run and which are output: mark runnable ones with the word exec after the language, leave output blocks untagged.
2. Write an extractor that pulls only runnable blocks into temp files, preserving order per document:
   `awk '/^```bash exec/{f=1;next}/^```/{f=0}f' docs/quickstart.md`
3. Run each in the CI environment with the same dependency versions the docs claim, pinned in the same lockfile the library uses.
4. Assert exit code 0 and, where the block prints, compare against the adjacent output block.
5. Skip blocks that need live credentials by tagging them needs-secret and running them only in a nightly job.
6. Fail the build on any block that errors; a broken sample is a release blocker, not a warning.
7. Cover the README, `docs/`, and long tutorials; the README's first block is the highest-value one to test.
8. Update the sample the moment the API changes; a rename PR should touch the docs and still pass the check.
9. Keep extraction deterministic: strip trailing whitespace and normalise shell prompts so output comparison is stable.
10. Give each block a stable id (file path plus index) so a failure names it precisely.
11. Report per-block pass/fail so a red build names the exact file and line.
12. Run the check on a schedule even without a PR, so drift from a dependency bump is caught.

## Pitfalls

- Extracting illustrative fragments that lack context, then failing the build on them.
- Comparing output that contains timing, IDs, or paths that vary run to run; normalise first.
- Running against main dependencies while the doc pins an older version the reader will use.
- Blocks that pass by exiting 0 while printing an error page.
- A sample that needs network and breaks CI when the registry rate-limits.
- Treating a red block as flaky and skipping it, which is how samples rot.
- Testing the code in isolation from the prose, so a correct snippet sits under wrong instructions.

## Verification

    for b in /tmp/docblocks/*; do bash "$b" >/dev/null 2>&1 || echo "FAIL $b"; done

Empty output means every extracted block executed cleanly. Report the number of blocks executed and any that failed with their file and line, not "docs are fine".
