import { createServer } from 'vite';
import { chromium } from '@playwright/test';

process.env.VITE_DEPLOY_BASE='/';
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});
await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:390,height:844}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{
  for(const key of ['run','settings']){
   const fixture=sessionStorage.getItem(`nexus-test-${key}`);
   if(fixture){localStorage.setItem(`nexus-v1-${key}`,fixture);sessionStorage.removeItem(`nexus-test-${key}`);}
  }
 });
 await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
 await page.evaluate(async()=>{
  const {createBattle}=await import('/src/engine/battle.ts');
  const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
  const team=['goku','pikachu','captain'],seed=42,encounters=generateCampaign(seed,team);
  encounters[0]={...encounters[0],team:['vegeta','raven','hulk'],scale:1};
  sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle:createBattle(team,encounters[0].team,seed),recorded:false}));
  sessionStorage.setItem('nexus-test-settings',JSON.stringify({volume:0,musicVolume:0,effectsVolume:0,effects:true,speed:1,numbers:true,reducedMotion:false,auto:false}));
 });
 await page.reload({waitUntil:'networkidle'});
 await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
 await page.getByRole('button',{name:'Continuar',exact:true}).click();
 await page.getByRole('button',{name:'Pular guia',exact:true}).last().click();
 await page.clock.install();
 const read=()=>page.evaluate(()=>({
  hp:[...document.querySelectorAll('[data-fighter]')].map(f=>Number(f.querySelector('[role=progressbar]')?.getAttribute('aria-valuenow'))),
  impact:!!document.querySelector('.sprite-landed'),
  ko:[...document.querySelectorAll('[data-fighter]')].map(f=>f.classList.contains('incapacitated')),
  clock:document.querySelector('.battle-clock strong')?.textContent,
 }));
 let previous=await read(),changes=0;
 for(let i=0;i<650;i++){
  await page.clock.runFor(24);
  const now=await read();
  if(now.hp.some((hp,j)=>hp!==previous.hp[j])){
   if(!now.impact)throw Error(`HP changed without rendered impact on frame ${i}: ${JSON.stringify({previous,now})}`);
   changes++;
  }
  if(now.ko.some((ko,j)=>ko&&!previous.ko[j])&&!now.impact)throw Error(`KO appeared before impact on frame ${i}`);
  previous=now;
 }
 if(changes<5)throw Error(`Too few observed impacts: ${changes}`);
 await page.getByRole('button',{name:'Pausar',exact:true}).click();
 const before=await read();
 const checkpoint=await page.evaluate(()=>JSON.parse(localStorage.getItem('nexus-v1-run')).presentation);
 if(!checkpoint||checkpoint.battleTime<=0||checkpoint.visibleNextEvent<=1)throw Error('Missing presentation checkpoint');
 await page.reload({waitUntil:'networkidle'});
 await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
 const after=await read();
 if(JSON.stringify(before.hp)!==JSON.stringify(after.hp)||before.clock!==after.clock||JSON.stringify(before.ko)!==JSON.stringify(after.ko))throw Error(`Reload skipped the visible timeline: ${JSON.stringify({before,after})}`);
 if(errors.length)throw Error(errors.join('\n'));
 console.log(JSON.stringify({ok:true,causalHpChanges:changes,checkpointBattleTime:checkpoint.battleTime,visibleNextEvent:checkpoint.visibleNextEvent,reloadPreservedVisibleHp:true}));
}finally{await browser.close();await server.close();}
