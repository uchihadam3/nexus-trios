/*
 * FASE I · a tela de Conta (remake visual: medalhão, vantagens em peças,
 * abas e campos de jogo; a lógica é a mesma).
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
import { useEffect, useState, type CSSProperties } from 'react';
import { BadgeCheck, KeyRound, LogIn, LogOut, Mail, ShieldCheck, Smartphone, Swords, Trophy, UserPlus } from 'lucide-react';
import { TelaTopo } from '../components/Casca';

import type { Autenticacao, Conta } from '../lib/auth';
import { validarHandle } from '../lib/auth';
import { deveOferecer, levarParaAConta, manterSeparado, resumoDoProgresso } from '../lib/migracao';
import type { Profile } from '../lib/storage';
import { numero, t, tx } from '../i18n/idioma';

type Modo = 'entrar' | 'criar' | 'recuperar';

export function AccountScreen({ autenticacao, conta, profile, conectado, google = false, aoMudarPerfil, obrigatorio = false }:
{ autenticacao: Autenticacao; conta: Conta | null; profile: Profile; conectado: boolean;
  google?: boolean; aoMudarPerfil: (p: Profile) => void;
  /** A porta de entrada (PortaoDaConta): sem conta não se joga, e quem chega primeiro cria a conta. */
  obrigatorio?: boolean }) {
  const [modo, setModo] = useState<Modo>(obrigatorio ? 'criar' : 'entrar');
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
    if (!r.ok) { setAviso({ tipo: 'erro', texto: r.erro ?? tx('Não deu certo.') }); return; }
    setAviso({ tipo: 'ok', texto: r.precisaConfirmarEmail ? tx('Conta criada. Confirme o e-mail que enviamos para entrar.') : sucesso });
    setSenha('');
  };

  const problemaNoHandle = modo === 'criar' && handle.length > 0 ? validarHandle(handle) : null;
  const resumo = resumoDoProgresso(profile);

  return <section className="account-screen conta-v2">
    <TelaTopo icone={<ShieldCheck />} cor="#86e3a8" rotulo={t('CONTA NEXUS')} titulo={logado ? t('Sua conta') : obrigatorio ? t('Entre para jogar') : t('Entre na disputa')}>
      <p>{logado ? t('Pronto: toda Jornada vale ranking.') : t('Crie sua conta ou entre: toda Jornada vai para o ranking.')}</p>
    </TelaTopo>
    {!logado && <div className="ct-vantagens">
      <span style={{ '--tile': '#ffd36b' } as CSSProperties}><Trophy size={20} /><b>{t('Ranking')}</b><small>{t('seu trio no placar')}</small></span>
      <span style={{ '--tile': '#8fd3ff' } as CSSProperties}><Swords size={20} /><b>{t('Ranking')}</b><small>{t('hoje, semana e geral')}</small></span>
      <span style={{ '--tile': '#c3a2ff' } as CSSProperties}><BadgeCheck size={20} /><b>{t('Nome público')}</b><small>{t('sem mostrar o e-mail')}</small></span>
    </div>}

    {/*
      * O aviso sobre o progresso vem antes dos campos, de propósito.
      *
      * O documento manda nunca apagar progresso em silêncio. Quem chega nesta
      * tela precisa saber, antes de clicar em qualquer coisa, que o que ele
      * conquistou está neste aparelho e vai continuar aqui.
      */}
    <p className="account-progresso">
      <Smartphone size={18} /><span>{obrigatorio ? t('O que você já jogou neste aparelho continua aqui: entrar não apaga nada.') : t('Seu recorde e suas jornadas ficam neste aparelho, com conta ou sem. Entrar não apaga nada.')}</span>
    </p>

    {!conectado && <p className="account-aviso erro">
      {t('A conta online ainda não foi conectada neste build.')}
    </p>}

    {/*
      * A oferta de levar o progresso do convidado para a conta.
      *
      * Aparece uma vez por conta, só para quem tem o que perder, e as duas
      * saídas preservam tudo: a diferença entre elas é de quem é o nome
      * público daqui para a frente, não o que sobrevive.
      */}
    {logado && oferta && <div className="account-migracao">
      <span className="eyebrow">{t('PROGRESSO DESTE APARELHO')}</span>
      <p>
        {t(resumo.jornadas === 1 ? 'Você já jogou aqui sem conta: {n} jornada' : 'Você já jogou aqui sem conta: {n} jornadas', { n: resumo.jornadas })}
        {resumo.recorde > 0 && t(' e um recorde de {pontos} pontos', { pontos: numero(resumo.recorde) })}.
        {' '}{t('Quer que esse progresso passe a contar como seu, nesta conta?')}
      </p>
      <div className="account-migracao-acoes">
        <button className="primary" onClick={() => {
          aoMudarPerfil(levarParaAConta(profile, conta));
          setOferta(false);
          setAviso({ tipo: 'ok', texto: tx('Pronto. O progresso deste aparelho agora é desta conta.') });
        }}>{t('Sim, é meu')}</button>
        <button className="secondary" onClick={() => {
          aoMudarPerfil(manterSeparado(profile, conta));
          setOferta(false);
          setAviso({ tipo: 'ok', texto: tx('Tudo bem. Nada foi apagado — o progresso continua neste aparelho.') });
        }}>{t('Deixar separado')}</button>
      </div>
      <small>{t('Nos dois casos nada é apagado.')}</small>
    </div>}

    {logado ? <div className="account-cartao">
      <div className="account-identidade">
        <span className="eyebrow">{conta.origem === 'google' ? t('ENTROU COM GOOGLE') : t('ENTROU COM E-MAIL')}</span>
        <strong>{conta.handle ?? profile.publicHandle ?? t('Sem nome público')}</strong>
        {/* O e-mail aparece só aqui, para o próprio dono. O ranking nunca o mostra. */}
        <small>{conta.email ?? '—'}</small>
      </div>
      <p className="account-privacidade">
        {t('No ranking aparecem só o seu nome público, o trio e a pontuação. O e-mail nunca.')}
      </p>
      <button className="secondary" disabled={ocupado}
        onClick={() => void executar(() => autenticacao.sair(), tx('Você saiu da conta.'))}>
        <LogOut size={16} /> {t('Sair da conta')}
      </button>
    </div> : <div className="account-formulario">
      <nav className="account-abas" aria-label={t('Entrar ou criar conta')}>
        <button className={modo === 'entrar' ? 'active' : ''} onClick={() => setModo('entrar')}>{t('Entrar')}</button>
        <button className={modo === 'criar' ? 'active' : ''} onClick={() => setModo('criar')}>{t('Criar conta')}</button>
        <button className={modo === 'recuperar' ? 'active' : ''} onClick={() => setModo('recuperar')}>{t('Esqueci a senha')}</button>
      </nav>

      <label><span>{t('E-mail')}</span>
        <input type="email" autoComplete="email" value={email} disabled={!conectado || ocupado}
          onChange={(e) => setEmail(e.target.value)} placeholder={t('voce@exemplo.com')} /></label>

      {modo !== 'recuperar' && <label><span>{t('Senha')}</span>
        <input type="password" value={senha} disabled={!conectado || ocupado}
          autoComplete={modo === 'criar' ? 'new-password' : 'current-password'}
          onChange={(e) => setSenha(e.target.value)} placeholder={t('pelo menos 8 caracteres')} /></label>}

      {modo === 'criar' && <label><span>{t('Nome público')}</span>
        <input value={handle} disabled={!conectado || ocupado} maxLength={16}
          onChange={(e) => setHandle(e.target.value)} placeholder={t('como você aparece no ranking')} />
        {problemaNoHandle && <small className="campo-erro">{t(problemaNoHandle)}</small>}</label>}

      {modo === 'entrar' && <button className="primary" disabled={!conectado || ocupado}
        onClick={() => void executar(() => autenticacao.entrar(email, senha), tx('Bem-vindo de volta.'))}>
        <LogIn size={17} /> {t('Entrar')}</button>}

      {modo === 'criar' && <button className="primary" disabled={!conectado || ocupado || problemaNoHandle !== null}
        onClick={() => void executar(() => autenticacao.criarConta(email, senha, handle), tx('Conta criada.'))}>
        <UserPlus size={17} /> {t('Criar conta')}</button>}

      {modo === 'recuperar' && <button className="primary" disabled={!conectado || ocupado}
        onClick={() => void executar(() => autenticacao.enviarRecuperacao(email), tx('Se existe conta com esse e-mail, o link de recuperação já foi enviado.'))}>
        <Mail size={17} /> {t('Enviar link de recuperação')}</button>}

      {/* O Google aparece só quando existe de verdade. Ver "onlineConfigured". */}
      {google && modo !== 'recuperar' && <>
        <div className="account-ou"><span>{t('ou')}</span></div>
        <button className="secondary" disabled={!conectado || ocupado}
          onClick={() => void executar(() => autenticacao.entrarComGoogle(), tx('Abrindo o Google…'))}>
          <KeyRound size={16} /> {t('Continuar com Google')}
        </button>
      </>}
    </div>}

    {aviso && <p className={`account-aviso ${aviso.tipo}`} role="status">{t(aviso.texto)}</p>}
  </section>;
}
