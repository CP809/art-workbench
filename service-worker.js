/* 美术台 - Service Worker（离线缓存）
   版本 art-v2：新增 daily.js 每日数据 + nocache 强制更新通道 */
const CACHE = 'art-v3';
const ASSETS = [
  './',
  './index.html',
  './data.js',
  './daily.js',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  // 带 nocache 参数：强制走网络并回填缓存（手机端「🔄 更新」按钮专用）
  if (url.searchParams.has('nocache')) {
    e.respondWith(
      fetch(e.request).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(url.origin + url.pathname, copy));
        return res;
      })
    );
    return;
  }
  // 跨域请求直接走网络，不进缓存
  if (url.origin !== self.location.origin) {
    e.respondWith(fetch(e.request));
    return;
  }
  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) return cached;
      return fetch(e.request).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
