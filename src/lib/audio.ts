import type { Settings } from './storage';
import { PRESENTATION as P } from '../presentation/config';
import { scoreStep,sixteenth,SCORE } from '../audio/score';
import { CUE_ASSETS,synthCue,type Sound } from '../audio/cues';
import type { Cue } from '../presentation/director';

// A local loop file can replace synthesis without changing the battle interface.
// Replace this list with final licensed stems later; the Web Audio mixer remains the same.
export const AUDIO_ASSETS={battleLoop:null as string|null,battleStems:['/assets/audio/harmony.ogg','/assets/audio/rhythm.ogg','/assets/audio/pulse.ogg','/assets/audio/lead.ogg'] as const};
export interface MusicMood {heat:number;pressure:number;time:number}
class BattleAudio {
  private ctx:AudioContext|null=null;
  private master:GainNode|null=null;
  private music:GainNode|null=null;
  private effects:GainNode|null=null;
  private bus:GainNode|null=null;
  private loop:HTMLAudioElement|null=null;
  private stemBuffers:AudioBuffer[]|null=null;
  private stemLoading:Promise<AudioBuffer[]>|null=null;
  private stemSources:AudioBufferSourceNode[]=[];
  private stemGains:GainNode[]=[];
  private startToken=0;
  private lastMoodChange=0;
  private musicStartedAt=0;
  private musicOffset=0;
  private mood:MusicMood={heat:.25,pressure:0,time:0};
  private timer:ReturnType<typeof setInterval>|null=null;
  private step=0;
  private next=0;
  private running=false;
  private active=false;
  private settings:Pick<Settings,'volume'|'musicVolume'|'effectsVolume'>={volume:P.audio.master,musicVolume:P.audio.music,effectsVolume:P.audio.effects};
  private lastCue=-100;
  private lastPriority=0;
  private recent=new Map<Sound,number>();
  private cueBuffers=new Map<string,AudioBuffer>();
  private cueLoading=new Map<string,Promise<AudioBuffer|null>>();
  private cueVariants=new Map<string,number>();
  private queued=0;
  async unlock(){
    try{
      if(!this.ctx){
        this.ctx=new AudioContext();const ctx=this.ctx;
        this.master=ctx.createGain();this.music=ctx.createGain();this.effects=ctx.createGain();
        const compressor=ctx.createDynamicsCompressor();compressor.threshold.value=-12;compressor.knee.value=12;compressor.ratio.value=4;compressor.attack.value=.012;compressor.release.value=.18;
        this.music.connect(this.master);this.effects.connect(this.master);this.master.connect(compressor);compressor.connect(ctx.destination);
        if(AUDIO_ASSETS.battleLoop){this.loop=new Audio(AUDIO_ASSETS.battleLoop);this.loop.loop=true;ctx.createMediaElementSource(this.loop).connect(this.music);}
        this.apply();
      }
      if(this.ctx.state==='suspended')await this.ctx.resume();
      if(this.active)this.start();
      if(this.active)void this.preloadCues();
      return this.ctx.state==='running';
    }catch{return false;}
  }
  configure(settings:Settings){this.settings=settings;this.apply();}
  private apply(){if(!this.ctx)return;const t=this.ctx.currentTime;this.master?.gain.setTargetAtTime(this.settings.volume/100,t,.06);this.music?.gain.setTargetAtTime(this.settings.musicVolume/100*.75,t,.08);this.effects?.gain.setTargetAtTime(this.settings.effectsVolume/100,t,.04);}
  setBattle(active:boolean){this.active=active;if(active){this.start();void this.preloadCues();}else this.stop();}
  setMood(mood:MusicMood){
    this.mood={heat:Math.max(0,Math.min(1,mood.heat)),pressure:Math.max(-1,Math.min(1,mood.pressure)),time:Math.max(0,Math.min(1,mood.time))};
    if(!this.ctx||!this.stemGains.length)return;
    const at=this.ctx.currentTime;if(at-this.lastMoodChange<.7)return;this.lastMoodChange=at;
    const levels=this.stemLevels();
    this.stemGains.forEach((gain,index)=>gain.gain.setTargetAtTime(levels[index],at,.65));
  }
  private stemLevels(){
    const {heat,time}=this.mood;
    return [.77,.17+heat*.2,.26+heat*.24,.04+heat*.27+Math.max(0,time-.55)*.08];
  }
  private start(){
    if(this.running||!this.ctx||this.ctx.state!=='running'||!this.music)return;
    this.running=true;const token=++this.startToken;this.bus=this.ctx.createGain();this.bus.gain.setValueAtTime(0,this.ctx.currentTime);this.bus.gain.linearRampToValueAtTime(1,this.ctx.currentTime+1.15);this.bus.connect(this.music);
    if(this.loop){void this.loop.play().catch(()=>undefined);return;}
    if(AUDIO_ASSETS.battleStems.length){void this.playStems(token);return;}
    this.startScore();
  }
  private async loadStems(){
    if(this.stemBuffers)return this.stemBuffers;
    if(!this.stemLoading){
      const ctx=this.ctx;if(!ctx)throw new Error('Áudio bloqueado pelo navegador');
      this.stemLoading=Promise.all(AUDIO_ASSETS.battleStems.map(async path=>{const response=await fetch(path);if(!response.ok)throw new Error(`Não foi possível carregar ${path}`);return ctx.decodeAudioData(await response.arrayBuffer());})).then(buffers=>this.stemBuffers=buffers).finally(()=>{this.stemLoading=null;});
    }
    return this.stemLoading;
  }
  private async playStems(token:number){
    try{
      const buffers=await this.loadStems(),ctx=this.ctx,bus=this.bus;
      if(!ctx||!bus||!this.running||token!==this.startToken)return;
      const levels=this.stemLevels(),startAt=ctx.currentTime+.09;this.musicStartedAt=startAt;
      this.stemSources=[];this.stemGains=[];
      buffers.forEach((buffer,index)=>{
        const source=ctx.createBufferSource(),gain=ctx.createGain();source.buffer=buffer;source.loop=true;gain.gain.setValueAtTime(levels[index],startAt);source.connect(gain);gain.connect(bus);source.onended=()=>{source.disconnect();gain.disconnect();};source.start(startAt,this.musicOffset%buffer.duration);this.stemSources.push(source);this.stemGains.push(gain);
      });
    }catch{
      if(token!==this.startToken||!this.running)return;
      this.startScore();
    }
  }
  private startScore(){if(!this.ctx||!this.running||this.timer)return;this.next=this.ctx.currentTime+.035;this.schedule();this.timer=setInterval(()=>this.schedule(),40);}
  private async loadCue(file:string):Promise<AudioBuffer|null>{
    const cached=this.cueBuffers.get(file);if(cached)return cached;
    const pending=this.cueLoading.get(file);if(pending)return pending;
    const ctx=this.ctx;if(!ctx)return null;
    const request=fetch(`/assets/audio/sfx/${file}.wav`).then(r=>{if(!r.ok)throw new Error(`SFX ${file} indisponível`);return r.arrayBuffer();}).then(data=>ctx.decodeAudioData(data)).then(buffer=>{this.cueBuffers.set(file,buffer);return buffer;}).catch(()=>null).finally(()=>this.cueLoading.delete(file));
    this.cueLoading.set(file,request);return request;
  }
  private async preloadCues(){
    const common=['physical-light','physical-heavy','energy-charge','energy-shot','energy-impact','electric-charge','electric-hit','magic-cast','magic-impact','shield-hit','grand-charge','grand-impact'];
    await Promise.all(common.map(file=>this.loadCue(file)));
  }
  private schedule(){
    if(!this.ctx||!this.bus||!this.running)return;
    if(this.next<this.ctx.currentTime-.2)this.next=this.ctx.currentTime+.02;
    while(this.next<this.ctx.currentTime+.14){scoreStep(this.ctx,this.bus,this.step,this.next);this.next+=sixteenth;this.step=(this.step+1)%(SCORE.bars*16);}
  }
  private stop(){
    this.running=false;this.startToken++;if(this.timer){clearInterval(this.timer);this.timer=null;}this.loop?.pause();
    if(this.ctx&&this.stemSources.length&&this.stemBuffers?.[0])this.musicOffset=(this.musicOffset+Math.max(0,this.ctx.currentTime-this.musicStartedAt))%this.stemBuffers[0].duration;
    if(this.ctx)for(const source of this.stemSources){try{source.stop(this.ctx.currentTime+.22);}catch{ /* Already stopped by the previous battle. */ }}
    this.stemSources=[];this.stemGains=[];
    if(this.ctx&&this.bus){const bus=this.bus;bus.gain.cancelScheduledValues(this.ctx.currentTime);bus.gain.setTargetAtTime(0,this.ctx.currentTime,.055);setTimeout(()=>bus.disconnect(),400);this.bus=null;}
  }
  sound(sound:Sound,priority=1,pan=0){
    const ctx=this.ctx;if(!ctx||ctx.state!=='running'||!this.effects||this.settings.volume===0||this.settings.effectsVolume===0)return;
    const now=ctx.currentTime,gap=priority>=3?P.audio.majorGap:P.audio.minorGap;
    if(this.queued>=P.audio.maxActiveCues||now-(this.recent.get(sound)??-100)<(priority>=3?.22:.6))return;
    if(now-this.lastCue<gap&&priority<=this.lastPriority)return;
    this.lastCue=now;this.lastPriority=priority;this.recent.set(sound,now);this.queued++;
    const panner=ctx.createStereoPanner();panner.pan.value=Math.max(-.6,Math.min(.6,pan));panner.connect(this.effects);
    const asset=CUE_ASSETS[sound],index=this.cueVariants.get(asset.file)??0;this.cueVariants.set(asset.file,(index+1)%4);
    void this.playAsset(asset.file,asset.duration,index,panner,sound,priority>=3?.88:priority===2?.68:.46,now+.006);
    setTimeout(()=>{panner.disconnect();this.queued=Math.max(0,this.queued-1);},2200);
    if(priority>=3&&this.music){const gain=this.music.gain;gain.cancelScheduledValues(now);gain.setTargetAtTime(this.settings.musicVolume/100*.75*P.audio.duck,now,.06);gain.setTargetAtTime(this.settings.musicVolume/100*.75,now+.55,.25);}
  }
  cue(cue:Cue){
    const {event,family,grand,phase}=cue,pan=((Number(event.source.split('-')[1])||0)-1)*.38;
    if(phase==='start'){
      if(event.kind==='cast'){const charge:Sound=grand?'grand-charge':family==='electric'?'electric-charge':family==='fire'?'fire-cast':['magic','psychic','dark'].includes(family)?'magic-cast':'energy-charge';this.sound(charge,3,pan);}
      else if(event.kind==='basic')this.sound('action',1,pan);
      else if(event.kind==='skill'){const charge:Sound=grand?'grand-charge':family==='energy'?'energy-shot':family==='electric'?'electric-charge':family==='fire'?'fire-cast':['magic','psychic','dark'].includes(family)?'magic-cast':'action';this.sound(charge,2,pan);}
      return;
    }
    if(event.kind==='cast')return;
    const sound:Sound=event.kind==='interrupt'?'shatter':grand?'grand-impact':family==='grand'?'grand-impact':family==='physical'?'physical':family;
    this.sound(sound,grand||['ko','turn','interrupt'].includes(event.kind)?4:2,pan);
  }
  private async playAsset(file:string,duration:number,variant:number,out:AudioNode,sound:Sound,gain:number,requestedAt:number){
    const ctx=this.ctx;if(!ctx)return;
    const buffer=await this.loadCue(file);
    if(!buffer||ctx.state!=='running'){synthCue(ctx,out,sound,ctx.currentTime+.005,gain*.62);return;}
    const source=ctx.createBufferSource(),volume=ctx.createGain();source.buffer=buffer;
    source.playbackRate.value=[.985,1,1.012,1.026][variant]??1;
    volume.gain.value=gain;source.connect(volume);volume.connect(out);
    const at=Math.max(ctx.currentTime+.003,requestedAt);
    source.start(at,variant*(duration+.11),duration);
    source.onended=()=>{source.disconnect();volume.disconnect();};
  }
  get status(){const trackSeconds=this.running&&this.ctx&&this.musicStartedAt?(this.musicOffset+Math.max(0,this.ctx.currentTime-this.musicStartedAt))%(this.stemBuffers?.[0]?.duration??Number.POSITIVE_INFINITY):this.musicOffset;return {state:this.ctx?.state??'locked',musicRunning:this.running,mode:this.stemSources.length?'stems':this.loop?'file':'synth',stemsPlaying:this.stemSources.length,musicSeconds:this.stemBuffers?.[0]?.duration??0,trackSeconds,activeCues:this.queued,step:this.step};}
}
export const battleAudio=new BattleAudio();
