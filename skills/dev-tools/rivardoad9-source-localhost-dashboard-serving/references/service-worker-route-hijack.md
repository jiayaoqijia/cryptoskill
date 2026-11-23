# Service-worker route hijack (one page's SW breaking its sibling)

Session: 6 Oct 2026, ZemizTracker (`/`) + Zemiz Risk (`/risk`), served by one stdlib server on
`127.0.0.1:8787` behind a cloudflared quick tunnel. User report: **"aplikasi kita eror ga muncul"**,
later narrowed to **"zemiz risk benerin dong, mana linknya"**.

## The confusing part (why it took a while)

Every server-side check was green, all day:

```
/        local 200 24764b | public 200 24764b
/risk    local 200 52001b | public 200 52001b
/api/risk 200 62568b      /healthz 200
```

Headless render was green too: `/risk` at a 390px viewport, `documentElement.scrollWidth == clientWidth
== 390`, zero console errors, 12 sections rendered with live numbers. So "server sehat, semua 200" AND
"user bilang eror" were both true at the same time — the bug lived ONLY on the phone that had the PWA
installed, and only through service-worker-controlled navigations.

Lesson: when the user says "eror" and the server says 200, suspect the CLIENT-side layer (service
worker / cache / installed PWA), not the backend, and reproduce it in a browser context that actually
registers the SW.

## Root cause (risk_sw.js, served at /sw.js with scope "/")

```js
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.origin !== location.origin) return;

  if (u.pathname.startsWith('/api/')) { e.respondWith(fetch(req).catch(() => caches.match(req))); return; }

  // BUG: every navigation is treated as "mine" …
  if (req.mode === 'navigate' || u.pathname === '/risk' || u.pathname === '/') {
    e.respondWith(
      fetch(req).then(r => {
        const c = r.clone();
        caches.open(CACHE).then(x => x.put('/risk', c));   // … and stored under a FIXED key
        return r;
      }).catch(() => caches.match('/risk'))                // … then served as the /risk fallback
    );
    return;
  }
  …
});
```

Two failure modes, both user-visible:

1. **Wrong app from cache** — navigating to `/` (ZemizTracker) while offline/flaky fell through to
   `caches.match('/risk')`, i.e. the tracker opened showing the RISK page.
2. **Cache poisoning the other way** — any successful navigation (including `/`) was written to the
   `/risk` cache key, so visiting the tracker overwrote the cached risk shell with tracker HTML.

Scope `"/"` meant the SW also controlled `/`, so the tracker was inside its blast radius even though
only the risk page registers it (`porto_dashboard.html` → `navigator.serviceWorker.register('/sw.js')`).

## The fix

- Only handle your own paths: `RISK_PATHS = ['/risk','/zemizrisk','/portofolio','/risiko'];
  if (RISK_PATHS.includes(u.pathname)) { … }` — everything else is left to the network untouched
  (no `respondWith`, so the browser does normal navigation).
- Cache under the requested URL (`x.put('/risk', c)` only for the risk routes), never blanket-write a
  fixed key from a handler that fires for other routes.
- Bump the cache name (`zemizrisk-v4` → `v5`) so `activate` deletes the stale caches:
  `caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))`.
  `skipWaiting()` + `clients.claim()` make the new SW take over on the next load.
- Serve `/sw.js` with `Cache-Control: public, max-age=300` (not 86400) so devices pick the fix up
  within minutes instead of a day.

## Verification that actually proves it

Click-through test (also proves the cross-nav links):

```
1) tracker punya link Risk: True
2) URL setelah klik: .../risk
3) judul: ZEMIZ RISK — Monitor Risiko Portofolio | ada 'Kesehatan Portofolio': True
4) service worker aktif: ['.../sw.js']
6) URL setelah klik Tracker: .../ | judul: ZemizTracker · Whale Hyperliquid
errors: []
```

Hijack test (the one that matters) — load `/risk`, let the SW take control, then go OFFLINE and
navigate to the sibling route:

```python
print("SW controlled:", await pg.evaluate("!!navigator.serviceWorker.controller"))   # True
await ctx.set_offline(True)
try:
    await pg.goto(BASE + "/", wait_until="load", timeout=20000)
    txt = await pg.inner_text("body")
    print("HIJACK" if "ZEMIZ RISK" in txt else "ok")
except Exception as exc:
    print("gagal load wajar (tidak dibajak):", str(exc)[:70])
```

Before the fix: `/` offline rendered the RISK page. After: `Page.goto: net::ERR_FAILED` — a normal
offline failure, i.e. the SW no longer substitutes the wrong document. Ship that assertion, not
"looks fine to me".

## Related defect found in the same pass

There was **no link back from `/risk` to `/`** (and the tracker→risk link was icon-only on phone,
`🛡️<span class="hidesm"> Risk</span>`), so from the phone the second app was effectively unreachable:
"mana linknya". Whenever you ship a second route/app on the same origin, wire BOTH directions and
verify the click actually changes the document (title change), not just that the href exists.

## User-facing handoff

The stale SW lives on the user's device, so the fix alone isn't enough — tell them: close the tab and
reopen (or delete the home-screen shortcut and re-add from the fresh link). The server can't clear a
device cache.
