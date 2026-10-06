import { chromium } from '@playwright/test';
import { mkdirSync,writeFileSync } from 'node:fs';

const base=process.env.NEXUS_URL??'http://127.0.0.1:5173/';
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
mkdirSync('test-results/ux',{recursive:true});
const results=[];
try{
  for(const width of [360,390,430]){
    const context=await browser.newContext({viewport:{width,height:844}});
    const page=await context.newPage(),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    const check=async screen=>{
      const geometry=await page.evaluate(()=>({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
      if(geometry.scrollWidth>geometry.viewport)throw Error(`${width}px ${screen}: overflow ${JSON.stringify(geometry)}`);
      if(errors.length)throw Error(`${width}px ${screen}: ${errors.join('; ')}`);
      results.push({width,screen,...geometry});
      await page.screenshot({path:`test-results/ux/${screen}-${width}.png`,fullPage:true});
    };
    await page.goto(base,{waitUntil:'networkidle'});
    await page.getByRole('button',{name:'Montar meu trio'}).waitFor();
    await check('home');
    await page.locator('.hub-links').getByRole('button',{name:/Como jogar/}).click();
    await page.getByText('Status positivos').waitFor();
    await check('help');
    await page.getByRole('button',{name:'Voltar ao início'}).click();
    await page.locator('.hub-links').getByRole('button',{name:/Personagens/}).click();
    await page.getByRole('textbox',{name:'Buscar personagem'}).fill('Light');
    await page.getByRole('button',{name:/Light Yagami/}).click();
    await page.locator('.character-modal').getByRole('heading',{name:'Light Yagami'}).waitFor();
    const modal=await page.locator('.character-modal').boundingBox();
    if(!modal||modal.x<0||modal.x+modal.width>width+1)throw Error(`${width}px: ficha cortada ${JSON.stringify(modal)}`);
    if(await page.locator('.character-modal').getByText('Death Note: compatível').count())throw Error('Spoiler na ficha');
    await check('light');
    await page.getByRole('button',{name:'Fechar detalhes'}).click();
    await page.getByRole('button',{name:'Voltar ao início'}).click();
    await page.getByRole('button',{name:'Montar meu trio'}).click();
    await page.getByRole('button',{name:/Escolher/}).first().waitFor();
    await check('draft');
    await page.evaluate(async()=>{
      const {createBattle}=await import('/src/engine/battle.ts');
      const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
      const team=['goku','pikachu','captain'],enemy=['vegeta','raven','hulk'],seed=451,encounters=generateCampaign(seed,team);
      encounters[0]={...encounters[0],team:enemy,power:0,scale:1};
      sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle:createBattle(team,enemy,seed),recorded:false}));
    });
    await page.addInitScript(()=>{const fixture=sessionStorage.getItem('nexus-test-run');if(fixture){localStorage.setItem('nexus-v1-run',fixture);sessionStorage.removeItem('nexus-test-run');}});
    await page.reload({waitUntil:'networkidle'});
    await page.getByRole('button',{name:'Continuar jornada'}).click();
    await page.getByRole('button',{name:'Continuar',exact:true}).click();
    await page.getByRole('button',{name:'Pular guia'}).last().click();
    await page.locator('[data-fighter]').first().waitFor();
    await check('battle');
    await context.close();
  }
  writeFileSync('test-results/ux/report.json',JSON.stringify({ok:true,results},null,2));
  console.log(JSON.stringify({ok:true,results}));
}finally{await browser.close();}
