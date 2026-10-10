/*
 * Quem vê o botão das Dicas de trio.
 *
 * Pedido do jogador: "o botão de dica não aparece no jogo. Ele só aparece pra
 * pessoa que conseguir fazer um milhão e meio de pontos com algum trio… e pra
 * minha conta ele fica disponível o tempo inteiro".
 *
 * - A conta do dono do jogo vê o botão sempre. O e-mail não fica escrito no
 *   código (o site é público): guardamos só o SHA-256 dele e comparamos com o
 *   SHA-256 do e-mail da conta logada.
 * - Os outros veem o botão trancado e só o ligam depois que o recorde de uma
 *   jornada (a soma dos
 *   pontos das lutas com um trio) chega a META_DAS_DICAS.
 *
 * O jogador escolheu 1,4 milhão. Medido em 6.000 jornadas simuladas de quem
 * escolhe bem o trio: sai em 1 de cada ~120 jornadas, ou 1 em ~16 das que
 * vencem as 10 lutas (1,5 mi: 1 em ~350; 1,3 mi: 1 em ~47).
 */
export const META_DAS_DICAS = 1_400_000;

/** SHA-256 do e-mail (em minúsculas, sem espaços) da conta do dono. */
const DONO = '7574fe4a489f32b6150dbf75d8997670a256e67760194bb0d079c9af4b4b6fe1';

export async function sha256(texto: string): Promise<string> {
  const dados = new TextEncoder().encode(texto);
  const resumo = await crypto.subtle.digest('SHA-256', dados);
  return [...new Uint8Array(resumo)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function ehDono(email: string | null | undefined): Promise<boolean> {
  if (!email || typeof crypto === 'undefined' || !crypto.subtle) return false;
  try { return (await sha256(email.trim().toLowerCase())) === DONO; } catch { return false; }
}

/** O botão aparece? (o dono sempre; os outros depois da meta) */
export const dicasLiberadas = (dono: boolean, recorde: number) => dono || recorde >= META_DAS_DICAS;
