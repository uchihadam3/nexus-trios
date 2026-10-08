#!/usr/bin/env python3
"""
Música de fundo da batalha (adendo, parte 6).

O pedido: música de fundo, boa de ouvir, que não atrapalha, não vira
barulheira e não fica repetitiva. Então:

- andamento calmo (84 BPM), ré menor com cores dórias, acordes com sétimas e
  nonas abertas;
- 64 compassos (~3 min) em quatro seções que não se repetem iguais: A (tema
  respirando), B (sobe um pouco), C (suspensa, mais aberta), A' (volta com
  variações) — e o jogo começa cada luta numa seção diferente;
- três camadas que o jogo mistura pela intensidade da luta:
  * base: pad quente, baixo macio e ar — sempre;
  * pulso: percussão leve (escovinha, bumbo macio) e um arpejo dedilhado;
  * tema: uma melodia esparsa, que só aparece quando a luta esquenta;
- nada de agudo estridente: tudo passa por filtro e reverberação de sala.

O laço é perfeito: o rabo da reverberação do fim é somado ao começo.

Uso: python3 tools/audio/generate_music_v2.py   (gera public/assets/audio/musica-*.ogg)
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, sosfilt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from som import passa_tudo, pente  # noqa: E402

SR = 32000                     # música de fundo: 32 kHz basta e economiza dados no celular
BPM = 84
BEAT = 60 / BPM
BAR = BEAT * 4
BARS = 64
DUR = BAR * BARS
N = int(round(DUR * SR))
CAUDA = int(4 * SR)            # sobra para a reverberação, somada ao começo depois
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get("SAIDA_MUSICA", ROOT / "public/assets/audio"))
rng = np.random.default_rng(84064)


def hz(m: float) -> float:
    return 440 * 2 ** ((m - 69) / 12)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "lowpass", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "highpass", fs=SR, output="sos"), x)


def bp(x, a, b, o=2):
    return sosfilt(butter(o, [a, b], "bandpass", fs=SR, output="sos"), x)


def sala(x, tamanho=0.85, umido=0.35, escuro=5000):
    """Reverberação estéreo simples (pentes diferentes em cada lado), em blocos."""
    def lado(sig, atrasos):
        y = sum(pente(sig, d, 0.78 + 0.18 * tamanho) for d in atrasos) / len(atrasos)
        for d, g in ((347, 0.6), (113, 0.6)):
            y = passa_tudo(y, d, g)
        return lp(hp(y, 180), escuro)
    mono = x.mean(axis=1)
    l = lado(mono, [1557, 1617, 1491, 1422])
    r = lado(mono, [1277, 1356, 1188, 1116])
    return x * (1 - umido * 0.3) + np.stack([l, r], 1) * umido


def estereo(sinal, pan=0.0):
    a = (pan + 1) * math.pi / 4
    return np.stack([sinal * math.cos(a), sinal * math.sin(a)], 1)


def soma(dest, x, em):
    i = int(round(em * SR))
    j = min(len(dest), i + len(x))
    if j > i:
        dest[i:j] += x[: j - i]


def env(n, ataque, solta, total=None):
    t = np.arange(n) / SR
    dur = n / SR
    a = np.clip(t / max(ataque, 1e-3), 0, 1) ** 1.5
    r = np.clip((dur - t) / max(solta, 1e-3), 0, 1) ** 1.2
    return a * r


# ------------------------------------------------------------------ harmonia
# (graus como acordes em MIDI, a partir de ré). Cada seção = 16 compassos, acorde a cada 2.
A = [[50, 57, 62, 65, 69], [46, 53, 58, 62, 65], [41, 48, 57, 60, 64], [48, 55, 60, 64, 67]] * 2          # Dm9 Bbmaj7 F(add9) C
B = [[43, 50, 58, 62, 65], [50, 57, 62, 65, 69], [46, 53, 58, 62, 69], [45, 52, 57, 60, 64]] * 2          # Gm Dm Bb Am
C = [[46, 53, 60, 62, 65], [48, 55, 62, 64, 67], [50, 57, 64, 65, 69], [50, 57, 62, 64, 69]] * 2          # Bb(add9) C(sus) Dm(add9) Dsus
A2 = [[50, 57, 62, 64, 69], [46, 53, 58, 62, 67], [41, 48, 55, 60, 64], [48, 55, 62, 64, 67]] * 2
SECOES = [("A", A), ("B", B), ("C", C), ("A2", A2)]
ACORDES = [c for _, sec in SECOES for c in sec]            # 32 acordes de 2 compassos


# ------------------------------------------------------------------ camadas
def pad() -> np.ndarray:
    out = np.zeros((N + CAUDA, 2))
    for i, acorde in enumerate(ACORDES):
        ini = i * 2 * BAR
        dur = 2 * BAR + 0.9
        n = int(dur * SR)
        t = np.arange(n) / SR
        for k, m in enumerate(acorde[1:]):
            for lado, det in ((-0.6, -0.07), (0.6, 0.07)):
                f = hz(m) * 2 ** (det / 12)
                fase = 2 * math.pi * f * t + rng.uniform(0, 6)
                # serra macia com poucos harmônicos e um tremor lento
                s = sum(np.sin(h * fase) / h ** 1.6 for h in range(1, 6))
                s *= 1 + 0.08 * np.sin(2 * math.pi * 0.23 * t + k)
                soma(out, estereo(s * env(n, 0.9, 1.1) * 0.035, lado), ini)
    out[:, 0] = lp(out[:, 0], 1900)
    out[:, 1] = lp(out[:, 1], 1900)
    return out


def baixo() -> np.ndarray:
    out = np.zeros((N + CAUDA, 2))
    for i, acorde in enumerate(ACORDES):
        raiz = acorde[0] - 12
        for b in range(2):
            ini = (i * 2 + b) * BAR
            for batida, dur, g in ((0, 2.5, 1.0), (2.5, 1.5, 0.6)):
                n = int(dur * BEAT * SR)
                t = np.arange(n) / SR
                f = hz(raiz + (7 if (b == 1 and batida > 0 and i % 2) else 0))
                s = np.sin(2 * math.pi * f * t) + 0.25 * np.sin(4 * math.pi * f * t)
                s = np.tanh(s * 1.3)
                soma(out, estereo(s * env(n, 0.03, 0.25) * 0.11 * g, 0), ini + batida * BEAT)
    out[:, 0] = lp(out[:, 0], 600)
    out[:, 1] = lp(out[:, 1], 600)
    return out


def ar() -> np.ndarray:
    n = N + CAUDA
    ruido = rng.standard_normal((n, 2))
    x = bp(ruido[:, 0], 2500, 6000), bp(ruido[:, 1], 2500, 6000)
    t = np.arange(n) / SR
    onda = 0.5 + 0.5 * np.sin(2 * math.pi * t / (BAR * 8))
    return np.stack(x, 1) * (0.004 + 0.004 * onda)[:, None]


def percussao() -> np.ndarray:
    out = np.zeros((N + CAUDA, 2))
    for bar in range(BARS):
        sec = bar // 16
        for batida in range(8):                                         # colcheias
            em = bar * BAR + batida * BEAT / 2
            # escovinha: ruído filtrado curtinho, forte nos tempos, leve nos contratempos
            n = int(0.09 * SR)
            g = (0.022 if batida % 2 == 0 else 0.013) * (0.85 + 0.3 * rng.random())
            if sec == 2 and batida % 2:                                  # a seção C respira
                g *= 0.5
            esc = bp(rng.standard_normal(n), 4000, 9000) * np.exp(-np.arange(n) / SR / 0.025) * g
            soma(out, estereo(esc, 0.35 if batida % 2 else -0.25), em)
        for batida, g in ((0, 1.0), (2.5, 0.55)) if bar % 4 != 3 else ((0, 1.0), (2, 0.7), (3.5, 0.5)):
            n = int(0.35 * SR)
            t = np.arange(n) / SR
            f = 52 + 40 * np.exp(-t / 0.03)
            k = np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12) * 0.09 * g   # bumbo macio
            soma(out, estereo(k, 0), bar * BAR + batida * BEAT)
        if bar % 2 == 1:                                                 # aro, só no tempo 3 de compassos alternados
            n = int(0.06 * SR)
            aro = bp(rng.standard_normal(n), 900, 2600) * np.exp(-np.arange(n) / SR / 0.012) * 0.03
            soma(out, estereo(aro, 0.15), bar * BAR + 2 * BEAT)
    return out


def arpejo() -> np.ndarray:
    out = np.zeros((N + CAUDA, 2))
    padroes = [[1, 2, 3, 4, 3, 2, 3, 1], [1, 3, 2, 4, 2, 3, 4, 2], [2, 3, 4, 3, 1, 3, 2, 4]]
    for bar in range(BARS):
        acorde = ACORDES[bar // 2]
        padrao = padroes[(bar // 4 + (bar // 16)) % 3]
        for k, idx in enumerate(padrao):
            if (bar // 16) == 2 and k % 2:                               # a seção C fica mais rala
                continue
            m = acorde[idx] + 12
            n = int(0.9 * SR)
            t = np.arange(n) / SR
            f = hz(m)
            s = (np.sin(2 * math.pi * f * t) + 0.3 * np.sin(4 * math.pi * f * t) + 0.1 * np.sin(6 * math.pi * f * t))
            s *= np.exp(-t / 0.28) * (1 - np.exp(-t / 0.004))
            g = 0.03 * (0.8 + 0.25 * rng.random()) * (1.1 if k == 0 else 1)
            soma(out, estereo(s * g, -0.45 if k % 2 else 0.45), bar * BAR + k * BEAT / 2)
    out[:, 0] = lp(out[:, 0], 4200)
    out[:, 1] = lp(out[:, 1], 4200)
    return out


def tema() -> np.ndarray:
    """Melodia esparsa: frases de 4 compassos, uma voz de flauta macia; cada seção varia a frase."""
    out = np.zeros((N + CAUDA, 2))
    frases = {
        "A": [(0, 74, 1.5), (1.5, 72, 0.5), (2, 69, 2), (4, 72, 1), (5, 74, 1), (6, 77, 2), (8, 76, 3), (12, 74, 1), (13, 72, 1), (14, 69, 2)],
        "B": [(0, 70, 2), (2, 69, 1), (3, 67, 1), (4, 69, 2.5), (8, 74, 1.5), (9.5, 72, 0.5), (10, 70, 2), (12, 69, 4)],
        "C": [(0, 77, 3), (4, 79, 2), (6, 76, 2), (8, 77, 4), (12, 74, 4)],
        "A2": [(0, 74, 1), (1, 76, 1), (2, 77, 2), (4, 76, 1.5), (5.5, 74, 0.5), (6, 72, 2), (8, 74, 2), (10, 69, 2), (12, 72, 1), (13, 74, 3)],
    }
    for s_i, (nome, _) in enumerate(SECOES):
        for rep in range(4):                                             # 4 frases de 4 compassos por seção
            if nome != "C" and rep == 1:
                continue                                                 # respiro: a melodia some uma frase
            base = (s_i * 16 + rep * 4) * BAR
            transp = 0 if rep < 2 else (-2 if nome == "B" else 0)
            for i, (beat, m, dur) in enumerate(frases[nome]):
                if rep == 3 and i % 3 == 2:
                    continue                                             # variação: tira notas na última frase
                n = int((dur * BEAT + 0.4) * SR)
                t = np.arange(n) / SR
                f = hz(m + transp)
                vib = 1 + 0.004 * np.sin(2 * math.pi * 5.2 * t) * np.clip((t - 0.25) / 0.3, 0, 1)
                fase = 2 * math.pi * np.cumsum(f * vib) / SR
                s = np.sin(fase) + 0.18 * np.sin(2 * fase) + 0.05 * np.sin(3 * fase)
                sopro = bp(rng.standard_normal(n), f * 0.9, min(f * 4, SR * 0.45)) * 0.05
                s = (s + sopro) * env(n, 0.07, 0.35) * 0.05
                soma(out, estereo(s, 0.05), base + beat * BEAT)
    out[:, 0] = lp(out[:, 0], 5000)
    out[:, 1] = lp(out[:, 1], 5000)
    return out


def fecha_laco(x: np.ndarray) -> np.ndarray:
    """Soma o rabo (depois do fim) no começo: o laço emenda sem buraco nem estalo."""
    y = x[:N].copy()
    y[:CAUDA] += x[N:N + CAUDA]
    return y


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    camadas = {
        "musica-base": sala(pad() + baixo() + ar(), 0.9, 0.3, 4200),
        "musica-pulso": sala(percussao() + arpejo(), 0.75, 0.25, 6000),
        "musica-tema": sala(tema(), 0.95, 0.42, 5500),
    }
    # mesma escala para as três (o jogo mistura por cima); pico conjunto em −3 dBFS
    juntas = sum(fecha_laco(x) for x in camadas.values())
    escala = 10 ** (-3 / 20) / (np.max(np.abs(juntas)) + 1e-9)
    info = {}
    for nome, x in camadas.items():
        y = (fecha_laco(x) * escala).astype(np.float32)
        destino = OUT / f"{nome}.ogg"
        # a melodia é central: vai em mono e economiza metade; o resto fica estéreo
        mono = nome == "musica-tema"
        if mono:
            y = y.mean(axis=1, keepdims=True)
        # em blocos de 1 s: o codificador Vorbis do libsndfile cai com arquivos longos de uma vez só
        with sf.SoundFile(destino, "w", SR, 1 if mono else 2, format="OGG", subtype="VORBIS", compression_level=0.9) as arq:
            for i in range(0, len(y), SR):
                arq.write(y[i:i + SR])
        rms = 20 * math.log10(np.sqrt(np.mean(y ** 2)) + 1e-12)
        info[nome] = {"arquivo": destino.name, "segundos": round(N / SR, 3), "bytes": destino.stat().st_size, "rmsDb": round(rms, 1)}
        print(f"{nome:14s} {destino.stat().st_size / 1024:7.1f} KB  rms {rms:5.1f} dB")
    secoes = [{"nome": n, "inicio": round(i * 16 * BAR, 3)} for i, (n, _) in enumerate(SECOES)]
    (OUT / "musica.json").write_text(json.dumps({"bpm": BPM, "compassos": BARS, "segundos": round(N / SR, 3), "secoes": secoes, "camadas": info}, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
