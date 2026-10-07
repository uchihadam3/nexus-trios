import {describe,it,expect} from 'vitest';
import {characters} from '../src/data/characters';

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
    {nome:'ataque básico',efeitos:c.basic.effects,carga:[] as {on:string}[]},
    {nome:c.trait.name,efeitos:c.trait.effects,carga:[] as {on:string}[]},
    ...c.skills.map(s=>({nome:s.name,efeitos:s.effects,carga:s.charge as {on:string}[]})),
  ];

  it('nunca aplica o mesmo Status duas vezes na mesma ação',()=>{
    for(const c of characters)for(const parte of partes(c)){
      const vistos=new Set<string>();
      for(const e of parte.efeitos){
        if(e.kind!=='status')continue;
        const chave=`${e.status}:${e.target??''}`;
        expect(vistos.has(chave),`${c.name} · ${parte.nome} · ${chave} repetido`).toBe(false);
        vistos.add(chave);
      }
    }
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
