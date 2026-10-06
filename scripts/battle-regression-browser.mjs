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
  await page.evaluate(async ({speed})=>{
   const {createBattle}=await import('/src/engine/battle.ts');
   const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
   const team=['goku','pikachu','captain'],enemy=['vegeta','raven','hulk'],seed=451;
   const encounters=generateCampaign(seed,team);
   encounters[0]={...encounters[0],team:enemy,power:0,scale:1};
   const battle=createBattle(team,enemy,seed);
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
  const baseline=await page.evaluate(()=>({time:JSON.parse(localStorage.getItem('nexus-v1-run')).battle.time}));
  let lastTime=baseline.time,mechanicalFinish=null,resultTime=null;
  const basicDurations=[],basicConfigured=[];let activeId=null,activeKind=null,activeSince=0;
  // Playwright fires the app's interval once per runFor call; use the same
  // 40 ms frame cadence as the real UI instead of skipping intermediate paints.
  const total=full?650:25,increment=full?.04:1;
  for(let frame=1;frame<=Math.floor(total/increment);frame++){
   const elapsed=frame*increment;
   await page.clock.runFor(increment*1000);
   if(full&&width===390&&speed===1&&elapsed<=80){
    const visual=await page.evaluate(()=>{const el=document.querySelector('.battle-screen');return {id:el?.getAttribute('data-beat-id')??null,kind:el?.getAttribute('data-beat-kind')??null,duration:Number(el?.getAttribute('data-beat-duration')),now:performance.now()};});
    if(visual.id!==activeId){
     if(activeId&&activeKind==='basic')basicDurations.push((visual.now-activeSince)/1000);
     if(visual.id&&visual.kind==='basic')basicConfigured.push(visual.duration);
     activeId=visual.id;activeKind=visual.kind;activeSince=visual.now;
    }
   }
   if(full&&frame%25!==0)continue;
   const state=await page.evaluate(()=>{
    const run=JSON.parse(localStorage.getItem('nexus-v1-run'));
    const clock=document.querySelector('.battle-clock strong')?.textContent??null;
    return {time:run.battle.time,finished:run.battle.finished,stage:run.stage,clock};
   });
   if(state.time+1e-6<lastTime)throw Error(`Relógio retrocedeu ${width}px/${speed}x: ${lastTime} → ${state.time}`);
   lastTime=state.time;
   if(state.finished&&mechanicalFinish===null)mechanicalFinish=elapsed;
   const sample=Math.round(elapsed);
   if(Math.abs(elapsed-sample)<.02&&[10,20,80].includes(sample))await page.screenshot({path:`test-results/battle-regression/battle-${width}-${speed}x-${full?'full':'sample'}-${sample}s.png`,fullPage:true});
   if(full&&state.stage==='result'){resultTime=elapsed;break;}
  }
  const final=await page.evaluate(()=>JSON.parse(localStorage.getItem('nexus-v1-run')).battle);
  if(full&&(resultTime===null||mechanicalFinish===null||final.time>120||!final.winner))throw Error(`Batalha inteira ${width}px/${speed}x: apresentação=${resultTime}s, motor=${final.time}s`);
  if(full&&width===390&&speed===1&&(basicDurations.length<3||basicDurations.some(duration=>duration<1.6)||basicConfigured.some(duration=>duration!==2)))throw Error(`Básicos comprimidos em 1×: ${JSON.stringify({basicDurations,basicConfigured})}`);
  const entry={width,speed,geometry,mechanicalFinish,resultTime,mechanicalTime:final.time,clockMonotonic:true,basicDurations:width===390&&speed===1?basicDurations:undefined,basicConfigured:width===390&&speed===1?basicConfigured:undefined,final:full?final:null};
  report.runs.push(entry);
  await page.close();
  return final;
 }
 await run(430,1,false);
 const one=await run(390,1,true),two=await run(390,2,true);
 const narrow=await run(360,1,true),desktop=await run(1280,1,true);
 if(JSON.stringify(one)!==JSON.stringify(two)||JSON.stringify(one)!==JSON.stringify(narrow)||JSON.stringify(one)!==JSON.stringify(desktop))throw Error('Viewport ou velocidade alterou o resultado mecânico');
 const oneTime=report.runs.find(run=>run.width===390&&run.speed===1).resultTime;
 const twoTime=report.runs.find(run=>run.width===390&&run.speed===2).resultTime;
 if(twoTime>=oneTime*.7)throw Error(`2× não acelerou a apresentação de forma constante: ${oneTime}s / ${twoTime}s`);
 if(report.errors.length)throw Error(report.errors.join('\n'));
 report.checks.push('batalhas inteiras em 360, 390 e 1280 px; layout 430 px sem overflow','básicos em 1× mantêm cerca de 2 s mesmo com eventos densos','relógio mecânico monotônico e limitado a 120 s','2× acelera a apresentação; resultado mecânico idêntico','nenhum erro de página');
 report.runs.forEach(run=>delete run.final);
 report.ok=true;
 writeFileSync('test-results/battle-regression/report.json',JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));
}finally{await browser.close();await server.close();}
