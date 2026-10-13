"""Rodada 57 das habilidades próprias: Bakugo, Todoroki, Mob, Rimuru, Ainz e Lelouch.

Bakugo
- explosao_bakugo: a palma aberta e a explosão laranja estourando no rival, com a fumaça (Queimando).
- granada_bakugo: a manopla de granada, o projétil e a bomba marcada no rival piscando (Marca explosiva).
- bakugo_preparo: o Preparo do Howitzer Impact — o corpo girando no ar, empurrado pelas explosões (laço).
- howitzer_impact: o tornado de explosões descendo em espiral e a explosão gigante em todos os rivais.

Todoroki
- muralha_de_gelo_todoroki: a geleira subindo pelo chão em pontas até o rival (Congelado).
- chama_esquerda: o jato de fogo da mão esquerda até o rival (Queimando).
- todoroki_preparo: o Preparo do Ponto de fusão — metade gelo, metade fogo em volta dele (laço).
- ponto_de_fusao: o gelo cobrindo o chão, o fogo por cima e a explosão de vapor em todos os rivais (Queimando e Lento).

Mob
- telecinese_mob: as pedras flutuando e voando no rival; a barra de energia enchendo.
- barreira_psiquica_mob: a cúpula psíquica brilhando em volta dele; a barra de energia enchendo.
- mob_preparo: o Preparo do 100% — a aura subindo, as pedras flutuando e o "%" piscando (laço).
- cem_por_cento: a coluna de energia explodindo para o alto e as ondas psíquicas em todos os rivais.

Rimuru
- devorar_rimuru: o slime abrindo a boca e engolindo a bolinha de luz do rival (copia a habilidade).
- grande_sabio: os painéis de luz do Grande Sábio aparecendo em cima do trio (Fortalecido).
- rimuru_preparo: o Preparo do Corte de água — as gotas girando e a lâmina de água se formando (laço).
- corte_de_agua: a lâmina fina de água em alta pressão cortando e os respingos.

Ainz
- toque_da_morte_ainz: a mão de esqueleto agarrando o rival e o selo da maldição (Amaldiçoado).
- invocar_mortos: o círculo de magia no chão e o Cavaleiro da Morte subindo com o escudo e a espada (Enfraquecido).
- ainz_preparo: o Preparo do O Goal of All Life Is Death — a caveira de olhos vermelhos e as runas girando (laço).
- o_fim_de_toda_vida: o relógio gigante, o ponteiro dando a volta e a onda da morte em todos os rivais (Amaldiçoado).

Lelouch
- geass_lelouch: o selo do Geass (o pássaro) saindo do olho e entrando no olho do rival (Confuso e Silenciado).
- xadrez: o tabuleiro sob o trio e as peças avançando (Fortalecido e o próximo ataque adiantado).
- lelouch_preparo: o Preparo do Xeque-mate — o rei do xadrez girando com o selo do Geass (laço).
- xeque_mate: o rei avançando no tabuleiro, o rei rival tombando e o feixe roxo (Enfraquecido).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (CHAMA, GOTA, anel, clarao, corte, estouro, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _bum(T, t, a, b, cx, cy, tam, seed, forca=1.0):
    """Uma explosão: a bola de fogo que incha, as nuvens de fumaça em volta e os estilhaços. Devolve (G, H)."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0, 0.0
    q = np.random.default_rng(seed)
    r = tam * ease_out(u, 2.5)
    k = (1 - u) * forca
    G = T.gauss(cx, cy, r * 0.6 + 0.01) * k * 1.4
    for j in range(7):
        a2 = TAU * j / 7 + q.uniform(-0.3, 0.3)
        d = r * q.uniform(0.6, 0.95)
        G += T.ring(r * 0.32 + 0.005, r * 0.08 + 0.003, cx + d * math.cos(a2), cy + d * math.sin(a2) * 0.8) * k * 0.9
    G += estouro(T, t, a, b, 10, seed, cx, cy, tam * 1.3, 0.012) * forca
    H = T.gauss(cx, cy, r * 0.25 + 0.005) * (1 - ease_in(u, 1.5)) * 1.8 * forca
    return G, H


def _palma(T, x, y, s, k):
    """A mão aberta virada para a frente (a palma do Bakugo): os cinco dedos abertos em leque."""
    G = T.gauss(x, y, s * 0.35, s * 0.4) * k * 0.9
    segs = []
    for j in range(5):
        a = -math.pi / 2 - 0.9 + 0.45 * j
        if j == 0:
            a += 0.5
        segs.append((x + s * 0.3 * math.cos(a), y + s * 0.3 * math.sin(a), x + s * 0.85 * math.cos(a), y + s * 0.85 * math.sin(a), 1.0))
    return G + T.lines(segs, s * 0.13) * k * 1.1


def _pico_gelo(T, x, y, h, w, k):
    pts = [(x - w, y), (x - w * 0.3, y - h * 0.7), (x, y - h), (x + w * 0.4, y - h * 0.6), (x + w, y)]
    return icone(T, pts, k * 1.1, 0.5)


def _pedra(T, x, y, s, ang, k):
    pts = [(-0.9, -0.2), (-0.4, -0.85), (0.35, -0.75), (0.9, -0.1), (0.6, 0.7), (-0.3, 0.8), (-0.85, 0.4)]
    return icone(T, poe(pts, x, y, s, ang), k * 1.1, 0.55)


def _barra(T, x, y, w, enche, k):
    """A barra de energia guardada: o contorno e o enchimento."""
    G = T.polyline([(x, y), (x + w, y), (x + w, y - 0.05), (x, y - 0.05), (x, y)], 0.006) * k
    if enche > 0:
        G += T.polys([([(x, y), (x + w * enche, y), (x + w * enche, y - 0.05), (x, y - 0.05)], 1.0)], 0.003) * k * 0.9
    return G


def _porcento(T, x, y, s, k):
    return (T.ring(s * 0.25, s * 0.07, x - s * 0.4, y - s * 0.45) + T.ring(s * 0.25, s * 0.07, x + s * 0.4, y + s * 0.45)) * k * 1.3 + \
        T.lines([(x + s * 0.6, y - s * 0.75, x - s * 0.6, y + s * 0.75, 1.0)], s * 0.09) * k * 1.3


