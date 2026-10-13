/*
 * O preparo da Mecânica única (pedido do jogador: "quando os personagens vão preparar pra usar uma habilidade tem
 * uma animação muito legal que acontece antes, quero que use essa animação quando eles forem usar a mecânica única
 * também… tudo tem que ser igual uma habilidade").
 *
 * Antes de a mecânica disparar sozinha, quem a usa prepara do mesmo jeito que prepara uma habilidade: o anel de
 * Preparo enchendo, o nome com o ícone de "preparando", a folha de preparo e o som de carregar. A folha e o som são
 * os da habilidade de Preparo mais longo do próprio personagem (a carga de ki do Goku, o Nen do Gon…); quem não tem
 * nenhuma habilidade com folha de preparo usa a carga comum.
 */
import { byId } from '../data/characters';
import { SOM_DA_FAMILIA, type Sound } from '../audio/cues';
import { familia, profileFor } from './vfxProfiles';

export interface PreparoDaUnica { folha: string; som: Sound }

const CACHE: Record<string, PreparoDaUnica> = {};

export function preparoDaUnica(characterId: string): PreparoDaUnica {
  const salvo = CACHE[characterId];
  if (salvo) return salvo;
  const c = byId[characterId];
  let melhor: PreparoDaUnica | undefined, maior = -1;
  c?.skills.forEach((s, i) => {
    const fam = profileFor(characterId, i)?.family;
    const preparo = fam ? familia(fam).preparo : undefined;
    if (!fam || !preparo || s.preparation <= maior) return;
    const som = SOM_DA_FAMILIA[fam];
    maior = s.preparation;
    melhor = { folha: preparo, som: som?.antes ?? som?.preparo ?? 'preparo' };
  });
  return (CACHE[characterId] = melhor ?? { folha: 'carga', som: 'preparo' });
}
