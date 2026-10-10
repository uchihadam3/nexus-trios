import { FAMILIA_DA_INVOCACAO } from '../src/presentation/vfx-atribuicao';
import { FAMILIAS_DO_JEITO } from '../src/presentation/jeito-efeito';
import { describe,expect,it } from 'vitest';
import { readFileSync,readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { SOM_DA_FAMILIA,TODOS_OS_SONS,type Manifesto } from '../src/audio/cues';
import { FAMILIAS,VFX_FAMILIES,folhasUsadas,hsl,profileFor } from '../src/presentation/vfxProfiles';
import { characters } from '../src/data/characters';
import { FAIXAS,LACO_DA_MUSICA,faixaDaLuta,posicaoNoLaco } from '../src/lib/audio';

const root=process.cwd();
const familias=JSON.parse(readFileSync(resolve(root,'public/assets/vfx/familias/manifest.json'),'utf8')) as Record<string,{quadros:number;grade:[number,number];tamanho:[number,number];laco:boolean;bytes:number}>;
const sfx=JSON.parse(readFileSync(resolve(root,'public/assets/audio/sfx/manifest.json'),'utf8')) as Manifesto;
const musica=JSON.parse(readFileSync(resolve(root,'public/assets/audio/musica.json'),'utf8')) as {bpm:number;compassos:number;segundos:number;secoes:{nome:string;inicio:number}[];laco:{inicio:number;fim:number};camadas:Record<string,{arquivo:string;mp3?:string;bytes:number;rmsDb:number}>};

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
      // as faixas (512 × 96) são as maiores; o resto fica bem abaixo
      expect(f.bytes,`${nome} pequeno o bastante para celular`).toBeLessThan(f.tamanho[0]>200?240_000:200_000);
      bytes+=f.bytes;decodificado+=f.tamanho[0]*f.tamanho[1]*12*4;
    }
    // só as folhas das famílias da luta são baixadas; o total é o catálogo inteiro (com os jeitos de bater)
    // cresce com as habilidades desenhadas para cada personagem (Madara, Kakashi, Cloud…); a luta baixa
    // só as folhas de quem está nela, então o catálogo inteiro não pesa no celular
    expect(bytes).toBeLessThan(28_000_000);
    // nenhuma folha decodificada passa de ~4,5 MB na memória (a maior é a faixa de 512 × 96 × 12)
    expect(decodificado/Object.keys(familias).length).toBeLessThan(2_000_000);
    expect(readdirSync(resolve(root,'public/assets/vfx')).filter(x=>x.endsWith('.webp'))).toEqual(['arena.webp']);
  });
  it('maps every basic and skill to one of the 150–400 families (signature skills and the own basic attack of each character), all of them used, none dominating',()=>{
    expect(FAMILIAS.length).toBeGreaterThanOrEqual(150);expect(FAMILIAS.length).toBeLessThanOrEqual(400);
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
    // não são de habilidade: as brasas aparecem no lutador caído (ArenaUnit) e a marca de
    // Provocado por cima de quem recebe o Status, seja qual for o golpe (BattleEffects)
    // e o espelho, os espinhos e as gotas de sangue sobre quem devolve o golpe ou rouba a Vida;
    // o renascer é o fogo de quem volta sozinho (o beat de Renasceu); a esfera e a terra são as reservas
    // dos golpes de energia e de pedra sem família própria (vfxProfiles: ícone 'beam' e nomes de terra)
    const SO_NA_ARENA=new Set(['esfera','terra','renascer','brasas_renascendo','provocar','reflexo','espinhos','vampirismo','dissipar','sono','cegueira','esquiva','ultima_resistencia','copia',...FAMILIAS_DO_JEITO,...Object.values(FAMILIA_DA_INVOCACAO)]);
    for(const f of FAMILIAS)if(!SO_NA_ARENA.has(f))expect(uso.get(f)??0,`${f} usada`).toBeGreaterThan(0);
    for(const [f,n] of uso)expect(n/total,`${f} não domina`).toBeLessThan(.16);
  });
  it('gives the famous skills the effect and colour people recognise',()=>{
    expect(profileFor('goku',0)?.family).toBe('kamehameha');
    const [h]=hsl(profileFor('goku',0)!.color);expect(h).toBeGreaterThan(185);expect(h).toBeLessThan(215);
    expect(profileFor('superman',0)?.family).toBe('visao_de_calor');expect(hsl(profileFor('superman',0)!.color)[0]).toBeLessThan(15);
    expect(profileFor('pikachu',0)?.family).toBe('raio');
    expect(profileFor('spiderman',0)?.family).toBe('teia');
    expect(profileFor('light',2)?.family).toBe('death_note');
    expect(profileFor('naruto',1)?.family).toBe('rasengan');
    expect(profileFor('gojo',0)?.family).toBe('atracao');expect(profileFor('gojo',1)?.family).toBe('repulsao');expect(profileFor('gojo',2)?.family).toBe('dominio');
    expect(profileFor('beerus',0)?.family).toBe('toque_da_destruicao');expect(profileFor('sasuke',0)?.family).toBe('chidori');
    expect(profileFor('saitama',2)?.family).toBe('soco_serio');expect(profileFor('itachi',2)?.family).toBe('susanoo');
    expect(profileFor('ichigo',0)?.family).toBe('corte_de_energia');
    expect(profileFor('charizard',0)?.family).toBe('lanca_chamas');
    // a mesma família muda de cor com o personagem
    expect(profileFor('vegeta',0)?.family).toBe('kamehameha');expect(profileFor('vegeta',0)?.color).not.toBe(profileFor('goku',0)?.color);
  });
  it('has a sound family for every visual family, with 4 MP3 versions per sound, within budget',()=>{
    expect(sfx.versoes).toBe(4);
    expect(Object.keys(sfx.sons).sort()).toEqual([...new Set(TODOS_OS_SONS)].sort());
    for(const familia of FAMILIAS){
      const som=SOM_DA_FAMILIA[familia];expect(som,familia).toBeDefined();
      for(const nome of [som.impacto,som.saida,som.preparo].filter(Boolean))expect(sfx.sons[nome!],`${familia} → ${nome}`).toBeDefined();
    }
    let bytes=0;
    for(const [nome,som] of Object.entries(sfx.sons)){
      const data=readFileSync(resolve(root,'public/assets/audio/sfx',som.arquivo));bytes+=data.length;
      // MP3: cabeçalho ID3 ou quadro de sincronia
      expect(data.subarray(0,3).toString('ascii')==='ID3'||(data[0]===0xff&&(data[1]!&0xe0)===0xe0),nome).toBe(true);
      expect(som.versoes,nome).toHaveLength(4);expect(som.duracoes,nome).toHaveLength(4);
      for(let v=1;v<4;v++)expect(som.versoes[v]!,nome).toBeGreaterThan(som.versoes[v-1]!+som.duracoes[v-1]!);
      expect(som.descricao.length,nome).toBeGreaterThan(3);
    }
    // a luta baixa só os sons das famílias dos seis lutadores (precarregarLuta)
    // as mecânicas novas (reviver, provocar, refletir, status novos…) trazem sons próprios; a luta continua baixando só os dos seis lutadores
    expect(bytes).toBeLessThan(21_000_000);
    expect(readdirSync(resolve(root,'public/assets/audio/sfx')).filter(x=>x.endsWith('.wav'))).toEqual([]);
  });
  it('a música começa na Intro e, depois do fim, volta ao Encontro',()=>{
    expect(posicaoNoLaco(0,10,146)).toBeCloseTo(10);
    expect(posicaoNoLaco(0,146.5,146)).toBeCloseTo(LACO_DA_MUSICA+.5,3);
    expect(posicaoNoLaco(100,100,146)).toBeGreaterThanOrEqual(LACO_DA_MUSICA);
  });
  it('keeps the background music in three looping layers of the same piece',()=>{
    expect(Object.keys(musica.camadas).sort()).toEqual(['musica-base','musica-pulso','musica-tema']);
    expect(musica.segundos).toBeCloseTo(musica.compassos*4*60/musica.bpm,1);
    // a música de batalha cresce em fases e faz laço a partir do Encontro (nunca volta à Intro)
    expect(musica.secoes.map(x=>x.nome)).toEqual(['Intro','Encontro','Choque','Ponte','Clímax','Virada']);
    expect(musica.segundos).toBeGreaterThan(120);expect(musica.segundos).toBeLessThan(160);
    expect(musica.laco.inicio).toBeCloseTo(LACO_DA_MUSICA,2);expect(musica.secoes[1]!.inicio).toBeCloseTo(LACO_DA_MUSICA,2);
    let bytes=0;
    for(const camada of Object.values(musica.camadas)){const data=readFileSync(resolve(root,'public/assets/audio',camada.arquivo));bytes+=data.length;expect(data.subarray(0,4).toString('ascii')).toBe('OggS');}
    // a mesma camada em MP3 para quem não decodifica Ogg (iPhone/Safari): sem ela, tocaria a música sintetizada antiga
    for(const camada of Object.values(musica.camadas)){const mp3=readFileSync(resolve(root,'public/assets/audio',camada.arquivo.replace(/\.ogg$/,'.mp3')));const cab=mp3.subarray(0,3);expect(cab.toString('ascii')==='ID3'||(cab[0]===0xff&&(cab[1]!&0xe0)===0xe0)).toBe(true);expect(mp3.length).toBeLessThan(1_800_000);}
    expect(bytes).toBeLessThan(4_200_000);
    // a base é a mais presente; pulso e tema ficam por baixo
    expect(musica.camadas['musica-base']!.rmsDb).toBeGreaterThan(musica.camadas['musica-tema']!.rmsDb);
  });
  /* Pedido do jogador: a música de agora nas lutas 1–5, uma mais tensa nas 6–9 e uma de chefe na 10. */
  it('troca de música com a jornada: principal (1–5), tensão (6–9), chefe (10)',()=>{
    expect(Array.from({length:10},(_,i)=>faixaDaLuta(i))).toEqual(['principal','principal','principal','principal','principal','tensao','tensao','tensao','tensao','chefe']);
  });
  for(const [faixa,secoes] of [['tensao',['Intro','Perigo','Pressão','Ruptura','Confronto','Retorno']],['chefe',['Aparição','Duelo','Fúria','Desespero','Último golpe','Virada']]] as const){
    it(`a música ${faixa} vem nas mesmas três camadas, em OGG e MP3, com o laço na segunda seção`,()=>{
      const m=JSON.parse(readFileSync(resolve(root,`public/assets/audio/musica-${faixa}.json`),'utf8')) as typeof musica;
      expect(Object.keys(m.camadas).sort()).toEqual(['base','pulso','tema'].map(c=>`musica-${faixa}-${c}`));
      expect(m.secoes.map(x=>x.nome)).toEqual(secoes);
      expect(m.segundos).toBeCloseTo(m.compassos*4*60/m.bpm,1);
      expect(m.segundos).toBeGreaterThan(100);expect(m.segundos).toBeLessThan(160);
      // o jogo volta a música no mesmo ponto que o arquivo diz
      expect(FAIXAS[faixa].laco).toBeCloseTo(m.laco.inicio,2);expect(m.secoes[1]!.inicio).toBeCloseTo(m.laco.inicio,2);
      expect(FAIXAS[faixa].camadas.map(c=>c.split('/').pop())).toEqual(Object.values(m.camadas).map(c=>c.arquivo));
      for(const camada of Object.values(m.camadas)){
        const ogg=readFileSync(resolve(root,'public/assets/audio',camada.arquivo));expect(ogg.subarray(0,4).toString('ascii')).toBe('OggS');expect(ogg.length).toBeLessThan(1_800_000);
        const mp3=readFileSync(resolve(root,'public/assets/audio',camada.mp3!));const cab=mp3.subarray(0,3);expect(cab.toString('ascii')==='ID3'||(cab[0]===0xff&&(cab[1]!&0xe0)===0xe0)).toBe(true);expect(mp3.length).toBeLessThan(1_800_000);
      }
      // o mesmo volume da música principal: trocar de música não pula de volume
      for(const c of ['base','pulso','tema'])expect(Math.abs(m.camadas[`musica-${faixa}-${c}`]!.rmsDb-musica.camadas[`musica-${c}`]!.rmsDb)).toBeLessThan(2.5);
    });
  }
});
