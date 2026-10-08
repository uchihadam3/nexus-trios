/*
 * FASE I · o contrato da conta.
 *
 * Não existe Supabase alcançável deste contêiner — a política de rede do
 * ambiente nega o host — então o fluxo ponta a ponta tem que ser conferido no
 * navegador, por quem tem acesso. O que **é** verificável aqui, e é o que mais
 * erra na prática, está coberto: validação antes de gastar uma viagem ao
 * servidor, o endereço de volta do Google com o caminho base certo, a
 * tradução dos erros, a distinção entre convidado e conta, e o fato de nenhum
 * token circular fora deste módulo.
 */
import { describe, expect, it, vi } from 'vitest';
import type { SupabaseClient } from '@supabase/supabase-js';

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

import {
  criarAutenticacao, criarAutenticacaoPreguicosa, enderecoDeVolta, validarEmail, validarHandle, validarSenha,
} from '../src/lib/auth';

/** Um Supabase de mentira: registra o que foi chamado e devolve o que mandarem. */
const falso = (respostas: Record<string, unknown> = {}) => {
  const chamadas: { metodo: string; args: unknown[] }[] = [];
  const metodo = (nome: string, padrao: unknown = { data: {}, error: null }) =>
    vi.fn((...args: unknown[]) => { chamadas.push({ metodo: nome, args }); return Promise.resolve(respostas[nome] ?? padrao); });
  const client = {
    auth: {
      getSession: metodo('getSession', { data: { session: null }, error: null }),
      signUp: metodo('signUp', { data: { session: { user: {} } }, error: null }),
      signInWithPassword: metodo('signInWithPassword'),
      signInWithOAuth: metodo('signInWithOAuth'),
      signOut: metodo('signOut'),
      resetPasswordForEmail: metodo('resetPasswordForEmail'),
      updateUser: metodo('updateUser'),
      onAuthStateChange: vi.fn(() => ({ data: { subscription: { unsubscribe: vi.fn() } } })),
    },
  } as unknown as SupabaseClient;
  return { client, chamadas };
};

describe('validação, antes de incomodar o servidor', () => {
  it('reprova e-mail malformado', () => {
    expect(validarEmail('nada')).toBeTruthy();
    expect(validarEmail('a@b')).toBeTruthy();
    expect(validarEmail('jogador@exemplo.com')).toBeNull();
  });

  it('exige oito caracteres de senha', () => {
    expect(validarSenha('1234567')).toBeTruthy();
    expect(validarSenha('12345678')).toBeNull();
  });

  /*
   * O banco tem `handle ~ '^[A-Za-z0-9_ ]{3,16}$' and handle = btrim(handle)`.
   * Validar aqui não substitui essa regra — serve para o jogador saber o que
   * está errado antes de a viagem voltar com um erro de constraint.
   */
  it('segue a mesma regra de nome que a tabela players', () => {
    expect(validarHandle('ab')).toBeTruthy();
    expect(validarHandle('dezessete letras!')).toBeTruthy();
    expect(validarHandle(' espaco')).toBeTruthy();
    expect(validarHandle('espaco ')).toBeTruthy();
    expect(validarHandle('nome@invalido')).toBeTruthy();
    expect(validarHandle('Jogador_01')).toBeNull();
    expect(validarHandle('tres palavras ok')).toBeNull();
  });

  it('nem chega ao servidor quando os campos estão errados', async () => {
    const { client, chamadas } = falso();
    const a = criarAutenticacao(client);
    expect((await a.entrar('nada', 'x')).ok).toBe(false);
    expect((await a.criarConta('a@b.com', 'curta', 'Nome')).ok).toBe(false);
    expect((await a.criarConta('a@b.com', 'senhaboa1', 'ab')).ok).toBe(false);
    expect(chamadas.filter((c) => c.metodo !== 'getSession')).toHaveLength(0);
  });
});

