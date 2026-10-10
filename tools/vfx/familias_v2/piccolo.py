"""As três habilidades do Piccolo, desenhadas para ele.

Pedido do jogador: "a primeira skill dele tinha que ser Makankosappo… de
ataque… troca o nome da segunda… e faz as skills do Piccolo também, os efeitos,
bem feita".

- makanko_carga: os dois dedos na testa, a ponta acendendo e a espiral de ki
  girando em volta dela, com os estalos (no Preparo, laço).
- makanko_faixa: o raio fino e reto do Piccolo até o rival, com a espiral
  enrolada em volta dele girando (faixa, laço).
- makankosappo: o raio fura o rival — entra por −x, a espiral aperta no
  ponto, o clarão e os pedaços saindo pelas costas (+x).
- escudo_do_mentor: a capa passa na frente do aliado e a barreira de ki sobe e
  fecha em volta dele, com a malha acendendo.
- regeneracao_namekiana: as gotas de ki voltam para o corpo, o braço novo
  nasce do ombro e a onda de vida fecha.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _espiral(T, x0, x1, y, amp, voltas, giro, larg, n=260):
    """A espiral em volta de um eixo horizontal: devolve (frente, trás). O lado que passa na frente
    do raio é mais forte; o de trás é mais fraco, o que dá a ideia de volume."""
    frente, tras = [], []
    for fase in (0.0, math.pi):
        for k in range(n):
            f = k / (n - 1)
            ph = TAU * voltas * f - giro + fase
            a = amp(f) if callable(amp) else amp
            x = x0 + (x1 - x0) * f
            yy = y + a * math.sin(ph)
            (frente if math.cos(ph) > 0 else tras).append((x, yy, 1.0))
    return T.splats(frente, larg), T.splats(tras, larg)


# ------------------------------------------------------------------ Makankosappo
def makanko_carga(T, t, rng):
    """A ponta dos dois dedos acendendo na testa: o ponto muito claro, a espiral de ki apertando em
    volta dele (duas fitas girando para dentro) e os estalos curtos."""
    G, H = vazio(T)
    q = _quadro(t, 41)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 5)
    ponto = T.gauss(0, 0, 0.06) * pul
    halo = T.gauss(0, 0, 0.2) * 0.5
    fitas = []
    for j in range(2):
        for k in range(70):
            f = k / 69
            r = 0.7 * (1 - f) + 0.05
            a = TAU * (1.6 * f + t * 2) + math.pi * j
            fitas.append((r * math.cos(a), r * math.sin(a) * 0.8, f ** 0.7))
    F = T.splats(fitas, 0.014)
    estalos = T.zero()
    for _ in range(3):
        a = q.uniform(0, TAU)
        r0 = q.uniform(0.08, 0.15)
        pts = jagged(q, r0 * math.cos(a), r0 * math.sin(a), 0.4 * math.cos(a), 0.4 * math.sin(a), 3, 0.3)
        estalos += T.polyline(pts, 0.008)
    G += ponto * 1.8 + halo + F * 1.2 + T.blur(F, 0.02) * 0.6 + estalos * 1.1
    H += ponto * 2.0 + F * 0.5 + estalos * 0.8
    return G, H


def makanko_faixa(T, t, rng):
    """O raio do Makankosappo esticado do Piccolo até o rival: o núcleo fino e reto, a espiral que
    gira em volta dele (a parte da frente forte, a de trás fraca) e o brilho do lado."""
    G, H = vazio(T)
    alto = T.H / T.W
    nucleo = T.lines([(-0.98, 0.0, 0.98, 0.0, 1.0)], 0.02)
    frente, tras = _espiral(T, -0.98, 0.98, 0.0, lambda f: alto * (0.2 + 0.14 * f) * min(1.0, f / 0.04 + 0.2),
                            7, TAU * t * 3, 0.0065, 620)
    brilho = T.gauss(0, 0, 2.0, alto * 0.22)
    ponta = T.gauss(-0.95, 0, 0.04, alto * 0.3)
    G += nucleo * 1.8 + T.blur(nucleo, 0.012) * 1.6 + frente * 1.2 + tras * 0.35 + brilho * 0.25 + ponta
    H += nucleo * 1.6 + frente * 0.55 + ponta * 0.9
    return G, H


def makankosappo(T, t, rng):
    """O raio fura o rival: a ponta entra por −x, a espiral aperta no ponto (os anéis girando, vistos
    de lado), o clarão, o furo que abre e os pedaços saindo pelas costas (+x)."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    entra = ease_in(rel(t, 0.0, 0.12), 1.5)
    raio = T.lines([(-1.0, 0.0, -0.95 + 1.0 * entra, 0.0, 1.0)], 0.02) * (1 - rel(t, 0.3, 0.55))
    # os anéis da espiral, achatados (vistos de lado), girando e correndo para a frente
    aneis = T.zero()
    for j in range(5):
        f = (j / 5 + t * 1.6) % 1
        x = -0.75 + 0.95 * f
        if x > -0.95 + entra:
            continue
        u = (T.U - x) / 0.06
        v = T.V / (0.22 * (1 - 0.5 * f) + 0.04)
        aneis += np.exp(-((np.hypot(u, v) - 1) / 0.18) ** 2) * (0.5 + 0.5 * f)
    aneis *= 1 - rel(t, 0.35, 0.6)
    k = pulso(t, 0.1, 0.45)
    clarao = T.gauss(0, 0, 0.2) * k * 2.0 + T.flare(0, 0, 1.1 * k + 1e-3, 0.0, 0.01)
    # o furo: um anel que abre e um ponto escuro no meio (sai da luz)
    furo = T.ring(0.05 + 0.18 * ease_out(rel(t, 0.12, 0.5), 2), 0.03) * pulso(t, 0.12, 0.7)
    # o raio que sai pelas costas, comprido
    sai = ease_out(rel(t, 0.12, 0.3), 2)
    costas = T.lines([(0.0, 0.0, 0.98 * sai, 0.0, 1.0)], 0.016) * (1 - rel(t, 0.4, 0.7))
    sub = np.random.default_rng(57)
    pedacos = []
    for _ in range(24):
        a = sub.normal(0, 0.35)
        d = 0.08 + 0.8 * ease_out(rel(t, 0.12, 0.8), 2) * sub.uniform(0.35, 1)
        pedacos.append((d * math.cos(a), d * math.sin(a) + 0.15 * rel(t, 0.3, 1.0) ** 2, pulso(t, 0.12, 0.9) * sub.uniform(0.4, 1)))
    P = T.splats(pedacos, 0.012)
    G += (raio * 1.6 + T.blur(raio, 0.015) + aneis * 1.1 + clarao + furo * 1.2 + costas * 1.5 + T.blur(costas, 0.02) + P * 1.2) * env
    H += (raio * 1.4 + aneis * 0.5 + clarao * 1.1 + furo * 0.6 + costas * 1.2 + P * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Escudo do mentor
def _capa(T, cx, larg, alto, balanco):
    """A capa: os ombros arredondados no alto e o pano abrindo para baixo, com a barra ondulando."""
    pts = []
    n = 14
    for k in range(n + 1):        # lado esquerdo, de cima para baixo
        f = k / n
        pts.append((cx - larg * (0.62 + 0.18 * f), -alto * 0.42 + alto * 0.92 * f))
    for k in range(n + 1):        # barra, da esquerda para a direita, ondulando
        f = k / n
        x = cx - larg * 0.8 + larg * 1.6 * f
        pts.append((x, alto * 0.5 + 0.04 * math.sin(TAU * (2 * f + balanco))))
    for k in range(n, -1, -1):    # lado direito, de baixo para cima
        f = k / n
        pts.append((cx + larg * (0.62 + 0.18 * f), -alto * 0.42 + alto * 0.92 * f))
    return pts


def escudo_do_mentor(T, t, rng):
    """A capa branca do Piccolo passa na frente do aliado (da esquerda para a direita) e a barreira
    de ki sobe por baixo e fecha numa cúpula; a malha acende e o brilho fica pulsando."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    # a capa varrendo
    f = ease_out(rel(t, 0.0, 0.32), 2.2)
    cx = -1.0 + 1.0 * f
    capa = T.polys([(_capa(T, cx, 0.55, 0.95, t * 2), 1.0)], 0.006)
    gola = T.polyline([(cx - 0.4, -0.33), (cx - 0.25, -0.43), (cx + 0.25, -0.43), (cx + 0.4, -0.33)], 0.07)
    capa = np.maximum(capa, gola)
    capa = np.clip(capa, 0, 1) * (1 - rel(t, 0.3, 0.5))
    dobras = T.zero()
    for j in (-0.2, 0.0, 0.2):
        dobras += T.lines([(cx + j * 0.8, -0.35, cx + j * 1.3, 0.42, 1.0)], 0.008)
    capa_tudo = np.clip(capa - dobras * 0.5 * capa, 0, None)
    # a cúpula subindo de baixo
    sobe = ease_out(rel(t, 0.18, 0.55), 2)
    R = 0.72
    topo = 0.62 - (R + 0.62) * sobe       # linha que sobe: acima dela ainda não tem cúpula
    corte = 1 / (1 + np.exp(-(T.V - topo) / 0.02))
    borda = T.ring(R, 0.03, 0, 0.0, 1.05) * corte
    dentro = (T.RAD < R).astype(np.float32) * corte
    malha = T.zero()
    k = 0.15
    for th in (math.pi / 6, math.pi / 2, 5 * math.pi / 6):
        p = (T.U * math.cos(th) + T.V * math.sin(th)) / k
        malha = np.maximum(malha, np.exp(-((p - np.round(p)) / 0.07) ** 2))
    luz_malha = malha * dentro * (0.25 + 0.6 * pulso(t, 0.45, 0.8)) * np.clip(T.RAD / R, 0.25, 1)
    frente_sobe = np.exp(-((T.V - topo) / 0.03) ** 2) * (T.RAD < R) * (sobe < 1) * (1 - rel(t, 0.5, 0.58))
    fecha = pulso(t, 0.5, 0.8)
    clarao = T.flare(0, -R + 0.02, 0.9 * fecha + 1e-3, 0.0, 0.01) * fecha
    respira = 0.85 + 0.15 * math.sin(TAU * t * 3)
    sub = np.random.default_rng(71)
    pontos = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        ff = (sub.uniform() + t * 0.8) % 1
        rr = R * (0.95 + 0.1 * sub.uniform())
        pontos.append((rr * math.cos(a), rr * math.sin(a) - 0.25 * ff, (1 - ff) * sub.uniform(0.4, 1) * rel(t, 0.3, 0.5)))
    G += (capa_tudo * 1.1 + (borda * 1.3 + T.blur(borda, 0.03) * 0.9) * respira + dentro * 0.12 + luz_malha
          + frente_sobe * 1.2 + clarao + T.splats(pontos, 0.012)) * env
    H += (capa_tudo * 0.9 + borda * 0.6 + frente_sobe * 0.8 + clarao * 0.9 + luz_malha * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Regeneração namekiana
def regeneracao_namekiana(T, t, rng):
    """A regeneração do Piccolo: as gotas de ki voltam para o corpo de todos os lados, o braço novo
    nasce do ombro e se estica até a mão abrir, e a onda de vida fecha em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sub = np.random.default_rng(83)
    gotas = []
    for _ in range(30):
        a = sub.uniform(0, TAU)
        d0 = sub.uniform(0.55, 0.95)
        f = ease_in(rel(t, sub.uniform(0.0, 0.15), 0.45), 1.6)
        d = d0 * (1 - f) + 0.05
        gotas.append((d * math.cos(a), d * math.sin(a), (1 - rel(t, 0.38, 0.5)) * sub.uniform(0.5, 1)))
    Gt = T.splats(gotas, 0.022)
    # o braço nascendo do ombro: o tronco do braço sai e estica, com a mão (três dedos) no fim
    cresce = ease_out(rel(t, 0.3, 0.7), 2.4)
    ox, oy = -0.3, 0.05
    ang = -0.3
    comp = 0.78 * cresce
    ex, ey = ox + comp * math.cos(ang), oy + comp * math.sin(ang)
    braco = (T.polyline([(ox, oy), (ox + (ex - ox) * 0.5, oy + (ey - oy) * 0.5 + 0.03), (ex + 1e-3, ey)], 0.12) + T.gauss(ox, oy, 0.12)) * (cresce > 0.01)
    mao = T.zero()
    if cresce > 0.5:
        abre = rel(cresce, 0.5, 1.0)
        mao += T.gauss(ex, ey, 0.085) * abre
        for d in (-0.5, 0.0, 0.5):
            a2 = ang + d * abre
            mao += T.tapered([(ex, ey, ex + 0.22 * abre * math.cos(a2) + 1e-3, ey + 0.22 * abre * math.sin(a2), 1.0)], 0.05)
    # as veias de luz no braço novo
    veia = T.lines([(ox, oy, ox + (ex - ox) * 0.9, oy + (ey - oy) * 0.9, 1.0)], 0.008) * pulso(t, 0.45, 0.9)
    k = pulso(t, 0.62, 0.95)
    onda = T.ring(0.15 + 0.65 * ease_out(rel(t, 0.62, 0.95), 2), 0.05) * k
    corpo = T.gauss(0, 0, 0.3) * (0.3 + 0.4 * pulso(t, 0.3, 0.9))
    sobem = []
    for _ in range(18):
        x = sub.uniform(-0.5, 0.5)
        ff = (sub.uniform() + t * 1.2) % 1
        sobem.append((x, 0.5 - 0.9 * ff, (1 - ff) * rel(t, 0.55, 0.7) * sub.uniform(0.4, 1)))
    G += (Gt * 1.2 + braco * 1.1 + mao * 1.2 + veia * 0.8 + onda * 1.2 + T.blur(onda, 0.03) * 0.5 + corpo + T.splats(sobem, 0.014)) * env
    H += (Gt * 0.6 + braco * 0.4 + mao * 0.5 + veia * 1.0 + onda * 0.4 + corpo * 0.5) * env
    return G, H


REGISTRO = [
    ("makanko_carga", makanko_carga, MEDIA, "Piccolo · os dedos na testa e a espiral de ki apertando (laço)", True),
    ("makanko_faixa", makanko_faixa, FAIXA, "Piccolo · o raio do Makankosappo com a espiral girando (faixa)", True),
    ("makankosappo", makankosappo, GRANDE, "Piccolo · Makankosappo: o raio fura o rival e sai pelas costas", False),
    ("escudo_do_mentor", escudo_do_mentor, GRANDE, "Piccolo · a capa passa na frente e a barreira de ki fecha", False),
    ("regeneracao_namekiana", regeneracao_namekiana, GRANDE, "Piccolo · as gotas voltam e o braço novo nasce", False),
]
