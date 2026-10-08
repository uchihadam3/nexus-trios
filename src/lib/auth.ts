/*
 * FASE I · contas reais.
 *
 * O documento pede e-mail/senha, Google, logout, recuperação de senha, sessão
 * persistida, sessão expirada e uma tela de Conta — com a regra de acesso
 * escrita em duas linhas: *"Casual pode ser guest. Online/Ranqueado exige
 * conta."*
 *
 * O que existia era `signInAnonymously()`: qualquer um publicava no ranking
 * sem conta nenhuma. Isso sai.
 *
 * Nada aqui guarda senha, token ou e-mail. Quem faz isso é o Supabase, no
 * armazenamento dele; este módulo só traduz o que ele devolve para um formato
 * que as telas entendem — e deliberadamente **não** expõe `access_token` nem
 * metadados do provedor para o resto do aplicativo, porque nenhuma tela
 * precisa disso e o que não circula não vaza.
 *
 * O cliente entra por injeção para que o comportamento possa ser testado sem
 * um Supabase de verdade.
 */
import type { AuthChangeEvent, Session, SupabaseClient } from '@supabase/supabase-js';

/** O que as telas podem saber sobre quem está logado. */
export interface Conta {
  id: string;
  /** Visível só para o próprio dono, na tela de Conta. Nunca vai ao ranking. */
  email: string | null;
  /** O nome público. Pode faltar enquanto o jogador não escolheu. */
  handle: string | null;
  /** Entrou por e-mail, Google, ou é uma sessão anônima herdada. */
  origem: 'email' | 'google' | 'convidado';
}

export interface ResultadoDaConta { ok: boolean; erro?: string; precisaConfirmarEmail?: boolean }

/*
 * O handle precisa casar com o `check` da tabela `players`:
 *   handle ~ '^[A-Za-z0-9_ ]{3,16}$' and handle = btrim(handle)
 *
 * Validar aqui não substitui a regra do banco — substituir seria perigoso.
 * Serve para o jogador saber o que está errado antes de a viagem ao servidor
 * voltar com um erro de constraint que ninguém entende.
 */
export const HANDLE_VALIDO = /^[A-Za-z0-9_ ]{3,16}$/;
export const validarHandle = (handle: string): string | null => {
  const limpo = handle.trim();
  if (limpo !== handle) return 'O nome não pode começar nem terminar com espaço.';
  if (limpo.length < 3) return 'O nome precisa de pelo menos 3 caracteres.';
  if (limpo.length > 16) return 'O nome pode ter no máximo 16 caracteres.';
  if (!HANDLE_VALIDO.test(limpo)) return 'Use apenas letras, números, espaço e _ no nome.';
  return null;
};

export const validarEmail = (email: string): string | null =>
  /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim()) ? null : 'E-mail inválido.';

/*
 * Oito caracteres é o mínimo do Supabase. Pedir mais aqui só empurraria o
 * jogador para a senha de sempre; a defesa real é o próprio Supabase, que
 * recusa senhas vazadas quando essa checagem está ligada no painel.
 */
export const validarSenha = (senha: string): string | null =>
  senha.length >= 8 ? null : 'A senha precisa de pelo menos 8 caracteres.';

/* ---------------------------------------------------------------------------
 * Para onde o Google devolve o jogador
 * ------------------------------------------------------------------------- */

/*
 * O endereço de volta precisa incluir o caminho base.
 *
 * No GitHub Pages o jogo vive em `/nexus-trios/`, não na raiz. Um `redirectTo`
 * sem o caminho leva a uma página que não existe, e o jogador volta do Google
 * para um 404 com o token pendurado na URL. `import.meta.env.BASE_URL` é
 * exatamente o que o Vite compilou, então acompanha dev e produção sozinho.
 */
export const enderecoDeVolta = (base = import.meta.env.BASE_URL, origem = globalThis.location?.origin ?? ''): string =>
  `${origem}${base.endsWith('/') ? base : `${base}/`}`;

/* ---------------------------------------------------------------------------
 * A tradução do que o Supabase devolve
 * ------------------------------------------------------------------------- */

const contaDaSessao = (sessao: Session | null): Conta | null => {
  const u = sessao?.user;
  if (!u) return null;
  /*
   * `is_anonymous` marca as sessões que o jogo criava antes desta fase. Elas
   * continuam válidas para jogar casual, mas não contam como conta.
   */
  const anonimo = u.is_anonymous === true;
  const provedor = (u.app_metadata as { provider?: string } | undefined)?.provider;
  return {
    id: u.id,
    email: anonimo ? null : u.email ?? null,
    handle: (u.user_metadata as { handle?: string } | undefined)?.handle ?? null,
    origem: anonimo ? 'convidado' : provedor === 'google' ? 'google' : 'email',
  };
};

/** Mensagens do Supabase vêm em inglês; as que o jogador vê, não. */
const traduzir = (mensagem: string): string => {
  const m = mensagem.toLowerCase();
  if (m.includes('invalid login credentials')) return 'E-mail ou senha incorretos.';
  if (m.includes('email not confirmed')) return 'Confirme o e-mail antes de entrar.';
  if (m.includes('user already registered')) return 'Já existe uma conta com esse e-mail.';
  if (m.includes('password should be')) return 'A senha precisa de pelo menos 8 caracteres.';
  if (m.includes('rate limit') || m.includes('too many')) return 'Muitas tentativas. Espere um minuto e tente de novo.';
  if (m.includes('provider is not enabled')) return 'O login com Google ainda não foi ligado neste projeto.';
  if (m.includes('network') || m.includes('fetch')) return 'Sem conexão com o servidor.';
  return mensagem;
};

/* ---------------------------------------------------------------------------
 * As operações
 * ------------------------------------------------------------------------- */

