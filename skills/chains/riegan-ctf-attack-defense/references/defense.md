# Defense — patch doctrine, deploy pipeline, hardening

## Patch doctrine

1. **Minimal diff.** Every changed line is a chance to break a checker
   assertion. Fix the vulnerability at its site; do not refactor, do not
   "clean up".
2. **Checker green before deploy. No exceptions.** One `checker-wrap.sh` run
   against the patched replica gates every deploy (pipeline below).
3. **Patch series, not snapshots.** `orig/` stays pristine forever. Work in
   `patched/`; record every change as `patches/NNN-description.patch` in
   order. The deploy artifact is always `orig` + series, reproducible.
4. **Never upgrade frameworks or major deps mid-game.** `pip install -U`,
   `composer update`, `npm audit fix` pull new code you have not read — new
   attack surface, new breakage, and a fat diff. Patch in place.
5. **Patch the vuln, not the feature.** If the checker fails after your
   patch, you patched too much: narrow it until green again.

### Series mechanics

```
services/foo/
  orig/       pristine unpacked bundle (read-only, forever)
  patched/    working tree = orig + patches applied
  patches/    001-strlen-check.patch  002-sqli-prepare.patch ...
  verify/     throwaway rebuild target
```

```bash
cd services/foo
# record patch N
diff -ruN orig/src patched/src > patches/003-atoi-bounds.patch

# prove the whole series rebuilds from pristine (run after every new patch)
rm -rf verify && rsync -a orig/src/ verify/src/
for p in patches/*.patch; do patch -d verify -p2 < "$p" || break; done
diff -ruN verify/src patched/src && echo "series reproduces patched/"
```

Keep the `-p2` convention constant (paths `orig/src/...` in headers) so the
loop applies every patch the same way. Commit each patch with its own message.

## Per-language quick patches

| Language | Typical vuln class | Minimal patch at the site |
|---|---|---|
| C/C++ | `strcpy`/`sprintf` overflow, off-by-one, unchecked `atoi` index | bounds check at the parse site; replace copy with `snprintf(dst, sizeof dst, ...)` |
| Python | `eval`/`exec`, unpickled input, missing length/type checks, f-string SQL | `ast.literal_eval`; length/type check at entry; driver-parameter SQL |
| PHP | SQL string concat, dynamic `include`, `unserialize` | PDO prepared statement; fixed include list; `unserialize` allowed-classes |
| Node/JS | `eval`/`new Function`, prototype pollution, NoSQL operator injection | remove eval; validate/coerce input at the sink |
| Java | native deserialization, SQL concat | `ObjectInputFilter` whitelist; `PreparedStatement` |

### C — validate at the parse site

```c
/* vuln: attacker-controlled index straight into a fixed array */
int idx = atoi(buf);
do_send(fd, items[idx]);              /* out-of-bounds read / info leak */

/* patch: reject before first use — checker only ever sends valid idx */
int idx = atoi(buf);
if (idx < 0 || idx >= MAX_ITEMS) {
    dprintf(fd, "err\n");
    return;
}
do_send(fd, items[idx]);
```

```c
/* vuln: unbounded copy into stack buffer */
strcpy(name, req->name);
/* patch: */
snprintf(name, sizeof(name), "%s", req->name);
```

### Python — kill code exec, validate at entry

```python
# vuln: eval of a user-supplied expression
result = eval(expr)
# patch: literals only (numbers, strings, lists) — checker input still works
import ast
result = ast.literal_eval(expr)
```

```python
# entry-point validation: length + type before any parsing
def handle(data: bytes) -> None:
    if not isinstance(data, (bytes, bytearray)) or not 1 <= len(data) <= 4096:
        return reply(b"err\n")
```

```python
# vuln: f-string SQL          # patch: driver placeholder (sqlite3: "?")
cur.execute(f"SELECT * FROM t WHERE n = '{x}'")
cur.execute("SELECT * FROM t WHERE n = ?", (x,))
```

### PHP — prepared statements, unserialize whitelist

