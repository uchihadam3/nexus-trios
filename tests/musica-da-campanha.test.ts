import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { FAIXAS, REGIOES_DA_MUSICA } from '../src/lib/audio';
import { REGIOES } from '../src/engine/campanha';

/* O Caminho do Nexus (v9, tools/audio/generate_music_v9.py): uma música por região e uma por chefe. */
const root = resolve(__dirname, '..');
interface Info { bpm: number; compassos: number; segundos: number; secoes: { nome: string; inicio: number }[]; laco: { inicio: number }; camadas: Record<string, { arquivo: string; mp3: string; rmsDb: number }> }
const ler = (nome: string) => JSON.parse(readFileSync(resolve(root, `public/assets/audio/${nome}.json`), 'utf8')) as Info;
const principal = ler('musica');

describe('as músicas do Caminho do Nexus', () => {
  it('cada região do mapa tem a sua música e a do chefe', () => {
    expect([...REGIOES_DA_MUSICA]).toEqual(REGIOES.map((r) => r.id));
  });
  for (const regiao of REGIOES_DA_MUSICA) {
    for (const [faixa, arquivo] of [[`regiao-${regiao}`, `musica-reg-${regiao}`], [`chefe-${regiao}`, `musica-chefe-${regiao}`]] as const) {
      it(`${faixa}: três camadas em OGG e MP3, o laço no Tema e o mesmo volume da música principal`, () => {
        const m = ler(arquivo);
        expect(m.secoes.map((s) => s.nome)).toEqual(['Abertura', 'Tema', 'Ação', 'Respiro', 'Hino', 'Refrão', 'Volta']);
        expect(m.compassos).toBe(72);
        expect(m.segundos).toBeCloseTo((m.compassos * 4 * 60) / m.bpm, 1);
        expect(FAIXAS[faixa].laco).toBeCloseTo(m.laco.inicio, 2);
        expect(m.secoes[1]!.inicio).toBeCloseTo(m.laco.inicio, 2);
        expect(FAIXAS[faixa].camadas.map((c) => c.split('/').pop())).toEqual(Object.values(m.camadas).map((c) => c.arquivo));
        for (const c of Object.values(m.camadas)) {
          const ogg = readFileSync(resolve(root, 'public/assets/audio', c.arquivo));
          expect(ogg.subarray(0, 4).toString('ascii')).toBe('OggS');
          expect(ogg.length).toBeLessThan(2_600_000);
          expect(readFileSync(resolve(root, 'public/assets/audio', c.mp3)).length).toBeLessThan(2_600_000);
        }
        for (const c of ['base', 'pulso', 'tema']) expect(Math.abs(m.camadas[`${arquivo}-${c}`]!.rmsDb - principal.camadas[`musica-${c}`]!.rmsDb)).toBeLessThan(2.5);
      });
    }
  }
});
