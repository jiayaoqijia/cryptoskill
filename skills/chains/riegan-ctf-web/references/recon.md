# Web recon — fingerprint, enumerate, find exposed source

All live requests against a remote target are gated by the sibling `ctf` router rules.
Mirror the app locally when source is provided (`php -S 127.0.0.1:8000`,
`python3 -m http.server 8000`, `podman` for shipped images) and recon the mirror freely.

## 1. Fingerprint (manual Wappalyzer logic)

| Signal | Read as |
|---|---|
| `Server:` / `X-Powered-By:` headers | nginx/apache version, PHP, Express, ASP.NET |
| Cookie names: `PHPSESSID` / `JSESSIONID` / `laravel_session` / `connect.sid` / `csrftoken` | PHP / Java / Laravel / Node-Express / Django |
| 404/500 page styling | framework error pages (Laravel stack traces, Werkzeug debugger) |
| `/wp-login.php`, `/administrator/`, `/drupal/` | WordPress / Joomla / Drupal |
| `/_next/static/`, `__NEXT_DATA__`, React/Vue chunk names in HTML | JS framework, SPA |
| `GraphQL` in JS bundles, `X-Powered-By: Express` | API surface |
| Favicon hash | compare against known apps (hash via `python3 -c "import hashlib,sys;print(hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest())"`) |

```bash
curl -s -D - -o /dev/null "$URL"                 # headers
curl -s -D - -o /dev/null "$URL/nonexist-xyz"    # 404 fingerprint
curl -s "$URL" | grep -aoE '(src|href)="[^"]+"' | sort -u   # assets, JS files, routes
```

## 2. Quick exposed-file probes

Run these before any fuzzing — they win challenges by themselves.

```bash
base="http://target:port"
for p in robots.txt sitemap.xml .git/HEAD .git/config .env .env.bak .env.local \
         server-status adminer.php phpmyadmin/ .DS_Store package.json \
         composer.json backup.zip backup.tar.gz www.zip source.zip site.zip \
         index.php.bak index.php~ .index.php.swp dump.sql database.sql; do
  out=$(curl -s -m 8 -o /dev/null -w '%{http_code} %{size_download}' "$base/$p")
  case "$out" in 404*) ;; *) echo "$out  $base/$p";; esac
done
```

| Hit | Meaning | Next |
|---|---|---|
| `/robots.txt`, `/sitemap.xml` | disallowed = interesting paths | fetch, test each `Disallow` |
| `/.git/HEAD` returns `ref: ...` | full source recoverable | git-dumper (below) |
| `/.env` | DB creds, API keys, Laravel `APP_KEY` | try creds on login/DB; `APP_KEY` → see `references/deser-files.md` |
| `/server-status` | Apache mod_status exposed | internal URLs, request paths |
| `package.json` / `composer.json` | exact deps and versions | CVE lookup, source-map hunt |
| `.swp`/`.bak`/`~` files | editor backups of server code | diff against live behavior |
| `/adminer.php`, `/phpmyadmin/` | DB front doors | default creds, session reuse |

Backup-file hunting with ffuf once basic fuzzing works:

```bash
ffuf -u "$base/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt \
     -e .bak,~,old,orig,txt,zip,tar.gz -ac -t 40
```

### Exposed `.git/` → git-dumper

```bash
# install (PyPI package, single command):
uv tool install git-dumper
# dump (target dir must not exist or be empty):
git-dumper "$base/.git/" src
cd src
git log --oneline --all        # history incl. deleted secrets
git log -p | less              # full diffs
git stash list; git fsck --lost-found   # dangling blobs = deleted flags/keys
```

If `.git/HEAD` is blocked but `/.git/config` leaks, manually fetch referenced
object paths — packfiles may still be reachable.

### JS source maps and bundles

```bash
curl -s "$base/static/js/app.js" | tail -c 200        # sourceMappingURL=app.js.map
curl -s -o app.js.map "$base/static/js/app.js.map"    # then pretty-print and read
.venv/bin/python -c "import json;d=json.load(open('app.js.map'));print('\n'.join(d['sources']))"
```

Source maps contain original file paths and code; bundles leak API routes and
hidden params even without maps: `grep -aoE '/api/[a-zA-Z0-9/_-]+' app.js | sort -u`.

### API documentation surfaces

