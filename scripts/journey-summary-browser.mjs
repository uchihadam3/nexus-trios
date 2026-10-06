import { createServer } from 'vite';
import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';

process.env.VITE_DEPLOY_BASE='/';
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});
await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
mkdirSync('test-results/journey',{recursive:true});
try{
 const page=await browser.newPage({viewport:{width:390,height:844}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{
  const fixture=sessionStorage.getItem('nexus-test-run');
  if(fixture){localStorage.setItem('nexus-v1-run',fixture);sessionStorage.removeItem('nexus-test-run');}
 });
 await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
 await page.evaluate(async()=>{
  const {simulate}=await import('/src/engine/battle.ts');
  const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
  const {summarizeBattle}=await import('/src/engine/run-summary.ts');
  const team=['goku','pikachu','captain'],seed=42,encounters=generateCampaign(seed,team);
  const summaries=encounters.map((encounter,index)=>{
   const battle=simulate(team,encounter.team,seed+index*7919,encounter.scale);
   battle.winner='player';
   return summarizeBattle(index,battle,[{source:'player-0',target:'player-1',count:index+1,charge:10*(index+1)}]);
  });
  const battle=simulate(team,encounters[9].team,seed+9*7919,encounters[9].scale);battle.winner='player';
  sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:9,stage:'result',draft:{...newDraft(seed),team},battle,recorded:true,summaries}));
 });
 await page.reload({waitUntil:'networkidle'});
 await page.getByRole('button',{name:'Ver conclusão',exact:true}).click();
 for(const width of [360,390,430,1280]){
  await page.setViewportSize({width,height:width>600?900:844});
  if(await page.locator('.journey-battles li').count()!==10)throw Error(`Missing ten battle summaries at ${width}px`);
  if(!await page.getByText('10 de 10 vitórias').count())throw Error('Champion score missing');
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error(`Overflow at ${width}px`);
  await page.screenshot({path:`test-results/journey/champion-${width}.png`,fullPage:true});
 }
 const profile={journeys:3,victories:1,best:10,wins:12};
 await page.evaluate(async profile=>{
  const {simulate}=await import('/src/engine/battle.ts');
  const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
  const {summarizeBattle}=await import('/src/engine/run-summary.ts');
  const seed=14,team=['light','batman','deadpool'],encounters=generateCampaign(seed,team),battle=simulate(team,encounters[3].team,seed+3*7919,encounters[3].scale);
  battle.winner='player';
  sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:3,stage:'result',draft:{...newDraft(seed),team},battle,recorded:true,summaries:[summarizeBattle(3,battle)]}));
  localStorage.setItem('nexus-v1-profile',JSON.stringify(profile));
 },profile);
 await page.reload({waitUntil:'networkidle'});
 await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
 await page.getByRole('button',{name:'Desistir da campanha'}).click();
 if(!await page.getByRole('heading',{name:'Desistir desta campanha?'}).count())throw Error('Missing confirmation');
 await page.getByRole('button',{name:'Continuar campanha'}).click();
 if(!await page.getByRole('button',{name:'Desistir da campanha'}).count())throw Error('Cancel did not preserve run');
 await page.getByRole('button',{name:'Desistir da campanha'}).click();
 await page.getByRole('button',{name:'Desistir e começar outra'}).click();
 const state=await page.evaluate(()=>({run:JSON.parse(localStorage.getItem('nexus-v1-run')),profile:JSON.parse(localStorage.getItem('nexus-v1-profile'))}));
 if(state.run.stage!=='draft'||state.run.summaries.length!==0||JSON.stringify(state.profile)!==JSON.stringify(profile))throw Error('Abandon altered records or kept the former run');
 if(errors.length)throw Error(errors.join('\n'));
 console.log(JSON.stringify({ok:true,summaryRows:10,widths:[360,390,430,1280],abandonConfirmed:true,recordsPreserved:true}));
}finally{await browser.close();await server.close();}
