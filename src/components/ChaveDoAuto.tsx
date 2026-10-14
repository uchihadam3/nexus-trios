import { Repeat } from 'lucide-react';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import '../presentation/chave-auto.css';

/*
 * Lutas seguidas (pedido do jogador: o botão de deixar as lutas correndo uma atrás da outra estava "muito escondidinho
 * lá embaixo… muito pequenininho"). Agora ele fica à vista nos dois lugares em que importa:
 *  - na tela do resultado, dentro do rodapé fixo, logo acima de "Próxima luta" (ChaveDoAuto);
 *  - na barra de controles da batalha, ao lado da velocidade (BotaoAutoDaBatalha).
 * Ligado, a próxima luta começa sozinha depois de uma vitória, ESPERA_DA_PROXIMA_MS depois do resultado.
 */
export const ESPERA_DA_PROXIMA_MS = 4500;

const toque = (ligado: boolean) => battleAudio.sound(ligado ? 'pronto' : 'toque', PRIORIDADE.interface);

/** A chave grande do resultado: um interruptor de verdade, que acende e gira quando está ligado. */
export function ChaveDoAuto({ ligado, onChange }: { ligado: boolean; onChange: (v: boolean) => void }) {
  return <button type="button" role="switch" aria-checked={ligado} className={`seq-chave ${ligado ? 'ligado' : ''}`}
    onClick={() => { onChange(!ligado); toque(!ligado); }}>
    <span className="seq-icone" aria-hidden="true"><Repeat size={20} /></span>
    <span className="seq-texto">
      <b>LUTAS SEGUIDAS</b>
      <small>{ligado ? 'Ligado: a próxima luta começa sozinha' : 'Ligue para as lutas seguirem sozinhas'}</small>
    </span>
    <span className="seq-trilho" aria-hidden="true"><i>{ligado ? 'ON' : 'OFF'}</i><span className="seq-bolinha" /></span>
  </button>;
}

/** O mesmo interruptor, pequeno, na barra de controles da batalha. */
export function BotaoAutoDaBatalha({ ligado, onChange }: { ligado: boolean; onChange: (v: boolean) => void }) {
  return <button type="button" role="switch" aria-checked={ligado} className={`control seq-controle ${ligado ? 'ligado' : ''}`}
    aria-label={ligado ? 'Lutas seguidas ligado: a próxima luta começa sozinha. Toque para desligar' : 'Lutas seguidas desligado. Toque para ligar'}
    title="Lutas seguidas" onClick={() => { onChange(!ligado); toque(!ligado); }}>
    <Repeat size={17} /><b>AUTO</b>
  </button>;
}