def _slime(T, x, y, s, k, boca=0.0, t=0.0):
    """O slime azul: a gota achatada que balança, os olhos e a boca que abre."""
    pts = []
    for a in np.linspace(0, TAU, 32, endpoint=False):
        r = 1.0 + 0.05 * math.sin(3 * a + t * 10)
        yy = math.sin(a)
        pts.append((x + s * r * math.cos(a), y + s * (0.7 * yy if yy > 0 else 0.85 * yy * (1 + 0.15 * math.cos(a)))))
    g, h = icone(T, pts, k * 1.1, 0.45)
    G = g
    H = h
    for lado in (-1, 1):
        G += T.lines([(x + lado * s * 0.3, y - s * 0.3, x + lado * s * 0.3, y - s * 0.12, 1.0)], s * 0.08) * k * 1.2
    if boca > 0:
        G += T.ring(s * 0.25 * boca, s * 0.05, x + s * 0.1, y + s * 0.2, 1.0 / max(0.3, boca)) * k * 1.3
    return G, H


def _painel(T, x, y, w, h, k, linhas=3):
    G = T.polyline([(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h), (x - w, y - h)], 0.008) * k * 1.2
    G += T.polys([([(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)], 1.0)], 0.003) * k * 0.15
    segs = [(x - w * 0.8, y - h + h * 2 * (j + 1) / (linhas + 1), x - w * 0.8 + w * (1.6 - 0.4 * (j % 2)), y - h + h * 2 * (j + 1) / (linhas + 1), 0.8) for j in range(linhas)]
    return G + T.lines(segs, 0.005) * k


def _mao_osso(T, x, y, s, k, fecha=0.0):
    """A mão de esqueleto do Ainz: os ossos do pulso e os dedos compridos (fecha = 1 é a mão agarrando)."""
    segs = [(x - s * 0.6, y, x - s * 0.15, y, 1.0)]
    for j in range(4):
        b = -0.45 + 0.3 * j
        bx, by = x - s * 0.1, y + s * b * 0.5
        a = b * 0.6 - fecha * 1.2 * (1 if b < 0 else -1) * 0.5
        mx, my = bx + s * 0.35 * math.cos(a), by + s * 0.35 * math.sin(a)
        a2 = a + fecha * 1.3 * (1 if b >= 0 else -1) * -1 + fecha * (0.6 if b < 0 else -0.6)
        segs += [(x - s * 0.15, y, bx, by, 1.0), (bx, by, mx, my, 1.0), (mx, my, mx + s * 0.25 * math.cos(a2), my + s * 0.25 * math.sin(a2), 1.0)]
    G = T.lines(segs, s * 0.06) * k * 1.2
    nos = [(px, py, 1.0) for (_, _, px, py, _) in segs[1:]]
    return G, T.splats(nos, s * 0.03) * k


def _cavaleiro(T, x, y, s, k):
    """O Cavaleiro da Morte: o elmo com chifres, o escudo de torre e a espada flamejante."""
    G, H = 0.0, 0.0
    corpo = [(-0.35, 1.0), (-0.45, 0.1), (-0.3, -0.45), (0.3, -0.45), (0.45, 0.1), (0.35, 1.0)]
    g, h = icone(T, poe(corpo, x, y, s), k, 0.4)
    G, H = G + g, H + h
    elmo = [(-0.2, -0.45), (-0.25, -0.75), (0.0, -0.85), (0.25, -0.75), (0.2, -0.45)]
    g, h = icone(T, poe(elmo, x, y, s), k * 1.2, 0.6)
    G, H = G + g, H + h
    for lado in (-1, 1):
        G += T.polyline([(x + lado * s * 0.2, y - s * 0.75), (x + lado * s * 0.4, y - s * 0.95), (x + lado * s * 0.35, y - s * 1.1)], s * 0.04) * k * 1.2
        H += T.gauss(x + lado * s * 0.09, y - s * 0.66, s * 0.03) * k * 2.0
    escudo = [(-0.95, -0.3), (-0.45, -0.35), (-0.45, 0.65), (-0.7, 0.85), (-0.95, 0.65)]
    g, h = icone(T, poe(escudo, x, y, s), k * 1.1, 0.5)
    G, H = G + g, H + h
    pts = [(x + s * (0.55 + 0.05 * math.sin(u * 20)), y + s * (0.3 - 1.4 * u)) for u in np.linspace(0, 1, 18)]
    G += T.polyline(pts, s * 0.05) * k * 1.2
    return G, H


def _caveira_ainz(T, x, y, s, k, olho=1.0):
    G = T.ring(s, s * 0.06, x, y - s * 0.1, 0.95) * k * 1.2
    G += T.polyline([(x - s * 0.55, y + s * 0.5), (x - s * 0.4, y + s * 0.9), (x + s * 0.4, y + s * 0.9), (x + s * 0.55, y + s * 0.5)], s * 0.06) * k
    G += T.lines([(x - s * 0.3 + s * 0.15 * j, y + s * 0.7, x - s * 0.3 + s * 0.15 * j, y + s * 0.9, 1.0) for j in range(5)], s * 0.03) * k
    H = 0.0
    for lado in (-1, 1):
        G += T.ring(s * 0.22, s * 0.05, x + lado * s * 0.38, y - s * 0.05) * k
        H += T.gauss(x + lado * s * 0.38, y - s * 0.05, s * 0.07) * k * olho * 2.2
    return G, H


def _passaro_geass(T, x, y, s, k, ang=0.0):
    """O selo do Geass: o pássaro de asas abertas."""
    pts = [(0, -0.2), (0.25, -0.45), (0.55, -0.55), (1.0, -0.35), (0.6, -0.25), (0.85, -0.05), (0.4, -0.05), (0.15, 0.15), (0.12, 0.6),
           (0, 0.85), (-0.12, 0.6), (-0.15, 0.15), (-0.4, -0.05), (-0.85, -0.05), (-0.6, -0.25), (-1.0, -0.35), (-0.55, -0.55), (-0.25, -0.45)]
    return icone(T, poe(pts, x, y, s, ang), k * 1.3, 0.75)


