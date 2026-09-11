---
name: git-helper
description: "Common git commands, workflows, and troubleshooting for everyday development"
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🔀",
        "requires": { "bins": ["git"] },
        "credentials": [],
      },
  }
---
# Git Helper

Quick reference for common git operations, workflows, and fixes.

## Daily Workflow

```bash
# Start your day - pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/my-new-feature

# Stage and commit changes
git add -A
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-new-feature
```

## Commit Message Convention

Follow conventional commits for clean history:

```bash
# Format: type(scope): description

git commit -m "feat: add user authentication"
git commit -m "fix: resolve login redirect bug"
git commit -m "docs: update API documentation"
git commit -m "style: format code with prettier"
git commit -m "refactor: simplify database queries"
git commit -m "test: add unit tests for auth module"
git commit -m "chore: update dependencies"
```

## Undo Mistakes

```bash
# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset HEAD~1

# Discard all local changes
git checkout -- .

# Discard changes to specific file
git checkout -- path/to/file

# Undo a pushed commit (creates new commit)
git revert HEAD

# Amend last commit message
git commit --amend -m "new message"
```

## Branch Management

```bash
# List all branches
git branch -a

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Rename current branch
git branch -m new-name

# Switch to previous branch
git checkout -

# Create branch from specific commit
git checkout -b new-branch abc1234
```

## Stashing

```bash
# Stash current changes
git stash

# Stash with message
git stash push -m "work in progress on feature X"

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop a stash
git stash drop stash@{0}
```

## Viewing History

```bash
# Pretty log
git log --oneline --graph --decorate -20

# Log with stats
git log --stat -5

# Search commits by message
git log --grep="bug fix"

# Show commits by author
git log --author="Ian"

# Show changes in commit
git show abc1234

# Blame a file (who changed what)
git blame path/to/file
```

## Merging & Rebasing

```bash
# Merge branch into current
git merge feature-branch

# Rebase onto main (cleaner history)
git rebase main

# Interactive rebase (squash commits)
git rebase -i HEAD~3

# Abort a merge/rebase
git merge --abort
git rebase --abort

# Continue after resolving conflicts
git rebase --continue
```

## Working with Remotes

```bash
# List remotes
git remote -v

# Add remote
git remote add upstream https://github.com/openclaw/openclaw.git

# Fetch from all remotes
git fetch --all

# Pull from upstream
git pull upstream main

# Push to different remote
git push upstream feature-branch
```

## Cherry Pick

```bash
# Apply specific commit to current branch
git cherry-pick abc1234

# Cherry pick without committing
git cherry-pick -n abc1234

# Cherry pick range of commits
git cherry-pick abc1234..def5678
```

## Clean Up

```bash
# Remove untracked files (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Prune remote tracking branches
git remote prune origin

# Garbage collect
git gc
```

## Diff & Compare

```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged

# Compare branches
git diff main..feature-branch

# Compare with remote
git diff origin/main

# Show changed files only
git diff --name-only
```

## Tags

```bash
# Create tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push origin --tags

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## Troubleshooting

```bash
# Fix "detached HEAD"
git checkout main

# Recover deleted branch
git reflog
git checkout -b recovered-branch abc1234

# Find lost commits
git fsck --lost-found

# Reset to remote state
git fetch origin
git reset --hard origin/main
```

## Git Aliases

Add to `~/.gitconfig`:

```ini
[alias]
  co = checkout
  br = branch
  ci = commit
  st = status
  lg = log --oneline --graph --decorate -20
  unstage = reset HEAD --
  last = log -1 HEAD
  amend = commit --amend --no-edit
```

## Tips

- Always pull before starting new work
- Commit early and often
- Write meaningful commit messages
- Use branches for features/fixes
- Never force push to shared branches
- Review changes before committing with `git diff`

## Resources

- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)
