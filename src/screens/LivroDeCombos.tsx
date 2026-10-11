import { useEffect, useLayoutEffect, useRef, useState, type CSSProperties, type PointerEvent } from 'react';
import { BookOpen, Castle, ChevronLeft, ChevronRight, Crown, Globe, Link2, Lock, Sparkles, X, type LucideIcon } from 'lucide-react';
import { CartaDoCombo, TODOS_OS_COMBOS, visualDoCombo, type TipoDeCombo } from '../components/CombosDoTrio';

/*
 * O Livro de Combos (pedido do jogador: sair do "Como jogar" e ficar na tela
 * inicial, "muito bonito e muito gamificado e sem scroll").
 *
 * Todos começam apagados: só o nome aparece — nem o que forma o combo, nem o
 * que ele faz. O jogador descobre jogando: quando o trio dele forma um combo,
 * ou quando ele vê o rival usar um, a peça acende aqui (src/App.tsx, no começo
 * de cada luta) e passa a abrir a ficha completa.
 *
 * Sem scroll: a grade mede o espaço que sobra na tela e mostra uma página de
 * peças que cabe nele; as outras páginas vêm pelas setas, pelos pontinhos ou
 * arrastando o dedo para o lado.
 */
const ABAS: { id: TipoDeCombo; nome: string; icone: LucideIcon; cor: string }[] = [
  { id: 'duplas', nome: 'Duplas', icone: Link2, cor: '#8fd3ff' },
  { id: 'trios', nome: 'Trios', icone: Castle, cor: '#c58cff' },
  { id: 'universo', nome: 'Universo', icone: Globe, cor: '#86e3a8' },
  { id: 'lendarias', nome: 'Lendárias', icone: Crown, cor: '#ffd36b' },
];
/** O tamanho mínimo de cada peça da grade (px); a grade divide o espaço que sobra entre elas. */
const PECA = { largura: 104, altura: 84, vao: 8 };