_REI = [(-0.45, 1.0), (0.45, 1.0), (0.35, 0.8), (0.2, 0.75), (0.25, 0.0), (0.4, -0.15), (0.3, -0.35), (0.15, -0.45), (0.15, -0.6),
        (0.3, -0.6), (0.3, -0.72), (0.08, -0.72), (0.08, -0.95), (-0.08, -0.95), (-0.08, -0.72), (-0.3, -0.72), (-0.3, -0.6), (-0.15, -0.6),
        (-0.15, -0.45), (-0.3, -0.35), (-0.4, -0.15), (-0.25, 0.0), (-0.2, 0.75), (-0.35, 0.8)]
_PEAO = [(-0.4, 1.0), (0.4, 1.0), (0.3, 0.8), (0.15, 0.7), (0.2, 0.2), (0.35, 0.05), (0.2, -0.1), (0.3, -0.35), (0.0, -0.6), (-0.3, -0.35),
         (-0.2, -0.1), (-0.35, 0.05), (-0.2, 0.2), (-0.15, 0.7), (-0.3, 0.8)]


def _tabuleiro(T, cx, cy, w, k, n=6):
    """O tabuleiro de xadrez visto deitado (as casas claras acesas)."""
    G = 0.0
    polys = []
    for i in range(n):
        for j in range(n):
            if (i + j) % 2:
                continue
            x0, x1 = cx - w + 2 * w * i / n, cx - w + 2 * w * (i + 1) / n
            y0, y1 = cy - w * 0.25 + 0.5 * w * j / n, cy - w * 0.25 + 0.5 * w * (j + 1) / n
            sh = 0.25 * (j / n - 0.5)
            polys.append(([(x0 + sh * x0, y0), (x1 + sh * x1, y0), (x1 + sh * x1, y1), (x0 + sh * x0, y1)], 1.0))
    G += T.polys(polys, 0.003) * k * 0.45
    G += T.polyline([(cx - w * 0.9, cy - w * 0.25), (cx + w * 0.9, cy - w * 0.25), (cx + w * 1.1, cy + w * 0.25), (cx - w * 1.1, cy + w * 0.25),
                     (cx - w * 0.9, cy - w * 0.25)], 0.008) * k
    return G


# ------------------------------------------------------------------ Bakugo

def explosao_bakugo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.2), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        G += _palma(T, -0.55 + 0.25 * u, -0.05, 0.38, k)
        H += T.gauss(-0.25 * u - 0.5 + 0.25, -0.05, 0.03) * pulso(t, 0.1, 0.3) * 2.0
    g, h = _bum(T, t, 0.2, 0.75, 0.45, -0.05, 0.42, 571)
    G, H = G + g, H + h
    g, h = _bum(T, t, 0.28, 0.8, 0.6, -0.2, 0.22, 572, 0.8)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.2, 0.42, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    q = pulso(t, 0.5, 1.0)
    if q > 0:
        for j in range(3):
            g, h = icone(T, poe(CHAMA, 0.35 + 0.1 * j, 0.12 - 0.04 * (j % 2), 0.07 + 0.015 * math.sin(t * 25 + j)), q, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.45, 1.0, 16, 573, 0.45, -0.1, 0.3, 0.6, 0.02)
    return G * env, H * env


def granada_bakugo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.6, 0.75))
    if k > 0:
        # a manopla em forma de granada no braço
        man = [(-0.75, -0.12), (-0.45, -0.18), (-0.38, -0.08), (-0.38, 0.08), (-0.45, 0.18), (-0.75, 0.12)]
        g, h = icone(T, man, k * 1.2, 0.6)
        G, H = G + g, H + h
        G += T.lines([(-0.7 + 0.08 * j, -0.13, -0.7 + 0.08 * j, 0.13, 1.0) for j in range(4)], 0.008) * k
        G += T.ring(0.04, 0.01, -0.48, -0.22) * k * pulso(t, 0.0, 0.3) * 1.3
    u = rel(t, 0.2, 0.45)
    if 0 < u < 1:
        x = -0.35 + 0.8 * ease_in(u, 1.3)
        y = -0.05 - 0.15 * math.sin(math.pi * u)
        G += T.ring(0.035, 0.012, x, y) * 1.3 + T.tapered([(x - 0.3, y + 0.05 * u, x, y, 0.8)], 0.025)
        H += T.gauss(x, y, 0.015) * 1.8
    g, h = _bum(T, t, 0.43, 0.75, 0.45, -0.05, 0.3, 574)
    G, H = G + g, H + h
    # a bomba marcada no rival, piscando (Marca explosiva)
    m = surge(t, 0.5, 0.68) * (1 - rel(t, 0.9, 1))
    if m > 0:
        pis = 0.6 + 0.4 * (1 if (t * 8) % 1 < 0.5 else 0)
        G += T.ring(0.07 * m, 0.012, 0.45, -0.42) * 1.2 + T.polyline([(0.49, -0.48), (0.53, -0.53), (0.58, -0.52)], 0.008) * m
        H += T.gauss(0.585, -0.52, 0.015) * m * pis * 2.0
        G += T.ring(0.18 * m, 0.008, 0.45, -0.05) * pis * 0.9
        G += T.lines([(0.45, -0.28, 0.45, -0.2, 1.0), (0.45, 0.1, 0.45, 0.18, 1.0), (0.27, -0.05, 0.35, -0.05, 1.0), (0.55, -0.05, 0.63, -0.05, 1.0)], 0.01) * m * pis
    return G * env, H * env


def bakugo_preparo(T, t, rng):
    G, H = vazio(T)
    a = t * TAU
    for j in range(3):
        b = a + TAU * j / 3
        x, y = 0.45 * math.cos(b), -0.05 + 0.45 * math.sin(b) * 0.55
        u = (t * 3 + j / 3) % 1
        G += T.gauss(x, y, 0.06 + 0.1 * u) * (1 - u) * 1.3
        G += T.ring(0.05 + 0.13 * u, 0.012, x, y) * (1 - u) * 1.1
        H += T.gauss(x, y, 0.012) * (1 - u) * 2.0
    G += T.arc_band(0.45, 0.035, a, a + 4.5, 0.55, 0, 0.0, -0.05, 1.0) * 1.1
    G += T.gauss(0.0, -0.05, 0.1) * 0.6
    return G, H


