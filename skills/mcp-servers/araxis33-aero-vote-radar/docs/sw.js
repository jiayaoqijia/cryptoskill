// Service worker for the radar's "Notify me" alerts (index.html, arPush*).
// Pushes arrive without a payload; the text waiting for this browser is
// fetched from the Worker that sent it (base-tools/check-worker/push.js).
const PUSH_API = "https://deftools-check.araxis67.workers.dev/push/msg";
const RADAR = "https://aero.deftools.xyz/";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

self.addEventListener("push", (event) => {
  event.waitUntil((async () => {
    let msg = { title: "Aero Vote Radar", body: "Open the radar to see your timers.", url: RADAR };
    try {
      const sub = await self.registration.pushManager.getSubscription();
      if (sub) {
        const r = await fetch(PUSH_API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ endpoint: sub.endpoint }) });
        if (r.ok) msg = { ...msg, ...(await r.json()) };
      }
    } catch (e) { /* show the plain message */ }
    await self.registration.showNotification(msg.title, { body: msg.body, icon: RADAR + "card-v3.png", tag: "aero-radar", data: { url: msg.url || RADAR } });
  })());
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || RADAR;
  event.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
    const open = all.find((c) => c.url.startsWith(RADAR));
    if (open) return open.focus();
    return self.clients.openWindow(url);
  })());
});
