import {mkdirSync,writeFileSync} from 'node:fs';
import {characters} from '../src/data/characters';
import {expandedCharacters,rosterDesignQuestions,rosterMechanicStyles} from '../src/data/expanded-roster';
import {createBattle,stepBattle} from '../src/engine/battle';
import {shuffle} from '../src/engine/random';

const runs=12;
const totals=new Map<string,{skills:number[];basic:number;fights:number;knockouts:number;longest:number}>();
const archetypes:Record<string,string[]>={};
for(const c of expandedCharacters){totals.set(c.id,{skills:[0,0,0],basic:0,fights:0,knockouts:0,longest:0});(archetypes[rosterMechanicStyles[c.id]]??=[]).push(c.name);}
let crashes=0,completed=0;
for(let ci=0;ci<expandedCharacters.length;ci++){
  const chosen=expandedCharacters[ci];
  for(let seed=1;seed<=runs;seed++){
    const index=characters.findIndex(c=>c.id===chosen.id);
    const allies=[chosen.id,characters[(index+seed*7+1)%100].id,characters[(index+seed*13+2)%100].id];
    const pool=characters.filter(c=>!allies.includes(c.id)).map(c=>c.id);
    const enemy=shuffle(pool,{rng:(seed*7919+ci*1543+17)>>>0}).slice(0,3);
    const b=createBattle(allies,enemy,(ci+1)*1009+seed*65537);
    const seen=new Set<number>();const record=totals.get(chosen.id)!;
    try{
      while(!b.finished){
        stepBattle(b);
        for(const event of b.events){if(seen.has(event.id))continue;seen.add(event.id);if(event.source==='player-0'&&event.kind==='skill'&&typeof event.skill==='number')record.skills[event.skill]++;if(event.source==='player-0'&&event.kind==='basic')record.basic++;}
      }
      record.fights++;record.longest=Math.max(record.longest,b.time);if(b.fighters[0].hp<=0)record.knockouts++;completed++;
    }catch(error){crashes++;console.error(`SIM_ERROR ${chosen.id} seed=${seed}:`,error);}
  }
}
const allSkillAudits=expandedCharacters.flatMap(c=>c.skills.map((s,i)=>{const t=totals.get(c.id)!;return {character:c.name,skill:s.name,averageUsesPerFight:t.fights?Number((t.skills[i]/t.fights).toFixed(2)):0,uses:t.skills[i],fights:t.fights};}));
const dark=allSkillAudits.filter(s=>s.uses===0);
const sparse=allSkillAudits.filter(s=>s.averageUsesPerFight>0&&s.averageUsesPerFight<.25);
const fingerprint=(c:typeof expandedCharacters[number])=>JSON.stringify({basic:c.basic.effects.slice(1).map(e=>e.kind==='status'?`s:${e.status}`:e.kind).sort(),skills:c.skills.map(s=>({charge:s.charge.map(r=>r.on).sort(),target:s.target,condition:s.condition,preparation:s.preparation>0,effects:s.effects.map(e=>e.kind==='status'?`s:${e.status}`:e.kind).sort()}))});
const fingerprints=new Set(expandedCharacters.map(fingerprint));
const all=characters;
const uses=(c:typeof characters[number],kind:string)=>c.skills.some(s=>s.effects.some(e=>e.kind===kind)||(kind==='status'&&s.effects.some(e=>e.kind==='status'&&e.status==='protected')));
const behaviorCounts={
  'início explosivo':all.filter(c=>c.tags.includes('burst')||c.interval<2.7).length,
  crescimento:all.filter(c=>['growth','revenge','transform','charge'].some(t=>c.tags.includes(t))).length,
  controle:all.filter(c=>['control','trap','psychic','shadow'].some(t=>c.tags.includes(t))||c.skills.some(s=>s.effects.some(e=>e.kind==='interrupt'))).length,
  interrupção:all.filter(c=>c.skills.some(s=>s.effects.some(e=>e.kind==='interrupt'))).length,
  proteção:all.filter(c=>uses(c,'shield')||c.skills.some(s=>s.effects.some(e=>e.kind==='status'&&e.status==='protected'))).length,
  cura:all.filter(c=>uses(c,'heal')).length,
  regeneração:all.filter(c=>c.tags.includes('regen')||c.skills.some(s=>s.effects.some(e=>e.kind==='status'&&e.status==='regen'))).length,
  preparação:all.filter(c=>c.skills.some(s=>s.preparation>=2)).length,
  execução:all.filter(c=>['finisher','execution','assassin'].some(t=>c.tags.includes(t))||c.skills.some(s=>s.effects.some(e=>e.kind==='damage'&&e.value>=350))).length,
  manipulação:all.filter(c=>['manipulation','illusion','trickster','psychic'].some(t=>c.tags.includes(t))).length,
  invocação:all.filter(c=>c.tags.includes('summoner')).length,
  transformação:all.filter(c=>c.tags.includes('transform')).length,
  velocidade:all.filter(c=>c.interval<=2.8||c.tags.includes('speedster')).length,
  suporte:all.filter(c=>['support','protector','healer','leader'].some(t=>c.tags.includes(t))||uses(c,'heal')||uses(c,'shield')).length,
};
const diversity=Object.entries(archetypes).map(([style,people])=>`${style}: ${people.length} (${people.join(', ')})`).join('\n');
const design=expandedCharacters.map(c=>{
  const question=rosterDesignQuestions[c.id];
  const skills=c.skills.map((s,i)=>`${i+1}. **${s.name}** — ${s.description} Carga: ${s.chargeText} (${s.charge.map(x=>`${x.on} ${x.amount}`).join(' + ')}); alvo ${s.target}; uso ${s.condition}; prep ${s.preparation}s; recarga ${s.cooldown}s.`).join('\n');
  const trait=c.trait;
  return `### ${c.name} (${c.universe})\n\n- Ideia: ${c.idea}\n- Pergunta estratégica: ${question}\n- Estimativa inicial: poder ${c.power}/100; Condição ${c.hp}; intervalo de ação ${c.interval}s.\n- Traço: ${trait.name} — ${trait.description} (${trait.on}, recarga ${trait.cooldown}s)\n- Ação principal: ${c.basic.name} — alvo ${c.basic.target}; ${c.basic.effects.map(e=>e.kind==='status'?`${e.status} ${e.value}`:e.kind==='release'?`${e.kind} x${e.multiplier}`:`${e.kind} ${e.value}`).join(', ')}\n- Vulnerabilidade: ${c.vulnerability}\n- Tags: ${c.tags.join(', ')}\n- Death Note: ${c.deathNoteCompatible?'compatível':'incompatível'}\n${skills}`;
}).join('\n\n');
const audit=`# Catálogo mecânico Nexus Trios — 100 personagens\n\nO catálogo manteve os 24 kits originais e acrescentou 76 fichas. A ordem seguiu os candidatos do anexo até Shazam: 45 nomes de anime e os primeiros 31 de quadrinhos. Nenhum retrato existente foi alterado; os novos usam placeholders individuais.\n\n## Variedade de padrões mecânicos\n\n${diversity}\n\nContagem aproximada de comportamentos no catálogo todo (categorias podem se sobrepor):\n\n${Object.entries(behaviorCounts).map(([k,v])=>`- ${k}: ${v}`).join('\n')}\n\nAuditoria estrutural de similaridade: ${fingerprints.size}/${expandedCharacters.length} fichas novas têm assinaturas distintas nos gatilhos de carga, alvos, condições, preparação e famílias de efeitos; ${expandedCharacters.length-fingerprints.size} clones exatos por essa comparação. Isso detecta configurações iguais, não substitui avaliação humana da fantasia temática.\n\n## Uso de habilidades em simulação\n\nCada personagem novo participou de ${runs} batalhas headless com sementes e trios variados (${completed} batalhas concluídas; ${crashes} crashes). Usos médios por luta = quantidade observada dividida pelo número de batalhas. Pode passar de 100%: 16 usos em 12 batalhas = 1,33 uso por luta (133%), não 133% de chance.\n\n| Personagem | Habilidade | Usos / ${runs} | Usos médios por luta |\n|---|---|---:|---:|\n${allSkillAudits.map(s=>`| ${s.character} | ${s.skill} | ${s.uses} | ${s.averageUsesPerFight.toFixed(2)} |`).join('\n')}\n\nHabilidades sem uso: ${dark.length}${dark.length?` (${dark.map(s=>`${s.character}: ${s.skill}`).join('; ')})`:'.'}\n\nHabilidades raras (<0,25 uso por luta): ${sparse.length}${sparse.length?` (${sparse.map(s=>`${s.character}: ${s.skill}`).join('; ')})`:'.'}\n\n## Notas de arquitetura e limites da auditoria\n\nAs 22 receitas compartilhadas reutilizam efeitos existentes (dano, estados, proteção, cura, interrupção e avanço/atraso de ação). Hooks orientados por tags variam efeitos da ação principal e gatilhos de carga sem checagens pelo nome do personagem. O motor e suas regras não foram clonados por personagem. Invocações e transformações aparecem como efeitos temporários no kit; não foi adicionado subsistema persistente de entidades. Compatibilidade com Death Note é um campo por ficha. Não houve ajuste de balanceamento estatístico.\n\nA simulação usa 12 sementes por personagem e serve para encontrar gatilhos estruturalmente mortos, não para provar balanceamento.\n\n## Fichas resumidas\n\n${design}\n`;
mkdirSync('docs',{recursive:true});writeFileSync('docs/roster-design-and-audit.md',audit);
writeFileSync('docs/roster-simulation.json',JSON.stringify({runsPerCharacter:runs,completed,crashes,metric:'uses per fight; values above 1 (100%) are valid averages, not probabilities',skills:allSkillAudits,unused:dark,rare:sparse},null,2));
console.log(JSON.stringify({characters:characters.length,newCharacters:expandedCharacters.length,runsPerCharacter:runs,completed,crashes,zeroUse:dark,rare:sparse,styleCounts:Object.fromEntries(Object.entries(archetypes).map(([k,v])=>[k,v.length]))},null,2));
