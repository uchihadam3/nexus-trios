import { existsSync,readFileSync,readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { describe,it,expect } from 'vitest';
import { characters } from '../src/data/characters';
import { familyOf } from '../src/presentation/director';
import { createBattle } from '../src/engine/battle';
import type { BattleEvent } from '../src/engine/types';
import { statuses } from '../src/data/statuses';
import { skillArtPath } from '../src/data/skill-art';
import approvedPortraits from '../src/data/expanded-portrait-approvals.json';

const root=new URL('../public/',import.meta.url);
describe('Arte local e composição',()=>{
  it('mantém um retrato disponível e próprio para cada personagem',()=>{
    for(const character of characters){
      const file=new URL(character.portrait.slice(1),root);
      expect(existsSync(file),`retrato de ${character.id}`).toBe(true);
    }
    expect(characters.every(character=>character.portrait.startsWith('/assets/portraits/'))).toBe(true);
    expect(new Set(characters.map(character=>character.portrait)).size).toBe(characters.length);
  });
  it('usa somente retratos revisados dos quadros originais para a expansão',()=>{
    const approved=new Set(approvedPortraits);
    const expanded=characters.slice(100);
    expect(approved.size).toBe(approvedPortraits.length);
    expect(expanded.filter(character=>approved.has(character.id))).toHaveLength(approved.size);
    expect(existsSync(new URL('../assets/ai-source/portraits/overrides/rick.webp',root))).toBe(true);
    for(const character of expanded){
      const reviewed=approved.has(character.id);
      expect(character.portrait).toBe(reviewed
        ?`/assets/portraits/expanded/${character.id}.webp`
        :`/assets/portraits/placeholder-${character.id}.svg`);
      if(reviewed){
        const file=readFileSync(new URL(character.portrait.slice(1),root));
        expect(file.toString('ascii',0,4)).toBe('RIFF');
        expect(file.toString('ascii',8,12)).toBe('WEBP');
      }
    }
  });
  it('usa retratos revisados em WebP para o primeiro elenco e mantém alternativas válidas',()=>{
    const source=new URL('../assets/portraits/source/',root);
    const reviewed=new Set(readdirSync(source).filter(name=>name.endsWith('.webp')).map(name=>name.slice(0,-5)));
    expect(reviewed.size).toBe(56);
    for(const character of characters.slice(0,100)){
      const path=character.portrait;
      expect(path,character.id).not.toContain('placeholder');
      const bytes=readFileSync(new URL(path.slice(1),root));
      expect(bytes.length,character.id).toBeGreaterThan(4_000);
      if(reviewed.has(character.id)){
        expect(path,character.id).toBe(`/assets/portraits/${character.id}.webp`);
        expect(bytes.toString('ascii',0,4),character.id).toBe('RIFF');
        expect(bytes.toString('ascii',8,12),character.id).toBe('WEBP');
      }
    }
    for(const id of ['megumi','eren','killua'])expect(reviewed.has(id)).toBe(true);
  });
  it('mantém os ícones de habilidade existentes válidos no catálogo expandido',()=>{
    const manifest=JSON.parse(readFileSync(new URL('assets/skills/manifest.json',root),'utf8')) as {count:number;skills:{id:string;character:string;path:string;sheet:string;row:number;column:number;crop:{x:number;y:number;width:number;height:number}}[]};
    expect(manifest.count).toBe(manifest.skills.length);
    expect(new Set(manifest.skills.map(s=>`${s.character}/${s.id}`)).size).toBe(manifest.skills.length);
    const known=new Set(characters.flatMap(c=>c.skills.map(s=>`${c.id}/${s.id}`)));
    for(const skill of manifest.skills)expect(known.has(`${skill.character}/${skill.id}`),`${skill.character}/${skill.id}`).toBe(true);
    for(const skill of manifest.skills){
      expect(existsSync(new URL(skill.path.slice(1),root)),skill.path).toBe(true);
      expect(skill.path).toBe(skillArtPath(skill.character,skill.id));
    }
    expect(manifest.count).toBe(characters.length*3);
    expect(manifest.skills.every(skill=>skill.path.startsWith(`/assets/skills/${skill.character}/`))).toBe(true);
    const pngs=manifest.skills.map(skill=>readFileSync(new URL(skill.path.slice(1),root)));
    const pngHash=pngs.map(file=>createHash('sha256').update(file).digest('hex'));
    expect(new Set(pngHash).size).toBe(manifest.count);
    expect(pngs.every(png=>png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))).toBe(true);
    expect(pngs.every(png=>png.readUInt32BE(16)===128&&png.readUInt32BE(20)===128&&png[25]===6)).toBe(true);
    expect(manifest.skills.every(skill=>skill.sheet.startsWith('/assets/sheets/skills/pages/')&&skill.crop.width===128&&skill.crop.height===128)).toBe(true);
    const sheetManifest=JSON.parse(readFileSync(new URL('assets/sheets/skills/manifest.json',root),'utf8')) as {count:number;pages:{sourceSheet:string;sheet:string;resolution:number[];columns:number;rows:number;cell:number[];icons:unknown[]}[]};
    expect(sheetManifest.count).toBe(characters.length*3);
    expect(sheetManifest.pages).toHaveLength(characters.length);
    expect(sheetManifest.pages.every(page=>page.resolution[0]===512&&page.resolution[1]===176&&page.columns===3&&page.rows===1&&page.cell[0]===160&&page.cell[1]===160&&page.icons.length===3&&existsSync(new URL(page.sourceSheet.slice(1),root)))).toBe(true);
    const expanded=manifest.skills.slice(300) as (typeof manifest.skills[number]&{artMethod:string})[];
    expect(expanded.filter(skill=>skill.artMethod==='AI sheet')).toHaveLength(447);
    expect(expanded.filter(skill=>skill.artMethod==='object illustration')).toHaveLength(3);
    expect(expanded.every(skill=>!('placeholder' in skill)&&['AI sheet','object illustration'].includes(skill.artMethod))).toBe(true);
    expect(sheetManifest.pages.slice(100).every(page=>!('placeholder' in page))).toBe(true);
    for(const character of characters.slice(100).filter(character=>character.id!=='mario')){
      expect(existsSync(new URL(`../assets/ai-source/skills/${character.id}.png`,root)),character.id).toBe(true);
    }
  });
  it('mantém ícones universais próprios para todos os 14 estados e remove glifos emoji antigos',()=>{
    expect(Object.keys(statuses)).toHaveLength(14);
    for(const [id,status] of Object.entries(statuses)){expect(status).toMatchObject({name:expect.any(String),description:expect.any(String)});expect((status as {glyph?:string}).glyph,`${id} ainda usa glifo`).toBeUndefined();}
  });
  it('exporta folha transparente de estados e auxiliares com manifesto de recorte',()=>{
    const states=JSON.parse(readFileSync(new URL('assets/sheets/statuses/manifest.json',root),'utf8')) as {count:number;sourceSheet:string;resolution:number[];columns:number;rows:number;cell:number[];items:{id:string;name:string;path:string;row:number;column:number;crop:{width:number;height:number}}[]};
    const ui=JSON.parse(readFileSync(new URL('assets/sheets/ui/manifest.json',root),'utf8')) as {count:number;sourceSheet:string;resolution:number[];columns:number;rows:number;cell:number[];items:{id:string;name:string;path:string;row:number;column:number;crop:{width:number;height:number}}[]};
    expect(states).toMatchObject({count:14,resolution:[680,680],columns:4,rows:4,cell:[160,160]});
    expect(ui).toMatchObject({count:16,resolution:[680,680],columns:4,rows:4,cell:[160,160]});
    for(const manifest of [states,ui])expect(existsSync(new URL(manifest.sourceSheet.slice(1),root))).toBe(true);
    expect(states.items.map(item=>item.name)).toEqual(Object.values(statuses).map(status=>status.name));
    expect(states.items.every((item,index)=>item.row===Math.floor(index/4)&&item.column===index%4)).toBe(true);
    expect(ui.items.map(item=>item.name)).toEqual(['Habilidade pronta','Cooldown','Carregando','Preparando','Executando','Buff','Debuff','Ação acelerada','Ação atrasada','Interrupção','Histórico','Inspeção','Ajuda','Domínio','Vitória','Derrota']);
    for(const manifest of [states,ui])for(const item of manifest.items){
      const png=readFileSync(new URL(item.path.slice(1),root));
      expect(png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])),item.id).toBe(true);
      expect(png.readUInt32BE(16)===128&&png.readUInt32BE(20)===128&&png[25]===6,item.id).toBe(true);
      expect(item.crop).toMatchObject({width:128,height:128});
    }
  });
  it('inclui as faixas originais, arena e atlas reutilizáveis no build offline',()=>{
    for(const file of ['assets/audio/harmony.ogg','assets/audio/rhythm.ogg','assets/audio/pulse.ogg','assets/audio/lead.ogg','assets/vfx/arena.webp','assets/vfx/familias/fogo.webp','assets/vfx/familias/golpe_pesado.webp','assets/vfx/familias/feixe_pesado.webp'])expect(existsSync(new URL(file,root)),file).toBe(true);
  });
  it('identifica queimadura como efeito de fogo',()=>{
    const battle=createBattle(['sasuke','goku','gojo'],['pikachu','hulk','raven'],42);
    const event:BattleEvent={id:1,time:1,kind:'skill',source:'player-0',skill:1,label:'Amaterasu',visual:'psychic'};
    expect(familyOf(event,battle)).toBe('fire');
  });
});
