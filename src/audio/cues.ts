/** Reusable offline banks; every file holds three deterministic takes. */
export type Sound='action'|'physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'impact'|'block'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ready'|'prepare'|'shatter'|'ko'|'dominion'|'turn'|'victory'|'defeat'|'energy-shot'|'energy-charge'|'electric-charge'|'fire-cast'|'magic-cast'|'grand-charge'|'grand-impact';
export interface CueAsset {file:string;duration:number}
const cue=(file:string,duration:number):CueAsset=>({file,duration});
export const CUE_ASSETS:Record<Sound,CueAsset>={
  action:cue('physical-light',.28),physical:cue('physical-heavy',.46),impact:cue('physical-heavy',.46),
  energy:cue('energy-impact',.48),electric:cue('electric',.4),fire:cue('fire',.48),
  magic:cue('magic',.5),psychic:cue('magic',.5),dark:cue('dark-control',.5),
  slash:cue('slash',.38),prison:cue('dark-control',.5),block:cue('shield',.45),shield:cue('shield',.45),
  heal:cue('heal-buff',.58),regen:cue('heal-buff',.58),buff:cue('heal-buff',.58),debuff:cue('dark-control',.5),
  interrupt:cue('interrupt',.3),ready:cue('energy-charge',.55),prepare:cue('energy-charge',.55),
  shatter:cue('interrupt',.3),ko:cue('ko',.65),dominion:cue('magic',.5),turn:cue('magic',.5),
  victory:cue('victory',1.05),defeat:cue('defeat',.95),
  'energy-shot':cue('energy-shot',.36),'energy-charge':cue('energy-charge',.55),
  'electric-charge':cue('electric',.4),'fire-cast':cue('fire',.48),
  'magic-cast':cue('magic',.5),'grand-charge':cue('energy-charge',.55),'grand-impact':cue('grand',.76),
};
export const CUE_FILES=[...new Set(Object.values(CUE_ASSETS).map(asset=>asset.file)),'projectile'];
