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

## NestJS (Node/TypeScript)

| Dangerous | Safe | Notes |
|---|---|---|
| `query(`... ${user}`)` on the TypeORM repo | `.setParameter()` / QueryBuilder params | raw boundary again |
| `class-validator` without `forbidNonWhitelisted: true` | whitelist + forbid | mass assignment via unknown keys |
| `res.send(userHtml)` / `{{...}}`-style inline templates | DTO responses (`@ResponseBody`) | reflected XSS |
| `@Public()` on a controller that mutates | explicit guards per handler | route-census target |

## Ktor (Kotlin)

| Dangerous | Safe | Notes |
|---|---|---|
| `exec { it.write("sh -c $userInput".toByteArray()) }` | `ProcessBuilder(listOf(bin, arg))` | shell string vs arg list |
| `"SELECT ... WHERE x = $user"` passed to `transaction` | `Users.select { Users.name eq user }` (Exposed) / JDBC `?` | string templates are Kotlin concat |
| `call.respondText(userHtml, ContentType.Text.Html)` | `call.respond(user)` (JSON) | reflected XSS |
| FreeMarker `${user}` in user-chosen template name | fixed template map | SSTI |

## Django REST Framework

| Dangerous | Safe | Notes |
|---|---|---|
| `fields = '__all__'` on user-facing serializers | explicit field list | mass assignment (role/is_superuser writable) |
| `serializer.save(**request.data)`-style extras | `read_only_fields` for role/id | |
| `@api_view(['POST'])` + `permission_classes=[]` default | explicit `IsAuthenticated` | default is AllowAll — census every view |
| `django-filter` with user-controlled field list | allowlisted filterset fields | data-model enumeration |

## Rails — API-only mode

| Dangerous | Safe | Notes |
|---|---|---|
| `render json: user` (full model) | explicit `as_json(methods:, only:)` / serializer | password_hash/token leakage |
| `skip_before_action :verify_authenticity_token` on cookie-auth API | token auth (Bearer) or CSRF tokens | API mode makes CSRF *more* subtle, not gone |
| `params.permit!` / `params.to_unsafe_h` into model update | `permit(:name, :email)` | mass assignment |

## Java — libraries that are sinks by themselves

| Dangerous | Safe | Notes |
|---|---|---|
| fastjson `JSON.parseObject(userJson)` with autoType (`setAutoTypeSupport(true)`, ≤1.2.80) | typed `parseObject(json, DTO.class)`; fastjson2 | CVE-2022-25845 RCE family — version + sink |
| commons-text `StringSubstitutor.createDefault().replace(userText)` (1.0–1.9) | explicit map/string lookups only | Text4Shell CVE-2022-42889 — `${script:}` executes |
| Shiro rememberMe with default/known `setCipherKey` (`kPH+bIxk5D2deZiIxcaaaA==`) | unique random key from env/secret | Shiro550 deserialization RCE — the key string is the finding |

## Rust (axum / actix-web / sqlx)

| Dangerous | Safe | Notes |
|---|---|---|
| `sqlx::query(&format!("... {u}"))` / `query(&s)` with built string | `query("... $1").bind(u)` | same raw-boundary rule as every ORM |
| `Command::new("sh").arg("-c").arg(user)` | `Command::new(bin).args([...])` | sh -c reintroduces shell |
| `format!` into `Html(user)` (actix `HttpResponse` with text/html) | templates (askama/tera auto-escape) | reflected XSS |
| `unwrap()` on parsed user input → 500 | typed extractors with validators | DoS-ish hygiene, note |
| `serde_json::from_str` on unbounded user JSON | depth-capped readers | nesting DoS (same class as jackson CVE-2020-36518) |

## Elixir / Phoenix

| Dangerous | Safe | Notes |
|---|---|---|
| `Repo.query!` / `Ecto.Adapters.SQL.query` with string interpolation | `Ecto.Query` bindings / fragment with `^pin` | `fragment("... #{u}")` = SQLi; `fragment("... ^u")` safe |
| `raw(user)` in `.heex` templates | automatic HEEx escaping | Phoenix escapes by default; `raw` opts out |
| `System.cmd("sh", ["-c", user])` | `System.cmd(bin, [args])` | shell reintroduction |
| `Plug.Conn.send_resp` with user-built content-type/html | render views | reflected XSS |
| `:crypto` direct use for passwords (`:crypto.hash(:md5, pw)`) | `Argon2`/`Bcrypt` (comeonin) | password hashing vs raw crypto |

## Adding a framework

Same rules as `patterns.md`: one row = one fixture line (true positive + a
near-miss), precision first. PR per `CONTRIBUTING.md`.
