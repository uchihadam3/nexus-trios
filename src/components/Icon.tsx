import { Zap, Shield, Waves, Swords, Orbit, Sparkles, Crosshair, Hexagon } from 'lucide-react';
import type { Visual } from '../engine/types';
import { skillArtPath, skillArtSlug } from '../data/skill-art';
import { NEW_SKILL_TILES } from '../data/new-skill-atlas';
const icons={beam:Sparkles,bolt:Zap,slash:Swords,web:Hexagon,shield:Shield,wave:Waves,psychic:Orbit,impact:Crosshair};
export function SkillIcon({type,size=20,characterId,skillId}:{type:Visual;size?:number;characterId?:string;skillId?:string}){const Component=icons[type];
  const tile=skillId?NEW_SKILL_TILES[`${characterId??'unknown'}/${skillArtSlug(skillId)}`]:undefined;
  if(tile){const [page,index]=tile;return <span className="skill-icon-art" role="presentation" aria-hidden="true" style={{display:'inline-block',width:size,height:size,flexShrink:0,backgroundImage:`url(/assets/skills/atlas/page-${String(page).padStart(2,'0')}.png)`,backgroundSize:`${16*size}px ${3*size}px`,backgroundPosition:`-${(index%16)*size}px -${Math.floor(index/16)*size}px`,backgroundRepeat:'no-repeat'}}/>;}
  return skillId?<img loading="lazy" decoding="async" className="skill-icon-art" src={skillArtPath(characterId??'unknown',skillId)} width={size} height={size} alt="" aria-hidden="true"/>:<Component size={size} strokeWidth={1.6}/>;}

export type AuxiliaryIconId='ready'|'cooldown'|'charging'|'preparing'|'executing'|'buff'|'debuff'|'tempo-up'|'tempo-down'|'interrupt'|'history'|'inspect'|'help'|'domain'|'victory'|'defeat';
export function AuxIcon({id,size=18,className=''}:{id:AuxiliaryIconId;size?:number;className?:string}){
  return <img loading="lazy" decoding="async" className={`aux-icon-art ${className}`.trim()} src={`/assets/ui/${id}.png`} width={size} height={size} alt="" aria-hidden="true"/>;
}