| Path | What |
|---|---|
| `/swagger`, `/swagger-ui`, `/swagger-ui.html`, `/api-docs`, `/openapi.json`, `/v2/api-docs` | Swagger/OpenAPI spec |
| `/graphql`, `/api/graphql` | GraphQL endpoint (introspection below) |
| `/actuator`, `/actuator/env`, `/actuator/heapdump` | Spring Boot leaks (env vars, heap → creds) |
| `/debug`, `/metrics`, `/trace` | debug endpoints |
| `/api/` directory listing | framework default listings |

GraphQL manual introspection (works even when GUI tools fail):

```bash
curl -s "$base/graphql" -H 'Content-Type: application/json' -d \
'{"query":"{ __schema { queryType { name } mutationType { name } types { kind name fields { name args { name } } } } }"}' \
| .venv/bin/python -m json.tool
# then query concrete fields: {"query":"{ users { id username passwordHash } }"}
```

InQL (Burp extension) renders the schema tree once introspection returns anything.

## 3. ffuf — content, extension, recursion

Install (AUR on this host — ffuf is not in official repos): `paru -S ffuf` (or
`ffuf-bin`), or upstream binary from https://github.com/ffuf/ffuf/releases.

Wordlists (AUR package `seclists` → `/usr/share/seclists`, or
`git clone https://github.com/danielmiessler/SecLists`):

| List | Use |
|---|---|
| `Discovery/Web-Content/common.txt` | default content sweep |
| `Discovery/Web-Content/raft-small-words.txt` + `-e` extensions | backup/config hunt |
| `Discovery/Web-Content/directory-list-2.3-medium.txt` | deeper pass |
| `Discovery/DNS/subdomains-top1million-5000.txt` | vhost/subdomain mode |
| `Discovery/Web-Content/swagger.txt` | API-specific paths |

```bash
ffuf -u "$base/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -ac -t 40

# extensions (tests word AND word.ext), follow one redirect:
ffuf -u "$base/FUZZ" -w common.txt -e .php,.html,.js,.json,.bak -r -ac

# recursion (re-fuzzes discovered dirs, slower — use targeted):
ffuf -u "$base/FUZZ" -w common.txt -recursion -recursion-depth 2 -ac -t 50

# two keywords at once (dir list x extension list):
ffuf -u "$base/FUZZ.FUZ2Z" -w raft-small-words.txt -w ext.txt -ac

# POST bodies / params:
ffuf -u "$base/login" -X POST -d 'user=admin&pass=FUZZ' -w passwords.txt -fc 401
ffuf -u "$base/index.php?FUZZ=1" -w params.txt -ac        # param-name fuzzing

# useful flags: -fc 404,302   filter codes | -fs 1234 filter size (soft-404)
#              -mr 'admin'    match regex     | -o out.json -of json
#              -H 'Cookie: x=y'               | -ac auto-calibrate (soft-404 safe)
```

`-ac` is essential on apps returning 200 for everything: it self-calibrates size/word
counts. Write results to `recon/` in the challenge dir.

## 4. Vhost / subdomain enumeration

Many CTF web challenges serve different apps per `Host` header.

```bash
host=$(curl -s -o /dev/null -w '%{remote_ip}' http://target)     # resolve first
base_size=$(curl -s -H "Host: random-junk.target" "http://$host/" | wc -c)
ffuf -u "http://$host/" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -H "Host: FUZZ.target" -fs "$base_size" -t 40
# probe without DNS at all — any IP:port serving by Host header works the same way
```

Try likely names directly when fuzzing is blocked: `admin`, `dev`, `staging`,
`internal`, `flag`, `backup`, `old` as `Host:` values against the same IP.

## 5. Historical endpoints (Wayback)

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=target/*&fl=original&collapse=urlkey&output=text" \
  | sort -u | head -50
```

Old endpoints often still exist after links are removed (admin panels, `/backup`,
API v1). Also try `https://web.archive.org/web/2023/http://target/` snapshots for
deleted content.

## 6. Hidden parameter mining (arjun)

```bash
uv pip install --python .venv/bin/python arjun
scripts/ctf arjun -u "$base/profile" -m GET        # GET / POST / JSON / XML
```

Arjun finds params the app reads but never links (admin toggles, debug flags,
template params). Manual alternative: intercept a request and append
`?debug=1&admin=1&test=1&template=x&file=index&lang=en` — watch for response diffs.

## 7. Recon output layout

Keep everything under `work/<event>/web-<chal>/recon/`:

```
recon/headers.txt     curl -D output of /
recon/exposed.txt     quick-probe results
recon/ffuf-common.json, recon/vhosts.json
recon/src/            git-dumper output
```

`scripts/dirquick.sh` (this skill) automates sections 2 + 3 + 4 in one run.