export interface Autenticacao {
  conta: () => Promise<Conta | null>;
  criarConta: (email: string, senha: string, handle: string) => Promise<ResultadoDaConta>;
  entrar: (email: string, senha: string) => Promise<ResultadoDaConta>;
  entrarComGoogle: () => Promise<ResultadoDaConta>;
  sair: () => Promise<ResultadoDaConta>;
  enviarRecuperacao: (email: string) => Promise<ResultadoDaConta>;
  definirNovaSenha: (senha: string) => Promise<ResultadoDaConta>;
  observar: (aviso: (conta: Conta | null, evento: AuthChangeEvent) => void) => () => void;
}

export function criarAutenticacao(client: SupabaseClient | null): Autenticacao {
  const semServidor = async (): Promise<ResultadoDaConta> =>
    ({ ok: false, erro: 'A conta online ainda não foi conectada neste build.' });

  if (!client) {
    return {
      conta: async () => null,
      criarConta: semServidor, entrar: semServidor, entrarComGoogle: semServidor,
      sair: semServidor, enviarRecuperacao: semServidor, definirNovaSenha: semServidor,
      observar: () => () => undefined,
    };
  }

  const tentar = async (acao: () => Promise<{ error: { message: string } | null }>): Promise<ResultadoDaConta> => {
    try {
      const { error } = await acao();
      return error ? { ok: false, erro: traduzir(error.message) } : { ok: true };
    } catch (e) {
      return { ok: false, erro: traduzir(e instanceof Error ? e.message : 'Falha inesperada.') };
    }
  };

  return {
    conta: async () => {
      const { data, error } = await client.auth.getSession();
      /*
       * Sessão expirada não é erro de programa: o jogador simplesmente volta a
       * ser convidado, e o jogo casual continua funcionando.
       */
      if (error) return null;
      return contaDaSessao(data.session);
    },

    criarConta: async (email, senha, handle) => {
      const problema = validarEmail(email) ?? validarSenha(senha) ?? validarHandle(handle);
      if (problema) return { ok: false, erro: problema };
      try {
        const { data, error } = await client.auth.signUp({
          email: email.trim(), password: senha,
          /* O handle viaja como metadado para o servidor criar o perfil público. */
          options: { data: { handle: handle.trim() }, emailRedirectTo: enderecoDeVolta() },
        });
        if (error) return { ok: false, erro: traduzir(error.message) };
        /* Sem sessão depois do cadastro quer dizer que o projeto exige confirmação. */
        return { ok: true, precisaConfirmarEmail: !data.session };
      } catch (e) {
        return { ok: false, erro: traduzir(e instanceof Error ? e.message : 'Falha inesperada.') };
      }
    },

    entrar: async (email, senha) => {
      const problema = validarEmail(email);
      if (problema) return { ok: false, erro: problema };
      return tentar(() => client.auth.signInWithPassword({ email: email.trim(), password: senha }));
    },

    entrarComGoogle: () => tentar(() => client.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: enderecoDeVolta() },
    }) as Promise<{ error: { message: string } | null }>),

    sair: () => tentar(() => client.auth.signOut()),

    enviarRecuperacao: async (email) => {
      const problema = validarEmail(email);
      if (problema) return { ok: false, erro: problema };
      return tentar(() => client.auth.resetPasswordForEmail(email.trim(), { redirectTo: enderecoDeVolta() }));
    },

    definirNovaSenha: async (senha) => {
      const problema = validarSenha(senha);
      if (problema) return { ok: false, erro: problema };
      return tentar(() => client.auth.updateUser({ password: senha }));
    },

    observar: (aviso) => {
      const { data } = client.auth.onAuthStateChange((evento, sessao) => { aviso(contaDaSessao(sessao), evento); });
      return () => { data.subscription.unsubscribe(); };
    },
  };
}

/*
 * A mesma camada de conta, com o Supabase baixado só no primeiro uso.
 *
 * Qualquer ação (`conta`, `entrar`, `sair`...) busca o cliente e repassa.
 * `observar` não busca: só se registra, e passa a ouvir quando o cliente
 * chegar, por quem quer que o tenha pedido. Assim o jogo pode se inscrever
 * para saber da conta na abertura sem, por isso, baixar o Supabase.
 */
export function criarAutenticacaoPreguicosa(carregar: () => Promise<SupabaseClient | null>): Autenticacao {
  type Ouvinte = Parameters<Autenticacao['observar']>[0];
  const ouvintes = new Set<Ouvinte>(), paradas = new Map<Ouvinte, () => void>();
  let instancia: Autenticacao | null = null, pedido: Promise<Autenticacao> | null = null;
  const obter = () => pedido ??= carregar().then((client) => {
    instancia = criarAutenticacao(client);
    for (const o of ouvintes) if (!paradas.has(o)) paradas.set(o, instancia.observar(o));
    return instancia;
  });
  return {
    conta: async () => (await obter()).conta(),
    criarConta: async (email, senha, handle) => (await obter()).criarConta(email, senha, handle),
    entrar: async (email, senha) => (await obter()).entrar(email, senha),
    entrarComGoogle: async () => (await obter()).entrarComGoogle(),
    sair: async () => (await obter()).sair(),
    enviarRecuperacao: async (email) => (await obter()).enviarRecuperacao(email),
    definirNovaSenha: async (senha) => (await obter()).definirNovaSenha(senha),
    observar: (aviso) => {
      ouvintes.add(aviso);
      if (instancia && !paradas.has(aviso)) paradas.set(aviso, instancia.observar(aviso));
      return () => { ouvintes.delete(aviso); paradas.get(aviso)?.(); paradas.delete(aviso); };
    },
  };
}
