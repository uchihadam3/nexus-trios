import type { Settings } from './storage';
import { PRESENTATION as P } from '../presentation/config';
import { scoreStep,sixteenth,SCORE } from '../audio/score';
import { FAMILIAS_DE_APOIO,PRIORIDADE,SOM_DA_FAMILIA,SONS,type Manifesto,type Sound } from '../audio/cues';
import type { Cue } from '../presentation/director';
import type { Battle } from '../engine/types';
import { profileFor } from '../presentation/vfxProfiles';

/*
 * O som da batalha (adendo, parte 6).
 *
 * Efeitos: a biblioteca em MP3 (4 versões por som), decodificada antes de
 * precisar — no impacto só se lê do cache. Cada ação toca o som da família do
 * efeito visual dela: a saída (disparo, feixe, lâmina) no instante em que o
 * golpe sai, e o impacto no instante do contato.
 *
 * Mixagem: no máximo 5 sons ao mesmo tempo; quando passa disso, o de menor
 * prioridade sai (grand > nocaute/interrupção > habilidade > básico > apoio >
 * interface). A música abaixa nos momentos grandes. Um compressor no fim
 * segura os picos. Cada som vem do lado de quem age (estéreo leve, nunca
 * extremo), e varia de versão, de tom e de volume — de forma determinística,
 * pelo número do evento, para o replay soar igual.
 *
 * Música: três camadas do mesmo trecho de ~3 min (base, pulso, tema), em laço.
 * A base toca sempre; o pulso e o tema sobem com a intensidade da luta. Cada
 * luta começa numa seção diferente.
 */
const SFX='/assets/audio/sfx/';
export const AUDIO_ASSETS={battleLoop:null as string|null,battleStems:['/assets/audio/musica-base.ogg','/assets/audio/musica-pulso.ogg','/assets/audio/musica-tema.ogg'] as const};
/*
 * A música de batalha (tools/audio/generate_music_v3.py): Intro, Encontro,
 * Choque, Ponte, Clímax e Virada, ~2 min 26 s. Toda luta nova começa na Intro;
 * se a luta passar do fim, a música volta ao Encontro (o laço), nunca à Intro.
 */
