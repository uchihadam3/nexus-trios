import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { BookOpen, Castle, ChevronLeft, ChevronRight, Crown, Globe, Link2, Lock, Sparkles, X, type LucideIcon } from 'lucide-react';
import { CartaDoCombo, TODOS_OS_COMBOS, visualDoCombo, type TipoDeCombo } from '../components/CombosDoTrio';

/*
 * O Livro de Combos (pedido do jogador: sair do "Como jogar" e ficar na tela
 * inicial, "muito bonito e muito gamificado e sem scroll" — e depois: "bem
 * animado, igualzinho a parte das Conquistas").
 *
 * Todos começam apagados: só o nome aparece — nem o que forma o combo, nem o
 * que ele faz. O jogador descobre jogando: quando o trio dele forma um combo,
 * ou quando ele vê o rival usar um, a peça acende aqui (src/App.tsx, no começo
 * de cada luta) e passa a abrir a ficha completa.
 *
 * Como nas Conquistas: o anel que enche e o título do colecionador no topo, as
 * abas com a barrinha, e as páginas num trilho que passa de lado junto com o
 * dedo e encaixa (scroll-snap), com os pontinhos e as setas embaixo. Sem scroll
 * para baixo: a grade mede o espaço que sobra e cada página traz o que cabe.
 */
const ABAS: { id: TipoDeCombo; nome: string; icone: LucideIcon; cor: string }[] = [
  { id: 'duplas', nome: 'Duplas', icone: Link2, cor: '#8fd3ff' },
  { id: 'trios', nome: 'Trios', icone: Castle, cor: '#c58cff' },
  { id: 'universo', nome: 'Universo', icone: Globe, cor: '#86e3a8' },
  { id: 'lendarias', nome: 'Lendárias', icone: Crown, cor: '#ffd36b' },
];
/** O título do colecionador, pela fração do livro descoberta. */
const TITULOS = [
  { fracao: 0, nome: 'Curioso', cor: '#9fb3c2' },
  { fracao: 0.1, nome: 'Aprendiz de combos', cor: '#86e3a8' },
  { fracao: 0.25, nome: 'Estrategista', cor: '#8fd3ff' },
  { fracao: 0.45, nome: 'Mestre dos combos', cor: '#c58cff' },
  { fracao: 0.7, nome: 'Lenda dos combos', cor: '#ffd36b' },
  { fracao: 1, nome: 'Enciclopédia viva', cor: '#ff9f5a' },
];
/** O tamanho mínimo de cada peça da grade (px); a grade divide o espaço que sobra entre elas. */
const PECA = { largura: 104, altura: 84, vao: 8 };

