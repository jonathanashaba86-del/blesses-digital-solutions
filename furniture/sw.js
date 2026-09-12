/* Nyumba Furniture Co. — offline shell.
   The catalogue is drawn, not photographed, so the whole shop is one
   file and it works with no connection at all once it has been opened. */
const CACHE = 'nyumba-v1';
const SHELL = ['./', './index.html', './site.webmanifest', './icon-192.png', './icon-512.png'];

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

  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok && (url.origin === location.origin || /fonts\.(googleapis|gstatic)/.test(url.host))) {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => hit))
  );
});
