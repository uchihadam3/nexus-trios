import { beforeEach, describe, expect, it, vi } from 'vitest';
import { enviosPendentes, guardarEnvio, reenviarPendentes } from '../src/lib/envios-pendentes';

const e = (runId: string) => ({ runId, digest: 'd'.repeat(64), dicas: false, em: '2026-10-13T00:00:00Z' });

describe('envios pendentes (jornadas que não chegaram ao servidor)', () => {
  beforeEach(() => {
    const m = new Map<string, string>();
    vi.stubGlobal('localStorage', { getItem: (k: string) => m.get(k) ?? null, setItem: (k: string, v: string) => void m.set(k, v), removeItem: (k: string) => void m.delete(k) });
  });

  it('guarda sem repetir a mesma jornada', () => {
    guardarEnvio(e('a')); guardarEnvio(e('a')); guardarEnvio(e('b'));
    expect(enviosPendentes().map((x) => x.runId)).toEqual(['a', 'b']);
  });

  it('reenviar tira da fila o que entrou e o que foi recusado de vez', async () => {
    guardarEnvio(e('ok')); guardarEnvio(e('velha')); guardarEnvio(e('ok2'));
    const n = await reenviarPendentes(async (x) => { if (x.runId === 'velha') throw new Error('Jornada já validada.'); });
    expect(n).toBe(2);
    expect(enviosPendentes()).toEqual([]);
  });

  it('sem internet, para e guarda tudo para a próxima vez', async () => {
    guardarEnvio(e('a')); guardarEnvio(e('b'));
    const n = await reenviarPendentes(async () => { throw new Error('Sem conexão com o servidor.'); });
    expect(n).toBe(0);
    expect(enviosPendentes().map((x) => x.runId)).toEqual(['a', 'b']);
  });
});
