/*
 * O idioma do jogo (pedido do dono: "colocar o jogo todo em inglês… um botão pra mudar de português pra inglês… nas
 * configurações e na tela de login"). Português é o idioma de origem: todo texto do jogo é escrito em português e passa
 * por t() na hora de aparecer; em inglês, t() procura a tradução no dicionário (src/i18n/en.ts, baixado só por quem joga
 * em inglês). Os dados do motor nunca são traduzidos: o servidor confere os replays com eles, em português.
 *
 * A escolha fica salva no aparelho; trocar recarrega o jogo (os textos montados ao abrir saem no idioma novo).
 */
export type Idioma = 'pt' | 'en';
const CHAVE = 'nexus-v1-idioma';
/* Enquanto o fluxo principal não está todo traduzido, o inglês fica escondido (só aparece com ?idioma=en, para conferir). */
export const INGLES_LIBERADO = false;

function inicial(): Idioma {
  if (typeof window === 'undefined') return 'pt';
  try {
    const pedido = new URLSearchParams(location.search).get('idioma');
    if (pedido === 'pt' || pedido === 'en') { localStorage.setItem(CHAVE, pedido); return pedido; }
    if (!INGLES_LIBERADO) return localStorage.getItem(CHAVE) === 'en' ? 'en' : 'pt';
    const salvo = localStorage.getItem(CHAVE);
    if (salvo === 'pt' || salvo === 'en') return salvo;
  } catch { /* sem armazenamento: segue pelo navegador */ }
  if (!INGLES_LIBERADO) return 'pt';
  return /^pt/i.test(navigator.language || '') ? 'pt' : 'en';
}
export const IDIOMA: Idioma = inicial();
export const LOCALE = IDIOMA === 'en' ? 'en-US' : 'pt-BR';

let dicionario: Readonly<Record<string, string>> = {};
/** Carrega o dicionário do idioma (só em inglês); o jogo só abre depois disso (src/main.tsx). */
export async function carregarIdioma(): Promise<void> {
  if (typeof document !== 'undefined') document.documentElement.lang = IDIOMA === 'en' ? 'en' : 'pt-BR';
  if (IDIOMA === 'en') dicionario = (await import('./en')).EN;
}
/** Para os testes: usa este dicionário. */
export function usarDicionario(d: Readonly<Record<string, string>>): void { dicionario = d; }

/** Troca o idioma e recarrega o jogo. */
export function trocarIdioma(novo: Idioma): void {
  try { localStorage.setItem(CHAVE, novo); } catch { /* sem armazenamento */ }
  const url = new URL(location.href); url.searchParams.delete('idioma');
  location.replace(url.toString());
}

/**
 * O texto no idioma do jogo. `pt` é o texto em português, exatamente como está no código (é a chave do dicionário);
 * `{nome}` no texto é trocado por vars.nome (números no formato do idioma).
 */
export function t(pt: string, vars?: Readonly<Record<string, string | number>>): string {
  let s = IDIOMA === 'en' ? (dicionario[pt] ?? pt) : pt;
  if (vars) s = s.replace(/\{(\w+)\}/g, (m, k: string) => (k in vars ? (typeof vars[k] === 'number' ? numero(vars[k] as number) : String(vars[k])) : m));
  return s;
}
/**
 * Marca um texto que é traduzido depois, onde ele aparece (uma mensagem de erro que viaja numa variável até a tela,
 * que faz t(mensagem)): devolve o próprio texto, e o scripts/i18n-faltando.ts o encontra para conferir a tradução.
 */
export const tx = (pt: string): string => pt;
/** O nome do personagem no idioma do jogo (em inglês, o nome oficial: "nome:<id>" no dicionário). */
export const nomeDe = (c: { id: string; name: string }): string => (IDIOMA === 'en' ? dicionario[`nome:${c.id}`] ?? c.name : c.name);
/** Um número no formato do idioma (1.234 em português, 1,234 em inglês). */
export const numero = (n: number, opcoes?: Intl.NumberFormatOptions) => n.toLocaleString(LOCALE, opcoes);
/** A posição: 5º em português, 5th em inglês. */
export const ordinal = (n: number): string => {
  if (IDIOMA !== 'en') return `${numero(n)}º`;
  const d = n % 100, u = n % 10;
  return `${numero(n)}${d >= 11 && d <= 13 ? 'th' : u === 1 ? 'st' : u === 2 ? 'nd' : u === 3 ? 'rd' : 'th'}`;
};
/** Escolhe o texto pela quantidade: plural(n, 'combo', 'combos'). Os dois textos passam por t(). */
export const plural = (n: number, um: string, varios: string) => t(n === 1 ? um : varios, { n });
