/*
 * FASE I · a tela de Conta.
 *
 * O documento pede criar conta, entrar, Google, sair, recuperar senha e ver a
 * sessão — e acrescenta duas regras que mandam no desenho desta tela:
 *
 *   "Privado: e-mail, auth id, tokens, provider metadata."
 *   "Preservar progresso local. Nunca apagar progresso silenciosamente."
 *
 * Por isso a tela mostra o e-mail só para o próprio dono e nunca o id da
 * conta; e por isso ela diz, antes de qualquer coisa, que o progresso é deste
 * aparelho e continua aqui com ou sem conta.
 */
import { useEffect, useState } from 'react';
import { KeyRound, LogIn, LogOut, Mail, ShieldCheck, UserPlus } from 'lucide-react';

import type { Autenticacao, Conta } from '../lib/auth';
import { validarHandle } from '../lib/auth';
import { deveOferecer, levarParaAConta, manterSeparado, resumoDoProgresso } from '../lib/migracao';
import type { Profile } from '../lib/storage';

type Modo = 'entrar' | 'criar' | 'recuperar';

export function AccountScreen({ autenticacao, conta, profile, conectado, google = false, aoMudarPerfil }:
{ autenticacao: Autenticacao; conta: Conta | null; profile: Profile; conectado: boolean;
  google?: boolean; aoMudarPerfil: (p: Profile) => void }) {
  const [modo, setModo] = useState<Modo>('entrar');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [handle, setHandle] = useState(profile.publicHandle ?? '');
  const [ocupado, setOcupado] = useState(false);
  const [aviso, setAviso] = useState<{ tipo: 'erro' | 'ok'; texto: string } | null>(null);
  /*
   * A oferta é decidida uma vez, quando a conta aparece. Se fosse recalculada
   * a cada render, responder faria o cartão sumir no mesmo instante — sem o
   * jogador ver a confirmação do que acabou de escolher.
   */
  const [oferta, setOferta] = useState(() => deveOferecer(conta, profile));
  useEffect(() => { if (deveOferecer(conta, profile)) setOferta(true); }, [conta, profile]);

  useEffect(() => { setAviso(null); }, [modo]);

  const logado = conta !== null && conta.origem !== 'convidado';

  const executar = async (acao: () => Promise<{ ok: boolean; erro?: string; precisaConfirmarEmail?: boolean }>, sucesso: string) => {
    setOcupado(true);
    const r = await acao();
    setOcupado(false);
    if (!r.ok) { setAviso({ tipo: 'erro', texto: r.erro ?? 'Não deu certo.' }); return; }
    setAviso({ tipo: 'ok', texto: r.precisaConfirmarEmail ? 'Conta criada. Confirme o e-mail que enviamos para entrar.' : sucesso });
    setSenha('');
  };

  const problemaNoHandle = modo === 'criar' && handle.length > 0 ? validarHandle(handle) : null;
  const resumo = resumoDoProgresso(profile);

  return <section className="account-screen">
    <div className="screen-title">
      <span className="eyebrow"><ShieldCheck size={14} /> CONTA NEXUS</span>
      <h1>{logado ? 'Sua conta' : 'Entrar é opcional.'}</h1>
      <p>
        {logado
          ? 'Com conta você pode jogar a Jornada Ranqueada e aparecer no ranking.'
          : 'Jogar funciona sem conta. A conta serve para a Jornada Ranqueada e para colocar seus pontos no ranking.'}
      </p>
    </div>

    {/*
      * O aviso sobre o progresso vem antes dos campos, de propósito.
      *
      * O documento manda nunca apagar progresso em silêncio. Quem chega nesta
      * tela precisa saber, antes de clicar em qualquer coisa, que o que ele
      * conquistou está neste aparelho e vai continuar aqui.
      */}
    <p className="account-progresso">
      Seu recorde de pontos e suas jornadas ficam <b>neste aparelho</b> e continuam aqui, com conta ou sem.
      Entrar não apaga nada.
    </p>

    {!conectado && <p className="account-aviso erro">
      A conta online ainda não foi conectada neste build. O jogo casual funciona normalmente.
    </p>}

    {/*
      * A oferta de levar o progresso do convidado para a conta.
      *
      * Aparece uma vez por conta, só para quem tem o que perder, e as duas
      * saídas preservam tudo: a diferença entre elas é de quem é o nome
      * público daqui para a frente, não o que sobrevive.
      */}
    {logado && oferta && <div className="account-migracao">
      <span className="eyebrow">PROGRESSO DESTE APARELHO</span>
      <p>
        Você já jogou aqui sem conta: <b>{resumo.jornadas} {resumo.jornadas === 1 ? 'jornada' : 'jornadas'}</b>
        {resumo.recorde > 0 && <> e um recorde de <b>{resumo.recorde.toLocaleString('pt-BR')} pontos</b></>}.
        {' '}Quer que esse progresso passe a contar como seu, nesta conta?
      </p>
      <div className="account-migracao-acoes">
        <button className="primary" onClick={() => {
          aoMudarPerfil(levarParaAConta(profile, conta));
          setOferta(false);
          setAviso({ tipo: 'ok', texto: 'Pronto. O progresso deste aparelho agora é desta conta.' });
        }}>Sim, é meu</button>
        <button className="secondary" onClick={() => {
          aoMudarPerfil(manterSeparado(profile, conta));
          setOferta(false);
          setAviso({ tipo: 'ok', texto: 'Tudo bem. Nada foi apagado — o progresso continua neste aparelho.' });
        }}>Deixar separado</button>
      </div>
      <small>Nos dois casos nada é apagado.</small>
    </div>}

    {logado ? <div className="account-cartao">
      <div className="account-identidade">
        <span className="eyebrow">{conta.origem === 'google' ? 'ENTROU COM GOOGLE' : 'ENTROU COM E-MAIL'}</span>
        <strong>{conta.handle ?? profile.publicHandle ?? 'Sem nome público'}</strong>
        {/* O e-mail aparece só aqui, para o próprio dono. O ranking nunca o mostra. */}
        <small>{conta.email ?? '—'}</small>
      </div>
      <p className="account-privacidade">
        No ranking aparecem só o seu nome público, o trio e a pontuação. O e-mail nunca.
      </p>
      <button className="secondary" disabled={ocupado}
        onClick={() => void executar(() => autenticacao.sair(), 'Você saiu da conta.')}>
        <LogOut size={16} /> Sair da conta
      </button>
    </div> : <div className="account-formulario">
      <nav className="account-abas" aria-label="Entrar ou criar conta">
        <button className={modo === 'entrar' ? 'active' : ''} onClick={() => setModo('entrar')}>Entrar</button>
        <button className={modo === 'criar' ? 'active' : ''} onClick={() => setModo('criar')}>Criar conta</button>
        <button className={modo === 'recuperar' ? 'active' : ''} onClick={() => setModo('recuperar')}>Esqueci a senha</button>
      </nav>

      <label><span>E-mail</span>
        <input type="email" autoComplete="email" value={email} disabled={!conectado || ocupado}
          onChange={(e) => setEmail(e.target.value)} placeholder="voce@exemplo.com" /></label>

      {modo !== 'recuperar' && <label><span>Senha</span>
        <input type="password" value={senha} disabled={!conectado || ocupado}
          autoComplete={modo === 'criar' ? 'new-password' : 'current-password'}
          onChange={(e) => setSenha(e.target.value)} placeholder="pelo menos 8 caracteres" /></label>}

      {modo === 'criar' && <label><span>Nome público</span>
        <input value={handle} disabled={!conectado || ocupado} maxLength={16}
          onChange={(e) => setHandle(e.target.value)} placeholder="como você aparece no ranking" />
        {problemaNoHandle && <small className="campo-erro">{problemaNoHandle}</small>}</label>}

      {modo === 'entrar' && <button className="primary" disabled={!conectado || ocupado}
        onClick={() => void executar(() => autenticacao.entrar(email, senha), 'Bem-vindo de volta.')}>
        <LogIn size={17} /> Entrar</button>}

      {modo === 'criar' && <button className="primary" disabled={!conectado || ocupado || problemaNoHandle !== null}
        onClick={() => void executar(() => autenticacao.criarConta(email, senha, handle), 'Conta criada.')}>
        <UserPlus size={17} /> Criar conta</button>}

      {modo === 'recuperar' && <button className="primary" disabled={!conectado || ocupado}
        onClick={() => void executar(() => autenticacao.enviarRecuperacao(email), 'Se existe conta com esse e-mail, o link de recuperação já foi enviado.')}>
        <Mail size={17} /> Enviar link de recuperação</button>}

      {/* O Google aparece só quando existe de verdade. Ver "onlineConfigured". */}
      {google && modo !== 'recuperar' && <>
        <div className="account-ou"><span>ou</span></div>
        <button className="secondary" disabled={!conectado || ocupado}
          onClick={() => void executar(() => autenticacao.entrarComGoogle(), 'Abrindo o Google…')}>
          <KeyRound size={16} /> Continuar com Google
        </button>
      </>}
    </div>}

    {aviso && <p className={`account-aviso ${aviso.tipo}`} role="status">{aviso.texto}</p>}
  </section>;
}
