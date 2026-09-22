# Injection Pattern Library

Load this when you need language-specific greps beyond the SKILL.md quick set.
Run from the project root. Always exclude vendored/generated code.

## SQL injection sinks

| Language | Grep |
|---|---|
| Node | `rg -n "pool\.query\(|client\.query\(|db\.(query|raw)\(" ` then eyeball template literals |
| Python | `rg -n "cursor\.execute\(.*[%f+]|\.execute\(['\"].*\{"` |
| Java | `rg -n "Statement|createQuery\(.*\+|prepareStatement"` (string-concat `createQuery` = bug) |
| Go | `rg -n "db\.(Query|Exec)\(.*\+|fmt\.Sprintf\([^)]*SELECT"` |
| PHP | `rg -n "mysqli_query\(|->query\(.*\\\$"` |
| Ruby | `rg -n "\.where\([\"'].*#\{|exec_query"` |

Safe forms to whitelist while eyeballing: `$1`/`?` placeholders, named params (`:name`, `@name`), query builders (Sequelize `.findAll({where})`, Django ORM, SQLAlchemy expressions).

## Command injection

| Language | Dangerous | Safe |
|---|---|---|
| Node | `child_process.exec`, `execSync`, backticks | `execFile`, `spawn` with args array |
| Python | `os.system`, `subprocess.*` with `shell=True`, `os.popen` | `subprocess.run([...])` |
| Java | `Runtime.exec(String)` (single-string form) | `Runtime.exec(String[])`, `ProcessBuilder` |
| Go | `exec.Command("sh", "-c", userStr)` | `exec.Command(bin, args...)` |
| PHP | `system`, `shell_exec`, backticks, `escapeshellarg` missing | `escapeshellarg` per arg |

## XSS sinks (frontend + SSR)

- Raw sinks: `innerHTML`, `outerHTML`, `document.write`, `insertAdjacentHTML`
- Framework escapes: `v-html`, `dangerouslySetInnerHTML`, Angular `bypassSecurityTrust*`, `|safe`/`raw` filters, Twig `|raw`
- Server: `res.send(userInput)` with HTML content-type, `render_template_string`, `autoescape=False`
- DOM-based: `location.hash`/`location.search` → sink; `eval`, `setTimeout("str")`, `new Function`

## Path traversal

- Danger signs: `open(user)`, `send_file(req.query.f)`, `Path.Combine(base, user)` without containment check, `include($page)`, `require(userPath)`
- Fix pattern to recommend: `const safe = path.resolve(base, user); if (!safe.startsWith(base + path.sep)) throw` (note: `startsWith(base)` alone is bypassable with sibling dirs)

## Deserialization / eval-family

- Python: `pickle`, `cPickle`, `dill`, `marshal`, `yaml.load` (non-Safe), `eval`/`exec`/`compile`
- Java: `ObjectInputStream.readObject`, XStream without security framework, Apache Commons Collections on classpath + any deserialization (historical gadget chains)
- PHP: `unserialize` with user input; phar deserialization via `file_exists("phar://...")`
- .NET: `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer`, `ObjectStateFormatter`
- Ruby: `Marshal.load`, `Oj.load` with `mode: :object`
- JS: `eval`, `new Function`, `node:vm` `runInNewContext` on remote strings

## Prototype pollution (Node/JS)

| Pattern | Dangerous | Safe |
|---|---|---|
| Merge target | `deepMerge(cfg, req.body)`, `_.set(obj, userPath, v)`, `Object.assign(cfg, req.body)` | allowlist-picked fields into a fresh object; `Object.create(null)` target |
| Body parsing | `urlencoded({extended:true})` / `qs.parse` (nested objects from attacker) | `app.set('query parser', 'simple')`, flat bodies |
| Keys | `__proto__`, `constructor`, `prototype` accepted as keys | sanitizer strips these three keys recursively |

Chains to check for (raise severity): merged config → `child_process.spawn` (NODE_OPTIONS gadget), template engine options (EJS `outputFunctionName`), cached objects. Report merge-of-user-keys into existing objects even without an obvious gadget.

