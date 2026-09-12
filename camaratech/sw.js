/* Camara Tech — offline shell.
   Cache-first for the shop itself, network-first for everything else, and a
   graceful fall back to whatever was cached when the line drops. Kampala
   connections drop; the shop should not. */
const CACHE = 'camaratech-v3';
const SHELL = [
  './',
  './index.html',
  './site.webmanifest',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  /* The page itself: serve it instantly from cache, refresh it in the background. */
  if (req.mode === 'navigate' || url.pathname.endsWith('/index.html')) {
    e.respondWith(
      caches.match('./index.html').then(hit => {
        const live = fetch(req).then(res => {
          caches.open(CACHE).then(c => c.put('./index.html', res.clone()));
          return res;
        }).catch(() => hit);
        return hit || live;
      })
    );
    return;
  }

  /* Product photography and fonts: cache whatever succeeds, reuse it forever after. */
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok && (url.origin === location.origin || /images\.unsplash|fonts\.(googleapis|gstatic)/.test(url.host))) {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => hit))
  );
});
