import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
import { createServer } from 'vite';
process.env.PLAYWRIGHT_BROWSERS_PATH??='/tmp/nexus-browsers';
const {chromium}=createRequire(import.meta.url)('@playwright/test');
const server=await createServer({server:{host:'127.0.0.1',port:5174,strictPort:true}});await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:390,height:844}});await page.clock.install();
 await page.addInitScript(()=>{const fixture=sessionStorage.getItem('moment-fixture');if(fixture){localStorage.setItem('nexus-v1-run',fixture);sessionStorage.removeItem('moment-fixture');}});
 await page.goto('http://127.0.0.1:5174');
 await page.evaluate(async()=>{const {createBattle}=await import('/src/engine/battle.ts');const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');const team=['light','pikachu','wolverine'],seed=42,encounters=generateCampaign(seed);encounters[0].team=['gojo','goku','raven'];sessionStorage.setItem('moment-fixture',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle:createBattle(team,encounters[0].team,seed),recorded:false}));localStorage.setItem('nexus-v1-settings',JSON.stringify({volume:0,speed:1,effects:true,numbers:false,reducedMotion:false,auto:false}));});
 await page.reload();await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();await page.getByRole('button',{name:'Continuar',exact:true}).click();
 const wanted={cast:'.fighter.casting',electric:'.family-electric .trajectory',grand:'.grand-event .impact-shape',interruption:'.cast-broken',synergy:'.connection-synergy',block:'.connection-block',turn:'.dominion-turn',ko:'.incapacitated'};
 const captured=new Set();let maxNodes=0;
 for(let i=0;i<440;i++){
  await page.clock.runFor(500);
  if(await page.locator('.result-screen').count())break;
  maxNodes=Math.max(maxNodes,await page.locator('.arena *').count());
  for(const [name,selector] of Object.entries(wanted)){if(!captured.has(name)&&await page.locator(selector).count()){await page.screenshot({path:`test-results/moment-${name}.png`,fullPage:true});captured.add(name);}}
 }
 if(!captured.has('interruption')||!captured.has('grand')||!captured.has('synergy'))throw Error(`Momentos ausentes: ${[...captured]}`);
 writeFileSync('test-results/moments-report.json',JSON.stringify({captured:[...captured],maxArenaNodes:maxNodes},null,2));console.log({captured:[...captured],maxArenaNodes:maxNodes});
}finally{await browser.close();await server.close();}
