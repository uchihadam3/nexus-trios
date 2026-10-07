/*
 * FASE G · o Raio-X do Trio, na tela.
 *
 * Depois de toda batalha, ganhando ou perdendo, o jogador precisa aprender
 * alguma coisa sobre a combinação que montou — e o documento da direção é
 * explícito sobre a forma: **não parede de texto**, usar os três retratos e as
 * conexões, nas seis direções (A→B, A→C, B→A, B→C, C→A, C→B).
 *
 * Então cada par é uma linha: dois retratos, a classificação, e no máximo uma
 * frase por direção — a conexão mais forte que de fato aconteceu. As frases
 * vêm prontas de `engine/raio-x.ts`, que as monta a partir dos eventos reais
 * do combate; aqui não se calcula nem se interpreta nada.
 */
import { ArrowRight, Scan } from 'lucide-react';

import { byId } from '../data/characters';
import type { Battle } from '../engine/types';
import { lerRaioX, quemAbsorveu, type Classificacao, type EstadoRaioX } from '../engine/raio-x';
import { Portrait } from './Portrait';

/* O tom de cada classificação. "Independentes" não é defeito, e não se pinta como tal. */
const TOM: Record<Classificacao, string> = {
  'ÓTIMA CONEXÃO': 'otima', 'BOA CONEXÃO': 'boa', 'POUCA CONEXÃO': 'pouca',
  'INDEPENDENTES': 'neutra', 'CONFLITO': 'conflito',
};

/* O que a classificação quer dizer, numa linha. */
const EXPLICACAO: Record<Classificacao, string> = {
  'ÓTIMA CONEXÃO': 'Um ativou o outro o tempo todo.',
  'BOA CONEXÃO': 'Um ajudou o outro várias vezes.',
  'POUCA CONEXÃO': 'Quase não ativaram mecânicas um do outro.',
  'INDEPENDENTES': 'Lutaram bem, cada um por si. Não é problema.',
  'CONFLITO': 'Um atrapalhou o outro.',
};

export function RaioXDoTrio({ estado, battle }: { estado: EstadoRaioX; battle: Battle }) {
  const pares = lerRaioX(estado, battle);
  if (pares.length === 0) return null;
  const nome = (uid: string) => {
    const f = battle.fighters.find((x) => x.uid === uid);
    return f ? byId[f.characterId]?.name ?? '' : '';
  };
  const retrato = (uid: string) => {
    const f = battle.fighters.find((x) => x.uid === uid);
    return f ? byId[f.characterId] : undefined;
  };
  const pressao = quemAbsorveu(estado, battle);

  return <section className="raio-x">
    <div className="raio-x-head"><Scan size={18} /><h2>Raio-X do trio</h2>
      <small>O que cada um fez pelo outro nesta luta.</small></div>

    {pares.map((par) => {
      const a = retrato(par.a), b = retrato(par.b);
      if (!a || !b) return null;
      return <article className={`raio-x-par ${TOM[par.classificacao]}`} key={`${par.a}-${par.b}`}>
        <div className="raio-x-duo">
          <div className="raio-x-rosto" style={{ '--character': a.color } as React.CSSProperties}><Portrait character={a} className="tiny" /><span>{a.name}</span></div>
          <div className="raio-x-rosto" style={{ '--character': b.color } as React.CSSProperties}><Portrait character={b} className="tiny" /><span>{b.name}</span></div>
        </div>
        <div className="raio-x-corpo">
          <span className="raio-x-selo">{par.classificacao}</span>
          {/*
            * As duas direções, cada uma com a sua frase. Quando uma delas não
            * tem elo nenhum, a linha simplesmente não aparece — dizer "não
            * ajudou" seria inventar um julgamento onde só houve ausência.
            */}
          {par.aParaB.frase && <p><b>{nome(par.a)}</b> <ArrowRight size={12} /> {par.aParaB.frase}</p>}
          {par.bParaA.frase && <p><b>{nome(par.b)}</b> <ArrowRight size={12} /> {par.bParaA.frase}</p>}
          {!par.aParaB.frase && !par.bParaA.frase && <p className="raio-x-vazio">{EXPLICACAO[par.classificacao]}</p>}
          {(par.aParaB.frase ?? par.bParaA.frase) && <small>{EXPLICACAO[par.classificacao]}</small>}
        </div>
      </article>;
    })}

    {pressao && <p className="raio-x-pressao">
      <b>{nome(pressao.uid)}</b> segurou a pressão: {pressao.dano.toLocaleString('pt-BR')} de dano recebido,
      {' '}{Math.round(pressao.parte * 100)}% de tudo que o trio levou.
    </p>}
  </section>;
}
