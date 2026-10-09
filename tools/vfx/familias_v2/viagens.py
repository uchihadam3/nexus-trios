"""O que sai do personagem e vai até o alvo.

Pedido do jogador: "efeitos à distância, ele deveria sair do personagem e ir até
o coisa… o dragão saísse do Shiryu, fosse grande… o escudo também saindo do
Capitão e indo até no personagem". Folhas em laço: as de voo (MEDIA) mostram o
objeto inteiro apontado para +x, girando, com o rastro atrás; a do dragão é uma
faixa (esticada de quem age até o alvo), o corpo serpenteando e a cabeça na ponta.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, estrela, janela, lamina, pulso, rel, smooth, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _rastro(T, cx, n=5, comp=0.75, espalha=0.12, larg=0.018, seed=3):
    sub = np.random.default_rng(seed)
    segs = []
    for k in range(n):
        y = (k - (n - 1) / 2) * espalha / max(1, n - 1) * 2
        c = comp * sub.uniform(0.6, 1)
        segs.append((cx - 0.2 - c, y, cx - 0.2, y, sub.uniform(0.5, 1)))
    return T.tapered(segs, larg)


# ------------------------------------------------------------------ objetos que voam
def escudo_voando(T, t, rng):
    """O escudo do Capitão em voo: o disco visto meio de lado, os aros e a estrela girando."""
    G, H = vazio(T)
    cx, giro = 0.3, TAU * t * 2
    sq = 0.62 + 0.08 * math.sin(giro)
    aros = T.ring(0.34, 0.03, cx=cx, squash=1 / sq) + T.ring(0.24, 0.03, cx=cx, squash=1 / sq) * 0.85 + T.ring(0.14, 0.025, cx=cx, squash=1 / sq) * 0.7
    est = T.polys([([(cx + x, y * sq) for x, y in _gira([(math.cos(a) * r, math.sin(a) * r) for a, r in ((giro + math.pi * k / 5, 0.11 if k % 2 == 0 else 0.045) for k in range(10))], 0.0)], 1.0)], 0.003)
    disco = T.gauss(cx, 0, 0.3, 0.3 * sq) * 0.5
    G += disco + aros * 1.2 + est * 1.4 + _rastro(T, cx, 5, 0.6, 0.18, 0.02) * 0.7
    H += aros * 0.5 + est * 1.1
    return G, H


def batarangue_voando(T, t, rng):
    """O batarangue em voo: a silhueta de morcego girando rápido, com o rastro em arco."""
    G, H = vazio(T)
    cx = 0.3
    asa = [(0.0, 0.0), (0.12, -0.05), (0.2, -0.16), (0.25, -0.05), (0.33, -0.1), (0.36, 0.02), (0.25, 0.02), (0.18, 0.06), (0.08, 0.04)]
    morcego = asa + [(-x, y) for x, y in reversed(asa)]
    giro = TAU * t
    B = T.polys([(_gira([(x * 1.25, y * 1.25) for x, y in morcego], giro, cx, 0.0), 1.0)], 0.003)
    arco = T.arc_band(0.3, 0.03, giro - 2.4, giro, cx=cx, taper=1.3) * 0.7
    G += B * 1.4 + arco + _rastro(T, cx, 3, 0.55, 0.1) * 0.5
    H += B * 0.9 + arco * 0.4
    return G, H


def shuriken_voando(T, t, rng):
    """Duas shurikens de quatro pontas girando em formação."""
    G, H = vazio(T)
    giro = TAU * t
    formas = []
    for cx, cy in ((0.35, -0.12), (0.12, 0.14)):
        formas.append((estrela(cx, cy, 0.17, giro, 4, 0.3), 1.0))
    S = T.polys(formas, 0.003)
    furos = T.gauss(0.35, -0.12, 0.025) + T.gauss(0.12, 0.14, 0.025)
    G += S * 1.4 + _rastro(T, 0.25, 4, 0.5, 0.26) * 0.6 - furos * 0.6
    H += S * 0.9
    return G, H


def tiara_voando(T, t, rng):
    """A tiara lunar em voo: o disco dourado girando com a meia-lua no meio e brilhos."""
    G, H = vazio(T)
    cx, giro = 0.3, TAU * t * 2
    sq = 0.55 + 0.1 * math.sin(giro)
    aro = T.ring(0.28, 0.05, cx=cx, squash=1 / sq)
    lua = T.polys([([(cx + math.cos(a) * 0.13 * (1 if k < 13 else 0.7) + (0 if k < 13 else 0.05), math.sin(a) * 0.13 * sq) for k, a in enumerate(list(np.linspace(-1.9, 1.9, 13)) + list(np.linspace(1.9, -1.9, 13)))], 1.0)], 0.003)
    brilho = T.flare(cx + 0.28 * math.cos(giro * 2), 0.28 * sq * math.sin(giro * 2), 0.35, giro, 0.02)
    G += aro * 1.3 + lua * 1.2 + brilho + _rastro(T, cx, 5, 0.55, 0.16) * 0.6
    H += aro * 0.6 + lua + brilho * 0.8
    return G, H


def _crescente(cx, cy, r, ang, n=16):
    fora, dentro = [], []
    for k in range(n + 1):
        a = math.pi * (0.36 + 1.28 * k / n)
        fora.append((math.cos(a) * r, math.sin(a) * r))
        dentro.append((math.cos(a) * r * 0.8 + r * 0.32, math.sin(a) * r * 0.8))
    return _gira(fora + dentro[::-1], ang, cx, cy)


def dardo_voando(T, t, rng):
    """Os três dardos crescentes do Cavaleiro da Lua girando em formação."""
    G, H = vazio(T)
    giro = TAU * t
    D = T.polys([(_crescente(cx, cy, 0.15, giro + k), 1.0) for k, (cx, cy) in enumerate(((0.4, 0.0), (0.12, -0.2), (0.12, 0.2)))], 0.003)
    G += D * 1.4 + _rastro(T, 0.25, 5, 0.5, 0.36) * 0.5
    H += D * 0.9
    return G, H


def _asa(lift, s=(0.14, -0.03), raiz=(-0.1, -0.01), dedos=5):
    """Asa de ave vista de lado: bordo de ataque curvo até a ponta e as penas abertas atrás."""
    dy = -0.42 * lift
    ponta = (0.0, s[1] + dy)
    pts = [s, (0.13, s[1] + dy * 0.6), ponta]
    for k in range(1, dedos + 1):
        f = k / (dedos + 1)
        bx, by = ponta[0] + (raiz[0] - ponta[0]) * f, ponta[1] + (raiz[1] - ponta[1]) * f
        pts += [(bx - 0.07 * (1 - f * 0.6), by + 0.02 * math.copysign(1, dy or 1)), (bx + 0.01, by)]
    pts.append(raiz)
    return pts


def corvo_voando(T, t, rng):
    """O corvo de energia da Ravena voando: asas de penas batendo, bico, cauda em leque, o olho
    aceso e a fumaça de sombra que fica para trás."""
    G, H = vazio(T)
    bate = math.sin(TAU * t * 2)
    sobe = 0.02 * math.cos(TAU * t * 2)
    corpo = [(0.3, -0.07), (0.38, -0.05), (0.5, -0.02), (0.38, 0.0), (0.3, 0.04), (0.1, 0.06), (-0.12, 0.04), (-0.18, 0.0), (-0.1, -0.04), (0.12, -0.06)]
    cauda = [(-0.14, -0.02), (-0.36, -0.1), (-0.33, -0.03), (-0.38, 0.02), (-0.33, 0.06), (-0.36, 0.12), (-0.14, 0.04)]
    perto = _asa(bate)
    longe = [(x - 0.04, y - 0.02) for x, y in _asa(bate * 0.8 + 0.15)]
    sob = lambda pts: [(x, y + sobe) for x, y in pts]
    C = T.polys([(sob(longe), 0.55), (sob(corpo), 1.0), (sob(cauda), 0.9), (sob(perto), 1.0)], 0.004)
    olho = T.gauss(0.36, -0.035 + sobe, 0.016, 0.012)
    sub = np.random.default_rng(7)
    fumo = []
    for _ in range(18):
        f = (sub.uniform() + t) % 1
        fumo.append((-0.3 - 0.65 * f, sub.normal(0, 0.05) + 0.1 * f * sub.normal(), 0.7 * (1 - f)))
    Fm = T.splats(fumo, 0.045)
    G += C * 1.3 + T.blur(C, 0.025) * 0.8 + Fm * 0.8
    H += C * 0.25 + T.ring(0.0, 0.004) * 0 + olho * 3.0
    return G, H


# ------------------------------------------------------------------ o dragão do Shiryu
def dragao_faixa(T, t, rng):
    """O dragão do Cólera do Dragão esticado de quem age até o alvo: o corpo serpenteia (mais fino
    na cauda, perto do Shiryu, e grosso perto da cabeça), as escamas e as barbatanas correm, e a
    cabeça na ponta, de boca aberta, com chifres e bigodes."""
    G, H = vazio(T)
    alto = T.H / T.W
    fase = TAU * t
    n = 60
    cima, baixo, dorso = [], [], []
    for k in range(n + 1):
        u = k / n
        x = -0.98 + 1.7 * u
        y = alto * 0.45 * math.sin(u * 3.2 * math.pi - fase * 2) * (0.4 + 0.6 * u)
        w = alto * (0.08 + 0.3 * u ** 0.8)
        cima.append((x, y - w))
        baixo.append((x, y + w))
        if k % 4 == 0 and 0.1 < u < 0.95:
            dorso.append((x, y - w, u))
    corpo = T.polys([(cima + baixo[::-1], 1.0)], 0.004)
    # escamas: marcas em V ao longo do corpo, correndo
    escamas = T.zero()
    for k in range(4, n - 4, 3):
        u = (k / n + t * 0.05) % 1
        x0, y0 = cima[k]
        _, y1 = baixo[k]
        meio = (y0 + y1) / 2
        escamas += T.polyline([(x0 - 0.012, y0 + (meio - y0) * 0.3), (x0 + 0.01, meio), (x0 - 0.012, y1 - (y1 - meio) * 0.3)], 0.004) * (0.5 + 0.5 * u)
    barbatanas = T.polys([([(x - 0.02, y), (x + 0.015, y - alto * (0.12 + 0.14 * u)), (x + 0.03, y)], 0.9) for x, y, u in dorso], 0.004)
    # cabeça na ponta (+x)
    hx, hy = cima[-1][0], (cima[-1][1] + baixo[-1][1]) / 2
    a = alto
    boca = 0.35 + 0.25 * math.sin(fase * 3)
    cabeca = [(hx - 0.02, hy - a * 0.42), (hx + 0.12, hy - a * 0.38), (hx + 0.2, hy - a * 0.2 * boca - a * 0.05), (hx + 0.08, hy - a * 0.02),
              (hx + 0.18, hy + a * 0.2 * boca + a * 0.04), (hx + 0.08, hy + a * 0.36), (hx - 0.02, hy + a * 0.42)]
    chifres = [[(hx + 0.02, hy - a * 0.38), (hx - 0.1, hy - a * 0.85), (hx + 0.06, hy - a * 0.4)], [(hx + 0.0, hy - a * 0.3), (hx - 0.13, hy - a * 0.62), (hx + 0.03, hy - a * 0.32)]]
    Cb = T.polys([(cabeca, 1.0)] + [(c, 0.9) for c in chifres], 0.004)
    olho = T.gauss(hx + 0.07, hy - a * 0.22, 0.012, 0.01)
    bigodes = sum(T.polyline([(hx + 0.12, hy + s * a * 0.08), (hx + 0.02 - 0.15 * k / 6, hy + s * a * (0.15 + 0.4 * math.sin(k / 6 * 2 + fase + s)) ) if False else (hx - 0.1, hy + s * a * (0.5 + 0.2 * math.sin(fase * 2 + s)))], 0.004) for k, s in ((0, 1), (0, -1)))
    ponta = smooth(T.U, -0.99, -0.94)
    G += (corpo * 1.1 + T.blur(corpo, 0.012) * 0.8 + barbatanas * 0.9 + Cb * 1.2 + T.blur(Cb, 0.01) * 0.8 + bigodes * 0.8) * ponta
    H += (escamas * 1.4 + corpo * 0.25 + Cb * 0.45 + olho * 3.0 + barbatanas * 0.3) * ponta
    return G, H


def colera_impacto(T, t, rng):
    """O dragão atravessa o alvo: o estouro de energia verde-água no ponto de entrada, as escamas e
    os respingos saindo pelo outro lado (+x, para onde o dragão segue) e o anel que abre e some."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    k = pulso(t, 0.0, 0.4)
    est = T.polys([(estrela(0.0, 0.0, 0.34 * k + 0.01, 0.2, 9, 0.35), 1.0)], 0.005) * k
    anel = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.0, 0.55), 2.2), 0.04) * pulso(t, 0.0, 0.6)
    clarao = T.gauss(0, 0, 0.22, 0.22) * pulso(t, 0.0, 0.25) * 2.2
    # o rastro do corpo passando: faixas que atravessam o alvo e seguem para +x
    sub = np.random.default_rng(91)
    riscos = []
    for _ in range(9):
        y = sub.normal(0, 0.12)
        x0 = -0.5 + 1.6 * ease_out(rel(t, 0.0, 0.7), 1.6) * sub.uniform(0.6, 1)
        riscos.append((x0 - 0.45, y, x0, y, pulso(t, 0.0, 0.75) * sub.uniform(0.5, 1)))
    R = T.tapered(riscos, 0.035)
    # escamas soltas e respingos voando para frente
    gotas = []
    for _ in range(22):
        a = sub.normal(0, 0.6)
        d = 0.1 + 0.85 * ease_out(rel(t, 0.05, 0.8), 2) * sub.uniform(0.4, 1)
        gotas.append((d * math.cos(a), d * math.sin(a) * 0.8, pulso(t, 0.05, 0.85) * sub.uniform(0.4, 1)))
    Gt = T.splats(gotas, 0.016)
    G += (est * 1.2 + anel + clarao + R * 1.1 + T.blur(R, 0.02) + Gt * 1.3) * env
    H += (est + anel * 0.4 + clarao * 1.2 + R * 0.6 + Gt * 0.8) * env
    return G, H


REGISTRO = [
    ("escudo_voando", escudo_voando, MEDIA, "o escudo do Capitão girando em voo (+x)", True),
    ("batarangue_voando", batarangue_voando, MEDIA, "o batarangue girando em voo (+x)", True),
    ("shuriken_voando", shuriken_voando, MEDIA, "duas shurikens girando em voo (+x)", True),
    ("tiara_voando", tiara_voando, MEDIA, "a tiara lunar girando em voo (+x)", True),
    ("dardo_voando", dardo_voando, MEDIA, "os dardos crescentes girando em voo (+x)", True),
    ("corvo_voando", corvo_voando, MEDIA, "o corvo de energia voando (+x)", True),
    ("dragao_faixa", dragao_faixa, FAIXA, "o dragão do Cólera do Dragão esticado até o alvo (faixa)", True),
    ("colera_impacto", colera_impacto, GRANDE, "o dragão atravessando o alvo: estouro e rastro para a frente", False),
]
