import { createServer } from 'vite';
import { chromium } from '@playwright/test';
import { readFileSync,mkdirSync,writeFileSync } from 'node:fs';
import { join } from 'node:path';

process.env.VITE_DEPLOY_BASE='/';
const mode=process.env.VFX_BENCHMARK_MODE??'before';
const seconds=Number(process.env.VFX_BENCHMARK_SECONDS??25);
const mobileCpuThrottling=Number(process.env.VFX_BENCHMARK_CPU??4);
const widths=[1280,360,390,430];
const vfx=JSON.parse(readFileSync('public/assets/vfx/manifest.json','utf8'));
const sfx=JSON.parse(readFileSync('public/assets/audio/sfx/manifest.json','utf8'));
const vfxBytes=Object.values(vfx.families).reduce((n,f)=>n+f.bytes,0);
const vfxDecoded=Object.values(vfx.families).reduce((n,f)=>n+f.frameSize[0]*f.frameSize[1]*f.columns*f.rows*4,0);
const sfxBytes=Object.values(sfx.sounds).reduce((n,s)=>n+readFileSync(join('public/assets/audio/sfx',s.file)).byteLength,0);
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});
await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const report={mode,seconds,browser:'Chromium headless',mobileCpuThrottling,fixture:{team:['goku','pikachu','sakura'],enemy:['thor','scarletwitch','captain'],seed:451,chargedSkills:true},assets:{vfxBytes,vfxDecodedBytes:vfxDecoded,sfxBytes,atlasCount:Object.keys(vfx.families).length},runs:[]};
try{
 for(const width of widths)for(const effects of [false,true]){
  const page=await browser.newPage({viewport:{width,height:844},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  if(width<600&&mobileCpuThrottling>1){const client=await page.context().newCDPSession(page);await client.send('Emulation.setCPUThrottlingRate',{rate:mobileCpuThrottling});}
  await page.addInitScript(()=>{for(const key of ['run','settings']){const fixture=sessionStorage.getItem(`nexus-test-${key}`);if(fixture){localStorage.setItem(`nexus-v1-${key}`,fixture);sessionStorage.removeItem(`nexus-test-${key}`);}}});
  await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
  await page.evaluate(async ({effects})=>{
   const {createBattle}=await import('/src/engine/battle.ts');
   const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
   const team=['goku','pikachu','sakura'],enemy=['thor','scarletwitch','captain'],seed=451;
   const encounters=generateCampaign(seed,team);
   encounters[0]={...encounters[0],team,power:0,scale:1};
   encounters[0].team=enemy;
   const battle=createBattle(team,enemy,seed);
   for(const f of battle.fighters)f.skills[2].charge=100;
   sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle,recorded:false}));
   sessionStorage.setItem('nexus-test-settings',JSON.stringify({volume:0,musicVolume:0,effectsVolume:0,effects,speed:1,numbers:true,reducedMotion:false,auto:false,explanations:'normal'}));
  },{effects});
  await page.reload({waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
  await page.getByRole('button',{name:'Continuar',exact:true}).click();
  const tutorial=page.getByRole('button',{name:'Pular guia',exact:true}).last();if(await tutorial.isVisible())await tutorial.click();
  await page.locator('.battle-screen').waitFor();
  const metrics=await page.evaluate(async duration=>{
   const frames=[],longTasks=[];let nodes=0,filters=0;
   const started=performance.now();let previous=started,raf=0;
   const observer=new PerformanceObserver(list=>{for(const e of list.getEntries())longTasks.push(e.duration)});
   try{observer.observe({entryTypes:['longtask']})}catch{/* unsupported */}
   const tick=now=>{frames.push(now-previous);previous=now;raf=requestAnimationFrame(tick)};
   raf=requestAnimationFrame(tick);
   const sample=window.setInterval(()=>{
    const fx=document.querySelector('.battle-effects');if(!fx)return;
    const all=[...fx.querySelectorAll('*')];nodes=Math.max(nodes,all.length);
    filters=Math.max(filters,all.filter(el=>getComputedStyle(el).filter!=='none').length);
   },250);
   await new Promise(resolve=>setTimeout(resolve,duration*1000));
   cancelAnimationFrame(raf);clearInterval(sample);observer.disconnect();
   const sorted=frames.slice(1).sort((a,b)=>a-b),pct=p=>sorted[Math.min(sorted.length-1,Math.floor(sorted.length*p))]??0;
   return {seconds:(performance.now()-started)/1000,frames:sorted.length,fps:sorted.length/((performance.now()-started)/1000),medianMs:pct(.5),p95Ms:pct(.95),p99Ms:pct(.99),over25:sorted.filter(x=>x>25).length,over33:sorted.filter(x=>x>33).length,longTasks:longTasks.length,longTaskMs:longTasks.reduce((a,b)=>a+b,0),maxVfxNodes:nodes,maxFilteredVfxNodes:filters};
  },seconds);
  const state=await page.evaluate(()=>{const b=JSON.parse(localStorage.getItem('nexus-v1-run')).battle;return {battleTime:b.time,events:b.nextEvent-1,finished:b.finished,overflow:document.documentElement.scrollWidth>innerWidth}});
  report.runs.push({width,effects,...metrics,...state,errors});
  console.log(`${mode} ${width}px ${effects?'on':'off'} ${metrics.fps.toFixed(1)} fps, p95 ${metrics.p95Ms.toFixed(1)} ms, >33 ${metrics.over33}, VFX DOM ${metrics.maxVfxNodes}`);
  await page.close();
 }
 mkdirSync('reports',{recursive:true});
 writeFileSync(`reports/vfx-benchmark-${mode}.json`,JSON.stringify(report,null,2));
}finally{await browser.close();await server.close();}