describe('a volta do Google', () => {
  /*
   * No GitHub Pages o jogo vive em `/nexus-trios/`. Um endereço de volta sem o
   * caminho base leva a uma página que não existe, e o jogador volta do Google
   * para um 404 com o token pendurado na URL.
   */
  it('inclui o caminho base do deploy', () => {
    expect(enderecoDeVolta('/nexus-trios/', 'https://uchihadam3.github.io'))
      .toBe('https://uchihadam3.github.io/nexus-trios/');
    expect(enderecoDeVolta('/', 'http://localhost:5173')).toBe('http://localhost:5173/');
    /* Mesmo que a base venha sem a barra final. */
    expect(enderecoDeVolta('/nexus-trios', 'https://x.io')).toBe('https://x.io/nexus-trios/');
  });

  it('manda o endereço de volta para o Supabase', async () => {
    const { client, chamadas } = falso();
    await criarAutenticacao(client).entrarComGoogle();
    const chamada = chamadas.find((c) => c.metodo === 'signInWithOAuth');
    expect(chamada).toBeDefined();
    const opcoes = chamada!.args[0] as { provider: string; options: { redirectTo: string } };
    expect(opcoes.provider).toBe('google');
    expect(opcoes.options.redirectTo).toContain('/');
  });
});

describe('convidado e conta', () => {
  const sessaoCom = (user: Record<string, unknown>) => ({ data: { session: { user } }, error: null });

  it('sessão anônima é convidado, não conta', async () => {
    const { client } = falso({ getSession: sessaoCom({ id: 'u1', is_anonymous: true, email: 'x@y.com' }) });
    const conta = await criarAutenticacao(client).conta();
    expect(conta?.origem).toBe('convidado');
    /* E o e-mail de uma sessão anônima não é exposto nem para ela mesma. */
    expect(conta?.email).toBeNull();
  });

  it('reconhece de onde a conta veio', async () => {
    const porEmail = falso({ getSession: sessaoCom({ id: 'u2', email: 'a@b.com', app_metadata: { provider: 'email' } }) });
    expect((await criarAutenticacao(porEmail.client).conta())?.origem).toBe('email');
    const porGoogle = falso({ getSession: sessaoCom({ id: 'u3', email: 'a@b.com', app_metadata: { provider: 'google' } }) });
    expect((await criarAutenticacao(porGoogle.client).conta())?.origem).toBe('google');
  });

  it('lê o nome público dos metadados', async () => {
    const { client } = falso({ getSession: sessaoCom({ id: 'u4', email: 'a@b.com', user_metadata: { handle: 'Jogador_01' } }) });
    expect((await criarAutenticacao(client).conta())?.handle).toBe('Jogador_01');
  });

  /*
   * Sessão expirada não é erro de programa: o jogador volta a ser convidado e
   * o jogo casual continua funcionando.
   */
  it('sessão expirada vira ausência de conta, não exceção', async () => {
    const { client } = falso({ getSession: { data: { session: null }, error: { message: 'JWT expired' } } });
    await expect(criarAutenticacao(client).conta()).resolves.toBeNull();
  });

  /*
   * "Privado: e-mail, auth id, tokens, provider metadata." O que o módulo
   * devolve é exatamente o que as telas precisam, e nada mais.
   */
  it('nunca entrega token nem metadados do provedor', async () => {
    const { client } = falso({
      getSession: sessaoCom({ id: 'u5', email: 'a@b.com', app_metadata: { provider: 'google', secreto: 'x' } }),
    });
    const conta = await criarAutenticacao(client).conta();
    expect(Object.keys(conta!).sort()).toEqual(['email', 'handle', 'id', 'origem']);
    expect(JSON.stringify(conta)).not.toContain('secreto');
    expect(JSON.stringify(conta)).not.toContain('token');
  });
});

describe('erros em português', () => {
  it.each([
    ['Invalid login credentials', 'E-mail ou senha incorretos.'],
    ['Email not confirmed', 'Confirme o e-mail antes de entrar.'],
    ['User already registered', 'Já existe uma conta com esse e-mail.'],
    ['Unsupported provider: provider is not enabled', 'O login com Google ainda não foi ligado neste projeto.'],
  ])('traduz "%s"', async (original, esperado) => {
    const { client } = falso({ signInWithPassword: { data: {}, error: { message: original } } });
    const r = await criarAutenticacao(client).entrar('a@b.com', 'senhaboa1');
    expect(r.ok).toBe(false);
    expect(r.erro).toBe(esperado);
  });
});