def howitzer_impact(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    # o tornado de explosões descendo em espiral
    d = rel(t, 0.0, 0.5)
    if 0 < d < 1:
        for j in range(10):
            u = j / 10
            y = -0.95 + 0.9 * (u * 0.6 + d * 0.6)
            a = u * TAU * 2.2 + t * 18
            r = 0.3 * (1 - u * 0.5) * (1 - d * 0.5)
            x = r * math.cos(a)
            kk = (1 - d * 0.3) * (0.4 + 0.6 * u)
            G += T.gauss(x, y, 0.04) * kk * 1.1 + T.ring(0.05, 0.01, x, y) * kk * 0.8
        G += T.arc_band(0.3 * (1 - d * 0.5), 0.03, t * 18, t * 18 + 5.0, 0.35, 0, 0.0, -0.95 + 0.9 * d * 0.7, 1.0) * 1.2
    g, h = clarao(T, t, 0.45, 0.7, 0.0, 0.0, 2.2, 2.0)
    G, H = G + g, H + h
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = _bum(T, t, 0.46 + 0.04 * i, 0.9, cx, 0.0, 0.38, 575 + i)
        G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.46, 1.0, 1.0, 0.38, 1.8)
    G += particulas(T, t, 0.5, 1.0, 28, 578, 0.0, 0.0, 0.8, 0.7, 0.02)
    return G * env, H * env


# ------------------------------------------------------------------ Todoroki

def muralha_de_gelo_todoroki(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    for j in range(9):
        x = -0.6 + 0.135 * j
        s = surge(t, 0.05 + 0.04 * j, 0.25 + 0.04 * j)
        if s > 0:
            h = (0.18 + 0.05 * j) * s if j < 8 else 0.6 * s
            g, hh = _pico_gelo(T, x, 0.38, h, 0.09 + 0.01 * j, kk)
            G, H = G + g, H + hh
    g, h = clarao(T, t, 0.38, 0.58, 0.45, -0.05, 1.2, 1.2)
    G, H = G + g, H + h
    m = pulso(t, 0.45, 1.0)
    if m > 0:
        G += T.ring(0.22, 0.03, 0.45, -0.05, 0.75) * m * 1.0
        for j in range(4):
            a = TAU * j / 4 + 0.4
            H += T.lines([(0.45 + 0.1 * math.cos(a), -0.05 + 0.14 * math.sin(a), 0.45 + 0.24 * math.cos(a), -0.05 + 0.3 * math.sin(a), 1.0)], 0.006) * m
    G += particulas(T, t, 0.3, 1.0, 20, 579, 0.0, 0.25, 0.7, 0.3, 0.01)
    return G * env, H * env


def chama_esquerda(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.6)
    G += T.gauss(-0.55, -0.05, 0.08) * k * 1.0
    u = ease_out(rel(t, 0.05, 0.35), 1.6)
    kk = 1 - rel(t, 0.5, 0.65)
    if u > 0 and kk > 0:
        ponta = -0.55 + 1.0 * u
        q = np.random.default_rng(580 + int(t * 30))
        for j in range(4):
            pts = [(-0.55 + (ponta + 0.55) * v, -0.05 + (0.04 + 0.05 * v) * math.sin(v * 10 + t * 30 + j * 1.7) * (1 + j * 0.3)) for v in np.linspace(0, 1, 24)]
            G += T.polyline(pts, 0.03 - 0.005 * j) * kk * (1.0 - 0.15 * j)
        G += T.tapered([(-0.55, -0.05, ponta, -0.05, 1.0)], 0.1) * kk * 0.7
        for _ in range(4):
            v = q.uniform(0.3, 1)
            g, h = icone(T, poe(CHAMA, -0.55 + (ponta + 0.55) * v, -0.05 + q.uniform(-0.1, 0.1), 0.05 + 0.04 * v, -math.pi / 2), kk * 0.9, 0.6)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.55, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    q2 = pulso(t, 0.45, 1.0)
    if q2 > 0:
        for j in range(4):
            g, h = icone(T, poe(CHAMA, 0.33 + 0.08 * j, 0.1 - 0.04 * (j % 2), 0.08 + 0.02 * math.sin(t * 25 + j)), q2, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.35, 1.0, 14, 581, 0.45, 0.0, 0.25, 0.6, 0.012)
    return G * env, H * env


def todoroki_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0.0, -0.05, 0.2, 0.3) * 0.35
    for j in range(4):
        y = -0.35 + 0.18 * j
        g, h = icone(T, poe(CHAMA, -0.25 - 0.05 * math.sin(t * TAU * 2 + j), y, 0.08 + 0.015 * math.sin(t * TAU * 3 + j)), 1.0, 0.6)
        G, H = G + g, H + h
        g, h = _pico_gelo(T, 0.25, y + 0.08, 0.14, 0.06, 1.0)
        G, H = G + g, H + h
    G += T.lines([(0.0, -0.45, 0.0, 0.35, 1.0)], 0.008) * 0.9
    H += T.splats([(0.15 + 0.15 * math.cos(t * TAU + j), -0.05 + 0.3 * math.sin(t * TAU + j), 1.0) for j in range(3)], 0.012)
    return G, H


def ponto_de_fusao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    # o gelo cobrindo o chão
    gelo = ease_out(rel(t, 0.0, 0.3), 2)
    kg = 1 - rel(t, 0.5, 0.65)
    if gelo > 0 and kg > 0:
        G += T.ring(0.05 + 1.0 * gelo, 0.04, 0.0, 0.38, 3.0) * kg * 1.2
        for j in range(7):
            x = -0.75 + 0.25 * j
            if abs(x) < gelo:
                g, h = _pico_gelo(T, x, 0.38, 0.15 + 0.05 * (j % 3), 0.06, kg)
                G, H = G + g, H + h
    # o fogo por cima
    fogo = pulso(t, 0.3, 0.75)
    if fogo > 0:
        for j in range(9):
            x = -0.8 + 0.2 * j
            g, h = icone(T, poe(CHAMA, x, 0.22 - 0.06 * (j % 2), 0.12 + 0.03 * math.sin(t * 25 + j)), fogo * 1.1, 0.6)
            G, H = G + g, H + h
    # a explosão de vapor (o choque de gelo e fogo)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        u = rel(t, 0.5 + 0.04 * i, 0.95)
        if 0 < u < 1:
            for j in range(5):
                a = TAU * j / 5 + i
                d = 0.25 * ease_out(u)
                G += T.gauss(cx + d * math.cos(a), -0.05 + d * math.sin(a) * 0.7 - 0.2 * u, 0.06 + 0.08 * u) * (1 - u) * 0.9
        g, h = clarao(T, t, 0.5 + 0.04 * i, 0.7 + 0.04 * i, cx, -0.05, 0.8, 1.0)
        G, H = G + g, H + h
    G += particulas(T, t, 0.5, 1.0, 26, 582, 0.0, 0.0, 0.8, 0.6, 0.016)
    return G * env, H * env


