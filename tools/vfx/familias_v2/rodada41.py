"""Rodada 41 das habilidades próprias: Heihachi, Jake, Marceline, Robin, Luigi e Princesa Peach.

Heihachi Mishima
- punho_do_deus_do_trovao: o soco com os raios enrolados no punho (Eletrificado).
- postura_demoniaca: a aura vermelha escura, os chifres de sombra e as placas de defesa (Escudo e Fortalecido).
- heihachi_preparo: o Preparo do Raio do Mishima — agachado, as faíscas juntando no punho (laço).
- raio_do_mishima: o raio enorme saindo do soco e rasgando até o rival (Eletrificado).

Jake
- punho_gigante_jake: o punho que incha enorme no caminho e esmaga o rival.
- escudo_elastico_jake: o Jake esticado como uma cúpula amarela por cima do aliado (Escudo e Protegido).
- jake_preparo: o Preparo do Jake gigante — o corpo inchando e pulsando (laço).
- jake_gigante: a pata gigante pisando em todos e o chão tremendo (Preso).

Marceline
- mordida_de_marceline: as duas presas, os furinhos e a vida vermelha voltando para ela (Roubo de vida).
- baixo_machado: o baixo-machado girando no golpe e as notas graves.
- marceline_preparo: o Preparo da Forma de morcego — os olhos vermelhos e as asas se formando (laço).
- forma_de_morcego: as asas enormes de morcego varrendo todos e a vida sendo sugada (Vampirismo).

Robin
- bastao_retratil: o bastão estendendo num estalo e a pancada (Marcado).
- batarangue_robin: o bumerangue de pássaro voando em arco, acertando e voltando (Paralisado).
- robin_preparo: o Preparo do Ataque em dupla — dois bumerangues prontos e a capa (laço).
- ataque_em_dupla: Robin e o Morcego cruzando em X no rival (Exposto).

Luigi
- bola_de_fogo_verde: a bola de fogo verde quicando até o rival (Queimando).
- poltergust: o aspirador sugando em cone e o redemoinho (Enfraquecido e Lento).
- luigi_preparo: o Preparo do Míssil Luigi — a cabeça baixa, as faíscas e o tremor (laço).
- missil_luigi: o Luigi voando de cabeça como um míssil e o impacto enorme.

Princesa Peach
- sombrinha: a sombrinha abrindo por cima do aliado (Escudo e Protegido).
- bolo_de_cura: o bolo com as velinhas e o coração de cura (Vida).
- peach_preparo: o Preparo da Vibe da princesa — a coroa brilhando e os coraçõezinhos (laço).
- vibe_da_princesa: as ondas cor-de-rosa, os corações e as estrelinhas no trio (Fortalecido e Acelerado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, CHAMA, COROA, CORACAO, NOTA, anel, aura, cheio, circulo, clarao, converge, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, raios, surge)


def _raio(T, t, x0, y0, x1, y1, k, w=0.016, seed=0, desvio=0.1):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, desvio)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.6


def _tontas(T, t, a, b, cx, cy, n=3, r=0.12, s=0.035):
    G, H = 0.0, 0.0
    k = pulso(t, a, b)
    if k <= 0:
        return G, H
    for j in range(n):
        ang = t * 9 + TAU * j / n
        g, h = cheio(T, poe(estrela_pts(5, 0.45), cx + r * math.cos(ang), cy + r * 0.4 * math.sin(ang), s), k * 1.3)
        G, H = G + g, H + h
    return G, H


# ------------------------------------------------------------------ Heihachi

def punho_do_deus_do_trovao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        x = -0.55 + 0.95 * u
        P, nos = _punho(T, x, 0.0, 2.4, 0)
        G += P * 0.95 * k
        H += nos * 0.45 * k
        for j in range(3):
            g, h = _raio(T, t, x - 0.25, -0.1 + 0.1 * j, x + 0.1, -0.08 + 0.08 * j, k, 0.01, j, 0.2)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.3, 0.75, 6, 5, 0.45, 0.0, 0.4, 0.011)
    return G * env, H * env


def postura_demoniaca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.95)
    q = np.random.default_rng(int(t * 12))
    pts = [(q.normal(0, 0.18), 0.1 - 0.5 * q.uniform(0, 1), k * q.uniform(0.3, 0.7)) for _ in range(24)]
    G += T.splats(pts, 0.06) * 0.6
    s = surge(t, 0.1, 0.35) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            chifre = [(lado * 0.1, -0.45), (lado * 0.25 * s, -0.75 * s - 0.1), (lado * 0.2, -0.45)]
            g, h = icone(T, chifre, 1.2, 0.6)
            G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(lado * 0.07, -0.38, 0.015) * s * 2.0
    for j in range(6):
        a = TAU * j / 6
        m = surge(t, 0.35 + 0.04 * j, 0.55 + 0.04 * j) * (1 - rel(t, 0.88, 1))
        if m > 0:
            cx, cy = 0.3 * math.cos(a), 0.0 + 0.3 * math.sin(a)
            g2, h2 = icone(T, [(cx - 0.07 * m, cy - 0.05 * m), (cx + 0.07 * m, cy - 0.05 * m), (cx + 0.06 * m, cy + 0.05 * m), (cx - 0.06 * m, cy + 0.05 * m)],
                           1.1, 0.5)
            G, H = G + g2, H + h2
    G += raios(T, t, 0.2, 0.7, 4, 2, 0, 0.0, 0.4, 0.008)
    return G * env, H * env


def heihachi_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.0, 0.1, 1.9, -math.pi / 2)
    G += P * 0.85
    H += nos * 0.3
    G += converge(T, (t * 2) % 1, 0.0, 1.0, 10, int(t * 2), 0.0, 0.0, 0.4)
    G += raios(T, t, 0.0, 1.0, 3, 1, 0.0, 0.0, 0.25, 0.008)
    H += T.gauss(0, 0.0, 0.04) * (1.2 + 0.6 * math.sin(t * 15))
    return G, H


def raio_do_mishima(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.1, 0.65)
    if k > 0:
        for j in range(3):
            g, h = _raio(T, t, -0.6, 0.0, 0.6, 0.0, k, 0.03 if j == 0 else 0.012, j * 5, 0.15)
            G, H = G + g, H + h
        G += T.gauss(0, 0, 0.7, 0.12) * k * 0.45
    G += T.gauss(-0.6, 0.0, 0.08) * pulso(t, 0.0, 0.3) * 1.4
    g2, h2 = clarao(T, t, 0.15, 0.6, 0.6, 0.0, 1.5, 1.5)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.2, 0.85, 7, 9, 0.6, 0.0, 0.45, 0.011)
    G += anel(T, t, 0.3, 0.8, 0.05, 0.55, 0.035, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ Jake

def punho_gigante_jake(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.6)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        x = -0.6 + 0.95 * u
        cresce = 1.5 + 2.5 * u
        G += T.lines([(-0.85, 0.05, x - 0.1 * cresce, 0.05, 1.0)], 0.03 + 0.01 * cresce) * k * 1.0
        P, nos = _punho(T, x, 0.05, cresce, 0)
        G += P * 0.95 * k
        H += nos * 0.45 * k
    g, h = clarao(T, t, 0.33, 0.55, 0.45, 0.05, 1.3, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.35, 0.85, 14, 4, 0.45, 0.05, 0.55, 0.014)
    return G * env, H * env


def escudo_elastico_jake(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2.5) * (1 - rel(t, 0.88, 1))
    if s > 0:
        bal = 0.04 * math.sin(t * 14) * (1 - rel(t, 0.3, 0.9))
        pts = [(0.35 * s * math.cos(a), 0.3 - (0.42 + bal) * s * math.sin(a)) for a in np.linspace(0, math.pi, 30)]
        G += T.polyline(pts, 0.05) * 1.1
        G += T.polyline(pts, 0.012) * 0.8
        G += T.polys([(pts, 1.0)], 0.03) * 0.25
        for lado in (-1, 1):
            G += T.gauss(lado * 0.35 * s, 0.3, 0.05) * 1.0
    g, h = aura(T, t, 0.35, 1.0, 0.25, 0.1, 0.6)
    return (G + g) * env, (H + h) * env


def jake_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2.5)
    r = 0.18 + 0.06 * b
    G += T.gauss(0, 0.05, r, r * 0.85) * 0.9
    G += T.ring(r * 1.05, 0.02, 0, 0.05, 1.15) * 1.0
    for lado in (-1, 1):
        G += T.gauss(lado * r * 0.35, -0.02, 0.025) * 1.2
    return G, H


def jake_gigante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.05, 0.35), 2.4)
    k = 1 - rel(t, 0.55, 0.7)
    if desce > 0 and k > 0:
        y = -1.0 + 1.15 * desce
        g, h = icone(T, [(-0.7, y - 0.4), (0.7, y - 0.4), (0.75, y + 0.05), (-0.75, y + 0.05)], k * 1.0, 0.45)
        G, H = G + g, H + h
        for j in range(4):
            x = -0.45 + 0.3 * j
            g2, h2 = cheio(T, poe(circulo(14), x, y + 0.08, 0.1), k * 1.0)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.33, 0.55, 0.0, 0.2, 1.5, 1.4)
    G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.33, 0.95, 1.0, 0.35, 1.8)
    G += estouro(T, t, 0.35, 0.9, 20, 6, 0.0, 0.25, 0.8, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Marceline

def mordida_de_marceline(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_in(rel(t, 0.1, 0.35), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        for lado in (-1, 1):
            x = 0.45 + lado * 0.12
            y0 = -0.3 + 0.25 * fecha
            g, h = icone(T, [(x - 0.06, y0 - 0.18), (x + 0.06, y0 - 0.18), (x, y0 + 0.12)], k * 1.3, 0.6)
            G, H = G + g, H + h
    s = surge(t, 0.35, 0.5) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            G += T.gauss(0.45 + lado * 0.08, -0.05, 0.02 * s + 0.002) * 1.6
    u = rel(t, 0.45, 0.9)
    if 0 < u < 1:
        for j in range(6):
            v = (u + j / 6) % 1
            x = 0.45 + (-0.6 - 0.45) * v
            G += T.gauss(x, -0.05 - 0.15 * math.sin(math.pi * v), 0.025) * (1 - abs(2 * v - 1)) * 1.4
    g2, h2 = clarao(T, t, 0.32, 0.5, 0.45, -0.05, 0.6)
    return (G + g2) * env, (H + h2) * env


_BAIXO = [(-0.2, 1.0), (0.2, 1.0), (0.2, 0.1), (0.55, 0.0), (0.7, -0.35), (0.35, -0.3), (0.15, -0.55), (0.1, -1.0), (-0.1, -1.0), (-0.15, -0.55),
          (-0.4, -0.35), (-0.6, -0.1), (-0.2, 0.1)]


def baixo_machado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        a = -2.2 + 2.0 * u
        px, py = -0.15, 0.35
        hx, hy = px + 0.55 * math.cos(a), py + 0.55 * math.sin(a)
        g, h = icone(T, poe(_BAIXO, hx, hy, 0.18, a + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
        if u < 1:
            G += T.arc_band(0.55, 0.06, a - 0.9, a, 1.0, 0, px, py, 1.0) * k * 0.6
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.45, 0.1, 1.2, 1.3)
    G, H = G + g2, H + h2
    for j in range(4):
        w = rel(t, 0.38 + 0.05 * j, 0.9)
        if 0 < w < 1:
            g3, h3 = cheio(T, poe(NOTA, 0.45 + 0.1 * (j - 1.5) + 0.1 * w, -0.1 - 0.4 * w, 0.06), (1 - w) * 1.3)
            G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.35, 0.8, 0.6, 0.35, 1.2)
    return G * env, H * env


def marceline_preparo(T, t, rng):
    G, H = vazio(T)
    abre = 0.6 + 0.4 * math.sin(t * TAU * 1.5)
    for lado in (-1, 1):
        asa = [(lado * x * abre, y * 0.7) for x, y in ASA]
        g, h = icone(T, poe(asa, 0, 0.0, 0.45), 1.0, 0.5)
        G, H = G + g, H + h
    for lado in (-1, 1):
        H += T.gauss(lado * 0.04, -0.03, 0.012) * 2.2
        G += T.gauss(lado * 0.04, -0.03, 0.025) * 1.4
    return G, H


def forma_de_morcego(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5)
    k = 1 - rel(t, 0.75, 0.9)
    if abre > 0 and k > 0:
        bat = 0.25 * math.sin(t * 18)
        for lado in (-1, 1):
            asa = [(lado * x * (0.6 + 0.4 * abre), y * (1 + bat)) for x, y in ASA]
            g, h = icone(T, poe(asa, -0.3, -0.25, 0.65 * abre), k * 1.1, 0.45)
            G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(-0.3 + lado * 0.04, -0.28, 0.015) * k * 2.0
    for j in range(3):
        u = rel(t, 0.3 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            G += T.arc_band(0.4 + 0.5 * u, 0.04, -0.7, 0.7, 0.6, 0, -0.3, 0.0, 0.0) * (1 - u) * 1.2
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.45, 0.62, x + 0.1, 0.05, 0.45)
        G, H = G + g2, H + h2
    G += converge(T, t, 0.55, 0.95, 18, 5, -0.3, -0.1, 0.9)
    return G * env, H * env


# ------------------------------------------------------------------ Robin

def _bastao(T, x0, y0, x1, y1, k, w=0.05):
    return T.lines([(x0, y0, x1, y1, 1.0)], w) * k * 1.3 + T.lines([(x0, y0, x1, y1, 1.0)], w * 0.3) * k * 0.6


def bastao_retratil(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    estica = ease_out(rel(t, 0.1, 0.25), 3)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        comp = 0.15 + 0.6 * estica
        G += _bastao(T, -0.2, 0.1, -0.2 + comp, 0.05, k)
        for m in range(3):
            G += T.ring(0.015, 0.006, -0.2 + comp * (m + 1) / 3.2, 0.1 - 0.05 * (m + 1) / 3.2) * k * 1.2
    g, h = clarao(T, t, 0.25, 0.45, 0.55, 0.05, 1.0)
    G, H = G + g, H + h
    m = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.018, 0.55, 0.05) * 1.3 + T.ring(0.07 * m, 0.012, 0.55, 0.05) * 1.2
    G += estouro(T, t, 0.27, 0.7, 10, 4, 0.55, 0.05, 0.35, 0.012)
    return G * env, H * env


_BUMERANGUE = [(0, -0.2), (0.4, -0.5), (1.0, -0.35), (0.55, -0.1), (0.3, 0.2), (0, 0.05), (-0.3, 0.2), (-0.55, -0.1), (-1.0, -0.35), (-0.4, -0.5)]


def batarangue_robin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.85)
    if 0 < u < 1:
        a = math.pi * u * 2
        x = -0.6 + 0.6 * (1 - math.cos(a)) * 0.95
        y = -0.35 * math.sin(a)
        g, h = icone(T, poe(_BUMERANGUE, x, y, 0.16, t * 25), 1.2, 0.5)
        G, H = G + g, H + h
        pts = [(-0.6 + 0.6 * (1 - math.cos(math.pi * v * 2)) * 0.95, -0.35 * math.sin(math.pi * v * 2)) for v in np.linspace(max(0, u - 0.15), u, 10)]
        G += T.polyline(pts, 0.01) * 0.8
    g2, h2 = clarao(T, t, 0.38, 0.55, 0.54, 0.0, 0.9)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.42, 0.65, 3, 4, 0.54, 0.0, 0.25, 0.009)
    return G * env, H * env


def robin_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        g, h = icone(T, poe(_BUMERANGUE, lado * 0.2, -0.05 + 0.03 * math.sin(t * 6 + lado), 0.08, lado * 0.3), 1.1, 0.5)
        G, H = G + g, H + h
    capa = [(-0.15 + 0.3 * v, 0.1 + 0.25 + 0.04 * math.sin(v * 8 + t * 6)) for v in np.linspace(0, 1, 16)]
    G += T.polyline(capa, 0.02) * 1.0
    G += T.gauss(0, 0.05, 0.2) * 0.4
    return G, H


def ataque_em_dupla(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, (x0, y0, x1, y1, a0) in enumerate(((-0.6, -0.5, 0.9, 0.35, 0.0), (-0.6, 0.35, 0.9, -0.5, 0.08))):
        u = ease_in(rel(t, a0, a0 + 0.35), 1.6)
        if 0 < u < 1:
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            xr, yr = x0 + (x1 - x0) * max(0, u - 0.3), y0 + (y1 - y0) * max(0, u - 0.3)
            G += T.tapered([(xr, yr, x, y, 1.0)], 0.08) * 1.2
            H += T.lines([(xr, yr, x, y, 1.0)], 0.008) * 1.0
            if j == 1:
                for lado in (-1, 1):
                    asa = [(lado * px, py) for px, py in ASA]
                    g, h = icone(T, poe(asa, x, y, 0.12), 0.9, 0.5)
                    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.2, 0.45, 0.2, -0.05, 1.4, 1.4)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.25, 0.75, 0.05, 0.6, 0.04, -0.05)
    G += estouro(T, t, 0.25, 0.8, 16, 4, 0.2, -0.05, 0.55, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Luigi

def bola_de_fogo_verde(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.6)
    if 0 < u < 1:
        x = -0.6 + 1.15 * u
        y = 0.3 - 0.3 * abs(math.sin(u * math.pi * 3))
        g, h = icone(T, poe(CHAMA, x, y, 0.19, -math.pi / 2 + 0.3 * math.sin(t * 20)), 1.3, 0.6)
        G, H = G + g, H + h * 1.6
        pts = [(-0.6 + 1.15 * v, 0.3 - 0.3 * abs(math.sin(v * math.pi * 3))) for v in np.linspace(max(0, u - 0.2), u, 10)]
        G += T.polyline(pts, 0.03) * 0.7
    g2, h2 = clarao(T, t, 0.55, 0.75, 0.55, 0.3, 0.9)
    G, H = G + g2, H + h2
    for m in range(4):
        kk = pulso(t, 0.58, 1.0)
        g3, h3 = icone(T, poe(CHAMA, 0.45 + 0.07 * m, 0.25, 0.06 * kk), kk, 0.6)
        G, H = G + g3, H + h3
    return G * env, H * env


def poltergust(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    G += T.polys([([(-0.55, -0.04), (0.75, -0.4), (0.75, 0.4), (-0.55, 0.04)], 1.0)], 0.05) * k * 0.25
    G += T.lines([(-0.75, 0.0, -0.55, 0.0, 1.0)], 0.06) * k * 1.1
    G += T.ring(0.06, 0.02, -0.55, 0.0) * k * 1.2
    for j in range(5):
        v = 1 - ((t * 2 + j / 5) % 1)
        x = -0.55 + 1.2 * v
        G += T.ring(0.03 + 0.3 * v, 0.012, x, 0.0, 0.5) * k * (1 - v) * 1.3
    G += converge(T, t, 0.1, 0.9, 20, 4, -0.55, 0.0, 1.0)
    a = t * 15
    G += T.arc_band(0.2, 0.03, a, a + 4, 0.5, 0, 0.55, 0.0, 1.0) * k * 1.0
    return G * env, H * env


def luigi_preparo(T, t, rng):
    G, H = vazio(T)
    treme = 0.02 * math.sin(t * 50)
    G += T.gauss(treme, 0.05, 0.14, 0.1) * 0.9
    G += T.arc_band(0.12, 0.04, math.pi, TAU, 1.0, 0, treme, -0.02, 0.0) * 1.2
    q = np.random.default_rng(int(t * 15))
    for _ in range(5):
        a = q.uniform(-math.pi, 0)
        G += T.lines([(0.2 * math.cos(a), 0.05 + 0.2 * math.sin(a), 0.3 * math.cos(a), 0.05 + 0.3 * math.sin(a), 1.0)], 0.008) * 1.2
    return G, H


def missil_luigi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.32), 2.2)
    k = 1 - rel(t, 0.32, 0.38)
    if k > 0:
        x = -0.85 + 1.25 * u
        G += T.gauss(x, 0.0, 0.1, 0.07) * k * 1.2
        G += T.arc_band(0.08, 0.035, -math.pi / 2, math.pi / 2, 1.0, 0, x + 0.05, 0.0, 0.0) * k * 1.2
        G += T.tapered([(x - 0.7, 0.0, x - 0.08, 0.0, 1.0)], 0.12) * k * 0.9
        H += T.gauss(x + 0.08, 0.0, 0.03) * k * 1.5
    g, h = clarao(T, t, 0.3, 0.55, 0.45, 0.0, 1.7, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.32, 0.8, 0.05, 0.75, 0.05, 0.0)
    G += estouro(T, t, 0.32, 0.9, 20, 6, 0.45, 0.0, 0.8, 0.015)
    g2, h2 = _tontas(T, t, 0.5, 1.0, 0.45, -0.25, 4, 0.14, 0.04)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Princesa Peach

def sombrinha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.1, 0.4), 2.5)
    k = 1 - rel(t, 0.88, 1)
    if t > 0.02 and k > 0:
        cx, cy = 0.0, -0.15
        larg = 0.08 + 0.32 * abre
        topo = [(cx + larg * math.cos(a), cy - 0.22 * math.sin(a) * (0.3 + 0.7 * abre)) for a in np.linspace(0, math.pi, 20)]
        borda = [(cx - larg + 2 * larg * m / 10, cy + 0.03 * math.sin(m * math.pi) - 0.03 * (m % 2)) for m in range(11)][::-1]
        g, h = icone(T, topo + borda, k * 1.1, 0.45)
        G, H = G + g, H + h
        G += T.lines([(cx, cy - 0.22 * (0.3 + 0.7 * abre), cx, cy + 0.35, 1.0)], 0.014) * k * 1.1
        G += T.arc_band(0.04, 0.012, 0, math.pi, 1.0, 0, cx - 0.04, cy + 0.35, 0.0) * k * 1.2
    G += particulas(T, t, 0.35, 1.0, 14, 4, 0, -0.2, 0.4, 0.3, 0.011)
    g2, h2 = aura(T, t, 0.4, 1.0, 0.3, 0.1, 0.5)
    return (G + g2) * env, (H + h2) * env


def bolo_de_cura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        for j, (w, y) in enumerate(((0.22, 0.15), (0.16, 0.0))):
            g, h = icone(T, [(-w * s, y), (w * s, y), (w * s, y - 0.13 * s), (-w * s, y - 0.13 * s)], 1.1, 0.45)
            G, H = G + g, H + h
        for m in range(3):
            x = -0.08 + 0.08 * m
            G += T.lines([(x * s, -0.13 * s, x * s, -0.22 * s, 1.0)], 0.012) * 1.2
            g2, h2 = icone(T, poe(CHAMA, x * s, -0.26 * s, 0.025 * s), 1.2, 0.6)
            G, H = G + g2, H + h2 * 1.5
    w = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if w > 0:
        g3, h3 = icone(T, poe(CORACAO, 0.0, -0.45, 0.13 * w), 1.3, 0.5)
        G, H = G + g3, H + h3
    g4, h4 = aura(T, t, 0.5, 1.0, 0.35, 0.0, 0.8)
    G += anel(T, t, 0.55, 0.95, 0.1, 0.55, 0.03, 0.0)
    return (G + g4) * env, (H + h4) * env


def peach_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(COROA, 0, -0.1, 0.16), 1.2, 0.5)
    G, H = G + g, H + h
    for j in range(3):
        H += T.gauss(-0.1 + 0.1 * j, -0.2, 0.012) * (1.5 + math.sin(t * 12 + j))
    for j in range(3):
        u = ((t * 1.3) + j / 3) % 1
        g2, h2 = cheio(T, poe(CORACAO, -0.2 + 0.2 * j, 0.15 - 0.35 * u, 0.04), (1 - u) * 1.3)
        G, H = G + g2, H + h2
    return G, H


def vibe_da_princesa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = rel(t, 0.05 + 0.12 * j, 0.6 + 0.12 * j)
        if 0 < u < 1:
            G += T.ring(0.1 + 0.9 * ease_out(u, 2), 0.035 * (1 - 0.5 * u), 0.0, 0.1, 1.8) * (1 - u) * 1.2
    q = np.random.default_rng(5)
    for j in range(12):
        x0 = q.uniform(-0.8, 0.8)
        u = rel(t, 0.1 + 0.04 * j, 0.7 + 0.03 * j)
        if 0 < u < 1:
            forma = CORACAO if j % 2 else estrela_pts(5, 0.45)
            g, h = cheio(T, poe(forma, x0 + 0.05 * math.sin(u * 8 + j), 0.3 - 0.6 * u, 0.04), (1 - rel(u, 0.75, 1)) * 1.3)
            G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        G += T.gauss(x, 0.1, 0.15, 0.2) * pulso(t, 0.4, 1.0) * 0.5
    return G * env, H * env


REGISTRO = [
    ("punho_do_deus_do_trovao", punho_do_deus_do_trovao, GRANDE, "Heihachi · o soco com os raios", False),
    ("postura_demoniaca", postura_demoniaca, GRANDE, "Heihachi · a aura escura e os chifres", False),
    ("heihachi_preparo", heihachi_preparo, MEDIA, "Heihachi · as faíscas no punho (Preparo, laço)", True),
    ("raio_do_mishima", raio_do_mishima, GRANDE, "Heihachi · o raio enorme", False),
    ("punho_gigante_jake", punho_gigante_jake, GRANDE, "Jake · o punho que incha", False),
    ("escudo_elastico_jake", escudo_elastico_jake, GRANDE, "Jake · a cúpula amarela no aliado", False),
    ("jake_preparo", jake_preparo, MEDIA, "Jake · o corpo inchando (Preparo, laço)", True),
    ("jake_gigante", jake_gigante, GRANDE, "Jake · a pata gigante pisando", False),
    ("mordida_de_marceline", mordida_de_marceline, GRANDE, "Marceline · as presas e a vida voltando", False),
    ("baixo_machado", baixo_machado, GRANDE, "Marceline · o baixo-machado e as notas", False),
    ("marceline_preparo", marceline_preparo, MEDIA, "Marceline · as asas e os olhos vermelhos (Preparo, laço)", True),
    ("forma_de_morcego", forma_de_morcego, GRANDE, "Marceline · as asas de morcego varrendo", False),
    ("bastao_retratil", bastao_retratil, GRANDE, "Robin · o bastão estendendo", False),
    ("batarangue_robin", batarangue_robin, GRANDE, "Robin · o bumerangue de pássaro", False),
    ("robin_preparo", robin_preparo, MEDIA, "Robin · os dois bumerangues e a capa (Preparo, laço)", True),
    ("ataque_em_dupla", ataque_em_dupla, GRANDE, "Robin · o X com o Morcego", False),
    ("bola_de_fogo_verde", bola_de_fogo_verde, GRANDE, "Luigi · a bola de fogo verde quicando", False),
    ("poltergust", poltergust, GRANDE, "Luigi · o aspirador sugando", False),
    ("luigi_preparo", luigi_preparo, MEDIA, "Luigi · a cabeça baixa tremendo (Preparo, laço)", True),
    ("missil_luigi", missil_luigi, GRANDE, "Luigi · o voo de cabeça e o impacto", False),
    ("sombrinha", sombrinha, GRANDE, "Princesa Peach · a sombrinha abrindo", False),
    ("bolo_de_cura", bolo_de_cura, GRANDE, "Princesa Peach · o bolo e o coração", False),
    ("peach_preparo", peach_preparo, MEDIA, "Princesa Peach · a coroa e os corações (Preparo, laço)", True),
    ("vibe_da_princesa", vibe_da_princesa, GRANDE, "Princesa Peach · as ondas rosa e os corações", False),
]
