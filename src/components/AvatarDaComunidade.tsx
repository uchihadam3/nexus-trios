import type { CSSProperties } from 'react';
import { byId } from '../data/characters';
import { Portrait } from './Portrait';
import { corDoNome, type Jogador } from '../lib/comunidade';
import '../presentation/comunidade.css';

/** A foto de cada um: o primeiro do trio recorde dele; sem trio, a inicial numa medalha da cor do nome. */
export function Avatar({ jogador, id, nome, tamanho = 44, online }: { jogador?: Jogador; id: string; nome: string; tamanho?: number; online?: boolean }) {
  const c = jogador?.trio?.[0] ? byId[jogador.trio[0]] : undefined, ligado = online ?? jogador?.online ?? false;
  return <span className={`cm-avatar ${ligado ? 'online' : ''}`} style={{ '--t': `${tamanho}px`, '--cor': corDoNome(id), ...(c ? { '--character': c.color } : {}) } as CSSProperties}>
    {c ? <Portrait character={c} /> : <b>{nome.slice(0, 1).toUpperCase()}</b>}
    <i aria-hidden="true" />
  </span>;
}

