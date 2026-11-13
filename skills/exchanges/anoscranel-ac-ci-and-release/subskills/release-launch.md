---
name: release-launch
domain: software-engineering/release-launch
trigger: "\"cut a release\", \"bump the version\", \"launch checklist\", \"ship to the App Store\", \"stage this rollout\"."
anti_trigger: "Pushing to production hosts (subskills/deployment.md); flipping exposure after deploy (subskills/feature-flags.md); commit messages and changelog text; running the outage; retiring a feature."
scope: "SemVer release cut, launch-readiness checklist, staged and mobile-store rollout"
status: "seedling"
---

# Release & Launch

## Standard

- **SemVer 2.0.0** (https://semver.org/spec/v2.0.0.html): PATCH for compatible fixes, MINOR for added function, MAJOR for a public incompatibility. Pre-release suffixes sort before the release.
- **Release governance**: every artifact is signed; an unsigned artifact is unreleasable. Prefer flag-off or forward-fix over a binary rollback, because an untested rollback fails twice.
- **Two paths after launch**: a normal train for batched changes, a narrow hotfix lane for P1 only. Both ride the same gate.
- **Apple phased release** (https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/): fixed 1/2/5/10/20/50/100 % over 7 days. **Play**: developer-chosen %, manual increases, halt and resume, 100 % terminal.

## Decision rules

1. Cut the version from the change list, never by feel. A breaking public change is MAJOR.
2. Publish the rollback note before the release.
3. Rollback order: flag off, forward-fix, revert the release. Data restore comes last.
4. A hotfix carries only the fix and its regression test.
5. Ramp percentages are gates with a halt rule, not a formality.
6. Never break an old client mid-cycle; announce a sunset first.
7. Store submission and the release cut are **human-gated**.

## Procedure

1. Confirm main is green and the changes are merged.
2. List changes since the last tag: `git log --oneline v1.4.0..HEAD`.
3. Decide MAJOR, MINOR or PATCH from that list.
4. Update the version and the changelog, in the repo's existing format.
5. Build the artifacts and sign each one.
6. Run the release smoke set against the artifact, not against main.
7. Write the rollback note: what breaks, which flag flips, which data needs a restore.
8. Tag and publish: `git tag -a v1.5.0 -m "orders: idempotency key"`.
9. Stage the rollout: server 1 % → 10 % → 50 % → 100 %, holding each step for a full traffic cycle; iOS uses the phased schedule; Android sets a percentage with halt reachable.
10. Compare release metrics against budget at each stage. Over budget → halt.
11. Announce the release. Announcement copy is human-approved.
12. After the ramp, retire the flag.

Mobile extras: the build number rises monotonically, read from the store rather than hardcoded. TestFlight takes 100 internal and 10,000 external users, and builds expire after 90 days. Budget about 12 days before launch and two rejection cycles; ⚠️ the 24-hour review norm is single-sourced.

## Anti-patterns

- Version bumped by feel; a breaking change shipped as MINOR.
- Rollback note written after the release.
- Binary rollback as the first move.
- A hotfix carrying a feature along.
- Ramp set to 100 % at cut time, so the stages prove nothing.
- A hardcoded build number in a mobile pipeline.

## Done checklist

- [ ] Version matches the change list.
- [ ] Artifacts signed; smoke set run against the artifact.
- [ ] Rollback note published before the cut.
- [ ] Ramp stages and halt rule written down.
- [ ] Human approved the cut, submission and announcement.

## Sources

- <https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321670229>
- <https://builtplain.com/app-review-rejection-playbook>
- <https://rootly.com/incident-response/support-levels>
- https://semver.org/spec/v2.0.0.html
