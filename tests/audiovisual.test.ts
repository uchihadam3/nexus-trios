import { describe,expect,it } from 'vitest';
import { readFileSync,statSync,readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { CUE_ASSETS,CUE_FILES } from '../src/audio/cues';
import { VFX_FAMILIES,atlasFor,profileFor } from '../src/presentation/vfxProfiles';
import { characters } from '../src/data/characters';

const root=process.cwd();
const vfx=JSON.parse(readFileSync(resolve(root,'public/assets/vfx/manifest.json'),'utf8')) as {columns:number;rows:number;families:Record<string,{file:string;frames:number;frameSize:[number,number];alpha:boolean;bytes:number}>;beam:{file:string;bytes:number}};
const sfx=JSON.parse(readFileSync(resolve(root,'public/assets/audio/sfx/manifest.json'),'utf8')) as {sampleRate:number;variants:number;sounds:Record<string,{file:string;duration:number;variantOffsets:number[]}>};

describe('compact reusable audiovisual library',()=>{
  it('ships only transparent 3×4 atlases, a prerendered beam and arena within budget',()=>{
    expect(vfx.columns).toBe(3);expect(vfx.rows).toBe(4);
    expect(Object.keys(vfx.families).sort()).toEqual([...new Set(Object.keys(VFX_FAMILIES).map(f=>atlasFor(f as keyof typeof VFX_FAMILIES)))].sort());
    let bytes=vfx.beam.bytes+statSync(resolve(root,'public/assets/vfx/arena.webp')).size;
    let decoded=0;
    for(const [family,atlas] of Object.entries(vfx.families)){
      expect(atlas.frames,family).toBe(12);expect(atlas.alpha,family).toBe(true);
      expect(atlas.frameSize).toEqual([VFX_FAMILIES[family as keyof typeof VFX_FAMILIES].size,VFX_FAMILIES[family as keyof typeof VFX_FAMILIES].size]);
      expect(statSync(resolve(root,'public/assets/vfx',atlas.file)).size).toBe(atlas.bytes);
      bytes+=atlas.bytes;decoded+=atlas.frameSize[0]*atlas.frameSize[1]*12*4;
    }
    expect(statSync(resolve(root,'public/assets/vfx',vfx.beam.file)).size).toBe(vfx.beam.bytes);
    expect(bytes).toBeLessThan(2_000_000);expect(decoded).toBeLessThan(14_000_000);
    expect(readdirSync(resolve(root,'public/assets/vfx')).filter(x=>x.endsWith('.webp')).length).toBe(14);
  });
  it('maps every basic and skill through shared families without per-character presets',()=>{
    for(const character of characters){
      const basic=profileFor(character.id);
      expect(basic,`${character.id} basic`).toBeDefined();expect(VFX_FAMILIES[basic!.family]).toBeDefined();
      character.skills.forEach((skill,index)=>{
        const p=profileFor(character.id,index);
        expect(p,`${character.id}: ${skill.name}`).toBeDefined();expect(VFX_FAMILIES[p!.family]).toBeDefined();
        expect(p!.area,skill.name).toBe(skill.target==='allEnemies'||skill.target==='allAllies'||skill.effects.some(e=>e.target==='allEnemies'||e.target==='allAllies'));
      });
    }
    expect(profileFor('goku',0)?.family).toBe('energy_beam');
    expect(profileFor('pikachu',0)?.family).toBe('electric');
    expect(profileFor('spiderman',0)?.family).toBe('control');
  });
  it('keeps three deterministic, decoded-ahead WAV variants within budget',()=>{
    expect(sfx.sampleRate).toBe(22050);expect(sfx.variants).toBe(3);
    expect(Object.keys(sfx.sounds).sort()).toEqual(CUE_FILES.sort());
    let bytes=0;
    for(const asset of Object.values(CUE_ASSETS))expect(sfx.sounds[asset.file]).toBeDefined();
    for(const [name,cue] of Object.entries(sfx.sounds)){
      const data=readFileSync(resolve(root,'public/assets/audio/sfx',cue.file));bytes+=data.length;
      expect(data.subarray(0,4).toString('ascii'),name).toBe('RIFF');expect(data.subarray(8,12).toString('ascii'),name).toBe('WAVE');
      expect(cue.variantOffsets).toHaveLength(3);expect(data.length).toBeGreaterThan(Math.round(cue.duration*22050*2));
    }
    expect(bytes).toBeLessThan(2_000_000);
    expect(readdirSync(resolve(root,'public/assets/audio/sfx')).filter(x=>x.endsWith('.wav')).length).toBe(18);
  });
});
