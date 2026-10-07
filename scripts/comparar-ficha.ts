/* Antes e depois, nos exemplos que o jogador apontou nos prints. */
import { byId } from '../src/data/characters';
import { presentSkill } from '../src/engine/skill-descriptions';

for(const id of ['naruto','wonderwoman','cyclops','shazam']){
  const c=byId[id]; if(!c)continue;
  console.log(`\n######## ${c.name}`);
  for(const s of c.skills){
    const p=presentSkill(s);
    console.log(`\n-- ${s.name}`);
    console.log('  ANTES:');
    for(const l of p.effects)console.log(`    ${l}`);
    if(p.mostrarAlvo)console.log(`    Alvo: ${p.target}`);
    console.log('  DEPOIS:');
    for(const g of p.grupos){
      if(g.titulo)console.log(`    ${g.titulo}`);
      for(const l of g.linhas)console.log(`      ${l.texto}`);
    }
    if(p.mostrarAlvo)console.log(`    Alvo: ${p.target}`);
  }
}