# ------------------------------------------------------------------ Mob

def telecinese_mob(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.gauss(-0.55, -0.05, 0.2, 0.3) * pulso(t, 0.0, 0.6) * 0.5
    for j in range(4):
        sobe = ease_out(rel(t, 0.0 + 0.04 * j, 0.25 + 0.04 * j), 2)
        voa = ease_in(rel(t, 0.3 + 0.04 * j, 0.5 + 0.04 * j), 2)
        if sobe > 0 and voa < 1:
            x0, y0 = -0.75 + 0.15 * j, 0.35 - 0.55 * sobe - 0.08 * (j % 2)
            x, y = x0 + (0.45 - x0) * voa, y0 + (-0.05 - y0) * voa
            g, h = _pedra(T, x, y, 0.11 + 0.02 * j, t * 4 + j, 1.0)
            G, H = G + g, H + h
            G += T.ring(0.17, 0.008, x, y) * (1 - voa) * 0.8 * pulso(t, 0.0, 0.5)
            if voa > 0:
                G += T.tapered([(x0 + (0.45 - x0) * max(0, voa - 0.3), y0 + (-0.05 - y0) * max(0, voa - 0.3), x, y, 0.8)], 0.03)
    g, h = clarao(T, t, 0.45, 0.68, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.46, 0.85, 14, 583, 0.45, -0.05, 0.55, 0.013)
    b = surge(t, 0.5, 0.65) * (1 - rel(t, 0.9, 1))
    if b > 0:
        G += _barra(T, -0.75, -0.45, 0.4, 0.3 + 0.25 * rel(t, 0.55, 0.85), b)
    return G * env, H * env


def barreira_psiquica_mob(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.05, 0.35) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        G += T.arc_band(0.45 * s, 0.03, math.pi, TAU, 1.0, 0, 0.0, 0.3, 0.0) * 1.3
        G += T.ring(0.45 * s, 0.02, 0.0, 0.3, 4.0) * 0.9
        G += T.gauss(0.0, 0.1, 0.35 * s, 0.25 * s) * 0.25
        q = np.random.default_rng(584 + int(t * 12))
        for _ in range(5):
            a = q.uniform(math.pi * 1.1, math.pi * 1.9)
            H += T.gauss(0.45 * s * math.cos(a), 0.3 + 0.45 * s * math.sin(a), 0.015) * 2.0
    G += anel(T, t, 0.05, 0.45, 0.1, 0.6, 0.03, 0.1, 1.0, 1.2)
    b = surge(t, 0.4, 0.55) * (1 - rel(t, 0.9, 1))
    if b > 0:
        G += _barra(T, -0.2, -0.3, 0.4, 0.3 + 0.35 * rel(t, 0.45, 0.85), b)
    return G * env, H * env


def mob_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0.0, -0.05, 0.25, 0.4) * (0.4 + 0.2 * math.sin(t * TAU * 3))
    for j in range(5):
        u = (t + j / 5) % 1
        x = -0.3 + 0.15 * j
        G += T.tapered([(x, 0.35 - 0.6 * u + 0.15, x, 0.35 - 0.6 * u, 0.8)], 0.02) * math.sin(math.pi * u)
    for j in range(3):
        a = t * TAU + TAU * j / 3
        g, h = _pedra(T, 0.4 * math.cos(a), 0.15 + 0.12 * math.sin(a), 0.09, a, 1.0)
        G, H = G + g, H + h
    pis = 0.7 + 0.3 * math.sin(t * TAU * 4)
    G += _porcento(T, 0.0, -0.45, 0.22, pis)
    return G, H


