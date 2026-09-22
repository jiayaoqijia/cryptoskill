---
name: injection-flaws
description: Detects injection vulnerabilities in code — SQL/NoSQL injection (including NoSQL operator injection), OS command injection, cross-site scripting (XSS), path traversal, SSRF, insecure deserialization, template injection (SSTI), XXE, prototype pollution, ReDoS, open redirect, and unsafe file upload handling. Covers Node/JS, Python, Java, Go, PHP, Ruby, C# with per-language grep patterns and context-review rules. Use when auditing input handling, query construction, file operations, subprocess calls, XML parsing, file uploads, or template rendering.
license: MIT
---

# Injection Flaws

## Method

For each category: (1) grep for sink patterns — the table below and `references/patterns.md` have ready-to-run commands per language, and `references/frameworks.md` has framework-specific dangerous/safe construct tables (Express, Django, Spring, Rails, Laravel, Go); (2) for each hit, trace backwards to the input source; (3) report only if untrusted input reaches the sink without a real sanitizer.

**Source → sink tracing.** Untrusted sources: HTTP params/body/headers/cookies, file uploads, DB rows fed to templates, webhook payloads, environment-adjacent user data, message queues. Sanitizers that count: parameterized queries, allowlist validation, `DOMPurify` for HTML, framework auto-escaping (verify it's actually on), `shlex.quote`/argument-array subprocess calls, canonicalized + allowlisted paths. "Escaping" done by string formatting does NOT count.

**Second-order (stored) flows.** The input isn't always the request in front of you. Treat these as untrusted sources and re-check sink greps against their outputs:
- **DB/model rows at render time** — the classic stored XSS: sanitized on write, rendered raw on read (`<%- user.bio %>`, `\|safe`, `{!! !!}`, `v-html`, `dangerouslySetInnerHTML` on model fields). Write-path validation ≠ read-path safety; check the READ path even when the write path looks clean.
- **Webhook/queue/cron payloads** — worker consuming messages that hit command/SQL/URL sinks (`exec(job.cmd)`, `query(task.sql)`). Producers are not trust boundaries.
- **Exports** — data written to CSV/HTML opened in Excel/Sheets: formula injection (`=cmd|...`, `@SUM(`) unless `-`/`=`/`+`/`@` prefixes are stripped.
- **Upstream service headers/bodies** on internal calls — see trusted-header rules in `../auth-review/SKILL.md`.

**Query-builder raw APIs** are SQL sinks too — the ORM does not save you at the raw boundary:
```bash
rg -n "\.raw\(|\.literal\(|knex\.raw|sequelize\.literal|typeOrm.*\.query\(|createNativeQuery|cursor\.execute\(\s*f?[\"'].*\{|MyBatis.*\$\{" 
```
`knex.raw('... ' + req.query.sort)`, `sequelize.literal(...)` with interpolation, `createNativeQuery` concat, MyBatis `${}` (vs safe `#{}`) — all equal to string-built SQL.

**Multi-line construction:** single-line greps miss queries built across lines (triple-quoted f-strings, chained concatenation). Run bounded multiline scans on the DB layer only — they're slow on whole repos:
```bash
rg -nU "execute\(\s*[frb]?['\"]{3}[\s\S]{0,300}(SELECT|INSERT|UPDATE|DELETE)[\s\S]{0,300}(\$\{|%s|\+|f['\"]|#\{)" app/ db/ models/ 2>/dev/null
```

## Categories & quick greps

### SQL / NoSQL injection
```bash
rg -n -i "(SELECT|INSERT|UPDATE|DELETE).*(\$\{|%s|%d|\+|f['\"]|\.\s*\$|#{|\"\s*\+)" -g '!*.min.js' -g '!test/**'
rg -n "\\\$where|\\\$expr|MongoClient.*eval|mapReduce"            # NoSQL: JS-in-query
```
Confirm the value is bound (`?`, `$1`, `:param`, `.execute(sql, params)`) vs concatenated/interpolated. String-built queries that only touch constants are noise.

**NoSQL operator injection:** in document stores the query object IS the API — passing request data straight through lets attackers inject operators. `User.find({ password: req.body.password })` accepts `{"password": {"$ne": ""}}` → auth bypass; `$where`/`$function` = JS execution in the DB.
```bash
rg -n "(find|findOne|findOneAndUpdate|updateOne|deleteOne|aggregate)\(\s*\{\s*\.\.\.(req|ctx|event)\.|\{\s*\.\.\.(body|query|params)|find(One)?\(\s*\{[^}]*req\.(body|query)"
```
Report when a request object/field reaches a Mongo-style query without operator stripping (`mongo-sanitize`, allowlisted keys, `$eq`-coerced values, or an ODM schema that rejects operators). Safe-looking code that builds `{ [field]: value }` with user-controlled `field` is the same bug.

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

**Egress controls (defense verification, A10):** when the app fetches user-influenced URLs, also check the environment makes SSRF expensive:
- Kubernetes: any `NetworkPolicy` restricting egress for the fetcher pods? (absence → note; pair with the SSRF finding — see `../container-iac-security/SKILL.md`)
- Cloud: metadata service reachable with v1 tokens (AWS `metadata_options http_tokens = "optional"`, no hop limit) → cloud-metadata SSRF = credential theft, raise SSRF severity
- No egress proxy/allowlist at all → mention as hardening: the fix lives in network config, not app code
```bash
rg -n "http_tokens|metadata_options|hop_limit" -g '*.tf' -g '*.yaml' -g '*.json'
rg --files -g '*networkpolicy*' -g '*NetworkPolicy*' ; rg -n "kind: NetworkPolicy|policyTypes:.*Egress" -g '*.yaml' -g '*.yml'
```

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

### Prototype pollution (Node/JS)
```bash
rg -n "(__proto__|constructor\s*[\[.:]|\.prototype\s*\[)"
rg -n "(deepMerge|defaultsDeep|merge\(|extend\(|\.set\()\(.*req\.(body|query|params)|Object\.assign\(\s*\{\}\s*,\s*req\.(body|query)"
rg -n "urlencoded\(\s*\{\s*extended:\s*true|bodyParser\(\s*\)|query\s*parser"   # deep-parsed bodies are the usual source
```
Any recursive merge / `_.set` / `Object.assign` that copies user-controlled **keys** into existing objects lets `__proto__`/`constructor.prototype` overwrite built-ins → pollutes every object, chains to RCE via gadgets (`child_process` + `NODE_OPTIONS`, EJS, template engines). Report as **High** (Critical when merged config feeds templating/process spawning). Fixes: allowlist-pick fields before merging, strip `__proto__`/`constructor`/`prototype` keys, `Object.create(null)` targets, `app.set('query parser', 'simple')`.

### XXE / unsafe XML parsing
```bash
rg -n "DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|XMLReader"          # Java — check hardening
rg -n "etree\.(parse|fromstring)|xml\.etree|minidom|pulldom|sax\.|expat|simplexml|DOMDocument|libxml|libxmljs|Nokogiri|REXML"
```
- Java factory parsing request XML without `setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` → **Critical** (file read, SSRF via parameter entities, billion-laughs DoS).
- Python stdlib `xml.*` on user XML → internal entity expansion (billion laughs) → **High**; fix is `defusedxml`.
- `lxml.etree` with default parser resolves entities (incl. external `file://`) → **Critical**; fix `XMLParser(resolve_entities=False)` or defusedxml.
- PHP `libxml` < 2.9 / `libxml_disable_entity_loader(false)` era stacks → flag. Go `encoding/xml` is entity-safe; don't flag.

### ReDoS
```bash
rg -n "\(\s*[^()]*[+*]\s*\)[+*{]|(\[[^\]]*[+*][^\]]*\])[+*{]"   # heuristic: nested/starred quantifiers
rg -n "\.test\(|\.match\(|\.replace\(|\.search\(|re\.(match|search|fullmatch|sub)|Pattern\.matches|regexp\.MustCompile"
```
Cross the two lists manually: report only when a nested-quantifier regex (`(a+)+b`, `(a|a)*$`, `([a-z]+)*d`) runs on **user-controlled, unbounded-length input** → event-loop/thread starvation → **High** (Medium for capped-length inputs). Safe: bounded input length, linear engines (Go RE2, `re2` bindings), single non-nested quantifier. Verify the pattern really nests quantifiers before reporting — this heuristic over-fires.

### Open redirect
```bash
rg -n -i "res\.redirect\(|redirect_to |redirect\(request|Redirect\(.*param|sendRedirect|window\.location(\.href)?\s*=|location\.replace\(|header\(\s*['\"]Location|RedirectToAction"
rg -n -i "\?(next|continue|returnTo|returnUrl|redirect|redirect_uri|url|goto)="   # in views/handlers
```
Flag when the redirect target comes from user input with no exact-host allowlist. Login/logout/reset flows carrying `?next=` params are the classic; **High** when the URL carries tokens/codes (OAuth `code`, reset token) or silences origin checks, otherwise **Medium**. Safe: exact allowlist of destinations, or relative-only after `new URL(next, base)` origin check — prefix/suffix matching on the host is bypassable (`evil.com` vs `evil-example.com`).

### Unsafe file upload
```bash
rg -n "multer|multipart|form\.File|FormFile|MultipartFormDataEntry|\.originalname|file\.filename|Storage\(|upload"
```
For every upload handler check:
1. **Type allowlist** — trusting `Content-Type` or the client filename alone is bypassable (double extension `avatar.php.png`; `x.svg` = stored XSS; `.shtml`)
2. **Storage location** — files written under webroot/static/public → served/parsed by the web server = **Critical** (parse-to-RCE chains); non-served storage → High
3. **Filename** — user filename used verbatim (`../../` traversal, collisions) instead of CSPRNG-generated names
4. **Caps** — no size limit / no per-entry decompression cap → zip bomb (`zipfile.extractall` unchecked) → High
5. **Serving** — uploads served `inline` without `X-Content-Type-Options: nosniff` / `Content-Disposition: attachment`; SVG uploads rendered (embed `<script>`, XXE via `<externalEntity>`)

## Reporting

Each confirmed finding: severity (SQLi/command/deserialization/SSTI/XXE reachable unauthenticated = **Critical**; prototype pollution = High→Critical with gadget; open redirect = Medium, High with tokens in URL; ReDoS = Medium/High), `file:line`, the source→sink trace in two lines, and the fix: parameterize / argument-array exec / auto-escape / allowlist + canonicalize / defusedxml / bounded regex / exact-host redirect allowlist.

False-positive discipline: hits inside `test/`, `examples/`, `migrations/`, or on constant strings get dropped — note the count of dropped hits in the summary so effort is visible.
