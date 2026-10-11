import { useEffect, useState, type CSSProperties } from 'react';
import { Anchor, Ban, BatteryCharging, Biohazard, Bomb, Castle, ChevronRight, CloudLightning, Crosshair, Droplet, Droplets, Dumbbell, EyeOff, Flame, Gem, Ghost, Globe, HeartPulse, Hourglass, Infinity as Infinito, Link2, Lock, Crown, Timer, TrendingDown, Skull, MoonStar, Shield, Heart, Wind, Copy, Battery, Mountain, Leaf, Moon, Rocket, ShieldAlert, ShieldHalf, ShieldPlus, Snowflake, Sparkles, Sprout, Sunrise, Swords, Target, Tornado, Users, VolumeX, Zap, type LucideIcon } from 'lucide-react';
import { byId } from '../data/characters';
import { DUPLAS_LENDARIAS, PECAS, PISO, REGRAS, TRIOS, UNIVERSO, bonusEfetivo, raridadeDe, type Raridade } from '../engine/combos';
import type { Bonus, ComboAtivo, Pulso } from '../engine/types';
import { Portrait } from './Portrait';

/*
 * Os combos do trio na tela (src/engine/combos.ts), gamificados (pedido do
 * jogador: "tudo tem que ser muito bem gamificado, nada de só lista"): cada
 * combo é uma medalha com ícone e cor; no Livro de Combos, cada um é uma carta
 * para colecionar (acende quando o jogador ativa pela primeira vez); na luta,
 * a abertura mostra os combos do trio entrando.
 *
 * A escolha do trio não mostra combo nenhum (pedido do jogador: "a pessoa tem
 * que aprender… ler os negócios e aprender; não quero que você fale qual é
 * bom"): o jogador lê as regras no Livro, lê as fichas e monta o trio; o que
 * ele acertou aparece na abertura da luta.
 */
