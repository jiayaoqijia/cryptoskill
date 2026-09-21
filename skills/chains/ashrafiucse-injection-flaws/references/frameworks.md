# Framework Pattern Pack — Injection Sinks per Framework

Framework knowledge is where precision comes from: the same user input is
*auto-escaped* in one framework and *fatal* in another. Load this during Phase 1
when the stack matches. Format: dangerous → safe → grep.

## Node / Express

| Dangerous | Safe | Notes |
|---|---|---|
| `res.send(userInput)` (HTML content-type) | `res.json(userInput)` | reflected XSS via string sends |
| EJS `<%- user %>` / Pug `!{user}` | `<%= user %>` | raw interpolation sinks |
| `db.query(\`... ${user}...\`)` | `db.query('... ?', [user])` | mysql/pg/mysql2 |
| `mongoose.find({ $where: userExpr })` | field queries | JS execution in Mongo |
| `sequelize.literal(userStr)` / `knex.raw(userStr)` | bind parameters | |
| `child_process.exec(userStr)` | `execFile(bin, [args])` | |

## Django / Flask / Jinja2 (Python)

| Dangerous | Safe | Notes |
|---|---|---|
| `Model.objects.raw(f"...{user}")` / `.extra(where=[user])` | ORM filters | |
| `cursor.execute("... %s" % user)` | `execute(sql, (user,))` | |
| Jinja `{{ user \| safe }}` / `autoescape=False` | plain `{{ user }}` | auto-escape is on by default — flag bypasses |
| `render_template_string(user)` | `render_template(tpl, data)` | SSTI |
| `eval`/`exec`/`pickle.loads`/`yaml.load(unsafe)` | `ast.literal_eval`, SafeLoader | |

## Spring / Thymeleaf / JPA (Java)

| Dangerous | Safe | Notes |
|---|---|---|
| `jdbcTemplate.query("... " + user)` | `?` placeholders / `NamedParameterJdbcTemplate` | |
| `em.createQuery("... " + user)` | parameter binding `:name` | JPQL concat = injection |
| Thymeleaf `th:utext="${user}"` | `th:text` | unescaped |
| SpEL `parser.parseExpression(user)` | constants only | SpEL injection → RCE |
| `new ScriptEngine(...).eval(user)` | never with user input | |
| `ObjectInputStream.readObject` on network data | JSON, protobuf | gadget chains |

## Rails (Ruby)

| Dangerous | Safe | Notes |
|---|---|---|
| `where("name = '#{user}'")` | `where(name: user)` | |
| `Model.find_by_sql(user_sql)` | ORM | |
| ERB `<%= raw user %>` / `html_safe` / `String#html_safe` | plain `<%= %>` | Rails escapes by default |
| `send(params[:method])` | explicit allowlist dispatch | dangerous send |
| `Marshal.load` / `Oj.load(mode: :object)` | JSON.parse | deserialization |
| `system("cmd #{user}")` / backticks | `system("cmd", user)` | |

## Laravel / Blade (PHP)

| Dangerous | Safe | Notes |
|---|---|---|
| `DB::raw($user)` inside query builder | bindings `?` / named | |
| Blade `{!! $user !!}` | `{{ $user }}` | escaped by default |
| `unserialize($userInput)` | `json_decode` | object injection → RCE chains |
| `exec`/`shell_exec`/backticks with concat | `escapeshellarg` per arg | |
| `include($page . '.php')` | explicit route map | LFI/RFI |
| `preg_replace('/e', ...)` (old PHP) | `preg_replace_callback` | |

## Go

| Dangerous | Safe | Notes |
|---|---|---|
| `db.Query(fmt.Sprintf("... %s", user))` | `db.Query(sql, args...)` | |
| `text/template` rendering HTML | `html/template` | only html/template auto-escapes |
| `exec.Command("sh", "-c", userStr)` | `exec.Command(bin, args...)` | |
| `template.HTML(userStr)` cast | omit cast | bypasses escaping |

## Vue / Nuxt

| Dangerous | Safe | Notes |
|---|---|---|
| `v-html="userHtml"` | `{{ userHtml }}` | the raw HTML sink |
| `:href="userUrl"` / `:src="userUrl"` | scheme allowlist (`http(s):` only) | `javascript:` URLs |
| `eval` / `new Function` on props | never | |

## Angular

| Dangerous | Safe | Notes |
|---|---|---|
| `bypassSecurityTrustHtml/Url/Style/ResourceUrl(user)` | `sanitizer.sanitize(...)` or binding as text | every bypass = review |
| `[innerHTML]` is escaped by default | — | only dangerous with a bypass |
| `[src]`/`[href]` with user values | DOMSanitizer | |

## Svelte / SvelteKit

| Dangerous | Safe | Notes |
|---|---|---|
| `{@html userContent}` | `{userContent}` | the only raw sink in Svelte |
| `window.location = userUrl` | validated navigation | |

## FastAPI (Python)

| Dangerous | Safe | Notes |
|---|---|---|
| `db.execute(text(f"...{user}"))` | `text("... :u").bindparams(u=user)` | SQLAlchemy |
| rendering user-provided template *strings* | fixed template files | SSTI |
| JSON responses are XSS-safe | — | pydantic validators count as sanitizers |

## Gin / Echo / Fiber (Go)

| Dangerous | Safe | Notes |
|---|---|---|
| `fmt.Sprintf` into `db.Query/Exec` | placeholders | |
| `c.HTML(200, userTemplatePath, data)` | fixed template names | template injection |
| `template.HTML(user)` cast | omit cast | bypasses html/template escaping (which is otherwise automatic ✓) |

## Symfony / Twig (PHP)

| Dangerous | Safe | Notes |
|---|---|---|
| `{{ user|raw }}` | plain `{{ user }}` | Twig escapes by default |
| `$conn->executeQuery("... ".$user)` | `executeQuery($sql, [$user])` | Doctrine binds |
| `Process::fromShellCommandline("cmd ".$user)` | `new Process([$bin, $arg])` | |

## ASP.NET Core (C#)

| Dangerous | Safe | Notes |
|---|---|---|
| Razor `@Html.Raw(user)` | `@user` | |
| `FromSqlRaw($"... {user}")` (EF Core) | `FromSqlInterpolated` or parameters | |
| `Process.Start("cmd", "/c " + user)` | `ProcessStartInfo.ArgumentList` | |

## Adding a framework

Same rules as `patterns.md`: one row = one fixture line (true positive + a
near-miss), precision first. PR per `CONTRIBUTING.md`.
