---
name: spring-security
description: Audits Spring Boot / Spring (Java) applications for framework-specific vulnerabilities — JPQL/native query concatenation, JdbcTemplate string-concat SQL injection, MyBatis ${} substitution, Thymeleaf th:utext and JSP scriplet XSS, Spring Security misconfigurations (csrf().disable(), permitAll() on sensitive matchers), Actuator endpoint over-exposure (env/heapdump leak credentials), hardcoded datasource/JWT secrets in properties, Jackson enableDefaultTyping deserialization, SpEL injection, session cookie flags, and stacktrace inclusion. Use when the project has pom.xml or build.gradle with spring dependencies.
license: MIT
---

# Spring Security

## Step 0 — Detect

```bash
rg -n "spring-boot|springframework" -g 'pom.xml' -g 'build.gradle*' | head -5
rg --files -g 'application*.properties' -g 'application*.yml' -g '*SecurityConfig*'
```

Record Spring Boot/Framework version (Spring4Shell check: `../cve-research/vuln-db/entries/`), Security config style (WebSecurityConfigurerAdapter vs SecurityFilterChain), template engine.

## Step 1 — Configuration files

```bash
rg -n "password|secret|include-stacktrace|exposure|cookie" -g 'application*.properties' -g 'application*.yml' -g 'application*.yaml'
```

- `spring.datasource.password=...` / `server.ssl.key-store-password=` / JWT secret hardcoded → Critical in public repos, High otherwise
- `management.endpoints.web.exposure.include=*` (or env,heapdump listed) → **Critical**: `/actuator/env` leaks every property incl. credentials; `/actuator/heapdump` leaks in-memory secrets
- `server.error.include-stacktrace=always` → Medium
- `server.servlet.session.cookie.secure=false` / `http-only=false` → Medium

## Step 2 — Spring Security config

```bash
rg -n "csrf\(\)\.disable|permitAll|antMatchers|authorizeHttpRequests|@PreAuthorize|@EnableWebSecurity" src/
```

- `http.csrf().disable()` with cookie sessions → High (state-changing endpoints)
- `.antMatchers("/admin/**").permitAll()` → Critical
- `@PreAuthorize`/`@PostAuthorize` absent across controllers with role-sensitive ops → High (verify per-handler)
- CORS config: `allowedOrigins("*")` + `allowCredentials(true)` → Critical (per spec should fail, frameworks reflect)

## Step 3 — SQL injection

```bash
rg -n "createQuery\([\"'][^\"']*\+|createNativeQuery.*\+|jdbcTemplate\.\w+\([\"'][^\"']*\+" src/
rg -n "\\\$\{" -g '*.xml' src/   # MyBatis mappers
```

- String-concatenated `createQuery`/`createNativeQuery`/`JdbcTemplate.query` → Critical (fix: bound params `:name` / `?`)
- MyBatis `${...}` (string substitution) vs `#{...}` (prepared) — any `${}` reachable from request params → Critical

## Step 4 — XSS / templates

```bash
rg -n "th:utext|<%=|escapeXml=\"false\"|c:out" src/main/resources/templates/ src/ 2>/dev/null
```

Census, don't sample: disposition every hit. Severity by privilege direction per `../injection-flaws/SKILL.md` (XSS table) — unprivileged-authored content rendered unescaped in a staff view = Critical.

- `th:utext="${user...}"` → direction-triaged (`th:text` escapes)
- JSP scriplets `<%= user %>` → direction-triaged
- `escapeXml="false"` on c:out → direction-triaged

## Step 5 — Deserialization & SpEL

```bash
rg -n "enableDefaultTyping|ObjectInputStream|readObject|parseExpression" src/
```

- Jackson `enableDefaultTyping()` / `@JsonTypeInfo(use=Id.CLASS)` on external input → Critical (polymorphic gadget chains)
- `ObjectInputStream.readObject` on network data → Critical
- `spelParser.parseExpression(userInput)` → Critical (SpEL = RCE)
- Spring expression in `@Value` from constants → safe

## Step 6 — Files & commands

```bash
rg -n "FileInputStream\(|Files\.(read|copy)|new File\(" src/ | rg -i "request|param" | head
rg -n "Runtime\.getRuntime|ProcessBuilder" src/
```

- File ops with request params → traversal, High
- `Runtime.exec(String)` single-string form → High (argument injection); `exec(String[])`/ProcessBuilder list → OK-ish

## Reporting

Severity table above; fixes are localized (bound params, `th:text`, matcher tightening). Cross-reference framework CVEs (Spring4Shell, historic) via `../cve-research/SKILL.md` and dependency CVEs via `../dependency-vulns/SKILL.md`.
