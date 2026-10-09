/*
 * O efeito e o som de cada jeito de bater (src/data/basicos.ts).
 *
 * Pedido do jogador: "as mecânicas especiais do ataque básico… animação
 * própria… com efeito sonoro também correto". O golpe em si usa a família do
 * básico; por cima, cada mecânica mostra o que fez, em quem fez: o quique no
 * segundo rival, a varrida, o golpe final da série com os três pontos do
 * combo, a cura no aliado, a Carga saindo do rival e chegando em quem roubou,
 * os cacos virando escudo e o relógio de quem acelerou.
 */
import { byId } from '../data/characters';
import type { BattleEvent, Fighter } from '../engine/types';
import type { FamiliaNova } from './vfx-familias-novas';

export const FAMILIAS_DO_JEITO = ['quique', 'golpe_largo', 'golpe_da_serie', 'golpe_que_cura', 'roubar_carga', 'carga_roubada', 'guarda_do_golpe', 'acelera'] as const satisfies readonly FamiliaNova[];
type FamiliaDoJeito = (typeof FAMILIAS_DO_JEITO)[number];

export interface EfeitoDoJeito { alvo: string; familia: FamiliaDoJeito; evento: BattleEvent; atraso: number }

/** Os efeitos de jeito de bater de um beat: o evento principal e os que vieram com ele. */
export function efeitosDoJeito(principal: BattleEvent, eventos: BattleEvent[], lutadores: Fighter[]): EfeitoDoJeito[] {
  const out: EfeitoDoJeito[] = [];
  if (principal.kind === 'basic' && principal.target) {
    const f = lutadores.find((x) => x.uid === principal.source);
    const jeito = f ? byId[f.characterId]?.basic.jeito : undefined;
    // o golpe especial da série sai com o nome dele no lugar do nome do básico
    if (jeito?.tipo === 'serie' && principal.label === jeito.nome) out.push({ alvo: principal.target, familia: 'golpe_da_serie', evento: principal, atraso: 0 });
  }
  for (const e of eventos) {
    if (e.kind === 'damage' && e.label === 'Ricochete' && e.target) out.push({ alvo: e.target, familia: 'quique', evento: e, atraso: 0 });
    if (e.kind === 'damage' && e.label === 'Golpe largo' && e.target) out.push({ alvo: e.target, familia: 'golpe_largo', evento: e, atraso: 0 });
    if (e.kind === 'heal' && e.label === 'Golpe que cura' && e.target) out.push({ alvo: e.target, familia: 'golpe_que_cura', evento: e, atraso: 0.05 });
    if (e.kind === 'shield' && e.label === 'Guarda do golpe' && e.target) out.push({ alvo: e.target, familia: 'guarda_do_golpe', evento: e, atraso: 0.05 });
    if (e.kind === 'tempo' && e.label === 'Acelerou' && e.target) out.push({ alvo: e.target, familia: 'acelera', evento: e, atraso: 0.05 });
    if (e.kind === 'charge' && e.label === 'Roubou Carga') {
      // sai de quem levou o golpe e chega em quem roubou
      if (principal.target && principal.target !== e.source) out.push({ alvo: principal.target, familia: 'roubar_carga', evento: e, atraso: 0 });
      out.push({ alvo: e.source, familia: 'carga_roubada', evento: e, atraso: 0.25 });
    }
  }
  return out;
}

/** O som de uma família de jeito de bater (o arquivo em public/assets/audio/sfx). */
export const somDoJeito = (f: FamiliaDoJeito) => f.replace(/_/g, '-');
