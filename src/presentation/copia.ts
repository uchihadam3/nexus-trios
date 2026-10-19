import type { BattleEvent } from '../engine/types';
import type { Beat } from './director';
import { profileFor, type VfxFamily } from './vfxProfiles';

/*
 * Copiar habilidade (a Cópia perfeita do Kakashi e as outras cópias): a habilidade copiada aparece com o efeito e o som
 * de quem ela é (pedido do dono: "ele deveria usar exatamente o mesmo efeito da pessoa… o efeito visual, o efeito
 * sonoro"). O motor diz qual habilidade foi copiada (`copiada` no evento de cópia, src/engine/battle.ts); aqui saem a
 * família do efeito dela e quem a cópia acertou (os eventos de quem copiou que vêm depois da cópia, na mesma ação).
 */
export interface CopiaNaTela { familia: VfxFamily; alvos: string[] }

export function copiaNaTela(beat: Pick<Beat, 'events' | 'after'>, copia: BattleEvent): CopiaNaTela | undefined {
  if (copia.kind !== 'copy' || copia.copiada === undefined) return undefined;
  const dono = beat.after.fighters.find((f) => f.uid === copia.target);
  const familia = dono ? profileFor(dono.characterId, copia.copiada)?.family : undefined;
  if (!familia) return undefined;
  const alvos = [...new Set(beat.events
    .filter((e) => e.id > copia.id && e.source === copia.source && e.target && ['damage', 'heal', 'shield', 'status'].includes(e.kind))
    .map((e) => e.target!))];
  return { familia, alvos: alvos.length ? alvos : [copia.source] };
}
