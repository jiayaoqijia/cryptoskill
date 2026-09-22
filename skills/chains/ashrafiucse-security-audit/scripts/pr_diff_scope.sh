#!/usr/bin/env bash
# pr_diff_scope.sh [base-ref] — incremental-audit scoper. READ-ONLY.
# Prints BASE, changed files since base, and which sibling skills apply.
# Never writes: git is called with --no-optional-locks and diff/rev-parse only.
set -euo pipefail

base="${1:-origin/main}"
if ! git rev-parse --verify --quiet "$base" >/dev/null 2>&1; then
  for fb in origin/main origin/master main master; do
    if git rev-parse --verify --quiet "$fb" >/dev/null 2>&1; then base="$fb"; break; fi
  done
fi
mb="$(git merge-base "$base" HEAD 2>/dev/null || echo "$base")"

echo "BASE=$base (merge-base: $mb)"
echo "--- changed files (added/copied/modified) ---"
git --no-optional-locks diff --name-only --diff-filter=ACMR "$mb" HEAD

echo "--- skill dispatch (file -> skills) ---"
skills_for() {
  case "$1" in
    *.blade.php|artisan|composer.json|composer.lock|*.php) echo laravel-security ;;
    manage.py|settings.py|urls.py|wsgi.py) echo django-security ;;
    Gemfile*|*.rb|Rakefile) echo rails-security ;;
    pom.xml|build.gradle*|*.java) echo spring-security ;;
    *.graphql) echo graphql-security ;;
    package.json|package-lock.json|yarn.lock|pnpm-lock.yaml|\
    requirements*.txt|Pipfile*|pyproject.toml|poetry.lock|\
    Cargo.toml|Cargo.lock|go.mod|go.sum|*.csproj|pubspec.yaml|mix.exs)
      echo dependency-vulns ;;
    Dockerfile*|docker-compose*|*.tf) echo container-iac-security ;;
    k8s/*.yaml|k8s/*.yml|*.service) echo container-iac-security config-hardening ;;
    .env*|*.conf|nginx*|*.toml|*.yaml|*.yml) echo config-hardening ;;
    AndroidManifest.xml|Info.plist|*.kt|*.swift) echo mobile-security ;;
    *controller*|*routes*|middleware*|*policy*|*guard*) echo auth-review flow-security ;;
    *.tsx|*.jsx|*.ts|*.js) echo injection-flaws auth-review ;;
    *.py) echo injection-flaws data-exposure ;;
    *.md) echo "" ;;
    *) echo "" ;;
  esac
}

manifests_changed=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in
    package.json|package-lock.json|yarn.lock|pnpm-lock.yaml|requirements*.txt|\
    Pipfile*|pyproject.toml|poetry.lock|Cargo.*|go.*|pom.xml|build.gradle*|\
    composer.json|composer.lock|*.csproj|pubspec.yaml|mix.exs|Gemfile*)
      manifests_changed=1 ;;
  esac
  for s in $(skills_for "$f"); do
    [ -n "$s" ] && printf '%s\t%s\n' "$s" "$f"
  done
done < <(git --no-optional-locks diff --name-only --diff-filter=ACMR "$mb" HEAD) | sort -u

echo "--- always ---"
echo -e "secrets-detection\t(added lines of every changed file)"
[ "$manifests_changed" -eq 1 ] && echo -e "dependency-vulns\t(manifest/lockfile changed)"
exit 0