describe('sem servidor configurado', () => {
  /*
   * Com `VITE_RANKED_ENABLED=false` o cliente é nulo. Nada pode explodir: o
   * jogo casual não depende de conta nenhuma.
   */
  it('todas as ações falham com aviso, nenhuma com exceção', async () => {
    const a = criarAutenticacao(null);
    expect(await a.conta()).toBeNull();
    for (const acao of [
      () => a.entrar('a@b.com', 'senhaboa1'), () => a.criarConta('a@b.com', 'senhaboa1', 'Nome'),
      () => a.entrarComGoogle(), () => a.sair(), () => a.enviarRecuperacao('a@b.com'),
      () => a.definirNovaSenha('senhaboa1'),
    ]) {
      const r = await acao();
      expect(r.ok).toBe(false);
      expect(r.erro).toBeTruthy();
    }
    expect(() => { a.observar(() => undefined)(); }).not.toThrow();
  });
});

describe('cadastro', () => {
  it('avisa quando o projeto exige confirmar o e-mail', async () => {
    const semSessao = falso({ signUp: { data: { session: null }, error: null } });
    const r = await criarAutenticacao(semSessao.client).criarConta('a@b.com', 'senhaboa1', 'Jogador_01');
    expect(r.ok).toBe(true);
    expect(r.precisaConfirmarEmail).toBe(true);
  });

  it('manda o nome público junto, para o servidor criar o perfil', async () => {
    const { client, chamadas } = falso();
    await criarAutenticacao(client).criarConta('a@b.com', 'senhaboa1', 'Jogador_01');
    const chamada = chamadas.find((c) => c.metodo === 'signUp');
    const corpo = chamada!.args[0] as { options: { data: { handle: string } } };
    expect(corpo.options.data.handle).toBe('Jogador_01');
  });
});

/*
 * O Supabase é quase metade do JavaScript do jogo. Quem só joga casual não
 * deveria baixá-lo — e quem se inscreveu para saber da conta não pode perder
 * o aviso por ele ter chegado depois.
 */
describe('Supabase sob demanda', () => {
  it('só busca o cliente quando alguém usa a conta', async () => {
    const { client } = falso();
    const carregar = vi.fn(() => Promise.resolve(client));
    const a = criarAutenticacaoPreguicosa(carregar);
    const parar = a.observar(() => undefined);
    expect(carregar).not.toHaveBeenCalled();
    await a.conta();
    await a.entrar('a@b.com', 'senhaboa1');
    expect(carregar).toHaveBeenCalledTimes(1);
    parar();
  });

  it('quem se inscreveu antes passa a ouvir quando o cliente chega', async () => {
    const { client } = falso();
    const a = criarAutenticacaoPreguicosa(() => Promise.resolve(client));
    a.observar(() => undefined);
    expect(client.auth.onAuthStateChange).not.toHaveBeenCalled();
    await a.conta();
    expect(client.auth.onAuthStateChange).toHaveBeenCalledTimes(1);
    /* E quem se inscreve depois também, uma vez só. */
    a.observar(() => undefined);
    expect(client.auth.onAuthStateChange).toHaveBeenCalledTimes(2);
  });

  it('quem desistiu antes do cliente chegar não é inscrito', async () => {
    const { client } = falso();
    const a = criarAutenticacaoPreguicosa(() => Promise.resolve(client));
    const parar = a.observar(() => undefined);
    parar();
    await a.conta();
    expect(client.auth.onAuthStateChange).not.toHaveBeenCalled();
  });

  it('sem servidor configurado continua respondendo sem quebrar', async () => {
    const a = criarAutenticacaoPreguicosa(() => Promise.resolve(null));
    expect(await a.conta()).toBeNull();
    expect((await a.entrar('a@b.com', 'senhaboa1')).ok).toBe(false);
  });

  /*
   * A trava: um `import { ... } from '@supabase/supabase-js'` comum em
   * qualquer arquivo do jogo puxaria a biblioteca inteira de volta para o
   * pacote principal. Só `import type` (que some na compilação) e o
   * `import()` dinâmico de lib/online.ts podem existir.
   */
  it('nenhum arquivo do jogo importa o Supabase diretamente', () => {
    const arquivos = (dir: string): string[] => readdirSync(dir).flatMap((n) => {
      const c = join(dir, n);
      return statSync(c).isDirectory() ? arquivos(c) : /\.tsx?$/.test(n) ? [c] : [];
    });
    const culpados = arquivos('src').filter((f) =>
      /^\s*import\s+(?!type\b)[^;]*from\s+['"]@supabase\//m.test(readFileSync(f, 'utf8')));
    expect(culpados).toEqual([]);
  });
});