/** O navegador decodifica Ogg Vorbis? (o Safari do iPhone, muitas vezes, não). */
export function tocaOgg(){try{return typeof Audio!=='undefined'&&new Audio().canPlayType('audio/ogg; codecs="vorbis"')!=='';}catch{return false;}}
export const LACO_DA_MUSICA=13.913;
/** Posição na música depois de `t` segundos tocando, a partir de `inicio`, respeitando o laço. */
export function posicaoNoLaco(inicio:number,t:number,duracao:number){
  const p=inicio+t;if(p<duracao)return p;
  const volta=duracao-LACO_DA_MUSICA;return LACO_DA_MUSICA+((p-LACO_DA_MUSICA)%volta);
}
const MAX_VOZES=5;
export interface MusicMood {heat:number;pressure:number;time:number}
class BattleAudio {
  private ctx:AudioContext|null=null;
  private master:GainNode|null=null;
  private music:GainNode|null=null;
  private effects:GainNode|null=null;
  private bus:GainNode|null=null;
  private stemBuffers:(AudioBuffer|null)[]=[];
  private stemLoading:Promise<void>|null=null;
  private stemSources:AudioBufferSourceNode[]=[];
  private stemGains:GainNode[]=[];
  private startToken=0;
  private lastMoodChange=0;
  private musicStartedAt=0;
  private musicOffset=0;
  private luta:string|undefined;
  private mood:MusicMood={heat:.25,pressure:0,time:0};
  private timer:ReturnType<typeof setInterval>|null=null;
  private step=0;
  private next=0;
  private running=false;
  private active=false;
  private settings:Pick<Settings,'volume'|'musicVolume'|'effectsVolume'>&{speed?:number}={volume:P.audio.master,musicVolume:P.audio.music,effectsVolume:P.audio.effects};
  private manifest:Manifesto|null=null;
  private manifestLoading:Promise<Manifesto|null>|null=null;
  private buffers=new Map<Sound,AudioBuffer>();
  private loading=new Map<Sound,Promise<AudioBuffer|null>>();
  private recent=new Map<Sound,number>();
  private vozes:{source:AudioBufferSourceNode;prioridade:number;fim:number}[]=[];
  /* Posição horizontal de cada lutador (0–100), para o estéreo. */
  private posicoes:Record<string,number>={};
  async unlock(){
    try{
      if(!this.ctx){
        // iPhone: sem isto, a chave do silencioso cala o áudio do jogo (Safari 17+ entende como mídia, igual vídeo)
        try{const sessao=(navigator as Navigator&{audioSession?:{type:string}}).audioSession;if(sessao)sessao.type='playback';}catch{/* navegador sem audioSession */}
        this.ctx=new AudioContext();const ctx=this.ctx;
        this.master=ctx.createGain();this.music=ctx.createGain();this.effects=ctx.createGain();
        // compressor no fim: segura picos de vários sons juntos sem esmagar a dinâmica
        const limiter=ctx.createDynamicsCompressor();limiter.threshold.value=-10;limiter.knee.value=6;limiter.ratio.value=12;limiter.attack.value=.003;limiter.release.value=.25;
        // equalizador da música para alto-falante de celular: quase 70% da energia dela fica abaixo
        // de 300 Hz, que o celular não toca; tira um pouco do grave e traz o corpo para o médio
        const grave=ctx.createBiquadFilter();grave.type='lowshelf';grave.frequency.value=140;grave.gain.value=-5;
        const medio=ctx.createBiquadFilter();medio.type='peaking';medio.frequency.value=1800;medio.Q.value=.7;medio.gain.value=5;
        const brilho=ctx.createBiquadFilter();brilho.type='highshelf';brilho.frequency.value=5000;brilho.gain.value=2;
        this.music.connect(grave);grave.connect(medio);medio.connect(brilho);brilho.connect(this.master);this.effects.connect(this.master);this.master.connect(limiter);limiter.connect(ctx.destination);
        this.apply();
      }
      if(this.ctx.state==='suspended')await this.ctx.resume();
      if(this.active)this.start();
      void this.preloadCues();
      return this.ctx.state==='running';
    }catch{return false;}
  }
  configure(settings:Settings){this.settings=settings;this.apply();}
  private apply(){if(!this.ctx)return;const t=this.ctx.currentTime;this.master?.gain.setTargetAtTime(this.settings.volume/100,t,.06);this.music?.gain.setTargetAtTime(this.musicLevel(),t,.08);this.effects?.gain.setTargetAtTime(this.settings.effectsVolume/100,t,.04);}
  /* Música de fundo: logo abaixo dos golpes (medido no alcance do alto-falante do celular), presente sem atrapalhar. */
  private musicLevel(){return this.settings.musicVolume/100;}
  /** Onde cada lutador está na tela (x em %), para o som vir do lado certo. */
  setPositions(anchors:Record<string,{x:number;y:number}>){this.posicoes=Object.fromEntries(Object.entries(anchors).filter(([k])=>/^(player|enemy)-\d$/.test(k)).map(([k,a])=>[k,a.x]));}
  private pan(uid?:string){if(!uid)return 0;const x=this.posicoes[uid]??(17+(Number(uid.split('-')[1])||0)*33);return Math.max(-.45,Math.min(.45,(x-50)/50*.5));}
  /** Liga/desliga a música da luta. `luta` identifica a luta: numa luta nova a música começa numa seção sorteada; na mesma luta (depois de uma pausa) continua de onde parou. */
  setBattle(active:boolean,luta?:string){
    this.active=active;
    if(active){if(luta!==undefined&&luta!==this.luta){this.luta=luta;this.musicOffset=0;}this.start();void this.preloadCues();}
    else this.stop();
  }
  setMood(mood:MusicMood){
    this.mood={heat:Math.max(0,Math.min(1,mood.heat)),pressure:Math.max(-1,Math.min(1,mood.pressure)),time:Math.max(0,Math.min(1,mood.time))};
    if(!this.ctx||!this.stemGains.length)return;
    const at=this.ctx.currentTime;if(at-this.lastMoodChange<.7)return;this.lastMoodChange=at;
    const levels=this.stemLevels();
    this.stemGains.forEach((gain,index)=>gain.gain.setTargetAtTime(levels[index],at,1.2));
  }
  /*
   * A música já cresce sozinha (cada fase é mais cheia que a anterior); por cima,
   * as camadas sobem com a luta: a base sempre inteira, o pulso (pratos,
   * percussão, guitarras) e o tema (melodia, coro) ganham força quando a luta
   * esquenta ou se arrasta.
   */
  private stemLevels(){
    const {heat,time}=this.mood;
    return [.95,Math.min(1,.5+heat*.5+time*.15),Math.min(1,.55+heat*.45+time*.2)];
  }
  private start(){
    if(this.running||!this.ctx||this.ctx.state!=='running'||!this.music)return;
    this.running=true;const token=++this.startToken;this.bus=this.ctx.createGain();this.bus.gain.setValueAtTime(0,this.ctx.currentTime);this.bus.gain.linearRampToValueAtTime(1,this.ctx.currentTime+2.4);this.bus.connect(this.music);
    void this.playStems(token);
  }
  private loadStems(){
    const ctx=this.ctx;if(!ctx)return Promise.resolve();
    if(!this.stemLoading){
      this.stemBuffers=AUDIO_ASSETS.battleStems.map(()=>null);
      // a base primeiro: a música começa assim que ela chega; as outras camadas entram depois
      this.stemLoading=AUDIO_ASSETS.battleStems.reduce<Promise<void>>((anterior,path,index)=>anterior.then(async()=>{
        // OGG onde o navegador toca OGG; senão (iPhone/Safari) o MP3. Se o OGG não decodificar, tenta o MP3.
        const mp3=path.replace(/\.ogg$/,'.mp3'),ordem=tocaOgg()?[path,mp3]:[mp3];
        for(const arquivo of ordem){
          try{const r=await fetch(arquivo);if(!r.ok)continue;this.stemBuffers[index]=await ctx.decodeAudioData(await r.arrayBuffer());this.attachStem(index);return;}catch{/* tenta o próximo formato */}
        }
      }),Promise.resolve());
    }
    return this.stemLoading;
  }
  private attachStem(index:number){
    const ctx=this.ctx,bus=this.bus,buffer=this.stemBuffers[index];
    if(!ctx||!bus||!buffer||!this.running||this.stemSources[index])return;
    if(index===0)this.musicStartedAt=ctx.currentTime+.05;
    const base=this.stemBuffers[0];if(!base)return;
    const source=ctx.createBufferSource(),gain=ctx.createGain();source.buffer=buffer;source.loop=true;source.loopStart=Math.min(LACO_DA_MUSICA,buffer.duration-1);source.loopEnd=buffer.duration;
    const posicao=posicaoNoLaco(this.musicOffset,Math.max(0,ctx.currentTime+.05-this.musicStartedAt),buffer.duration);
    gain.gain.setValueAtTime(0,ctx.currentTime);gain.gain.linearRampToValueAtTime(this.stemLevels()[index],ctx.currentTime+(index===0?.05:2));
    source.connect(gain);gain.connect(bus);source.onended=()=>{source.disconnect();gain.disconnect();};
    source.start(ctx.currentTime+.05,posicao);this.stemSources[index]=source;this.stemGains[index]=gain;
  }
  private async playStems(token:number){
    await this.loadStems();
    if(token!==this.startToken||!this.running)return;
    this.stemBuffers.forEach((_,i)=>this.attachStem(i));
    if(!this.stemBuffers[0])this.startScore();
  }
  private startScore(){if(!this.ctx||!this.running||this.timer)return;this.next=this.ctx.currentTime+.035;this.schedule();this.timer=setInterval(()=>this.schedule(),40);}
  private schedule(){
    if(!this.ctx||!this.bus||!this.running)return;
    if(this.next<this.ctx.currentTime-.2)this.next=this.ctx.currentTime+.02;
    while(this.next<this.ctx.currentTime+.14){scoreStep(this.ctx,this.bus,this.step,this.next);this.next+=sixteenth;this.step=(this.step+1)%(SCORE.bars*16);}
  }
  private stop(){
    // guarda onde a música estava, para continuar dali depois de uma pausa
    if(this.running)this.musicOffset=this.posicaoDaMusica();
    this.running=false;this.startToken++;if(this.timer){clearInterval(this.timer);this.timer=null;}
    if(this.ctx)for(const source of this.stemSources){try{source?.stop(this.ctx.currentTime+.4);}catch{ /* já parado */ }}
    this.stemSources=[];this.stemGains=[];
    if(this.ctx&&this.bus){const bus=this.bus;bus.gain.cancelScheduledValues(this.ctx.currentTime);bus.gain.setTargetAtTime(0,this.ctx.currentTime,.12);setTimeout(()=>bus.disconnect(),700);this.bus=null;}
  }
  private async loadManifest(){
    if(this.manifest)return this.manifest;
    this.manifestLoading??=fetch(`${SFX}manifest.json`).then(r=>r.ok?r.json() as Promise<Manifesto>:null).then(m=>this.manifest=m).catch(()=>null);
    return this.manifestLoading;
  }
  private async loadCue(som:Sound):Promise<AudioBuffer|null>{
    const cached=this.buffers.get(som);if(cached)return cached;
    const pending=this.loading.get(som);if(pending)return pending;
    const ctx=this.ctx;if(!ctx)return null;
    const request=this.loadManifest().then(m=>{const info=m?.sons[som];if(!info)throw new Error(som);return fetch(SFX+info.arquivo);})
      .then(r=>{if(!r.ok)throw new Error(som);return r.arrayBuffer();}).then(data=>ctx.decodeAudioData(data))
      .then(buffer=>{this.buffers.set(som,buffer);return buffer;}).catch(()=>null).finally(()=>this.loading.delete(som));
    this.loading.set(som,request);return request;
  }
  /** Os sons da luta que vai começar (as famílias dos seis lutadores), antes do primeiro golpe. */
  async precarregarLuta(personagens:string[]){
    await this.loadManifest();
    const sons=new Set<Sound>();
    for(const id of personagens)for(const i of [undefined,0,1,2]){
      const p=profileFor(id,i);const s=p?SOM_DA_FAMILIA[p.family]:undefined;
      if(s){sons.add(s.impacto);if(s.saida)sons.add(s.saida);if(s.preparo)sons.add(s.preparo);if(s.antes)sons.add(s.antes);}
    }
    await Promise.all([...sons].map(s=>this.loadCue(s)));
  }
  private async preloadCues(){
    // os mais comuns primeiro; o resto em seguida. No impacto, só se lê do cache.
    const comuns:Sound[]=['ui-clique','ui-confirma','ui-abrir','ui-fechar','soco-leve','soco-pesado','corte','disparo','impacto-energia','preparo','pronto','nocaute','interrupcao','grand-carga','grand-impacto'];
    await Promise.all(comuns.map(s=>this.loadCue(s)));
    await Promise.all(SONS.filter(s=>!comuns.includes(s)).map(s=>this.loadCue(s)));
  }
  /**
   * Toca um som. `chave` escolhe a versão e a variação (o mesmo evento soa
   * igual no replay); `atraso` em segundos de apresentação (já dividido pela
   * velocidade da luta aqui).
   */
  sound(som:Sound,prioridade:number=PRIORIDADE.basico,pan=0,chave=0,atraso=0){
    const ctx=this.ctx;if(!ctx||ctx.state!=='running'||!this.effects||this.settings.volume===0||this.settings.effectsVolume===0)return;
    const buffer=this.buffers.get(som),info=this.manifest?.sons[som];
    // som que ainda não chegou: pede agora, para a próxima vez
    if(!buffer){if(info)void this.loadCue(som);return;}
    if(!info)return;
    const quando=ctx.currentTime+.006+Math.max(0,atraso)/Math.max(.25,this.settings.speed??1);
    // o mesmo som duas vezes em 70 ms vira um só
    if(quando-(this.recent.get(som)??-100)<.07)return;
    this.vozes=this.vozes.filter(v=>v.fim>ctx.currentTime);
    if(this.vozes.length>=MAX_VOZES){
      const menor=this.vozes.reduce((a,b)=>a.prioridade<=b.prioridade?a:b);
      if(menor.prioridade>=prioridade)return;
      try{menor.source.stop();}catch{/* */}this.vozes=this.vozes.filter(v=>v!==menor);
    }
    this.recent.set(som,quando);
    const n=info.versoes.length,v=Math.abs(chave)%n,offset=info.versoes[v],dur=info.duracoes[v];
    const source=ctx.createBufferSource(),volume=ctx.createGain(),panner=ctx.createStereoPanner();
    source.buffer=buffer;
    // variação leve e determinística: tom ±1,5%, volume ±1,5 dB
    source.playbackRate.value=1+(((chave*7)%5)-2)*.0075;
    const ganhoDaPrioridade=prioridade>=5?1:prioridade>=4?.92:prioridade>=3?.84:prioridade>=2?.74:prioridade>=1.5?.62:.5;
    volume.gain.value=ganhoDaPrioridade*10**((((chave*3)%3)-1)*1.5/20);
    panner.pan.value=Math.max(-.45,Math.min(.45,pan));
    source.connect(volume);volume.connect(panner);panner.connect(this.effects);
    const voz={source,prioridade,fim:quando+dur/source.playbackRate.value};this.vozes.push(voz);
    source.onended=()=>{this.vozes=this.vozes.filter(x=>x!==voz);source.disconnect();volume.disconnect();panner.disconnect();};
    source.start(quando,offset,dur);
    // a música abaixa nos momentos grandes e volta devagar
    if(prioridade>=4&&this.music){const g=this.music.gain,alvo=this.musicLevel();g.cancelScheduledValues(quando);g.setTargetAtTime(alvo*P.audio.duck,quando,.05);g.setTargetAtTime(alvo,quando+Math.min(1.2,dur),.35);}
  }
  /** Ouve um som (ou uma sequência: preparo, saída, impacto) na galeria. */
  async preview(sons:Sound|Sound[]){
    const lista=Array.isArray(sons)?sons:[sons];
    if(!await this.unlock())return;
    await this.loadManifest();await Promise.all(lista.map(s=>this.loadCue(s)));
    let atraso=0;
    for(const [i,s] of lista.entries()){this.sound(s,PRIORIDADE.habilidade,0,i,atraso);atraso+=Math.min(.7,this.manifest?.sons[s]?.duracoes[0]??.4)*.8;}
  }
  /** Som de uma deixa do diretor: a saída do golpe e o impacto, pela família do efeito. */
  cue(cue:Cue,battle?:Battle){
    const {event,grand,phase}=cue,fonte=battle?.fighters.find(f=>f.uid===event.source);
    const perfil=fonte&&['basic','skill','cast'].includes(event.kind)?profileFor(fonte.characterId,event.skill):undefined;
    const som=perfil?SOM_DA_FAMILIA[perfil.family]:undefined;
    const panFonte=this.pan(event.source),panAlvo=this.pan(event.target??event.source),chave=event.id;
    const apoio=perfil?FAMILIAS_DE_APOIO.has(perfil.family):false;
    if(phase==='start'){
      if(event.kind==='cast'){this.sound(grand?'grand-carga':som?.preparo??'preparo',grand?PRIORIDADE.grand:PRIORIDADE.habilidade,panFonte,chave);return;}
      // a saída toca quando o golpe deixa quem age (a viagem começa a ~58% do tempo até o impacto)
      const ate=P.impactAt*(event.kind==='skill'?P.skillSeconds:P.normalSeconds),sai=ate*.55,prio=event.kind==='skill'?PRIORIDADE.habilidade:PRIORIDADE.basico;
      const voa=!!(som?.saida&&perfil?.travel);
      // o "antes" (carga, giro, marreta subindo) termina no instante em que o golpe sai ou chega
      if(som?.antes){const fim=voa?sai:ate,d=this.manifest?.sons[som.antes]?.duracoes[0]??.8;this.sound(som.antes,prio,panFonte,chave+2,Math.max(0,fim-d));}
      if(voa)this.sound(som!.saida!,prio,panFonte,chave,sai);
      return;
    }
    if(event.kind==='cast'||event.kind==='turn')return;
    if(grand){this.sound('grand-impacto',PRIORIDADE.grand,panAlvo,chave);if(som)this.sound(som.impacto,PRIORIDADE.importante,panAlvo,chave+1);return;}
    if(som)this.sound(som.impacto,apoio?PRIORIDADE.apoio:event.kind==='skill'?PRIORIDADE.habilidade:PRIORIDADE.basico,panAlvo,chave);
  }
  private posicaoDaMusica(){const base=this.stemBuffers[0];return this.running&&this.ctx&&this.musicStartedAt&&base&&this.stemSources[0]?posicaoNoLaco(this.musicOffset,Math.max(0,this.ctx.currentTime-this.musicStartedAt),base.duration):this.musicOffset;}
  get status(){const base=this.stemBuffers[0];const trackSeconds=this.posicaoDaMusica();return {state:this.ctx?.state??'locked',musicRunning:this.running,mode:this.stemSources.length?'stems':'synth',stemsPlaying:this.stemSources.filter(Boolean).length,musicSeconds:base?.duration??0,trackSeconds,activeCues:this.vozes.length,loadedCues:this.buffers.size,step:this.step};}
}
export const battleAudio=new BattleAudio();
