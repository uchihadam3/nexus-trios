/*
 * Banco de provas da tela de resultado da Jornada Ranqueada, com o aviso do
 * Top 3 em cada uma das cinco situações (`?situacao=fora`, `entrou`...).
 *
 * A batalha é de verdade — o motor roda até o fim aqui mesmo —, só a resposta
 * do servidor é inventada: chegar a esta tela pelo jogo levaria dez minutos e
 * uma conta de verdade por situação.
 */
import { createRoot } from 'react-dom/client';

import { ResultScreen } from './screens/ResultScreen';
import { createBattle, stepBattle } from './engine/battle';
import { generateCampaign, newDraft } from './engine/campaign';
import { emptyTally } from './engine/progression';
import type { Run } from './lib/storage';
import type { ResultadoTop3, SituacaoTop3 } from './lib/top3';
import './styles.css';
import './presentation/progress.css';

const situacao = (new URLSearchParams(location.search).get('situacao') ?? 'entrou') as SituacaoTop3;
const exemplos: Record<SituacaoTop3, ResultadoTop3> = {
  novo: { situacao: 'novo', score: 3078971, vagas: 1, precisa_superar: null },
  melhorou: { situacao: 'melhorou', score: 3550000, vagas: 1, precisa_superar: null, anterior: 3078971 },
  manteve: { situacao: 'manteve', score: 2900000, vagas: 1, precisa_superar: null, recorde: 3078971 },
  entrou: { situacao: 'entrou', score: 1550000, vagas: 0, precisa_superar: 1400000, removido: 1300000 },
  fora: { situacao: 'fora', score: 1200000, vagas: 0, precisa_superar: 1300000 },
};

const seed = 528586810, team = ['goku', 'naruto', 'sakura'], encounters = generateCampaign(seed, team);
const battle = createBattle(team, encounters[0].team, seed, encounters[0].scale);
for (let i = 0; i < 9000 && !battle.finished; i++) stepBattle(battle);
const run: Run = {
  seed, team, encounters, index: 0, stage: 'result', draft: newDraft(seed), battle, recorded: true, telemetry: emptyTally(),
  ranked: { mode: 'daily', id: 'probe', status: 'verified', score: exemplos[situacao].score, daily: 4, weekly: null, season: 9,
    top3: { periodo: exemplos[situacao] } },
};
const nada = () => undefined;
createRoot(document.getElementById('root')!).render(
  <main className="app"><ResultScreen run={run} onNext={nada} onRestart={nada} onAbandon={nada} onHome={nada} onRanking={nada} auto={false} onAuto={nada} /></main>,
);
