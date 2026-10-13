/*
 * A bolinha da Mecânica única (pedido do jogador: "usar essa bolinha pra demonstrar alguma coisa, pra cada uma das
 * mecânicas únicas… mostrar que tá prestes a ativar… extremamente bem gamificado").
 *
 * Cada personagem tem um ícone que conta a mecânica dele e um jeito de encher (src/presentation/bolinhas.ts):
 *   relogio · "a cada X s": enche com o tempo e mostra os segundos que faltam (sai sozinho do relógio do motor);
 *   barra   · uma barra até um máximo (o ???% do Mob): mostra a porcentagem;
 *   ciclo   · "a cada N golpes": enche a cada golpe e mostra quantos faltam;
 *   conta   · um contador até disparar (os 4 golpes do Saitama): mostra quantos faltam; cheio, fica aceso;
 *   pilhas  · acumula até um teto (os clones do Naruto): os pontinhos em volta mostram quantas tem;
 *   tempo   · "aos X s de luta": mostra os segundos até lá; depois, aceso ou usado;
 *   vida    · "com menos de X% da Vida": enche conforme a Vida desce até o limite, que aparece no meio;
 *   vez     · "1 vez por luta": acesa, pronta; depois de usar, apagada com o ✓;
 *   chance  · "X% de chance": mostra a chance;
 *   liga    · vale quando algo acontece (um rival em Preparo, alguém Sangrando): acende enquanto vale;
 *   acesa   · vale a luta toda (brilho calmo, sem pulsar: o pulso fica para quando algo está para acontecer).
 * A luz diz como ela brilha: carregando, quase (prestes a ativar), pronta, usada.
 */
import type { LucideIcon } from 'lucide-react';
import type { Battle, Fighter } from '../engine/types';

export type ModoDaBolinha = 'relogio' | 'barra' | 'ciclo' | 'conta' | 'pilhas' | 'tempo' | 'vida' | 'vez' | 'chance' | 'liga' | 'acesa';
export interface Bolinha {
  ic: LucideIcon;
  modo?: ModoDaBolinha;
  /** a chave do estado da mecânica no lutador (f.u); termina em * para "a maior entre as que começam assim" */
  k?: string;
  max?: number;
  n?: number;
  em?: number;
  lim?: number[];
  p?: number;
  /** a chave que diz que já foi usada (vez, tempo, vida) */
  usada?: string;
  /** já foi usada, para os casos que uma chave não diz */
  usadaSe?: (f: Fighter, b: Battle) => boolean;
  /** quando ela vale (liga) */
  vale?: (f: Fighter, b: Battle) => boolean;
  /** o quanto encheu (0 a 1), para os casos que não cabem num modo */
  valor?: (f: Fighter, b: Battle) => number;
  /** o texto do meio, para os casos especiais */
  texto?: (f: Fighter, b: Battle) => string | undefined;
  /** a cor (o padrão é o roxo da mecânica) */
  cor?: string;
}

export type LuzDaBolinha = 'carregando' | 'quase' | 'pronta' | 'usada' | 'apagada' | 'acesa';
export interface BolinhaNaTela { carga: number; texto?: string; pontos?: { tem: number; max: number }; luz: LuzDaBolinha }

const leia = (f: Fighter, k?: string): number => {
  const s = f.u;
  if (!s || !k) return 0;
  if (k.endsWith('*')) {
    const p = k.slice(0, -1);
    let m = 0;
    for (const x in s) if (x.startsWith(p) && !x.includes('|')) m = Math.max(m, s[x] ?? 0);
    return m;
  }
  return s[k] ?? 0;
};
/** O relógio do motor ("a cada X s", src/engine/unicas-base.ts: relogio): o que falta e o tamanho da volta. */
function relogioDoMotor(f: Fighter): { falta: number; volta: number } | undefined {
  const s = f.u;
  if (!s) return undefined;
  let melhor: { falta: number; volta: number } | undefined;
  for (const k in s) {
    if (!k.startsWith('relogio_') || k.endsWith('_volta')) continue;
    const volta = s[`${k}_volta`];
    if (!volta) continue;
    const falta = Math.max(0, s[k]!);
    if (!melhor || falta / volta < melhor.falta / melhor.volta) melhor = { falta, volta };
  }
  return melhor;
}
/** os segundos com a unidade ("19s"); com 100 ou mais, só o número, para caber */
const segundos = (x: number) => (x >= 99.5 ? `${Math.ceil(x)}` : x >= 1 ? `${Math.ceil(x)}s` : '!');

