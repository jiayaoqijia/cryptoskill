---
name: write-a-readme-people-finish
description: Use when writing or fixing a project README so a stranger can run the software without asking you anything. Front-loads install, a runnable example, and the one entry point for depth.
---

# Write a README People Finish

A README's job is to take a stranger from clone to a working example with no questions asked. Lead with what it does and how to run it; put reference material after.

## Procedure

1. Write the one-line description first: what it does and for whom, under 120 characters, no marketing. Put it directly under the title.
2. Add an install block that is copy-pasteable and pinned to a version: `pip install acme-tool==1.4.2` or `npm i acme-tool@1.4.2`. Never write "install the usual way".
3. Follow with the smallest runnable example that produces visible output. Three to eight lines, real filenames, expected output in a fenced block.
4. Add a Requirements line with concrete versions: `Python >= 3.11, Postgres >= 14`. Unstated prerequisites are the top reason a README fails.
5. Link a single entry point for depth, `docs/` or a wiki, rather than pasting the whole manual.
6. Include a license line and the exact command to report a bug (the issue URL).
7. Place badges under the title but keep them to build status, version, and license; drop vanity badges.
8. State the supported platforms explicitly: `Linux, macOS; Windows via WSL2`.
9. Add a short "why this exists" of two sentences at most, after the quickstart, for the curious reader.
10. Verify by following your own README in a clean container and fixing every command that fails.
11. Keep the README under about 200 lines; move reference tables to `docs/`.
12. Re-read it as the last commit before tagging a release and fix anything that drifted.

## Pitfalls

- "Simply install and run" with no commands, assuming knowledge the reader does not have.
- A quickstart that depends on environment variables set only on your machine.
- Screenshots of install steps that go stale the moment the UI changes; use text.
- Burying the run command below three paragraphs of origin story.
- Claiming support for versions the CI never tested.
- An example that reads a file not present in the repo, so it fails on the first run.
- A license section that names the file but not the license, forcing a second click.

## Verification

    docker run --rm -v "$PWD:/w" -w /w python:3.11 bash -c 'pip install -e . && python examples/hello.py'

Run the README top to bottom in a clean environment; it passes when every command succeeds without edits and the example prints the documented output.
