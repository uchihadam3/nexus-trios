import { createServer } from 'vite';
import { chromium } from '@playwright/test';
import { mkdirSync,writeFileSync } from 'node:fs';

process.env.VITE_DEPLOY_BASE='/';
const seconds=Number(process.env.VFX_MOBILE_SECONDS??75);
const widths=(process.env.VFX_MOBILE_WIDTHS??'360,390,430').split(',').map(Number);
const effects=process.env.VFX_MOBILE_EFFECTS!=='off';
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const report={seconds,runs:[],lab:null};mkdirSync('test-results/vfx',{recursive:true});
try{
 for(const width of widths){
  const page=await browser.newPage({viewport:{width,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>{for(const key of ['run','settings']){const fixture=sessionStorage.getItem(`nexus-test-${key}`);if(fixture){localStorage.setItem(`nexus-v1-${key}`,fixture);sessionStorage.removeItem(`nexus-test-${key}`);}}});
  await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
  await page.evaluate(async effects=>{
   const {createBattle}=await import('/src/engine/battle.ts'),{generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
   const team=['goku','sakura','thor'],enemy=['pikachu','scarletwitch','captain'],seed=451,encounters=generateCampaign(seed,team);
   encounters[0]={...encounters[0],team:enemy,power:0,scale:1};
   const battle=createBattle(team,enemy,seed);
   sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle,recorded:false}));
   sessionStorage.setItem('nexus-test-settings',JSON.stringify({volume:65,musicVolume:30,effectsVolume:55,effects,speed:2,numbers:true,reducedMotion:false,auto:false,explanations:'normal'}));
  },effects);
  await page.reload({waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();await page.getByRole('button',{name:'Continuar',exact:true}).click();
  const tutorial=page.getByRole('button',{name:'Pular guia',exact:true}).last();if(await tutorial.isVisible())await tutorial.click();
  await page.locator('.battle-screen').waitFor();
  const metrics=await page.evaluate(async duration=>{
   const frames=[],seen=new Set(),kinds=new Set(),longTasks=[];let previous=performance.now(),maxNodes=0,impactFrames=[];
   const observer=new PerformanceObserver(list=>{for(const entry of list.getEntries())longTasks.push(entry.duration)});observer.observe({entryTypes:['longtask']});
   let priorBeat='',priorImpact=false;let r=requestAnimationFrame(function tick(now){const delta=now-previous;frames.push(delta);previous=now;
    const screen=document.querySelector('.battle-screen'),fx=document.querySelector('.battle-effects');
    const id=screen?.getAttribute('data-beat-id')??'',impact=!!fx?.querySelector('.sprite-impact');
    if(impact&&(!priorImpact||id!==priorBeat))impactFrames.push(delta);
    priorBeat=id;priorImpact=impact;
    if(fx){const items=fx.querySelectorAll('.effect-sprite,.fx-beam');maxNodes=Math.max(maxNodes,items.length);for(const el of items){const src=getComputedStyle(el).backgroundImage;const family=src.match(/\/vfx\/([^/]+)\.webp/)?.[1];if(family)seen.add(family)}}
    const kind=screen?.getAttribute('data-beat-kind');if(kind)kinds.add(kind);
    r=requestAnimationFrame(tick);
   });
   await new Promise(resolve=>setTimeout(resolve,duration*1000));cancelAnimationFrame(r);observer.disconnect();
   frames.sort((a,b)=>a-b);const pct=p=>frames[Math.min(frames.length-1,Math.floor(frames.length*p))];
   return {fps:frames.length/duration,p95Ms:pct(.95),p99Ms:pct(.99),over33:frames.filter(x=>x>33).length,longTasks:longTasks.length,maxEffectNodes:maxNodes,firstImpactFrames:impactFrames,families:[...seen],kinds:[...kinds]};
  },seconds);
  const state=await page.evaluate(async()=>({battleTime:JSON.parse(localStorage.getItem('nexus-v1-run')).battle.time,overflow:document.documentElement.scrollWidth>innerWidth,audio:(await import('/src/lib/audio.ts')).battleAudio.status}));
  await page.screenshot({path:`test-results/vfx/mobile-${width}-${seconds}s-${effects?'on':'off'}.png`,fullPage:true});
  if(errors.length||state.overflow||metrics.maxEffectNodes>3||state.audio.loadedCues<18)throw Error(`${width}px ${JSON.stringify({errors,state,metrics})}`);
  report.runs.push({width,...metrics,...state,errors});console.log(`${width}px: ${metrics.fps.toFixed(1)}fps p95=${metrics.p95Ms.toFixed(1)}ms, ${metrics.families.join(', ')}, time=${state.battleTime}`);
  await page.close();
 }
 const lab=await browser.newPage({viewport:{width:390,height:844}}),errors=[];lab.on('pageerror',e=>errors.push(e.message));
 await lab.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
 await lab.getByRole('button',{name:'Galeria de efeitos'}).click();
 await lab.locator('.vfx-family-card').first().waitFor();
 const count=await lab.locator('.vfx-family-card').count();
 await lab.getByRole('button',{name:'Trajeto',exact:true}).click();
 await lab.getByRole('button',{name:'Ouvir SFX'}).click();
 await lab.screenshot({path:'test-results/vfx/lab-390.png',fullPage:true});
 report.lab={count,errors,overflow:await lab.evaluate(()=>document.documentElement.scrollWidth>innerWidth)};
 if(count!==13||errors.length||report.lab.overflow)throw Error(`VFX Lab: ${JSON.stringify(report.lab)}`);
 writeFileSync(`test-results/vfx/mobile-report-${seconds}s-${widths.join('-')}-${effects?'on':'off'}.json`,JSON.stringify(report,null,2));
 console.log('VFX Lab: 13 famílias, SFX e preview sem erro');
 await lab.close();
}finally{await browser.close();await server.close();}
