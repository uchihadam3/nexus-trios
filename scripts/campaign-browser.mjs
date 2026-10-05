import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
import { createServer } from 'vite';
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});
await server.listen();
process.env.PLAYWRIGHT_BROWSERS_PATH??='/tmp/nexus-browsers';
const {chromium}=createRequire(import.meta.url)('@playwright/test');
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:390,height:844}});
await page.addInitScript(()=>{
 for(const key of ['run','settings']){const fixture=sessionStorage.getItem(`nexus-test-${key}`);if(fixture){localStorage.setItem(`nexus-v1-${key}`,fixture);sessionStorage.removeItem(`nexus-test-${key}`);}}
});
await page.clock.install();
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
await page.evaluate(async()=>{
  const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
  const team=['wolverine','wonderwoman','sasuke'],seed=35;
  const draft={...newDraft(seed),team,candidates:[]};
  sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters:generateCampaign(seed),index:0,stage:'draft',draft,battle:null,recorded:false}));
  sessionStorage.setItem('nexus-test-settings',JSON.stringify({volume:0,effects:true,speed:2,numbers:false,reducedMotion:true,auto:true}));
});
await page.reload({waitUntil:'networkidle'});
await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
await page.getByRole('button',{name:'Entrar na arena'}).click();
for(let i=0;i<45;i++){
  await page.clock.runFor(65000);
  if(await page.getByRole('heading',{name:'A conexão perfeita.'}).count())break;
}
if(!await page.getByRole('heading',{name:'A conexão perfeita.'}).count())throw Error('Campanha de 10 batalhas não concluída');
await page.screenshot({path:'test-results/champion-mobile.png',fullPage:true});
const profile=await page.evaluate(()=>JSON.parse(localStorage.getItem('nexus-v1-profile')));
if(profile.victories!==1||profile.best!==10||profile.wins!==10)throw Error('Contagem da campanha incorreta');
await page.getByRole('button',{name:'Montar outro trio'}).click();
if(await page.getByRole('button',{name:'Escolher',exact:true}).count()!==3)throw Error('Nova jornada não iniciou');
// Exercise defeat and restart with a genuine losing simulation snapshot.
await page.evaluate(async()=>{
 const {simulate}=await import('/src/engine/battle.ts');
 const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
 const team=['light','batman','deadpool'];let battle;
 const encounters=generateCampaign(14);
 for(let seed=1;seed<100;seed++){battle=simulate(team,encounters[0].team,seed,1.2);if(battle.winner==='enemy')break;}
 if(battle.winner!=='enemy')throw Error('Fixture de derrota indisponível');
 sessionStorage.setItem('nexus-test-run',JSON.stringify({seed:14,team,encounters,index:0,stage:'battle',draft:{...newDraft(14),team,candidates:[]},battle,recorded:false}));
});
await page.reload();
await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();
await page.getByRole('button',{name:'Continuar',exact:true}).click();
await page.clock.runFor(2000);
if(!await page.getByRole('heading',{name:'Toda conexão ensina.'}).count())throw Error('Derrota não encerrou a jornada');
await page.screenshot({path:'test-results/defeat-mobile.png',fullPage:true});
await page.getByRole('button',{name:'Montar outro trio'}).click();
if(await page.getByRole('button',{name:'Escolher',exact:true}).count()!==3)throw Error('Não reiniciou após derrota');
writeFileSync('test-results/campaign-browser-report.json',JSON.stringify({ok:true,errors,profile,checks:['ten real automatic battles','champion conclusion','accurate profile counters','restart after championship','defeat ends journey','restart after defeat']},null,2));
console.log(JSON.stringify({ok:true,errors,profile}));await browser.close();await server.close();
