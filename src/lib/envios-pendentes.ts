import { read, save } from './storage';
/*
 * Jornadas terminadas que não chegaram ao servidor (pedido do dono do jogo:
 * "liberei mais um personagem, na hora tem que atualizar o ranking").
 *
 * O envio falhava sem volta quando a internet caía ou o servidor demorava no
 * fim da jornada: os pontos e as Conquistas ficavam só no aparelho, e o
 * ranking mostrava menos do que a tela de Conquistas. Agora o envio que falha
 * por rede fica guardado aqui e é refeito sozinho ao abrir o jogo com a conta
 * conectada. Recusas definitivas (já validada, inexistente, expirada) saem da
 * fila: reenviar não mudaria a resposta.
 */
/** `desistiu`/`lutas`: a jornada fechou pelo botão Desistir depois de `lutas` lutas (conta como perdida). */
/** `pontos`: os pontos que a tela mostrou (o ranking nunca registra mais que isso). */
export interface EnvioPendente { runId: string; digest: string; dicas: boolean; em: string; vencidas?: number; desistiu?: boolean; lutas?: number; pontos?: number }
const CHAVE = 'envios-pendentes';
const DEFINITIVO = /já validada|já enviada|inexistente|expirada|inválid/i;

export function enviosPendentes(): EnvioPendente[] {
  const x = read(CHAVE);
  return Array.isArray(x) ? x.filter((e): e is EnvioPendente => !!e && typeof e.runId === 'string' && typeof e.digest === 'string').slice(-20) : [];
}
export function guardarEnvio(e: EnvioPendente) { save(CHAVE, [...enviosPendentes().filter((x) => x.runId !== e.runId), e]); }
export function tirarEnvio(runId: string) { save(CHAVE, enviosPendentes().filter((x) => x.runId !== runId)); }
/** O erro de envio é definitivo (não adianta tentar de novo)? */
export const recusaDefinitiva = (mensagem: string) => DEFINITIVO.test(mensagem);

/** Reenvia a fila, um por vez. Devolve quantos entraram. */
export async function reenviarPendentes(enviar: (e: EnvioPendente) => Promise<unknown>): Promise<number> {
  let entraram = 0;
  for (const e of enviosPendentes()) {
    try { await enviar(e); tirarEnvio(e.runId); entraram++; }
    catch (erro) { if (recusaDefinitiva(erro instanceof Error ? erro.message : '')) tirarEnvio(e.runId); else break; }
  }
  return entraram;
}
