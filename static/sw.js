self.addEventListener('install',function(event){
    event.waitUntil(
        caches.open('sw-cache').then(function(cache){
            return cache.addAll([//the basic caches we need 
            ]);
        })
    );
});

self.addEventListener('fetch',function(event){
    event.respondWith(
        fetch(event.request, {cache: "no-store"}).catch(function() {
            return caches.match(event.request);
        })
    );
});