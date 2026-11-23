# Profile polish recipe — worked example (account `rivardoad9-source`, 10 Oct 2026)

The ask was "perbagus github gw" (plus a CV and a work report). What actually moved the
needle, in the order that worked, with the commands that were used.

## 0. Inventory first (cheap, one call per repo)

```bash
gh api user --jq '{login,name,bio,company,location,blog,twitter_username,hireable,public_repos}'
gh repo list --limit 60 --json name,description,visibility,isFork,pushedAt,primaryLanguage,repositoryTopics,url \
  --jq '.[] | [.name, (.visibility), (.pushedAt[:10]), ((.primaryLanguage.name) // "none"),
        ((.description) // "TANPA DESKRIPSI"), ([.repositoryTopics[]?.name] | join(",")), .url] | @tsv'
```

Two jq traps: `.repositoryTopics` is `null` when a repo has no topics (`[]?` fixes the
`cannot iterate over: null` abort), and `(.primaryLanguage.name) // "-"` avoids `null` keys.

Read the pins + README sha in the same pass:

```bash
gh api graphql -f query='{ user(login:LOGIN){ pinnedItems(first:10, types:REPOSITORY){ nodes{ ... on Repository { name } } }
  itemShowcase { items(first:10){ nodes{ ... on Repository { name } } } } } }'
gh api repos/OWNER/OWNER/contents/README.md --jq '.sha'
```

## 1. Find the actual gap, not the vibe

For every repo: `gh api repos/O/r/readme --jq .size`. A repo with **no** README answers with a
404 body (`{"message":"Not Found",...}`), which is easy to mistake for a size. In this case the
macro-news repo had a full engine, a PRD, a test suite and a CLAUDE.md — and zero README. That
was the highest-value single edit on the whole account.

Write that README from the repo's own documents (PRD, CLAUDE.md, file tree) plus the module map,
and add a short **"Honest limitations"** section. The PRD here was partly wrong and the code's own
notes said so (no free consensus data → the surprise delta cannot be computed live; the documented
fallback chain was invalid). Quoting the code's real constraints is what makes the repo read as
engineered rather than generated.

## 2. Rewrite the profile README (PUT with sha)

```bash
SHA=$(gh api repos/OWNER/OWNER/contents/README.md --jq '.sha')
gh api -X PUT repos/OWNER/OWNER/contents/README.md \
  -f message="docs: rewrite profile README — projects, now, skills" \
  -f content="$(base64 -w0 README.md)" -f sha="$SHA" \
  --jq '{commit: .commit.sha, url: .content.html_url}'
```

Structure that worked: identity line + contact/links → **Now** (what is being built this month) →
**Selected projects** table (project, what it is, stack) → what I work on → skills → education →
one closing line. Add private/monetised products as a row marked `(private)` with "demo available on
request" rather than pinning or publishing them.

Then verify by re-reading the file, not by trusting the PUT: `gh api .../contents/README.md --jq
'.content' | base64 -d | head -5` and a `curl` of `raw.githubusercontent.com` for the same string.

## 3. Profile fields (bio) need the `user` scope

```bash
gh api -X PATCH /user -f bio="Digital Business student · AI-agent automation for finance, crypto/Web3 & small-business operations · open to remote internships" --jq '.bio'
```

Missing `user` scope = **404** with a body that names the scope. Max 160 chars; squeeze the
keywords a recruiter searches for into it.

## 4. Refresh the Pages portfolio in the same pass

The portfolio URL is pasted in the profile bio, the profile README and the CV, so a stale page is
visible everywhere. Update `index.html` (PUT with its own sha), then wait for the build:

```bash
gh api repos/O/r/pages/builds/latest --jq '{status,created_at}'     # building → built
curl -s https://OWNER.github.io/REPO/ | grep -c "NEW STRING"         # 200 + the new content
```

`status: building` immediately after the push is normal; a README-only repo has no site at all.
Wait for `status: built` before grepping, and grep for a fragment that survives **HTML entity
escaping** — the live file renders `&` as `&amp;`, so a search for `AI Implementation & Automation`
returns 0 matches on a page that is actually deployed. Grep a single escaped-safe word, or reuse the
row's own markup (`AI Implementation &amp; Automation`). Same trap when the same copy is asserted
against `raw.githubusercontent.com` (plain `&`) and the live page (escaped) in one pass.

## 5. Pinning: confirmed impossible via API

`mutation { updateUserPinnedItems(...) }` → `undefinedField` (`Field 'updateUserPinnedItems'
doesn't exist on type 'Mutation'`). `pinnedItems` is read-only. So: recommend an ORDER, tell the
user it is 2 clicks in the web UI (profile → Customize your pins), and note that private repos
cannot be pinned. Do not spend calls probing for another endpoint.

## 6. What to hand back

One message: what changed with links, the manual step that remains (pins), and the one judgment
call the user owns (here: keep the monetised product's code private, show the WHAT only). Verified
state to quote: profile README live, per-repo README live, portfolio page HTTP 200 with the new
content, `pages.status == built`.