```php
// vuln: concatenated SQL
$q = $pdo->query("SELECT * FROM users WHERE name = '" . $_GET['n'] . "'");
// patch:
$stmt = $pdo->prepare('SELECT * FROM users WHERE name = ?');
$stmt->execute([$_GET['n']]);
```

```php
// vuln: unserialize of user bytes -> gadget chains
$obj = unserialize($_COOKIE['data']);
// patch: no object may be instantiated (PHP >= 7.0 second arg)
$obj = unserialize($_COOKIE['data'], ['allowed_classes' => false]);
```

### Node — sanitize at the sink

```js
// vuln: NoSQL operator injection — ?name[$gt]= dumps every user
User.find({ name: req.query.name });
// patch: coerce at the sink so only a plain string reaches the query
User.find({ name: String(req.query.name) });
```

```js
// vuln: computed code
const f = eval('(' + req.body.cb + ')');
// patch: dispatch table instead of eval
const actions = { ping: () => 'pong' };
const f = actions[req.body.cb];
if (!f) return res.status(400).end();
```

## Binary-only services

When there is no source: patch bytes, one instruction at a time, checker-gated
like everything else. Keep notes of every address + original bytes.

**radare2 file patch** (always work on a copy):

```bash
cp orig/svc binaries/svc.patched
r2 -w binaries/svc.patched
[0x00400b20]> aaa
[0x00400b20]> pdf @ sym.handle_cmd     # find the vulnerable call / missing check
[0x00400b20]> s 0x004012f3
[0x004012f3]> pd 8                     # disassemble BEFORE
[0x004012f3]> wa cmp esi, 0x200        # example: inject a bounds check (assemble)
[0x004012f3]> pd 8                     # disassemble AFTER — verify the bytes
```

Other useful writes at seek: `wx 9090` (nops), `wa jmp 0x00401310` (skip a
call). For PIE binaries note `r2 -B 0x400000` to inspect at a fixed base, but
patch using file offsets/vaddrs from the binary itself, then re-run the
checker locally — the checker does not care about your ASM aesthetics.

**gdb attach — runtime hot-patch (temporary)**: buys time while the file
patch is prepared; gone on service restart.

```bash
gdb -p "$(pidof svc)"
(gdb) set {char}0x4012f3 = 0x90        # nop one byte at runtime
(gdb) detach
```

ASLR/PIE: runtime addresses = file vaddr + load base from
`/proc/<pid>/maps`; compute before writing.

**Validating proxy (no binary edits)**: move the real service to
`127.0.0.1:5001`, front it with a small proxy on :5000 that enforces the
protocol and logs every payload (the log doubles as your exploit feed,
`offense.md`):

```python
#!/usr/bin/env python3
# proxy.py — validating, logging TCP front for a raw-protocol service.
import asyncio, re, time

UPSTREAM = ("127.0.0.1", 5001)
MAX_LINE = 256                       # tune to checker's longest request + slack
OK = re.compile(rb"^[A-Za-z0-9 ._+-]{1,%d}\n$" % MAX_LINE)
LOG = open("proxy.log", "ab")

async def pipe(reader, writer, direction, check=False):
    try:
        while data := await reader.read(4096):
            LOG.write(f"{time.time():.0f} {direction}\n".encode() + data + b"\n")
            LOG.flush()
            if check and not OK.match(data):
                writer.write(b"err\n"); break
            writer.write(data)
            await writer.drain()
    except OSError:
        pass
    finally:
        writer.close()

async def handle(client):
    try:
        upstream = await asyncio.open_connection(*UPSTREAM)
    except OSError:
        client.close(); return
    await asyncio.gather(pipe(client, upstream, ">", check=True),
                         pipe(upstream, client, "<"))

async def main():
    server = await asyncio.start_server(handle, "0.0.0.0", 5000)
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

Rules for the validator: read the checker first, permit exactly what it sends
(plus slack), reject everything else. A proxy that blocks the checker is an
own goal; a checker-shaped hole an attacker fits through is decoration.

## Deploy pipeline (per patch)

```bash
# 0. local gates: series applies clean + checker green on the replica
cd work/<event>
scripts/checker-wrap.sh -n foo -t 60 -- \
    python3 services/foo/checker/check.py 127.0.0.1 5000

