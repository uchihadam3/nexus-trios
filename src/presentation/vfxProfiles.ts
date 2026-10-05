/** Declarative, character specific staging layered over reusable VFX families. */
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
  'spiderman:2':profile('impact-web','web',1.2,true,'impact'),
  'thor:0':profile('mjolnir-strike','hammer',1.35,true,'electric'),
  'thor:1':profile('mjolnir-storm','hammer',1.55,true,'electric',true),
  'strange:2':profile('sling-ring-portal','portal',1.2,false,'magic',true),
  'flash:0':profile('thousand-blows','speed',1.45,false,'physical',true),
  'magneto:0':profile('magnetic-prison','magnetic',1.3,false,'prison',true),
  'raven:2':profile('azarath-shadow','shadow',1.35,false,'dark',true),
  'thanos:2':profile('titan-cosmic-wave','cosmic',1.6,true,'grand',true),
};
export function profileFor(characterId:string,skillIndex?:number):VfxProfile|undefined{return skillIndex===undefined?undefined:presets[`${characterId}:${skillIndex}`];}
export const VFX_PRESETS=presets;
