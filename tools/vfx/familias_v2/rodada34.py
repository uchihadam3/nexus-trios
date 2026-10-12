"""Rodada 34 das habilidades próprias: Iroh, Patolino, Taz, Coiote, Papa-Léguas e Marvin.

Iroh
- cha_de_jasmim: o bule servindo, o vapor subindo em espiral e as flores de jasmim (Protegido, Acelerado e Purificar).
- redirecionar_do_iroh: o raio entrando pelos dedos, dando a volta na barriga e saindo pela outra mão (Paralisado e Refletir).
- iroh_preparo: o Preparo do Dragão do Oeste — a respiração funda puxando o ar e as brasas (laço).
- dragao_do_oeste: o sopro de fogo enorme em cone, como o hálito de um dragão (Queimando e Protegido).

Patolino
- exijo_atencao: o holofote no rival, os pontos de exclamação e o pato pulando "hu-hu!" (Confuso e Provocado).
- bico_afiado: os bicos abrindo e fechando em todos os rivais (Exposto).
- patolino_preparo: o Preparo do Desastre anunciado — a bomba redonda com o pavio queimando (laço).
- desastre_anunciado: a bomba explodindo em todos e o bico rodopiando para longe (Confuso e Exposto).

Taz
- redemoinho_taz: o redemoinho marrom indo até o rival, levantando pedaços (Enfraquecido e Silenciado).
- mastigar: a bocarra mastigando, os farelos e o brilho de força (Vida e Fortalecido).
- taz_preparo: o Preparo da Fome sem fim — o redemoinho começando a girar e a baba (laço).
- fome_sem_fim: o tornado enorme sugando tudo para o meio e a mordida (Exposto e Vida).

Coiote
- encomenda_acme: a caixa ACME caindo, abrindo e a bomba presa no rival (Preso e Marca explosiva).
- armadilha_montada: a luva de boxe na mola saltando da caixa (Interrompe o Preparo).
- coiote_preparo: o Preparo do Plano infalível — o pavio do foguete queimando até o fim (laço).
- plano_infalivel: o foguete ACME voando, batendo em todos e a explosão (com a fumacinha nele mesmo).

Papa-Léguas
- bip_bip: o risco azul passando num instante e as nuvenzinhas de poeira (Adianta o ataque).
- poeira_na_pista: a cortina de poeira que fica para trás em cima dos rivais (Confuso e Lento).
- velocidade_impossivel: as várias cópias do corredor e a pista de poeira em laço (Acelerado, Vida e Esquiva).

Marvin
- modulador_illudium: o Modulador Explosivo Espacial Illudium Q-36 com a antena piscando e a mira no rival (Marcado e Exposto).
- mira_marciana: o feixe verde da pistola de raios com os anéis (Lento).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, anel, aura, cheio, circulo, clarao, converge, estouro, estrela_pts, flor, icone, onda_no_chao, particulas, poe,
                         raios, surge)


def _raio(T, t, x0, y0, x1, y1, k, w=0.016, seed=0, desvio=0.1):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, desvio)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.6


def _poeira(T, cx, cy, s, k, seed=3, n=10):
    q = np.random.default_rng(seed)
    pts = [(cx + q.normal(0, s), cy + q.normal(0, s * 0.6), k * q.uniform(0.4, 1.0)) for _ in range(n)]
    return T.splats(pts, s * 0.7)


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


def _bomba(T, cx, cy, s, t, k=1.0):
    """A bomba redonda de desenho, com o pavio e a faísca."""
    g, h = icone(T, poe(circulo(22), cx, cy, s), k * 1.1, 0.6)
    pavio = [(cx + s * 0.5, cy - s * 0.85), (cx + s * 0.75, cy - s * 1.2), (cx + s * 1.05, cy - s * 1.3)]
    g = g + T.polyline(pavio, s * 0.1) * k * 1.0
    fx, fy = pavio[-1]
    q = np.random.default_rng(int(t * 40))
    for _ in range(4):
        a = q.uniform(0, TAU)
        g = g + T.lines([(fx, fy, fx + s * 0.35 * math.cos(a), fy + s * 0.35 * math.sin(a), 1.0)], s * 0.05) * k * 1.4
    h = h + T.gauss(fx, fy, s * 0.15) * k * 2.0
    return g, h


# ------------------------------------------------------------------ Iroh

_BULE = [(-0.6, -0.3), (0.5, -0.3), (0.62, 0.0), (0.5, 0.45), (-0.5, 0.45), (-0.62, 0.0)]


def cha_de_jasmim(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        g, h = icone(T, poe(_BULE, -0.38, -0.38, 0.3 * s, 0.35), 1.2, 0.5)
        G, H = G + g, H + h
        G += T.lines([(-0.2, -0.45, -0.02, -0.52, 1.0)], 0.03) * s * 1.2
    u = rel(t, 0.15, 0.5)
    if 0 < u < 1:
        pts = [(-0.02 + 0.05 * v, -0.5 + 0.45 * v * v) for v in np.linspace(0, u, 10)]
        G += T.polyline(pts, 0.015) * 1.2
    for j in range(3):
        v = rel(t, 0.3 + 0.08 * j, 0.95)
        if 0 < v < 1:
            pts = [(0.05 * (j - 1) + 0.06 * math.sin(m * 0.6 + j + t * 6), -0.05 - 0.6 * v * m / 15) for m in range(16)]
            G += T.polyline(pts, 0.012) * (1 - v) * 1.1
    for j in range(6):
        a = TAU * j / 6 + t * 1.5
        w = surge(t, 0.4 + 0.04 * j, 0.6 + 0.04 * j) * (1 - rel(t, 0.88, 1))
        if w > 0:
            g2, h2 = icone(T, poe(flor(5, 1.0, 0.3), 0.35 * math.cos(a), 0.05 + 0.3 * math.sin(a), 0.05 * w, a), 1.2, 0.55)
            G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.4, 1.0, 0.38, 0.05, 0.8)
    return (G + g3) * env, (H + h3) * env


def redirecionar_do_iroh(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k1 = pulso(t, 0.0, 0.25)
    if k1 > 0:
        g, h = _raio(T, t, 0.95, -0.7, 0.2, -0.1, k1, 0.016, 1)
        G, H = G + g, H + h
    u = rel(t, 0.15, 0.5)
    if 0 < u < 1:
        pts = [(0.28 * math.cos(TAU * v * 0.95), 0.05 + 0.22 * math.sin(TAU * v * 0.95)) for v in np.linspace(0, u, 30)]
        G += T.polyline(pts, 0.022) * 1.3
        H += T.polyline(pts, 0.007) * 1.4
        G += T.gauss(0.0, 0.05, 0.12) * 0.6
    k2 = pulso(t, 0.45, 0.75)
    if k2 > 0:
        g2, h2 = _raio(T, t, -0.2, -0.1, -0.85, 0.0, k2, 0.022, 2)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.5, 0.72, -0.8, 0.0, 1.0)
    G, H = G + g3, H + h3
    G += raios(T, t, 0.5, 0.85, 5, 3, -0.8, 0.0, 0.3, 0.009)
    return G * env, H * env


def iroh_preparo(T, t, rng):
    G, H = vazio(T)
    u = (t * 1.5) % 1
    G += converge(T, u, 0.0, 1.0, 12, int(t * 1.5), 0.0, 0.05, 0.45)
    b = math.sin(math.pi * u)
    G += T.gauss(0, 0.05, 0.12 + 0.05 * b) * (0.6 + 0.5 * b)
    H += T.gauss(0, 0.05, 0.04) * (1.0 + 0.8 * b)
    q = np.random.default_rng(int(t * 10))
    for _ in range(5):
        x = q.uniform(-0.3, 0.3)
        G += T.gauss(x, 0.2 - 0.4 * q.uniform(0, 1), 0.012) * 1.4
    return G, H


def dragao_do_oeste(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.05, 0.75)
    alcance = ease_out(rel(t, 0.05, 0.35), 2)
    if k > 0:
        q = np.random.default_rng(int(t * 30))
        for j in range(26):
            v = q.uniform(0, 1) * alcance
            ang = q.normal(0, 0.18) * (0.3 + v)
            x = -0.75 + 1.5 * v
            y = 0.0 + math.tan(ang) * (x + 0.75) * 0.6
            g, h = icone(T, poe(CHAMA, x, y, 0.04 + 0.12 * v, -math.pi / 2 + ang), k * 1.0, 0.6)
            G, H = G + g, H + h * 1.2
        G += T.gauss(-0.3 + 0.6 * alcance, 0.0, 0.5 * alcance + 0.05, 0.12 + 0.15 * alcance) * k * 0.9
        H += T.gauss(-0.7, 0.0, 0.05) * k * 1.6
    g2, h2 = clarao(T, t, 0.3, 0.6, 0.6, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    G += particulas(T, t, 0.35, 1.0, 22, 5, 0.6, 0.0, 0.25, 0.6, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Patolino

def exijo_atencao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.9)
    G += T.polys([([(0.35, -1.0), (0.45, -1.0), (0.75, 0.35), (0.05, 0.35)], 1.0)], 0.03) * k * 0.35
    G += T.gauss(0.4, 0.3, 0.3, 0.06) * k * 0.8
    for j in range(3):
        s = surge(t, 0.15 + 0.08 * j, 0.35 + 0.08 * j) * (1 - rel(t, 0.85, 1))
        if s > 0:
            x = 0.15 + 0.25 * j
            y = -0.45 - 0.05 * (j % 2)
            G += T.lines([(x, y - 0.12 * s, x, y + 0.02 * s, 1.0)], 0.025) * 1.3
            G += T.gauss(x, y + 0.08 * s, 0.02) * s * 1.6
    u = rel(t, 0.05, 0.85)
    if 0 < u < 1:
        x = -0.6 + 0.15 * math.sin(u * TAU * 2)
        y = 0.15 - 0.3 * abs(math.sin(u * TAU * 2))
        G += T.gauss(x, y, 0.06) * 0.9
        H += T.gauss(x, y, 0.02) * 1.0
    g, h = _tontas(T, t, 0.4, 1.0, 0.4, -0.15, 3, 0.12, 0.035)
    return (G + g) * env, (H + h) * env


def _bico(T, cx, cy, s, abre, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        a = lado * abre
        pts = [(cx, cy), (cx + s * math.cos(a), cy + s * math.sin(a) + lado * s * 0.05),
               (cx + s * 0.9 * math.cos(a + lado * 0.25), cy + s * 0.9 * math.sin(a + lado * 0.25) + lado * s * 0.22)]
        g, h = icone(T, pts, k * 1.2, 0.6)
        G, H = G + g, H + h
    return G, H


def bico_afiado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.08 * j
        u = rel(t, a0, a0 + 0.5)
        if 0 < u < 1:
            abre = 0.55 * abs(math.sin(u * TAU * 1.5))
            g, h = _bico(T, x - 0.15, 0.0, 0.3, abre, 1 - rel(u, 0.85, 1))
            G, H = G + g, H + h
        for m in range(2):
            g2, h2 = clarao(T, t, a0 + 0.15 + 0.2 * m, a0 + 0.28 + 0.2 * m, x + 0.12, 0.0, 0.4)
            G, H = G + g2, H + h2
    G += particulas(T, t, 0.3, 0.9, 14, 4, 0, 0.0, 0.7, 0.3, 0.012)
    return G * env, H * env


def patolino_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _bomba(T, 0.0, 0.05, 0.16, t)
    G, H = G + g, H + h
    G += T.gauss(0, 0.05, 0.3) * (0.25 + 0.15 * math.sin(t * 12))
    return G, H


def desastre_anunciado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.35))
    if s > 0:
        g, h = _bomba(T, 0.0, 0.0, 0.14 * s, t)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.3, 0.55, 0.0, 0.0, 1.6, 1.6)
    G, H = G + g2, H + h2
    for j in range(2):
        G += anel(T, t, 0.32 + 0.08 * j, 0.85 + 0.05 * j, 0.1, 1.0, 0.05, 0.0)
    G += estouro(T, t, 0.32, 0.9, 20, 5, 0, 0.0, 0.9, 0.015)
    G += onda_no_chao(T, t, 0.32, 0.9, 1.0, 0.35, 1.5)
    u = rel(t, 0.4, 0.95)
    if 0 < u < 1:
        g3, h3 = _bico(T, -0.2 - 0.5 * u, -0.1 - 0.45 * math.sin(math.pi * u), 0.12, 0.25, 1 - rel(u, 0.8, 1))
        G, H = G + g3 * 1.0, H + h3
    for x in (-0.55, 0.0, 0.55):
        g4, h4 = _tontas(T, t, 0.6, 1.0, x, -0.2, 3, 0.1, 0.03)
        G, H = G + g4, H + h4
    return G * env, H * env


# ------------------------------------------------------------------ Taz

def _tornado(T, t, cx, cy, alto, larg, k, seed=0):
    G = 0.0
    for m in range(9):
        v = m / 8
        y = cy - alto * v
        r = larg * (0.25 + 0.75 * v)
        a = t * 30 + m * 0.8 + seed
        G = G + T.arc_band(r, 0.025 + 0.02 * v, a, a + 3.6, 0.3, 0, cx + 0.03 * math.sin(t * 20 + m), y, 1.0) * k * 1.2
    return G


def redemoinho_taz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.45), 1.5)
    k = 1 - rel(t, 0.8, 0.95)
    x = -0.6 + 1.1 * u
    G += _tornado(T, t, x, 0.3, 0.6, 0.25, k)
    q = np.random.default_rng(int(t * 20))
    for _ in range(6):
        a = q.uniform(0, TAU)
        G += T.gauss(x + 0.3 * math.cos(a), 0.0 + 0.25 * math.sin(a), 0.018) * k * 1.3
    g, h = clarao(T, t, 0.42, 0.6, 0.5, 0.0, 0.9)
    G, H = G + g, H + h
    g2, h2 = _tontas(T, t, 0.5, 1.0, 0.5, -0.35, 3, 0.12, 0.035)
    return (G + g2) * env, (H + h2) * env


def _boca(T, cx, cy, s, abre, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        y = cy + lado * abre * s
        arco = [(cx + s * math.cos(a), y + lado * 0.35 * s * math.sin(a)) for a in np.linspace(0, math.pi, 14)]
        g, h = icone(T, arco, k * 1.0, 0.4)
        G, H = G + g, H + h
        dentes = [(cx - 0.8 * s + 0.32 * s * m, y, cx - 0.64 * s + 0.32 * s * m, y - lado * 0.22 * s, 1.0) for m in range(6)]
        G = G + T.lines(dentes, 0.012) * k * 1.3
    return G, H


def mastigar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.7)
    abre = 0.35 * abs(math.sin(t * TAU * 3))
    g, h = _boca(T, 0.0, -0.1, 0.28, abre + 0.03, k)
    G, H = G + g, H + h
    q = np.random.default_rng(5)
    for j in range(12):
        a = q.uniform(0, TAU)
        w = ((t * 2 + j / 12) % 1)
        G += T.gauss(0.3 * w * math.cos(a), -0.1 + 0.3 * w * math.sin(a) + 0.2 * w * w, 0.015) * (1 - w) * k * 1.3
    g2, h2 = aura(T, t, 0.55, 1.0, 0.38, 0.0, 0.9)
    G += anel(T, t, 0.6, 0.95, 0.1, 0.6, 0.03, 0.0)
    return (G + g2) * env, (H + h2) * env


def taz_preparo(T, t, rng):
    G, H = vazio(T)
    G += _tornado(T, t, 0.0, 0.3, 0.45, 0.2, 0.9)
    for j in range(2):
        u = ((t * 1.5) + j / 2) % 1
        G += T.gauss(-0.08 + 0.16 * j, -0.1 + 0.25 * u, 0.012, 0.025) * (1 - u) * 1.3
    return G, H


def fome_sem_fim(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.75)
    G += _tornado(T, t, 0.0, 0.35, 0.9, 0.55, k)
    G += converge(T, t, 0.0, 0.6, 24, 6, 0.0, 0.0, 0.95)
    q = np.random.default_rng(7)
    for j in range(10):
        a = q.uniform(0, TAU)
        u = rel(t, 0.05 + 0.03 * j, 0.5 + 0.03 * j)
        if 0 < u < 1:
            r = 0.9 * (1 - ease_in(u, 2))
            g, h = icone(T, poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], r * math.cos(a + u * 4), r * 0.6 * math.sin(a + u * 4), 0.03, u * 8), 1.1, 0.5)
            G, H = G + g, H + h
    abre = 0.35 * (1 - ease_in(rel(t, 0.55, 0.7), 2))
    s = pulso(t, 0.5, 0.95)
    if s > 0:
        g2, h2 = _boca(T, 0.0, -0.05, 0.45, abre + 0.02, s)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.65, 0.85, 0.0, -0.05, 1.3, 1.3)
    return (G + g3) * env, (H + h3) * env


# ------------------------------------------------------------------ Coiote

def _caixa(T, cx, cy, s, k):
    g, h = icone(T, [(cx - s, cy - s * 0.8), (cx + s, cy - s * 0.8), (cx + s, cy + s * 0.8), (cx - s, cy + s * 0.8)], k * 1.1, 0.45)
    linhas = [(cx - s, cy - s * 0.3, cx + s, cy - s * 0.3, 1.0), (cx - s, cy + s * 0.3, cx + s, cy + s * 0.3, 1.0),
              (cx - s * 0.6, cy - s * 0.1, cx - s * 0.6, cy + s * 0.1, 1.0), (cx - s * 0.2, cy - s * 0.1, cx + s * 0.2, cy + s * 0.1, 1.0),
              (cx + s * 0.4, cy - s * 0.1, cx + s * 0.6, cy + s * 0.1, 1.0)]
    return g + T.lines(linhas, s * 0.05) * k * 1.2, h


def encomenda_acme(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2.2)
    k = 1 - rel(t, 0.45, 0.55)
    if u > 0 and k > 0:
        g, h = _caixa(T, 0.4, -0.9 + 1.0 * u, 0.22, k)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.4, 0.1, 0.7)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.28, 0.6, 0.5, 0.35, 1.2)
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g3, h3 = _bomba(T, 0.4, 0.0, 0.1 * s, t)
        G, H = G + g3, H + h3
        G += T.ring(0.2 * s, 0.012, 0.4, 0.0) * 1.1
        for j in range(4):
            a = TAU * j / 4
            G += T.lines([(0.4 + 0.15 * s * math.cos(a), 0.15 * s * math.sin(a), 0.4 + 0.25 * s * math.cos(a), 0.25 * s * math.sin(a), 1.0)], 0.01) * 1.2
    return G * env, H * env


def armadilha_montada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g, h = _caixa(T, -0.45, 0.15, 0.13 * s, 1.0)
        G, H = G + g, H + h
    u = ease_out(rel(t, 0.2, 0.4), 3) * (1 - ease_in(rel(t, 0.6, 0.8), 2))
    if u > 0:
        xe = -0.45 + 0.9 * u
        pts = [(-0.45 + (xe + 0.45) * m / 16, 0.05 + (0.04 if m % 2 else -0.04)) for m in range(17)]
        G += T.polyline(pts, 0.012) * 1.3
        P, nos = _punho(T, xe + 0.05, 0.05, 2.0, 0)
        G += P * 0.95
        H += nos * 0.4
    g2, h2 = clarao(T, t, 0.35, 0.55, 0.5, 0.05, 1.0)
    G, H = G + g2, H + h2
    g3, h3 = _tontas(T, t, 0.45, 1.0, 0.5, -0.2, 3, 0.12, 0.035)
    return (G + g3) * env, (H + h3) * env


_FOGUETE = [(1.0, 0), (0.6, -0.22), (-0.7, -0.22), (-1.0, -0.45), (-0.9, 0), (-1.0, 0.45), (-0.7, 0.22), (0.6, 0.22)]


def coiote_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(_FOGUETE, 0.05, 0.0, 0.25), 1.1, 0.45)
    G, H = G + g, H + h
    u = (t * 1.2) % 1
    pavio = [(-0.2 - 0.3 * v, 0.0 + 0.08 * math.sin(v * 8)) for v in np.linspace(0, 1 - u, 12)]
    if len(pavio) > 1:
        G += T.polyline(pavio, 0.008) * 1.0
    fx, fy = pavio[-1]
    H += T.gauss(fx, fy, 0.025) * 2.0
    G += T.gauss(fx, fy, 0.05) * 1.2
    return G, H


def plano_infalivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.8)
    if 0 < u < 1:
        x = -0.85 + 1.4 * u
        y = 0.05 - 0.2 * math.sin(math.pi * u) + 0.03 * math.sin(u * 30)
        g, h = icone(T, poe(_FOGUETE, x, y, 0.18), 1.2, 0.45)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.7, y + 0.02, x - 0.18, y, 1.0)], 0.07) * 1.1
        H += T.gauss(x - 0.2, y, 0.04) * 1.8
    g2, h2 = clarao(T, t, 0.38, 0.62, 0.55, 0.0, 1.6, 1.6)
    G, H = G + g2, H + h2
    for x in (-0.5, 0.1, 0.65):
        g3, h3 = clarao(T, t, 0.42, 0.6, x, 0.1, 0.5)
        G, H = G + g3, H + h3
    G += anel(T, t, 0.4, 0.9, 0.1, 1.0, 0.05, 0.05)
    G += estouro(T, t, 0.4, 0.95, 20, 5, 0.3, 0.05, 0.9, 0.015)
    G += onda_no_chao(T, t, 0.4, 0.95, 1.0, 0.35, 1.5)
    w = rel(t, 0.55, 1.0)
    if 0 < w < 1:
        G += _poeira(T, -0.75, -0.1 - 0.15 * w, 0.06 + 0.04 * w, 1 - w, 9, 8) * 0.9
    return G * env, H * env


# ------------------------------------------------------------------ Papa-Léguas

def bip_bip(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.18), 1.4)
    k = 1 - rel(t, 0.35, 0.55)
    if u > 0 and k > 0:
        x = -0.9 + 1.4 * u
        G += T.tapered([(-0.95, 0.0, x, 0.0, 1.0)], 0.12) * k * 1.1
        H += T.lines([(-0.95, 0.0, x, 0.0, 1.0)], 0.01) * k * 1.2
        for j in range(4):
            G += T.lines([(x - 0.3 - 0.1 * j, -0.15 + 0.1 * j, x - 0.7 - 0.1 * j, -0.15 + 0.1 * j, 1.0)], 0.006) * k
    for j in range(5):
        w = rel(t, 0.05 + 0.03 * j, 0.6 + 0.03 * j)
        if 0 < w < 1:
            G += _poeira(T, -0.7 + 0.3 * j, 0.3 - 0.05 * w, 0.04 + 0.04 * w, 1 - w, j, 6) * 1.0
    g, h = clarao(T, t, 0.15, 0.35, 0.5, 0.0, 0.9)
    G, H = G + g, H + h
    G += estouro(T, t, 0.17, 0.6, 10, 3, 0.5, 0.0, 0.35, 0.012)
    return G * env, H * env


def poeira_na_pista(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.3)
    if 0 < u < 1:
        G += T.tapered([(-0.95, 0.25, -0.95 + 1.9 * u, 0.25, 1.0)], 0.06) * 1.0
    for j in range(7):
        x = -0.8 + 0.27 * j
        w = rel(t, 0.05 + 0.04 * j, 0.95)
        if 0 < w < 1:
            cresce = ease_out(w, 2)
            G += _poeira(T, x, 0.15 - 0.25 * cresce, 0.05 + 0.07 * cresce, (1 - rel(w, 0.7, 1)), 10 + j, 7) * 0.45
    for x in (-0.55, 0.0, 0.55):
        g, h = _tontas(T, t, 0.5, 1.0, x, -0.3, 3, 0.1, 0.03)
        G, H = G + g, H + h
    return G * env, H * env


def velocidade_impossivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    for m in range(5):
        a = t * 14 - m * 0.35
        x, y = 0.45 * math.cos(a), 0.1 + 0.2 * math.sin(a)
        G += T.gauss(x, y, 0.05, 0.08) * k * (1 - m / 5) * 1.2
        if m == 0:
            H += T.gauss(x, y, 0.025) * k * 1.4
    G += T.ring(0.45, 0.025, 0, 0.1, 2.2) * k * 0.9
    for j in range(8):
        a = t * 14 - 1.0 - j * 0.3
        G += _poeira(T, 0.45 * math.cos(a), 0.1 + 0.2 * math.sin(a) + 0.08, 0.03, k * (1 - j / 8), j, 4) * 1.0
    g, h = aura(T, t, 0.5, 1.0, 0.35, 0.05, 0.8)
    G += anel(T, t, 0.55, 0.95, 0.1, 0.6, 0.03, 0.05)
    return (G + g) * env, (H + h) * env


# ------------------------------------------------------------------ Marvin

def modulador_illudium(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        g, h = icone(T, [(-0.55, -0.05), (-0.25, -0.05), (-0.25, 0.12), (-0.55, 0.12)], s * 1.1, 0.45)
        G, H = G + g, H + h
        G += T.lines([(-0.4, -0.05, -0.4, -0.25 * s - 0.05, 1.0)], 0.012) * s * 1.2
        pis = 0.5 + 0.5 * math.sin(t * 40)
        H += T.gauss(-0.4, -0.25 * s - 0.07, 0.025) * s * (1 + pis) * 1.5
        G += T.gauss(-0.4, -0.25 * s - 0.07, 0.05) * s * pis * 1.0
    u = rel(t, 0.3, 0.6)
    if 0 < u < 1:
        pts = [(-0.4 + 0.85 * v, -0.3 - 0.25 * math.sin(math.pi * v)) for v in np.linspace(0, u, 14)]
        G += T.polyline(pts, 0.008) * 1.0
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.18 * m, 0.02, 0.45, 0.0) * 1.3 + T.ring(0.09 * m, 0.014, 0.45, 0.0) * 1.2
        G += T.lines([(0.45 - 0.26 * m, 0.0, 0.45 + 0.26 * m, 0.0, 1.0), (0.45, -0.26 * m, 0.45, 0.26 * m, 1.0)], 0.008) * 1.2
    g2, h2 = clarao(T, t, 0.55, 0.72, 0.45, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


def mira_marciana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.gauss(-0.65, 0.0, 0.05) * pulso(t, 0.0, 0.3) * 1.4
    k = pulso(t, 0.15, 0.7)
    if k > 0:
        G += T.tapered([(-0.65, 0.0, 0.55, 0.0, 1.0)], 0.06 * k + 0.01) * 1.3
        H += T.lines([(-0.65, 0.0, 0.55, 0.0, 1.0)], 0.014) * k * 1.6
    for j in range(4):
        v = ((t * 2.5) + j / 4) % 1
        x = -0.6 + 1.15 * v
        G += T.ring(0.06 + 0.02 * math.sin(v * 6), 0.012, x, 0.0, 0.6) * k * 1.3
    g, h = clarao(T, t, 0.25, 0.65, 0.55, 0.0, 1.0)
    G, H = G + g, H + h
    G += estouro(T, t, 0.3, 0.8, 12, 4, 0.55, 0.0, 0.4, 0.012)
    return G * env, H * env


REGISTRO = [
    ("cha_de_jasmim", cha_de_jasmim, GRANDE, "Iroh · o bule, o vapor e as flores de jasmim", False),
    ("redirecionar_do_iroh", redirecionar_do_iroh, GRANDE, "Iroh · o raio dando a volta na barriga", False),
    ("iroh_preparo", iroh_preparo, MEDIA, "Iroh · a respiração funda e as brasas (Preparo, laço)", True),
    ("dragao_do_oeste", dragao_do_oeste, GRANDE, "Iroh · o sopro de fogo em cone", False),
    ("exijo_atencao", exijo_atencao, GRANDE, "Patolino · o holofote e as exclamações", False),
    ("bico_afiado", bico_afiado, GRANDE, "Patolino · os bicos em todos os rivais", False),
    ("patolino_preparo", patolino_preparo, MEDIA, "Patolino · a bomba com o pavio queimando (Preparo, laço)", True),
    ("desastre_anunciado", desastre_anunciado, GRANDE, "Patolino · a bomba explodindo e o bico voando", False),
    ("redemoinho_taz", redemoinho_taz, GRANDE, "Taz · o redemoinho marrom", False),
    ("mastigar", mastigar, GRANDE, "Taz · a bocarra mastigando", False),
    ("taz_preparo", taz_preparo, MEDIA, "Taz · o redemoinho começando (Preparo, laço)", True),
    ("fome_sem_fim", fome_sem_fim, GRANDE, "Taz · o tornado sugando tudo e a mordida", False),
    ("encomenda_acme", encomenda_acme, GRANDE, "Coiote · a caixa ACME e a bomba presa", False),
    ("armadilha_montada", armadilha_montada, GRANDE, "Coiote · a luva de boxe na mola", False),
    ("coiote_preparo", coiote_preparo, MEDIA, "Coiote · o pavio do foguete queimando (Preparo, laço)", True),
    ("plano_infalivel", plano_infalivel, GRANDE, "Coiote · o foguete ACME e a explosão", False),
    ("bip_bip", bip_bip, GRANDE, "Papa-Léguas · o risco azul e a poeira", False),
    ("poeira_na_pista", poeira_na_pista, GRANDE, "Papa-Léguas · a cortina de poeira", False),
    ("velocidade_impossivel", velocidade_impossivel, GRANDE, "Papa-Léguas · as cópias correndo em laço", False),
    ("modulador_illudium", modulador_illudium, GRANDE, "Marvin · o Modulador Illudium Q-36 e a mira", False),
    ("mira_marciana", mira_marciana, GRANDE, "Marvin · o feixe verde com os anéis", False),
]
