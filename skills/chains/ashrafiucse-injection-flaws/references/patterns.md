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

## SSRF hardening checklist (for recommendations)

1. Allowlist destination hosts; deny by default
2. Resolve DNS then block private/link-local ranges (169.254.169.254 = cloud metadata!)
3. Disable/limit redirects (bypass naive allowlists)
4. No raw-IP URLs from user, scheme restricted to https
5. Separate egress network for fetchers
