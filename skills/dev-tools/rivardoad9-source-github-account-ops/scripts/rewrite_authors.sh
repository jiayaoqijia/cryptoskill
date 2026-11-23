#!/usr/bin/env bash
# Rewrite commit authorship across repos with git-filter-repo, then push and realign
# any live clone of the same repo.
#
# Usage:
#   MMLINE='Rivardo <306490977+login@users.noreply.github.com>' \
#   REMOTE_URLS='https://github.com/OWNER/REPO.git' \
#   LIVE_CLONES='/home/ubuntu/REPO' \
#   bash rewrite_authors.sh
#
# The mailmap shorthand "Name <proper@email> <commit@email>" rewrites every commit
# whose author/committer email matches, whatever the name was.
set -u
OWN=${OWN:-}
FR=$HOME/.local/bin/git-filter-repo
[ -x "$FR" ] || { echo "install git-filter-repo:"; echo "  curl -sL -o ~/.local/bin/git-filter-repo https://raw.githubusercontent.com/newren/git-filter-repo/main/git-filter-repo && chmod +x ~/.local/bin/git-filter-repo"; exit 1; }
export FILTER_BRANCH_SQUELCH_WARNING=1

# 1) collect the identities you want gone
#    git -C <repo> log --all --format='%an|%ae' | sort -u
MM=${MM:-/tmp/gh_mailmap.txt}
cat > "$MM" <<EOF
Rivardo <306490977+rivardoad9-source@users.noreply.github.com> <ubuntu@localhost.localdomain>
Rivardo <306490977+rivardoad9-source@users.noreply.github.com> <hermes@local>
Rivardo <306490977+rivardoad9-source@users.noreply.github.com> <noreply@anthropic.com>
Rivardo <306490977+rivardoad9-source@users.noreply.github.com> <your-email@example.com>
EOF

for url in ${REMOTE_URLS:-}; do
  repo=$(basename "$url" .git); d=/tmp/rw/$repo
  echo "──── $repo ────"
  rm -rf "$d"; mkdir -p /tmp/rw
  git clone -q --no-single-branch "$url" "$d" || { echo "  clone gagal"; continue; }
  ( cd "$d"
    echo "  sebelum: $(git log --all --format='%an' | sort -u | tr '\n' ',')"
    $FR --mailmap "$MM" --force >/dev/null 2>&1 || { echo "  filter-repo gagal"; exit 1; }
    echo "  sesudah: $(git log --all --format='%an|%ae' | sort -u | tr '\n' ',')"
    # filter-repo REMOVES origin -> push by URL
    git push --force "$url" --all >/dev/null 2>&1 && echo "  push branches OK" || echo "  push branches GAGAL"
    git push --force "$url" --tags >/dev/null 2>&1
  )
done

# 2) realign live clones (cron engines, vault sync) so their next push doesn't diverge
for live in ${LIVE_CLONES:-}; do
  [ -d "$live/.git" ] || continue
  echo "──── realign $live ────"
  git -C "$live" fetch --all --prune -q
  git -C "$live" reset --hard "$(git -C "$live" rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo origin/main)" >/dev/null 2>&1 \
    && echo "  ok: $(git -C "$live" log -1 --format='%an <%ae>')"
  echo "  selisih vs upstream: $(git -C "$live" rev-list --left-right --count @{u}...HEAD 2>/dev/null)"
done
echo "=== verify each pushed repo: HEAD == origin/<branch>, '%an <%ae>' = new identity ==="
