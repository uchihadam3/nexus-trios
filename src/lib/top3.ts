import { LOCALE, t } from '../i18n/idioma';
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

export const pontos = (n: number): string => n.toLocaleString(LOCALE);

/** "Próxima entrada precisa superar 1.400." ou "1 vaga livre." */
export function situacaoDasVagas(vagas: number, precisaSuperar: number | null): string {
  if (vagas > 0) return vagas === 1 ? t('1 vaga livre.') : t('{n} vagas livres.', { n: vagas });
  return precisaSuperar === null ? '' : t('Próxima entrada precisa superar {p}.', { p: pontos(precisaSuperar) });
}

export function mensagemDoTop3(r: ResultadoTop3): MensagemTop3 {
  const vagas = situacaoDasVagas(r.vagas, r.precisa_superar);
  switch (r.situacao) {
    case 'novo':
      return { titulo: t('NOVO TRIO NO SEU TOP 3'), destaque: true,
        linhas: [t('{p} entrou no ranking.', { p: pontos(r.score) }), vagas].filter(Boolean) };
    case 'melhorou':
      return { titulo: t('RECORDE DO TRIO'), destaque: true,
        linhas: [t('Este trio subiu de {de} para {para}.', { de: pontos(r.anterior ?? 0), para: pontos(r.score) }), t('Continua sendo uma entrada só no ranking.')] };
    case 'manteve':
      return { titulo: t('MESMO TRIO'), destaque: false,
        linhas: [t('{p} pontos.', { p: pontos(r.score) }), t('O recorde deste trio continua {p}.', { p: pontos(r.recorde ?? r.score) })] };
    case 'entrou':
      return { titulo: t('NOVO TOP 3'), destaque: true,
        linhas: [t('{p} entrou no ranking.', { p: pontos(r.score) }), t('O resultado de {p} saiu dos seus 3 melhores.', { p: pontos(r.removido ?? 0) })] };
    case 'fora':
      return { titulo: t('{p} PONTOS', { p: pontos(r.score) }), destaque: false,
        linhas: [t('Não entrou nos seus 3 melhores.'), t('Para entrar: supere {p}.', { p: pontos(r.precisa_superar ?? 0) })] };
  }
}
