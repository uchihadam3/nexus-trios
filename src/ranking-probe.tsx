/*
 * Banco de provas do ranking (remake). O ranking só aparece com conta e com o
 * servidor, que a rede deste ambiente não alcança; aqui o placar recebe dados
 * de mentira e desenha de verdade. `?estado=placar|meus|historico|sem-conta|
 * carregando|desligado|vazio`.
 */
import { useState } from 'react';
import { createRoot } from 'react-dom/client';

import { Placar, type EstadoDoPlacar } from './screens/RankingScreen';
import type { Leaderboard, PublicRun, RankingDeConquistas } from './lib/online';
import './styles.css';
import './presentation/ui-fx.css';
import './presentation/casca-v2.css';
import './presentation/telas-v2.css';
import './presentation/conquistas.css';

const trios = [['goku', 'pikachu', 'gojo'], ['naruto', 'sakura', 'kakashi'], ['ironman', 'thor', 'hulk'], ['luffy', 'zoro', 'nami'], ['vegeta', 'raven', 'hulk'], ['batman', 'superman', 'wonderwoman'], ['ichigo', 'rukia', 'aizen'], ['sonic', 'tails', 'knuckles']];
const nomes = ['Kaio', 'Uchihadam', 'MariaZ', 'TrioDeOuro', 'Lia_02', 'Rafa', 'NexusFan', 'Bea'];
const linha = (i: number): PublicRun => ({ position: i + 1, id: `r${i}`, handle: nomes[i % nomes.length], score: 10_046_000 - i * 1_013_377, progress: Math.max(3, 10 - i), team: trios[i % trios.length], date: '2026-10-08', seed: 4242, engineVersion: 'nexus-250.4', balanceVersion: 'b', highlights: { survivors: 3 - (i % 3), turns: i % 4 } });
const board: Leaderboard = { mode: 'daily', period: '08/10', entries: Array.from({ length: 8 }, (_, i) => linha(i)), mine: linha(1), details: null, meus: { entries: [linha(1), linha(6)], vagas: 1, precisaSuperar: null }, temMais: true, total: 37 };
const qual = new URLSearchParams(location.search).get('estado') ?? 'placar';
const estados: Record<string, EstadoDoPlacar> = {
  placar: { tipo: 'placar', board }, vazio: { tipo: 'placar', board: { ...board, entries: [], meus: undefined } },
  historico: { tipo: 'historico', partidas: [0, 1, 2].map((i) => ({ id: `h${i}`, mode: i ? 'weekly' : 'daily', period: 'x', score: 4_000_000 - i * 900_000, progress: 10 - i * 3, team: trios[i], date: '2026-10-0' + (8 - i) })) },
  conquistas: { tipo: 'conquistas', ranking: { mode: 'conquistas', de: 250, pagina: 0, total: 41, temMais: true,
    entries: Array.from({ length: 9 }, (_, i) => ({ position: i + 1, id: `p${i}`, handle: nomes[i % nomes.length], total: 87 - i * 9, date: '2026-10-10', ultimos: i < 3 ? trios[i] : [], mine: i === 4 })),
    mine: { position: 5, id: 'p4', handle: 'Uchihadam', total: 51, date: '2026-10-10', ultimos: trios[3], mine: true } } as RankingDeConquistas },
  'sem-conta': { tipo: 'sem-conta' }, carregando: { tipo: 'carregando' }, desligado: { tipo: 'desligado' },
};
function Probe() {
  const [mode, setMode] = useState<'daily' | 'weekly' | 'season' | 'mine' | 'conquistas'>(qual === 'conquistas' ? 'conquistas' : 'daily');
  return <Placar mode={mode} onMode={setMode} estado={estados[qual]} handle="Uchihadam" onConta={() => undefined} onMais={() => undefined} />;
}
createRoot(document.getElementById('root')!).render(<main className="app"><div className="main"><Probe /></div></main>);
