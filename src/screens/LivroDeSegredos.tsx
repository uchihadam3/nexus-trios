import { useEffect, useState, type CSSProperties } from 'react';
import { KeyRound, Lock, Sparkles, Star, Crown, Gift, SkipForward } from 'lucide-react';
import { PULOS_COM_O_LIVRO_COMPLETO, PULOS_DA_JORNADA, SEGREDOS } from '../engine/segredos';
import { ICONE_DO_SEGREDO, NOME_DA_LUTA, ONDE_FICA } from '../components/SeloDoSegredo';
import '../presentation/segredos.css';
import { t } from '../i18n/idioma';

/*
 * O Livro de Segredos (pedido do jogador: "seis segredos… bem gamificado"). As seis cartas começam trancadas, só com
 * a charada e a luta extra que liberam; cumprido o segredo numa jornada (src/App.tsx), a carta acende com o nome e a
 * regra. Cabe na tela do celular: duas colunas de três.
 */
const TITULOS = ['Curioso', 'Farejador', 'Detetive', 'Caçador de segredos', 'Guardião dos segredos', 'Mestre dos segredos', 'Lenda oculta'];

export function LivroDeSegredos({ descobertos, vistos, onVer }: { descobertos: readonly string[]; vistos: readonly string[]; onVer: (ids: string[]) => void }) {
  /* o que já estava visto ao abrir: o selo NOVO fica na tela enquanto ela estiver aberta */
  const [vistosAoAbrir] = useState(() => new Set(vistos));
  const achados = SEGREDOS.filter((s) => descobertos.includes(s.id)), n = achados.length;
  useEffect(() => {
    const novos = achados.filter((s) => !vistos.includes(s.id)).map((s) => s.id);
    if (novos.length) onVer(novos);
    // marca uma vez, ao abrir
  }, []);
  const anel = 2 * Math.PI * 38;
  return <section className="sg" aria-label={t('Livro de Segredos')}>
    <header className="sg-topo">
      <div className="sg-anel">
        <svg viewBox="0 0 86 86" aria-hidden="true"><circle className="sg-anel-fundo" cx="43" cy="43" r="38" /><circle className="sg-anel-cheio" cx="43" cy="43" r="38" strokeDasharray={`${(anel * n) / 6} ${anel}`} /></svg>
        <span><KeyRound size={16} /><b>{n}</b><small>{t('de')} 6</small></span>
      </div>
      <div className="sg-titulo">
        <span className="sg-nivel">{t('LIVRO DE SEGREDOS')}</span>
        <strong>{t(TITULOS[n]!)}</strong>
        <small>{t('Cada segredo cumprido abre uma luta extra na jornada. Ela só vale pontos se você vencer.')}</small>
      </div>
    </header>
    <div className={`sg-premio ${n === 6 ? 'ganho' : ''}`} role="note">
      <span className="sg-premio-icone">{n === 6 ? <SkipForward size={22} /> : <Gift size={22} />}</span>
      <div>
        <small>{n === 6 ? t('PRÊMIO GANHO!') : t('PRÊMIO DOS 6 SEGREDOS')}</small>
        <b>{t('+1 pulo para sempre')}</b>
        <span>{n === 6 ? t('Agora você tem {n} pulos para trocar as opções na escolha do trio, em vez de {antes}.', { n: PULOS_COM_O_LIVRO_COMPLETO, antes: PULOS_DA_JORNADA }) : t('Descubra os 6 e a escolha do trio passa a ter {n} pulos em vez de {antes}. Faltam {faltam}.', { n: PULOS_COM_O_LIVRO_COMPLETO, antes: PULOS_DA_JORNADA, faltam: 6 - n })}</span>
      </div>
    </div>
    <div className="sg-lutas" aria-hidden="true">
      {[1, 2, 3, 4, 5].map((i) => <i key={i}>{i}</i>)}<i className="extra"><Star size={11} fill="currentColor" /></i>
      {[6, 7, 8, 9, 10].map((i) => <i key={i}>{i === 10 ? <Crown size={11} /> : i}</i>)}<i className="extra">11</i>
    </div>
    <ul className="sg-grade">
      {SEGREDOS.map((s, i) => {
        const ok = descobertos.includes(s.id), novo = ok && !vistosAoAbrir.has(s.id), Ic = ICONE_DO_SEGREDO[s.id];
        return <li key={s.id} className={`sg-carta ${ok ? 'aberta' : 'trancada'}`} style={{ '--cor': s.cor, '--i': i } as CSSProperties}>
          {novo && <em className="sg-novo">{t('NOVO')}</em>}
          <span className="sg-selo">{ok ? <Ic size={22} /> : <Lock size={18} />}</span>
          <b className="sg-nome">{ok ? t(s.nome) : t('Segredo trancado')}</b>
          <p className="sg-texto">{ok ? t(s.regra) : <i>“{t(s.charada)}”</i>}</p>
          <span className="sg-libera">{s.libera.map((q) => <span key={q} title={`${t(NOME_DA_LUTA[q])}, ${t(ONDE_FICA[q])}`}>{q === 'onze' && <Sparkles size={10} />}{t(NOME_DA_LUTA[q])}</span>)}</span>
        </li>;
      })}
    </ul>
  </section>;
}
