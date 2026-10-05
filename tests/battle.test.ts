import { describe,it,expect } from 'vitest';
import { characters,byId } from '../src/data/characters';
import { createBattle,stepBattle,simulate,applyEffects,resolve,updateDominion,intensity,targets } from '../src/engine/battle';
import { generateCampaign,newDraft,pickDraft,skipDraft,validateCampaignUniqueness } from '../src/engine/campaign';
import { shuffle } from '../src/engine/random';
import type { Effect,Target } from '../src/engine/types';
const player=['goku','pikachu','captain'],enemy=['vegeta','raven','hulk'];
describe('Catálogo e seleção',()=>{
 it('100 fichas válidas com exatamente 3 habilidades e Flash mais rápido',()=>{expect(characters).toHaveLength(100);expect(new Set(characters.map(c=>c.id)).size).toBe(100);expect(characters.every(c=>typeof c.intelligence==='number'&&c.intelligence>=0&&c.intelligence<=100)).toBe(true);expect(byId.batman.intelligence).toBeGreaterThan(byId.hulk.intelligence!);for(const c of characters){expect(c.skills).toHaveLength(3);expect(c.hp).toBeGreaterThan(0);for(const s of c.skills){expect(s.charge.length).toBeGreaterThan(0);expect(s.effects.length).toBeGreaterThan(0);}}expect([...characters].sort((a,b)=>a.interval-b.interval)[0].id).toBe('flash');});
 it('três pulos, sem repetição imediata e sem duplicar integrantes',()=>{let d=newDraft(124);for(let i=0;i<3;i++){const old=d.candidates;d=skipDraft(d);expect(d.skips).toBe(2-i);expect(d.candidates.some(x=>old.includes(x))).toBe(false);}expect(skipDraft(d)).toEqual(d);for(let i=0;i<3;i++){d=pickDraft(d,d.candidates[0]);expect(d.candidates.some(x=>d.team.includes(x))).toBe(false);}expect(new Set(d.team).size).toBe(3);expect(d.candidates).toHaveLength(0);});
 it('gera campanha determinística, progressiva e independente do jogador',()=>{const a=generateCampaign(765,player);expect(a).toEqual(generateCampaign(765,player));expect(a).toHaveLength(10);expect(a[9].scale).toBeGreaterThan(a[0].scale);expect(a[8].power).toBeGreaterThan(a[0].power);expect(validateCampaignUniqueness({team:player,encounters:a}).valid).toBe(true);for(const e of a)expect(new Set(e.team).size).toBe(3);});
});
 it('gera mil jornadas sem repetir jogador nem inimigos, em várias seeds e trios',()=>{
  const presets=[['batman','pikachu','gojo'],['goku','vegeta','naruto'],['superman','thor','hulk'],['light','spiderman','raven']];
  const rng={rng:0x91a4};
  for(let seed=1;seed<=1000;seed++){
   const team=seed%5===0?shuffle(characters.map(c=>c.id),rng).slice(0,3):presets[seed%presets.length];
   const first=generateCampaign(seed,team);
   const audit=validateCampaignUniqueness({team,encounters:first});
   expect(audit).toEqual({valid:true,errors:[]});
   const enemies=first.flatMap(e=>e.team);
   expect(enemies).toHaveLength(30);
   expect(new Set(enemies).size).toBe(30);
   for(const id of team)expect(enemies).not.toContain(id);
   for(const encounter of first)expect(new Set(encounter.team).size).toBe(3);
  }
 });
 it('audita explicitamente uma repetição entre encontros como inválida',()=>{
  const encounters=generateCampaign(44,player).map(e=>({...e,team:[...e.team]}));
  encounters[1].team[0]=encounters[0].team[0];
  expect(validateCampaignUniqueness({team:player,encounters}).valid).toBe(false);
 });
