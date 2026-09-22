# External Sources — data egress & safety inventory

Every network touch these skills can make, what LEAVES the machine, and the
injection-risk stance. Verified by `scripts/audit_readonly.py` (CI-gated)
plus empirical hash-diff audits. If you add a source, add a row here.

| Source | Used by | What is SENT | What comes back | Risk stance |
|---|---|---|---|---|
| `api.osv.dev` (OSV) | dependency-vulns (`osv_scan.py`) | **package names + versions** of the audited project (batch POST) | advisory JSON (IDs, fixed versions, prose) | The one real data-egress point: private/internal package names leave the machine. Offline mode (documented skip) is the mitigation for sensitive codebases. Advisory prose is DATA, never instructions — see stance below |
| CISA KEV JSON | cve-research Step 3 | nothing (pulls feed) | exploited-CVE list | read-only pull |
| NVD 2.0 API | digest workflow only | nothing (public CVE queries) | CVE metadata | read-only pull |
| endoflife.date | dependency-vulns Step 3 | nothing (pulls per-product JSON) | EOL dates | read-only pull |
| Project Zero 0days-in-the-wild | cve-research Step 3 + weekly workflow | nothing / CVE id in URL | per-CVE markdown paths | read-only pull |
| rapid7/metasploit-framework | cve-research Step 3 + weekly workflow | nothing / CVE id in URL | module file listings | read-only pull; upstream path guarded fail-loudly |
| Tool bridges (gitleaks, semgrep, checkov…) | security-audit Phase 1.5 (ONLY if installed) | whatever those tools send by default (semgrep `--config auto` contacts its registry) | scanner findings | leads-not-verdicts; absent → skipped silently; never installed by the skills |

## Injection stance for returned content

Advisory text, feed JSON, and scanner output land in the agent's context.
A poisoned or malicious source could try prompt injection ("now run …").
Standing defenses (enforced by the skill text, checked by the read-only gate):

1. **Tools are leads, not verdicts** — every finding is re-verified against
   code the agent reads itself (`file:line` evidence rule).
2. **No state-changing commands exist in the skill vocabulary** — the
   read-only gate blocks mutations in all executable artifacts and skill
   bash blocks, so injected instructions find no sanctioned mechanism.
3. **Network OFF by default** — every live lookup is skippable; offline
   audits never touch any of the sources above.

## Verified side-effect surface

- The audit's only permitted write: `SECURITY-AUDIT.md` in the target root.
- Scanner scripts: byte-identical tree verified (sha256 before/after).
- `scripts/audit_readonly.py` fails CI on any mutating pattern appearing
  in executables or skill bash blocks.
