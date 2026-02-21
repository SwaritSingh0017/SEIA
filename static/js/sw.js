// sw.js — SEIA Service Worker (PWA)
// Caches static assets for offline/fast loading
 
const CACHE_NAME = 'seia-v1';
const STATIC_ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/css/chat.css',
  '/static/css/dashboard.css',
  '/static/js/chat.js',
  '/static/js/voice.js',
  '/static/js/mood.js',
  '/static/js/tasks.js',
  'https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Syne:wght@300;400;500;600&display=swap',
];
 
// Install — cache all static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch(() => {
        // Fail silently — some assets might not be available offline
      });
    })
  );
  self.skipWaiting();
});
 
// Activate — clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});
 
// Fetch — network first, fall back to cache
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
 
  // Always go to network for API calls
  if (url.pathname.startsWith('/api/')) {
    return;
  }
 
  // Network first strategy
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache successful responses for static assets
        if (response.ok && event.request.method === 'GET') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => {
        // Fall back to cache
        return caches.match(event.request).then((cached) => {
          if (cached) return cached;
          // Return offline page for navigation requests
          if (event.request.mode === 'navigate') {
            return new Response(
              '<html><body style="background:#02050e;color:#60a5fa;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center;">' +
              '<div><div style="font-size:3rem;margin-bottom:16px;">📡</div>' +
              '<h2>SEIA is offline</h2>' +
              '<p style="color:#6b85b5;">Check your connection and try again.</p></div></body></html>',
              { headers: { 'Content-Type': 'text/html' } }
            );
          }
        });
      })
  );
});
 
