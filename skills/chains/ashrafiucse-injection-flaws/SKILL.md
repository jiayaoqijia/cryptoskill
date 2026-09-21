---
name: injection-flaws
description: Detects injection vulnerabilities in code — SQL/NoSQL injection, OS command injection, cross-site scripting (XSS), path traversal, SSRF, insecure deserialization, and template injection (SSTI). Covers Node/JS, Python, Java, Go, PHP, Ruby, C# with per-language grep patterns and context-review rules. Use when auditing input handling, query construction, file operations, subprocess calls, or template rendering.
license: MIT
---

# Injection Flaws

## Method

For each category: (1) grep for sink patterns — the table below and `references/patterns.md` have ready-to-run commands per language, and `references/frameworks.md` has framework-specific dangerous/safe construct tables (Express, Django, Spring, Rails, Laravel, Go); (2) for each hit, trace backwards to the input source; (3) report only if untrusted input reaches the sink without a real sanitizer.

**Source → sink tracing.** Untrusted sources: HTTP params/body/headers/cookies, file uploads, DB rows fed to templates, webhook payloads, environment-adjacent user data, message queues. Sanitizers that count: parameterized queries, allowlist validation, `DOMPurify` for HTML, framework auto-escaping (verify it's actually on), `shlex.quote`/argument-array subprocess calls, canonicalized + allowlisted paths. "Escaping" done by string formatting does NOT count.

## Categories & quick greps

### SQL / NoSQL injection
```bash
rg -n -i "(SELECT|INSERT|UPDATE|DELETE).*(\$\{|%s|%d|\+|f['\"]|\.\s*\$|#{|\"\s*\+)" -g '!*.min.js' -g '!test/**'
rg -n "\\\$where|\\\$expr|MongoClient.*eval|mapReduce"            # NoSQL: JS-in-query
```
Confirm the value is bound (`?`, `$1`, `:param`, `.execute(sql, params)`) vs concatenated/interpolated. String-built queries that only touch constants are noise.

### OS command injection
```bash
rg -n "os\.system|subprocess\.(call|run|Popen)\(.*shell\s*=\s*True|child_process\.(exec|execSync)|Runtime\.getRuntime\(\)\.exec|system\(|popen\(|exec\.Command\(.*\+"
```
`exec("ls " + filename)` = classic. Safe: `execFile(cmd, [args])`, `subprocess.run([cmd, arg])` without `shell=True`.

### XSS
```bash
rg -n "innerHTML|document\.write|v-html|dangerouslySetInnerHTML|\.html\(|render_template_string|autoescape\s*=\s*False|\|safe\b|markupsafe\.Markup"
rg -n -i "<%=.*request|res\.send\(.*req\.(body|query|params)"
```
Flag reflected user input into any of these sinks. Framework auto-escaping (Jinja2, React JSX text nodes) is a valid defense — but `dangerouslySetInnerHTML`/`v-html`/`|safe` bypass it.

### Path traversal
```bash
rg -n "open\(|readFile|writeFile|sendFile|send_file|File\(|Path\.Combine|require\(.*\+|include\(.*\$|fopen\("
```
Flag when user input influences the path and there's no `path.resolve` + allowlist prefix check / `send_file(..., safe=True)` equivalent.

### SSRF
```bash
rg -n "requests\.get\(|axios\.(get|post)|fetch\(|urllib\.request|HttpClient|curl_exec|http\.Get\("
```
Flag only when the URL (host or full) derives from user input — e.g. "fetch this webhook URL", URL preview features, image import by URL. Check for allowlist/redirect limits/private-IP blocking.

### Deserialization
```bash
rg -n "pickle\.loads?|yaml\.load\((?!.*Loader=)|marshal\.loads|ObjectInputStream|readObject|unserialize\(|eval\(|exec\(|new Function\(|Function\("
```
`yaml.load` without `SafeLoader`, `pickle.loads` on user-controlled bytes, PHP `unserialize` on user input, `eval` on anything remote = CRITICAL.

### Template injection (SSTI)
```bash
rg -n "render_template_string|Template\(.*\+|Jinja2\(.*from_string|erb\.new\(.*\+|Mustache\.render\(.*\+|StringTemplate"
```
User input inside the template *string* (not the data context) = SSTI.

## Reporting

Each confirmed finding: severity (SQLi/command/deserialization/SSTI reachable unauthenticated = **Critical**), `file:line`, the source→sink trace in two lines, and the fix: parameterize / argument-array exec / auto-escape / allowlist + canonicalize.

False-positive discipline: hits inside `test/`, `examples/`, `migrations/`, or on constant strings get dropped — note the count of dropped hits in the summary so effort is visible.