describe('Motor independente',()=>{
 it('seleciona pelo contexto da habilidade sem depender da posição dos personagens',()=>{
  const original=createBattle(['light','pikachu','wolverine'],['flash','hulk','batman'],0x8321);
  const light=original.fighters[0],pika=original.fighters[1],wolverine=original.fighters[2];
  const flash=original.fighters[3],hulk=original.fighters[4],batman=original.fighters[5];
  hulk.hp=hulk.maxHp*.38;flash.statuses.push({id:'exposed',remaining:6,intensity:.4,source:pika.uid});
  light.investigation[flash.uid]=35;light.investigation[batman.uid]=78;
  flash.cast={skill:0,elapsed:3.2,duration:4,targets:[pika.uid]};
  batman.cast={skill:0,elapsed:.5,duration:4,targets:[light.uid]};
  wolverine.hp=wolverine.maxHp*.9;light.hp=light.maxHp*.43;pika.hp=pika.maxHp*.76;
  const permuted=structuredClone(original);permuted.fighters.reverse();
  const pick=(battle:typeof original,uid:string,rule:Parameters<typeof targets>[2],effects:Parameters<typeof targets>[3]=[])=>{
   const actor=battle.fighters.find(f=>f.uid===uid)!;return targets(battle,actor,rule,effects)[0]?.characterId;
  };
  const cases:[string,Target,Effect[]][]=[
   [pika.uid,'enemyWeak',byId.pikachu.basic.effects],
   [pika.uid,'enemyCast',[{kind:'interrupt',mode:'cancel',value:1}]],
   [light.uid,'investigated',[{kind:'investigate',value:1}]],
   [wolverine.uid,'allyWeak',[{kind:'heal',value:180}]],
  ];
  for(const [actor,rule,effects] of cases)expect(pick(permuted,actor,rule,effects)).toBe(pick(original,actor,rule,effects));
  expect(pick(original,pika.uid,'enemyCast',[{kind:'interrupt',mode:'cancel',value:1}])).toBe('flash');
  flash.cast=null;batman.cast=null;
  expect(pick(original,light.uid,'investigated',[{kind:'investigate',value:1}])).toBe('batman');
  expect(original.targetLog?.some(d=>d.actor===pika.uid&&d.reasons.some(r=>r.includes('preparação ativa')))).toBe(true);
 });
 it('pontua habilidades prontas com motivos e Inteligência do personagem',()=>{
  const battle=createBattle(player,enemy,0xabc);
  for(const fighter of battle.fighters)fighter.skills.forEach(state=>{state.charge=100;state.readySince=0;});
  for(let i=0;i<40&&!battle.decisionLog?.length;i++)stepBattle(battle);
  expect(battle.decisionLog?.length).toBeGreaterThan(0);
  const decision=battle.decisionLog![0],character=byId[battle.fighters.find(f=>f.uid===decision.actor)!.characterId];
  expect(decision.intelligence).toBe(character.intelligence);
  expect(decision.candidates.length).toBeGreaterThan(0);
  expect(decision.candidates[0].score).toBeGreaterThanOrEqual(decision.candidates.at(-1)!.score);
  expect(decision.candidates[0].reasons.length).toBeGreaterThan(0);
 });
 it('intenção de cura escolhe necessidade real e nunca apenas o primeiro aliado',()=>{
  const battle=createBattle(['wolverine','light','pikachu'],enemy,0x55),wolverine=battle.fighters[0],light=battle.fighters[1];
  light.hp=light.maxHp*.28;
  expect(targets(battle,wolverine,'allyWeak',[{kind:'heal',value:150}])[0]?.characterId).toBe('light');
  const reversed=structuredClone(battle);reversed.fighters.reverse();
  const actor=reversed.fighters.find(f=>f.uid===wolverine.uid)!;
  expect(targets(reversed,actor,'allyWeak',[{kind:'heal',value:150}])[0]?.characterId).toBe('light');
 });
 it('é reprodutível e não depende da velocidade de apresentação',()=>{const one=createBattle(player,enemy,42),two=createBattle(player,enemy,42);while(!one.finished)stepBattle(one);while(!two.finished){stepBattle(two);stepBattle(two);}expect(two).toEqual(one);expect(one).toEqual(simulate(player,enemy,42));});
 it('retoma um snapshot JSON com o mesmo resultado',()=>{const b=createBattle(player,enemy,19);for(let i=0;i<117;i++)stepBattle(b);const resumed=JSON.parse(JSON.stringify(b));while(!b.finished)stepBattle(b);while(!resumed.finished)stepBattle(resumed);expect(resumed).toEqual(b);});
 it('não gera Domínio com cura cheia e escudo não usado',()=>{const b=createBattle(player,enemy,9),f=b.fighters[0];applyEffects(b,f,[f],[{kind:'heal',value:500},{kind:'shield',value:300}]);updateDominion(b);expect(b.dominion).toBe(0);expect(f.stats.healing).toBe(0);expect(f.stats.protection).toBe(0);});
 it('atribui proteção somente ao dano realmente absorvido',()=>{const b=createBattle(player,enemy,2),source=b.fighters[0],target=b.fighters[1],attacker=b.fighters[3];applyEffects(b,source,[target],[{kind:'shield',value:300}]);applyEffects(b,attacker,[target],[{kind:'damage',value:100}]);expect(target.hp).toBe(target.maxHp);expect(source.stats.protection).toBe(100);});
 it('interrompe, atrasa, reduz e respeita proteção da preparação',()=>{const b=createBattle(player,enemy,2),a=b.fighters[0],t=b.fighters[3];t.cast={skill:0,elapsed:2,duration:4,targets:[a.uid]};applyEffects(b,a,[t],[{kind:'interrupt',mode:'delay',value:1}]);expect(t.cast?.elapsed).toBe(1);applyEffects(b,a,[t],[{kind:'interrupt',mode:'reduce',value:.5}]);expect(t.cast?.elapsed).toBe(.5);applyEffects(b,t,[t],[{kind:'status',status:'protected',value:.5,duration:5}]);applyEffects(b,a,[t],[{kind:'interrupt',mode:'cancel',value:1}]);expect(t.cast).not.toBe(null);t.statuses=[];applyEffects(b,a,[t],[{kind:'interrupt',mode:'cancel',value:1}]);expect(t.cast).toBe(null);expect(t.skills[0].charge).toBe(25);expect(a.stats.interrupts).toBe(3);});
 it('Death Note exige investigação, finaliza humanos e expõe incompatíveis',()=>{const b=createBattle(['light','pikachu','captain'],['batman','goku','thanos'],1),light=b.fighters[0],human=b.fighters[3],alien=b.fighters[4];applyEffects(b,light,[human],[{kind:'deathnote',value:100}]);expect(human.hp).toBe(human.maxHp);light.investigation[human.uid]=100;applyEffects(b,light,[human],[{kind:'deathnote',value:100}]);expect(human.hp).toBe(0);light.investigation[alien.uid]=100;applyEffects(b,light,[alien],[{kind:'deathnote',value:100}]);expect(alien.hp).toBeGreaterThan(0);expect(intensity(alien,'exposed')).toBe(.55);expect(light.investigation[alien.uid]).toBe(0);});
 it('cooldown bloqueia carga, e habilidade pronta espera alvo ferido',()=>{const b=createBattle(['deadpool','flash','captain'],enemy,3),d=b.fighters[0];d.skills[2].charge=100;d.skills[0].cooldown=10;for(let i=0;i<5;i++)stepBattle(b);expect(d.skills[2].charge).toBe(100);expect(d.skills[0].charge).toBe(0);d.hp=d.maxHp*.5;stepBattle(b);expect(d.skills[2].cooldown).toBeGreaterThan(0);expect(d.hp).toBeGreaterThan(d.maxHp*.5);});
 it('paralisia congela ação e preparação e expira',()=>{const b=createBattle(player,enemy,8),f=b.fighters[0];f.cast={skill:0,elapsed:1,duration:3,targets:[b.fighters[3].uid]};applyEffects(b,b.fighters[3],[f],[{kind:'status',status:'paralyzed',value:1,duration:1}]);for(let i=0;i<5;i++)stepBattle(b);expect(f.cast?.elapsed).toBe(1);for(let i=0;i<8;i++)stepBattle(b);expect(f.cast!.elapsed).toBeGreaterThan(1);});
 it('encerra imediatamente por incapacitação',()=>{const b=createBattle(player,enemy,8);b.fighters.filter(f=>f.side==='enemy').forEach(f=>f.hp=0);resolve(b);expect(b.finished).toBe(true);expect(b.winner).toBe('player');expect(b.time).toBe(0);});
 it('chega a 120 segundos e vence por Domínio',()=>{const b=createBattle(player,enemy,8);for(const f of b.fighters){f.maxHp=1e8;f.hp=1e8;if(f.side==='enemy')f.hp*=.8;}while(!b.finished)stepBattle(b);expect(b.time).toBe(120);expect(b.reason).toBe('Vantagem de Domínio');expect(b.winner).toBe('player');});
 it('desempata por Condição total quando o Domínio está empatado',()=>{const b=createBattle(player,enemy,8);b.time=120;b.dominion=0;b.fighters[0].hp-=10;resolve(b);const p=b.fighters.slice(0,3).reduce((s,f)=>s+f.hp,0),e=b.fighters.slice(3).reduce((s,f)=>s+f.hp,0);expect(b.winner).toBe(p>e?'player':'enemy');expect(b.reason).toContain('Condição');});
 it('mantém invariantes em 100 confrontos aleatórios',()=>{const rng={rng:343};let shortest=120,longest=0;for(let i=0;i<100;i++){const a=shuffle(characters.map(c=>c.id),rng).slice(0,3),z=shuffle(characters.map(c=>c.id),rng).slice(0,3);const b=simulate(a,z,i);shortest=Math.min(shortest,b.time);longest=Math.max(longest,b.time);expect(b.finished).toBe(true);expect(b.winner).not.toBe(null);expect(Number.isFinite(b.dominion)).toBe(true);expect(b.time).toBeLessThanOrEqual(120);for(const f of b.fighters){expect(f.hp).toBeGreaterThanOrEqual(0);expect(f.hp).toBeLessThanOrEqual(f.maxHp);for(const s of f.skills){expect(s.charge).toBeGreaterThanOrEqual(0);expect(s.charge).toBeLessThanOrEqual(100);}}}expect(shortest).toBeLessThan(120);expect(longest).toBeGreaterThan(25);});
 it('permite sinergia de controle alimentar Light',()=>{const b=createBattle(['light','pikachu','captain'],enemy,8),light=b.fighters[0],pika=b.fighters[1];applyEffects(b,pika,[b.fighters[3]],[{kind:'status',status:'paralyzed',value:1,duration:2}]);expect(light.skills[0].charge).toBeGreaterThan(0);expect(Object.values(light.investigation).reduce((n,v)=>n+v,0)).toBeGreaterThan(0);expect(b.events.some(e=>e.kind==='synergy'&&e.target===light.uid)).toBe(true);});
 it('emite causa/origem da carga e sinaliza avanços ou atrasos de ação',()=>{const b=createBattle(['sasuke','pikachu','goku'],enemy,81),sasuke=b.fighters[0],pika=b.fighters[1];applyEffects(b,pika,[b.fighters[3]],[{kind:'status',status:'paralyzed',value:1,duration:2}]);const charge=b.events.find(e=>e.kind==='charge'&&e.target===sasuke.uid&&e.skill===2);expect(charge).toMatchObject({source:pika.uid,label:'status'});const before=sasuke.action;applyEffects(b,pika,[sasuke],[{kind:'shift',value:.2}]);expect(b.events.at(-1)).toMatchObject({kind:'tempo',source:pika.uid,target:sasuke.uid,value:.2});expect(sasuke.action).toBeGreaterThan(before);});
 it('todas as fichas participam sem condições inválidas',()=>{for(const c of characters){const allies=characters.filter(x=>x.id!==c.id).slice(0,2).map(x=>x.id);const b=simulate([c.id,...allies],['thanos','raven','flash'],50);expect(b.finished).toBe(true);expect(byId[c.id].portrait).toContain(c.id);}});
});
