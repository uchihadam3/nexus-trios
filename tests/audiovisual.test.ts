import { describe,expect,it } from 'vitest';
import { readFileSync,statSync } from 'node:fs';
import { resolve } from 'node:path';
import { CUE_ASSETS } from '../src/audio/cues';
import { VFX_PRESETS,profileFor } from '../src/presentation/vfxProfiles';

const root=process.cwd();
const vfx=JSON.parse(readFileSync(resolve(root,'public/assets/vfx/manifest.json'),'utf8')) as {columns:number;rows:number;families:Record<string,{file:string;frames:number;frameSize:[number,number];alpha:boolean;bytes:number}>};
const sfx=JSON.parse(readFileSync(resolve(root,'public/assets/audio/sfx/manifest.json'),'utf8')) as {sampleRate:number;variants:number;sounds:Record<string,{file:string;duration:number;variantOffsets:number[]}>};

describe('presentation audiovisual assets',()=>{
  it('publishes all visual families as transparent, normalized 4×4 atlases',()=>{
    expect(vfx.columns).toBe(4);expect(vfx.rows).toBe(4);expect(Object.keys(vfx.families).length).toBeGreaterThanOrEqual(17);
    for(const [family,atlas] of Object.entries(vfx.families)){
      expect(atlas.frames,`${family} frame count`).toBe(16);expect(atlas.alpha,`${family} alpha`).toBe(true);
      expect(atlas.frameSize[0]).toBe(atlas.frameSize[1]);expect(statSync(resolve(root,'public/assets/vfx',atlas.file)).size).toBe(atlas.bytes);
    }
    expect(vfx.families.energy.frameSize[0]).toBeGreaterThanOrEqual(256);
    expect(vfx.families.grand.frameSize[0]).toBeGreaterThanOrEqual(384);
  });

  it('stages the iconic abilities through distinct family and motif combinations',()=>{
    const expected=['kamehameha','final-flash','rasengan','chidori','death-note','gear-fifth','serious-punch','heat-vision','web-cast','mjolnir-storm','sling-ring-portal','thousand-blows','magnetic-prison','azarath-shadow'];
    for(const id of expected)expect(Object.values(VFX_PRESETS).some(p=>p.id===id),id).toBe(true);
    expect(profileFor('goku',0)?.motif).toBe('beam');expect(profileFor('naruto',1)?.motif).toBe('spiral');
    expect(profileFor('sasuke',0)?.motif).toBe('branching');expect(profileFor('light',2)?.travel).toBe(false);
    expect(profileFor('pikachu',0)?.family).toBe('electric');expect(profileFor('saitama',2)?.motif).toBe('punch');
    expect(profileFor('spiderman',0)?.motif).toBe('web');expect(profileFor('thor',1)?.area).toBe(true);
    expect(profileFor('strange',2)?.motif).toBe('portal');expect(profileFor('flash',0)?.motif).toBe('speed');
    expect(profileFor('magneto',0)?.motif).toBe('magnetic');expect(profileFor('raven',2)?.family).toBe('dark');
    expect(new Set(Object.values(VFX_PRESETS).map(p=>p.motif)).size).toBeGreaterThanOrEqual(10);
  });

  it('generates playable four-variation WAV banks for every Web Audio cue',()=>{
    expect(sfx.sampleRate).toBe(24000);expect(sfx.variants).toBe(4);
    const names=new Set(Object.values(sfx.sounds).map(x=>x.file));
    for(const asset of Object.values(CUE_ASSETS))expect(names.has(`${asset.file}.wav`),asset.file).toBe(true);
    for(const [name,cue] of Object.entries(sfx.sounds)){
      const data=readFileSync(resolve(root,'public/assets/audio/sfx',cue.file));
      expect(data.subarray(0,4).toString('ascii'),name).toBe('RIFF');expect(data.subarray(8,12).toString('ascii'),name).toBe('WAVE');
      expect(cue.variantOffsets).toHaveLength(4);expect(data.length).toBeGreaterThan(Math.round(cue.duration*24000*2));
    }
  });
});