# 1. ship (deploy artifact = fresh apply of orig + patches, never ad-hoc edits)
rsync -a --delete services/foo/patched/src/ gamebox:~/svc/src/

# 2. restart via the event-supplied mechanism (systemctl/supervisor/redeploy API)
ssh gamebox 'sudo systemctl restart foo'

# 3. verify IMMEDIATELY — the scoreboard checks next tick, you check now
scripts/checker-wrap.sh -n foo -t 60 -- \
    python3 services/foo/checker/check.py gamebox-host 5000

# 4. on FAIL: rollback to last-known-good, then re-check
ssh gamebox 'rm -rf ~/svc/src && mv ~/svc/good ~/svc/src && sudo systemctl restart foo'
scripts/checker-wrap.sh -n foo -t 60 -- python3 services/foo/checker/check.py gamebox-host 5000
```

Rollback discipline: after every green deploy, refresh the on-box good copy:

```bash
rsync -a services/foo/patched/src/ gamebox:~/svc/good/
```

## Hardening (gamebox)

**Firewall to service ports only** (nftables; SSH must be allowed *first*):

```bash
sudo nft add table inet ad
sudo nft 'add chain inet ad input { type filter hook input priority 0 ; policy accept ; }'
sudo nft add rule inet ad input iif lo accept
sudo nft add rule inet ad input ct state established,related accept
sudo nft add rule inet ad input ip saddr <team-vpn-subnet> tcp dport 22 accept
sudo nft add rule inet ad input tcp dport { 5000 } accept
sudo nft add rule inet ad input drop
```

iptables equivalent, same ordering trap:

```bash
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -s <team-vpn-subnet> -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables -A INPUT -j DROP        # never before the allows above
```

**Rate limiting** on the service port (blunts floods and dumb brute forcers):

```bash
sudo nft add rule inet ad input tcp dport 5000 ct state new \
     limit rate 10/second burst 20 packets accept
```

```bash
sudo iptables -A INPUT -p tcp --dport 5000 -m conntrack --ctstate NEW \
     -m limit --limit 10/s --limit-burst 20 -j ACCEPT
```

Set the limit above the checker's own connect rate or you will fail your own
SLA. **fail2ban concept** (`sudo pacman -S fail2ban`): a jail tails the
service/proxy log, counts abuse signatures per source IP (oversized lines,
regex hits from `proxy.log`), bans via firewall on `maxretry` within
`findtime`:

```ini
# /etc/fail2ban/jail.local (sketch — filter must match YOUR log format)
[ad-foo]
enabled  = true
filter   = ad-foo
logpath  = /home/team/svc/proxy.log
maxretry = 8
findtime = 60
bantime  = 300
```

Never ban the checker/bot: allowlist its source IP (`ignoreip`) and confirm
your filter does not match benign checker traffic — test the filter against a
baseline capture before enabling the jail.

**Log every request with the full payload.** Proxy log (`proxy.log` above) +
always-on tcpdump (`offense.md`). Incoming attacks are your exploit feed: the
same pcap defends you (patch the bug they hit) and attacks for you (adapt
their payload).

**Alerting on SLA dips** — from `checker-wrap.sh` verdicts:

```bash
n=$(grep ' foo ' monitor/verdicts.log | tail -n 2 | awk '$3=="FAIL"' | wc -l)
[ "$n" -eq 2 ] && curl -sf -X POST -d "svc=foo&msg=SLA down 2 ticks" "$WEBHOOK" \
              || notify-send "A/D" "svc-foo SLA FAIL x2"
```

Run per tick from the same timer that runs the checker (`infra.md`).

## Not this skill

King-of-the-hill / hold-the-box (no ticks, shared scoreboard per foothold) is
the sibling skill `ctf-boot2root` — fortification doctrine lives there.