export function LivroDeCombos({ descobertos, vistos, onVer }: { descobertos: readonly string[]; vistos: readonly string[]; onVer: (id: string) => void }) {
  const [aba, setAba] = useState<TipoDeCombo>('duplas');
  const [pagina, setPagina] = useState(0);
  const [aberto, setAberto] = useState<string | null>(null), [trancado, setTrancado] = useState<string | null>(null);
  const [grade, setGrade] = useState({ colunas: 3, linhas: 4 });
  const caixa = useRef<HTMLDivElement>(null), trilho = useRef<HTMLDivElement>(null);
  /* o que já estava visto ao abrir: o selo NOVO fica na tela enquanto ela estiver aberta */
  const [vistosAoAbrir] = useState(() => new Set(vistos));

  // quantas peças cabem: mede o espaço da grade (muda com a tela e ao girar o celular)
  useLayoutEffect(() => {
    const el = caixa.current;
    if (!el) return;
    const mede = () => {
      const { width, height } = el.getBoundingClientRect();
      // celular deitado (pouca altura): a peça fica deitada também, com o ícone ao lado do nome (livro.css)
      const baixa = innerHeight < 520, largura = baixa ? 150 : PECA.largura, altura = baixa ? 50 : PECA.altura;
      const n = { colunas: Math.max(2, Math.floor((width + PECA.vao) / (largura + PECA.vao))), linhas: Math.max(1, Math.floor((height + PECA.vao) / (altura + PECA.vao))) };
      setGrade((g) => (n.colunas === g.colunas && n.linhas === g.linhas ? g : n));
    };
    mede();
    const ro = new ResizeObserver(mede);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const aceso = (id: string) => descobertos.includes(id);
  const lista = useMemo(() => TODOS_OS_COMBOS.filter((c) => c.tipo === aba), [aba]);
  const porPagina = grade.colunas * grade.linhas;
  const folhas = useMemo(() => Array.from({ length: Math.max(1, Math.ceil(lista.length / porPagina)) }, (_, i) => lista.slice(i * porPagina, (i + 1) * porPagina)), [lista, porPagina]);
  const total = TODOS_OS_COMBOS.length, achados = TODOS_OS_COMBOS.filter((c) => aceso(c.id)).length, fracao = achados / total;
  let nivel = 0;
  while (nivel + 1 < TITULOS.length && fracao >= TITULOS[nivel + 1]!.fracao) nivel++;
  const titulo = TITULOS[nivel]!, proximo = TITULOS[nivel + 1];
  const faltamProximo = proximo ? Math.max(1, Math.ceil(proximo.fracao * total) - achados) : 0;
  const progressoNivel = proximo ? (fracao - titulo.fracao) / (proximo.fracao - titulo.fracao) : 1;
  const corDaAba = ABAS.find((a) => a.id === aba)!.cor;

  const irPara = (p: number, suave = true) => {
    const t = trilho.current, alvo = Math.max(0, Math.min(folhas.length - 1, p));
    t?.scrollTo({ left: alvo * t.clientWidth, behavior: suave ? 'smooth' : 'auto' });
    setPagina(alvo);
  };
  useEffect(() => { if (!trancado) return; const t = window.setTimeout(() => setTrancado(null), 2600); return () => clearTimeout(t); }, [trancado]);
  // a grade mudou de tamanho (girou o celular): fica na página que ainda existe
  useEffect(() => { if (pagina > folhas.length - 1) irPara(folhas.length - 1, false); }, [folhas.length]);
  const trocaAba = (a: TipoDeCombo) => { if (a === aba) return; setAba(a); setPagina(0); trilho.current?.scrollTo({ left: 0 }); };
  const abre = (id: string) => { if (aceso(id)) { setAberto(id); onVer(id); } else setTrancado(id); };
  const R = 44, C = 2 * Math.PI * R;

  return <section className="lc" aria-label="Livro de Combos">
    <header className="lc-topo" style={{ '--titulo': titulo.cor } as CSSProperties}>
      <div className="lc-anel" aria-label={`${achados} de ${total} descobertos`}>
        <svg viewBox="0 0 100 100"><circle className="lc-anel-fundo" cx="50" cy="50" r={R} /><circle className="lc-anel-cheio" cx="50" cy="50" r={R} style={{ strokeDasharray: `${C * fracao} ${C}` }} /></svg>
        <span><BookOpen size={13} /><b>{achados}</b><small>de {total}</small></span>
      </div>
      <div className="lc-titulo">
        <span className="lc-nivel">LIVRO DE COMBOS · NÍVEL {nivel + 1}</span>
        <strong>{titulo.nome}</strong>
        <div className="lc-barra"><i style={{ width: `${Math.round(progressoNivel * 100)}%` }} /></div>
        <small>{proximo ? <>Faltam <b>{faltamProximo}</b> para <b style={{ color: proximo.cor }}>{proximo.nome}</b><span> · monte trios ou veja os rivais</span></> : <>Você descobriu todos os combos!</>}</small>
      </div>
    </header>

    <nav className="lc-abas" role="tablist">{ABAS.map((a) => {
      const Ic = a.icone, dela = TODOS_OS_COMBOS.filter((c) => c.tipo === a.id), n = dela.filter((c) => aceso(c.id)).length;
      const novos = dela.filter((c) => aceso(c.id) && !vistos.includes(c.id)).length;
      return <button key={a.id} role="tab" aria-selected={aba === a.id} className={aba === a.id ? 'ativa' : ''} style={{ '--aba': a.cor } as CSSProperties} onClick={() => trocaAba(a.id)}>
        <Ic size={16} /><b>{a.nome}</b><small>{n}/{dela.length}</small><i style={{ width: `${(100 * n) / Math.max(1, dela.length)}%` }} />{novos > 0 && <em>{novos}</em>}
      </button>;
    })}</nav>

    <div className="lc-album" style={{ '--aba': corDaAba } as CSSProperties}>
      <div className="lc-grade-caixa" ref={caixa}>
        <div className="lc-trilho" ref={trilho} onScroll={(e) => { const t = e.currentTarget, p = Math.round(t.scrollLeft / Math.max(1, t.clientWidth)); if (p !== pagina) setPagina(p); }}>
          {folhas.map((folha, fi) => <div key={`${aba}-${fi}`} className="lc-grade" style={{ gridTemplateColumns: `repeat(${grade.colunas},minmax(0,1fr))`, gridTemplateRows: `repeat(${grade.linhas},minmax(0,1fr))` }}>
            {folha.map((c, i) => {
              const v = visualDoCombo(c.id), Icone = v.icone, on = aceso(c.id), novo = on && !vistosAoAbrir.has(c.id);
              return <button key={c.id} type="button" className={`lc-peca ${on ? `acesa ${v.raridade}` : 'apagada'} ${novo ? 'nova' : ''} ${trancado === c.id ? 'treme' : ''}`}
                style={{ '--cb': c.tipo === 'lendarias' ? '#ffd36b' : v.cor, '--i': i } as CSSProperties} onClick={() => abre(c.id)}
                aria-label={on ? `${c.nome}: ver a ficha` : `${c.nome}: ainda não descoberto`}>
                <span className="lc-selo">{on ? <Icone size={20} /> : <Lock size={16} />}</span>
                <b>{c.nome}</b>
                {novo && <em>NOVO</em>}
              </button>;
            })}
          </div>)}
        </div>
      </div>
      <footer className="lc-rodape">
        {trancado ? <p className="lc-dica" role="status"><Lock size={14} />Ainda escondido. Forme este combo no seu trio, ou veja um rival usar.</p>
          : folhas.length > 1 && <div className="lc-paginas">
            <button className="lc-seta" onClick={() => irPara(pagina - 1)} disabled={pagina === 0} aria-label="Página anterior"><ChevronLeft size={18} /></button>
            <span className="lc-pontos">{folhas.map((_, i) => <button key={i} className={i === pagina ? 'ativo' : ''} aria-label={`Página ${i + 1}`} onClick={() => irPara(i)} />)}</span>
            <button className="lc-seta" onClick={() => irPara(pagina + 1)} disabled={pagina >= folhas.length - 1} aria-label="Próxima página"><ChevronRight size={18} /></button>
          </div>}
      </footer>
    </div>

    {aberto && <div className="lc-veu" role="dialog" aria-modal="true" aria-label="Ficha do combo" onClick={() => setAberto(null)}>
      <div className="lc-ficha" onClick={(e) => e.stopPropagation()}>
        <span className="lc-ficha-brilho" aria-hidden><Sparkles size={16} /></span>
        <CartaDoCombo id={aberto} />
        <button className="lc-fechar" onClick={() => setAberto(null)} aria-label="Fechar a ficha"><X size={18} /></button>
      </div>
    </div>}
  </section>;
}
