/* MANNIE service worker — the shop opens even on a dead connection.
   Bump CACHE when you redeploy so returning visitors get the new file. */
const CACHE = 'mannie-v2';
const IMGS  = 'mannie-img-v2';
const SHELL = ['./', './index.html', './site.webmanifest'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== IMGS).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url) } catch (err) { return }

  /* Photographs — cache first, refresh quietly behind it.
     Every path returns a Response: a handler that resolves to undefined
     turns a perfectly good image into a broken one, and a failed fetch must
     never be written to the cache or it poisons the next visit. */
  if (url.hostname === 'images.unsplash.com') {
    e.respondWith((async () => {
      const cache = await caches.open(IMGS);
      const hit = await cache.match(req);
      if (hit) {
        e.waitUntil(fetch(req).then(r => { if (r && r.ok) cache.put(req, r.clone()) }).catch(() => {}));
        return hit;
      }
      try {
        const res = await fetch(req);
        if (res && res.ok && res.type !== 'opaque') cache.put(req, res.clone());
        return res;
      } catch (err) {
        return Response.error();   // the page falls back to its vector render
      }
    })());
    return;
  }

  /* The page itself — network first, cache as the safety net. */
  if (req.mode === 'navigate' || url.origin === location.origin) {
    e.respondWith((async () => {
      try {
        const res = await fetch(req);
        if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {}) }
        return res;
      } catch (err) {
        return (await caches.match(req)) || (await caches.match('./index.html')) || Response.error();
      }
    })());
  }
});