def cem_por_cento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    c = pulso(t, 0.05, 0.6)
    if c > 0:
        G += T.gauss(-0.55, -0.4, 0.12, 0.6) * c * 1.0
        G += T.tapered([(-0.55, 0.35, -0.55, -1.0, 1.0)], 0.12) * c * 0.9
        H += T.lines([(-0.55, 0.3, -0.55, -0.95, 1.0)], 0.01) * c * 1.6
    p = surge(t, 0.1, 0.3) * (1 - rel(t, 0.5, 0.6))
    if p > 0:
        G += _porcento(T, -0.55, -0.55, 0.16 * p, 1.0)
    g, h = clarao(T, t, 0.25, 0.5, -0.55, -0.3, 1.8, 1.6)
    G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.35 + 0.07 * j, 0.85 + 0.05 * j)
        if 0 < u < 1:
            G += T.arc_band(0.2 + 1.2 * ease_out(u), 0.05 * (1 - 0.5 * u), -0.8, 0.8, 0.8, 0, -0.55, -0.05, 0.0) * (1 - u) * 1.3
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.05 * i, 0.72 + 0.05 * i, cx + 0.1, -0.05, 0.8, 1.0)
        G, H = G + g, H + h
    G += estouro(T, t, 0.3, 0.8, 22, 585, -0.55, -0.3, 0.9, 0.016)
    G += particulas(T, t, 0.3, 1.0, 26, 586, -0.2, 0.0, 0.8, 0.8, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Rimuru

def devorar_rimuru(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = pulso(t, 0.15, 0.75)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        g, h = _slime(T, -0.5, 0.15, 0.2 * s, 1.0, abre, t)
        G, H = G + g, H + h
    # a bolinha de luz (a habilidade copiada) saindo do rival e entrando na boca
    u = rel(t, 0.25, 0.65)
    if 0 < u < 1:
        e = ease_in(u, 1.6)
        x, y = 0.45 + (-0.48 - 0.45) * e, -0.15 + (0.19 + 0.15) * e - 0.15 * math.sin(math.pi * e)
        G += T.gauss(x, y, 0.05) * 1.2 + T.tapered([(x + 0.25 * (1 - e), y - 0.05, x, y, 0.8)], 0.03)
        H += T.gauss(x, y, 0.02) * 2.0
        for j in range(3):
            a = t * 12 + TAU * j / 3
            H += T.gauss(x + 0.07 * math.cos(a), y + 0.07 * math.sin(a), 0.01) * 1.5
    g, h = clarao(T, t, 0.2, 0.4, 0.45, -0.1, 0.8, 1.0)
    G, H = G + g, H + h
    G += anel(T, t, 0.62, 0.95, 0.1, 0.45, 0.03, 0.15, 1.0, 1.3)
    G += particulas(T, t, 0.62, 1.0, 12, 587, -0.5, 0.1, 0.2, 0.4, 0.01)
    return G * env, H * env


def grande_sabio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        s = surge(t, 0.08 + 0.08 * i, 0.3 + 0.08 * i) * (1 - rel(t, 0.85, 0.97))
        if s > 0:
            G += _painel(T, cx, -0.45, 0.14 * s, 0.09 * s, 1.0)
            # a varredura de leitura descendo no painel
            v = (t * 2 + i / 3) % 1
            H += T.lines([(cx - 0.13 * s, -0.54 + 0.18 * v * s, cx + 0.13 * s, -0.54 + 0.18 * v * s, 1.0)], 0.004) * s
            G += T.lines([(cx, -0.36, cx, -0.2, 1.0)], 0.004) * s * 0.8
            G += T.ring(0.2 * s, 0.012, cx, 0.0, 0.9) * pulso(t, 0.35 + 0.08 * i, 0.8)
        g, h = clarao(T, t, 0.4 + 0.08 * i, 0.6 + 0.08 * i, cx, 0.0, 0.5, 0.8)
        G, H = G + g, H + h
    G += particulas(T, t, 0.3, 1.0, 16, 588, 0.0, -0.2, 0.6, 0.3, 0.009)
    return G * env, H * env


def rimuru_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(6):
        a = t * TAU + TAU * j / 6
        g, h = icone(T, poe(GOTA, 0.42 * math.cos(a), -0.05 + 0.24 * math.sin(a), 0.09), 1.0, 0.6)
        G, H = G + g, H + h
    G += T.arc_band(0.32, 0.03, -2.4, -0.6, 1.0, 0, 0.0, 0.12, 1.0, True) * (0.9 + 0.3 * math.sin(t * TAU * 3))
    H += T.arc_band(0.32, 0.008, -2.4, -0.6, 1.0, 0, 0.0, 0.12, 1.0, True) * 1.2
    return G, H


def corte_de_agua(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.35)
    G += T.ring(0.14, 0.016, -0.55, -0.05) * k * 1.2
    u = rel(t, 0.15, 0.45)
    if 0 < u < 1:
        e = ease_in(u, 1.5)
        x = -0.55 + 1.0 * e
        G += T.arc_band(0.3, 0.03, -1.3, 1.3, 1.0, 0, x - 0.15, -0.05, 1.0, True) * 1.4
        H += T.arc_band(0.3, 0.008, -1.3, 1.3, 1.0, 0, x - 0.15, -0.05, 1.0, True) * 1.4
        G += T.tapered([(x - 0.4, -0.05, x, -0.05, 0.6)], 0.015)
    g, h = corte(T, t, 0.38, 0.6, 1.35, 1.2, 0.035, 0.45, -0.05, 0.08)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.4, 0.6, 0.45, -0.05, 1.2, 1.2)
    G, H = G + g, H + h
    q = np.random.default_rng(589)
    sp = rel(t, 0.42, 0.95)
    if 0 < sp < 1:
        for _ in range(10):
            a, v = q.uniform(-math.pi, 0), q.uniform(0.4, 1.0)
            x = 0.45 + 0.4 * v * sp * math.cos(a)
            y = -0.05 + 0.35 * v * sp * math.sin(a) + 0.5 * sp * sp
            g, h = icone(T, poe(GOTA, x, y, 0.03 * (1 - sp) + 0.01), 1 - sp, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Ainz

def toque_da_morte_ainz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.6, 0.75)
    if k > 0:
        g, h = _mao_osso(T, -0.25 + 0.5 * u, -0.05, 0.5, k, rel(t, 0.28, 0.4))
        G, H = G + g, H + h
        G += T.gauss(-0.25 + 0.5 * u, -0.05, 0.25) * k * 0.3
    g, h = clarao(T, t, 0.3, 0.5, 0.45, -0.05, 1.0, 1.1)
    G, H = G + g, H + h
    # o selo da maldição no rival: o círculo com a caveira pequena
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.012, 0.45, -0.45) * 1.2 + T.ring(0.11 * m, 0.006, 0.45, -0.45)
        g, h = _caveira_ainz(T, 0.45, -0.45, 0.06 * m, 1.0)
        G, H = G + g, H + h
        for j in range(6):
            a = TAU * j / 6 + t * 3
            G += T.lines([(0.45 + 0.13 * m * math.cos(a), -0.45 + 0.13 * m * math.sin(a), 0.45 + 0.15 * m * math.cos(a), -0.45 + 0.15 * m * math.sin(a), 1.0)], 0.008)
    G += particulas(T, t, 0.4, 1.0, 14, 590, 0.45, -0.05, 0.2, -0.4, 0.012)
    return G * env, H * env


