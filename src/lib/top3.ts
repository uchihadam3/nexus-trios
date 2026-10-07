/*
 * FASE K · o que dizer ao jogador sobre os seus 3 melhores trios.
 *
 * As frases são as do documento, ao pé da letra — "Não entrou nos seus 3
 * melhores.", "Para entrar: supere 1.300.", "NOVO TOP 3" — porque são elas
 * que explicam a regra sem tutorial. Ficam aqui, puras, e não espalhadas
 * pelas telas, para a tela de resultado e o ranking dizerem a mesma coisa.
 *
 * Quem decide o que aconteceu é o banco (`registrar_no_top3`); esta camada só
 * traduz a resposta.
 */
export type SituacaoTop3 = 'novo' | 'melhorou' | 'manteve' | 'entrou' | 'fora';
export interface ResultadoTop3 {
  situacao: SituacaoTop3;
  score: number;
  vagas: number;
  precisa_superar: number | null;
  anterior?: number;
  recorde?: number;
  removido?: number;
}
export interface MensagemTop3 { titulo: string; linhas: string[]; destaque: boolean }

export const pontos = (n: number): string => n.toLocaleString('pt-BR');

/** "Próxima entrada precisa superar 1.400." ou "1 vaga livre." */
export function situacaoDasVagas(vagas: number, precisaSuperar: number | null): string {
  if (vagas > 0) return vagas === 1 ? '1 vaga livre.' : `${vagas} vagas livres.`;
  return precisaSuperar === null ? '' : `Próxima entrada precisa superar ${pontos(precisaSuperar)}.`;
}

export function mensagemDoTop3(r: ResultadoTop3): MensagemTop3 {
  const vagas = situacaoDasVagas(r.vagas, r.precisa_superar);
  switch (r.situacao) {
    case 'novo':
      return { titulo: 'NOVO TRIO NO SEU TOP 3', destaque: true,
        linhas: [`${pontos(r.score)} entrou no ranking.`, vagas].filter(Boolean) };
    case 'melhorou':
      return { titulo: 'RECORDE DO TRIO', destaque: true,
        linhas: [`Este trio subiu de ${pontos(r.anterior ?? 0)} para ${pontos(r.score)}.`, 'Continua sendo uma entrada só no ranking.'] };
    case 'manteve':
      return { titulo: 'MESMO TRIO', destaque: false,
        linhas: [`${pontos(r.score)} pontos.`, `O recorde deste trio continua ${pontos(r.recorde ?? r.score)}.`] };
    case 'entrou':
      return { titulo: 'NOVO TOP 3', destaque: true,
        linhas: [`${pontos(r.score)} entrou no ranking.`, `O resultado de ${pontos(r.removido ?? 0)} saiu dos seus 3 melhores.`] };
    case 'fora':
      return { titulo: `${pontos(r.score)} PONTOS`, destaque: false,
        linhas: ['Não entrou nos seus 3 melhores.', `Para entrar: supere ${pontos(r.precisa_superar ?? 0)}.`] };
  }
}
