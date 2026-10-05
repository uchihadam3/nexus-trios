import { createServer } from 'vite';
import { chromium } from '@playwright/test';
import { mkdirSync,writeFileSync } from 'node:fs';

process.env.VITE_DEPLOY_BASE='/';
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});
await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
mkdirSync('test-results/battle-regression',{recursive:true});
const report={checks:[],runs:[],errors:[]};
try{
 async function run(width,speed,full){
  const page=await browser.newPage({viewport:{width,height:844}});
  page.on('pageerror',error=>report.errors.push(`${width}/${speed}x: ${error.message}`));
  await page.addInitScript(()=>{
   for(const key of ['run','settings']){
    const fixture=sessionStorage.getItem(`nexus-test-${key}`);
    if(fixture){localStorage.setItem(`nexus-v1-${key}`,fixture);sessionStorage.removeItem(`nexus-test-${key}`);}
   }
  });
  await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
  await page.evaluate(async ({speed,full})=>{
   const {createBattle}=await import('/src/engine/battle.ts');
   const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
   const team=['goku','pikachu','captain'],enemy=['vegeta','raven','hulk'],seed=451;
   const encounters=generateCampaign(seed,team);
   encounters[0]={...encounters[0],team:enemy,power:0,scale:1};
   const battle=createBattle(team,enemy,seed);
   if(full)for(const fighter of battle.fighters){fighter.maxHp=1e8;fighter.hp=fighter.side==='enemy'?8e7:1e8;}
   sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle,recorded:false}));
   sessionStorage.setItem('nexus-test-settings',JSON.stringify({volume:0,musicVolume:0,effectsVolume:0,effects:true,speed,numbers:true,reducedMotion:false,auto:false,explanations:'normal'}));
  },{speed,full});
  await page.reload({waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
  await page.getByRole('button',{name:'Continuar',exact:true}).click();
  await page.getByRole('button',{name:'Entendi',exact:true}).click();
  await page.getByRole('button',{name:`Velocidade ${speed} vezes`}).waitFor();
  const geometry=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,fighters:document.querySelectorAll('[data-fighter]').length,portraits:[...document.querySelectorAll('.fighter-portrait')].map(x=>Math.round(x.getBoundingClientRect().width))}));
  if(geometry.overflow||geometry.fighters!==6||Math.min(...geometry.portraits)<70)throw Error(`Layout ${width}px: ${JSON.stringify(geometry)}`);
  await page.clock.install();
  const baseline=await page.evaluate(()=>({time:JSON.parse(localStorage.getItem('nexus-v1-run')).battle.time,performance:performance.now()}));
  let lastTime=baseline.time,mechanicalFinish=null;
  const total=full?125:22;
  for(let elapsed=1;elapsed<=total;elapsed++){
   await page.clock.runFor(1000);
   const state=await page.evaluate(()=>{
    const run=JSON.parse(localStorage.getItem('nexus-v1-run'));
    const clock=document.querySelector('.battle-clock strong')?.textContent??null;
    return {time:run.battle.time,finished:run.battle.finished,clock,performance:performance.now()};
   });
   if(state.time+1e-6<lastTime)throw Error(`Relógio retrocedeu ${width}px/${speed}x: ${lastTime} → ${state.time}`);
   if(state.time-baseline.time>(state.performance-baseline.performance)/1000+1.2)throw Error(`Simulação acelerou em ${width}px/${speed}x: ${state.time}s em ${elapsed}s reais simulados`);
   lastTime=state.time;
   if(state.finished&&mechanicalFinish===null)mechanicalFinish=baseline.time+(state.performance-baseline.performance)/1000;
   if(elapsed===10||elapsed===20||elapsed===80&&full)await page.screenshot({path:`test-results/battle-regression/battle-${width}-${speed}x-${full?'timeout':'normal'}-${elapsed}s.png`,fullPage:true});
  }
  const final=await page.evaluate(()=>JSON.parse(localStorage.getItem('nexus-v1-run')).battle);
  if(full&&(final.time!==120||mechanicalFinish===null||Math.abs(mechanicalFinish-120)>2))throw Error(`Duração ${width}px/${speed}x: fim em ${mechanicalFinish}s, motor=${final.time}`);
  const entry={width,speed,geometry,mechanicalFinish,mechanicalTime:final.time,clockMonotonic:true,final:full?final:null};
  report.runs.push(entry);
  await page.close();
  return final;
 }
 for(const width of [360,390,430])await run(width,1,false);
 const one=await run(390,1,true),two=await run(390,2,true);
 if(JSON.stringify(one)!==JSON.stringify(two))throw Error('A velocidade visual alterou o resultado mecânico');
 if(report.errors.length)throw Error(report.errors.join('\n'));
 report.checks.push('360/390/430 px sem overflow, seis retratos visíveis','relógio monotônico em todas as capturas','1× e 2× encerram 120 s mecânicos em ~120 s reais simulados','resultado mecânico idêntico entre 1× e 2×','nenhum erro de página');
 report.runs.forEach(run=>delete run.final);
 report.ok=true;
 writeFileSync('test-results/battle-regression/report.json',JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));
}finally{await browser.close();await server.close();}
