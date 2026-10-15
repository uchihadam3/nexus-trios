/*
 * O espelho da luta (PvP online): a mesma luta vista do outro lado.
 *
 * A luta de uma rodada é uma só, calculada com o desafiante no lado de baixo ('player'). Quem foi desafiado vê o
 * time dele embaixo: antes de desenhar, cada quadro da luta passa por aqui e os lados trocam — 'player' ↔ 'enemy',
 * 'player-0' ↔ 'enemy-0' (em valores e em chaves), e a Vantagem (dominion) e a pressão (momentum) mudam de sinal.
 * O resto (quem é aliado ou rival de quem, os números, os eventos) continua igual, porque é relativo.
 */
const UID = /^(player|enemy)-(\d+)$/;
const NEGA = new Set(['dominion', 'momentum']);

const troca = (s: string): string => {
  if (s === 'player') return 'enemy';
  if (s === 'enemy') return 'player';
  const m = UID.exec(s);
  return m ? `${m[1] === 'player' ? 'enemy' : 'player'}-${m[2]}` : s;
};

/* os eventos não mudam depois de criados: o espelho de cada um é feito uma vez só */
const eventos = new WeakMap<object, unknown>();

function vira(x: unknown, chave = ''): unknown {
  if (typeof x === 'string') return troca(x);
  if (typeof x === 'number') return NEGA.has(chave) ? -x : x;
  if (x === null || typeof x !== 'object') return x;
  if (Array.isArray(x)) return x.map((v) => vira(v));
  const ehEvento = 'kind' in x && 'id' in x && 'source' in x;
  if (ehEvento) { const ja = eventos.get(x); if (ja) return ja; }
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(x)) out[troca(k)] = vira(v, k);
  if (ehEvento) eventos.set(x, out);
  return out;
}

/** A luta (ou um beat do diretor) vista do outro lado da arena. */
export function espelhar<T>(x: T): T {
  return vira(x) as T;
}
