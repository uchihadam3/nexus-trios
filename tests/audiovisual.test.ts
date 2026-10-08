import { describe,expect,it } from 'vitest';
import { readFileSync,readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { CUE_ASSETS,CUE_FILES } from '../src/audio/cues';
import { FAMILIAS,VFX_FAMILIES,folhasUsadas,hsl,profileFor } from '../src/presentation/vfxProfiles';
import { characters } from '../src/data/characters';

const root=process.cwd();
const familias=JSON.parse(readFileSync(resolve(root,'public/assets/vfx/familias/manifest.json'),'utf8')) as Record<string,{quadros:number;grade:[number,number];tamanho:[number,number];laco:boolean;bytes:number}>;
const sfx=JSON.parse(readFileSync(resolve(root,'public/assets/audio/sfx/manifest.json'),'utf8')) as {sampleRate:number;variants:number;sounds:Record<string,{file:string;duration:number;variantOffsets:number[]}>};

describe('compact reusable audiovisual library',()=>{
  it('ships the Python-drawn family sheets: 3×4, transparent WebP, all used, within budget',()=>{
    const usadas=folhasUsadas();
    expect(Object.keys(familias).sort()).toEqual(usadas);
    let bytes=0,decodificado=0;
    for(const [nome,f] of Object.entries(familias)){
      expect(f.quadros,nome).toBe(12);expect(f.grade,nome).toEqual([3,4]);
      const data=readFileSync(resolve(root,'public/assets/vfx/familias',`${nome}.webp`));
      expect(data.length,nome).toBe(f.bytes);
      expect(data.subarray(0,4).toString('ascii')).toBe('RIFF');expect(data.subarray(8,12).toString('ascii')).toBe('WEBP');
      expect(data.subarray(12,16).toString('ascii'),`${nome} tem alfa (VP8X)`).toBe('VP8X');
      expect(f.bytes,`${nome} pequeno o bastante para celular`).toBeLessThan(160_000);
      bytes+=f.bytes;decodificado+=f.tamanho[0]*f.tamanho[1]*12*4;
    }
    expect(bytes).toBeLessThan(3_500_000);
    // nenhuma folha decodificada passa de ~4,5 MB na memória (a maior é a faixa de 512 × 96 × 12)
    expect(decodificado/Object.keys(familias).length).toBeLessThan(2_000_000);
    expect(readdirSync(resolve(root,'public/assets/vfx')).filter(x=>x.endsWith('.webp'))).toEqual(['arena.webp']);
  });
  it('maps every basic and skill to one of 30–45 shared families, all of them used, none dominating',()=>{
    expect(FAMILIAS.length).toBeGreaterThanOrEqual(30);expect(FAMILIAS.length).toBeLessThanOrEqual(45);
    const uso=new Map<string,number>();let total=0;
    for(const character of characters){
      for(const index of [undefined,0,1,2] as const){
        const p=profileFor(character.id,index);
        expect(p,`${character.id} ${index}`).toBeDefined();expect(VFX_FAMILIES[p!.family]).toBeDefined();
        expect(p).toEqual(profileFor(character.id,index));
        // cor legível sobre a arena escura
        const [,,l]=hsl(p!.color);expect(l,`${character.id} ${index} ${p!.color}`).toBeGreaterThanOrEqual(.45);expect(l).toBeLessThanOrEqual(.76);
        uso.set(p!.family,(uso.get(p!.family)??0)+1);total++;
        if(index!==undefined){const skill=character.skills[index];expect(p!.area,skill.name).toBe(skill.target==='allEnemies'||skill.target==='allAllies'||skill.effects.some(e=>e.target==='allEnemies'||e.target==='allAllies'));}
      }
    }
    for(const f of FAMILIAS)expect(uso.get(f)??0,`${f} usada`).toBeGreaterThan(0);
    for(const [f,n] of uso)expect(n/total,`${f} não domina`).toBeLessThan(.16);
  });
  it('gives the famous skills the effect and colour people recognise',()=>{
    expect(profileFor('goku',0)?.family).toBe('feixe_pesado');
    const [h]=hsl(profileFor('goku',0)!.color);expect(h).toBeGreaterThan(185);expect(h).toBeLessThan(215);
    expect(profileFor('superman',0)?.family).toBe('feixe');expect(hsl(profileFor('superman',0)!.color)[0]).toBeLessThan(15);
    expect(profileFor('pikachu',0)?.family).toBe('raio');
    expect(profileFor('spiderman',0)?.family).toBe('prisao');
    expect(profileFor('light',2)?.family).toBe('execucao');
    expect(profileFor('naruto',1)?.family).toBe('esfera_carregada');
    expect(profileFor('ichigo',0)?.family).toBe('corte_de_energia');
    expect(profileFor('charizard',0)?.family).toBe('fogo');
    // a mesma família muda de cor com o personagem
    expect(profileFor('vegeta',0)?.family).toBe('feixe_pesado');expect(profileFor('vegeta',0)?.color).not.toBe(profileFor('goku',0)?.color);
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
