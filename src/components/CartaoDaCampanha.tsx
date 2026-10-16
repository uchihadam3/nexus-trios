import type { CSSProperties, ReactNode } from 'react';
import { Crown, Lock, Play, Star } from 'lucide-react';
import { byId } from '../data/characters';
import { Portrait } from './Portrait';
import { RIVAIS, TOTAL_DE_ESTRELAS, rivalPorId, type Rival } from '../engine/campanha';
import { read } from '../lib/storage';
import '../presentation/campanha.css';

/*
 * O cartão do Caminho do Nexus no lobby do PvP e o rosto de cada rival (src/screens/CaminhoDoNexus.tsx). Fica fora da
 * tela da campanha para o lobby não carregar a campanha inteira só para mostrar o cartão.
 */

/** O resumo que o lobby mostra no cartão da campanha (guardado pela tela da campanha, sem pedir nada ao servidor). */
export interface ResumoDaCampanha { estrelas: number; titulo: string; proximo: string | null; zerou: boolean }
export const CHAVE_DO_RESUMO = 'campanha-resumo';

export function AvatarDoRival({ rival, tamanho = 64, apagado = false }: { rival: Rival; tamanho?: number; apagado?: boolean }) {
  return <span className={`cn-avatar ${rival.chefe ? 'chefe' : ''} ${apagado ? 'apagado' : ''}`} style={{ '--cor': rival.cor, '--t': `${tamanho}px` } as CSSProperties}>
    <Portrait character={byId[rival.avatar]!} />
    {rival.chefe && <Crown className="cn-coroa" size={Math.round(tamanho * 0.32)} />}
  </span>;
}
/** O cartão da campanha no lobby do PvP. */
export function CartaoDaCampanha({ podeJogar, motivo, onAbrir }: { podeJogar: boolean; motivo?: ReactNode; onAbrir: () => void }) {
  const resumo = read(CHAVE_DO_RESUMO) as ResumoDaCampanha | null, proximo = resumo?.proximo ? rivalPorId(resumo.proximo) : RIVAIS[0]!;
  const chefes = [RIVAIS[4]!, RIVAIS[19]!, RIVAIS[39]!];
  return <button className={`cn-cartao ${podeJogar ? '' : 'travado'}`} onClick={podeJogar ? onAbrir : undefined} aria-disabled={!podeJogar}>
    <span className="cn-cartao-chefes" aria-hidden="true">{chefes.map((c, i) => <AvatarDoRival key={c.id} rival={c} tamanho={i === 2 ? 58 : 44} />)}</span>
    <span className="cn-cartao-texto">
      <small>MODO CAMPANHA · 40 RIVAIS · 8 REGIÕES</small>
      <b>CAMINHO DO NEXUS</b>
      {podeJogar ? <em>{resumo ? <><Star size={12} />{resumo.estrelas}/{TOTAL_DE_ESTRELAS} · {resumo.titulo}{resumo.zerou ? ' · Zerou!' : proximo ? ` · próximo: ${proximo.nome}` : ''}</> : 'Comece na Vila do Começo. Só o primeiro rival está liberado.'}</em> : <em className="cn-cartao-motivo"><Lock size={12} />{motivo}</em>}
    </span>
    {podeJogar && <Play size={24} className="cn-cartao-play" />}
  </button>;
}
