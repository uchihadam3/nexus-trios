import { createRequire } from 'node:module';
import { writeFileSync,mkdirSync } from 'node:fs';
import { createServer } from 'vite';
process.env.PLAYWRIGHT_BROWSERS_PATH??='/tmp/nexus-browsers';
const {chromium}=createRequire(import.meta.url)('@playwright/test');
const server=await createServer({server:{host:'127.0.0.1',port:5173,strictPort:true}});await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
mkdirSync('test-results',{recursive:true});
const errors=[],report={checks:[],errors};
try{
 const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{for(const key of ['run','settings']){const fixture=sessionStorage.getItem(`nexus-test-${key}`);if(fixture){localStorage.setItem(`nexus-v1-${key}`,fixture);sessionStorage.removeItem(`nexus-test-${key}`);}}});
 await page.goto('http://127.0.0.1:5173',{waitUntil:'networkidle'});
 const locked=await page.evaluate(async()=>(await import('/src/lib/audio.ts')).battleAudio.status);
 if(locked.state!=='locked')throw Error('AudioContext criado antes do gesto');
 await page.evaluate(async()=>{
  const {createBattle}=await import('/src/engine/battle.ts');const {generateCampaign,newDraft}=await import('/src/engine/campaign.ts');
  const team=['light','pikachu','wolverine'],seed=42,encounters=generateCampaign(seed);encounters[0].team=['gojo','goku','raven'];encounters[0].scale=1;
  sessionStorage.setItem('nexus-test-run',JSON.stringify({seed,team,encounters,index:0,stage:'battle',draft:{...newDraft(seed),team},battle:createBattle(team,encounters[0].team,seed),recorded:false}));
  sessionStorage.setItem('nexus-test-settings',JSON.stringify({volume:65,musicVolume:45,effectsVolume:70,effects:true,speed:1,numbers:true,reducedMotion:false,auto:false}));
 });
 await page.reload({waitUntil:'networkidle'});
 await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();await page.getByRole('button',{name:'Continuar',exact:true}).click();
 await page.waitForTimeout(8500);
 const audio=await page.evaluate(async()=>(await import('/src/lib/audio.ts')).battleAudio.status);
 if(audio.state!=='running'||!audio.musicRunning||audio.mode!=='stems'||audio.stemsPlaying!==4||audio.musicSeconds<140)throw Error('Música original em camadas não iniciou após gesto');report.audio=audio;
 await page.screenshot({path:'test-results/presentation-mobile.png',fullPage:true});
 await page.getByRole('button',{name:'Pausar',exact:true}).click();
 const pausedMusic=await page.evaluate(async()=>(await import('/src/lib/audio.ts')).battleAudio.status);if(pausedMusic.musicRunning)throw Error('Música não pausou');
 await page.getByRole('button',{name:'Continuar',exact:true}).click();await page.waitForTimeout(700);
 const resumedMusic=await page.evaluate(async()=>(await import('/src/lib/audio.ts')).battleAudio.status);if(!resumedMusic.musicRunning||resumedMusic.trackSeconds<=pausedMusic.trackSeconds)throw Error('A trilha não retomou do mesmo ponto após a pausa');
 await page.getByRole('button',{name:'Pausar',exact:true}).click();
 await page.getByRole('button',{name:'Ajustar música e efeitos'}).click();await page.getByLabel('Música',{exact:true}).fill('31');await page.getByLabel('Efeitos',{exact:true}).fill('57');
 await page.getByRole('button',{name:'Ajustar música e efeitos'}).click();
 for(const width of [320,360,390,1280]){
  await page.setViewportSize({width,height:width>600?1000:844});await page.waitForTimeout(100);
  const geometry=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,portraits:[...document.querySelectorAll('.fighter-portrait')].map(e=>e.getBoundingClientRect().width),fighters:document.querySelectorAll('[data-fighter]').length,meters:document.querySelectorAll('[role=meter]').length,offenders:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>({tag:e.tagName,cls:e.className?.baseVal??e.className,right:e.getBoundingClientRect().right}))}));
  await page.screenshot({path:`test-results/presentation-${width}.png`,fullPage:true});
  if(geometry.overflow||Math.min(...geometry.portraits)<75||geometry.fighters!==6||geometry.meters!==1)throw Error(`Layout inválido ${width}: ${JSON.stringify(geometry)}`);
 }
 await page.reload({waitUntil:'networkidle'});const settings=await page.evaluate(()=>JSON.parse(localStorage.getItem('nexus-v1-settings')));if(settings.musicVolume!==31||settings.effectsVolume!==57)throw Error('Mixer não persistiu');
 report.checks.push('autoplay bloqueado antes de gesto','música inicia após gesto, pausa e retoma sem reiniciar','mixer persiste','320/360/390/1280 sem overflow e seis retratos >=76 px','barra única');
 // Complete the same seeded battle via the actual UI at both presentation speeds.
 await page.clock.install();
 const results=[];
 for(const speed of [1,2]){
  await page.evaluate(async(speed)=>{const {createBattle}=await import('/src/engine/battle.ts');const run=JSON.parse(localStorage.getItem('nexus-v1-run'));run.battle=createBattle(run.team,run.encounters[0].team,run.seed);run.stage='battle';run.recorded=false;sessionStorage.setItem('nexus-test-run',JSON.stringify(run));const s=JSON.parse(localStorage.getItem('nexus-v1-settings'));s.speed=speed;s.volume=0;sessionStorage.setItem('nexus-test-settings',JSON.stringify(s));},speed);
  await page.reload({waitUntil:'networkidle'});await page.getByRole('button',{name:'Continuar jornada',exact:true}).click();await page.getByRole('button',{name:'Continuar',exact:true}).click();
  let elapsed=0,states=new Set();
  while(elapsed<900000){await page.clock.runFor(10000);elapsed+=10000;for(const c of await page.locator('.ability').evaluateAll(els=>els.map(e=>e.className)))states.add(c);if(await page.locator('.result-screen').count())break;}
  if(!await page.locator('.result-screen').count()){console.log(await page.evaluate(()=>({clock:document.querySelector('.battle-clock')?.textContent,paused:!!document.querySelector('.paused-banner'),run:JSON.parse(localStorage.getItem('nexus-v1-run')),now:performance.now()})));throw Error('Batalha não terminou');}
  const result=await page.evaluate(()=>JSON.parse(localStorage.getItem('nexus-v1-run')).battle);results.push(result);
  report[`battle${speed}x`]={elapsedSampleSeconds:elapsed/1000,time:result.time,winner:result.winner,reason:result.reason,states:[...states]};
 }
 if(JSON.stringify(results[0])!==JSON.stringify(results[1]))throw Error('Resultado mudou entre velocidades');
 report.checks.push('batalhas completas via interface em 1× e 2× com resultados idênticos');
 // Render the original score and each cue through the browser audio engine.
 report.synthesis=await page.evaluate(async()=>{
 const {scoreStep,sixteenth,SCORE}=await import('/src/audio/score.ts');const {synthCue}=await import('/src/audio/cues.ts');const {AUDIO_ASSETS}=await import('/src/lib/audio.ts');
  const length=SCORE.bars*16*sixteenth,ctx=new OfflineAudioContext(1,Math.ceil((length+2)*22050),22050);
  const out=ctx.createGain();out.gain.value=.4;out.connect(ctx.destination);for(let step=0;step<SCORE.bars*16;step++)scoreStep(ctx,out,step,step*sixteenth);
  const buffer=(await ctx.startRendering()).getChannelData(0);let peak=0,sum=0;for(const sample of buffer){peak=Math.max(peak,Math.abs(sample));sum+=sample*sample;}
 const sounds=['action','physical','energy','electric','fire','magic','dark','psychic','slash','prison','impact','block','shield','heal','regen','buff','debuff','interrupt','ready','prepare','shatter','ko','dominion','turn','victory','defeat'];
  const cues=[];for(const sound of sounds){const c=new OfflineAudioContext(1,44100,22050);synthCue(c,c.destination,sound,0);const data=(await c.startRendering()).getChannelData(0);let energy=0,peak=0;for(const v of data){energy+=v*v;peak=Math.max(peak,Math.abs(v));}cues.push({sound,rms:Math.sqrt(energy/data.length),peak});}
  const decoder=new OfflineAudioContext(1,128,22050),stems=[];for(const path of AUDIO_ASSETS.battleStems){const decoded=await decoder.decodeAudioData(await (await fetch(path)).arrayBuffer()),samples=decoded.getChannelData(0);let energy=0,peak=0;for(const sample of samples){energy+=sample*sample;peak=Math.max(peak,Math.abs(sample));}stems.push({path,seconds:decoded.duration,rms:Math.sqrt(energy/samples.length),peak});}
  return {loopSeconds:length,peak,rms:Math.sqrt(sum/buffer.length),cues,stems};
 });
 if(report.synthesis.rms<.01||report.synthesis.peak>=1||report.synthesis.cues.some(s=>s.rms<=0||s.peak>=1)||report.synthesis.stems.length!==4||report.synthesis.stems.some(s=>s.seconds<140||s.rms<=0||s.peak>=1))throw Error('Música em camadas ou efeitos silenciosos, curtos ou saturados');
 report.checks.push('tema original de 2m22 em quatro camadas e 26 efeitos renderizados sem clipping');
 if(errors.length)throw Error(errors.join('\n'));report.ok=true;
 writeFileSync('test-results/presentation-browser-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
}finally{await browser.close();await server.close();}
