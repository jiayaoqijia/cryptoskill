---
name: push-publish
domain: skill-authoring/push-publish
trigger: "Pushing an approved release; writing the commit and tag for a small public repository; publishing notes after the tag exists"
anti_trigger: "Deciding whether the release may ship; verifying the published tree afterwards; repairing content defects found before the push"
scope: "The release mechanics: fetch before building on the remote, commit with a message file, tag the final commit, push without force, publish notes from the changelog"
status: "seedling"
---

# Push and Publish

## Standard

- **git fetch**: the remote is the authority on what exists, so fetch before building on it. <https://git-scm.com/docs/git-fetch>
- **git push**: a non-fast-forward rejection means the remote moved. The answer is to integrate, not to force. <https://git-scm.com/docs/git-push>
- **Conventional Commits 1.0.0**: a structured subject line keeps history readable. <https://www.conventionalcommits.org/en/v1.0.0/>
- **SemVer 2.0.0** and **Keep a Changelog 1.1.0**: the tag and the changelog section state the same claim, so they must agree. <https://semver.org> <https://keepachangelog.com/en/1.1.0/>
- **GitHub Docs, releases**: a release attaches notes and assets to a tag. <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>

## Decision rules

1. Fetch first: the owner may have committed while the audit ran. If the branch moved, integrate on top; never discard the owner's commit.
2. Never force-push. `--force-with-lease` is still a rewrite; it guards a lost update, not the rule.
3. Set the commit identity explicitly; authorship is not a machine default.
4. Pass the message as a file; the body survives quoting and wrapping.
5. Tag the final commit, annotated. If the commit is amended before the push, delete the local tag and re-create it on the new commit.
6. Verify that the tag target equals HEAD before pushing.
7. Notes come from the changelog section for that version, never typed from memory.

## Procedure

1. Fetch and inspect:

   ```
   git fetch origin
   git status -sb
   git log --oneline HEAD..origin/main
   ```

   A non-empty log means the remote moved; integrate first.
2. Set the identity and stage:

   ```
   git config user.name  "Release Bot"
   git config user.email "release@example.invalid"
   git add -A
   git diff --cached --stat
   ```

   Read the staged file list. An unexpected file is a finding, not a bonus.
3. Commit from a file:

   ```
   git commit -F .git/RELEASE_MSG
   ```

   Subject in the imperative; body saying what changed and why, in `type(scope): summary` form when the repo uses it.
4. Tag and verify:

   ```
   git tag -a v1.2.3 -m "v1.2.3"
   git rev-parse HEAD
   git rev-parse 'v1.2.3^{commit}'
   ```

   The two hashes must match.
5. Push the branch, then the tag:

   ```
   git push origin main
   git push origin v1.2.3
   ```

   A rejection means fetch, integrate, re-tag, push. Never force.
6. Set the repository description and topics from the same claim set. Create the release against the tag, with notes copied from the changelog heading for that version. Check the rendered page: tag name, notes, and every link.
7. Upload assets after the tag exists, then re-read the page.

## Anti-patterns

- **Force-push to tidy history.** It deletes commits others built on. Fix: a new commit that corrects the record.
- **Tag on a pre-amend commit.** The tag names a tree nobody reviewed. Fix: re-create the tag on the final commit.
- **Notes typed from memory.** The page becomes a second, unaudited claim set. Fix: copy from the changelog.
- **Branch pushed, tag forgotten.** The code ships and the version does not. Fix: push both and verify both.

## Done checklist

- [ ] Fetched; remote state known; owner commits preserved.
- [ ] Identity set; staged file list expected; message supplied as a file.
- [ ] Tag annotated and pointing at HEAD.
- [ ] Branch and tag pushed without force.
- [ ] Release bound to the tag; notes copied from the changelog.
- [ ] Rendered release page checked, including links.

## Sources

- git fetch: <https://git-scm.com/docs/git-fetch>
- git push: <https://git-scm.com/docs/git-push>
- Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>
- GitHub Docs, about releases: <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>
