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
import { emptyProgress } from './engine/progression';
import type { Profile } from './lib/storage';
import './styles.css';

const conta: Conta = { id: 'probe', email: 'voce@exemplo.com', handle: 'Uchihadam', origem: 'google' };
const perfil: Profile = {
  journeys: 12, victories: 4, best: 880, wins: 31,
  progress: { ...emptyProgress(), unlocked: ['a', 'b', 'c', 'd', 'e'], mastery: { goku: { grau: 2, feitos: {} }, sakura: { grau: 1, feitos: {} } } },
} as Profile;

const nada = () => Promise.resolve({ ok: true });
const autenticacao: Autenticacao = {
  conta: () => Promise.resolve(conta), criarConta: nada, entrar: nada, entrarComGoogle: nada,
  sair: nada, enviarRecuperacao: nada, definirNovaSenha: nada, observar: () => () => undefined,
} as unknown as Autenticacao;

createRoot(document.getElementById('root')!).render(
  <main className="app"><AccountScreen autenticacao={autenticacao} conta={conta} profile={perfil} conectado aoMudarPerfil={() => undefined} /></main>,
);