export const VISUAL_DO_COMBO: Record<string, { icone: LucideIcon; cor: string }> = {
  'gelo-fogo': { icone: Snowflake, cor: '#7fd8ff' },
  'gelo-quebra': { icone: Gem, cor: '#a8e8ff' },
  'veneno-sangue': { icone: Droplet, cor: '#9be05a' },
  'sangue-vampiro': { icone: Droplets, cor: '#ff3a5a' },
  'maldicao-vampiro': { icone: Ghost, cor: '#b46aff' },
  'sono-golpe': { icone: Moon, cor: '#9aa8ff' },
  'controla-dano': { icone: Anchor, cor: '#a58aff' },
  'dissipa-golpe': { icone: Ban, cor: '#ff9a6a' },
  'reforca-forte': { icone: Dumbbell, cor: '#ff9a3a' },
  'carga-golpe': { icone: BatteryCharging, cor: '#ffd84a' },
  'bomba-area': { icone: Bomb, cor: '#ff7a3a' },
  'expostos-ferido': { icone: Crosshair, cor: '#ff5a6a' },
  'silencio-preparo': { icone: VolumeX, cor: '#8fb8ff' },
  'pressa-acumula': { icone: Hourglass, cor: '#ffc85a' },
  'status-gatilho': { icone: Zap, cor: '#c8f560' },
  'cego-esquiva': { icone: EyeOff, cor: '#c0c8d8' },
  'escudo-espinhos': { icone: ShieldPlus, cor: '#a6d36a' },
  'provoca-espinhos': { icone: ShieldAlert, cor: '#e0a060' },
  'provoca-golpe': { icone: ShieldHalf, cor: '#8fd3ff' },
  'cura-tanque': { icone: HeartPulse, cor: '#5ae08a' },
  'regen-tanque': { icone: Sprout, cor: '#7ae07a' },
  'limpa-fragil': { icone: Sparkles, cor: '#b8f0ff' },
  'revive-virada': { icone: Sunrise, cor: '#ffcf6a' },
  'duas-invocacoes': { icone: Users, cor: '#c9a2ff' },
  'veneno-maldicao': { icone: Skull, cor: '#8fd14f' },
  'gelo-sono': { icone: MoonStar, cor: '#9fd8ff' },
  'barreira-purifica': { icone: Shield, cor: '#b8f0ff' },
  'regen-cura': { icone: Heart, cor: '#6ae0a0' },
  'invoca-carga': { icone: Wind, cor: '#c9a2ff' },
  'bomba-fogo': { icone: Flame, cor: '#ff8a3a' },
  'eletrico-golpe': { icone: Zap, cor: '#ffe35a' },
  'cego-golpe': { icone: EyeOff, cor: '#ff9a7a' },
  'dissipa-maldicao': { icone: Ban, cor: '#d08aff' },
  'copia-golpe': { icone: Copy, cor: '#7fe0ff' },
  'acumula-barreira': { icone: Battery, cor: '#ffd84a' },
  'paralisa-golpe': { icone: Mountain, cor: '#ffcf6a' },
  'provoca-regen': { icone: Leaf, cor: '#7ae07a' },
  'universo-2': { icone: Globe, cor: '#ffd36b' },
  'universo-3': { icone: Globe, cor: '#ffb02a' },
  'trio-armadilha': { icone: Target, cor: '#ff6b8a' },
  'trio-execucao': { icone: Swords, cor: '#ff5a3c' },
  'trio-elementos': { icone: CloudLightning, cor: '#b98cff' },
  'trio-pragas': { icone: Biohazard, cor: '#9be05a' },
  'trio-caos': { icone: Tornado, cor: '#c8a0ff' },
  'trio-turbo': { icone: Rocket, cor: '#5ad7ff' },
  'trio-ataque-total': { icone: Flame, cor: '#ffa23a' },
  'trio-muralha': { icone: Castle, cor: '#7fe0b0' },
  'trio-imortais': { icone: Infinito, cor: '#ffe27a' },
};
const ehTrio = (id: string) => id.startsWith('trio-');
const visual = (id: string) => VISUAL_DO_COMBO[id] ?? (id.startsWith('lenda-') ? { icone: Crown, cor: '#ffd36b' } : { icone: Link2, cor: '#c8f560' });
const pct = (v: number) => `${Math.round(v * 100)}%`;
export function textoDoBonus(b: Partial<Bonus>): string {
  const partes: string[] = [];
  if (b.dano) partes.push(`+${pct(b.dano)} de dano`);
  if (b.defesa) partes.push(`recebe ${pct(b.defesa)} menos dano`);
  if (b.carga) partes.push(`Carga ${pct(b.carga)} mais rápida`);
  if (b.ritmo) partes.push(`ataque ${pct(b.ritmo)} mais rápido`);
  if (b.cura) partes.push(`+${pct(b.cura)} de cura`);
  if (b.vida) partes.push(`+${pct(b.vida)} de Vida`);
  if (b.escudo) partes.push(`começa com Escudo de ${pct(b.escudo)} da Vida`);
  if (b.preparo) partes.push(`Preparo ${pct(b.preparo)} mais curto`);
  if (b.traco) partes.push(`o Traço volta ${pct(b.traco)} mais rápido`);
  if (b.basico) partes.push(`ataque básico +${pct(b.basico)} de dano`);
  if (b.duracao) partes.push(`os Status que ele põe duram ${pct(b.duracao)} mais`);
  if (b.resiste) partes.push(`Status ruins nele duram ${pct(b.resiste)} menos`);
  if (b.segura) partes.push('uma vez por luta, o golpe que o derrubaria deixa com 1 de Vida');
  return partes.join(', ');
}
/** O que o combo tira do trio rival (os valores vêm em positivo). */
export function textoDosRivais(b: Partial<Bonus> | undefined): string {
  if (!b) return '';
  const partes: string[] = [];
  if (b.dano) partes.push(`−${pct(b.dano)} de dano`);
  if (b.defesa) partes.push(`recebem ${pct(b.defesa)} mais dano`);
  if (b.cura) partes.push(`−${pct(b.cura)} de cura`);
  if (b.carga) partes.push(`Carga ${pct(b.carga)} mais lenta`);
  if (b.ritmo) partes.push(`ataque ${pct(b.ritmo)} mais lento`);
  if (b.preparo) partes.push(`Preparo ${pct(b.preparo)} mais longo`);
  if (b.traco) partes.push(`o Traço demora ${pct(b.traco)} mais`);
  if (b.basico) partes.push(`ataque básico −${pct(b.basico)} de dano`);
  if (b.duracao) partes.push(`os Status que eles põem duram ${pct(b.duracao)} menos`);
  return partes.length ? `rivais: ${partes.join(', ')}` : '';
}
/** O texto inteiro do que o combo dá (para quem ganha e contra os rivais), já com a força dos combos. */
export function textoDoCombo(id: string, b: Partial<Bonus>, nosRivais?: Partial<Bonus>): string {
  return [textoDoBonus(bonusEfetivo(b, id)), nosRivais ? textoDosRivais(bonusEfetivo(nosRivais, id, PISO)) : ''].filter(Boolean).join(' · ');
}
const chave = (c: ComboAtivo) => `${c.id}:${c.para.join(',')}`;

