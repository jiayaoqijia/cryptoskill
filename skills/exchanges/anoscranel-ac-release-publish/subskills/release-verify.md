---
name: release-verify
domain: skill-authoring/release-verify
trigger: "The release is pushed and the published tree must be checked; installed copies may differ from the public files; closing a release record with evidence"
anti_trigger: "Pushing the release; reviewing evidence before the push; building the original claim inventory"
scope: "Verifying the published tree from a fresh clone, checking the release page, syncing installed copies through the install gate, and closing with lessons"
status: "seedling"
---

# Release Verify

## Standard

- **SLSA**: verification runs against the published artifact and its provenance, not the directory where it was built. <https://slsa.dev>
- **Reproducible builds**: a clean-room checkout is the honest test surface, because it holds only what was published. <https://reproducible-builds.org/>
- **git clone**: a fresh clone receives the pushed refs and nothing from the local working tree. <https://git-scm.com/docs/git-clone>
- ⚠️ House convention: installed copies are synced through the install gate, never by hand.

## Decision rules

1. Verify from a fresh clone in a scratch directory. Never verify the working copy.
2. Re-run every gate against the clone. A pass before the push is not evidence about the published tree.
3. Compare file lists and content hashes between clone and working tree. A difference is a missed add or a leaked private file.
4. Check the release page as a claim set: tag name, notes, links, assets.
5. Install through the gate, not by copying files.
6. Compare installed files with the public files by hash after install.
7. Close with evidence per item; anything open gets a named next release. Record the lessons: what the gates missed, what the audit caught, what the repair broke.

## Procedure

1. Make a scratch directory and clone:

   ```
   scratch=$(mktemp -d)
   git clone <url> "$scratch/checkout"
   cd "$scratch/checkout"
   git rev-parse HEAD
   ```

2. Compare the clone's HEAD with the release tag and the hash the gate approved. All three must match.
3. Run the gate suite inside the clone: structure, security, strict YAML, links, private data. The commands match the pre-push run; only the tree is different.
4. Compare trees: `git ls-files | sort` in the clone and in the working tree, then diff the two lists. A file only in the working tree was never published; a file only in the clone came from somewhere else.
5. Read the release page once: title, tag, notes against the changelog section, and every link in the notes.
6. Install through the gate from the clone or the public URL. Hash-compare the installed files with the clone, then run the gate's verification step; a tampered file must fail it.
7. Re-run claim proofs that depend on installation, such as a version string printed by the installed copy.
8. Remove the scratch directory.
9. Write the close record: version, tag, commit hash, gates run, audit verdict, install result, open items, lessons.

## Anti-patterns

- **Verifying the working copy.** Untracked fixes make it pass. Fix: clone.
- **`git status` clean read as proof of the push.** It describes the local repository only. Fix: compare the clone.
- **Hand-copying into the install location.** The copy skips every check and drifts immediately. Fix: install through the gate.
- **Skipping the release page.** The notes are a claim set too. Fix: read the rendered page.

## Done checklist

- [ ] Fresh clone made; HEAD matches the tag and the approved hash.
- [ ] Every gate re-run inside the clone and passing.
- [ ] File lists compared between clone and working tree.
- [ ] Release page read: tag, notes, links, assets.
- [ ] Installed copies synced through the gate; hashes match.
- [ ] Scratch directory removed.
- [ ] Close record written with hash, results, open items, lessons.

## Sources

- SLSA: <https://slsa.dev>
- Reproducible builds: <https://reproducible-builds.org/>
- git clone: <https://git-scm.com/docs/git-clone>
- GitHub Docs, managing releases: <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository>
