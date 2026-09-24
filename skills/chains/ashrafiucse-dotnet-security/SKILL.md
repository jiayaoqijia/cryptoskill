---
name: dotnet-security
description: Audits ASP.NET Core / .NET Framework applications — Razor Html.Raw and Blazor MarkupString XSS, EF Core FromSqlRaw/SqlQueryRaw and Dapper/ADO string-concat SQL injection, BinaryFormatter/ObjectStateFormatter deserialization RCE, hardcoded machineKey → ViewState RCE, XXE via DtdProcessing.Parse, Newtonsoft TypeNameHandling polymorphic gadgets, AllowAnonymous on sensitive endpoints, antiforgery gaps, CORS AllowAnyOrigin+AllowCredentials, open redirect, Process.Start command injection, hardcoded connection strings, developer exception page in prod. Use when the project has .csproj, .sln, packages.lock.json, packages.config, or web.config.
license: MIT
---

# .NET Security (ASP.NET Core / .NET Framework)

## Step 0 — Detect

```bash
rg --files -g '*.csproj' -g '*.sln' -g 'packages.lock.json' -g 'packages.config' -g 'web.config' -g 'appsettings*.json' | head -10
rg -n "Microsoft.AspNetCore|System.Web|TargetFramework" -g '*.csproj'
```

Record: TargetFramework (`netcoreapp`/`net5+` = ASP.NET Core; `net4x` = Web Forms/MVC5), template engine (Razor `.cshtml`, Blazor `.razor`, Web Forms `.aspx`), data access (EF Core, Dapper, ADO.NET). Check NuGet versions against `../cve-research/vuln-db/entries/`.

## Step 1 — Config & secrets

```bash
rg -n "Password=|password\"|machineKey|validationKey|UseDeveloperExceptionPage" -g 'appsettings*.json' -g '*.config' -g 'launchSettings.json' -g 'Program.cs' -g 'Startup.cs'
```

- Connection strings with embedded passwords (`"Password=..."`) → Critical in public repos, High otherwise
- `<machineKey validationKey="<literal>" decryptionKey="<literal>"/>` in web.config → **Critical**: leaked/hardcoded machine key → forged `__VIEWSTATE` → pre-auth RCE (KEV-class exploit chains). `AutoGenerate` is the safe form
- `UseDeveloperExceptionPage()` without environment guard, or `ASPNETCORE_ENVIRONMENT: Development` committed → High (stacktrace + path leak)

## Step 2 — Authorization & antiforgery

```bash
rg -n "AllowAnonymous|Authorize|ValidateAntiForgeryToken|IgnoreAntiforgery" -g '*.cs'
rg -n "AllowAnyOrigin|AllowCredentials|AddCors" -g '*.cs'
```

- `[AllowAnonymous]` on any action touching data, users, or admin ops → Critical (route-census discipline: disposition EVERY controller/action, `../auth-review/SKILL.md` §1)
- Controller classes with role-sensitive ops and no `[Authorize]` → High (verify per-handler)
- Cookie-auth POST actions without `[ValidateAntiForgeryToken]` → High (state change + CSRF)
- `.AllowAnyOrigin()` combined with `.AllowCredentials()` → High (reflected-origin patterns)
- Mass assignment: request-bound model assigning privilege fields (`user.Role = model.Role`) → Critical (CWE-915; the Umbraco GHSL class)

## Step 3 — SQL injection

```bash
rg -n "FromSqlRaw|SqlQueryRaw|ExecuteSqlRaw|\.Query\(|SqlCommand\(" -g '*.cs'
```

- EF Core `FromSqlRaw($"... {user}")` / `ExecuteSqlRaw($"...")` with interpolated strings → Critical. **Near-miss:** `FromSqlInterpolated($"... {user}")` is SAFE — the API parameterizes C# interpolation by design
- Dapper `conn.Query("... " + user)` or `$"... {user}"` → Critical; `conn.Query(sql, new { id })` → safe
- ADO.NET `new SqlCommand("... " + user)` → Critical; `Parameters.Add`/`SqlParameter` → safe

## Step 4 — XSS / templates

```bash
rg -n "Html\.Raw|MarkupString|<%=" -g '*.cshtml' -g '*.razor' -g '*.aspx' -g '*.ascx'
rg -n "Mode=\"PassThrough\"|Literal" -g '*.aspx' -g '*.ascx' -g '*.cs'
```

Census, don't sample: disposition every raw sink with privilege direction (`../injection-flaws/SKILL.md` XSS table).

- Razor `@Html.Raw(userContent)` → direction-triaged (plain `@user` auto-encodes ✓)
- Blazor `@((MarkupString)userContent)` → direction-triaged
- Web Forms `<%= user %>` (raw) vs `<%: user %>` (encoded ✓); `<asp:Literal Mode="PassThrough">` → unencoded

## Step 5 — Deserialization & XML

```bash
rg -n "BinaryFormatter|ObjectStateFormatter|LosFormatter|NetDataContractSerializer|TypeNameHandling" -g '*.cs'
rg -n "DtdProcessing\.Parse|ProhibitDtd\s*=\s*false|XmlResolver" -g '*.cs'
```

- `BinaryFormatter.Deserialize` / `ObjectStateFormatter` / `LosFormatter` / `NetDataContractSerializer` on request/external data → Critical (gadget chains)
- Newtonsoft `TypeNameHandling.All/Auto/Objects` enabled on request bodies → Critical (polymorphic gadgets; same class as Jackson defaultTyping). `TypeNameHandling.None` safe
- `XmlSerializer` over type-controlled input → High; XXE: `DtdProcessing.Parse` or `XmlResolver` non-null on untrusted XML → High

## Step 6 — Files, commands, redirects

```bash
rg -n "Path\.Combine|PhysicalFile\(" -g '*.cs' | rg -i "request|query|param|route|input"
rg -n "Process\.Start|ProcessStartInfo" -g '*.cs'
rg -n "Redirect\(" -g '*.cs' | rg -i "request|query|param|url"
```

- `Path.Combine(root, userInput)` serving/reading files → traversal, High
- `Process.Start`/`ProcessStartInfo` with concatenated single-string args → High (argument injection; `ArgumentList` additive form → safe)
- `return Redirect(Request.Query["url"])` unvalidated → open redirect, High; `Url.IsLocalUrl` allowlist check → safe

## Reporting

Severity table above; fixes localized (bound params, `@` encoding, `[Authorize]` per-route, `AutoGenerate` machineKey, JSON over BinaryFormatter). Cross-reference NuGet CVEs via `../cve-research/SKILL.md` and dependency reachability via `../dependency-vulns/SKILL.md`.
