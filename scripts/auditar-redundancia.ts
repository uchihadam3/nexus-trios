/*
 * Caça a redundância que a direção descreveu no handoff.
 *
 * Dois casos, e os dois enganam o jogador do mesmo jeito: a ficha mostra duas
 * linhas onde só uma tem efeito prático.
 *
 *   1. o mesmo Status aplicado duas vezes na mesma habilidade — o menor é
 *      dominado pelo maior e não acrescenta decisão nenhuma;
 *   2. a mesma fonte de Carga contada duas vezes — para o jogador é um número
 *      só, e mostrar dois é ruído.
 */
import { characters } from '../src/data/characters';

type Achado = { personagem: string; habilidade: string; tipo: string; detalhe: string };
const achados: Achado[] = [];

for (const c of characters) {
  const partes: { nome: string; efeitos: typeof c.basic.effects; carga?: { on: string }[] }[] = [
    { nome: 'ataque básico', efeitos: c.basic.effects },
    { nome: c.trait.name, efeitos: c.trait.effects },
    ...c.skills.map((s) => ({ nome: s.name, efeitos: s.effects, carga: s.charge })),
  ];

  for (const parte of partes) {
    const porStatus = new Map<string, number[]>();
    for (const e of parte.efeitos) {
      if (e.kind !== 'status') continue;
      const chave = `${e.status}:${e.target ?? 'padrão'}`;
      porStatus.set(chave, [...(porStatus.get(chave) ?? []), e.value]);
    }
    for (const [chave, valores] of porStatus) {
      if (valores.length < 2) continue;
      achados.push({
        personagem: c.name, habilidade: parte.nome, tipo: 'Status repetido',
        detalhe: `${chave} ×${String(valores.length)} (${valores.map((v) => v.toFixed(2)).join(', ')})`,
      });
    }

    const porTopico = new Map<string, number>();
    for (const r of parte.carga ?? []) porTopico.set(r.on, (porTopico.get(r.on) ?? 0) + 1);
    for (const [topico, n] of porTopico) {
      if (n < 2) continue;
      achados.push({
        personagem: c.name, habilidade: parte.nome, tipo: 'Carga duplicada',
        detalhe: `${topico} aparece ${String(n)} vezes`,
      });
    }
  }
}

const porTipo = new Map<string, number>();
for (const a of achados) porTipo.set(a.tipo, (porTipo.get(a.tipo) ?? 0) + 1);
console.log(`personagens auditados: ${String(characters.length)}`);
console.log(`achados: ${String(achados.length)}`, Object.fromEntries(porTipo));
for (const a of achados.slice(0, 40)) {
  console.log(`  ${a.personagem} · ${a.habilidade} · ${a.tipo} · ${a.detalhe}`);
}
if (achados.length > 40) console.log(`  ... e mais ${String(achados.length - 40)}`);

if (achados.length > 0) process.exitCode = 1;