function Rostos({ ids }: { ids: string[] }) {
  return <span className="cb-rostos">{ids.map((id) => byId[id] && <Portrait key={id} character={byId[id]} />)}</span>;
}
/** A medalha de um combo: ícone, nome, bônus e quem ajuda → quem ganha (os retratos). */
export function MedalhaDeCombo({ combo, novo = false, i = 0 }: { combo: ComboAtivo; novo?: boolean; i?: number }) {
  const v = visual(combo.id), Icone = v.icone, universo = combo.id.startsWith('universo'), trio = ehTrio(combo.id);
  return <li className={`cb-medalha ${novo ? 'novo' : ''} ${trio ? 'trio' : ''}`} style={{ '--cb': v.cor, '--i': i } as CSSProperties}>
    <span className="cb-icone"><span className="cb-anel" aria-hidden /><Icone size={20} /></span>
    <span className="cb-texto"><b>{trio && <em>TRIO</em>}{combo.nome}</b><small>{trio && textoDoBonus(combo.bonus) ? 'o trio todo: ' : ''}{[textoDoCombo(combo.id, combo.bonus, combo.nosRivais), combo.pulso && `a cada ${combo.pulso.cada} s, ${combo.pulso.texto}`].filter(Boolean).join(' · ')}</small>
      <span className="cb-quem">{universo || trio ? <Rostos ids={combo.de} /> : <><Rostos ids={combo.de} /><i aria-hidden>➜</i><Rostos ids={combo.para} /></>}</span></span>
    {novo && <span className="cb-novo">NOVO!</span>}
  </li>;
}
/** A lista da luta (os dois lados), em medalhas; com `onEscolher`, cada medalha abre a ficha do combo. */
export function ListaDeCombos({ combos, vazio, onEscolher }: { combos: ComboAtivo[]; vazio?: string; onEscolher?: (c: ComboAtivo) => void }) {
  if (!combos.length) return vazio ? <p className="cb-vazio">{vazio}</p> : null;
  return <ul className={`cb-lista ${onEscolher ? 'clicavel' : ''}`}>{combos.map((c, i) => onEscolher
    ? <button key={chave(c)} type="button" className="cb-medalha-botao" onClick={() => onEscolher(c)} aria-label={`Ver a ficha de ${c.nome}`}><MedalhaDeCombo combo={c} i={i} /><ChevronRight className="cb-abrir" size={16} /></button>
    : <MedalhaDeCombo key={chave(c)} combo={c} i={i} />)}</ul>;
}
/**
 * A ficha completa de um combo ativo na luta, igual à carta do Livro de Combos: raridade, o que forma o
 * combo, quem ajuda e quem recebe (com os retratos) e o que ele faz — a luta toda, de tempo em tempo e nos rivais.
 */
