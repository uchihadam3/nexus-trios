import { chromium } from '@playwright/test';
import { mkdirSync,writeFileSync } from 'node:fs';

const root='test-results/combat-proof';mkdirSync(root,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const scenarios={basic:{source:'player-0',target:'enemy-0',kind:'attack',number:'−190'},energy:{source:'player-1',target:'enemy-0',kind:'attack',number:'−155'},heal:{source:'player-0',target:'player-2',kind:'heal',number:'+170'},shield:{source:'player-1',target:'player-2',kind:'shield',number:'+240'},buff:{source:'player-2',target:'player-0',kind:'buff',status:'Acelerado'},debuff:{source:'player-1',target:'enemy-0',kind:'debuff',status:'Exposto'},interrupt:{source:'player-1',target:'enemy-0',kind:'interrupt',status:'Interrompido'},aoe:{source:'player-1',target:'enemy-0',kind:'attack',number:'−180'},synergy:{source:'player-2',target:'player-0',kind:'support'},ko:{source:'player-0',target:'enemy-0',kind:'attack',number:'−80'}};
const report=[];
try{
  for(const [name,expected] of Object.entries(scenarios)){
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    const load=async phase=>{
      await page.goto(`http://127.0.0.1:5173/visual-probe.html?scenario=${name}&phase=${phase}`,{waitUntil:'networkidle'});
      await page.locator('[data-fighter]').first().waitFor();
      await page.waitForTimeout(phase==='windup'?330:120);
    };
    await load('windup');
    const source=page.locator(`[data-fighter="${expected.source}"]`),target=page.locator(`[data-fighter="${expected.target}"]`),link=page.locator(`[data-link="${expected.source}:${expected.target}:${expected.kind}"]`);
    if(!await source.evaluate(el=>el.classList.contains('link-source')))throw Error(`${name}: fonte apagada`);
    if(!await target.evaluate(el=>el.classList.contains('link-target')))throw Error(`${name}: alvo sem marcação`);
    if(await link.count()!==1)throw Error(`${name}: conexão ausente`);
    if(name==='aoe'&&await page.locator('[data-link$=":attack"]').count()!==3)throw Error('Área não conectou os três alvos');
    if(name==='interrupt'&&!await target.locator('.cast-label').count())throw Error('Preparo não apareceu');
    await page.screenshot({path:`${root}/${name}-travel.png`,fullPage:true});
    await load('impact');
    if(expected.number&&!await page.locator(`[data-fighter="${expected.target}"] .combat-feedback`).getByText(expected.number,{exact:name!=='shield'}).count())throw Error(`${name}: número ausente`);
    if(expected.status&&!await page.locator(`[data-fighter="${expected.target}"]`).getByText(expected.status,{exact:false}).count())throw Error(`${name}: consequência ausente`);
    if(name==='ko'&&!await page.locator('[data-fighter="enemy-0"]').getByText('FORA DA LUTA').count())throw Error('KO ausente');
    if(name==='synergy'&&!await page.locator('[data-fighter="player-0"] .ability-assisted').count())throw Error('Carga recebida não pulsa');
    if(name==='aoe'&&await page.locator('.enemy-team .taking-hit').count()!==3)throw Error('Área não atingiu três');
    if(errors.length)throw Error(`${name}: ${errors.join('; ')}`);
    await page.screenshot({path:`${root}/${name}-impact.png`,fullPage:true});
    report.push({name,source:expected.source,target:expected.target,kind:expected.kind,ok:true});
    await page.close();
  }
  const page=await browser.newPage({viewport:{width:390,height:844}});
  await page.goto('http://127.0.0.1:5173/visual-probe.html?scenario=basic&phase=windup',{waitUntil:'networkidle'});
  for(const [step,delay] of [['01-source',10],['02-target',80],['03-travel',350]]){await page.waitForTimeout(delay);await page.screenshot({path:`${root}/${step}.png`,fullPage:true});}
  await page.goto('http://127.0.0.1:5173/visual-probe.html?scenario=basic&phase=impact',{waitUntil:'networkidle'});
  for(const [step,delay] of [['04-impact',20],['05-number',110],['06-consequence',220]]){await page.waitForTimeout(delay);await page.screenshot({path:`${root}/${step}.png`,fullPage:true});}
  await page.close();
  writeFileSync(`${root}/report.json`,JSON.stringify({ok:true,report},null,2));
  console.log(JSON.stringify({ok:true,scenarios:report.length}));
}finally{await browser.close();}
