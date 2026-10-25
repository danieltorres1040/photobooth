// Keeps the booth working offline (e.g. while the iPad is joined to the Selphy's own Wi-Fi).
// Network-first so updates arrive when online; falls back to the cached copy when offline.
const CACHE = 'booth-v30';  // bump this number whenever you change the files
const SHELL = ['./', './index.html', './manifest.json', './icon.png', './logo.png', './frames.json', './qr.js', './bg.mp4', './bg-poster.jpg', './bg-still.jpg',
  './fonts/Inter-Regular.woff', './fonts/Inter-Medium.woff', './fonts/Inter-SemiBold.woff'];

self.addEventListener('install', e => {
  // also cache every frame listed in frames.json, so new frames work offline without editing this file
  e.waitUntil(caches.open(CACHE).then(async c => {
    await c.addAll(SHELL);
    try {
      const list = await (await fetch('./frames.json', { cache: 'no-cache' })).json();
      await c.addAll((list.frames || []).filter(f => f.file).map(f => './' + f.file));
    } catch (err) {}
  }).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function timeout(ms) { return new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), ms)); }

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin || /\/(print|status)$/.test(url.pathname)) return;
  e.respondWith(
    Promise.race([fetch(e.request), timeout(3000)])
      .then(res => {
        if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
        return res;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('./index.html')))
  );
});
