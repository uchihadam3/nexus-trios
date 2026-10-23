import { notaDoTrio } from './dicas-do-trio';
import type { TopoMedido } from './posicao-do-trio';

/**
 * "Montar o melhor" (só na conta do dono, no treino), um time por vez (pedido dele: "eu seleciono o time 1 e ele
 * monta o melhor time possível ali… se já tem o Snorlax, monta os outros dois que mais combinam com o Snorlax"):
 *  - o time escolhido com 1 ou 2 personagens fica com eles, e entram os que dão a maior nota com eles (busca completa);
 *  - vazio ou já cheio, monta do zero: vários começos sorteados e, em cada um, troca um por um enquanto a nota sobe;
 *  - nunca usa quem já está nos outros dois times. A nota é a mesma das estrelas (notaDoTrio).
 * Antes de tudo, a lista do topo medido em luta (melhorDoTopo): é dela que sai a posição mostrada no time.
 */
export function melhorTimeAqui(colecao: string[], time: string[], outros: ReadonlySet<string>, topo?: TopoMedido): string[] | null {
  const fixos = time.length === 3 ? [] : time;
  const livres = colecao.filter((id) => !outros.has(id) && !fixos.includes(id));
  if (livres.length < 3 - fixos.length) return null;
  const doTopo = topo && melhorDoTopo(topo, fixos, new Set(livres));
  if (doTopo) return doTopo;
  if (fixos.length === 2) return [...fixos, livres.reduce((a, b) => (notaDoTrio([...fixos, b]) > notaDoTrio([...fixos, a]) ? b : a))];
  if (fixos.length === 1) {
    let melhor: string[] = [], nm = -Infinity;
    for (let a = 0; a < livres.length; a++) for (let b = a + 1; b < livres.length; b++) {
      const t = [fixos[0]!, livres[a]!, livres[b]!], n = notaDoTrio(t);
      if (n > nm) { melhor = t; nm = n; }
    }
    return melhor;
  }
  const ao = () => { const p = [...livres], t: string[] = []; while (t.length < 3) t.push(p.splice(Math.floor(Math.random() * p.length), 1)[0]!); return t; };
  let melhor: string[] = ao(), nm = notaDoTrio(melhor);
  // 30 começos (eram 8, e só 4 em 10 achavam o melhor): aqui a coleção é pequena (a lista do topo não tem nenhum trio dela)
  for (let r = 0; r < 30; r++) {
    let t = ao(), n = notaDoTrio(t);
    for (let mudou = true, voltas = 0; mudou && voltas < 6; voltas++) {
      mudou = false;
      for (let pos = 0; pos < 3; pos++) for (const c of livres) {
        if (t.includes(c)) continue;
        const novo = t.map((x, j) => (j === pos ? c : x)), nn = notaDoTrio(novo);
        if (nn > n + 1e-9) { t = novo; n = nn; mudou = true; }
      }
    }
    if (n > nm) { melhor = t; nm = n; }
  }
  return melhor;
}
/*
 * A posição que aparece no time (1º, 2º…) vem das lutas de verdade dos trios do topo (src/data/topo-medido.ts), não da
 * nota: o trio de nota mais alta aparecia em 342º (pedido do dono: "ele me falou que era o melhor, eu troquei e ficou
 * melhor ainda"). Então o botão procura nessa lista, de cima para baixo, o primeiro trio que dá para montar com quem já está
 * no time e sem os outros dois times; qualquer trio dela fica acima de todos os de fora. Só se nenhum der, vai pela nota.
 */
function melhorDoTopo(topo: TopoMedido, fixos: string[], livres: ReadonlySet<string>): string[] | null {
  for (const chave of topo.lugar.keys()) {
    const t = chave.split('+');
    if (fixos.every((id) => t.includes(id)) && t.every((id) => fixos.includes(id) || livres.has(id))) return [...fixos, ...t.filter((id) => !fixos.includes(id))];
  }
  return null;
}
