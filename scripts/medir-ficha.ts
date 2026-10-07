/*
 * Quanto texto a ficha joga na tela, antes e depois de agrupar por alvo.
 *
 * "Antes" é a lista plana (`effects` + linha "Alvo"), que é o que a tela
 * mostrava. "Depois" é o que a tela mostra agora: cabeçalhos + linhas.
 */
import { characters } from '../src/data/characters';
import { presentSkill } from '../src/engine/skill-descriptions';

let charsAntes = 0, charsDepois = 0, repetidasAntes = 0, repetidasDepois = 0, alvoEcoAntes = 0, alvoEcoDepois = 0;
const maiorAntes: number[] = [], maiorDepois: number[] = [];
const ALVO = /\b(em si próprio|em todo o trio|em todos os inimigos|no [a-zà-ú ]+?)(?= ·|$)/;

for (const c of characters) for (const s of c.skills) {
  const p = presentSkill(s);
  /* Antes: linhas planas, cada uma podendo dizer o alvo, mais o rodapé. */
  const alvosAntes = p.effects.map((l) => ALVO.exec(l)?.[0] ?? (l.includes(' → ') ? l.split(' → ')[1] : null)).filter(Boolean);
  repetidasAntes += alvosAntes.length - new Set(alvosAntes).size;
  const rodapeAntes = !p.effects.every((l) => /^Aplica |→/.test(l)) && s.effects.length > 0;
  if (rodapeAntes && alvosAntes.length > 0) alvoEcoAntes++;
  for (const l of p.effects) { charsAntes += l.length; maiorAntes.push(l.length); }
  if (rodapeAntes) charsAntes += p.target.length + 6;

  /* Depois: cada cabeçalho uma vez, linhas sem alvo. */
  const titulos = p.grupos.map((g) => g.titulo).filter(Boolean);
  repetidasDepois += titulos.length - new Set(titulos).size;
  for (const g of p.grupos) {
    charsDepois += g.titulo.length;
    for (const l of g.linhas) {
      charsDepois += l.texto.length; maiorDepois.push(l.texto.length);
      if (ALVO.test(l.texto) || l.texto.includes(' → ')) repetidasDepois++;
    }
  }
  if (p.mostrarAlvo) { charsDepois += p.target.length + 6; if (titulos.length > 0) alvoEcoDepois++; }
}
const q = (a: number[], f: number) => [...a].sort((x, y) => x - y)[Math.floor(a.length * f)];
console.log('                                    ANTES    DEPOIS');
console.log(`alvo repetido na mesma ficha        ${String(repetidasAntes).padStart(5)}    ${String(repetidasDepois).padStart(6)}`);
console.log(`linha "Alvo" ecoando                ${String(alvoEcoAntes).padStart(5)}    ${String(alvoEcoDepois).padStart(6)}`);
console.log(`maior linha (caracteres)            ${String(Math.max(...maiorAntes)).padStart(5)}    ${String(Math.max(...maiorDepois)).padStart(6)}`);
console.log(`linha típica, p90 (caracteres)      ${String(q(maiorAntes, .9)).padStart(5)}    ${String(q(maiorDepois, .9)).padStart(6)}`);
console.log(`texto total nas 750 fichas          ${String(charsAntes).padStart(5)}    ${String(charsDepois).padStart(6)}   (${Math.round((1 - charsDepois / charsAntes) * 100)}% menos)`);
