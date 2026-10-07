import { chromium } from '@playwright/test';
import { mkdirSync,writeFileSync } from 'node:fs';

const phase=process.argv[2]??'after';
const root=`test-results/visual-${phase}`;
mkdirSync(root,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
const errors=[];
page.on('pageerror',e=>errors.push(e.message));
const base='http://127.0.0.1:5173/';
const shot=async name=>{await page.waitForTimeout(650);await page.screenshot({path:`${root}/${name}.png`,fullPage:true});};
try{
  await page.goto(base,{waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Montar meu trio'}).waitFor();
  await shot('home');
  await page.locator('.hub-links').getByRole('button',{name:/Personagens/}).click();
  await shot('characters');
  await page.getByRole('button',{name:'Voltar ao início'}).click();
  await page.locator('.hub-links').getByRole('button',{name:/Como jogar/}).click();
  await shot('help');
  await page.getByRole('button',{name:'Voltar ao início'}).click();
  await page.locator('.hub-links').getByRole('button',{name:/Configurações/}).click();
  await shot('settings');
  await page.getByRole('button',{name:'Voltar ao início'}).click();
  await page.getByRole('button',{name:'Montar meu trio'}).click();
  await page.locator('.candidate-card').first().waitFor();
  await shot('draft');
  await page.evaluate(async()=>{
    const {createBattle,simulate}=await import('/src/engine/battle.ts');
    const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
    const {summarizeBattle}=await import('/src/engine/run-summary.ts');
    const team=['goku','pikachu','captain'],enemy=['vegeta','raven','hulk'],seed=451;
    const encounters=generateCampaign(seed,team);
    encounters[0]={...encounters[0],team:enemy,power:0,scale:1};
    const draft={...newDraft(seed),team};
    const profile={journeys:7,victories:1,best:6,wins:22,champion:['goku','pikachu','captain']};
    localStorage.setItem('nexus-v1-profile',JSON.stringify(profile));
    localStorage.setItem('nexus-v1-settings',JSON.stringify({volume:0,musicVolume:0,effectsVolume:0,effects:true,speed:1,numbers:true,reducedMotion:false,auto:false,explanations:'normal'}));
    localStorage.setItem('nexus-battle-guide-v1','1');
    sessionStorage.setItem('visual-battle',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft,battle:createBattle(team,enemy,seed),recorded:false}));
    const final=simulate(team,enemy,seed,.25);
    sessionStorage.setItem('visual-result',JSON.stringify({seed,team,encounters,index:0,stage:'result',draft,battle:final,recorded:true,summaries:[summarizeBattle(0,final)]}));
    const finalEncounters=encounters.map((x,i)=>({...x,team:i===9?enemy:x.team,scale:.25}));
    sessionStorage.setItem('visual-conclusion',JSON.stringify({seed,team,encounters:finalEncounters,index:9,stage:'result',draft,battle:final,recorded:true,summaries:Array.from({length:10},(_,i)=>summarizeBattle(i,final))}));
  });
  async function fixture(key){
    await page.evaluate(key=>sessionStorage.setItem('visual-pending',sessionStorage.getItem(`visual-${key}`)),key);
    await page.addInitScript(()=>{const pending=sessionStorage.getItem('visual-pending');if(pending){localStorage.setItem('nexus-v1-run',pending);sessionStorage.removeItem('visual-pending');}});
    await page.reload({waitUntil:'networkidle'});
    await page.getByRole('button',{name:/Continuar jornada|Ver resultado/}).first().click();
  }
  await fixture('battle');
  await page.getByRole('button',{name:'Continuar',exact:true}).click();
  await page.locator('[data-fighter]').first().waitFor();
  await shot('battle');
  await fixture('result');
  await page.locator('.result-screen').waitFor();
  await shot('result');
  await fixture('conclusion');
  await page.locator('.result-screen').waitFor();
  await shot('conclusion');
  writeFileSync(`${root}/manifest.json`,JSON.stringify({phase,errors,files:['home','draft','characters','help','settings','battle','result','conclusion']},null,2));
  if(errors.length)throw Error(errors.join('\n'));
  console.log(`${root}: 8 screenshots`);
}finally{await browser.close();}
