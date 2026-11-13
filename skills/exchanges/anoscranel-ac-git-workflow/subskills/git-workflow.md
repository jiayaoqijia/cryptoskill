---
name: git-workflow
domain: software-engineering/git-workflow
trigger: "\"Which branching model\", \"trunk-based or GitFlow\", \"set up branch protection\", \"add a merge queue\", \"set up CODEOWNERS\", \"monorepo or polyrepo\"."
anti_trigger: "Writing or repairing individual commits (subskills/commits-history.md); preparing one PR; pipeline job design."
scope: "Branching model, trunk-based work, merge queues, CODEOWNERS, monorepo layout"
status: "seedling"
---

# Git Workflow

## Standard

- **Trunk-based development**: small batches merged to trunk at least daily, three or fewer active branches, main always green (https://dora.dev/capabilities/trunk-based-development/; https://trunkbaseddevelopment.com).
- Trunk-based work *correlates* with higher delivery performance (*Accelerate*, 2018). Not causal.
- **GitFlow** (Driessen 2010) fits versioned, packaged releases; its author later advised against it for continuous delivery (⚠️ secondary).
- **GitHub flow**: short branch → PR → merge (https://docs.github.com/en/get-started).
- **Merge queues**: GitHub merge queue GA 2023; Google and Meta ran them for years.
- **CODEOWNERS** maps paths to owners for auto-review requests (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

## Decision rules

1. Default: trunk-based with short-lived branches (hours to one day) and feature flags.
2. Add a thin release branch only for versioned libraries, mobile apps or supported old versions.
3. Protect main: require PR, required status checks, linear history or squash, no force-push, no direct push. An agent never pushes to main.
4. Add a merge queue when main breaks from semantically conflicting merges, or when more than a few PRs merge per hour. ⚠️ House trigger.
5. Every directory has an owner in CODEOWNERS. Owners are teams, not one person.
6. Monorepo when changes often cross projects, libraries are shared and CI can test affected targets only. Polyrepo when compliance fences, open-source surfaces or very different toolchains apply. Past ~500 engineers expect a hybrid (⚠️ secondary).
7. Monorepo CI tests affected targets only (`nx affected`, `turbo --filter`, Bazel rdeps).
8. Merging into protected main is **human-gated**.

## Procedure

1. Write the policy in `CONTRIBUTING.md`: model, branch naming (`feat/…`, `fix/…`), max branch age, merge method.
2. Configure protection on main (GitHub: Settings → Rules → Rulesets):
 - require a pull request and at least 1 approval;
 - require status checks: lint, typecheck, test, build;
 - require linear history or squash merge;
 - block force-push and deletion.
3. Create `.github/CODEOWNERS`:
   ```text
   *                @org/platform
   /services/billing/ @org/billing
   /docs/adr/       @org/architects
   ```
 Turn on "require review from code owners".
4. If rule 4 applies, enable the merge queue and add the `merge_group` event to required workflows.
5. Set a stale-branch rule: list branches older than the limit each week (`git for-each-ref --sort=committerdate refs/remotes`). Merge, flag or delete them (delete with the owner's OK).
6. For a monorepo: set up workspace tooling and affected-target CI before adding projects.
7. Review the policy each quarter against branch age and main break rate.

## Anti-patterns

- Long-lived `develop` branches for a SaaS app.
- Admin bypass used routinely.
- CODEOWNERS pointing at one person.
- Monorepo that runs every test on every commit.
- Force-push to shared branches.

## Done checklist

- [ ] Branching model written down.
- [ ] Main protected with required checks; no direct or force-push.
- [ ] CODEOWNERS covers every path.
- [ ] Merge queue on, or a reason it is not needed.
- [ ] Stale-branch review scheduled.

## Sources

- <https://sazardev.netlify.app/blog/en/go-at-scale-uber-engineering-workflow-patterns>
- <https://github.blog/developer-skills/github/write-better-commits-build-better-projects/>
- https://dora.dev/capabilities/trunk-based-development/
