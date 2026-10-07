import {describe,it,expect} from 'vitest';
import {characters} from '../src/data/characters';
import {chaveDaCombinacao,combinacoesIntencionais,fundirEfeitos} from '../src/data/expanded-roster';
import type {Effect,StatusId} from '../src/engine/types';

/*
 * Redundância é bug de clareza, e precisa de guarda automática.
 *
 * A direção descreveu os dois casos com exemplo: "Lento 20% por 6 s" junto de
 * "Lento 5% por 4 s", onde o menor não acrescenta nada; e duas fontes de Carga
 * do mesmo tópico, que para o jogador sempre foram um número só. Os dois
 * nasciam da mesma linha de código — o hook da tag era anexado ao kit sem
 * checar o que já estava lá — e os dois somavam trinta ocorrências no
 * catálogo, incluindo a Storm, que foi o caso que a direção apontou.
 */
describe('fichas sem redundância',()=>{
  const partes=(c:(typeof characters)[number])=>[
    {nome:'ataque básico',id:'basico',efeitos:c.basic.effects,carga:[] as {on:string}[]},
    {nome:c.trait.name,id:'traco',efeitos:c.trait.effects,carga:[] as {on:string}[]},
    ...c.skills.map(s=>({nome:s.name,id:s.id,efeitos:s.effects,carga:s.charge as {on:string}[]})),
  ];

  it('nunca aplica o mesmo Status duas vezes na mesma ação, exceto onde for declarado',()=>{
    for(const c of characters)for(const parte of partes(c)){
      const permitidos=combinacoesIntencionais[chaveDaCombinacao(c.id,parte.id)]??[];
      const vistos=new Set<string>();
      for(const e of parte.efeitos){
        if(e.kind!=='status')continue;
        if(permitidos.includes(e.status))continue;
        const chave=`${e.status}:${e.target??''}`;
        expect(vistos.has(chave),`${c.name} · ${parte.nome} · ${chave} repetido`).toBe(false);
        vistos.add(chave);
      }
    }
  });

  /*
   * O registro não pode virar um cesto de desculpas.
   *
   * Cada entrada precisa apontar para uma habilidade que existe e para um
   * Status que aquela habilidade de fato aplica — senão ela estaria perdoando
   * um defeito que ninguém revisou, ou sobrevivendo a uma renomeação.
   */
  it('cada combinação declarada corresponde a uma habilidade e a um Status reais',()=>{
    for(const [chave,statuses] of Object.entries(combinacoesIntencionais)){
      const [personagem,habilidade]=chave.split('/');
      const c=characters.find(x=>x.id===personagem);
      expect(c,`${chave}: personagem inexistente`).toBeDefined();
      const parte=partes(c!).find(x=>x.id===habilidade);
      expect(parte,`${chave}: habilidade inexistente`).toBeDefined();
      for(const status of statuses){
        const aplicadas=parte!.efeitos.filter(e=>e.kind==='status'&&e.status===status);
        expect(aplicadas.length,`${chave}: ${status} declarado mas aplicado ${String(aplicadas.length)}× `).toBeGreaterThan(1);
      }
    }
  });

  it('o registro de combinações intencionais usa Status que o motor conhece',()=>{
    const validos=new Set<StatusId>(['exposed','paralyzed','protected','marked','slow','haste','confused','rooted','regen','burning','electric','silenced','strengthened','weakened']);
    for(const statuses of Object.values(combinacoesIntencionais))
      for(const s of statuses)expect(validos.has(s),`Status desconhecido: ${s}`).toBe(true);
  });

  it('nunca conta a mesma fonte de Carga duas vezes',()=>{
    for(const c of characters)for(const parte of partes(c)){
      const vistos=new Set<string>();
      for(const r of parte.carga){
        expect(vistos.has(r.on),`${c.name} · ${parte.nome} · Carga ${r.on} duplicada`).toBe(false);
        vistos.add(r.on);
      }
    }
  });
});

/*
 * A fusão em si, exercitada nos dois sentidos.
 *
 * Com o registro de combinações intencionais vazio, os testes acima passam
 * sem provar nada. Estes provam: por padrão a fusão acontece, e quando o
 * Status está declarado como intencional ela **não** acontece — que é
 * exatamente a ressalva levantada na revisão do lote 1.
 */
describe('fundirEfeitos',()=>{
  const lento=(value:number,duration:number,target?:'allEnemies'):Effect=>
    ({kind:'status',status:'slow',value,duration,...(target?{target}:{})});

  it('funde duas aplicações iguais mantendo a maior intensidade e a maior duração',()=>{
    const saida=fundirEfeitos([lento(.2,6),lento(.05,9)]);
    expect(saida).toHaveLength(1);
    const unico=saida[0];
    expect(unico.kind).toBe('status');
    if(unico.kind!=='status')return;
    expect(unico.value).toBe(.2);
    expect(unico.duration).toBe(9);
  });

  it('não funde quando os alvos são diferentes',()=>{
    expect(fundirEfeitos([lento(.2,6),lento(.05,4,'allEnemies')])).toHaveLength(2);
  });

  it('preserva as duas aplicações quando o Status é declarado intencional',()=>{
    const saida=fundirEfeitos([lento(.2,6),lento(.05,9)],['slow']);
    expect(saida).toHaveLength(2);
    expect(saida.map(e=>e.kind==='status'?e.value:0)).toEqual([.2,.05]);
  });

  it('nunca mexe no que não é Status',()=>{
    const dano:Effect={kind:'damage',value:100};
    expect(fundirEfeitos([dano,dano])).toHaveLength(2);
  });
});