## XXE

| Stack | Dangerous | Safe |
|---|---|---|
| Java | `DocumentBuilderFactory`/`SAXParserFactory`/`XMLInputFactory` defaults on request XML | `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` (or both entity features off + no DTD) |
| Python | `xml.etree`, `minidom`, `pulldom`, `sax`, expat on user XML; `lxml.etree` default parser | `defusedxml.*`; `lxml` `XMLParser(resolve_entities=False)` |
| PHP | `simplexml`/`DOMDocument` with old libxml or loader enabled | libxml ≥2.9 defaults, `LIBXML_NOENT` absent |
| Ruby | `Nokogiri` defaults resolve entities? — no (safe since 1.x); flag `REXML` only with DTD + external entity patches absent | modern Nokogiri |
| Node | `libxmljs`/`sax` with entities enabled | `xml2js` (no entity resolution), `fast-xml-parser` |

## ReDoS

- Shape to look for: nested quantifiers `(a+)+`, `(a|a)*`, `([a-z]+)*`, overlapping alternations `(a|aa)+`, unbounded `.{n,}` on long inputs
- Sink: `.test/.match/.replace/.search/.split` (JS), `re.match/search/sub/fullmatch` (Py), `Pattern.matches` (Java), `regexp.MustCompile` (Go — linear, safe)
- Report only when: input is user-controlled AND unbounded. Cap input length → drop to Medium or dismiss.

## Open redirect sinks

| Stack | Grep |
|---|---|
| Express | `rg -n "res\.redirect\("` then trace the arg |
| Flask/Django | `rg -n "redirect\("` — flag `redirect(request.args\[|request.GET\[` |
| Rails | `rg -n "redirect_to "` — flag `redirect_to params\[" |
| Spring | `rg -n "sendRedirect\(\" + "response.sendRedirect"` (concat = bug) |
| PHP | `rg -n "header\(\s*['\"]Location:\\s*\.\s*\$_(GET|REQUEST)"` |
| SPA | `rg -n "location\.(href|replace|assign)\\s*=\\s*"` on router/query params |

Safe form: exact allowlist (`ALLOWED = new Set(['/dashboard','/'])`) or `new URL(next, ORIGIN).origin === ORIGIN && !next.startsWith('//')` (protocol-relative `//evil.com` bypasses naive relative checks).

## File upload checklist

1. Extension + MIME + magic-bytes allowlist? (one of three is not enough)
2. Stored under webroot/static/public? (`express.static`, `MEDIA_ROOT` served, `/static/*`)
3. Filename from user (`originalname`, `file.filename`) instead of `crypto.randomBytes`?
4. Size limit middleware + per-entry decompression cap (zip bombs: `zipfile.extractall`, `yauzl`, `adm-zip`)?
5. Served inline as original type? (`Content-Disposition: attachment` + `nosniff` for user files; SVG never rendered inline)
6. Parser exposure: ImageMagick/`sharp`/Ghostscript on uploads — flag as hardening note

## Query-builder raw sinks (ORM ≠ safe at the raw boundary)

| Builder | Dangerous | Safe |
|---|---|---|
| knex | `knex.raw('...' + req.query.sort)` | `knex.raw('... order by ??', [col])` (?? = identifier binding) |
| Sequelize | `sequelize.literal(` with interpolation | plain where-objects, `sequelize.literal` on constants only |
| TypeORM | `repo.query(... + x)` | `.setParameter()` / QueryBuilder params |
| SQLAlchemy | `text(f"SELECT ... {x}")`, `text('... %s' % x)` | `text('... :name')` + params |
| Django | `raw()`, `extra(where=)` with interpolation | ORM lookups, params in `raw(sql, [params])` |
| MyBatis / JPA | `${param}` in XML, `createNativeQuery(... + x)` | `#{param}`, named params |
| jOOQ | `.where("name = '" + x + "'")` plain-SQL fragments | type-safe DSL / `param(...)` |