export function FichaDoCombo({ combo }: { combo: ComboAtivo }) {
  const v = visual(combo.id), Icone = v.icone, rar = raridadeDe(combo.id);
  const regra = REGRAS.find((r) => r.id === combo.id), trio = TRIOS.find((t) => t.id === combo.id), lenda = DUPLAS_LENDARIAS.find((l) => l.id === combo.id);
  const quem = trio ? 'O trio todo' : combo.id.startsWith('universo') ? (combo.para.length === 3 ? 'Os três' : 'Os dois') : lenda ? (lenda.so ? byId[lenda.so]?.name ?? '' : 'Os dois') : 'Quem recebe';
  return <article className={`cb-carta cb-ficha acesa ${rar} ${trio ? 'trio' : ''} ${lenda ? 'lenda' : ''}`} style={{ '--cb': lenda ? '#ffd36b' : v.cor } as CSSProperties}>
    <span className="cb-icone"><span className="cb-anel" aria-hidden /><Icone size={24} /></span>
    <h3>{combo.nome}</h3>
    <SeloDeRaridade r={rar} />
    <span className="cb-quem">{combo.id.startsWith('universo') || trio ? <Rostos ids={combo.de} /> : <><Rostos ids={combo.de} /><i aria-hidden>➜</i><Rostos ids={combo.para} /></>}</span>
    {regra && <dl><dt>Quem ajuda</dt><dd>Alguém que {PECAS[regra.ajuda]}</dd><dt>Quem recebe</dt><dd>Alguém que {PECAS[regra.ganha]}</dd></dl>}
    {trio && <ol className="cb-pecas-trio">{trio.pecas.map((k) => <li key={k}>Alguém que {PECAS[k]}</li>)}</ol>}
    {lenda && <small className="cb-par-nomes">{byId[lenda.a]?.name} + {byId[lenda.b]?.name}</small>}
    <Efeitos quem={quem} bonus={combo.bonus} pulso={combo.pulso} nosRivais={combo.nosRivais} id={combo.id} />
  </article>;
}
/** A abertura da luta: "N COMBOS ATIVOS" e as medalhas entrando; some sozinha. */
export function AberturaDeCombos({ combos, chaveDaLuta, comecando }: { combos: ComboAtivo[]; chaveDaLuta: string; /** só no começo da luta (voltar para uma luta no meio não repete) */ comecando: boolean }) {
  const [ver, setVer] = useState(comecando);
  useEffect(() => { if (!comecando) return; setVer(true); const t = window.setTimeout(() => setVer(false), 2600); return () => clearTimeout(t); }, [chaveDaLuta]);
  if (!ver || !combos.length) return null;
  // o mesmo combo em dois do trio vira uma medalha só, com "×2"
  const grupos = [...combos.reduce((m, c) => m.set(c.id, [m.get(c.id)?.[0] ?? c, (m.get(c.id)?.[1] ?? 0) + 1]), new Map<string, [ComboAtivo, number]>()).values()];
  return <div className="cb-abertura" role="status" onClick={() => setVer(false)}>
    <strong><Link2 size={18} />{combos.length} {combos.length === 1 ? 'COMBO ATIVO' : 'COMBOS ATIVOS'}</strong>
    <span className="cb-abertura-medalhas">{grupos.map(([c, n], i) => { const v = visual(c.id), Icone = v.icone; return <span key={c.id} className={ehTrio(c.id) ? 'trio' : ''} style={{ '--cb': v.cor, '--i': i } as CSSProperties}><Icone size={ehTrio(c.id) ? 24 : 18} /><small>{c.nome}{n > 1 && <b> ×{n}</b>}</small></span>; })}</span>
  </div>;
}
/*
 * O Livro de Combos como álbum (pedido do jogador: "extremamente bem feito… bem gamificado, separadinho, tudo
 * muito bonito pra pessoa aprender fácil"): abas por tipo (duplas, trios, universo, lendárias), as duplas
 * separadas por raridade, cada carta com o que precisa, o que dá, o que faz de tempo em tempo e o que tira
 * dos rivais. Acende quando o jogador forma o combo pela primeira vez.
 */
const NOME_DA_RARIDADE: Record<Raridade, string> = { comum: 'Comum', raro: 'Raro', epico: 'Épico', lendario: 'Lendário' };
const ORDEM_DA_RARIDADE: Raridade[] = ['lendario', 'epico', 'raro', 'comum'];
function SeloDeRaridade({ r }: { r: Raridade }) {
  return <span className={`cb-raridade ${r}`}><Gem size={10} />{NOME_DA_RARIDADE[r]}</span>;
}
const maiuscula = (t: string) => t.charAt(0).toUpperCase() + t.slice(1);
/*
 * O que o combo dá, em blocos com título (pedido do jogador: "se ganham o tempo inteiro, deixa mostrando que
 * ganham; se tem uma condição, deixa dentro da condição… bater o olho e entender na hora"):
 *   A LUTA TODA — o bônus que vale desde o começo;  A CADA X s — o que acontece de tempo em tempo;
 *   NOS RIVAIS, A LUTA TODA — o que ele tira do outro trio.
 */
