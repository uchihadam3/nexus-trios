/*
 * Banco de provas da tela de Conta.
 *
 * O estado "logado" depende do Supabase, que a rede deste ambiente não
 * alcança. Sem isto, o cartão da migração seria código que ninguém nunca viu
 * rodar. Aqui a tela recebe uma conta de mentira e desenha de verdade.
 */
import { createRoot } from 'react-dom/client';

import { AccountScreen } from './screens/AccountScreen';
import type { Autenticacao, Conta } from './lib/auth';
import type { Profile } from './lib/storage';
import './styles.css';

const conta: Conta = { id: 'probe', email: 'voce@exemplo.com', handle: 'Uchihadam', origem: 'google' };
const perfil: Profile = { journeys: 12, victories: 4, best: 8, wins: 31, recordePontos: 7_042_000 };

const nada = () => Promise.resolve({ ok: true });
const autenticacao: Autenticacao = {
  conta: () => Promise.resolve(conta), criarConta: nada, entrar: nada, entrarComGoogle: nada,
  sair: nada, enviarRecuperacao: nada, definirNovaSenha: nada, observar: () => () => undefined,
} as unknown as Autenticacao;

createRoot(document.getElementById('root')!).render(
  <main className="app"><AccountScreen autenticacao={autenticacao} conta={conta} profile={perfil} conectado aoMudarPerfil={() => undefined} /></main>,
);
