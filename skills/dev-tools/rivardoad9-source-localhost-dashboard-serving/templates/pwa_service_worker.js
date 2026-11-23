/* PWA service worker for an agent dashboard served from the stdlib server.
 * Rules that matter (see references/pwa-installability.md):
 *   - serve this file as application/javascript with Cache-Control: public, max-age=300
 *     (NOT no-store — Chrome refuses to register a no-store service worker)
 *   - HTML navigation is NETWORK-FIRST so edits land immediately;
 *     cache-first only for icons/manifest; API stays network-only.
 *   - bump CACHE when the shell/assets change.
 */
const CACHE = 'zemizrisk-v1';
const SHELL = ['/risk', '/manifest.json', '/icon-192.png', '/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).catch(() => {}).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.origin !== location.origin) return;

  // API: network first, cache only as the offline fallback
  if (u.pathname.startsWith('/api/')) {
    e.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }
  // HTML: network-first, so a redeploy is visible without bumping the cache name
  if (req.mode === 'navigate' || u.pathname === '/risk' || u.pathname === '/') {
    e.respondWith(
      fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put('/risk', c)); return r; })
        .catch(() => caches.match('/risk'))
    );
    return;
  }
  // static assets (icons/manifest): cache-first
  e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => {
    const c = res.clone(); caches.open(CACHE).then(x => x.put(req, c)); return res;
  }).catch(() => r)));
});