export function LivroDeCombos({ descobertos, vistos, onVer }: { descobertos: readonly string[]; vistos: readonly string[]; onVer: (id: string) => void }) {
  const [aba, setAba] = useState<TipoDeCombo>('duplas');
  const [pagina, setPagina] = useState(0), [ida, setIda] = useState<1 | -1>(1);
  const [aberto, setAberto] = useState<string | null>(null), [trancado, setTrancado] = useState<string | null>(null);
  const [grade, setGrade] = useState({ colunas: 3, linhas: 4 });
  const caixa = useRef<HTMLDivElement>(null), toque = useRef<number | null>(null);

  // quantas peças cabem: mede o espaço da grade (muda com a tela e ao girar o celular)
  useLayoutEffect(() => {
    const el = caixa.current;
    if (!el) return;
    const mede = () => {
      const { width, height } = el.getBoundingClientRect();
      // celular deitado (pouca altura): a peça fica deitada também, com o ícone ao lado do nome (livro.css)
      const baixa = innerHeight < 520, largura = baixa ? 150 : PECA.largura, altura = baixa ? 50 : PECA.altura;
      setGrade({
        colunas: Math.max(2, Math.floor((width + PECA.vao) / (largura + PECA.vao))),
        linhas: Math.max(1, Math.floor((height + PECA.vao) / (altura + PECA.vao))),
      });
    };
    mede();
    const ro = new ResizeObserver(mede);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const lista = TODOS_OS_COMBOS.filter((c) => c.tipo === aba);
  const porPagina = grade.colunas * grade.linhas, paginas = Math.max(1, Math.ceil(lista.length / porPagina));
  const atual = Math.min(pagina, paginas - 1), daPagina = lista.slice(atual * porPagina, (atual + 1) * porPagina);
  const aceso = (id: string) => descobertos.includes(id);
  const total = TODOS_OS_COMBOS.length, achados = TODOS_OS_COMBOS.filter((c) => aceso(c.id)).length;

  useEffect(() => { if (!trancado) return; const t = window.setTimeout(() => setTrancado(null), 2600); return () => clearTimeout(t); }, [trancado]);
  const vai = (d: 1 | -1) => { const p = atual + d; if (p < 0 || p >= paginas) return; setIda(d); setPagina(p); };
  const trocaAba = (a: TipoDeCombo) => { setAba(a); setPagina(0); setIda(1); };
  const abre = (id: string) => { if (aceso(id)) { setAberto(id); onVer(id); } else setTrancado(id); };
  // arrastar o dedo para o lado troca de página
  const desce = (e: PointerEvent) => { toque.current = e.clientX; };
  const sobe = (e: PointerEvent) => { if (toque.current === null) return; const dx = e.clientX - toque.current; toque.current = null; if (Math.abs(dx) > 50) vai(dx < 0 ? 1 : -1); };

  return <section className="lc" aria-label="Livro de Combos">
    <header className="lc-topo">
      <span className="lc-anel" style={{ '--p': achados / total } as CSSProperties}><BookOpen size={22} /></span>
      <div className="lc-titulo">
        <h1>LIVRO DE COMBOS</h1>
        <p><b>{achados}</b>/{total} descobertos <span>· monte trios ou veja os rivais para revelar</span></p>
        <span className="lc-barra"><i style={{ width: `${(100 * achados) / total}%` }} /></span>
      </div>
    </header>

    <nav className="lc-abas" role="tablist">{ABAS.map((a) => {
      const Ic = a.icone, dela = TODOS_OS_COMBOS.filter((c) => c.tipo === a.id), n = dela.filter((c) => aceso(c.id)).length;
      const novos = dela.filter((c) => aceso(c.id) && !vistos.includes(c.id)).length;
      return <button key={a.id} role="tab" aria-selected={aba === a.id} className={aba === a.id ? 'ativa' : ''} style={{ '--aba': a.cor } as CSSProperties} onClick={() => trocaAba(a.id)}>
        <Ic size={16} /><span>{a.nome}</span><small>{n}/{dela.length}</small>{novos > 0 && <em>{novos}</em>}
      </button>;
    })}</nav>

    <div className="lc-grade-caixa" ref={caixa} onPointerDown={desce} onPointerUp={sobe} onPointerCancel={() => { toque.current = null; }}>
      <div key={`${aba}-${atual}`} className={`lc-grade ${ida > 0 ? 'vem-direita' : 'vem-esquerda'}`} style={{ gridTemplateColumns: `repeat(${grade.colunas},minmax(0,1fr))`, gridTemplateRows: `repeat(${grade.linhas},minmax(0,1fr))` }}>
        {daPagina.map((c, i) => {
          const v = visualDoCombo(c.id), Icone = v.icone, on = aceso(c.id), novo = on && !vistos.includes(c.id);
          return <button key={c.id} type="button" className={`lc-peca ${on ? `acesa ${v.raridade}` : 'apagada'} ${novo ? 'nova' : ''} ${trancado === c.id ? 'treme' : ''}`}
            style={{ '--cb': c.tipo === 'lendarias' ? '#ffd36b' : v.cor, '--i': i } as CSSProperties} onClick={() => abre(c.id)}
            aria-label={on ? `${c.nome}: ver a ficha` : `${c.nome}: ainda não descoberto`}>
            <span className="lc-selo">{on ? <Icone size={20} /> : <Lock size={16} />}</span>
            <b>{c.nome}</b>
            {novo && <em>NOVO</em>}
          </button>;
        })}
      </div>
    </div>

    <footer className="lc-rodape">
      {trancado ? <p className="lc-dica" role="status"><Lock size={14} />Ainda escondido. Forme este combo no seu trio, ou veja um rival usar.</p>
        : <div className="lc-paginas">
          <button className="lc-seta" onClick={() => vai(-1)} disabled={atual === 0} aria-label="Página anterior"><ChevronLeft size={20} /></button>
          <span className="lc-pontos">{Array.from({ length: paginas }, (_, i) => <button key={i} className={i === atual ? 'ativo' : ''} aria-label={`Página ${i + 1}`} onClick={() => { setIda(i > atual ? 1 : -1); setPagina(i); }} />)}</span>
          <button className="lc-seta" onClick={() => vai(1)} disabled={atual >= paginas - 1} aria-label="Próxima página"><ChevronRight size={20} /></button>
        </div>}
    </footer>

    {aberto && <div className="lc-veu" role="dialog" aria-modal="true" aria-label="Ficha do combo" onClick={() => setAberto(null)}>
      <div className="lc-ficha" onClick={(e) => e.stopPropagation()}>
        <span className="lc-ficha-brilho" aria-hidden><Sparkles size={16} /></span>
        <CartaDoCombo id={aberto} />
        <button className="lc-fechar" onClick={() => setAberto(null)} aria-label="Fechar a ficha"><X size={18} /></button>
      </div>
    </div>}
  </section>;
}
