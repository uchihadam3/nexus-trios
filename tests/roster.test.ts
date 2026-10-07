import {describe,it,expect} from 'vitest';
import {characters} from '../src/data/characters';
import {expandedCharacters,rosterDesignQuestions,rosterIdentityReviewGroups} from '../src/data/expanded-roster';
import type {Effect} from '../src/engine/types';

/** O tamanho atual do catálogo. Sobe a cada lote até 250. */
const TOTAL=160;

describe('catálogo competitivo de personagens',()=>{
  /*
   * O tamanho do catálogo é um contrato, e fica declarado num lugar só.
   *
   * O alvo final é 250. A cada lote da expansão este número sobe junto com o
   * roster, e as outras asserções abaixo são derivadas dele — elas cobram
   * unicidade, não um total escrito à mão em cinco arquivos.
   */
  it(`contém ${String(TOTAL)} identidades únicas, 24 preservadas e o restante vindo da expansão`,()=>{
    expect(characters).toHaveLength(TOTAL);
    expect(expandedCharacters).toHaveLength(TOTAL-24);
    expect(new Set(characters.map(c=>c.id)).size).toBe(TOTAL);
    expect(new Set(characters.map(c=>c.name.toLocaleLowerCase())).size).toBe(TOTAL);
    expect(Object.keys(rosterDesignQuestions)).toHaveLength(TOTAL-24);
  });
  it('cada ficha tem ação, traço, três habilidades alcançáveis e compatibilidade explícita',()=>{
    for(const c of characters){
      expect(c.basic.effects.length,`${c.id} ação principal`).toBeGreaterThan(0);
      expect(c.trait.name,`${c.id} traço`).toBeTruthy();
      expect(c.skills,`${c.id} habilidades`).toHaveLength(3);
      expect(typeof c.deathNoteCompatible,`${c.id} compatibilidade Death Note`).toBe('boolean');
      expect(c.vulnerability,`${c.id} vulnerabilidade`).toBeTruthy();
      expect(c.tags.length,`${c.id} tags`).toBeGreaterThan(0);
      for(const s of c.skills){
        expect(s.name,`${c.id}/${s.id} nome`).toBeTruthy();
        expect(s.effects.length,`${c.id}/${s.id} efeitos`).toBeGreaterThan(0);
        expect(s.charge.length,`${c.id}/${s.id} carga`).toBeGreaterThan(0);
        expect(s.cooldown,`${c.id}/${s.id} cooldown`).toBeGreaterThanOrEqual(0);
        expect(s.preparation,`${c.id}/${s.id} preparação`).toBeGreaterThanOrEqual(0);
        expect(s.charge.every(rule=>rule.amount>0&&Number.isFinite(rule.amount)),`${c.id}/${s.id} carga positiva`).toBe(true);
      }
    }
  });
  it('documenta uma pergunta estratégica para cada personagem novo',()=>{
    for(const c of expandedCharacters)expect(rosterDesignQuestions[c.id]?.length,`${c.name} pergunta`).toBeGreaterThan(12);
  });
  it('registra uma revisão humana para cada personagem novo, em exatamente um grupo',()=>{
    const groups=Object.values(rosterIdentityReviewGroups).flat();
    expect(new Set(groups).size).toBe(TOTAL-24);
    expect(new Set(groups)).toEqual(new Set(expandedCharacters.map(c=>c.id)));
  });
  it('implementa as identidades redesenhadas com condições e efeitos legíveis no motor',()=>{
    const get=(id:string)=>expandedCharacters.find(c=>c.id===id)!;
    const has=(effects:Effect[],kind:Effect['kind'])=>effects.some(e=>e.kind===kind);
    const vision=get('vision');
    expect(vision.skills[0].effects.some(e=>e.kind==='status'&&e.status==='protected')).toBe(true);
    expect(has(vision.skills[2].effects,'interrupt')).toBe(true);
    const lantern=get('greenlantern');
    expect(lantern.skills[0].condition).toBe('threatened');
    expect(has(lantern.skills[1].effects,'interrupt')).toBe(true);
    expect(lantern.skills[2].condition).toBe('vulnerable');
    const doom=get('doctordoom');
    expect(doom.skills[0].effects.some(e=>e.kind==='status'&&e.status==='marked')).toBe(true);
    expect(doom.skills[1].preparation).toBeGreaterThan(0);
    expect(doom.skills[2].preparation).toBeGreaterThan(doom.skills[1].preparation);
    expect(doom.skills[2].charge.map(rule=>rule.on)).toContain('status');
    expect(doom.skills[2].charge.map(rule=>rule.on)).toContain('protected');
    const griffith=get('griffith');
    expect(griffith.skills[1].effects.some(e=>e.kind==='shift'&&e.target==='allAllies')).toBe(true);
    expect(griffith.skills[2].effects.some(e=>e.kind==='status'&&e.status==='strengthened'&&e.target==='allAllies')).toBe(true);
    const panther=get('blackpanther');
    expect(panther.trait.on).toBe('received');
    expect(panther.skills[2].target).toBe('enemyWeak');
    expect(panther.skills[2].effects.some(e=>e.kind==='release'&&e.multiplier>0)).toBe(true);
    const surfer=get('silversurfer');
    expect(surfer.skills[1].effects.some(e=>e.kind==='shield'&&e.target==='allAllies')).toBe(true);
    const xavier=get('professorx');
    expect(xavier.basic.effects.some(e=>e.kind==='damage'&&e.value<=10)).toBe(true);
    expect(xavier.skills[2].effects.some(e=>e.kind==='status'&&e.status==='silenced')).toBe(true);
    expect(get('yugi').trait.effects.some(e=>e.kind==='charge')).toBe(true);
    expect(get('kaiba').trait.on).toBe('dealt');
    expect(get('kaiba').skills[2].preparation).toBeGreaterThan(2);
  });
  it('gates invocações finais atrás da construção e descarrega energia realmente armazenada',()=>{
    const get=(id:string)=>expandedCharacters.find(c=>c.id===id)!;
    for(const id of ['yugi','doctordoom']){
      expect(get(id).skills[1].requiresSkills).toContain(0);
      expect(get(id).skills[2].requiresSkills).toEqual([0,1]);
    }
    expect(get('kaiba').skills[1].requiresSkills).toContain(0);
    expect(get('kaiba').skills[2].requiresSkills).toContain(1);
    for(const id of ['blackpanther','captainmarvel']){
      expect(get(id).trait.effects.some(e=>e.kind==='store'&&e.cap>0)).toBe(true);
      expect(get(id).skills[2].condition).toBe('storedEnergy');
      expect(get(id).skills[2].effects.some(e=>e.kind==='release'&&e.multiplier>0)).toBe(true);
    }
  });
  it('não repete exatamente a assinatura de mecânicas entre os kits novos',()=>{
    const fingerprints=expandedCharacters.map(c=>JSON.stringify({basic:c.basic.effects.slice(1).map(e=>e.kind==='status'?`s:${e.status}`:e.kind).sort(),skills:c.skills.map(s=>({charge:s.charge.map(r=>r.on).sort(),target:s.target,condition:s.condition,preparation:s.preparation>0,effects:s.effects.map(e=>e.kind==='status'?`s:${e.status}`:e.kind).sort()}))}));
    /*
     * O guarda anti-clone.
     *
     * Dois personagens com a mesma assinatura de mecânicas são a mesma ficha
     * com outro nome. É a regra que a direção escreveu por extenso: 250 não
     * podem ser 250 skins. Qualquer lote novo que colida aqui falha antes de
     * chegar ao jogo.
     */
    expect(new Set(fingerprints).size).toBe(TOTAL-24);
  });
});
