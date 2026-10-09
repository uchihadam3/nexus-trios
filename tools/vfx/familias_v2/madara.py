"""As três técnicas do Madara Uchiha, desenhadas para ele.

Pedido do jogador: "faz as três do Madara muito bem feitas… o meteoro grande,
caindo no meio, pegando todo mundo… quando ele usar o Susanoo, aparecer nele".

- susanoo_perfeito: a espada do Susanoo desce num corte enorme e as chamas de
  chakra azul sobem do corte (no rival).
- susanoo_manto: a armadura espectral em volta do Madara — costelas, a máscara
  de nariz de tengu, os ombros e as asas, tudo em chamas de chakra (nele).
- meteoro_madara: a rocha gigante cai do alto com a cauda de fogo, a sombra cresce
  no chão e ela explode no meio dos rivais (uma vez, no centro do grupo).
- mugen_tsukuyomi: a lua vermelha com o Rinne Sharingan sobe, pulsa, e os raios de
  luz descem nos três rivais, que ficam presos nos casulos de raízes.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, janela, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _chama(cx, base, alt, larg, fase, ondula=0.3):
    """Língua de chakra: gota que afina para cima, com a ponta balançando."""
    pts = []
    for lado in (1, -1):
        rng = range(13) if lado == 1 else range(12, -1, -1)
        for k in rng:
            u = k / 12
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, base - alt * u))
    return pts


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.8, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.5
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.6 * k + 0.01, ang=ang + math.pi / 2, thin=0.012)) * k * 1.6
    return g, h


# ------------------------------------------------------------------ Susanoo Perfeito (no rival)
def susanoo_perfeito(T, t, rng):
    """A espada do Susanoo: a lâmina enorme surge no alto, desce num corte diagonal que cruza a
    tela, o clarão do impacto, e chamas de chakra azul sobem por toda a linha do corte."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    # a lâmina: aparece no alto à esquerda e gira para baixo
    surge = janela(t, 0.0, 0.1)
    desce = ease_in(rel(t, 0.1, 0.36), 1.8)
    ang = -1.25 + 1.95 * desce                    # a lâmina erguida no alto desce até cruzar o centro
    piv = (-1.15, -0.45)                          # o punho fica fora da tela, à esquerda (é o Susanoo, gigante)
    comp = 2.1
    ponta = (piv[0] + math.cos(ang) * comp, piv[1] + math.sin(ang) * comp)
    vis = surge * (1 - rel(t, 0.42, 0.56))
    lam = T.polys([(lamina(piv[0] + math.cos(ang) * 0.3, piv[1] + math.sin(ang) * 0.3, ponta[0], ponta[1], 0.11), 1.0)], 0.006) * vis
    gume = T.polyline([(piv[0] + math.cos(ang) * 0.55, piv[1] + math.sin(ang) * 0.55), ponta], 0.012) * vis
    # o arco que a lâmina varre
    arco = T.arc_band(comp - 0.3, 0.17, -1.25, ang + 0.01, cx=piv[0], cy=piv[1], taper=1.2) * pulso(t, 0.12, 0.5) if desce > 0.02 else T.zero()
    # o corte que fica: uma linha diagonal brilhante que se abre
    corte_k = janela(t, 0.34, 0.38) * (1 - rel(t, 0.62, 0.9))
    corte = T.polys([(lamina(-0.95, -0.55, 0.95, 0.6, 0.05 + 0.04 * rel(t, 0.36, 0.6)), 1.0)], 0.006) * corte_k
    k = pulso(t, 0.34, 0.62)
    g, h = _clarao(T, k, 0.0, 0.03, 0.34, 1.1, 0.55)
    # chamas de chakra sobem ao longo da linha do corte
    sub = np.random.default_rng(88)
    chamas = []
    for j in range(11):
        u = j / 10
        x, y = -0.85 + 1.7 * u, -0.5 + 1.05 * u
        a0 = 0.38 + 0.025 * j
        alt = 0.42 * ease_out(rel(t, a0, a0 + 0.18), 2) * (0.75 + 0.35 * abs(math.sin(t * 25 + j * 1.7)))
        if alt > 0.02:
            chamas.append((_chama(x, y + 0.05, alt, 0.09 + 0.03 * sub.uniform(), t * 30 + j * 1.3, 0.5), 0.8))
    C = T.polys(chamas, 0.012) * (1 - rel(t, 0.74, 0.95))
    # estilhaços
    fa = []
    for _ in range(18):
        a = sub.uniform(-math.pi, math.pi)
        d = 0.15 + 0.7 * ease_out(rel(t, 0.36, 0.8), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a), d * math.sin(a) + 0.2 * rel(t, 0.4, 1) ** 2, pulso(t, 0.36, 0.9) * sub.uniform(0.4, 1)))
    F = T.splats(fa, 0.013)
    G += (lam * 1.1 + T.blur(lam, 0.03) * 0.9 + gume * 0.6 + arco * 0.9 + corte * 1.3 + T.blur(corte, 0.03) + g + C * 1.2 + T.blur(C, 0.02) * 0.6 + F * 1.4) * env
    H += (lam * 0.5 + gume * 1.4 + arco * 0.3 + corte * 1.5 + h + C * 0.35 + F) * env
    return G, H


