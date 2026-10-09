#!/usr/bin/env python3
"""
Músicas de batalha v5: mais duas faixas, no mesmo som da v4 ("anime arcade").

Pedido do jogador: a música de agora fica nas lutas 1 a 5; das lutas 6 a 9
entra uma música mais séria, com mais tensão (as lutas ficam mais difíceis); e
na luta 10, a do chefe, uma música de chefe de verdade. As duas no nível da de
agora e combinando com o jogo.

As duas usam os mesmos instrumentos da v4 (bateria de rock, baixo
sintetizado, guitarras distorcidas, supersaw, arpejo de faíscas, pad), com o
peso orquestral que um jogo de luta de anime põe nas lutas sérias (coro,
metais, tímpano, cordas em spiccato, sinos — da v3).

TENSÃO (lutas 6–9) — ré menor harmônica, 150 BPM, 80 compassos (~2 min 8 s)
  Intro      cordas correndo como um relógio, tímpano, coro entrando
  Perigo     riff 3+3+2 (acentos quebrados), tema sombrio nos metais
  Pressão    meio-tempo pesado, coro, tema longo e sério
  Ruptura    tudo cai: relógio, lamento, e a carga subindo
  Confronto  o tema maior, bumbo duplo, e a música sobe meio tom (mi bemol)
  Retorno    o baixo sobe nota a nota (cromático) até voltar ao Perigo
  (o laço volta para o Perigo)

CHEFE (luta 10) — dó menor com o segundo grau frígio (ré bemol), 168 BPM,
80 compassos (~1 min 54 s)
  Aparição      sinos, coro, tambores: o chefe chega
  Duelo         galope, o tema do chefe nos metais e na guitarra-solo
  Fúria         bumbo em semicolcheias, arpejos rápidos, metais em resposta
  Desespero     meio-tempo, coro e sinos, um lamento
  Último golpe  hino em dó menor e o refrão final um tom acima (ré menor,
                cadência andaluza), tudo junto
  Virada        riff frígio (dó / ré bemol) e a subida de volta ao Duelo
  (o laço volta para o Duelo)

Cada faixa sai nas mesmas três camadas da v4 (base, pulso, tema), em OGG e
MP3, com o mesmo volume de cada camada: o jogo sobe pulso e tema quando a luta
esquenta, igual à música de agora.

Uso: python3 tools/audio/generate_music_v5.py [tensao|chefe]
     (gera public/assets/audio/musica-<faixa>-*.ogg/.mp3 e musica-<faixa>.json)
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_music_v3 as v3  # noqa: E402
import generate_music_v4 as v4  # noqa: E402
from generate_music_v3 import bp, escreve_mp3, hp, lp, pan, sala  # noqa: E402
from generate_music_v4 import baixo, bumbo, caixa, chimbal, conducao, eco, faisca, guitarra, impacto, pad, power, prato, riser, supersaw, tom  # noqa: E402

SR = v3.SR
OUT = v3.OUT
CAUDA = int(3 * SR)


def n_(seg):
    return max(1, int(seg * SR))


# ================================================================== instrumentos novos (a partir da v3)
def metal(nota, dur, forte=1.0, brilho=1.0, lado=0.0):
    """Metais sintéticos (v3), no nível do supersaw da v4."""
    return pan(v3.i_metal(nota, dur, 1.0, brilho) * 0.42 * forte, lado)


def metais(notas, dur, forte=1.0, brilho=1.0):
    """Acorde de metais: cada nota num lugar do palco."""
    x = None
    for k, m in enumerate(notas):
        y = metal(m, dur, forte / max(1, len(notas)) * 1.6, brilho, (k - (len(notas) - 1) / 2) * 0.35)
        x = y if x is None else _soma(x, y)
    return x


def _soma(a, b):
    n = max(len(a), len(b))
    out = np.zeros((n, 2))
    out[: len(a)] += a
    out[: len(b)] += b
    return out


def coro(notas, dur, forte=1.0):
    return v3.i_coro(notas, dur, 1.15 * forte)


def cordas(nota, dur, forte=1.0):
    """Cordas em spiccato: o "relógio" que corre por baixo."""
    return v3.i_cordas_curtas(nota, dur, 2.2 * forte)


def sino_grande(nota, forte=1.0):
    """Sino de torre (o chefe chega): o sino da v3 com um corpo grave e o golpe do badalo."""
    x = v3.i_sino(nota, 1.0) * 0.55
    n = len(x)
    t = np.arange(n) / SR
    corpo = np.sin(2 * math.pi * v3.hz(nota - 12) * t) * np.exp(-t / 1.1) * 0.25
    golpe = bp(v3.ruido(n), 1500, 6000) * np.exp(-t / 0.012) * 0.2
    return (x + corpo + golpe) * forte


def timpano(nota, forte=1.0, dur=1.6):
    return v3.i_timpano(nota, 0.75 * forte, dur)


def taiko(forte=1.0):
    return v3.i_taiko(0.55 * forte)


# ================================================================== a música
class Musica:
    """Uma faixa: tempo, compassos, seções, harmonia e as seis pistas que viram as três camadas."""

    def __init__(self, nome, bpm, prog, acordes, secoes, laco, semente):
        self.nome, self.bpm = nome, bpm
        self.BEAT = 60 / bpm
        self.BAR = self.BEAT * 4
        self.S16 = self.BEAT / 4
        self.prog, self.acordes, self.secoes, self.laco = prog, acordes, secoes, laco
        self.compassos = len(prog)
        self.N = int(round(self.compassos * self.BAR * SR))
        forma = (self.N + CAUDA, 2)
        self.base, self.pulso, self.tema = np.zeros(forma), np.zeros(forma), np.zeros(forma)
        self.base_sala, self.tema_eco, self.pulso_eco = np.zeros(forma), np.zeros(forma), np.zeros(forma)
        v4.rng = np.random.default_rng(semente)
        v3.rng = np.random.default_rng(semente + 1)
        # bateria (amostras feitas uma vez)
        self.BUMBO, self.BUMBO_F = bumbo(0.8), bumbo(1.0)
        self.CAIXA, self.CAIXA_F, self.CAIXA_FANTASMA = caixa(1.0), caixa(1.2), caixa(0.3)
        self.CHIMBAL, self.CHIMBAL_F, self.CHIMBAL_ABERTO = chimbal(False, 0.7), chimbal(False, 1.0), chimbal(True)
        self.CONDUCAO, self.PRATO, self.IMPACTO = conducao(), prato(), impacto()

    # ------------------------------------------------ utilidades
    def t(self, b):
        return b * self.BAR

    def secao(self, b):
        atual, ini = self.secoes[0]
        for nome, i in self.secoes:
            if b >= i:
                atual, ini = nome, i
        return atual, b - ini

    def acorde(self, b):
        return self.acordes[self.prog[b]]

    @staticmethod
    def poe(dest, x, em, ganho=1.0):
        v3.poe(dest, x * ganho if ganho != 1.0 else x, em)

    def bat(self, posicoes, amostra, dest, t0, ganho=1.0):
        for p in posicoes:
            self.poe(dest, amostra, t0 + p * self.S16, ganho)

    def rufo(self, compassos, inicio=0.2):
        """Rufo de caixa que acelera e cresce até a próxima fase."""
        sinal = np.zeros(n_(compassos * self.BAR + 0.5))
        pos, total = 0.0, compassos * self.BAR
        while pos < total:
            u = pos / total
            s = caixa(inicio + (1 - inicio) * u)
            i = int(pos * SR)
            sinal[i:i + len(s)] += s[: len(sinal) - i]
            pos += self.S16 if u < 0.5 else self.S16 / 2
        return sinal

    def virada_de_tons(self, t0, notas, forte=1.0):
        """Virada de tons na segunda metade do compasso."""
        for k, m in enumerate(notas):
            self.poe(self.base, tom(m, forte), t0 + (16 - len(notas) + k) * self.S16)

    def frase(self, dest, frase, t0, transp=0, forte=1.0, brilho=5200, dobra=None, voz="saw", ganho_dobra=0.45):
        """Toca uma melodia (início e duração em tempos, nota MIDI)."""
        for ini, dur, m in frase:
            d = dur * self.BEAT * 0.94
            em = t0 + ini * self.BEAT
            if voz in ("saw", "ambos"):
                self.poe(dest, supersaw(m + transp, d, forte, brilho), em)
            if voz in ("metal", "ambos"):
                self.poe(dest, metal(m + transp - (12 if voz == "ambos" else 0), d, forte * (0.7 if voz == "ambos" else 1.0)), em)
            if dobra is not None:
                self.poe(dest, supersaw(m + transp + dobra, d, forte * ganho_dobra, brilho * 0.8, False), em)

    # ------------------------------------------------ mixagem e arquivos (como a v4)
    def renderiza(self, estilo):
        B = self.BEAT
        tema = self.tema + eco(self.tema_eco, B * 0.75, 0.28, 3) + sala(self.tema_eco, 0.75, 0.2)
        pulso = self.pulso + eco(self.pulso_eco, B * 0.75, 0.3, 3)
        base = self.base + sala(self.base_sala, 0.65, 0.24)
        pulso = sala(pulso, 0.4, 0.08)

        # equalização para alto-falante de celular: grave contido, médio presente
        def eq(x, corte_grave, presenca):
            x = hp(x, 35, 2)
            x = x - corte_grave * lp(x, 130, 2)
            return x + presenca * bp(x, 1300, 4500, 2)
        base, pulso, tema = eq(base, 0.45, 0.2), eq(pulso, 0.6, 0.25), eq(tema, 0.2, 0.3)

        ini_laco = int(round(self.laco * self.BAR * SR))

        def fecha(x):
            y = x[: self.N].copy()
            y[ini_laco:ini_laco + CAUDA] += x[self.N:self.N + CAUDA]
            return y

        pre = f"musica-{self.nome}"
        camadas = {f"{pre}-base": fecha(base), f"{pre}-pulso": fecha(pulso), f"{pre}-tema": fecha(tema)}
        # o mesmo equilíbrio da música de agora (v4): a base mais presente, pulso e tema por baixo
        alvo_db = {f"{pre}-base": -19.5, f"{pre}-pulso": -23.0, f"{pre}-tema": -21.5}
        for k, x in camadas.items():
            rms = 20 * math.log10(float(np.sqrt(np.mean(x ** 2))) + 1e-12)
            camadas[k] = x * 10 ** ((alvo_db[k] - rms) / 20)
        soma = sum(camadas.values())
        ganho = min(1.0, 0.89 / np.max(np.abs(soma)))
        if os.environ.get("PREVIA_MUSICA"):
            # a mistura das três camadas, para ouvir fora do jogo
            escreve_mp3(Path(os.environ["PREVIA_MUSICA"]) / f"{pre}.mp3", (soma * ganho).astype(np.float32), SR)
        info = {}
        OUT.mkdir(parents=True, exist_ok=True)
        for nome, x in camadas.items():
            y = (x * ganho).astype(np.float32)
            destino = OUT / f"{nome}.ogg"
            with sf.SoundFile(destino, "w", SR, 2, format="OGG", subtype="VORBIS", compression_level=0.92) as arq:
                for i in range(0, len(y), SR):
                    arq.write(y[i:i + SR])
            escreve_mp3(OUT / f"{nome}.mp3", y, SR)
            rms = 20 * math.log10(float(np.sqrt(np.mean((x * ganho) ** 2))) + 1e-9)
            info[nome] = {"arquivo": destino.name, "mp3": f"{nome}.mp3", "segundos": round(self.N / SR, 3), "bytes": destino.stat().st_size, "rmsDb": round(rms, 1)}
            print(f"{nome:22s} {destino.stat().st_size / 1024:7.1f} KB  rms {rms:6.1f} dB")
        secoes = [{"nome": s, "inicio": round(i * self.BAR, 3)} for s, i in self.secoes]
        (OUT / f"{pre}.json").write_text(json.dumps({
            "bpm": self.bpm, "compassos": self.compassos, "segundos": round(self.N / SR, 3), "secoes": secoes, "estilo": estilo,
            "laco": {"inicio": round(self.laco * self.BAR, 3), "fim": round(self.N / SR, 3)}, "camadas": info,
        }, indent=1, ensure_ascii=False) + "\n")


# ================================================================== TENSÃO (lutas 6–9)
ACORDES_TENSAO = {  # nome -> (raiz do baixo, notas do pad)
    "Dm": (38, [50, 53, 57]), "Bb": (34, [46, 50, 53]), "Gm": (43, [55, 58, 62]), "A": (45, [57, 61, 64]),
    "C": (36, [48, 52, 55]), "Eb": (39, [51, 55, 58]),
    # o Confronto meio tom acima (mi bemol menor)
    "B": (35, [47, 51, 54]), "Db": (37, [49, 53, 56]), "Ebm": (39, [51, 54, 58]),
}
PROG_TENSAO = (["Dm"] * 4 + ["Bb", "Bb", "A", "A"]                                          # Intro 0–7
               + ["Dm", "Dm", "Bb", "A", "Dm", "Dm", "Eb", "A"] * 2                         # Perigo 8–23
               + ["Gm", "Dm", "Bb", "A", "Gm", "Dm", "Bb", "A"]                             # Pressão 24–39
               + ["Gm", "Dm", "Eb", "A", "Gm", "Bb", "A", "A"]
               + ["Dm", "Dm", "Bb", "Bb", "Gm", "Gm", "A", "A"]                             # Ruptura 40–47
               + ["Bb", "C", "Dm", "Dm", "Bb", "C", "A", "A"]                               # Confronto 48–55
               + ["B", "Db", "Ebm", "Ebm", "B", "Db", "Bb", "Bb"] * 2                       # Confronto +½ tom 56–71
               + ["Dm"] * 4 + ["A"] * 4)                                                    # Retorno 72–79
SECOES_TENSAO = [("Intro", 0), ("Perigo", 8), ("Pressão", 24), ("Ruptura", 40), ("Confronto", 48), ("Retorno", 72)]

# o tema do Perigo: começa embaixo, sobe, e para no dó sustenido (a sensível) — fica no ar
TEMA_PERIGO = [(0, 1.5, 74), (1.5, .5, 76), (2, 1, 77), (3, 1, 81),
               (4, 2, 82), (6, .5, 81), (6.5, .5, 79), (7, 1, 81),
               (8, 1.5, 77), (9.5, .5, 79), (10, 1, 81), (11, 1, 86),
               (12, 3, 85), (15, 1, 81),
               (16, 1.5, 74), (17.5, .5, 76), (18, 1, 77), (19, 1, 81),
               (20, 1, 86), (21, 1, 84), (22, 1, 82), (23, 1, 81),
               (24, 2, 79), (26, 1, 82), (27, 1, 87),
               (28, 1, 85), (29, 1, 82), (30, 2, 81)]
# a Pressão: notas longas, sérias, e a segunda metade mais alta
TEMA_PRESSAO = [(0, 2, 79), (2, 1, 82), (3, 1, 86),
                (4, 3, 86), (7, 1, 84),
                (8, 2, 82), (10, 1, 81), (11, 1, 79),
                (12, 2, 81), (14, 1, 85), (15, 1, 88),
                (16, 2, 86), (18, 1, 82), (19, 1, 79),
                (20, 2, 81), (22, 1, 77), (23, 1, 74),
                (24, 2, 77), (26, 1, 79), (27, 1, 82),
                (28, 4, 81),
                (32, 1, 86), (33, 1, 89), (34, 2, 91),
                (36, 2, 89), (38, 1, 86), (39, 1, 81),
                (40, 2, 87), (42, 1, 86), (43, 1, 82),
                (44, 3, 85), (47, 1, 88),
                (48, 2, 86), (50, 1, 82), (51, 1, 79),
                (52, 2, 82), (54, 1, 86), (55, 1, 89),
                (56, 6, 88), (62, 1, 85), (63, 1, 81)]
# o lamento da Ruptura
LAMENTO = [(0, 6, 81), (6, 2, 77), (8, 6, 82), (14, 2, 79), (16, 6, 79), (22, 2, 82), (24, 8, 85)]
# o Confronto: o tema grande (em ré menor; depois meio tom acima)
TEMA_CONFRONTO = [(0, 1, 77), (1, 1, 82), (2, 2, 86),
                  (4, 1, 84), (5, 1, 88), (6, 2, 91),
                  (8, 3, 89), (11, .5, 88), (11.5, .5, 86),
                  (12, 2, 86), (14, 1, 81), (15, 1, 86),
                  (16, 1, 89), (17, 1, 86), (18, 2, 82),
                  (20, 1, 84), (21, 1, 88), (22, 2, 91),
                  (24, 3, 93), (27, 1, 91),
                  (28, 2, 88), (30, 1, 85), (31, 1, 81)]


def tensao():
    m = Musica("tensao", 150, PROG_TENSAO, ACORDES_TENSAO, SECOES_TENSAO, laco=8, semente=150080)
    assert m.compassos == 80
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT
    QUEBRADO = [(0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)]          # 3+3+2, duas vezes

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        if sec == "Retorno":
            raiz = 38 + local                                                # o baixo sobe meio tom por compasso
        pc = power(raiz + 12 if raiz < 40 else raiz)

        # ------------------------------------------------ o relógio: cordas em spiccato
        relogio = [notas[0] + 12, notas[0] + 24, notas[1] + 12, notas[0] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[0] + 24]
        if sec == "Intro":
            for k in range(16):
                acento = 1.0 if k in (0, 3, 6, 8, 11, 14) else 0.55
                m.poe(m.base, pan(cordas(notas[0] + 12 if k % 2 == 0 else notas[0] + 24, S16 * 0.8, acento * (0.35 + 0.65 * local / 7)), 0.25), t0 + k * S16)
        elif sec in ("Perigo", "Confronto", "Retorno"):
            for k in range(16):
                m.poe(m.base, pan(cordas(relogio[k % 8], S16 * 0.8, 0.75 + 0.25 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)
        elif sec == "Pressão":
            for k in range(8):
                m.poe(m.base, pan(cordas(relogio[k], BEAT * 0.4, 0.8), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
        elif sec == "Ruptura":
            for k in range(16):
                m.poe(m.pulso_eco, pan(cordas(notas[0] + 24 if k % 2 == 0 else notas[2] + 12, S16 * 0.6, 0.55), 0.35 * (1 if k % 2 else -1)), t0 + k * S16)

        # ------------------------------------------------ pad e coro
        if sec == "Intro":
            m.poe(m.base_sala, pad(notas, BAR, 0.5 + 0.5 * local / 7, 1100 + 250 * local), t0)
            if local >= 4:
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.5 + 0.12 * (local - 4)), t0)
        elif sec == "Pressão":
            m.poe(m.base_sala, pad(notas, BAR, 0.7, 2200), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.75), t0)
        elif sec == "Ruptura":
            m.poe(m.base_sala, pad(notas, BAR, 0.9, 1500), t0)
        elif sec == "Confronto":
            m.poe(m.base_sala, pad(notas, BAR, 0.5, 3000), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.7 if local < 8 else 0.9), t0)
        else:
            m.poe(m.base_sala, pad(notas, BAR, 0.45, 2600), t0)

        # ------------------------------------------------ baixo
        if sec == "Intro":
            if local % 2 == 0:
                m.poe(m.base, timpano(raiz, 1.0), t0)
            if local >= 4:
                for p, d in QUEBRADO:
                    m.poe(m.base, baixo(raiz, S16 * d * 0.85, 0.55 + 0.1 * (local - 4)), t0 + p * S16)
        elif sec == "Perigo":
            for p, d in QUEBRADO:
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 1.05 if p in (0, 8) else 0.9), t0 + p * S16)
            if local % 4 == 3:                                               # a "puxada" cromática no fim da frase
                m.poe(m.base, baixo(raiz + 1, S16 * 1.8, 1.0), t0 + 14 * S16)
        elif sec == "Pressão":
            for p, d, o in ((0, 6, 0), (6, 4, 0), (10, 2, 12), (12, 4, 0)):
                m.poe(m.base, baixo(raiz + o, S16 * d * 0.9, 1.0), t0 + p * S16)
        elif sec == "Ruptura":
            m.poe(m.base, baixo(raiz, BAR * 0.95, 0.7), t0)
            m.poe(m.base, timpano(raiz, 0.9), t0)
        elif sec == "Confronto":
            if local < 8:
                for k in range(8):
                    m.poe(m.base, baixo(raiz + (12 if k in (3, 7) else 0), BEAT * 0.42, 1.0 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)
            else:
                for beat in range(4):                                        # galope
                    for p, d in ((0, 2), (2, 1), (3, 1)):
                        m.poe(m.base, baixo(raiz, S16 * d * 0.85, 1.0), t0 + (beat * 4 + p) * S16)
        elif sec == "Retorno":
            for k in range(8):
                m.poe(m.base, baixo(raiz, BEAT * 0.42, 1.0 + 0.04 * local), t0 + k * BEAT / 2)

        # ------------------------------------------------ guitarras (pulso)
        if sec == "Perigo":
            for p, d in QUEBRADO:
                aberto = p in (0, 8)
                m.poe(m.pulso, guitarra(pc, S16 * d * (0.95 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + p * S16)
                if not aberto:                                               # chug entre os acentos
                    m.poe(m.pulso, guitarra(pc, S16 * 0.6, 0.6, abafada=True), t0 + (p + 1) * S16)
            if local % 4 == 3:
                m.poe(m.pulso, guitarra(power(pc[0] + 1), S16 * 1.8, 1.0), t0 + 14 * S16)
        elif sec == "Pressão":
            if local < 8:
                m.poe(m.pulso, guitarra(pc, BAR * 0.95, 1.0), t0)
            else:
                m.poe(m.pulso, guitarra(pc, BEAT * 1.9, 1.0), t0)
                for k in range(4, 8):
                    m.poe(m.pulso, guitarra(pc, BEAT * 0.35, 0.85, abafada=True), t0 + k * BEAT / 2)
        elif sec == "Ruptura" and local >= 6:
            passo = BEAT / 2 if local == 6 else S16
            for k in range(int(BAR / passo)):
                m.poe(m.pulso, guitarra(pc, passo * 0.6, 0.55 + 0.35 * k * passo / BAR, abafada=True), t0 + k * passo)
        elif sec == "Confronto":
            if local < 8:
                for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                    m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 1.0), t0 + pos * S16)
            else:
                for beat in range(4):
                    for p, d in ((0, 2), (2, 1), (3, 1)):
                        aberto = beat == 0 and p == 0
                        m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + (beat * 4 + p) * S16)
        elif sec == "Retorno":
            m.poe(m.pulso, guitarra(pc, BEAT * 0.9, 1.0), t0)
            for k in range(2, 8):
                m.poe(m.pulso, guitarra(pc, BEAT * 0.35, 0.8 + 0.03 * local, abafada=True), t0 + k * BEAT / 2)

        # ------------------------------------------------ bateria
        if sec == "Intro":
            m.bat(range(0, 16, 2), m.CHIMBAL, m.pulso, t0, 0.5 + 0.5 * local / 7)       # o tique-taque
            if local >= 4:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO, m.base, t0)
            if local == 3:
                m.virada_de_tons(t0, [50, 50, 45, 45], 0.8)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2), t0)
        elif sec == "Perigo":
            m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA, m.base_sala, t0)
            m.bat(range(0, 16, 2), m.CHIMBAL_F, m.pulso, t0)
            m.bat(range(1, 16, 2), m.CHIMBAL, m.pulso, t0)
            if local in (0, 8):
                m.poe(m.pulso, m.PRATO, t0)
                if local == 0:
                    m.poe(m.base, m.IMPACTO, t0)
            if local == 15:
                m.virada_de_tons(t0, [55, 52, 50, 48, 45, 43, 41, 40])
        elif sec == "Pressão":
            m.bat([0, 3, 10], m.BUMBO_F, m.base, t0)
            m.bat([8], m.CAIXA_F, m.base_sala, t0)                           # meio-tempo: a caixa no 3
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.1)
            if local in (7, 15):
                m.virada_de_tons(t0, [57, 55, 52, 50, 48, 45, 43, 41])
        elif sec == "Ruptura":
            if local in (0, 4):
                m.poe(m.base, m.IMPACTO, t0, 0.8 if local else 1.0)
                m.poe(m.pulso, m.PRATO, t0, 0.6)
            m.bat([0, 8], m.CHIMBAL, m.pulso, t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.25), t0)
        elif sec == "Confronto":
            if local < 8:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
            else:
                m.bat(range(16), m.BUMBO, m.base, t0)                       # bumbo duplo
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8, 16):
                m.poe(m.base, m.IMPACTO, t0, 1.1)
            if local == 7:                                                   # a subida de meio tom
                m.poe(m.base, riser(BAR, 1.2), t0)
                m.virada_de_tons(t0, [57, 55, 52, 50, 48, 45, 43, 42])
            if local == 23:
                m.virada_de_tons(t0, [52, 50, 48, 45, 43, 41, 40, 38])
        elif sec == "Retorno":
            m.bat(range(0, 16, 2), m.BUMBO_F, m.base, t0)
            m.bat([4, 12] if local < 4 else range(0, 16, 2), m.CAIXA if local < 4 else m.CAIXA_FANTASMA, m.base_sala, t0)
            m.bat(range(0, 16, 2), m.CHIMBAL_F, m.pulso, t0)
            if local == 0:
                m.poe(m.pulso, m.PRATO, t0)
                m.poe(m.base, m.IMPACTO, t0, 0.9)
            if local == 4:
                m.poe(m.base, riser(BAR * 4, 1.3), t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.25), t0)

        # ------------------------------------------------ tema
        if sec == "Perigo" and local == 0:
            m.frase(m.tema_eco, TEMA_PERIGO, t0, forte=0.95, voz="metal")
            m.frase(m.tema_eco, TEMA_PERIGO, t0, forte=0.35, brilho=3200)
        if sec == "Perigo" and local == 8:
            m.frase(m.tema_eco, TEMA_PERIGO, t0, forte=1.0, brilho=4600, dobra=-12)
        if sec == "Pressão" and local == 0:
            m.frase(m.tema_eco, TEMA_PRESSAO, t0, forte=1.0, brilho=4400, dobra=-12)
        if sec == "Ruptura" and local == 0:
            m.frase(m.tema_eco, LAMENTO, t0, forte=0.75, brilho=2800)
        if sec == "Confronto" and local == 0:
            m.frase(m.tema_eco, TEMA_CONFRONTO, t0, forte=1.1, brilho=6000, dobra=-12)
        if sec == "Confronto" and local == 8:
            m.frase(m.tema_eco, TEMA_CONFRONTO, t0, transp=1, forte=1.1, brilho=6200, voz="ambos")
        if sec == "Confronto" and local == 16:
            m.frase(m.tema_eco, TEMA_CONFRONTO, t0, transp=1, forte=1.15, brilho=6500, dobra=-12, voz="ambos")
            m.frase(m.tema_eco, TEMA_CONFRONTO, t0, transp=1 - 5, forte=0.4, brilho=4000)
        if sec == "Retorno":
            # a sirene: uma nota longa que sobe meio tom por compasso
            m.poe(m.tema_eco, supersaw(74 + local, BAR * 0.95, 0.5 + 0.06 * local, 2400 + 500 * local, False), t0)
            m.poe(m.tema, metal(62 + local, BAR * 0.9, 0.5 + 0.05 * local), t0)

    m.renderiza("anime arcade · tensão (v5)")


# ================================================================== CHEFE (luta 10)
ACORDES_CHEFE = {
    "Cm": (36, [48, 51, 55]), "Ab": (44, [56, 60, 63]), "Db": (37, [49, 53, 56]), "G": (43, [55, 59, 62]),
    "Fm": (41, [53, 56, 60]), "Bb": (34, [46, 50, 53]),
    # o refrão final um tom acima (ré menor)
    "Dm": (38, [50, 53, 57]), "C": (36, [48, 52, 55]), "A": (45, [57, 61, 64]),
}
PROG_CHEFE = (["Cm"] * 4 + ["Db", "Db", "G", "G"]                                          # Aparição 0–7
              + ["Cm", "Ab", "Db", "G"] * 2 + ["Fm", "Cm", "Db", "G"] * 2                    # Duelo 8–23
              + ["Cm", "Bb", "Ab", "G"] * 2 + ["Fm", "Ab", "Db", "G", "Fm", "Ab", "G", "G"]  # Fúria 24–39
              + ["Ab", "Fm", "Cm", "G", "Ab", "Fm", "Db", "G"]                               # Desespero 40–47
              + ["Ab", "Bb", "Cm", "Cm", "Ab", "Bb", "G", "G"]                               # Último golpe: hino 48–55
              + ["Dm", "C", "Bb", "A"] * 4                                                   # refrão um tom acima 56–71
              + ["Cm", "Db", "Cm", "Db", "Cm", "Db", "G", "G"])                              # Virada 72–79
SECOES_CHEFE = [("Aparição", 0), ("Duelo", 8), ("Fúria", 24), ("Desespero", 40), ("Último golpe", 48), ("Virada", 72)]

# o tema do chefe: arpejo que sobe, o ré bemol (frígio) e o si natural sustentado
TEMA_CHEFE = [(0, 1, 72), (1, 1, 75), (2, 1, 79), (3, 1, 84),
              (4, 2, 84), (6, 1, 82), (7, 1, 80),
              (8, 1.5, 80), (9.5, .5, 77), (10, 1, 80), (11, 1, 85),
              (12, 3, 83), (15, 1, 79),
              (16, 1, 84), (17, 1, 87), (18, 2, 91),
              (20, 1.5, 92), (21.5, .5, 91), (22, 1, 87), (23, 1, 84),
              (24, 2, 89), (26, 1, 85), (27, 1, 89),
              (28, 2, 86), (30, 1, 83), (31, 1, 79),
              (32, 1.5, 80), (33.5, .5, 84), (34, 2, 89),
              (36, 1.5, 87), (37.5, .5, 86), (38, 2, 84),
              (40, 1, 85), (41, 1, 89), (42, 1, 92), (43, 1, 89),
              (44, 3, 86), (47, 1, 83),
              (48, 1, 84), (49, 1, 89), (50, 2, 92),
              (52, 1, 91), (53, 1, 87), (54, 2, 84),
              (56, 2, 85), (58, 1, 89), (59, 1, 92),
              (60, 3, 91), (63, 1, 86)]
LAMENTO_CHEFE = [(0, 3, 84), (3, 1, 80), (4, 3, 80), (7, 1, 84), (8, 2, 87), (10, 2, 86), (12, 4, 83),
                 (16, 3, 84), (19, 1, 87), (20, 3, 89), (23, 1, 87), (24, 2, 85), (26, 2, 89), (28, 4, 91)]
HINO_CHEFE = [(0, 2, 84), (2, 1, 80), (3, 1, 84),
              (4, 2, 86), (6, 1, 82), (7, 1, 86),
              (8, 3, 87), (11, .5, 86), (11.5, .5, 84),
              (12, 1, 87), (13, 3, 91),
              (16, 2, 92), (18, 1, 91), (19, 1, 87),
              (20, 2, 89), (22, 1, 86), (23, 1, 89),
              (24, 3, 91), (27, 1, 86),
              (28, 2, 91), (30, 2, 93)]
# o refrão final em ré menor sobre a cadência andaluza (ré, dó, si bemol, lá)
REFRAO_CHEFE = [(0, 1, 74), (1, 1, 77), (2, 2, 81),
                (4, 2, 79), (6, 1, 76), (7, 1, 79),
                (8, 3, 77), (11, 1, 74),
                (12, 2, 73), (14, 1, 76), (15, 1, 81),
                (16, 1, 86), (17, 1, 84), (18, 2, 81),
                (20, 1, 84), (21, 1, 81), (22, 2, 79),
                (24, 2, 77), (26, 1, 81), (27, 1, 82),
                (28, 3, 85), (31, 1, 81)]


def corrida(notas):
    """Arpejo rápido em semicolcheias sobre o acorde (sobe, desce, sobe), sem passar do si 6."""
    escada = sorted({n + 24 for n in notas} | {n + 36 for n in notas})
    while max(escada) > 93:
        escada = [n - 12 for n in escada]
    return [escada[i] for i in (0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5)]


def chefe():
    m = Musica("chefe", 168, PROG_CHEFE, ACORDES_CHEFE, SECOES_CHEFE, laco=8, semente=168080)
    assert m.compassos == 80
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT
    GALOPE = ((0, 2), (2, 1), (3, 1))

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        refrao = sec == "Último golpe" and local >= 8

        # ------------------------------------------------ cordas correndo (base)
        if sec == "Aparição" and local >= 2:
            for k in range(16):
                m.poe(m.base, pan(cordas(notas[0] + (12 if k % 2 == 0 else 24), S16 * 0.8, 0.3 + 0.6 * (local - 2) / 5), 0.25 * (1 if k % 2 else -1)), t0 + k * S16)
        elif sec in ("Duelo", "Fúria") or refrao or sec == "Virada":
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[2] + 12]
            for k in range(16):
                m.poe(m.base, pan(cordas(seq[k % 8], S16 * 0.8, 0.85 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)

        # ------------------------------------------------ pad e coro
        if sec == "Aparição":
            m.poe(m.base_sala, pad(notas, BAR, 0.6 + 0.4 * local / 7, 1200 + 200 * local), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.55 + 0.06 * local), t0)
        elif sec == "Desespero":
            m.poe(m.base_sala, pad(notas, BAR, 0.9, 2000), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.95), t0)
        elif sec == "Último golpe":
            m.poe(m.base_sala, pad(notas, BAR, 0.55, 3200), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0] + 24], BAR, 0.9 if local < 8 else 1.05), t0)
        else:
            m.poe(m.base_sala, pad(notas, BAR, 0.45, 2800), t0)
            if sec == "Duelo":
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.5), t0)

        # ------------------------------------------------ sinos e tambores da Aparição
        if sec == "Aparição":
            if local < 6:
                m.poe(m.base_sala, pan(sino_grande(48 if local < 4 else 49, 0.9), -0.15), t0)
                m.poe(m.base_sala, pan(sino_grande(60 if local < 4 else 61, 0.5), 0.2), t0 + BEAT * 2)
            if local in (0, 2):
                m.poe(m.base, m.IMPACTO, t0, 1.0)
                m.poe(m.base, timpano(36, 1.2), t0)
            if local >= 4:
                for k in range(8 if local < 6 else 16):
                    passo = BEAT / 2 if local < 6 else S16
                    m.poe(m.base, taiko(0.5 + 0.08 * (local - 4) + 0.3 * (k % 4 == 0)), t0 + k * passo)
            if local in (4, 6):
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.6, 1.2), t0)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.0), t0 + BEAT * 2.5)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.2, 1.1), t0 + BEAT * 3)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2, 1.2), t0)
                m.poe(m.pulso, guitarra(pc, BAR * 1.9, 0.9), t0)

        # ------------------------------------------------ baixo
        if sec in ("Duelo",) or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    m.poe(m.base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 1.0), t0 + (beat * 4 + p) * S16)
        elif sec == "Fúria":
            for k in range(16):
                m.poe(m.base, baixo(raiz, S16 * 0.8, 1.05 if k % 4 == 0 else 0.85), t0 + k * S16)
        elif sec == "Desespero":
            for p, d in ((0, 6), (6, 4), (10, 6)):
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 0.9), t0 + p * S16)
        elif sec == "Último golpe":
            for k in range(8):
                m.poe(m.base, baixo(raiz + (12 if k in (3, 7) else 0), BEAT * 0.42, 1.0 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)
        elif sec == "Virada":
            if local < 6:
                for pos, d in ((0, 2), (3, 1), (4, 2), (6, 2), (8, 3), (11, 1), (12, 2), (14, 2)):
                    m.poe(m.base, baixo(raiz, S16 * d * 0.9, 1.05), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.base, baixo(raiz, passo * 0.8, 0.85 + 0.1 * (local - 6)), t0 + k * passo)

        # ------------------------------------------------ guitarras (pulso)
        if sec == "Duelo" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    aberto = beat == 0 and p == 0
                    m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + (beat * 4 + p) * S16)
        elif sec == "Fúria":
            for k in range(16):                                              # palheta alternada em semicolcheias
                aberto = k in (0, 8)
                m.poe(m.pulso, guitarra(pc, S16 * (3.5 if aberto else 0.7), 1.0 if aberto else 0.8, abafada=not aberto), t0 + k * S16)
        elif sec == "Desespero" and local >= 6:
            m.poe(m.pulso, guitarra(pc, BAR * 0.95, 0.6 + 0.3 * (local - 6)), t0)
        elif sec == "Último golpe":
            for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 1.0), t0 + pos * S16)
        elif sec == "Virada":
            if local < 6:
                for pos, d in ((0, 2), (3, 1), (4, 2), (6, 2), (8, 3), (11, 1), (12, 2), (14, 2)):
                    m.poe(m.pulso, guitarra(pc, d * S16 * 0.85, 1.05, abafada=d < 2), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.pulso, guitarra(pc, passo * 0.5, 0.75 + 0.15 * (local - 6), abafada=True), t0 + k * passo)
                if local == 7:
                    m.poe(m.pulso, guitarra(pc, BAR * 0.45, 1.0), t0 + BAR * 0.5)

        # ------------------------------------------------ bateria
        if sec == "Duelo":
            m.bat([0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.1)
            if local in (7, 15):
                m.virada_de_tons(t0, [55, 52, 50, 48, 45, 43, 41, 40])
        elif sec == "Fúria":
            if local < 8:                                                    # a fúria: bumbo em semicolcheias, caixa em colcheias
                m.bat(range(16), m.BUMBO, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat([2, 6, 10, 14], m.CAIXA, m.base, t0, 0.55)
            else:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8):
                m.poe(m.base, m.IMPACTO, t0, 1.0)
            if local == 15:
                m.virada_de_tons(t0, [57, 55, 52, 50, 48, 45, 43, 41])
        elif sec == "Desespero":
            m.bat([0, 10], m.BUMBO, m.base, t0)
            m.bat([8], m.CAIXA, m.base_sala, t0)
            m.bat(range(0, 16, 4), m.CHIMBAL, m.pulso, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 0.8)
                m.poe(m.pulso, m.PRATO, t0, 0.7)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
        elif sec == "Último golpe":
            if local < 8:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
            else:
                m.bat(range(16), m.BUMBO, m.base, t0)                       # bumbo duplo no refrão
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO if local >= 8 else m.CHIMBAL_ABERTO, t0 + k * S16)
            if local % (2 if local >= 8 else 4) == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8, 16):
                m.poe(m.base, m.IMPACTO, t0, 1.2)
                m.poe(m.base, timpano(raiz, 1.0), t0)
            if local == 7:                                                   # a subida para ré menor
                m.poe(m.base, riser(BAR, 1.3), t0)
                m.virada_de_tons(t0, [57, 55, 52, 50, 48, 45, 43, 42])
            if local == 23:
                m.virada_de_tons(t0, [57, 55, 53, 50, 48, 45, 43, 41])
        elif sec == "Virada":
            if local < 6:
                m.bat([0, 3, 4, 6, 8, 11, 12, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat(range(0, 16, 2), m.CHIMBAL_F, m.pulso, t0)
                if local in (0, 4):
                    m.poe(m.pulso, m.PRATO, t0)
                    m.poe(m.base, m.IMPACTO, t0, 0.9)
            else:
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                if local == 6:
                    m.poe(m.base, m.rufo(2, 0.2), t0)
            if local == 4:
                m.poe(m.base, riser(BAR * 4, 1.3), t0)

        # ------------------------------------------------ tema
        if sec == "Duelo" and local == 0:
            m.frase(m.tema_eco, TEMA_CHEFE, t0, forte=1.05, brilho=5600, voz="ambos")
        if sec == "Fúria":
            if local < 8:
                for k, nota in enumerate(corrida(notas)):
                    m.poe(m.tema_eco, supersaw(nota, S16 * 0.9, 0.62 + 0.18 * (k % 4 == 0), 6200, False), t0 + k * S16)
            else:
                # metais em 3+3+2, e o supersaw responde descendo o acorde
                for pos, d in ((0, 2), (3, 2), (6, 2)):
                    m.poe(m.tema, metais([n + 12 for n in notas], S16 * d * 0.9, 1.15), t0 + pos * S16)
                topo = sorted(n + 24 for n in notas)
                for pos, d, nota in ((8, 2, topo[2]), (10, 2, topo[1]), (12, 4, topo[0] + (12 if topo[0] < 72 else 0))):
                    m.poe(m.tema_eco, supersaw(nota, S16 * d * 0.92, 0.95, 5600), t0 + pos * S16)
        if sec == "Desespero":
            if local == 0:
                m.frase(m.tema_eco, LAMENTO_CHEFE, t0, forte=0.85, brilho=3400)
            seq = [notas[0] + 24, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k, nota in enumerate(seq):
                m.poe(m.tema_eco, pan(v4.sino(nota, 0.8), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT)
        if sec == "Último golpe":
            if local == 0:
                m.frase(m.tema_eco, HINO_CHEFE, t0, forte=1.1, brilho=6000, dobra=-12)
                m.frase(m.tema, HINO_CHEFE, t0, transp=-12, forte=0.55, voz="metal")
            if local == 8:
                m.frase(m.tema_eco, REFRAO_CHEFE, t0, forte=1.1, brilho=6000, dobra=12, ganho_dobra=0.35)
                m.frase(m.tema, REFRAO_CHEFE, t0, transp=-12, forte=0.6, voz="metal")
            if local == 16:
                m.frase(m.tema_eco, REFRAO_CHEFE, t0, forte=1.2, brilho=6500, dobra=12, ganho_dobra=0.45)
                m.frase(m.tema, REFRAO_CHEFE, t0, transp=-12, forte=0.7, voz="metal")
                m.frase(m.tema_eco, REFRAO_CHEFE, t0, transp=-5, forte=0.35, brilho=4000)
        if sec == "Virada":
            if local < 6 and local % 2 == 0:
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.9, 1.2), t0)
                m.poe(m.tema, metais([n + 12 for n in m.acorde(b + 1)[1]], BEAT * 0.9, 1.2), t0 + BEAT * 1.5)
            if local == 2:
                m.frase(m.tema_eco, [(0, 1, 72), (1, 1, 73), (2, 2, 72), (4, 1, 75), (5, 1, 73), (6, 2, 72),
                                     (8, 1, 72), (9, 1, 73), (10, 2, 75), (12, 1, 79), (13, 1, 77), (14, 2, 73)], t0, forte=0.95)
            if local >= 6:
                m.poe(m.tema_eco, supersaw(79 + 2 * (local - 6), BAR * 0.95, 0.6 + 0.15 * (local - 6), 2600 + 1500 * (local - 6), False), t0)

    m.renderiza("anime arcade · chefe (v5)")


if __name__ == "__main__":
    qual = sys.argv[1:] or ["tensao", "chefe"]
    if "tensao" in qual:
        tensao()
    if "chefe" in qual:
        chefe()
