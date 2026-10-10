/*
 * A porta de entrada (pedido do jogador: "quando você entra, a primeira coisa
 * que você tem que fazer é se logar… criar a sua conta, colocar a sua senha e
 * se logar… e criar o seu nome. Se você não fizer isso, você não consegue
 * jogar… qualquer jogo que você fizer vai estar no rank").
 *
 * Antes, a conta era opcional: quem jogava sem ela, ou com a conta mas sem o
 * nome público no servidor, tinha as jornadas fora do ranking sem perceber.
 * Agora o jogo só abre depois das duas etapas:
 *   1. entrar ou criar a conta (a tela de Conta, no modo obrigatório);
 *   2. o nome público gravado no servidor — o nome escolhido no cadastro vai
 *      sozinho; se faltar (ou já tiver dono), o jogador escolhe aqui.
 */
import { useState } from 'react';
import { BadgeCheck, LogOut, RotateCcw, WifiOff } from 'lucide-react';
import type { Autenticacao, Conta } from '../lib/auth';
import { validarHandle } from '../lib/auth';
import type { Profile } from '../lib/storage';
import { AccountScreen } from './AccountScreen';

export type EtapaDoPortao = 'carregando' | 'entrar' | 'nome' | 'erro';

export function PortaoDaConta({ etapa, autenticacao, conta, profile, conectado, google, aoMudarPerfil, erro, onTentar, onNome }: {
  etapa: EtapaDoPortao; autenticacao: Autenticacao; conta: Conta | null; profile: Profile; conectado: boolean; google: boolean;
  aoMudarPerfil: (p: Profile) => void; erro?: string; onTentar: () => void; onNome: (handle: string) => Promise<string | null>;
}) {
  const [handle, setHandle] = useState(conta?.handle ?? '');
  const [ocupado, setOcupado] = useState(false);
  const [aviso, setAviso] = useState<string | null>(null);
  const problema = handle.length > 0 ? validarHandle(handle) : null;
  const confirmar = async () => {
    setOcupado(true); setAviso(null);
    const falha = await onNome(handle.trim());
    setOcupado(false);
    if (falha) setAviso(falha);
  };
  return <main className="portao">
    <header className="portao-marca"><b>NEXUS</b><span>TRIOS</span></header>
    {etapa === 'carregando' && <section className="portao-cartao" aria-busy="true"><span className="portao-giro" aria-hidden /><p>Conectando à sua conta…</p></section>}
    {etapa === 'erro' && <section className="portao-cartao" role="alert">
      <WifiOff size={28} /><h2>Sem conexão com o servidor</h2>
      <p>{erro || 'Não deu para confirmar a sua conta.'} O jogo precisa da conta para cada jornada valer no ranking.</p>
      <button className="primary" onClick={onTentar}><RotateCcw size={16} /> Tentar de novo</button>
      <button className="secondary" onClick={() => void autenticacao.sair()}><LogOut size={16} /> Sair da conta</button>
    </section>}
    {etapa === 'entrar' && <AccountScreen autenticacao={autenticacao} conta={conta} profile={profile} conectado={conectado} google={google} aoMudarPerfil={aoMudarPerfil} obrigatorio />}
    {etapa === 'nome' && <section className="portao-cartao">
      <BadgeCheck size={30} /><h2>Seu nome no ranking</h2>
      <p>Falta só o nome público: é ele que aparece no ranking, junto do seu trio e dos seus pontos. O e-mail nunca aparece.</p>
      <label className="portao-campo"><span>Nome público</span>
        <input value={handle} maxLength={16} disabled={ocupado} autoFocus onChange={(e) => setHandle(e.target.value)} placeholder="De 3 a 16 letras" />
        {problema && <small className="campo-erro">{problema}</small>}</label>
      <button className="primary" disabled={ocupado || !handle || problema !== null} onClick={() => void confirmar()}>Confirmar e jogar</button>
      {aviso && <p className="account-aviso erro" role="alert">{aviso}</p>}
      <button className="text-button" onClick={() => void autenticacao.sair()}><LogOut size={14} /> Entrar com outra conta</button>
    </section>}
  </main>;
}
