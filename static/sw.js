const version = 'v0.1';
const prefix = "upshot";
const DEFINE_STATIC_CACHE = `${prefix}-static-${version}`;
const DEFINE_RUNTIME_CACHE = `${prefix}-runtime-${version}`;
const OFFLINE_URL = "offline.html";
var filesToCache = [
    '/offline.html',
    '/about',
    '/app',
    '/',

    '/static/scripts/client.min.js',
    '/static/styles/reset.css',
    '/static/styles/client.css',

    '/static/assets/UpshotGoogleChrome1_6_2019.gif',


    '/static/font2/ionicons-2.0.1/fonts/ionicons.eot?v=2.0.0',
    '/static/font2/ionicons-2.0.1/fonts/ionicons.ttf?v=2.0.0',
    '/static/font2/ionicons-2.0.1/fonts/ionicons.woff?v=2.0.0',
    '/static/font2/ionicons-2.0.1/fonts/ionicons.svg?v=2.0.0#Ionicons',
    '/static/font2/ionicons-2.0.1/css/ionicons.min.css',

    '/manifest.json',
    "./static/icons/icon-blue64.png",
    "./static/icons/icon-blue128.png",
    "./static/icons/icon-blue256.png"
];

self.addEventListener('install', function(event) {

    event.waitUntil(
      caches.open(DEFINE_STATIC_CACHE)
        .then(function(cache) {
          return cache.addAll(filesToCache).then( ()=>{

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

                cache.put(event.request.url, res);
            });
        }

        return response;

    })
    .catch(function(error) {
      return caches.match(OFFLINE_URL);
   });
}
