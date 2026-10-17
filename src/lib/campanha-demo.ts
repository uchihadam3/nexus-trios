/*
 * A campanha sem servidor (VITE_CAMPANHA_DEMO=true): só para testar as telas do Caminho do Nexus no navegador; nunca
 * no jogo publicado. Faz o mesmo que o juiz (supabase/functions/ranked-api/campanha.ts), guardando tudo no aparelho.
 */
import { contaParaODescanso, depoisDaPartida, tituloDas, totalDeEstrelas, seuDescanso, escalaDoRival, escolhaDoRival, estrelasDaPartida, liberado, livresParaJogar, lutaDaRodada, quemLutou, rivalPorId, timesDoRival, DESCANSO } from '../engine/campanha';
import { RATING_INICIAL, problemaDosTimes, timesLivres, vencedorDaPartida, type RodadaPvp, type Times } from '../engine/pvp';
import type { PartidaDaCampanha, ProgressoDaCampanha, RespostaDaCampanha, ServicoDaCampanha } from './pvp-online';

interface Guardada extends PartidaDaCampanha { sementes: number[]; sorteios: number[] }
interface Banco { progresso: ProgressoDaCampanha; rating: number; v: number; d: number; partidas: Guardada[] }
const CHAVE = 'nexus-campanha-demo';
const vazio = (): Banco => ({ progresso: { estrelas: {}, placar: {}, descanso: {}, descanso_rivais: {}, partidas: 0 }, rating: RATING_INICIAL, v: 0, d: 0, partidas: [] });
const ler = (): Banco => { try { return { ...vazio(), ...JSON.parse(localStorage.getItem(CHAVE) ?? 'null') }; } catch { return vazio(); } };
const gravar = (b: Banco) => { try { localStorage.setItem(CHAVE, JSON.stringify(b)); } catch { /* sem espaço: segue */ } };
const sorteia = () => crypto.getRandomValues(new Uint32Array(1))[0]! & 0x7fffffff;
const espera = () => new Promise((r) => setTimeout(r, 250));

