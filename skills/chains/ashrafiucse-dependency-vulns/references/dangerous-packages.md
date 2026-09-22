# Dangerous Packages Pack — risk beyond CVE scanning

OSV/npm-audit answer "does this version have a published advisory?" — they
are silent on: discontinued-but-unpatched packages, compromised releases
that never got a CVE, packages that are only dangerous in HOW they're used,
and code VENDORED into the repo (invisible to manifest scanners entirely).
This pack covers the four classes. Load it with Step 2.7 of `../SKILL.md`.

## 1 — Discontinued / unfixable: flag regardless of advisory state

| Package | Why it's a finding | Detection | Fix |
|---|---|---|---|
| `vm2` (npm) | DISCONTINUED (Jul 2023). Multiple sandbox escapes (CVE-2023-30547/29199/37903 family); later escapes shipped AFTER the last release — any version is unpatched-by-design | `rg -n '"vm2"' package*.json; rg -n "require\(['\"]vm2['\"]\)|new VM\(" ` | migrate to `isolated-vm`, or OS process/containers with dropped privileges. Running untrusted code "in vm2" = HIGH now |
| `request` (npm) | Deprecated (2020), unmaintained; known issues will never be fixed (e.g. CVE-2023-28155 SSRF via redirect) | `rg -n '"request"' package*.json; rg -n "require\(['\"]request['\"]\)"` | `undici`/native fetch/`got`; short-term: disable redirect-following on user URLs |
| `node-uuid` | Renamed `uuid`; frozen old name | manifest grep | `uuid@8+` |
| `querystring` (npm) | Legacy API, unexpected prototype behavior | manifest grep | `URLSearchParams` / `qs` current |
| `moment` | Maintenance mode (project's own notice) — LOW/MEDIUM hygiene | manifest grep | `dayjs`/`luxon`/Intl |
| `faker`/`colors` post-2022 | Maintenance-dead after the self-sabotage incident family | manifest grep | modern alternatives |

Rule: discontinued + security-relevant usage (executes code, parses input,
makes requests) → **High**; discontinued + passive utility → MEDIUM note.

## 2 — Compromised-release history: exact versions, often NO CVE

These shipped malware in specific releases — version greps catch them even
with zero network and zero advisories:

| Package | Malicious versions | Payload |
|---|---|---|
| `event-stream` | 3.3.6 (via `flatmap-stream`) | wallet theft (targeted a Bitcoin copay dev) |
| `ua-parser-js` | 0.7.29, 0.8.1, 1.0.12 | cryptominer + credential dropper |
| `eslint-scope` | 3.7.2 | postinstall npm token exfiltration |
| `coa`, `rc` | one 2021 release each | environment/token exfiltration (stole npm tokens from CI) |
| `node-ipc` | 11.x ("protestware") | wiped/overwrote files on Russia-locale systems |
| `cross-env` | 7.0.x (2019, one release) | env exfiltration |

```bash
rg -n '"(event-stream|ua-parser-js|eslint-scope|coa|rc|node-ipc|cross-env)"\s*:\s*"[^"]*"' package*.json package-lock.json 2>/dev/null
```
Any exact-version match → **Critical**: rotate every credential that existed
while it was installed (postinstall ran with them), remove, lockfile-refresh.

## 3 — Safe package, dangerous usage (check the call site, not the version)

| Package | Dangerous usage | Safe shape |
|---|---|---|
| `lodash` | `.merge(target, req.body)` / `_.template(userInput)` | allowlist-pick before merge; templates are static strings with data params |
| `qs` | `allowPrototypes: true` | default false — never enable for user input |
| `serialize-javascript` | serializing user-controlled objects into `<script>` | it escapes for a reason — never `isJSON`+HTML combo on user data; prefer JSON in data attributes |
| `axios` | `validateStatus: () => true` swallowing errors on auth paths | explicit status handling |
| `handlebars`/`ejs` | `compile(userInput)`, `render(userInput)` | compile first-party templates only |
| `child_process`-wrappers (`execa` et al.) | `execa(userString)` shell mode | array args, `shell: false` |

These belong in findings only when user input reaches the dangerous call —
trace with the source→sink rules of `../../injection-flaws/SKILL.md`.

## 4 — Vendored / bundled copies: invisible to every manifest scanner

Committed `public/`, `static/`, `vendor/`, `dist/` assets and copied-in
library files carry their own version banners — read them:

```bash
rg -n -i "jQuery (JavaScript Library )?v?[123]\.|jquery\.com" public/ static/ vendor/ dist/ 2>/dev/null | head
rg -n -i "moment\.js\s+(version\s+)?2\.[0-9]|AngularJS v1\.|bootstrap v[345]" public/ static/ vendor/ 2>/dev/null | head
find . -name '*.min.js' -not -path './node_modules/*' -not -path './.git/*' | head -10   # every one needs a version verdict
```

Known vendored-library thresholds (banner → finding):
- jQuery `<3.5.0` → **High** (prototype pollution CVE-2019-11358, XSS CVE-2020-11022/11023; `<1.9.0` older selector XSS CVE-2012-6708)
- moment `<2.29.4` → Medium (ReDoS CVE-2022-31129 path traversal CVE-2022-24785… `<2.29.2` for the traversal)
- AngularJS 1.x any → Medium (expression sandbox removed in 1.8 — never bind user input)
- Bootstrap `<3.4.1`/`<4.3.1` → Medium (XSS CVE-2019-8331)

Also check `Dockerfile` `FROM` images bundling system libs (covered in
`../../container-iac-security/SKILL.md`) and lockfile-free installs
(Step 2 — the resolution risk applies to every dep here).

## Reporting

Report section "Dependency risk beyond CVEs": dead/unfixable list (with
usage verdict), compromised-version matches (with rotate-credentials
action), dangerous-usage call sites (with the source→sink trace), vendored
copies (with banner versions). Each row: package@version, class (1–4),
severity, fix. The summary must answer the user's real question: *"the main
code is clean — what do the packages bring in?"*
