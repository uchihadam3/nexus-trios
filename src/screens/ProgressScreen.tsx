/*
 * FASE H · a tela de Progresso.
 *
 * Três abas, não quatro: os Objetivos saíram. A razão está escrita em
 * `engine/progression.ts`, e o resumo é que diários e semanais são um
 * calendário num jogo que se abre quando dá vontade, e os de jornada sumiam
 * sem deixar rastro.
 *
 * O que ficou é o que vale guardar: 52 conquistas de momento, a Maestria dos
 * 250, e os números da sua história. Nenhum deles altera um atributo de
 * personagem — é prestígio, como o documento exige.
 */
import { useState } from 'react';
import { Award, ChartNoAxesCombined, Search, Sparkles, Trophy } from 'lucide-react';

import { characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { conquistas, categorias, type Categoria } from '../engine/conquistas';
import { desafiosDe, grauAlcancado } from '../engine/maestria';
import { dominados, nexusLevel } from '../engine/progression';
import type { Profile } from '../lib/storage';

const abas = ['Conquistas', 'Maestria', 'Estatísticas'] as const;
const ROMANOS = ['—', 'I', 'II', 'III'] as const;

const semAcento = (t: string) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

export function ProgressScreen({ profile }: { profile: Profile }) {
  const [aba, setAba] = useState<(typeof abas)[number]>('Conquistas');
  const [busca, setBusca] = useState('');
  const [escolhido, setEscolhido] = useState('goku');
  const [categoria, setCategoria] = useState<Categoria | 'Todas'>('Todas');

  const p = profile.progress;
  const nivel = nexusLevel(p.xp);
  const proximo = nivel * nivel * 100, anterior = (nivel - 1) ** 2 * 100;
  const avanco = Math.min(100, 100 * (p.xp - anterior) / Math.max(1, proximo - anterior));
  const mestres = dominados(p);

  const encontrados = characters.filter((c) => semAcento(`${c.name} ${c.universe}`).includes(semAcento(busca)));
  const atual = encontrados.find((c) => c.id === escolhido) ?? encontrados[0];
  const feitos = atual ? p.mastery[atual.id] ?? {} : {};
  const grau = atual ? grauAlcancado(atual.id, feitos) : 0;

  const visiveis = conquistas.filter((c) => categoria === 'Todas' || c.categoria === categoria);

  return <section className="progress-screen">
    <div className="screen-title">
      <span className="eyebrow"><Sparkles size={14} /> PROGRESSO NEXUS</span>
      <h1>Cada trio deixa uma história.</h1>
      <p>Conquistas e Maestria ficam neste dispositivo e continuam disponíveis sem conexão.</p>
    </div>

    <div className="progress-overview">
      <div><small>NÍVEL NEXUS</small><strong>{nivel}</strong><span>{p.title}</span></div>
      <div className="progress-xp">
        <strong>{p.xp.toLocaleString('pt-BR')} XP</strong>
        <div><i style={{ width: `${String(avanco)}%` }} /></div>
        <small>Próximo nível: {proximo.toLocaleString('pt-BR')} XP</small>
      </div>
      <div><small>LUTADORES EXPERIMENTADOS</small><strong>{p.seen.length}<span> / {characters.length}</span></strong>
        <span>{Math.round(100 * p.seen.length / characters.length)}% do elenco</span></div>
      <div><small>LUTADORES DOMINADOS</small><strong>{mestres}<span> / {characters.length}</span></strong>
        <span>Maestria III</span></div>
    </div>

    <nav className="progress-tabs" aria-label="Seções do progresso">
      {abas.map((x) => <button key={x} className={aba === x ? 'active' : ''} onClick={() => setAba(x)}>{x}</button>)}
    </nav>

    {aba === 'Conquistas' && <section className="progress-panel">
      <h2><Award size={21} /> Conquistas · {p.unlocked.length} / {conquistas.length}</h2>
      <div className="conquista-filtros">
        <button className={categoria === 'Todas' ? 'active' : ''} onClick={() => setCategoria('Todas')}>Todas</button>
        {categorias.map((c) => <button key={c} className={categoria === c ? 'active' : ''} onClick={() => setCategoria(c)}>{c}</button>)}
      </div>
      <div className="achievement-grid">{visiveis.map((c) => {
        const temos = p.unlocked.includes(c.id);
        /*
         * Segredo só revela a dica depois de conquistado. Antes disso, a carta
         * diz que existe — esconder a existência seria esconder o jogo.
         */
        const oculta = c.secreta && !temos;
        return <article key={c.id} className={`${temos ? 'unlocked' : ''} ${oculta ? 'secreta' : ''}`}>
          <small>{c.categoria}</small>
          <strong>{oculta ? '???' : c.nome}</strong>
          <span>{oculta ? 'Segredo · descubra jogando' : c.dica}</span>
        </article>;
      })}</div>
    </section>}

    {aba === 'Maestria' && <section className="progress-panel">
      <h2><Trophy size={21} /> Maestria · {mestres} dominados</h2>
      <label className="search"><Search size={18} />
        <input aria-label="Buscar maestria" placeholder={`Buscar entre ${String(characters.length)} lutadores…`}
          value={busca} onChange={(e) => setBusca(e.target.value)} /></label>
      <div className="mastery-layout">
        <div className="mastery-list">
          {encontrados.slice(0, 40).map((c) => <button key={c.id} className={atual?.id === c.id ? 'active' : ''} onClick={() => setEscolhido(c.id)}>
            <Portrait character={c} /><span>{c.name}</span>
            <small>{ROMANOS[grauAlcancado(c.id, p.mastery[c.id] ?? {})]} / III</small>
          </button>)}
          {encontrados.length > 40 && <small>Refine a busca para ver mais lutadores.</small>}
        </div>
        {atual ? <article className="mastery-card">
          <Portrait character={atual} />
          <div><span className="eyebrow">{atual.universe}</span><h3>{atual.name}</h3>
            <strong>MAESTRIA {ROMANOS[grau]} / III</strong></div>
          <ol>{desafiosDe(atual.id).map((d, i) => {
            const feito = feitos[d.feito] ?? 0;
            const completo = feito >= d.meta;
            return <li key={d.grau} className={completo ? 'done' : i === grau ? 'next' : ''}>
              <b>{d.grau}</b> {d.titulo}
              <span>{Math.min(feito, d.meta).toLocaleString('pt-BR')} / {d.meta.toLocaleString('pt-BR')}</span>
            </li>;
          })}</ol>
        </article> : <p>Nenhum lutador encontrado.</p>}
      </div>
    </section>}

    {aba === 'Estatísticas' && <section className="progress-panel">
      <h2><ChartNoAxesCombined size={21} /> A sua história</h2>
      <div className="stat-grid">
        {([
          ['Jornadas', p.stats.journeys], ['Jornadas vencidas', p.stats.champions],
          ['Confrontos', p.stats.battles], ['Confrontos vencidos', p.stats.wins],
          ['Vitórias com os três de pé', p.stats.perfect], ['Inimigos derrubados', p.stats.kos],
          ['Dano causado', p.stats.damage], ['Vida devolvida', p.stats.healing],
          ['Dano bloqueado', p.stats.protection], ['Preparos interrompidos', p.stats.interrupts],
          ['Status aplicados', p.stats.statuses], ['Conexões de Carga', p.stats.synergies],
          ['Recorde da trilha', profile.best], ['Habilidades vistas', p.stats.skills],
        ] as const).map(([rotulo, valor]) => <article key={rotulo}>
          <strong>{Math.round(valor).toLocaleString('pt-BR')}</strong><small>{rotulo}</small>
        </article>)}
      </div>
    </section>}
  </section>;
}
