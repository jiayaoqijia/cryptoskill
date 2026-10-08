---
name: triage-dependency-cves
description: Use when a scanner reports CVEs in installed dependencies and you must decide what to patch now. Ranks by reachability and exploitability, not raw CVSS, and pins the fix.
---

# Triage dependency CVEs

A CVE list is an inventory, not a work queue. Most reported CVEs are unreachable in your code, and
chasing them all burns time while a reachable one waits. Rank by whether the vulnerable function is
actually called with attacker input.

## Procedure

1. Produce the inventory with a scanner that knows your lockfile, plus OSV for advisory detail:

       pip-audit -r requirements.txt -f json -o /tmp/pipaudit.json
       npm audit --json > /tmp/npm-audit.json
       osv-scanner --lockfile=poetry.lock --format json > /tmp/osv.json
       grype dir:. -o json > /tmp/grype.json        # catches OS packages too

2. Extract the actionable set: only findings with a fix version available.

       jq -r '.dependencies[] | select(.vulns) | .name as $n | .vulns[] | "\($n) \(.id) \(.fix_versions|join(","))"' /tmp/pipaudit.json

3. For each, check reachability. Does your code import and call the vulnerable module? Search:

       rg -n "import <pkg>|require\(['\"]<pkg>" src/ | head

   A vulnerable transitive dep never on a code path is a lower priority than a direct dep in a
   request handler.

4. Weigh severity with exploitability context, not CVSS alone: check EPSS (probability of
   exploitation in the next 30 days) and whether a public PoC exists:

       curl -s "https://api.first.org/data/v1/epss?cve=CVE-2021-44228" | jq '.data[0].epss'

5. Rank into three buckets: patch now (reachable + RCE/SSRF/authz bypass), patch this sprint
   (reachable + DoS/info), track (unreachable or no fix).

6. Apply the fix by bumping the version and re-resolving, then confirm the lockfile moved:

       pip install --upgrade 'package==<fixed>' && pip freeze > requirements.txt

7. If no fix exists, mitigate: disable the feature, add an input filter, or vendor a patch, and
   record it with a review date.

## Pitfalls

- `npm audit fix --force` can jump a major version and break the build; read the semver delta.
- Reachability is not "is it in the lockfile" — a transitive dep under a code path you invoke
  counts.
- Scanner databases lag; cross-check a suspicious finding against the upstream advisory page.
- A pinned-and-old direct dependency hides its own outdated transitive graph; scan the resolved
  tree, not just top-level names.
- Dev-only dependencies rarely ship, but they can poison CI or the build image.
- Automerge bots that bump everything create churn without reducing reachable risk.

## Verification

    grype dir:. -o json | jq -r '[.matches[] | select(.vulnerability.severity=="High" or .vulnerability.severity=="Critical")] | length'
    git diff --stat -- '*lock*' 'requirements*.txt'

Pass: the count of remaining High/Critical matches is the documented, justified set (unreachable or
no-fix), and the lockfile diff shows the applied bumps. Report the buckets, the patches applied, and
the tracked-but-unpatched items with reasons.
