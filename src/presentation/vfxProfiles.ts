/** Declarative, character specific staging layered over reusable VFX families. */
import { byId } from '../data/characters';
import type { Skill } from '../engine/types';
export type VfxMotif = 'beam'|'orb'|'spiral'|'branching'|'death-note'|'elastic'|'punch'|'hammer'|'heat-vision'|'web'|'portal'|'speed'|'magnetic'|'shadow'|'cosmic';
export interface VfxProfile {id:string;motif:VfxMotif;family?:string;scale:number;travel:boolean;area?:boolean}
const profile=(id:string,motif:VfxMotif,scale=1,travel=true,family?:string,area=false):VfxProfile=>({id,motif,scale,travel,family,area});
const presets:Record<string,VfxProfile>={
  'goku:0':profile('kamehameha','beam',1.45,true,'energy'),
  'vegeta:2':profile('final-flash','beam',1.7,true,'grand'),
  'naruto:1':profile('rasengan','spiral',1.18,true,'magic'),
  'sasuke:0':profile('chidori','branching',1.12,true,'electric'),
  'sasuke:1':profile('amaterasu','shadow',1.12,true,'dark'),
  'light:2':profile('death-note','death-note',1.24,false,'dark'),
  'pikachu:0':profile('thunder-jolt','branching',1.06,true,'electric'),
  'luffy:2':profile('gear-fifth','elastic',1.35,false,'physical'),
  'saitama:2':profile('serious-punch','punch',1.7,false,'grand'),
  'superman:0':profile('heat-vision','heat-vision',1.05,true,'energy'),
  'spiderman:0':profile('web-cast','web',1.18,true,'prison'),
  'spiderman:2':profile('impact-web','web',1.2,true,'prison'),
  'thor:0':profile('mjolnir-strike','hammer',1.35,true,'electric'),
  'thor:1':profile('mjolnir-storm','hammer',1.55,true,'electric',true),
  'strange:2':profile('sling-ring-portal','portal',1.2,false,'magic',true),
  'flash:0':profile('thousand-blows','speed',1.45,false,'physical',true),
  'magneto:0':profile('magnetic-prison','magnetic',1.3,false,'prison',true),
  'raven:2':profile('azarath-shadow','shadow',1.35,false,'dark',true),
  'thanos:2':profile('titan-cosmic-wave','cosmic',1.6,true,'grand',true),
  'gojo:2':profile('infinite-domain','cosmic',1.65,false,'psychic',true),
  'ironman:2':profile('unibeam','beam',1.45,true,'energy'),
  'captain:0':profile('ricochet-shield','orb',1.05,true,'physical',true),
  'wonderwoman:0':profile('lasso-of-truth','web',1.1,true,'magic'),
  'gohan:2':profile('gohan-awakening','cosmic',1.5,false,'energy',true),
  'frieza:1':profile('death-ray','heat-vision',.95,true,'dark'),
  'kakashi:1':profile('raikiri','branching',1.16,true,'electric'),
  'itachi:0':profile('tsukuyomi','shadow',1.3,false,'psychic'),
  'tanjiro:2':profile('sun-breathing','spiral',1.36,true,'fire'),
  'zenitsu:2':profile('sixfold-thunder','speed',1.4,true,'electric'),
  'yuji:1':profile('black-flash','punch',1.28,false,'dark'),
  'sukuna:2':profile('malevolent-shrine','shadow',1.65,false,'dark',true),
  'ichigo:2':profile('bankai','speed',1.55,true,'dark'),
  'aizen:1':profile('hado-ninety','beam',1.5,true,'magic'),
  'levi:2':profile('thunder-execution','speed',1.4,true,'slash'),
  'killua:2':profile('godspeed','speed',1.35,true,'electric'),
  'roy:1':profile('flame-rain','orb',1.42,true,'fire',true),
  'guts:0':profile('dragon-slayer','hammer',1.48,false,'slash'),
  'jotaro:2':profile('time-stop','speed',1.38,false,'psychic',true),
  'dio:2':profile('the-world','shadow',1.38,false,'dark',true),
  'denji:2':profile('chainsaw-frenzy','speed',1.4,false,'slash',true),
  'frieren:1':profile('zoltraak','beam',1.24,true,'magic'),
  'jinwoo:2':profile('shadow-army','shadow',1.62,false,'dark',true),
  'kaiba:2':profile('ultimate-burst','beam',1.7,true,'grand',true),
  'scarletwitch:2':profile('chaos-distortion','cosmic',1.6,false,'psychic',true),
  'captainmarvel:2':profile('binary-explosion','cosmic',1.56,true,'energy',true),
  'ghostrider:2':profile('penance-stare','shadow',1.42,false,'fire'),
  'storm:2':profile('eye-of-the-storm','branching',1.62,true,'electric',true),
  'cyclops:2':profile('optic-beam','heat-vision',1.35,true,'energy'),
  'jeangrey:2':profile('phoenix-rise','cosmic',1.68,false,'fire',true),
  'loki:2':profile('perfect-deception','portal',1.34,false,'magic'),
  'silversurfer:2':profile('dimensional-surf','portal',1.46,true,'magic'),
  'galactus:2':profile('world-devourer','cosmic',1.8,false,'grand',true),
  'greenlantern:2':profile('will-construct','orb',1.42,false,'shield'),
  'shazam:0':profile('magic-lightning','branching',1.3,true,'electric'),
};
function familyFor(skill:Skill):string {
  if(skill.effects.some(e=>e.kind==='status'&&e.status==='burning'))return 'fire';
  if(skill.effects.some(e=>e.kind==='damage'||e.kind==='deathnote'||e.kind==='release'))return ({beam:'energy',bolt:'electric',slash:'slash',web:'prison',psychic:'psychic',wave:'magic',shield:'physical',impact:'physical'} as const)[skill.icon];
  if(skill.effects.some(e=>e.kind==='heal'||e.kind==='status'&&e.status==='regen'))return 'heal';
  if(skill.effects.some(e=>e.kind==='shield'))return 'shield';
  if(skill.effects.some(e=>e.kind==='status'&&['haste','strengthened','protected'].includes(e.status)))return 'buff';
  if(skill.effects.some(e=>e.kind==='status'&&['paralyzed','rooted','slow','silenced'].includes(e.status)))return 'prison';
  return skill.icon==='psychic'?'psychic':'magic';
}
function motifFor(skill:Skill):VfxMotif {
  const name=skill.name.toLocaleLowerCase('pt-BR');
  if(/portal|dimens|teleport/.test(name))return 'portal';
  if(/teia|corrente|laço|raiz/.test(name))return 'web';
  if(/sombra|noite|ilusão|hipnose/.test(name))return 'shadow';
  if(/raio|laser|feixe|visão/.test(name)&&skill.icon==='beam')return 'heat-vision';
  if(/veloc|relâmpago|giro|investida/.test(name))return 'speed';
  if(/martelo|esmag|soco|punho/.test(name))return skill.icon==='impact'?'punch':'hammer';
  return ({beam:'beam',bolt:'branching',slash:'speed',web:'web',shield:'orb',wave:'spiral',psychic:'shadow',impact:'punch'} as const)[skill.icon];
}
export function profileFor(characterId:string,skillIndex?:number):VfxProfile|undefined{
  if(skillIndex===undefined)return undefined;
  const specific=presets[`${characterId}:${skillIndex}`];if(specific)return specific;
  const skill=byId[characterId]?.skills[skillIndex];if(!skill)return undefined;
  const area=skill.target==='allEnemies'||skill.target==='allAllies'||skill.effects.some(e=>e.target==='allEnemies'||e.target==='allAllies');
  const family=familyFor(skill),motif=motifFor(skill);
  const travel=!['self','allAllies'].includes(skill.target)&&!['shield','heal','buff'].includes(family);
  return profile(`${characterId}-${skill.id}`,motif,1+skillIndex*.11+(skill.preparation>=2.5?.16:0),travel,family,area);
}
export const VFX_PRESETS=presets;
