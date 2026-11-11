// Offline support. Bump the version when you upload a new index.html.
const CACHE = 'rfd-picks-2027-v2';
const SHELL = ['./', 'index.html', 'how-to.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png',
  'guide/01-shift.webp', 'guide/02-mot-group.webp', 'guide/03-show.webp', 'guide/04-allotments.webp', 'guide/05-dock.webp', 'guide/06-calendar-wish.webp', 'guide/07-wish-list.webp', 'guide/08-eso.webp', 'guide/09-calendar-awarded.webp', 'guide/10-views.webp', 'guide/11-actions.webp'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Network first so updates show up; fall back to the saved copy when offline.
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(r => {
      if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return r;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html')))
  );
});
