#!/usr/bin/env python3
"""
Música v8: as faixas do Caminho do Nexus (src/engine/campanha.ts).

Pedido do jogador: "músicas novas pra cada região e uma música nova pra cada chefe, todas muito boas".

São 16 faixas: uma por região (as lutas contra os 4 rivais dela) e uma por chefe. O mesmo som e as mesmas três
camadas das faixas de batalha (v4–v7: base, pulso e tema, que sobem quando a luta esquenta), cada região com um
jeito próprio — tom, escala, andamento, bateria, baixo, acompanhamento e o instrumento do tema — e cada chefe com a
versão pesada da região: mais rápido, tom menor e escuro, sinos de torre, tímpanos, coro, metais e o último refrão
meio tom acima.

  vila      dó maior, 138 BPM, marcha saltitante, sininhos e caixinha
  floresta  ré dórico, 120 BPM, tambores tribais, cordas em pizzicato e coro
  neon      lá menor, 128 BPM, synthwave: bumbo reto, baixo pulsando e arpejos
  deserto   mi frígio dominante, 112 BPM, taikos no maqsum e metais com o tema árabe
  templo    ré menor (hirajoshi), 108 BPM, meio-tempo, sinos, taikos grandes e coro
  vulcao    mi frígio, 172 BPM, metal: bumbo duplo, guitarras abafadas e metais
  ceu       fá lídio, 150 BPM, épico: galope, coro inteiro, sinos e cordas correndo
  trono     si menor harmônica, 166 BPM, orquestral sombrio: coro, órgão, taikos e metais

Cada faixa: Chegada (8) · Tema (16) · Ponte (16) · Respiro (8) · Refrão (16) = 64 compassos; o laço volta para o Tema.
O tema é composto a partir de um motivo próprio de cada faixa (ritmo e contorno), sempre em notas do acorde nos tempos
fortes e passando pela escala nos fracos, em frase de pergunta e resposta.

Uso:  python3 tools/audio/generate_music_v8.py [vila floresta … | chefe-vila … | regioes | chefes]
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_music_v4 as v4  # noqa: E402
from generate_music_v3 import pan  # noqa: E402
from generate_music_v4 import baixo, faisca, guitarra, pad, power, riser, supersaw, tom  # noqa: E402
from generate_music_v5 import Musica, coro, cordas, metais, sino_grande, taiko, timpano  # noqa: E402

ESCALAS = {
    "maior": [0, 2, 4, 5, 7, 9, 11], "lidio": [0, 2, 4, 6, 7, 9, 11], "dorico": [0, 2, 3, 5, 7, 9, 10],
    "menor": [0, 2, 3, 5, 7, 8, 10], "harmonica": [0, 2, 3, 5, 7, 8, 11], "frigio": [0, 1, 3, 5, 7, 8, 10],
    "hijaz": [0, 1, 4, 5, 7, 8, 10], "hirajoshi": [0, 2, 3, 7, 8, 10, 12],
}
QUALIDADE = {"M": (0, 4, 7), "m": (0, 3, 7), "d": (0, 3, 6), "s": (0, 5, 7), "5": (0, 7, 12)}
SECOES = [("Chegada", 0), ("Tema", 8), ("Ponte", 24), ("Respiro", 40), ("Refrão", 48)]

# os motivos (ritmo de 2 compassos, em tempos) e os contornos (graus relativos: sobe, desce, arco…)
MOTIVOS = {
    "saltitante": [(0, .5), (.5, .5), (1, 1), (2, .5), (2.5, .5), (3, 1), (4, 1), (5, .5), (5.5, .5), (6, 2)],
    "heroico": [(0, 1), (1, .5), (1.5, .5), (2, 2), (4, 1.5), (5.5, .5), (6, 2)],
    "galope": [(0, .75), (.75, .25), (1, 1), (2, .75), (2.75, .25), (3, 1), (4, 1), (5, 1), (6, 2)],
    "longo": [(0, 2), (2, 1), (3, 1), (4, 3), (7, 1)],
    "sincopado": [(0, .75), (.75, .75), (1.5, .5), (2, 1), (3, .5), (3.5, .5), (4, .75), (4.75, .75), (5.5, .5), (6, 2)],
    "ornado": [(0, 1), (1, .25), (1.25, .25), (1.5, .5), (2, 1.5), (3.5, .5), (4, .5), (4.5, .5), (5, 1), (6, 2)],
}


class Receita:
    def __init__(self, nome, bpm, tonica, escala, prog, motivo, contorno, bateria, baixo_, acomp, voz, extras=(), brilho=5600, chefe=False, semente=1):
        self.nome, self.bpm, self.tonica, self.escala = nome, bpm, tonica, ESCALAS[escala]
        self.prog, self.motivo, self.contorno = prog, MOTIVOS[motivo], contorno
        self.bateria, self.baixo, self.acomp, self.voz, self.extras = bateria, baixo_, acomp, voz, set(extras)
        self.brilho, self.chefe, self.semente = brilho, chefe, semente


def acordes_de(r):
    """Os acordes da faixa a partir dos nomes "semitons+qualidade" (ex.: "0m", "8M", "7M")."""
    out = {}
    for sec, lista in r.prog.items():
        for nome in lista:
            if nome in out:
                continue
            off, q = int(nome[:-1]), nome[-1]
            raiz = r.tonica + off
            baixo_ = 36 + (raiz - 36) % 12
            notas = [52 + (raiz + i - 52) % 12 for i in QUALIDADE[q]]
            out[nome] = (baixo_, sorted(notas))
            raiz_s = raiz + 1                                                   # o refrão final do chefe: meio tom acima
            out[f"{nome}^1"] = (36 + (raiz_s - 36) % 12, sorted(52 + (raiz_s + i - 52) % 12 for i in QUALIDADE[q]))
    return out


def progressao(r):
    """64 compassos: cada seção repete a sua sequência; o último refrão do chefe sobe meio tom."""
    p = []
    for sec, ini in SECOES:
        tam = {"Chegada": 8, "Tema": 16, "Ponte": 16, "Respiro": 8, "Refrão": 16}[sec]
        lista = r.prog[sec]
        for k in range(tam):
            nome = lista[k % len(lista)]
            p.append(f"{nome}^1" if r.chefe and sec == "Refrão" and k >= 8 else nome)
    return p


# ------------------------------------------------------------------ o tema
def compoe(r, m, rng, alto=0):
    """Uma frase de 4 compassos (pergunta e resposta) para cada par de acordes; devolve [(compasso, ini, dur, nota)]."""
    escala = sorted({(r.tonica + i) % 12 for i in r.escala})

    def na_escala(n):
        return n % 12 in escala

    def perto(alvo, candidatas):
        return min(candidatas, key=lambda c: (abs(c - alvo), c))

    def tons_do_acorde(b):
        _, notas = m.acorde(b)
        pcs = {n % 12 for n in notas}
        return [n for n in range(64 + alto, 96 + alto) if n % 12 in pcs]

    def escala_entre(a, b):
        return [n for n in range(min(a, b), max(a, b) + 1) if na_escala(n)]

    def frase(b0, transp_contorno=0):
        notas = []
        prev = 74 + alto + transp_contorno
        for meio in range(2):                                                    # pergunta (2 compassos) e resposta
            ritmo = r.motivo
            for i, (ini, dur) in enumerate(ritmo):
                b = b0 + meio * 2 + int(ini // 4)
                forte = abs(ini - round(ini)) < 1e-6 and int(ini) % 2 == 0
                passo = r.contorno[i % len(r.contorno)] * (1 if meio == 0 else -1 if i > len(ritmo) // 2 else 1)
                alvo = prev + passo * 2
                if i == len(ritmo) - 1 and meio == 1:                            # a resposta termina na raiz
                    raiz = m.acorde(b)[1][0] % 12
                    n = perto(prev, [x for x in range(64 + alto, 96 + alto) if x % 12 == raiz])
                elif forte or dur >= 1.5:
                    n = perto(alvo, tons_do_acorde(b))
                else:
                    cands = [x for x in escala_entre(prev - 4, prev + 4) if x != prev] or [prev]
                    n = perto(alvo, cands)
                n = min(max(n, 66 + alto), 93 + alto)
                notas.append((b0 + meio * 2, ini + 0.0, dur, n))
                prev = n
        return notas

    return frase


# ------------------------------------------------------------------ a faixa
def faz(r):
    prog = progressao(r)
    acordes = acordes_de(r)
    m = Musica(r.nome, r.bpm, prog, acordes, SECOES, laco=8, semente=r.semente)
    assert m.compassos == 64
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT
    rng = np.random.default_rng(r.semente)
    frase = compoe(r, m, rng)
    # o tema de cada seção: composto uma vez (motivo) e repetido com variação
    temas = {}
    for sec, ini in SECOES:
        if sec in ("Tema", "Refrão"):
            a = frase(ini)
            b = frase(ini + 4, 3)
            temas[sec] = a + b
    ponte = compoe(r, m, rng, alto=-5)(24, -2) + compoe(r, m, rng, alto=-5)(28, 2)

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        cheio = sec in ("Tema", "Ponte", "Refrão")
        refrao = sec == "Refrão"

        # ------------------------------------------------ chegada: sinos, tímpanos e o crescendo
        if sec == "Chegada":
            m.poe(m.base_sala, pad(notas, BAR, 0.5 + 0.06 * local, 900 + 260 * local), t0)
            if r.chefe or "sinos" in r.extras:
                if local in (0, 4):
                    m.poe(m.base_sala, pan(sino_grande(raiz + 12, 0.85 if r.chefe else 0.5), -0.15), t0)
            if r.chefe:
                if local in (0, 2, 4, 6):
                    m.poe(m.base, timpano(raiz, 1.1), t0)
                    m.poe(m.base, m.IMPACTO, t0, 0.9)
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.45 + 0.08 * local), t0)
                if local in (3, 5):
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.5, 1.2), t0)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.2, 1.1), t0 + BEAT * 2.5)
            if "caixinha" in r.extras or r.acomp == "arpejo":
                seq = [notas[0] + 24, notas[1] + 24, notas[2] + 24, notas[1] + 36]
                for k in range(8):
                    m.poe(m.tema_eco, pan(v4.sino(seq[k % 4], 0.45 + 0.04 * local), 0.35 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
            if local >= 4:
                for k in range(4 if local < 6 else 8):
                    m.poe(m.base, taiko(0.4 + 0.08 * (local - 4)), t0 + k * BAR / (4 if local < 6 else 8))
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2, 1.2), t0)
            if local == 7:
                m.poe(m.pulso, guitarra(pc, BAR * 0.9, 0.8), t0)
            continue

        # ------------------------------------------------ pad e coro
        if sec == "Respiro":
            m.poe(m.base_sala, pad(notas, BAR, 0.9, 2000), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.9 if r.chefe else 0.7), t0)
        else:
            m.poe(m.base_sala, pad(notas, BAR, 0.45 if not refrao else 0.55, 2600 if not refrao else 3400), t0)
            if refrao and (r.chefe or "coro" in r.extras):
                m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0] + 24], BAR, 0.95 if r.chefe else 0.7), t0)
            elif sec == "Ponte" and "coro" in r.extras:
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.45), t0)

        # ------------------------------------------------ baixo
        meio_tempo = sec == "Respiro"
        if meio_tempo:
            for p, d in ((0, 6), (6, 4), (10, 6)):
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 0.9), t0 + p * S16)
        elif r.baixo == "saltitante":
            for k in range(8):
                nota = raiz + (7 if k % 2 else 0) + (12 if k in (3, 7) else 0)
                m.poe(m.base, baixo(nota, BEAT * 0.4, 1.0 if k % 2 == 0 else 0.85), t0 + k * BEAT / 2)
        elif r.baixo == "pulsante":
            for k in range(8):
                m.poe(m.base, baixo(raiz + (12 if k % 2 else 0), BEAT * 0.42, 1.0), t0 + k * BEAT / 2)
        elif r.baixo == "galope":
            for beat in range(4):
                for p, d in ((0, 2), (2, 1), (3, 1)):
                    m.poe(m.base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 1.0), t0 + (beat * 4 + p) * S16)
        elif r.baixo == "metal":
            for k in range(16):
                m.poe(m.base, baixo(raiz, S16 * 0.8, 1.08 if k % 4 == 0 else 0.86), t0 + k * S16)
        elif r.baixo == "drone":
            m.poe(m.base, baixo(raiz, BAR * 0.95, 0.8), t0)
            for p in (6, 10, 14):
                m.poe(m.base, baixo(raiz + (12 if p == 10 else 0), S16 * 1.6, 0.9), t0 + p * S16)
        else:  # tribal: síncope
            for p, d in ((0, 3), (3, 3), (6, 2), (10, 2), (12, 4)):
                m.poe(m.base, baixo(raiz + (12 if p == 12 else 0), S16 * d * 0.85, 1.0), t0 + p * S16)

        # ------------------------------------------------ acompanhamento (pulso)
        if meio_tempo:
            if local >= 6:
                m.poe(m.pulso, guitarra(pc, BAR * 0.95, 0.6 + 0.3 * (local - 6)), t0)
        elif r.acomp == "arpejo":
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[2] + 24, notas[1] + 24]
            for k in range(16):
                m.poe(m.pulso_eco, pan(faisca(seq[k % 8], 0.55 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)
            if refrao or r.chefe:
                for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                    m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 0.75), t0 + pos * S16)
        elif r.acomp == "pizzicato":
            seq = [notas[0] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k in range(8):
                m.poe(m.pulso, pan(cordas(seq[k % 4], S16 * 1.2, 0.9 + 0.15 * (k % 2 == 0)), 0.25 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
            if refrao or r.chefe:
                for pos, dur in ((0, 6), (6, 4), (10, 6)):
                    m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 0.7), t0 + pos * S16)
        elif r.acomp == "metal":
            for k in range(16):
                aberto = k in (0, 3, 6, 8, 11, 14)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), 1.05 if aberto else 0.8, abafada=not aberto), t0 + k * S16)
        elif r.acomp == "galope":
            for beat in range(4):
                for p, d in ((0, 2), (2, 1), (3, 1)):
                    aberto = beat == 0 and p == 0
                    m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + (beat * 4 + p) * S16)
        elif r.acomp == "marcha":
            for k in range(4):
                m.poe(m.pulso, guitarra(pc, BEAT * 0.35, 0.7, abafada=True), t0 + k * BEAT + BEAT / 2)
            for k in range(8):
                m.poe(m.pulso_eco, pan(faisca(notas[k % 3] + 24, 0.4), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
        else:  # cordas correndo (orquestral)
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[2] + 12]
            for k in range(16):
                m.poe(m.base, pan(cordas(seq[k % 8], S16 * 0.8, 0.85 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)
            if refrao or r.chefe:
                for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                    m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 0.95), t0 + pos * S16)

        # ------------------------------------------------ bateria
        if meio_tempo:
            m.bat([0, 10], m.BUMBO, m.base, t0)
            m.bat([8], m.CAIXA, m.base_sala, t0)
            m.bat(range(0, 16, 4), m.CHIMBAL, m.pulso, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 0.8)
                m.poe(m.pulso, m.PRATO, t0, 0.7)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
        else:
            bat = r.bateria
            if bat == "marcha":
                m.bat([0, 8] if not refrao else [0, 6, 8, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat(range(0, 16, 2), m.CHIMBAL_F if refrao else m.CHIMBAL, m.pulso, t0)
            elif bat == "quatro":
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(16):
                    m.poe(m.pulso, m.CHIMBAL_ABERTO if k % 4 == 2 else m.CHIMBAL, t0 + k * S16, 0.85 if k % 4 == 2 else 0.5)
            elif bat == "tribal":
                for p, f in ((0, 1.0), (3, 0.7), (6, 0.8), (8, 1.0), (10, 0.6), (11, 0.7), (14, 0.8)):
                    m.poe(m.base, taiko(0.7 * f), t0 + p * S16)
                m.bat([4, 12], m.CAIXA, m.base_sala, t0, 0.8)
                for k in range(16):
                    m.poe(m.pulso, m.CHIMBAL, t0 + k * S16, 0.55 if k % 2 == 0 else 0.3)
                if refrao:
                    m.bat([0, 8], m.BUMBO_F, m.base, t0)
            elif bat == "maqsum":
                for p, f, grave in ((0, 1.0, True), (3, 0.6, False), (6, 0.7, False), (8, 0.9, True), (12, 0.7, False)):
                    m.poe(m.base, taiko(f) if grave else tom(64, 0.6 * f), t0 + p * S16)
                m.bat([0, 8], m.BUMBO_F, m.base, t0)
                m.bat([4, 12] if refrao else [12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CHIMBAL, t0 + k * S16, 0.6)
            elif bat == "meio":
                m.bat([0, 7] if not refrao else [0, 3, 7, 10], m.BUMBO_F, m.base, t0)
                m.bat([8], m.CAIXA_F, m.base_sala, t0)
                m.poe(m.base, taiko(1.0), t0)
                m.poe(m.base, taiko(0.6), t0 + 10 * S16)
                m.bat(range(0, 16, 2), m.CHIMBAL, m.pulso, t0)
            elif bat == "metal":
                m.bat(range(16), m.BUMBO_F if refrao else m.BUMBO, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            else:  # galope
                m.bat([0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0, 0.9)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.1 if r.chefe else 0.9)
                if r.chefe:
                    m.poe(m.base, timpano(raiz, 1.0), t0)
            if local in (7, 15):
                m.virada_de_tons(t0, [59, 57, 55, 52, 50, 47, 45, 43])
                if refrao and r.chefe and local == 7:
                    m.poe(m.base, riser(BAR, 1.35), t0)
            if r.chefe and refrao and local % 2 == 0:
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.9, 1.15), t0)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.9, 1.1), t0 + BEAT * 1.5)

        # ------------------------------------------------ extras da região
        if "sinos" in r.extras and cheio and local % 2 == 0:
            m.poe(m.tema_eco, pan(v4.sino(notas[2] + 24, 0.5), 0.35), t0 + BEAT * 3)
        if "taikos" in r.extras and cheio and local % 4 == 3:
            for k in range(4):
                m.poe(m.base, taiko(0.6 + 0.12 * k), t0 + (12 + k) * S16)
        if "caixinha" in r.extras and sec == "Ponte":
            seq = [notas[0] + 36, notas[2] + 24, notas[1] + 36, notas[2] + 24]
            for k in range(4):
                m.poe(m.tema_eco, pan(v4.sino(seq[k], 0.35), 0.4 * (1 if k % 2 else -1)), t0 + k * BEAT)

        # ------------------------------------------------ o tema
        if sec in ("Tema", "Refrão") and local in (0, 8):
            frase_ = [(fb, ini, dur, n) for fb, ini, dur, n in temas[sec]]
            for fb, ini, dur, n in frase_:
                bb = fb + (local if local == 8 else 0)
                if refrao and r.chefe and local == 8:
                    n += 1
                em = m.t(bb) + ini * BEAT
                d = dur * BEAT * 0.94
                forte = 1.05 if refrao else 0.95
                if r.voz in ("saw", "ambos"):
                    m.poe(m.tema_eco, supersaw(n, d, forte, r.brilho), em)
                if r.voz in ("metal", "ambos") or (r.chefe and refrao):
                    m.poe(m.tema, metais([n - 12], d, forte * 0.9), em)
                if r.voz == "sino":
                    m.poe(m.tema_eco, pan(v4.sino(n, 0.95 * forte), 0.1), em)
                    m.poe(m.tema_eco, supersaw(n, d, 0.5 * forte, r.brilho * 0.7), em)
                if r.voz == "coro":
                    m.poe(m.tema, coro([n], d, 0.9 * forte), em)
                    m.poe(m.tema_eco, supersaw(n, d, 0.55 * forte, r.brilho * 0.8), em)
                if refrao:                                                       # o refrão dobra uma oitava acima
                    m.poe(m.tema_eco, supersaw(n + 12, d, 0.38 * forte, r.brilho * 0.8, False), em)
        if sec == "Ponte":
            if local in (0, 8):
                for fb, ini, dur, n in ponte:
                    bb = fb + (8 if local == 8 else 0)
                    em = m.t(bb) + ini * BEAT
                    d = dur * BEAT * 0.94
                    if r.voz == "sino" or "sinos" in r.extras:
                        m.poe(m.tema_eco, pan(v4.sino(n, 0.7), -0.15), em)
                    m.poe(m.tema_eco, supersaw(n, d, 0.7, r.brilho * 0.75), em)
                    if r.chefe or r.voz in ("metal", "ambos"):
                        m.poe(m.tema, metais([n - 12], d, 0.6), em)
        if sec == "Respiro" and local == 0:
            for fb, ini, dur, n in temas["Tema"][: len(temas["Tema"]) // 2]:
                em = m.t(40 + (fb - 8)) + ini * BEAT
                d = dur * BEAT * 0.94
                m.poe(m.tema_eco, supersaw(n, d, 0.6, r.brilho * 0.55), em)
                if r.voz == "sino" or "sinos" in r.extras or r.chefe:
                    m.poe(m.tema_eco, pan(v4.sino(n, 0.6), 0.2), em)

    m.renderiza(f"caminho do nexus · {r.nome} (v8)")


# ------------------------------------------------------------------ as 16 receitas
def regioes():
    R = {}
    R["vila"] = Receita("reg-vila", 138, 60, "maior",
                        {"Chegada": ["0M", "7M", "9m", "5M"], "Tema": ["0M", "7M", "9m", "5M", "0M", "5M", "7M", "7M"],
                         "Ponte": ["9m", "5M", "0M", "7M", "2m", "5M", "7M", "7M"], "Respiro": ["5M", "0M", "2m", "7M"],
                         "Refrão": ["5M", "7M", "0M", "9m", "5M", "7M", "0M", "0M"]},
                        "saltitante", [1, 1, -1, 2, -1, -1, 1, 0], "marcha", "saltitante", "marcha", "sino", ("caixinha", "sinos"), 6200, semente=801)
    R["floresta"] = Receita("reg-floresta", 120, 62, "dorico",
                            {"Chegada": ["0m", "5M", "0m", "10M"], "Tema": ["0m", "5M", "3M", "10M", "0m", "5M", "10M", "10M"],
                             "Ponte": ["3M", "10M", "5M", "0m", "3M", "10M", "7m", "7m"], "Respiro": ["0m", "5M", "3M", "10M"],
                             "Refrão": ["3M", "10M", "0m", "5M", "3M", "10M", "5M", "5M"]},
                            "longo", [1, 2, -1, -1, 2], "tribal", "tribal", "pizzicato", "coro", ("coro", "taikos"), 3600, semente=802)
    R["neon"] = Receita("reg-neon", 128, 57, "menor",
                        {"Chegada": ["0m", "8M", "3M", "10M"], "Tema": ["0m", "8M", "3M", "10M"],
                         "Ponte": ["5m", "8M", "3M", "10M", "5m", "8M", "7M", "7M"], "Respiro": ["8M", "3M", "10M", "0m"],
                         "Refrão": ["8M", "10M", "0m", "0m", "8M", "10M", "7M", "7M"]},
                        "sincopado", [1, 1, 2, -1, -2, 1, 1, 0, -1, 1], "quatro", "pulsante", "arpejo", "saw", (), 6800, semente=803)
    R["deserto"] = Receita("reg-deserto", 112, 52, "hijaz",
                           {"Chegada": ["0M", "1M", "0M", "10m"], "Tema": ["0M", "1M", "0M", "10m", "5m", "1M", "0M", "0M"],
                            "Ponte": ["5m", "1M", "0M", "0M", "8M", "1M", "0M", "0M"], "Respiro": ["0M", "1M", "5m", "0M"],
                            "Refrão": ["5m", "8M", "1M", "0M", "5m", "1M", "0M", "0M"]},
                           "ornado", [1, -1, 1, 2, -1, -1, 1, -1, -1, 0], "maqsum", "drone", "pizzicato", "metal", ("taikos",), 4200, semente=804)
    R["templo"] = Receita("reg-templo", 108, 62, "hirajoshi",
                          {"Chegada": ["0m", "8M", "0m", "7m"], "Tema": ["0m", "8M", "5m", "7m"],
                           "Ponte": ["8M", "5m", "0m", "7m", "8M", "10M", "7m", "7m"], "Respiro": ["0m", "8M", "5m", "7m"],
                           "Refrão": ["8M", "10M", "0m", "5m", "8M", "10M", "7M", "7M"]},
                          "longo", [2, -1, 1, -2, 1], "meio", "drone", "arpejo", "sino", ("sinos", "coro", "taikos"), 3800, semente=805)
    R["vulcao"] = Receita("reg-vulcao", 172, 52, "frigio",
                          {"Chegada": ["0m", "1M", "0m", "10M"], "Tema": ["0m", "1M", "0m", "10M", "8M", "10M", "0m", "0m"],
                           "Ponte": ["0m", "1M", "0m", "1M", "5m", "1M", "10M", "10M"], "Respiro": ["8M", "10M", "0m", "1M"],
                           "Refrão": ["8M", "10M", "0m", "0m", "8M", "10M", "1M", "1M"]},
                          "galope", [1, 1, 2, -1, 1, 2, -2, -1, 0], "metal", "metal", "metal", "ambos", (), 5200, semente=806)
    R["ceu"] = Receita("reg-ceu", 150, 65, "lidio",
                       {"Chegada": ["0M", "2M", "0M", "2M"], "Tema": ["0M", "2M", "9m", "7M", "0M", "2M", "5M", "7M"],
                        "Ponte": ["9m", "4m", "5M", "0M", "9m", "2M", "7M", "7M"], "Respiro": ["5M", "0M", "2M", "7M"],
                        "Refrão": ["5M", "7M", "9m", "0M", "5M", "7M", "2M", "2M"]},
                       "heroico", [2, 1, 2, -1, 1, -2, 0], "galope", "galope", "orquestra", "ambos", ("coro", "sinos"), 6400, semente=807)
    R["trono"] = Receita("reg-trono", 166, 59, "harmonica",
                         {"Chegada": ["0m", "5m", "7M", "0m"], "Tema": ["0m", "5m", "7M", "0m", "8M", "3M", "5m", "7M"],
                          "Ponte": ["8M", "3M", "5m", "0m", "8M", "1M", "7M", "7M"], "Respiro": ["0m", "8M", "5m", "7M"],
                          "Refrão": ["8M", "7M", "0m", "5m", "8M", "1M", "7M", "7M"]},
                         "heroico", [2, 1, 2, -2, 1, -1, 0], "galope", "galope", "orquestra", "ambos", ("coro", "sinos", "taikos"), 5600, semente=808)
    return R


def chefes():
    """O chefe de cada região: a mesma terra, mais rápido, no menor escuro, com sinos, tímpanos, coro e metais."""
    C = {}
    for nome, r in regioes().items():
        prog = r.prog
        if nome == "floresta":                                                   # o dórico fica menor: o IV maior vira menor
            prog = {k: [{"5M": "5m"}.get(x, x) for x in v] for k, v in r.prog.items()}
        if nome in ("vila", "ceu"):
            # as regiões em tom maior viram menor no chefe: o mesmo lugar, agora perigoso
            escala = "menor"
            prog = {k: [{"0M": "0m", "7M": "7M", "9m": "8M", "5M": "5m", "2m": "10M", "2M": "10M", "4m": "3M"}.get(x, x) for x in v] for k, v in r.prog.items()}
        else:
            escala = {"dorico": "menor", "lidio": "harmonica"}.get(next(k for k, s in ESCALAS.items() if s == r.escala), next(k for k, s in ESCALAS.items() if s == r.escala))
        motivo = {"saltitante": "heroico", "longo": "heroico", "sincopado": "galope", "ornado": "ornado", "galope": "galope", "heroico": "galope"}[next(k for k, v in MOTIVOS.items() if v == r.motivo)]
        bateria = {"marcha": "galope", "quatro": "galope", "tribal": "galope", "maqsum": "maqsum", "meio": "galope", "metal": "metal", "galope": "metal"}[r.bateria]
        baixo_ = {"saltitante": "galope", "pulsante": "galope", "tribal": "galope", "drone": "galope", "metal": "metal", "galope": "metal"}[r.baixo]
        acomp = {"marcha": "galope", "arpejo": "arpejo" if nome == "neon" else "metal", "pizzicato": "orquestra", "metal": "metal", "orquestra": "metal"}[r.acomp]
        C[nome] = Receita(r.nome.replace("reg-", "chefe-"), min(184, r.bpm + 18), r.tonica, escala, prog, motivo, r.contorno, bateria, baixo_, acomp,
                          "ambos", tuple(r.extras | {"coro", "sinos"}), r.brilho, chefe=True, semente=r.semente + 100)
    return C


if __name__ == "__main__":
    pedidos = sys.argv[1:] or ["regioes", "chefes"]
    R, C = regioes(), chefes()
    for p in pedidos:
        if p == "regioes":
            for r in R.values():
                faz(r)
        elif p == "chefes":
            for r in C.values():
                faz(r)
        elif p.startswith("chefe-"):
            faz(C[p[6:]])
        else:
            faz(R[p])
