"""Ataques básicos com animação própria, lote zc: Docinho, Mickey, Buzz Lightyear, Woody, Gelado, Iroh, Destruidor e
Casey Jones.

Golpes simples, cada um do personagem: a Docinho voando no soco com o rastro verde de Meninas Superpoderosas, a luva
branca do Mickey com as notinhas musicais saindo, o golpe de caratê do Buzz de mão reta caindo de cima, o soco do
Woody com a estrela de xerife brilhando, o soco do Gelado deslizando na rampa de gelo, a palma de fogo do Iroh com
a chama girando mansa, a manopla de lâminas do Destruidor e o soco com luva de hóquei do Casey Jones, que manda o
disco voando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_w import _soco
from .basicos_x import _gotas


# ------------------------------------------------------------------ Docinho
def soco_superpoderosa(T, t, rng):
    """Docinho: chega voando como um cometa, o punhinho redondo (sem dedos) na frente e o rastro grosso de cor atrás,
    e o acerto é uma estrela de desenho com o anel."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.18), 1.4)
    px = -1.0 + 0.88 * u - 0.25 * ease_out(rel(t, 0.3, 0.6), 2)
    vis = janela(t, 0.0, 0.03) * (1 - rel(t, 0.44, 0.6))
    punho = T.polys([(_elipse_pts(px, 0.0, 0.18, 0.16, 0.0, 18), 1.0)], 0.003) * vis
    rastro = T.zero()
    kr = vis * (1 - rel(t, 0.18, 0.4))
    if kr > 0:
        rastro = T.tapered([(px - 1.1, 0.0, px - 0.08, 0.0, 1.0)], 0.2) * kr * 0.9
        rastro += T.tapered([(px - 0.9, 0.0, px - 0.08, 0.0, 1.0)], 0.08) * kr
    t0 = 0.18
    est = T.polys([(estrela(0.02, 0.0, 0.32 * pulso(t, t0, t0 + 0.32) + 0.01, 0.2, 5, 0.45), 1.0)], 0.003) * pulso(t, t0, t0 + 0.32)
    anel = _anel(T, t, t0, t0 + 0.4, 0.1, 0.55, 0.045, 1.0)
    G += (punho * 1.1 + rastro * 0.9 + est * 1.2 + anel) * env
    H += (punho * 0.4 + rastro * 0.5 + est + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Mickey
def _nota(T, cx, cy, s):
    cabeca = T.polys([(_elipse_pts(cx, cy, 0.05 * s, 0.035 * s, -0.4, 12), 1.0)], 0.002)
    haste = T.polyline([(cx + 0.045 * s, cy - 0.01 * s), (cx + 0.045 * s, cy - 0.18 * s), (cx + 0.11 * s, cy - 0.13 * s)], 0.014 * s)
    return cabeca + haste


def soco_musical_mickey(T, t, rng):
    """Mickey: a luva branca de desenho (as três costuras nas costas da mão) vem esticando, borrachuda, e o acerto faz
    pular notinhas musicais que sobem dançando."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.6)
    estica = 1 + 0.4 * pulso(t, 0.1, 0.3)
    px = -0.95 + 0.82 * u - 0.22 * ease_out(rel(t, 0.3, 0.62), 2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.62))
    M, d = _mao(T, px, 0.0, 1.05, 'luva')
    A, _ = _antebraco(T, px, 0.0, 1.05, 0.42 * estica, 0.06)
    corpo = np.clip(M + A, 0, 1) * vis
    costuras = sum(T.polyline([(px - 0.08, -0.06 + 0.05 * k), (px + 0.02, -0.06 + 0.05 * k)], 0.01) for k in range(3)) * vis
    t0 = 0.2
    u2 = rel(t, t0, t0 + 0.7)
    notas = T.zero()
    if 0 < u2 < 1:
        for k in range(4):
            x = -0.2 + 0.15 * k + 0.05 * math.sin(u2 * 10 + k)
            y = -0.1 - 0.5 * u2 - 0.05 * k
            notas += _nota(T, x, y, 1.1 + 0.2 * (k % 2)) * (1 - u2) * (u2 > 0.05 * k)
    puf = _anel(T, t, t0, t0 + 0.35, 0.08, 0.42, 0.045, 1.2)
    est = _estrela_de_contato(T, t, t0, 0.24, 6, 0.4)
    G += (corpo * 1.1 + T.blur(corpo, 0.02) * 0.35 + notas * 1.4 + puf + est) * env
    H += (corpo * 0.6 + costuras * 0.8 + d * vis * 0.4 + notas * 1.0 + puf * 0.4 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Buzz
_MAO_RETA = [(-0.12, -0.08), (0.04, -0.09), (0.36, -0.07), (0.4, -0.03), (0.36, 0.0), (0.04, 0.02), (-0.12, 0.06)]


def golpe_de_carate_buzz(T, t, rng):
    """Buzz Lightyear: a mão reta de caratê sobe e desce de cima num golpe seco (o braço com a faixa roxa do traje),
    e o acerto deixa um risco reto e um brilho de estrelinhas espaciais."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.12), 2)
    desce = ease_in(rel(t, 0.12, 0.24), 2.4)
    ang = -0.9 * sobe + 1.6 * desce - 0.2
    px, py = -0.6 + 0.4 * desce, -0.35 + 0.3 * desce
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.44, 0.6))
    mao = T.polys([(_pts(_MAO_RETA, px, py, 1.5, ang), 1.0)], 0.003)
    braco = T.polys([(_pts([(-0.12, -0.08), (-0.55, -0.1), (-0.55, 0.1), (-0.12, 0.07)], px, py, 1.5, ang), 0.85)], 0.003)
    faixa = T.polyline(_pts([(-0.3, -0.1), (-0.3, 0.1)], px, py, 1.5, ang), 0.03)
    corpo = np.clip(mao + braco, 0, 1) * vis
    t0 = 0.24
    risco = T.zero()
    kr = janela(t, t0, t0 + 0.04) * (1 - rel(t, t0 + 0.2, t0 + 0.4))
    if kr > 0:
        risco = T.tapered([(-0.35, -0.3, 0.3, 0.25, 1.0)], 0.04) * kr
    brilhos = T.zero()
    kb = pulso(t, t0, t0 + 0.5)
    if kb > 0:
        for k in range(5):
            a = TAU * k / 5 + 0.4
            dd = 0.2 + 0.2 * rel(t, t0, t0 + 0.5)
            brilhos += T.polys([(estrela(dd * math.cos(a), dd * math.sin(a), 0.05, 0.0, 4, 0.25), 1.0)], 0.002)
        brilhos *= kb
    est = _estrela_de_contato(T, t, t0, 0.26, 6, 0.3, 0.5, 0.26)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + risco * 1.3 + brilhos * 1.4 + est) * env
    H += (corpo * 0.35 + faixa * vis * 1.0 + risco * 1.0 + brilhos * 1.1 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Woody
def soco_do_xerife(T, t, rng):
    """Woody: o soco de pano do xerife de brinquedo, com o punho da camisa xadrez, e no acerto a estrela de xerife
    aparece brilhando e girando por cima do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.22, 0.2, 1.05, faixa=(0.05, 0.12))
    xadrez = T.zero()
    if vis > 0.05:
        x0 = px - 0.08 - 0.05
        xadrez = (T.lines([(x0 - 0.12 + 0.04 * k, -0.15, x0 - 0.12 + 0.04 * k, 0.15, 1.0) for k in range(4)], 0.008)
                  + T.lines([(x0 - 0.14, -0.06 + 0.06 * k, x0, -0.06 + 0.06 * k, 1.0) for k in range(3)], 0.008)) * vis
    t0 = 0.22
    ke = pulso(t, t0, t0 + 0.62)
    xerife = T.zero()
    if ke > 0:
        r = 0.32 * (0.6 + 0.4 * ke)
        xerife = T.polys([(estrela(0.0, -0.05, r, t * 3, 6, 0.55), 1.0)], 0.003) * ke
        pontas = sum(T.gauss(r * math.cos(t * 3 + TAU * k / 6), -0.05 + r * math.sin(t * 3 + TAU * k / 6), 0.018) for k in range(6)) * ke
    else:
        pontas = T.zero()
    est = _estrela_de_contato(T, t, t0, 0.22, 8, 0.4)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + xerife * 1.3 + est) * env
    H += (corpo * 0.3 + (d + B) * 0.7 + xadrez * 0.8 + xerife * 0.5 + pontas * 1.8 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Gelado
def soco_de_rampa_de_gelo(T, t, rng):
    """Gelado: ele vem deslizando numa rampa de gelo que se forma embaixo do punho (a faixa curva de gelo com o brilho
    da borda) e o soco acerta frio, soltando cristais."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.22), 1.4)
    px = -0.95 + 0.82 * u - 0.18 * ease_out(rel(t, 0.3, 0.62), 2)
    py = -0.15 * math.sin(math.pi * u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, py, 1.05)
    A, _ = _antebraco(T, px, py, 1.05, 0.4, 0.1)
    corpo = np.clip(M + A, 0, 1) * vis
    rampa = T.zero()
    kr = janela(t, 0.0, 0.06) * apaga(t, 0.4, 0.75)
    if kr > 0:
        pts = []
        for s in np.linspace(0, max(0.02, u), 24):
            x = -0.95 + 0.82 * s
            pts.append((x, -0.15 * math.sin(math.pi * s) + 0.2))
        rampa = T.polyline(pts, 0.05) * kr
        rampa += T.polyline([(x, y - 0.03) for x, y in pts], 0.012) * kr * 0.8
    t0 = 0.22
    cristais = T.zero()
    kc = pulso(t, t0, t0 + 0.5)
    if kc > 0:
        segs = []
        for j in range(8):
            a = TAU * j / 8 + 0.2
            comp = 0.18 + 0.2 * rel(t, t0, t0 + 0.2)
            segs.append((comp * math.cos(a), comp * math.sin(a), 0.06 * math.cos(a), 0.06 * math.sin(a), 1.0))
        cristais = T.tapered(segs, 0.05) * kc
    clarao = T.gauss(0, 0, 0.14) * pulso(t, t0, t0 + 0.16) * 1.8
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + rampa * 1.2 + cristais * 1.3 + clarao) * env
    H += (corpo * 0.35 + d * vis * 0.7 + rampa * 0.8 + cristais * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Iroh
def palma_de_fogo_iroh(T, t, rng):
    """Iroh: a palma aberta empurra calma e a chama sai dela girando mansa, em espiral, como o fogo do dragão que é
    vida e não raiva; o acerto acende uma flor de fogo pequena e quente."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = -0.62 + 0.2 * ease_out(rel(t, 0.0, 0.2), 2)
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, 0.55, 0.7))
    palma = T.polys([(_elipse_pts(px, 0.0, 0.1, 0.13, 0.0, 16), 1.0)] + [(_elipse_pts(px + 0.12, -0.09 + 0.06 * k, 0.07, 0.025, 0.0, 10), 1.0) for k in range(4)], 0.003)
    braco = T.polys([([(px - 0.1, -0.08), (px - 0.5, -0.1), (px - 0.5, 0.1), (px - 0.1, 0.08)], 0.85)], 0.003)
    corpo = np.clip(palma + braco, 0, 1) * vis
    espiral = T.zero()
    ke = pulso(t, 0.1, 0.45)
    if ke > 0:
        uu = rel(t, 0.1, 0.45)
        pts = []
        for s in np.linspace(0, 1, 40):
            x = px + 0.15 + (0.0 - px - 0.15) * s * uu
            a = s * 12 + t * 10
            pts.append((x, 0.13 * math.sin(a) * (1 - s * 0.4)))
        espiral = T.polyline(pts, 0.05) * ke
    t0 = 0.4
    flor = T.zero()
    kf = pulso(t, t0, t0 + 0.45)
    if kf > 0:
        segs = []
        for j in range(8):
            a = TAU * j / 8 + t * 2
            r = 0.1 + 0.14 * kf
            segs.append((0.04 * math.cos(a), 0.04 * math.sin(a), r * math.cos(a + 0.4), r * math.sin(a + 0.4), 1.0))
        flor = T.tapered(segs, 0.06) * kf
    calor = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.3) * 1.5
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.4 + espiral * 1.3 + flor * 1.4 + calor) * env
    H += (corpo * 0.3 + espiral * 0.7 + flor * 0.6 + calor * 1.0) * env
    return G, H


# ------------------------------------------------------------------ Destruidor
def soco_de_laminas_destruidor(T, t, rng):
    """Destruidor: a manopla com as três lâminas presas no antebraço vem num soco e as lâminas riscam o alvo de
    passagem, deixando três cortes finos e retos com faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.2, 0.18, 1.05, 'armadura')
    laminas = T.zero()
    if vis > 0.05:
        polys = []
        for k in range(3):
            y = -0.13 - 0.05 * k
            polys.append(([(px - 0.35, y + 0.015), (px + 0.12 + 0.04 * k, y - 0.03 - 0.02 * k), (px - 0.35, y - 0.015)], 1.0))
        laminas = T.polys(polys, 0.002) * vis
    t0 = 0.2
    cortes = T.zero()
    kc = janela(t, t0, t0 + 0.04) * (1 - rel(t, t0 + 0.25, t0 + 0.45))
    if kc > 0:
        segs = [(-0.3, -0.28 + 0.1 * k, 0.32, -0.1 + 0.1 * k, 1.0) for k in range(3)]
        cortes = T.tapered(segs, 0.022) * kc
    faiscas = _riscos(T, t, t0, 0.35, 9, 0.15, 0.48, 0.02, 53, -1.5, 1.5)
    est = _estrela_de_contato(T, t, t0, 0.24, 6, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + laminas * 1.2 + cortes * 1.4 + faiscas * 1.3 + est) * env
    H += (corpo * 0.3 + d * 0.7 + laminas * 1.0 + cortes * 1.1 + faiscas * 0.9 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Casey Jones
def soco_de_hoquei(T, t, rng):
    """Casey Jones: a luva grossa de hóquei (dedos acolchoados) dá o soco e o disco de hóquei sai voando do acerto,
    girando para fora da tela, como um "gol"."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.18, 1.2, 'manopla', faixa=(0.0, 0.14))
    acolchoado = T.zero()
    if vis > 0.05:
        acolchoado = sum(T.polyline([(px - 0.02, -0.2 + 0.1 * k), (px + 0.16, -0.2 + 0.1 * k)], 0.01) for k in range(1, 4)) * vis
    t0 = 0.2
    u = rel(t, t0 + 0.02, t0 + 0.45)
    disco = T.zero()
    if 0 < u < 1:
        x, y = 0.15 + 0.8 * ease_out(u, 1.5), -0.1 - 0.25 * math.sin(math.pi * u)
        larg = 0.14
        disco = T.polys([(_elipse_pts(x, y, larg, 0.055, 0.2, 16), 1.0)], 0.003) * (1 - u ** 3)
        disco += T.tapered([(x - 0.4, y + 0.05, x - 0.08, y, 1.0)], 0.04) * (1 - u) * 0.8
    est = _estrela_de_contato(T, t, t0, 0.3, 8, 0.36)
    onda = _anel(T, t, t0, t0 + 0.4, 0.1, 0.5, 0.045, 1.2)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + disco * 1.4 + est + onda) * env
    H += (corpo * 0.3 + (d + B) * 0.6 + acolchoado * 0.9 + disco * 0.6 + est * 0.9 + onda * 0.4) * env
    return G, H


REGISTRO = [
    ("soco_superpoderosa", soco_superpoderosa, GRANDE, "básico da Docinho: o punhinho voando com o rastro de cor", False),
    ("soco_musical_mickey", soco_musical_mickey, GRANDE, "básico do Mickey: a luva branca e as notinhas musicais", False),
    ("golpe_de_carate_buzz", golpe_de_carate_buzz, GRANDE, "básico do Buzz: a mão reta de caratê caindo de cima", False),
    ("soco_do_xerife", soco_do_xerife, GRANDE, "básico do Woody: o punho xadrez e a estrela de xerife", False),
    ("soco_de_rampa_de_gelo", soco_de_rampa_de_gelo, GRANDE, "básico do Gelado: deslizando na rampa de gelo", False),
    ("palma_de_fogo_iroh", palma_de_fogo_iroh, GRANDE, "básico do Iroh: a palma aberta e a chama em espiral", False),
    ("soco_de_laminas_destruidor", soco_de_laminas_destruidor, GRANDE, "básico do Destruidor: a manopla de lâminas e os três cortes", False),
    ("soco_de_hoquei", soco_de_hoquei, GRANDE, "básico do Casey Jones: a luva de hóquei e o disco voando", False),
]
