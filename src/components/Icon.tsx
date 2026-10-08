import { Zap, Shield, Waves, Swords, Orbit, Sparkles, Crosshair, Hexagon } from 'lucide-react';
import type { Visual } from '../engine/types';
import { skillArtPath } from '../data/skill-art';
const icons={beam:Sparkles,bolt:Zap,slash:Swords,web:Hexagon,shield:Shield,wave:Waves,psychic:Orbit,impact:Crosshair};
export function SkillIcon({type,size=20,characterId,skillId}:{type:Visual;size?:number;characterId?:string;skillId?:string}){const Component=icons[type];return skillId?<img loading="lazy" decoding="async" className="skill-icon-art" src={skillArtPath(characterId??'unknown',skillId)} width={size} height={size} alt="" aria-hidden="true"/>:<Component size={size} strokeWidth={1.6}/>;}

export type AuxiliaryIconId='ready'|'cooldown'|'charging'|'preparing'|'executing'|'buff'|'debuff'|'tempo-up'|'tempo-down'|'interrupt'|'history'|'inspect'|'help'|'domain'|'victory'|'defeat';
export function AuxIcon({id,size=18,className=''}:{id:AuxiliaryIconId;size?:number;className?:string}){
  return <img loading="lazy" decoding="async" className={`aux-icon-art ${className}`.trim()} src={`/assets/ui/${id}.png`} width={size} height={size} alt="" aria-hidden="true"/>;
}