def invocar_mortos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    kc = 1 - rel(t, 0.8, 0.95)
    if abre > 0:
        G += (T.ring(0.42 * abre, 0.016, 0.0, 0.36, 3.0) + T.ring(0.32 * abre, 0.01, 0.0, 0.36, 3.0)) * kc * 1.2
        for j in range(8):
            a = TAU * j / 8 + t * 2
            G += T.lines([(0.37 * abre * math.cos(a), 0.36 + 0.37 * abre * math.sin(a) / 3, 0.37 * abre * math.cos(a + 0.4), 0.36 + 0.37 * abre * math.sin(a + 0.4) / 3, 1.0)], 0.006) * kc
    sobe = ease_out(rel(t, 0.25, 0.6), 2)
    if sobe > 0:
        g, h = _cavaleiro(T, 0.0, 0.36 - 0.42 * sobe, 0.3, kc * min(1, sobe * 1.5))
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.5, 0.7, 0.0, -0.3, 1.0, 1.0)
    G, H = G + g, H + h
    for i, cx in enumerate((0.2, 0.5, 0.8)):
        m = pulso(t, 0.6 + 0.04 * i, 1.0)
        if m > 0:
            G += T.lines([(cx, -0.45, cx, -0.25, 1.0), (cx - 0.05, -0.31, cx, -0.25, 1.0), (cx + 0.05, -0.31, cx, -0.25, 1.0)], 0.012) * m * 1.2
    G += particulas(T, t, 0.3, 1.0, 20, 591, 0.0, 0.3, 0.4, 0.6, 0.012)
    return G * env, H * env


def ainz_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _caveira_ainz(T, 0.0, -0.1, 0.18, 1.0, 0.7 + 0.3 * math.sin(t * TAU * 2))
    G, H = G + g, H + h
    G += T.ring(0.4, 0.012, 0.0, -0.05) * 0.9
    segs = []
    for j in range(10):
        a = TAU * j / 10 + t * TAU
        x, y = 0.4 * math.cos(a), -0.05 + 0.4 * math.sin(a)
        segs += [(x - 0.025, y, x + 0.025, y, 1.0), (x, y - 0.03, x, y + 0.03, 1.0)]
    G += T.lines(segs, 0.007) * 1.1
    return G, H


def o_fim_de_toda_vida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    # o relógio gigante no alto: as 12 marcas e o ponteiro dando a volta
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.65, 0.8))
    if s > 0:
        cx, cy, r = 0.0, -0.45, 0.32 * s
        G += T.ring(r, 0.016, cx, cy) * 1.3 + T.ring(r * 0.85, 0.008, cx, cy) * 0.9 + T.gauss(cx, cy, r * 0.8) * 0.2
        segs = [(cx + r * 0.75 * math.cos(TAU * j / 12), cy + r * 0.75 * math.sin(TAU * j / 12), cx + r * 0.85 * math.cos(TAU * j / 12),
                 cy + r * 0.85 * math.sin(TAU * j / 12), 1.0) for j in range(12)]
        G += T.lines(segs, 0.012) * 1.2
        volta = ease_in(rel(t, 0.15, 0.6), 1.3)
        a = -math.pi / 2 + TAU * volta
        G += T.lines([(cx, cy, cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a), 1.0)], 0.014) * 1.4
        G += T.arc_band(r * 0.5, 0.02, -math.pi / 2, a, 1.0, 0, cx, cy, 0.5) * 0.7
        H += T.gauss(cx, cy, 0.02) * 1.8
    g, h = clarao(T, t, 0.58, 0.78, 0.0, -0.45, 1.8, 1.6)
    G, H = G + g, H + h
    # a onda da morte descendo em todos
    u = rel(t, 0.6, 0.98)
    if 0 < u < 1:
        G += T.ring(0.1 + 1.1 * ease_out(u, 2), 0.06 * (1 - 0.5 * u), 0.0, -0.45, 1.0) * (1 - u) * 1.3
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        m = pulso(t, 0.65 + 0.04 * i, 1.0)
        if m > 0:
            g, h = _caveira_ainz(T, cx, -0.05, 0.08, m)
            G, H = G + g, H + h
    G += particulas(T, t, 0.6, 1.0, 26, 592, 0.0, 0.0, 0.8, -0.4, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Lelouch

def geass_lelouch(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    # o olho de Lelouch acendendo com o selo
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.65))
    if k > 0:
        G += T.ring(0.14, 0.014, -0.55, -0.25, 1.9) * k * 1.3
        g, h = _passaro_geass(T, -0.55, -0.25, 0.09 * k, k)
        G, H = G + g, H + h
        G += T.gauss(-0.55, -0.25, 0.15) * k * 0.4
    u = rel(t, 0.2, 0.5)
    if 0 < u < 1:
        e = ease_in(u, 1.3)
        x, y = -0.55 + 1.0 * e, -0.25 - 0.1 * math.sin(math.pi * e)
        g, h = _passaro_geass(T, x, y, 0.12 + 0.08 * math.sin(math.pi * u), 1.0)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.35, y + 0.02, x - 0.05, y, 0.8)], 0.025)
    m = surge(t, 0.48, 0.62) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.14, 0.014, 0.45, -0.25, 1.9) * m * 1.3
        g, h = _passaro_geass(T, 0.45, -0.25, 0.09 * m, m)
        G, H = G + g, H + h
        G += T.ring(0.16 * m, 0.008, 0.45, -0.25) * (0.6 + 0.4 * math.sin(t * 30))
        pts = [(0.45 + 0.12 * u2 * math.cos(-t * 9 + u2 * 9), -0.5 + 0.05 * u2 * math.sin(-t * 9 + u2 * 9)) for u2 in np.linspace(0.05, 1, 24)]
        G += T.polyline(pts, 0.012) * m * 1.2
        G += T.ring(0.07, 0.01, 0.45, 0.05) * m * 1.1 + T.lines([(0.39, 0.0, 0.51, 0.1, 1.0)], 0.01) * m * 1.2
    g, h = clarao(T, t, 0.45, 0.62, 0.45, -0.25, 0.8, 1.0)
    G, H = G + g, H + h
    return G * env, H * env