# ------------------------------------------------------------------ Susanoo em volta do Madara
def _costela(cx, cy, r, a0, a1, larg, n=14):
    fora, dentro = [], []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        w = larg * (0.55 + 0.45 * math.sin(math.pi * k / n))
        fora.append((cx + math.cos(a) * (r + w), cy + math.sin(a) * (r + w) * 0.8))
        dentro.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.8))
    return fora + dentro[::-1]


def susanoo_manto(T, t, rng):
    """O Susanoo em volta do Madara: as costelas se fecham dos dois lados, a cabeça com a máscara
    de nariz de tengu e os chifres surge acima, os ombros e as asas atrás — e tudo arde em chamas
    de chakra que tremem (em laço, enquanto ele prepara)."""
    G, H = vazio(T)
    fase = t * TAU
    # costelas: arcos dos dois lados do corpo
    formas = []
    for k in range(4):
        y = 0.05 + 0.13 * k
        r = 0.36 - 0.03 * k
        formas.append((_costela(0.0, y, r, -math.pi * 0.95, -math.pi * 0.55, 0.035), 1.0))
        formas.append((_costela(0.0, y, r, -math.pi * 0.45, -math.pi * 0.05, 0.035), 1.0))
    costelas = T.polys(formas, 0.006)
    # coluna
    coluna = T.polyline([(0.0, -0.15), (0.0, 0.6)], 0.03)
    # cabeça: crânio com a máscara de tengu (nariz comprido para a frente) e dois chifres
    cabeca = [(-0.17, -0.38), (-0.2, -0.55), (-0.12, -0.7), (0.0, -0.74), (0.12, -0.7), (0.2, -0.55), (0.17, -0.38), (0.05, -0.3), (-0.05, -0.3)]
    nariz = [(0.06, -0.52), (0.38, -0.47), (0.06, -0.44)]
    chifres = [[(-0.1, -0.7), (-0.2, -0.95), (-0.04, -0.73)], [(0.1, -0.7), (0.2, -0.95), (0.04, -0.73)]]
    olhos = T.gauss(-0.07, -0.56, 0.025, 0.018) + T.gauss(0.08, -0.56, 0.025, 0.018)
    C = T.polys([(cabeca, 1.0), (nariz, 1.0)] + [(c, 1.0) for c in chifres], 0.006)
    # ombros e asas
    ombros = T.polys([([(-0.62, -0.18), (-0.2, -0.3), (-0.2, -0.16), (-0.58, -0.04)], 0.9), ([(0.62, -0.18), (0.2, -0.3), (0.2, -0.16), (0.58, -0.04)], 0.9)], 0.006)
    asas = T.zero()
    for lado in (-1, 1):
        for k in range(4):
            a = -math.pi / 2 + lado * (0.6 + 0.28 * k)
            comp = 0.75 - 0.08 * k + 0.03 * math.sin(fase * 2 + k)
            asas += T.polys([(lamina(lado * 0.4, -0.22, lado * 0.4 + math.cos(a) * comp * lado * -1 * -1 if False else lado * (0.4 + 0.55 - 0.08 * k), -0.22 - comp * 0.75 + 0.12 * k, 0.05), 0.7)], 0.01)
    # chamas de chakra em volta da silhueta
    chamas = []
    for k in range(16):
        x = -0.72 + 1.44 * k / 15
        alt = (0.75 + 0.25 * math.cos(x * 2.2)) * (0.8 + 0.2 * math.sin(fase * 3 + k * 1.9))
        chamas.append((_chama(x, 0.75, alt * 1.15, 0.13, fase * 2 + k * 1.3, 0.5), 0.5))
    Ch = T.polys(chamas, 0.02)
    corpo = np.clip(costelas + coluna * 0.7 + C + ombros * 0.8 + asas, 0, 1)
    brilho = 0.85 + 0.15 * math.sin(fase * 2)
    G += (Ch * 0.75 + T.blur(corpo, 0.03) * 0.9 + corpo * 0.9) * brilho
    H += (corpo * 0.45 + olhos * 2.0 + Ch * 0.12) * brilho
    return G, H


