import { describe,it,expect } from 'vitest';
import { renderToStaticMarkup } from 'react-dom/server';
import { characters } from '../src/data/characters';
import { presentSkill,presentTrait,presentStatus,topicNames,positiveStatuses } from '../src/engine/skill-descriptions';
import { statuses } from '../src/data/statuses';
import { CharacterModal } from '../src/components/CharacterModal';
import { ArenaUnit } from '../src/components/ArenaUnit';
import { applyEffects,createBattle,targets } from '../src/engine/battle';

describe('linguagem pública e o catálogo inteiro',()=>{
  it('renderiza todas as fichas com as três habilidades e dados reais',()=>{
    expect(characters.length).toBeGreaterThanOrEqual(130);
    for(const c of characters){
      const html=renderToStaticMarkup(<CharacterModal character={c} onClose={()=>{}}/>);
      expect(html,c.id).toContain(c.name);
      expect(html,c.id).toContain('Ponto fraco');
      expect(html,c.id).not.toMatch(/NaN|undefined|RETRATO PROVISÓRIO|compatível com a sentença|Condição de uso|Recarga interna|alvo válido|efeito aplicado|MVP 1\.0/);
      expect(presentTrait(c.trait).effects,c.id).toHaveLength(c.trait.effects.length);
      expect(c.vulnerability.trim().length,c.id).toBeGreaterThan(12);
      c.skills.forEach((s,i)=>{
        const p=presentSkill(s);
        expect(html,c.id).toContain(`HABILIDADE ${i+1}`);
        expect(html,c.id).toContain(s.name);
        expect(p.effects,c.id).toHaveLength(s.effects.length);
        expect(p.effects.every(x=>x.length>5),c.id).toBe(true);
        /*
         * Uma linha por regra deixou de valer quando a ficha passou a somar as
         * fontes que o jogador lê como a mesma coisa (`time` e `survived` são
         * ambas "por segundo"). O que precisa valer é mais forte: agregar pode
         * juntar linhas, nunca perder Carga.
         */
        expect(p.charge.length,c.id).toBeGreaterThan(0);
        expect(p.charge.length,c.id).toBeLessThanOrEqual(s.charge.length);
        const somaNaFicha=p.charge.reduce((t,linha)=>t+Number(/\+([\d,]+)%/.exec(linha)![1]!.replace(',','.')),0);
        const somaNosDados=s.charge.reduce((t,r)=>t+r.amount,0);
        expect(somaNaFicha,c.id).toBeCloseTo(somaNosDados,1);
        expect(p.charge.every(x=>x.includes('%')),c.id).toBe(true);
        expect(p.target.length,c.id).toBeGreaterThan(4);
        expect(p.useWhen.length,c.id).toBeGreaterThan(10);
        expect(p.cooldown,c.id).toContain('s');
        if(s.preparation>0)expect(p.preparation,c.id).toContain('s');
      });
    }
  });
  it('explica cada Status, com valor e tom, sem esconder efeitos duplicados',()=>{
    for(const [id,def] of Object.entries(statuses)){
      const p=presentStatus(id as keyof typeof statuses,def.cap);
      // Fortalecido e Enfraquecido dizem só o número ("+18% de dano"), sem o verbo "Causa" que parecia um ataque
      if(id==='strengthened'||id==='weakened')expect(p.summary,id).toMatch(/^[+−]\d+% de dano$/);
      else expect(p.summary.length,id).toBeGreaterThanOrEqual(18);
      expect(p.tone,id).toBe(positiveStatuses.has(id as keyof typeof statuses)?'positivo':'negativo');
    }
    expect(presentStatus('marked',.15).summary).toContain('alvo preferencial');
    expect(presentStatus('rooted',.3).summary).toContain('Lento');
    expect(presentStatus('protected',.3).summary).toContain('não pode ser interrompido');
    expect(topicNames.losing).toContain('Vantagem');
    expect(topicNames.winning).toContain('Vantagem');
  });
  it('Light investiga sem conhecer imunidade, descobre uma vez e prefere desconhecidos',()=>{
    const b=createBattle(['light','pikachu','captain'],['goku','batman','thanos'],17),light=b.fighters[0],immune=b.fighters[3],unknown=b.fighters[4];
    expect(light.discovered).toEqual({});
    applyEffects(b,light,[immune],[{kind:'investigate',value:100}]);
    expect(light.discovered?.[immune.uid]).toBe('immune');
    const investigate=characters.find(c=>c.id==='light')!.skills[0];
    expect(targets(b,light,investigate.target,investigate.effects,false)[0]?.uid).not.toBe(immune.uid);
    expect([unknown.uid,b.fighters[5].uid]).toContain(targets(b,light,investigate.target,investigate.effects,false)[0]?.uid);
    applyEffects(b,light,[unknown],[{kind:'status',status:'protected',value:.2,duration:5}]);
    expect(light.skills[0].charge).toBe(0);
    applyEffects(b,b.fighters[1],[immune],[{kind:'status',status:'exposed',value:.2,duration:5}]);
    expect(light.skills[0].charge).toBeGreaterThan(0);
  });
  it('não cria caixas flutuantes de Carga no lutador',()=>{
    const b=createBattle(['light','pikachu','captain'],['goku','batman','thanos'],17),f=b.fighters[0];
    const html=renderToStaticMarkup(<ArenaUnit fighter={f} battle={b} beat={{event:{id:1,time:0,kind:'basic',source:f.uid,label:'Ataque básico'},events:[{id:2,time:0,kind:'charge',source:f.uid,target:f.uid,skill:0,label:'status',value:7}],before:b,after:b,duration:2,impacted:true,impactTime:1,grand:false,periodic:false,family:'physical'} as never} onInspect={()=>{}} numbers threatened={false}/>);
    expect(html).not.toContain('charge-reason');
    expect(html).not.toContain('+7%');
  });
});
