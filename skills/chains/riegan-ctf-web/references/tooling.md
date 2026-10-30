# Tooling — proxies, browsers, listeners, local mirrors

## 1. Proxies

### mitmproxy (scriptable, first choice for automation)

```bash
sudo pacman -S mitmproxy
mitmproxy                # terminal UI, port 8080
mitmweb                  # web UI at http://127.0.0.1:8081, proxy on 8080
mitmdump -s addon.py     # headless + scripting — best for CTF loops
```

```python
# addon.py — example: flag sniffing + auto-repeater
from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    body = flow.response.get_text(strict=False) or ""
    if "flag{" in body or "FLAG{" in body:
        print(f"[FLAG] {flow.request.url}\n{body[:500]}")

def request(flow: http.HTTPFlow) -> None:
    # mutate every request transparently
    if "debug" not in flow.request.query:
        flow.request.query["debug"] = "1"
```

Run: `mitmdump -s addon.py`, point the target's tools at `http://127.0.0.1:8080`.
Cert: mitmproxy CA at `~/.mitmproxy/mitmproxy-ca-cert.pem` (import into the
browser/tool when HTTPS interception fails).

### Burp Suite

```text
burpsuite                # AUR package `burpsuite` (paru -S burpsuite)
# or: download the community jar from portswigger.net/burp/communitydownload
#     and run: java -jar burpsuite_community.jar     (JDK 21 present on this host)
```

Essential built-ins: Repeater, Intruder (pitchfork/sniper/battering ram),
"Send group in parallel" in Repeater (race conditions), matched-response diffing.
BApp extensions worth installing: HTTP Request Smuggler, Turbo Intruder,
Param Miner, JWT Editor, Collaborator Everywhere.

### sqlmap through the proxy

```bash
sqlmap -r request.txt --batch --proxy http://127.0.0.1:8080
# force traffic even when tools try direct: --proxy socks5://127.0.0.1:9050 also works
```

### ffuf modes recap

```bash
ffuf -u "$base/FUZZ" -w common.txt -o recon/ffuf.json -of json          # dirs
ffuf -u "$base/FUZZ.FUZ2Z" -w raft-small-words.txt -w ext.txt -ac       # x extensions
ffuf -X POST -u "$base/login" -d 'user=admin&pass=FUZZ' -w pwds.txt     # post body
ffuf -u "$base" -H "Host: FUZZ.target" -w subs.txt -fs 1234             # vhosts
ffuf -u "$base/FUZZ=1" -w params.txt -ac                                # param names
```

## 2. Browser automation

This agent harness includes a browser tool (skill `agent-browser`): use it for
JS-heavy apps, login flows, admin-bot debugging, WebSocket/SSE apps, and any
challenge where curl misses client-side rendering. Capture the resulting requests
and replay them in curl/mitmproxy for speed. Local mirrors only, per the router gate.

## 3. HTTP clients from the shell

```bash
# curl cookie jar flows (login -> authenticated action -> logout):
curl -s -c jar.txt "$base/login" -d 'user=a&pass=b' -L
curl -s -b jar.txt -c jar.txt "$base/profile"
curl -s -b jar.txt "$base/api/secret"

# curl with raw request replay (from Burp "Copy to file" or manual):
curl -s --http1.1 -H 'Content-Type: application/json' -d @req.json "$base/api/x"

# httpie (nicer for exploratory JSON work):
sudo pacman -S httpie          # or: uv tool install httpie
http --session=jar --form POST "$base/login" user=a pass=b --follow
http --session=jar "$base/api/secret"
```

## 4. WebSockets

```bash
sudo pacman -S websocat        # (cargo install websocat also works)
websocat ws://target/ws        # interactive client: send/recv frames
echo '{"action":"ping"}' | websocat ws://target/ws
websocat -s 8080               # listener: print frames sent by victim pages (XSS exfil)
```

Proxy WebSocket testing: Burp intercepts ws:// natively (WebSocket history tab);
mitmproxy 10+ shows websocket flows. Origin and auth headers are the usual bug:
`websocat ws://target/ws -H "Origin: https://target"` vs a foreign origin.

## 5. Out-of-band callbacks (blind bugs)

```bash
go install -v github.com/projectdiscovery/interactsh-client@latest
interactsh-client              # prints a *.oast.pro domain; watch live DNS/HTTP hits
```

Use the generated domain in blind command injection, XXE, SSRF, jku/x5u JWT
headers, and ysoserial URLDNS payloads. Self-host with a VPS + DNS when the
challenge network blocks outbound — coordinate with the user (router gate).

## 6. Local mirrors (ungated)

```bash
php -S 127.0.0.1:8000                    # PHP source trees (sudo pacman -S php)
php -S 127.0.0.1:8000 -t dist/www        # with docroot
python3 -m http.server 8000              # static / quick check
scripts/ctf python app.py                # flask apps against repo venv
podman run --rm -p 8080:80 -v "$PWD/dist":/usr/share/nginx/html:ro,Z docker.io/library/nginx:alpine
# shipped Dockerfile / docker-compose.yml:
podman build -t chal . && podman run --rm -p 127.0.0.1:8080:80 chal
```

Point `dirquick.sh`, ffuf, sqlmap, and the browser at `127.0.0.1` mirrors to build
and verify payloads with zero gate friction, then replay the final exploit against
the remote once approved.

## 7. Workspace hygiene

- All recon artifacts into `recon/` in the challenge dir.
- One Burp project file per challenge (state: sessions, repeater tabs).
- mitmproxy flows saved with `mitmdump -w flows.txt` are replayable:
  `mitmdump -nr flows.txt -s addon.py` re-runs analysis offline.