export function bolinhaNaTela(spec: Bolinha | undefined, f: Fighter, b: Battle): BolinhaNaTela {
  const modo = spec?.modo ?? (relogioDoMotor(f) ? 'relogio' : 'acesa');
  const usada = spec?.usadaSe ? spec.usadaSe(f, b) : !!spec?.usada && !!leia(f, spec.usada);
  const fim = (carga: number, texto?: string, extra?: Partial<BolinhaNaTela>): BolinhaNaTela => {
    const c = Math.max(0, Math.min(1, spec?.valor ? spec.valor(f, b) : carga));
    const luz: LuzDaBolinha = usada ? 'usada' : c >= 1 ? 'pronta' : c >= 0.8 ? 'quase' : 'carregando';
    return { carga: usada ? 1 : c, texto: spec?.texto ? spec.texto(f, b) : usada ? undefined : texto, luz, ...extra };
  };
  switch (modo) {
    case 'relogio': {
      const r = relogioDoMotor(f);
      if (!r) return fim(1);
      return fim(1 - r.falta / r.volta, segundos(r.falta));
    }
    case 'barra': {
      const v = leia(f, spec?.k), max = spec?.max ?? 100;
      return fim(v / max, `${Math.min(99, Math.floor((100 * v) / max))}%`);
    }
    case 'ciclo': {
      const n = spec?.n ?? 1, v = Math.floor(leia(f, spec?.k)) % n;
      return fim(v / n, `${n - v}`);
    }
    case 'conta': {
      const max = spec?.max ?? 1, v = Math.min(max, leia(f, spec?.k));
      return fim(v / max, v >= max ? undefined : `${Math.ceil(max - v)}`);
    }
    case 'pilhas': {
      const max = spec?.max ?? 1, v = Math.min(max, leia(f, spec?.k));
      return fim(v / max, max > 6 ? `${Math.floor(v)}` : undefined, max <= 6 ? { pontos: { tem: Math.floor(v), max } } : undefined);
    }
    case 'tempo': {
      const em = spec?.em ?? 1;
      if (b.time >= em) { const r = fim(1); return r.luz === 'pronta' ? { ...r, luz: 'acesa' } : r; }
      return fim(b.time / em, segundos(em - b.time));
    }
    case 'vida': {
      const lims = spec?.lim ?? [0.5], frac = f.maxHp ? f.hp / f.maxHp : 1;
      const prox = lims.find((l) => frac >= l);
      if (prox === undefined) return fim(1);
      return fim((1 - frac) / Math.max(0.01, 1 - prox), `${Math.round(prox * 100)}`);
    }
    case 'vez': {
      // pronta para o momento dela: acesa e calma (a de recarga enche e mostra os segundos até poder de novo)
      const r = fim(1);
      return r.luz === 'pronta' ? { ...r, luz: 'acesa' } : r;
    }
    case 'chance':
      return { ...fim(1, `${Math.round((spec?.p ?? 0) * 100)}%`), luz: 'acesa' };
    case 'liga': {
      const on = !!spec?.vale?.(f, b);
      const r = fim(on ? 1 : 0.0001);
      return on ? r : { ...r, luz: usada ? 'usada' : 'apagada' };
    }
    default: {
      const r = fim(1);
      return r.luz === 'usada' ? r : { ...r, luz: 'acesa' };
    }
  }
}
