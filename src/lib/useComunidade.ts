import { useCallback, useEffect, useRef, useState } from 'react';
import { PULSO_DA_PRESENCA_MS, type Jogador, type ServicoDaComunidade } from './comunidade';

/*
 * O que a Comunidade faz com o jogo aberto, em qualquer tela:
 *  - marca presença (online) a cada PULSO_DA_PRESENCA_MS enquanto a aba está visível, e avisa a saída ao esconder ou
 *    fechar o jogo — é isso que dá o "online desde" e o "saiu há X" na lista;
 *  - conta as privadas não lidas (o selo na tela inicial, no menu e na aba);
 *  - mostra o aviso de mensagem nova quando ela chega e a pessoa não está na Comunidade;
 *  - na tela inicial, quantos estão online agora e quem.
 */
export interface AvisoDeMensagem { de: string; nome: string; texto: string; quando: number }

export function useComunidade({ servico, ligado, euId, naComunidade, noInicio }: {
  servico: ServicoDaComunidade | null; ligado: boolean; euId: string | null; naComunidade: boolean; noInicio: boolean;
}) {
  const [naoLidas, setNaoLidas] = useState(0);
  const [aviso, setAviso] = useState<AvisoDeMensagem | null>(null);
  const [online, setOnline] = useState<Jogador[] | null>(null);
  const naComunidadeRef = useRef(naComunidade);
  naComunidadeRef.current = naComunidade;
  const ativo = ligado && !!servico && !!euId;

  const recontar = useCallback(async () => {
    if (!ativo) return [];
    try { const cs = await servico!.conversas(); setNaoLidas(cs.reduce((s, c) => s + c.naoLidas, 0)); return cs; } catch { return []; }
  }, [ativo, servico]);

  // presença
  useEffect(() => {
    if (!ativo) return;
    const ping = () => { if (document.visibilityState === 'visible') void servico!.ping().catch(() => undefined); };
    const sair = () => { void servico!.sair().catch(() => undefined); };
    ping();
    const t = setInterval(ping, PULSO_DA_PRESENCA_MS);
    const muda = () => { if (document.visibilityState === 'visible') ping(); else sair(); };
    document.addEventListener('visibilitychange', muda);
    addEventListener('pagehide', sair);
    return () => { clearInterval(t); document.removeEventListener('visibilitychange', muda); removeEventListener('pagehide', sair); };
  }, [ativo, servico]);

  // não lidas + aviso de mensagem nova
  useEffect(() => {
    if (!ativo) { setNaoLidas(0); return; }
    void recontar();
    const t = setInterval(() => void recontar(), 60_000);
    const parar = servico!.ouvir({
      mensagem: (m, tipo) => {
        if (tipo !== 'nova' || m.paraId !== euId) return;
        void recontar().then((cs) => {
          if (naComunidadeRef.current) return;
          const nome = cs.find((c) => c.comId === m.autorId)?.comNome ?? 'Alguém';
          setAviso({ de: m.autorId, nome, texto: m.texto, quando: Date.now() });
        });
      },
    });
    return () => { clearInterval(t); parar(); };
  }, [ativo, servico, euId, recontar]);

  // o aviso some sozinho
  useEffect(() => { if (!aviso) return; const t = setTimeout(() => setAviso(null), 6000); return () => clearTimeout(t); }, [aviso]);

  // quem está online, para a tela inicial
  useEffect(() => {
    if (!ativo || !noInicio) return;
    const busca = () => { servico!.jogadores().then((js) => setOnline(js.filter((j) => j.online && j.id !== euId))).catch(() => undefined); };
    busca();
    const t = setInterval(busca, 45_000);
    return () => clearInterval(t);
  }, [ativo, noInicio, servico, euId]);

  return { naoLidas, recontar, aviso, fecharAviso: () => setAviso(null), online };
}
