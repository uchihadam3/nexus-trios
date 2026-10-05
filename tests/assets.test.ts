import { existsSync,readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { describe,it,expect } from 'vitest';
import { characters } from '../src/data/characters';
import { familyOf } from '../src/presentation/director';
import { createBattle } from '../src/engine/battle';
import type { BattleEvent } from '../src/engine/types';
import { statuses } from '../src/data/statuses';
import { skillArtPath } from '../src/data/skill-art';

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
  it('usa os 20 retratos originais enviados para os personagens correspondentes',()=>{
    const portraits:Record<string,string>={
      kaiba:'/assets/portraits/kaiba.webp',yugi:'/assets/portraits/yugi.jpg',kaneki:'/assets/portraits/kaneki.webp',jinwoo:'/assets/portraits/jinwoo.jpg',
      yor:'/assets/portraits/yor.png',loid:'/assets/portraits/loid.webp',anya:'/assets/portraits/anya.jpg',frieren:'/assets/portraits/frieren.webp',
      makima:'/assets/portraits/makima.jpg',power:'/assets/portraits/power.jpg',denji:'/assets/portraits/denji.jpg',giorno:'/assets/portraits/giorno.jpg',
      dio:'/assets/portraits/dio.webp',jotaro:'/assets/portraits/jotaro.webp',guts:'/assets/portraits/guts.jpg',griffith:'/assets/portraits/griffith.jpg',
      roy:'/assets/portraits/roy.png',alphonse:'/assets/portraits/alphonse.jpg',edward:'/assets/portraits/edward.webp',kurapika:'/assets/portraits/kurapika.webp',
    };
    for(const [id,path] of Object.entries(portraits)){
      expect(characters.find(character=>character.id===id)?.portrait,`retrato de ${id}`).toBe(path);
      expect(existsSync(new URL(path.slice(1),root)),path).toBe(true);
      expect(existsSync(new URL(`assets/portraits/placeholder-${id}.svg`,root)),`placeholder de ${id}`).toBe(false);
    }
  });
  it('usa os 20 retratos recém-enviados para os personagens correspondentes',()=>{
    const portraits:Record<string,string>={
      killua:'/assets/portraits/killua.png',gon:'/assets/portraits/gon.jpg',levi:'/assets/portraits/levi.jpeg',hisoka:'/assets/portraits/hisoka.webp',
      mikasa:'/assets/portraits/mikasa.png',eren:'/assets/portraits/eren.webp',kenpachi:'/assets/portraits/kenpachi.png',aizen:'/assets/portraits/aizen.webp',
      rukia:'/assets/portraits/rukia.jpg',ichigo:'/assets/portraits/ichigo.png',sukuna:'/assets/portraits/sukuna.jpg',nobara:'/assets/portraits/nobara.webp',
      megumi:'/assets/portraits/megumi.jpg',yuji:'/assets/portraits/yuji.jpg',muzan:'/assets/portraits/muzan.jpg',inosuke:'/assets/portraits/inosuke.jpg',
      zenitsu:'/assets/portraits/zenitsu.jpeg',nezuko:'/assets/portraits/nezuko.jpg',tanjiro:'/assets/portraits/tanjiro.webp',sakura:'/assets/portraits/sakura.jpg',
    };
    for(const [id,path] of Object.entries(portraits)){
      expect(characters.find(character=>character.id===id)?.portrait,`retrato de ${id}`).toBe(path);
      expect(existsSync(new URL(path.slice(1),root)),path).toBe(true);
      expect(existsSync(new URL(`assets/portraits/placeholder-${id}.svg`,root)),`placeholder de ${id}`).toBe(false);
    }
  });
  it('usa os cinco retratos de Naruto e Dragon Ball enviados depois',()=>{
    const portraits:Record<string,string>={itachi:'/assets/portraits/itachi.jpg',kakashi:'/assets/portraits/kakashi.jpg',frieza:'/assets/portraits/frieza.jpeg',piccolo:'/assets/portraits/piccolo.jpg',gohan:'/assets/portraits/gohan.jpg'};
    for(const [id,path] of Object.entries(portraits)){
      expect(characters.find(character=>character.id===id)?.portrait,`retrato de ${id}`).toBe(path);
      expect(existsSync(new URL(path.slice(1),root)),path).toBe(true);
      expect(existsSync(new URL(`assets/portraits/placeholder-${id}.svg`,root)),`placeholder de ${id}`).toBe(false);
    }
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
    expect(manifest.count).toBe(300);
    expect(manifest.skills.every(skill=>skill.path.startsWith(`/assets/skills/${skill.character}/`))).toBe(true);
    const pngs=manifest.skills.map(skill=>readFileSync(new URL(skill.path.slice(1),root)));
    const pngHash=pngs.map(file=>createHash('sha256').update(file).digest('hex'));
    expect(new Set(pngHash).size).toBe(manifest.count);
    expect(pngs.every(png=>png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))).toBe(true);
    expect(pngs.every(png=>png.readUInt32BE(16)===128&&png.readUInt32BE(20)===128&&png[25]===6)).toBe(true);
    expect(manifest.skills.every(skill=>skill.sheet.startsWith('/assets/sheets/skills/pages/')&&skill.crop.width===128&&skill.crop.height===128)).toBe(true);
    const sheetManifest=JSON.parse(readFileSync(new URL('assets/sheets/skills/manifest.json',root),'utf8')) as {count:number;pages:{sourceSheet:string;resolution:number[];columns:number;rows:number;cell:number[];icons:unknown[]}[]};
    expect(sheetManifest.count).toBe(300);
    expect(sheetManifest.pages).toHaveLength(100);
    expect(sheetManifest.pages.every(page=>page.resolution[0]===512&&page.resolution[1]===176&&page.columns===3&&page.rows===1&&page.cell[0]===160&&page.cell[1]===160&&page.icons.length===3&&existsSync(new URL(`../${page.sourceSheet}`,root)))).toBe(true);
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
    for(const manifest of [states,ui])expect(existsSync(new URL(`../${manifest.sourceSheet}`,root))).toBe(true);
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
  it('inclui as faixas originais longas, arena e atlas de fogo/impacto grandioso no build offline',()=>{
    for(const file of ['assets/audio/harmony.ogg','assets/audio/rhythm.ogg','assets/audio/pulse.ogg','assets/audio/lead.ogg','assets/vfx/arena.webp','assets/vfx/fire.webp','assets/vfx/grand.webp'])expect(existsSync(new URL(file,root)),file).toBe(true);
  });
  it('identifica queimadura como efeito de fogo',()=>{
    const battle=createBattle(['sasuke','goku','gojo'],['pikachu','hulk','raven'],42);
    const event:BattleEvent={id:1,time:1,kind:'skill',source:'player-0',skill:1,label:'Amaterasu',visual:'psychic'};
    expect(familyOf(event,battle)).toBe('fire');
  });
});
