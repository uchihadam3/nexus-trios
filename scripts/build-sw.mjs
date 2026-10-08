import { readdirSync,readFileSync,writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const base=process.env.VITE_DEPLOY_BASE??'/';
const walk=(dir)=>readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(`${dir}/${e.name}`):[`${dir}/${e.name}`]);
const files=walk('dist').filter(f=>!f.endsWith('/sw.js'));
const version=createHash('sha256').update(files.map(f=>readFileSync(f)).join('')).digest('hex').slice(0,12);
/* Efeitos sonoros e folhas de efeito visual entram no cache quando a luta usa, não na instalação. */
const SOB_DEMANDA=['/assets/audio/sfx/','/assets/vfx/familias/'];
const assets=files.filter(f=>!SOB_DEMANDA.some(d=>f.includes(d))).map(f=>base+f.replace('dist/',''));
writeFileSync('dist/sw.js',`const BASE=${JSON.stringify(base)};const CACHE='nexus-${version}';const ASSETS=${JSON.stringify(assets)};
self.addEventListener('install',event=>{event.waitUntil((async()=>{const cache=await caches.open(CACHE);await Promise.all(ASSETS.map(async path=>{const response=await fetch(path,{credentials:'same-origin'});if(response.ok&&!response.redirected)await cache.put(path,response);}));await self.skipWaiting();})());});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('nexus-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();})());});
self.addEventListener('fetch',event=>{const url=new URL(event.request.url);if(event.request.method!=='GET'||url.origin!==self.location.origin)return;if(event.request.mode==='navigate'){event.respondWith(fetch(event.request).catch(async()=>await caches.match(BASE+'index.html')||Response.error()));return;}if(url.pathname.includes('/assets/audio/sfx/')||url.pathname.includes('/assets/vfx/familias/')){event.respondWith(caches.open(CACHE).then(async cache=>{const cached=await cache.match(event.request);if(cached)return cached;const response=await fetch(event.request);if(response.ok)await cache.put(event.request,response.clone());return response;}));return;}if(!ASSETS.includes(url.pathname))return;event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)));});
`);