def xadrez(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    tab = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 0.97))
    if tab > 0:
        G += _tabuleiro(T, 0.0, 0.3, 0.7 * tab, 1.0)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        s = surge(t, 0.15 + 0.07 * i, 0.35 + 0.07 * i) * (1 - rel(t, 0.85, 0.97))
        avanca = ease_out(rel(t, 0.4 + 0.05 * i, 0.6 + 0.05 * i), 2)
        if s > 0:
            g, h = icone(T, poe(_PEAO if i != 1 else _REI, cx + 0.1 * avanca, 0.2 - 0.06 * avanca, 0.13 * s), 1.1, 0.5)
            G, H = G + g, H + h
        g, h = clarao(T, t, 0.45 + 0.05 * i, 0.65 + 0.05 * i, cx, -0.1, 0.6, 0.8)
        G, H = G + g, H + h
        G += T.ring(0.22, 0.012, cx, -0.05, 0.9) * pulso(t, 0.45 + 0.05 * i, 0.9)
    G += particulas(T, t, 0.4, 1.0, 14, 593, 0.0, 0.0, 0.6, 0.4, 0.01)
    return G * env, H * env


def lelouch_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(_REI, 0.0, 0.0, 0.3, 0.15 * math.sin(t * TAU)), 1.0, 0.45)
    G, H = G + g, H + h
    a = t * TAU
    g, h = _passaro_geass(T, 0.35 * math.cos(a), 0.0 + 0.15 * math.sin(a), 0.08, 1.0)
    G, H = G + g, H + h
    G += T.ring(0.38, 0.01, 0.0, 0.0, 2.2) * 0.8
    return G, H


def xeque_mate(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    tab = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 0.97))
    if tab > 0:
        G += _tabuleiro(T, 0.0, 0.3, 0.75 * tab, 1.0)
    av = ease_in(rel(t, 0.15, 0.4), 1.6)
    k = surge(t, 0.05, 0.2) * (1 - rel(t, 0.8, 0.95))
    if k > 0:
        g, h = icone(T, poe(_REI, -0.5 + 0.3 * av, 0.15, 0.16 * k), 1.2, 0.55)
        G, H = G + g, H + h
    # o rei rival tombando
    tomba = ease_in(rel(t, 0.42, 0.65), 1.6)
    kr = 1 - rel(t, 0.85, 0.97)
    if kr > 0:
        g, h = icone(T, poe(_REI, 0.45 + 0.12 * tomba, 0.15 + 0.06 * tomba, 0.16, tomba * math.pi / 2), kr * 0.9, 0.35)
        G, H = G + g, H + h
    u = rel(t, 0.32, 0.6)
    if 0 < u < 1:
        G += T.tapered([(-0.2, -0.0, -0.2 + 0.65 * ease_out(u), -0.02, 1.0)], 0.07) * 1.1
        H += T.lines([(-0.2, 0.0, -0.2 + 0.65 * ease_out(u), -0.02, 1.0)], 0.01) * 1.4
    g, h = clarao(T, t, 0.42, 0.65, 0.45, -0.02, 1.4, 1.4)
    G, H = G + g, H + h
    m = pulso(t, 0.6, 1.0)
    if m > 0:
        G += T.lines([(0.75, -0.35, 0.75, -0.15, 1.0), (0.7, -0.21, 0.75, -0.15, 1.0), (0.8, -0.21, 0.75, -0.15, 1.0)], 0.012) * m * 1.2
    G += estouro(T, t, 0.43, 0.85, 14, 594, 0.45, -0.02, 0.55, 0.013)
    return G * env, H * env


REGISTRO = [
    ("explosao_bakugo", explosao_bakugo, GRANDE, "Bakugo · a palma e a explosão", False),
    ("granada_bakugo", granada_bakugo, GRANDE, "Bakugo · a manopla e a bomba marcada", False),
    ("bakugo_preparo", bakugo_preparo, MEDIA, "Bakugo · girando nas explosões (Preparo, laço)", True),
    ("howitzer_impact", howitzer_impact, GRANDE, "Bakugo · o tornado de explosões", False),
    ("muralha_de_gelo_todoroki", muralha_de_gelo_todoroki, GRANDE, "Todoroki · a geleira subindo pelo chão", False),
    ("chama_esquerda", chama_esquerda, GRANDE, "Todoroki · o jato de fogo da mão esquerda", False),
    ("todoroki_preparo", todoroki_preparo, MEDIA, "Todoroki · metade gelo, metade fogo (Preparo, laço)", True),
    ("ponto_de_fusao", ponto_de_fusao, GRANDE, "Todoroki · o gelo, o fogo e o vapor", False),
    ("telecinese_mob", telecinese_mob, GRANDE, "Mob · as pedras voando e a energia enchendo", False),
    ("barreira_psiquica_mob", barreira_psiquica_mob, GRANDE, "Mob · a cúpula psíquica", False),
    ("mob_preparo", mob_preparo, MEDIA, "Mob · a aura e o % piscando (Preparo, laço)", True),
    ("cem_por_cento", cem_por_cento, GRANDE, "Mob · a coluna de energia e as ondas", False),
    ("devorar_rimuru", devorar_rimuru, GRANDE, "Rimuru · o slime engolindo a habilidade", False),
    ("grande_sabio", grande_sabio, GRANDE, "Rimuru · os painéis do Grande Sábio", False),
    ("rimuru_preparo", rimuru_preparo, MEDIA, "Rimuru · as gotas e a lâmina de água (Preparo, laço)", True),
    ("corte_de_agua", corte_de_agua, GRANDE, "Rimuru · a lâmina de água e os respingos", False),
    ("toque_da_morte_ainz", toque_da_morte_ainz, GRANDE, "Ainz · a mão de esqueleto e o selo", False),
    ("invocar_mortos", invocar_mortos, GRANDE, "Ainz · o círculo e o Cavaleiro da Morte", False),
    ("ainz_preparo", ainz_preparo, MEDIA, "Ainz · a caveira e as runas (Preparo, laço)", True),
    ("o_fim_de_toda_vida", o_fim_de_toda_vida, GRANDE, "Ainz · o relógio e a onda da morte", False),
    ("geass_lelouch", geass_lelouch, GRANDE, "Lelouch · o selo do Geass voando de olho a olho", False),
    ("xadrez", xadrez, GRANDE, "Lelouch · o tabuleiro e as peças", False),
    ("lelouch_preparo", lelouch_preparo, MEDIA, "Lelouch · o rei e o Geass (Preparo, laço)", True),
    ("xeque_mate", xeque_mate, GRANDE, "Lelouch · o rei rival tombando e o feixe", False),
]