export function criarCampanhaDemo(colecao: () => string[]): ServicoDaCampanha {
  const resposta = (b: Banco, p: Guardada | null): RespostaDaCampanha => {
    const vista: PartidaDaCampanha | null = p && { id: p.id, rival: p.rival, estado: p.estado, versao: p.versao, meus: p.meus, deles: p.deles, rodadas: p.rodadas, vencedor: p.vencedor,
      motivo: p.motivo, estrelas: p.estrelas, ratingAntes: p.ratingAntes, delta: p.delta, rating: b.rating };
    return { progresso: b.progresso, rating: { rating: b.rating, vitorias: b.v, derrotas: b.d }, colecao: colecao(), partida: vista };
  };
  const terminar = (b: Banco, p: Guardada, vencedor: 'eu' | 'rival', motivo: string) => {
    const rival = rivalPorId(p.rival)!, prog = b.progresso;
    const feitas = b.partidas.filter((x) => x.estado === 'terminada' && x.id !== p.id);
    const meu = (x: Guardada) => quemLutou(x.meus, x.rodadas.map((r) => ({ time: r.meu }))), dele = (x: Guardada) => quemLutou(x.deles, x.rodadas.map((r) => ({ time: r.dele })));
    if (contaParaODescanso(prog.estrelas, rival)) prog.descanso = depoisDaPartida(prog.descanso, [...feitas.slice(-(DESCANSO.janela - 1)), p].map(meu), seuDescanso(rival.regiao, colecao().length));
    prog.descanso_rivais[rival.id] = depoisDaPartida(prog.descanso_rivais[rival.id] ?? {}, [...feitas.filter((x) => x.rival === rival.id).slice(-(DESCANSO.janela - 1)), p].map(dele));
    // o Nexus não mexe no rating do PvP (como no servidor)
    const estrelas = vencedor === 'eu' ? estrelasDaPartida(p) : 0;
    Object.assign(p, { estado: 'terminada', vencedor, motivo, estrelas, ratingAntes: null, delta: null });
    if (estrelas > (prog.estrelas[rival.id] ?? 0)) prog.estrelas[rival.id] = estrelas;
    const placar = prog.placar[rival.id] ?? { v: 0, d: 0 };
    prog.placar[rival.id] = vencedor === 'eu' ? { ...placar, v: placar.v + 1 } : { ...placar, d: placar.d + 1 };
    prog.partidas++;
  };
  const aberta = (b: Banco) => b.partidas.find((x) => x.estado === 'jogando') ?? null;
  const achar = (b: Banco, id: string) => { const p = b.partidas.find((x) => x.id === id); if (!p) throw new Error('Partida não encontrada.'); return p; };
  return {
    estado: async () => { await espera(); const b = ler(); return resposta(b, aberta(b)); },
    // só você no ranking (a demonstração não tem servidor)
    ranking: async () => {
      const b = ler(), estrelas = totalDeEstrelas(b.progresso.estrelas);
      const eu = { posicao: 1, id: 'demo', nome: 'Você', estrelas, partidas: b.progresso.partidas, titulo: tituloDas(estrelas).nome };
      return b.progresso.partidas ? { ranking: [eu], eu, total: 1 } : { ranking: [], eu: null, total: 0 };
    },
    comecar: async (id, times) => {
      await espera();
      const b = ler(), rival = rivalPorId(id);
      if (!rival) throw new Error('Rival não encontrado.');
      if (aberta(b)) throw new Error('Você já tem uma partida da campanha aberta.');
      if (!liberado(b.progresso.estrelas, rival)) throw new Error('Rival bloqueado.');
      const problema = problemaDosTimes(times, new Set(livresParaJogar(colecao(), b.progresso.descanso)));
      if (problema) throw new Error(problema);
      const deles = timesDoRival(rival, sorteia(), Object.keys(b.progresso.descanso_rivais[rival.id] ?? {}), times.flat());
      const p: Guardada = { id: crypto.randomUUID(), rival: rival.id, estado: 'jogando', versao: '', meus: times, deles, rodadas: [], vencedor: null, motivo: null, estrelas: null,
        ratingAntes: null, delta: null, sementes: Array.from({ length: 5 }, sorteia), sorteios: Array.from({ length: 5 }, sorteia) };
      b.partidas = [...b.partidas.slice(-30), p]; gravar(b);
      return resposta(b, p);
    },
    escolher: async (id, n, time) => {
      await espera();
      const b = ler(), p = achar(b, id), rival = rivalPorId(p.rival)!;
      if (p.estado === 'jogando' && n === p.rodadas.length && timesLivres(p, 'eu').includes(time)) {
        const seed = p.sementes[n]!, partida = { meus: p.meus as Times, deles: p.deles as Times, rodadas: p.rodadas as RodadaPvp[], seed: 0 };
        const dele = escolhaDoRival(rival, partida, p.sorteios[n]!, seed), luta = lutaDaRodada(p.meus[time]!, p.deles[dele]!, seed, escalaDoRival(rival));
        p.rodadas = [...p.rodadas, { meu: time, dele, seed, vencedor: luta.winner === 'player' ? 'eu' : 'rival' }];
        const fim = vencedorDaPartida(p);
        if (fim) terminar(b, p, fim, 'venceu com os 3 times');
        gravar(b);
      }
      return resposta(b, p);
    },
    render: async (id, n) => {
      await espera();
      const b = ler(), p = achar(b, id), r = p.rodadas[n];
      if (p.estado === 'jogando' && r && n === p.rodadas.length - 1 && r.vencedor === 'eu') {
        p.rodadas = p.rodadas.map((x, i) => (i === n ? { ...x, vencedor: 'rival' as const, rendida: true } : x));
        if (vencedorDaPartida(p)) terminar(b, p, 'rival', 'venceu com os 3 times');
        gravar(b);
      }
      return resposta(b, p);
    },
    abandonar: async (id) => {
      await espera();
      const b = ler(), p = achar(b, id);
      if (p.estado === 'jogando') { terminar(b, p, 'rival', 'abandonou'); gravar(b); }
      return resposta(b, p);
    },
  };
}
