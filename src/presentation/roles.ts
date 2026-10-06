import type { Character,Effect } from '../engine/types';
export type Role='Dano'|'Proteção'|'Cura'|'Controle'|'Ritmo'|'Finalização';
export const roleOrder:Role[]=['Dano','Proteção','Cura','Controle','Ritmo','Finalização'];
export function rolesFor(c:Character):Role[]{
  const effects:Effect[]=[...c.basic.effects,...c.trait.effects,...c.skills.flatMap(s=>s.effects)];
  const has=(fn:(effect:Effect)=>boolean)=>effects.some(fn);
  const roles:Role[]=[];
  if(has(e=>e.kind==='damage'||e.kind==='release'))roles.push('Dano');
  if(has(e=>e.kind==='shield'||e.kind==='status'&&e.status==='protected'))roles.push('Proteção');
  if(has(e=>e.kind==='heal'||e.kind==='status'&&e.status==='regen'))roles.push('Cura');
  if(has(e=>e.kind==='interrupt'||e.kind==='status'&&['paralyzed','silenced','rooted','confused'].includes(e.status)))roles.push('Controle');
  if(has(e=>e.kind==='shift'||e.kind==='status'&&['haste','slow'].includes(e.status)))roles.push('Ritmo');
  if(has(e=>e.kind==='deathnote'||e.kind==='damage'&&e.value>=350))roles.push('Finalização');
  return roles.slice(0,3);
}