function Efeitos({ quem, bonus, pulso, nosRivais, id }: { quem: string; bonus: Partial<Bonus>; pulso?: Pulso; nosRivais?: Partial<Bonus>; id: string }) {
  const sempre = textoDoBonus(bonusEfetivo(bonus, id)), rivais = nosRivais ? textoDosRivais(bonusEfetivo(nosRivais, id, PISO)).replace(/^rivais: /, '') : '';
  return <ul className="cb-efeitos">
    {sempre && <li className="sempre"><b><Infinito size={12} />A LUTA TODA</b><span><em>{quem}:</em> {sempre}</span></li>}
    {pulso && <li className="pulso"><b><Timer size={12} />A CADA {String(pulso.cada).replace('.', ',')} s</b><span>{maiuscula(pulso.texto)}</span></li>}
    {rivais && <li className="rivais"><b><TrendingDown size={12} />NOS RIVAIS, A LUTA TODA</b><span>{maiuscula(rivais)}</span></li>}
  </ul>;
}
type Aba = 'duplas' | 'trios' | 'universo' | 'lendarias';
export function AlbumDeCombos({ descobertos }: { descobertos: readonly string[] }) {
  const [aba, setAba] = useState<Aba>('duplas');
  const aceso = (id: string) => descobertos.includes(id);
  const universos = [{ id: 'universo-2', nome: 'Dupla do mesmo universo', quem: 'Dois personagens do mesmo universo (o que aparece no topo da ficha)', b: UNIVERSO.dois }, { id: 'universo-3', nome: 'Trio do mesmo universo', quem: 'Os três do mesmo universo (o que aparece no topo da ficha)', b: UNIVERSO.tres }];
  const grupos: Record<Aba, string[]> = { duplas: REGRAS.map((r) => r.id), trios: TRIOS.map((t) => t.id), universo: universos.map((u) => u.id), lendarias: DUPLAS_LENDARIAS.map((l) => l.id) };
  const todos = Object.values(grupos).flat(), achados = todos.filter(aceso).length;
  const ABAS: { id: Aba; nome: string; icone: LucideIcon; dica: string }[] = [
    { id: 'duplas', nome: 'Duplas', icone: Link2, dica: 'Um ajuda, o outro recebe. Leia as fichas: cada peça é algo que o personagem faz.' },
    { id: 'trios', nome: 'Trios', icone: Castle, dica: 'Os três se completam, cada um numa peça. O bônus vai para o trio todo.' },
    { id: 'universo', nome: 'Universo', icone: Globe, dica: 'Personagens do mesmo universo lutam melhor juntos. O trio inteiro vale muito mais que a dupla. Marvel e DC são divididas em equipes (X-Men, Vingadores, Liga da Justiça…): vale a equipe, que aparece no topo da ficha.' },
    { id: 'lendarias', nome: 'Lendárias', icone: Crown, dica: 'Duplas de nome, da própria história. Juntar os dois no mesmo trio é raro, e vale a pena.' },
  ];
  const atual = ABAS.find((a) => a.id === aba)!;
  return <div className="cb-album">
    <div className="cb-album-topo"><b>{achados}<small>/{todos.length}</small></b><span><strong>COMBOS DESCOBERTOS</strong><small>Leia as fichas e monte o trio: o combo que você formar aparece no começo da luta e acende aqui.</small></span>
      <span className="cb-album-barra"><i style={{ width: `${(100 * achados) / todos.length}%` }} /></span></div>
    <div className="cb-legenda" aria-label="Raridade">{ORDEM_DA_RARIDADE.map((r) => <SeloDeRaridade key={r} r={r} />)}<small>quanto mais raro, mais difícil de montar — e mais forte</small></div>
    <nav className="cb-abas" role="tablist">{ABAS.map((a) => { const Ic = a.icone, n = grupos[a.id].filter(aceso).length; return <button key={a.id} role="tab" aria-selected={aba === a.id} className={aba === a.id ? 'ativa' : ''} onClick={() => setAba(a.id)}><Ic size={15} /><span>{a.nome}</span><small>{n}/{grupos[a.id].length}</small></button>; })}</nav>
    <p className="cb-aba-dica">{atual.dica}</p>
    {aba === 'duplas' && ORDEM_DA_RARIDADE.filter((r) => REGRAS.some((x) => raridadeDe(x.id) === r)).map((rar) => <section key={rar} className={`cb-faixa ${rar}`}>
      <h3 className="cb-album-secao"><SeloDeRaridade r={rar} /><small>{REGRAS.filter((x) => raridadeDe(x.id) === rar).filter((x) => aceso(x.id)).length}/{REGRAS.filter((x) => raridadeDe(x.id) === rar).length}</small></h3>
      <div className="cb-album-grade">{REGRAS.filter((x) => raridadeDe(x.id) === rar).map((r, i) => {
        const v = visual(r.id), Icone = v.icone;
        return <article key={r.id} className={`cb-carta ${rar} ${aceso(r.id) ? 'acesa' : ''}`} style={{ '--cb': v.cor, '--i': i } as CSSProperties}>
          <span className="cb-icone"><span className="cb-anel" aria-hidden /><Icone size={22} /></span>
          <h3>{r.nome}</h3>
          <dl><dt>Quem ajuda</dt><dd>Alguém que {PECAS[r.ajuda]}</dd><dt>Quem recebe</dt><dd>Alguém que {PECAS[r.ganha]}</dd></dl>
          <Efeitos quem="Quem recebe" bonus={r.bonus} pulso={r.pulso} nosRivais={r.nosRivais} id={r.id} />
          {!aceso(r.id) && <span className="cb-cadeado"><Lock size={12} />a descobrir</span>}
        </article>;
      })}</div>
    </section>)}
    {aba === 'trios' && <div className="cb-album-grade trios">{TRIOS.map((t, i) => {
      const v = visual(t.id), Icone = v.icone;
      return <article key={t.id} className={`cb-carta trio lendario ${aceso(t.id) ? 'acesa' : ''}`} style={{ '--cb': v.cor, '--i': i } as CSSProperties}>
        <span className="cb-icone"><span className="cb-anel" aria-hidden /><Icone size={24} /></span>
        <h3>{t.nome}</h3>
        <ol className="cb-pecas-trio">{t.pecas.map((k) => <li key={k}>Alguém que {PECAS[k]}</li>)}</ol>
        <Efeitos quem="O trio todo" bonus={t.bonus} pulso={t.pulso} nosRivais={t.nosRivais} id={t.id} />
        {!aceso(t.id) && <span className="cb-cadeado"><Lock size={12} />a descobrir</span>}
      </article>;
    })}</div>}
    {aba === 'universo' && <div className="cb-album-grade trios">{universos.map((u, i) => {
      const v = visual(u.id), Icone = v.icone;
      return <article key={u.id} className={`cb-carta ${raridadeDe(u.id)} ${aceso(u.id) ? 'acesa' : ''}`} style={{ '--cb': v.cor, '--i': i } as CSSProperties}>
        <span className="cb-icone"><span className="cb-anel" aria-hidden /><Icone size={22} /></span>
        <h3>{u.nome}</h3><SeloDeRaridade r={raridadeDe(u.id)} />
        <dl><dt>Quem forma</dt><dd>{u.quem}</dd></dl>
        <Efeitos quem={u.id === 'universo-3' ? 'Os três' : 'Os dois'} bonus={u.b} id={u.id} />
        {!aceso(u.id) && <span className="cb-cadeado"><Lock size={12} />a descobrir</span>}
      </article>;
    })}</div>}
    {aba === 'lendarias' && <div className="cb-album-grade trios">{DUPLAS_LENDARIAS.map((l, i) => {
      const a = byId[l.a], b = byId[l.b];
      if (!a || !b) return null;
      return <article key={l.id} className={`cb-carta lenda lendario ${aceso(l.id) ? 'acesa' : ''}`} style={{ '--cb': '#ffd36b', '--i': i } as CSSProperties}>
        <span className="cb-par"><Portrait character={a} /><Crown size={16} /><Portrait character={b} /></span>
        <h3>{l.nome}</h3>
        <small className="cb-par-nomes">{a.name} + {b.name}</small>
        <Efeitos quem={l.so ? byId[l.so]?.name ?? '' : 'Os dois'} bonus={l.bonus} pulso={l.pulso} id={l.id} />
        {!aceso(l.id) && <span className="cb-cadeado"><Lock size={12} />a descobrir</span>}
      </article>;
    })}</div>}
  </div>;
}