# ------------------------------------------------------------------ Meteoro (no centro dos rivais)
def _rocha(cx, cy, r, giro, sub):
    pts = []
    for k in range(20):
        a = giro + TAU * k / 20
        rr = r * (0.9 + 0.07 * math.sin(k * 1.3 + 0.5) + 0.04 * math.cos(k * 2.2))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def meteoro_madara(T, t, rng):
    """O Meteoro do Madara: a rocha gigante desce do alto com a cauda de fogo, a sombra no chão
    cresce embaixo dela, e ela cai no meio dos rivais — clarão, domo de explosão, onda de choque
    larga no chão, pedras voando e a poeira subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    chao = 0.42
    cai = ease_in(rel(t, 0.0, 0.46), 1.7)
    mx, my = -0.7 + 0.7 * cai, -1.25 + (chao - 0.05 + 1.25) * cai
    R = 0.46
    sub = np.random.default_rng(1915)
    vis = 1 - rel(t, 0.45, 0.5)
    rocha = T.polys([(_rocha(mx, my, R, t * 3, sub), 1.0)], 0.01) * vis
    crateras = (T.gauss(mx - 0.1, my - 0.08, 0.06) + T.gauss(mx + 0.12, my + 0.05, 0.05) + T.gauss(mx - 0.02, my + 0.14, 0.04)) * vis
    # a cauda de fogo atrás da rocha (para cima e para a esquerda)
    # a cauda de fogo: línguas largas que saem de trás da rocha, para cima e para a esquerda
    lingua = []
    for k in range(7):
        off = (k - 3) * 0.11
        comp = 0.75 + 0.2 * math.sin(t * 30 + k)
        lingua.append((_gira(_chama(0.0, 0.0, comp, 0.13, t * 25 + k, 0.4), -0.75 + off * 0.4, mx - 0.12 + off * 0.3, my - 0.1), 0.9))
    C = T.polys(lingua, 0.02) * vis * janela(t, 0.02, 0.1)
    sombra = T.gauss(0.0, chao + 0.1, 0.15 + 0.5 * cai, 0.03 + 0.07 * cai) * janela(t, 0.05, 0.2) * (1 - rel(t, 0.46, 0.54)) * 0.7
    # a explosão
    k = pulso(t, 0.46, 0.8)
    ex = rel(t, 0.46, 0.88)
    raio_d = 0.18 + 0.32 * ease_out(ex, 2)
    domo = T.polys([([(math.cos(a) * raio_d * 1.5, chao - math.sin(a) * raio_d * 1.2) for a in np.linspace(0, math.pi, 24)], 1.0)], 0.06) * k * 1.4
    g, h = _clarao(T, k, 0.0, chao - 0.05, 0.22, 1.2, 0.0)
    onda = T.ring(0.15 + 0.85 * ease_out(rel(t, 0.46, 0.88), 2.2), 0.05, cy=chao + 0.1, squash=3.2) * pulso(t, 0.46, 0.92) * 1.4
    pedras = []
    for _ in range(14):
        a = sub.uniform(-math.pi * 0.95, -math.pi * 0.05)
        v = sub.uniform(0.5, 1.1)
        tt = rel(t, 0.47, 0.97)
        x = math.cos(a) * v * tt * 1.1
        y = chao + math.sin(a) * v * tt * 1.3 + 1.6 * tt * tt
        if tt > 0:
            pedras.append((_rocha(x, y, 0.03 + 0.04 * sub.uniform(), tt * 9, sub), (1 - tt) ** 0.6))
    P = T.polys(pedras, 0.004) if pedras else T.zero()
    poeira = []
    for _ in range(16):
        x = sub.uniform(-0.95, 0.95)
        tt = rel(t, 0.45 + 0.1 * abs(x), 1.0)
        poeira.append((x * (1 + 0.2 * tt), chao + 0.05 - 0.35 * ease_out(tt, 2) * sub.uniform(0.3, 1), (1 - tt) ** 1.2 * (tt > 0) * 0.5))
    Po = T.blur(T.splats(poeira, 0.08), 0.03)
    G += (rocha * 1.0 + C * 1.3 + T.blur(C, 0.03) * 0.8 + sombra + domo + g + onda + P * 1.2 + Po * 0.7) * env
    H += (rocha * 0.25 - crateras * 0.0 + C * 0.9 + domo * 0.7 + h + onda * 0.5 + P * 0.5 + Po * 0.1) * env
    G -= crateras * 0.5 * env
    return np.clip(G, 0, None), H


# ------------------------------------------------------------------ Mugen Tsukuyomi (no centro dos rivais)
def mugen_tsukuyomi(T, t, rng):
    """Mugen Tsukuyomi: a lua cheia sobe no alto e vira o Rinne Sharingan (anéis concêntricos com
    os nove tomoe), pulsa, e três raios de luz descem nos rivais; no chão, as raízes da árvore
    sobem em espiral e fecham cada um num casulo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2)
    lx, ly = 0.0, -1.0 + 0.5 * sobe
    R = 0.44
    lua = T.gauss(lx, ly, R * 0.7, R * 0.7) * janela(t, 0.0, 0.12) * 1.1 + T.ring(R, 0.03, cx=lx, cy=ly) * janela(t, 0.0, 0.12)
    olho = janela(t, 0.2, 0.35)
    aneis = sum(T.ring(R * f, 0.012, cx=lx, cy=ly) for f in (0.28, 0.5, 0.72)) * olho
    tomoe = []
    for anel, f in enumerate((0.28, 0.5, 0.72)):
        for k in range(3):
            a = TAU * k / 3 + anel * 0.5 + t * 2.5
            tomoe.append((lx + math.cos(a) * R * f, ly + math.sin(a) * R * f, 1.0))
    Tm = T.splats(tomoe, 0.022) * olho
    pulsa = 1 + 0.15 * math.sin(t * 40) * olho
    # raios descendo nos três rivais
    alvos = [(-0.62, 0.55), (0.0, 0.62), (0.62, 0.55)]
    raios = T.zero()
    raio_k = pulso(t, 0.36, 0.8)
    for i, (ax, ay) in enumerate(alvos):
        u = ease_out(rel(t, 0.36 + 0.04 * i, 0.5 + 0.04 * i), 2)
        if u > 0:
            ex, ey = lx + (ax - lx) * u, ly + (ay - ly) * u
            raios += T.polys([(lamina(lx, ly + R * 0.6, ex, ey, 0.06), 1.0)], 0.02)
    raios *= raio_k
    # casulos de raízes subindo em espiral em volta de cada rival
    casulos = T.zero()
    for i, (ax, ay) in enumerate(alvos):
        u = ease_out(rel(t, 0.5 + 0.03 * i, 0.8), 1.8)
        if u <= 0:
            continue
        for lado in (1, -1):
            pts = []
            for k in range(26):
                v = k / 25 * u
                a = lado * v * 3.2 * math.pi
                pts.append((ax + 0.19 * math.cos(a) * (1 - 0.3 * v), ay + 0.25 - 0.62 * v + 0.04 * math.sin(a)))
            casulos += T.polyline(pts, 0.03)
    casulos *= 1 - rel(t, 0.88, 1.0)
    G += (lua * pulsa * 1.1 + aneis * 1.2 + Tm * 1.4 + T.blur(raios, 0.03) * 1.2 + raios * 0.8 + casulos * 1.2) * env
    H += (lua * 0.25 + aneis * 0.9 + Tm * 1.2 + raios * 0.9 + casulos * 0.5) * env
    G -= Tm * 0.0
    return G, H


REGISTRO = [
    ("susanoo_perfeito", susanoo_perfeito, GRANDE, "Susanoo Perfeito do Madara: a espada gigante desce e o chakra azul arde no corte", False),
    ("susanoo_manto", susanoo_manto, GRANDE, "O Susanoo em volta do Madara: costelas, máscara de tengu, asas e chamas de chakra", True),
    ("meteoro_madara", meteoro_madara, GRANDE, "Meteoro do Madara: a rocha gigante cai em fogo no meio dos rivais e explode", False),
    ("mugen_tsukuyomi", mugen_tsukuyomi, GRANDE, "Mugen Tsukuyomi: a lua do Rinne Sharingan, os raios e os casulos de raízes", False),
]
