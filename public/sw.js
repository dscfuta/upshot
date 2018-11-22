const version = 'v0.1';
const prefix = "upshot";
const DEFINE_STATIC_CACHE = `${prefix}-static-${version}`;
const DEFINE_RUNTIME_CACHE = `${prefix}-runtime-${version}`;
const OFFLINE_URL = "offline.html";

var filesToCache = [
    '/',

    '/scripts/client.min.js',

    '/styles/reset.css',
    '/styles/client.css',


    '/font2/ionicons-2.0.1/fonts/ionicons.eot?v=2.0.0',
    '/font2/ionicons-2.0.1/fonts/ionicons.eot?v=2.0.0#iefix',
    '/font2/ionicons-2.0.1/fonts/ionicons.ttf?v=2.0.0',
    '/font2/ionicons-2.0.1/fonts/ionicons.woff?v=2.0.0',
    '/font2/ionicons-2.0.1/fonts/ionicons.svg?v=2.0.0#Ionicons',
    '/font2/ionicons-2.0.1/css/ionicons.min.css',

    '/manifest.json',
];

self.addEventListener('install', function(event) {

    event.waitUntil(
      caches.open(DEFINE_STATIC_CACHE)
        .then(function(cache) {
          return cache.addAll(filesToCache).then( ()=>{
            console.log('[ServiceWorker] Installed');
          });
        })
       .then(self.skipWaiting())
    )
});

var expectedCaches = [
    DEFINE_STATIC_CACHE,
    DEFINE_RUNTIME_CACHE
 ];

 self.addEventListener('activate', function(event) {

    event.waitUntil(
      caches.keys().then(function(cacheNames) {

        return Promise.all(
          cacheNames.map(function(cacheName) {

            if (cacheName.startsWith(prefix + '-')  && expectedCaches.indexOf(cacheName) === -1) {
                console.log('deleted');
                return caches.delete(cacheName);
            }

          })
        );
      })
      .then(()=> self.clients.claim() )
    );

  });


self.addEventListener('fetch', function (event) {
    event.respondWith(
        caches.match(event.request).then(function(response){
            return response || fetchAndCache(event)
        })
    )
});

const fetchAndCache = (event)=>{

    var request = event.request.clone();

    return fetch(request)
    .then(function(response){

        var res = response.clone();
        if (request.method === 'GET') {
            caches.open( DEFINE_RUNTIME_CACHE).then(function(cache) {
                console.log("cached....")
                cache.put(event.request.url, res);
            });
        }

        return response;

    })
    .catch(function(error) {
      return caches.match(OFFLINE_URL);
      console.log('Request failed:', error);
   });
}

self.addEventListener('push', function(event) {
    if (!(self.Notification && self.Notification.permission === 'granted')) {
      return;
  }
    console.log('[Service Worker] Push Received.' , event.data.json());

    let title = event.data.json().title || '';
    let body = event.data.json().message || '';
    let clickTarget = event.data.json().clickTarget || 'http://127.0.0.1:3000/';
    let id = event.data.json().id || "";

    let options = {
        body: body,
        icon: 'icons/',
        vibrate: [100, 50, 100],
        data: {
          dateOfArrival: Date.now(),
          clickTarget: clickTarget,
          id: id,
        }
    };
    event.waitUntil(self.registration.showNotification(title, options));
});


self.addEventListener('notificationclick', function(event) {
    console.log('[Service Worker] Notification click Received.');

    event.notification.close();

    event.waitUntil(
      clients.openWindow( event.notification.data.clickTarget + "?show=" + event.notification.data.id)
    );
});
