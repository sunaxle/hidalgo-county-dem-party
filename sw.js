const CACHE_NAME = 'join-app-v2';
const urlsToCache = [
  '/join.html',
  '/css/state_party_clone.css',
  '/css/a11y.css',
  '/js/app.js',
  '/js/form_handler.js',
  '/js/value_counter.js',
  '/images/facebook_1656248751972_6946810765393131439.webp',
  '/images/hidalgo_dems_logo.png',
  '/images/icon-192.png',
  '/images/icon-512.png',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request).catch(() => {
          // If network request fails and it's a navigation request, try to return join.html
          if (event.request.mode === 'navigate') {
            return caches.match('/join.html');
          }
        });
      })
  );
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
