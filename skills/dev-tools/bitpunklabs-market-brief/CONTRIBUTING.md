# Contributing

Report a concrete problem or propose a focused improvement. You do not need to
write code: your request, an affected report excerpt, and a reliable source are useful.
Be considerate in discussions and remove personal information and credentials.

## Prompt changes

`assets/prompts/` is the single source of truth. Keep each prompt complete and
independently usable. Preserve its coverage, analytical depth, time boundaries,
measurement distinctions, source requirements, and readable output.

Distinguish an execution mistake from a prompt defect before editing. Explain the
specific issue and change only what addresses it. A user's focus adds depth;
restricted coverage is a separate instruction. Explicit user parameters override defaults.

Review the affected scenario and any neighboring scenario the change could affect.
Record the prompt version, date/cutoff, model, and source access for report comparisons.
Text review and offline package checks do not establish live report quality.
Keep model-produced reports, personal inputs, and local experiments out of the release.

## Local checks

Development utilities use Python 3.10+ and the standard library. They are not
needed to run the skill.

```sh
python scripts/check.py
python -m unittest discover -s tests -v
python scripts/package_release.py --output dist
```

The check validates routing, local links, metadata, and package boundaries. The
builder checks again, creates an installable ZIP and SHA256SUMS, and verifies the
archive's bytes against the source files. Use a new or empty output directory.
GitHub Actions runs the same commands on pushes and pull requests.

## Releases

Update `metadata.version` in `SKILL.md` and [CHANGELOG.md](CHANGELOG.md) together.
Use semantic versions and immutable `vX.Y.Z` tags. Check the final commit in CI
before tagging. Package from that clean, tagged commit and publish the ZIP and
SHA256SUMS with the release notes.

The release workflow validates the matching version/tag and attaches packages
when a GitHub Release is published. Marketplace listings are separate publication
steps; this repository does not imply registration or review on those services.
