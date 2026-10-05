import { hz,noise,tone } from './synth';
export type Sound='action'|'physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'impact'|'block'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ready'|'prepare'|'shatter'|'ko'|'dominion'|'turn'|'victory'|'defeat'|'energy-shot'|'energy-charge'|'electric-charge'|'fire-cast'|'magic-cast'|'grand-charge'|'grand-impact';
export interface CueAsset {file:string;duration:number}
const cue=(file:string,duration:number):CueAsset=>({file,duration});
export const CUE_ASSETS:Record<Sound,CueAsset>={
  action:cue('physical-light',.42),physical:cue('physical-heavy',.78),impact:cue('physical-heavy',.78),
  energy:cue('energy-impact',.78),electric:cue('electric-hit',.48),fire:cue('fire-impact',.72),
  magic:cue('magic-impact',.75),psychic:cue('magic-impact',.75),dark:cue('magic-impact',.75),
  slash:cue('slash-heavy',.61),prison:cue('shield-hit',.55),block:cue('shield-hit',.55),shield:cue('shield-on',.68),
  heal:cue('heal',.86),regen:cue('regen',.72),buff:cue('shield-on',.68),debuff:cue('interrupt',.38),
  interrupt:cue('interrupt',.38),ready:cue('energy-charge',.95),prepare:cue('energy-charge',.95),
  shatter:cue('shatter',.68),ko:cue('ko',1.05),dominion:cue('domain-turn',.82),turn:cue('domain-turn',.82),
  victory:cue('victory',1.45),defeat:cue('defeat',1.25),
  'energy-shot':cue('energy-shot',.58),'energy-charge':cue('energy-charge',.95),
  'electric-charge':cue('electric-charge',.52),'fire-cast':cue('fire-cast',.72),
  'magic-cast':cue('magic-cast',.95),'grand-charge':cue('grand-charge',1.25),'grand-impact':cue('grand-impact',1.18),
};
export function synthCue(ctx:BaseAudioContext,out:AudioNode,sound:Sound,time:number,power=1){
  const note=(f:number,d:number,g:number,type:OscillatorType='sine',end?:number,offset=0)=>tone(ctx,out,time+offset,f,d,g*power,type,end);
  const air=(d:number,g:number,f:number,offset=0)=>noise(ctx,out,time+offset,d,g*power,f);
  switch(sound){
    case 'action':air(.13,.07,1200);note(240,.14,.06,'triangle',140);break;
    case 'physical':case 'impact':note(sound==='physical'?105:72,.22,.25,'sine',34);air(.12,.16,1600);break;
    case 'energy':note(155,.40,.14,'triangle',540);note(320,.45,.055,'sine',100);air(.35,.055,1800);break;
    case 'electric':for(let i=0;i<4;i++){note(390+i*85,.055,.07,'triangle',160,i*.045);air(.04,.07,3200,i*.045);}break;
    case 'fire':note(72,.46,.11,'sine',39);note(116,.42,.06,'triangle',180,.03);air(.3,.12,1200);break;
    case 'magic':case 'psychic':case 'dark':{const root=sound==='dark'?45:sound==='psychic'?57:62;[0,7,12].forEach((n,i)=>note(hz(root+n),.55,.07,'sine',undefined,i*.055));if(sound==='dark')air(.5,.06,800);break;}
    case 'slash':air(.18,.15,2400);note(600,.13,.05,'triangle',140);break;
    case 'prison':note(280,.35,.08,'triangle',110);air(.17,.10,1500);break;
    case 'block':note(370,.18,.12,'triangle',260);note(740,.13,.04);air(.08,.08,2800);break;
    case 'shield':[330,495,660].forEach((f,i)=>note(f,.4,.055,'sine',undefined,i*.035));break;
    case 'heal':case 'regen':[60,64,67].forEach((n,i)=>note(hz(n),.43,sound==='regen'?.03:.065,'sine',undefined,i*.08));break;
    case 'buff':[55,62,67].forEach((n,i)=>note(hz(n),.30,.05,'triangle',undefined,i*.07));break;
    case 'debuff':note(230,.36,.085,'triangle',105);air(.2,.04,800);break;
    case 'interrupt':air(.10,.12,1600);note(420,.16,.09,'triangle',210);break;
    case 'shatter':air(.28,.17,2200);note(560,.26,.085,'triangle',100);note(155,.3,.11,'sine',45);break;
    case 'ready':note(523,.15,.037);note(784,.22,.025,'sine',undefined,.09);break;
    case 'prepare':note(85,.9,.09,'triangle',220);note(170,.9,.05,'sine',440);air(.7,.04,1000);break;
    case 'ko':note(160,.7,.18,'triangle',28);air(.45,.1,900);break;
    case 'dominion':note(196,.28,.06);note(294,.4,.04,'sine',undefined,.08);break;
    case 'turn':[50,57,62,65].forEach((n,i)=>note(hz(n),.45,.065,'triangle',undefined,i*.08));air(.3,.07,1900);break;
    case 'victory':[62,65,69,74,77].forEach((n,i)=>note(hz(n),.65,.08,'triangle',undefined,i*.13));note(146.83,1,.10);break;
    case 'defeat':[62,60,57,50].forEach((n,i)=>note(hz(n),.65,.075,'triangle',undefined,i*.17));break;
  }
}
