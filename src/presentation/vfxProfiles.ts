/** Small, shared visual vocabulary. Gameplay data selects one atlas and staging. */
import { byId } from '../data/characters';
import type { Effect,Skill,Target,Visual } from '../engine/types';

export const VFX_FAMILIES={
  physical_light:{name:'Impacto leve',color:'#ffe1b1',size:96},
  physical_heavy:{name:'Impacto forte',color:'#ffcc96',size:128},
  slash:{name:'Corte',color:'#daefff',size:128},
  projectile:{name:'Projétil',color:'#ffe1b1',size:96},
  energy_orb:{name:'Esfera de energia',color:'#8bdfff',size:128},
  energy_beam:{name:'Feixe de energia',color:'#8bdfff',size:128},
  electric:{name:'Eletricidade',color:'#ffef8e',size:128},
  fire:{name:'Fogo',color:'#ff7738',size:128},
  magic_psychic:{name:'Magia e psíquico',color:'#c197ff',size:128},
  dark:{name:'Sombras',color:'#ae63ef',size:128},
  control:{name:'Controle',color:'#9fe1f3',size:128},
  shield:{name:'Escudo',color:'#8edeff',size:128},
  heal_buff:{name:'Cura e bônus',color:'#8bffc1',size:128},
} as const;
export type VfxFamily=keyof typeof VFX_FAMILIES;
export const atlasFor=(family:VfxFamily):Exclude<VfxFamily,'energy_beam'>=>family==='energy_beam'?'energy_orb':family;
export interface VfxProfile {family:VfxFamily;variant:0|1;scale:number;travel:boolean;area:boolean;intensity:number}
const familyByIcon:Record<Visual,VfxFamily>={beam:'energy_beam',bolt:'electric',slash:'slash',web:'control',shield:'shield',wave:'magic_psychic',psychic:'magic_psychic',impact:'physical_light'};
const ranged=new Set<VfxFamily>(['projectile','energy_orb','energy_beam','electric','fire','magic_psychic','dark','control']);
function resolve(icon:Visual,effects:Effect[],target:Target,name:string):VfxFamily{
  const status=effects.find(e=>e.kind==='status');
  if(status?.kind==='status'&&status.status==='burning')return 'fire';
  if(effects.some(e=>e.kind==='heal'||e.kind==='status'&&e.status==='regen'))return 'heal_buff';
  if(effects.some(e=>e.kind==='shield')&&!effects.some(e=>e.kind==='damage'))return 'shield';
  if(!effects.some(e=>['damage','release','deathnote'].includes(e.kind))){
    if(status?.kind==='status'&&['paralyzed','electric'].includes(status.status))return 'electric';
    if(status?.kind==='status'&&['rooted','silenced','slow'].includes(status.status))return 'control';
    if(status?.kind==='status'&&['haste','strengthened','protected'].includes(status.status))return 'heal_buff';
  }
  if(/sombr|trev|escur|mald|death note|penance/i.test(name))return 'dark';
  if(/chama|fogo|flame|phoenix|inferno/i.test(name))return 'fire';
  if(icon==='impact'&&/esmag|soco sério|serious|hammer|martelo/i.test(name))return 'physical_heavy';
  if(icon==='impact'&&target==='randomEnemy')return 'projectile';
  return familyByIcon[icon];
}
export function profileFor(characterId:string,skillIndex?:number):VfxProfile|undefined{
  const character=byId[characterId];if(!character)return undefined;
  const skill:Pick<Skill,'icon'|'effects'|'target'|'name'|'preparation'>=skillIndex===undefined?{
    icon:character.basic.visual,effects:character.basic.effects,target:character.basic.target,name:character.basic.name,preparation:0,
  }:character.skills[skillIndex];
  if(!skill)return undefined;
  const family=resolve(skill.icon,skill.effects,skill.target,skill.name);
  const area=skill.target==='allEnemies'||skill.target==='allAllies'||skill.effects.some(e=>e.target==='allEnemies'||e.target==='allAllies');
  const travel=ranged.has(family)&&!['self','allAllies'].includes(skill.target);
  return {family,variant:skillIndex===2?1:0,scale:1+(skillIndex??0)*.1+(skill.preparation>=2.5?.17:0),travel,area,intensity:1};
}