## Second-order read-path sinks (stored XSS & friends)

Run the XSS greps against the READ path, with model/DB fields as the source:
- EJS `<%- %>`, Blade `{!! !!}`, Twig `|raw`, Jinja `|safe`/autoescape off, `v-html`, `dangerouslySetInnerHTML`, `ng-bind-html` on **model attributes** (`user.bio`, `post.body`, `comment.text` — not just `req.*`)
- CSV/HTML export paths: formula injection unless leading `= + - @` is stripped/prefixed
- Worker sinks fed by queue/webhook/cron payloads: `exec(payload.cmd)`, `query(task.sql)`, `fetch(payload.url)` — treat the producer's validation as irrelevant

## Multi-line query construction

Single-line greps miss queries assembled across lines. Scope to DB-layer dirs (multiline is slow repo-wide):

```bash
rg -nU "execute\(\s*[frb]?['\"]{3}[\s\S]{0,300}(SELECT|INSERT|UPDATE|DELETE)[\s\S]{0,300}(\$\{|%s|\+|f['\"]|#\{)" app/ db/ models/
rg -nU "query\(\s*`[\s\S]{0,300}(WHERE|ORDER BY)[\s\S]{0,300}\$\{" app/ db/    # JS template literals across lines
```

## C/C++ native code

Memory-safety + injection sinks for repos with native components (services, extensions, embedded). These bugs are RCE by default — severity starts High.

| Class | Dangerous | Safe / check |
|---|---|---|
| Buffer copy | `strcpy`, `strcat`, `sprintf`, `gets`, `scanf("%s")` | `strncpy`+explicit NUL, `snprintf`, `fgets(buf, sizeof buf, ...)` — verify SIZE matches destination |
| Format string | `printf(user)`, `syslog(user)`, `fprintf(f, user)` — user data as the FORMAT arg (`%n` = write primitive) | `printf("%s", user)` — format is always a literal |
| Command exec | `system(user)`, `popen(user, ...)`, `execl("sh", "-c", user)` | `execv(file, argv[])` with validated args — no shell |
| Integer overflow → alloc | `malloc(len + 1)` with attacker `len` (wraps at 2^32), `memcpy` with computed size | `if (len > SIZE_MAX - 1) fail;` before alloc/copy |
| Off-by-N | loops `<=`, `buf[N]` writes at `buf[N]` | review each loop bound against the declared size |
| TOCTOU | `access(path)` … then `open(path)` (syslog/temp races) | `open(path, O_NOFOLLOW)` fstat-after-open, or operate on the fd |
| Use-after-free / double-free | freeing in error paths then continuing | ownership discipline; `-fsanitize=address` in CI as a positive control |
| Path from user | `open(user)` without canonicalization | allowlist + `realpath` containment |

```bash
rg -n "\b(strcpy|strcat|sprintf|gets)\s*\(" -g '*.c' -g '*.cc' -g '*.cpp' -g '*.h'
rg -n "printf\s*\(\s*[a-z_]" -g '*.c' -g '*.cpp'        # non-literal first arg
rg -n "\b(system|popen)\s*\(" -g '*.c' -g '*.cpp'
rg -n "scanf\s*\(\s*\"%s\"" -g '*.c' -g '*.cpp'
rg -n "malloc\s*\(.*\+|memcpy\s*\(" -g '*.c' -g '*.cpp' | head
```

Triage: user-influenceable argument (argv, network input, file content) reaching the sink = High/Critical; constant strings = drop with a count. Modern-C positives worth noting in reports: `std::string`, `std::vector`, smart pointers, `std::format` — memory-safe idioms present = `What looks good` material.

## SSRF hardening checklist (for recommendations)

1. Allowlist destination hosts; deny by default
2. Resolve DNS then block private/link-local ranges (169.254.169.254 = cloud metadata!)
3. Disable/limit redirects (bypass naive allowlists)
4. No raw-IP URLs from user, scheme restricted to https
5. Separate egress network for fetchers
