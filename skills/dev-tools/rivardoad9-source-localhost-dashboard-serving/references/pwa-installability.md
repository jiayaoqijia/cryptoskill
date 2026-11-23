# Installable PWA for an agent dashboard ("kenapa ga bisa di-download appnya?")

The predictable follow-up once a dashboard is on the user's phone. Answer it in the same pass as the
page — not after they complain.

## Why a plain page is not installable

A page with `apple-mobile-web-app-capable` + a favicon still is NOT an app: Chrome only offers
"Install app" when it can parse a **manifest**, has an **active service worker** with scope `/`, and
has **192px + 512px PNG icons** fetched over **HTTPS or localhost**. Without them, "Add to Home
Screen" makes a bookmark that still shows the address bar — which is exactly what the user experienced.

Three assets, all served by the existing stdlib server (no build step, no deps):

1. `manifest.json` → `templates/pwa_manifest.json`
2. service worker at root path → `templates/pwa_service_worker.js`
3. PNG icons 192/512 → `scripts/gen_pwa_icons.py` (headless chromium renders an inline SVG; no PIL on
   this host)

## Server routes (add to the stdlib handler)

The template's `_send()` hard-codes `Cache-Control: no-store`. Give it a cache parameter — the SW must
NOT be `no-store` (see pitfalls) — and add a binary file sender:

```python
    def _send(self, code, body, ctype, cache="no-store"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_file(self, path, ctype, cache="public, max-age=86400"):
        try:
            with open(path, "rb") as f:
                self._send(200, f.read(), ctype, cache)
        except Exception as exc:
            self._send(404, f"file hilang: {os.path.basename(path)} ({type(exc).__name__})".encode(),
                       "text/plain; charset=utf-8")
```

Routes (put them BEFORE the generic `/api/*` branch):

```python
        elif u.path in ("/manifest.json", "/sw.js", "/icon-192.png", "/icon-512.png", "/apple-touch-icon.png"):
            if u.path == "/manifest.json":
                self._send_file(MANIFEST, "application/manifest+json; charset=utf-8", "public, max-age=600")
            elif u.path == "/sw.js":
                # NB: jangan no-store -> Chrome nolak daftarin service worker
                self._send_file(SW, "application/javascript; charset=utf-8", "public, max-age=300")
            elif u.path == "/icon-512.png":
                self._send_file(os.path.join(HERE, "icon-512.png"), "image/png")
            else:
                self._send_file(os.path.join(HERE, "icon-192.png"), "image/png")
```

Binary assets need a bytes read (`"rb"`) — serving a PNG through the text path yields a broken image.

## HTML head + install button

```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0a0f1c">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="ZemizRisk">
<link rel="apple-touch-icon" href="/icon-192.png">
```

```js
let deferred = null;
addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferred = e; showInstallBar(); });
btnInstall.onclick = async () => { deferred && deferred.prompt(); await deferred.userChoice; deferred = null; };
if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(() => {});
```

iOS never fires `beforeinstallprompt` — tell the user: **Share → "Add to Home Screen"**. The install
button should fall back to that instruction instead of doing nothing.

## Verify installability numerically (don't just claim it)

```python
cdp = await ctx.new_cdp_session(page)          # playwright
man = await cdp.send("Page.getAppManifest")
print(man.get("url"), man.get("errors"))       # errors == [] is the pass condition
sw = await page.evaluate("""async () => {const r = await navigator.serviceWorker.getRegistrations();
  return {count:r.length, scopes:r.map(x=>x.scope), active:r.map(x=>!!x.active)};}""")
```

Pass = manifest parsed with `errors: []`, `count: 1`, `active: [true]`. Then curl the public tunnel
for the four paths and assert `content_type` (`application/manifest+json`,
`application/javascript`, `image/png`) — installability is checked on the real host, not just localhost.

## Token-gated dashboards: the gate and installability fight each other

The install assets are fetched BY THE BROWSER, not by the page: no `?k=` on the request, and Chrome's
manifest fetch does not even send the cookie (verified — an authed page's manifest came back as
`start_url: "/"`). An all-or-nothing gate therefore makes "Install app" silently unavailable.

- Keep the gate on the page and `/api/*` only. Add a PUBLIC set — `/manifest.json`,
  `/manifest.webmanifest`, `/sw.js`, `/icon*.png`, `/icon.svg` (plus `/healthz`) — that skips the 401.
  Those files leak nothing on their own.
- NEVER ship the token in a publicly served manifest — anyone curling `/manifest.json` would get the
  key. Inject `start_url = "/?k=" + TOKEN` into the manifest response ONLY when that request is authed
  itself (`?k=` or a `k=` cookie); everyone else gets `start_url: "/"`.
- Keep the installed app usable anyway: an inline `<script>` in `<head>` (so it runs before anything
  fetches) does `if (search has k=) localStorage.setItem("kk", k); else if (localStorage.kk)
  location.replace(pathname + "?k=" + localStorage.kk)`. Android/Chrome PWAs share the origin's
  storage, so that redirect covers a tokenless `start_url`; iOS uses the CURRENT page URL as the
  home-screen start URL, so installing from the keyed link also lands keyed.
- The SW navigation branch must cache under a FIXED key (`x.put("/shell", r.clone())`, fallback
  `caches.match("/shell")`): the page URL carries `?k=`, so `caches.match("/")` never hits. Guard the
  write with `if (r.ok)` — a cached 401 locks the user out of their own installed app.
- Every SW fetch handler returns early for `/api/*` (and `/healthz`): live numbers must never come out
  of the cache.

## Pitfalls

- **Service worker served with `Cache-Control: no-store` is refused by Chrome.** The registration
  silently never activates. Use `max-age=300` for `/sw.js` and keep `no-store` only for the HTML API
  responses.
- **Registry/dedup trap:** if a dashboard already had a SW, bump the cache name (`zemizrisk-v1` →
  `-v2`) when the shell changes; keep the HTML network-first so edits land without a version bump.
- **Quick-tunnel URL rotation breaks an installed app.** The installed PWA pins `start_url` to the
  host it was installed from; when cloudflared restarts and `trycloudflare` gives a new hostname, the
  home-screen icon points at a dead URL and must be re-installed. Say this plainly and offer the
  permanent option (Cloudflare named tunnel + own domain).
- **Icon without a font dependency.** Emoji glyphs may render as tofu in headless chromium — draw the
  icon as inline SVG shapes (gradient shield + gauge ring) and screenshot it with
  `omit_background=True`. Supply a `purpose: "maskable"` entry with generous padding so Android's
  round mask doesn't clip it.
- **A gate that also covers the install assets kills installation silently.** 401 on manifest/sw/icons
  produces no visible error — it just never offers the install prompt, and a page that still has
  `apple-mobile-web-app-capable` gives the user a bookmark with an address bar ("kenapa ga bisa di
  download appnya?"). Prove the split per path: page + `/api/*` → 401 bare; assets → 200 bare; and the
  bare `/manifest.json` must NOT contain the token.
- **An installed app that opens straight to the locked page.** Tokenless `start_url` plus nothing in
  storage = the home-screen icon lands on the 401 page. The `<head>` localStorage redirect fixes it,
  but only for a browser that has opened the keyed link at least once — install from the KEYED link,
  open it once, and only then tell the user it's done.
- **Quick-tunnel hostname change also invalidates the stored key's origin.** The localStorage/`kk` and
  the cookie are per-origin, so after cloudflared rotates the hostname the user must open the new
  keyed link once; say that in the same message as the new URL.
