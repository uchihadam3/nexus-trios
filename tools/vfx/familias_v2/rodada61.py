"""Rodada 61 das habilidades próprias: Dexter, Aku, Megamente, Vilgax, Cosmo e Wanda e Steve.

Dexter
- raio_do_laboratorio: a pistola de raio do laboratório e o raio elétrico no rival (Eletrificado).
- gerador_de_carga: o gerador com as bobinas acendendo e os raios correndo para o trio (Carga e Acelerado).
- dexter_preparo: o Preparo do Robô gigante — o controle remoto e a tela com as barras subindo (laço).
- robo_gigante_dexter: o punho de metal gigante do robô descendo e prendendo o rival (Preso).

Aku
- olhos_de_laser_aku: os olhos de fogo verde do Aku e os dois lasers no rival (Amaldiçoado).
- forma_sem_forma: o corpo de sombra se desfazendo em fumaça e voltando (Esquiva e Protegido).
- aku_preparo: o Preparo do Portal do tempo — as sobrancelhas de chamas e o redemoinho escuro (laço).
- portal_do_tempo_aku: o portal do tempo abrindo e puxando todos os rivais (Amaldiçoado e atrasa o Preparo).

Megamente
- arma_de_desidratar: a arma de desidratar e o rival virando um cubinho azul (Preso).
- disfarce_megamente: o relógio do disfarce, a imagem piscando e o rival confuso (Esquiva e Confuso).
- megamente_preparo: o Preparo do Robô mecha — a cabeçona azul e as engrenagens girando (laço).
- robo_mecha: o braço do robô mecha com a garra socando o rival.

Vilgax
- tentaculos_vilgax: os tentáculos do rosto agarrando o rival (Preso).
- armadura_de_batalha_vilgax: as placas da armadura fechando e o escudo (Escudo e Fortalecido).
- vilgax_preparo: o Preparo do Soco planetário — o punho enorme com as veias verdes brilhando (laço).
- soco_planetario: o soco que faz o chão afundar como uma cratera.

Cosmo e Wanda
- desejo_de_forca: as varinhas com a estrela, o "puf" e os músculos de luz no trio (Fortalecido e Carga).
- desejo_de_protecao: as coroas, o "puf" e as bolhas cor-de-rosa no trio (Escudo e Regeneração).
- cosmowanda_preparo: o Preparo do Desejo do Timmy — as duas varinhas cruzadas soltando estrelas (laço).
- desejo_do_timmy: a nuvem do "puf" mágico e os rivais virando bagunça (Confuso e Lento).

Steve
- espada_de_diamante_steve: a espada de diamante de pixels cortando em diagonal.
- muro_de_blocos: os blocos de pedra caindo e se empilhando na frente do trio (Escudo e Protegido).
- golem_de_ferro_steve: os blocos de ferro e a abóbora formando o Golem (invoca).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, COROA, ESCUDO, anel, clarao, corte, engrenagem, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, surge)

ESTRELA = estrela_pts(5, 0.45)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _pistola_raio(T, x, y, s, k):
    """A pistola de raio de ficção: o cano com os anéis e a ponta redonda."""
    pts = [(-0.6, -0.15), (0.3, -0.15), (0.3, 0.1), (-0.1, 0.1), (-0.2, 0.55), (-0.5, 0.55), (-0.4, 0.1), (-0.6, 0.1)]
    g, h = icone(T, poe(pts, x, y, s), k * 1.2, 0.6)
    G = g
    for j in range(3):
        G += T.ring(s * 0.12, s * 0.03, x + s * (0.4 + 0.12 * j), y - s * 0.02, 0.5) * k * 1.1
    G += T.ring(s * 0.1, s * 0.04, x + s * 0.8, y - s * 0.02) * k * 1.2
    return G, h + T.gauss(x + s * 0.8, y - s * 0.02, s * 0.08) * k * 1.5


def _bloco(T, x, y, s, k, cheio=0.5):
    """Um bloco de pixels: o quadrado, a borda e a textura de pixel."""
    pts = [(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]
    g, h = icone(T, pts, k * 1.1, cheio)
    segs = [(x - s * 0.5, y - s * 0.4, x - s * 0.1, y - s * 0.4, 1.0), (x + s * 0.2, y + s * 0.3, x + s * 0.6, y + s * 0.3, 1.0),
            (x - s * 0.6, y + s * 0.5, x - s * 0.3, y + s * 0.5, 1.0)]
    return g + T.lines(segs, s * 0.15) * k * 0.7, h


def _espada_pixel(T, x, y, ang, s, k):
    """A espada de diamante em degraus (pixels): a lâmina em escada, a guarda e o cabo."""
    c, sn = math.cos(ang), math.sin(ang)
    G, H = 0.0, 0.0
    for j in range(7):
        d = s * (0.15 + 0.12 * j)
        px, py = x + c * d, y + sn * d
        g, h = icone(T, [(px - s * 0.06, py - s * 0.06), (px + s * 0.06, py - s * 0.06), (px + s * 0.06, py + s * 0.06), (px - s * 0.06, py + s * 0.06)], k * 1.2, 0.7)
        G, H = G + g, H + h
    G += T.lines([(x + sn * s * 0.15, y - c * s * 0.15, x - sn * s * 0.15, y + c * s * 0.15, 1.0)], s * 0.08) * k
    G += T.lines([(x, y, x - c * s * 0.2, y - sn * s * 0.2, 1.0)], s * 0.08) * k
    return G, H


def _olhos_aku(T, x, y, s, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        g, h = icone(T, poe(CHAMA, x + lado * s * 0.6, y, s * 0.35, lado * 0.3), k * 1.2, 0.7)
        G, H = G + g, H + h
        H += T.gauss(x + lado * s * 0.6, y + s * 0.05, s * 0.12) * k * 2.0
    return G, H


def _cabecona(T, x, y, s, k):
    """A cabeça enorme do Megamente: a cabeça grande em cima e o queixo fino."""
    G = T.ring(s, s * 0.07, x, y - s * 0.2, 1.0) * k * 1.2 + T.gauss(x, y - s * 0.2, s * 0.8) * k * 0.25
    G += T.polyline([(x - s * 0.6, y + s * 0.55), (x, y + s * 0.95), (x + s * 0.6, y + s * 0.55)], s * 0.07) * k * 1.1
    H = 0.0
    for lado in (-1, 1):
        H += T.gauss(x + lado * s * 0.3, y + s * 0.3, s * 0.08) * k * 1.6
    return G, H


def _tentaculo(T, x0, y0, x1, y1, fase, k, w=0.035):
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / L, dx / L
    pts = [(x0 + dx * u + nx * 0.06 * math.sin(math.pi * 2 * u + fase) * u, y0 + dy * u + ny * 0.06 * math.sin(math.pi * 2 * u + fase) * u) for u in np.linspace(0, 1, 20)]
    segs = [(a[0], a[1], b[0], b[1], 1.0 - 0.6 * i / 20) for i, (a, b) in enumerate(zip(pts, pts[1:]))]
    return T.lines(segs, w)


def _varinha(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x, y, x + c * s, y + sn * s, 1.0)], s * 0.05) * k * 1.1
    g, h = icone(T, poe(ESTRELA, x + c * s, y + sn * s, s * 0.22, ang), k * 1.3, 0.8)
    return G + g, h + T.gauss(x + c * s, y + sn * s, s * 0.1) * k * 1.5


def _puf(T, t, a, b, cx, cy, tam, seed):
    """A nuvem do "puf" mágico: as bolas de fumaça abrindo e as estrelinhas."""
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0, 0.0
    q = np.random.default_rng(seed)
    G = 0.0
    for j in range(8):
        a2 = TAU * j / 8 + q.uniform(-0.2, 0.2)
        d = tam * ease_out(u, 2) * q.uniform(0.5, 0.9)
        G += T.gauss(cx + d * math.cos(a2), cy + d * math.sin(a2) * 0.7, tam * (0.15 + 0.2 * u)) * (1 - u) * 0.9
    H = 0.0
    for j in range(5):
        a2 = TAU * j / 5 + 0.3
        d = tam * 1.2 * ease_out(u)
        H += T.gauss(cx + d * math.cos(a2), cy + d * math.sin(a2), 0.012) * (1 - u) * 1.8
    return G, H


# ------------------------------------------------------------------ Dexter

def raio_do_laboratorio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.6, 0.72))
    if k > 0:
        g, h = _pistola_raio(T, -0.65, -0.05, 0.42, k)
        G, H = G + g, H + h
    r = pulso(t, 0.2, 0.6)
    if r > 0:
        G += _zap(T, 650 + int(t * 25), -0.3, -0.06, 0.45, -0.05, 0.016, 5, 0.25) * r * 1.4
        G += _zap(T, 660 + int(t * 25), -0.35, -0.06, 0.45, -0.05, 0.008, 5, 0.4) * r * 1.1
        H += T.lines([(-0.35, -0.06, 0.45, -0.05, 1.0)], 0.006) * r
    g, h = clarao(T, t, 0.3, 0.55, 0.45, -0.05, 1.1, 1.2)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        for j in range(3):
            G += _zap(T, 670 + j + int(t * 15), 0.3, -0.25 + 0.15 * j, 0.6, -0.2 + 0.15 * j, 0.008, 3, 0.4) * m * 1.2
    return G * env, H * env


def gerador_de_carga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        # o gerador: a caixa e as duas bobinas
        G += T.polyline([(-0.75, 0.35), (-0.45, 0.35), (-0.45, 0.15), (-0.75, 0.15), (-0.75, 0.35)], 0.01) * s * 1.1
        for lado in (-1, 1):
            bx = -0.6 + lado * 0.08
            for j in range(4):
                G += T.ring(0.035, 0.008, bx, 0.12 - 0.05 * j, 3.0) * s * 1.1
            H += T.gauss(bx, -0.08, 0.02) * s * (0.6 + 0.4 * math.sin(t * 30 + lado)) * 2.0
        G += _zap(T, 680 + int(t * 25), -0.68, -0.08, -0.52, -0.08, 0.008, 3, 0.5) * s * 1.3
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        u = rel(t, 0.2 + 0.07 * i, 0.45 + 0.07 * i)
        if 0 < u < 1:
            x = -0.6 + (cx + 0.6) * u
            G += _zap(T, 690 + i + int(t * 20), -0.6, -0.08, x, -0.2 - 0.1 * math.sin(math.pi * u), 0.01, 4, 0.3) * 1.3
        m = pulso(t, 0.45 + 0.07 * i, 0.95)
        if m > 0:
            G += T.ring(0.22, 0.012, cx, 0.0, 0.9) * m
            G += _zap(T, 700 + i + int(t * 15), cx - 0.1, -0.3, cx + 0.1, 0.2, 0.007, 3, 0.4) * m
    return G * env, H * env


def dexter_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.polyline([(-0.25, -0.3), (0.25, -0.3), (0.25, 0.2), (-0.25, 0.2), (-0.25, -0.3)], 0.012) * 1.1
    for j in range(5):
        h = 0.08 + 0.32 * (0.5 + 0.5 * math.sin(t * TAU * 2 + j * 0.9))
        x = -0.18 + 0.09 * j
        G += T.polys([([(x - 0.03, 0.15), (x + 0.03, 0.15), (x + 0.03, 0.15 - h), (x - 0.03, 0.15 - h)], 1.0)], 0.003) * 0.9
    G += T.lines([(0.0, -0.3, 0.05, -0.45, 1.0)], 0.01)
    H += T.gauss(0.05, -0.47, 0.02) * (0.5 + 0.5 * math.sin(t * TAU * 4)) * 2.0
    return G, H


def robo_gigante_dexter(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    u = ease_in(rel(t, 0.1, 0.4), 2.3)
    k = 1 - rel(t, 0.6, 0.72)
    if u > 0 and k > 0:
        x, y = 0.45, -1.0 + 0.95 * u
        P, nos = _punho(T, x, y, 3.0, math.pi / 2)
        G += P * k
        H += nos * 0.5 * k
        G += T.lines([(x - 0.05, -1.2, x - 0.05, y - 0.2, 1.0), (x + 0.05, -1.2, x + 0.05, y - 0.2, 1.0)], 0.03) * k
        for j in range(3):
            G += T.ring(0.03, 0.008, x - 0.08 + 0.08 * j, y - 0.15) * k
    g, h = clarao(T, t, 0.38, 0.62, 0.45, -0.05, 1.8, 1.7)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.4, 0.9, 0.9, 0.38, 1.6)
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        for j in range(3):
            G += T.ring(0.15, 0.014, 0.45, -0.15 + 0.15 * j, 3.0) * m * 1.2
    G += estouro(T, t, 0.4, 0.85, 16, 710, 0.45, -0.05, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Aku

def olhos_de_laser_aku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.65, 0.8))
    if k > 0:
        g, h = _olhos_aku(T, -0.55, -0.3, 0.28, k)
        G, H = G + g, H + h
    r = pulso(t, 0.2, 0.6)
    if r > 0:
        for lado in (-1, 1):
            G += T.tapered([(-0.55 + lado * 0.17, -0.3, 0.45, -0.1 + lado * 0.04, 1.0)], 0.03) * r * 1.3
            H += T.lines([(-0.55 + lado * 0.17, -0.3, 0.45, -0.1 + lado * 0.04, 1.0)], 0.008) * r * 1.4
    g, h = clarao(T, t, 0.3, 0.55, 0.45, -0.1, 1.2, 1.2)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += T.ring(0.15, 0.012, 0.45, -0.45) * m * 1.2
        g, h = icone(T, poe(CHAMA, 0.45, -0.45, 0.07), m, 0.7)
        G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 14, 711, 0.45, -0.05, 0.2, 0.5, 0.012)
    return G * env, H * env


def forma_sem_forma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desfaz = pulso(t, 0.1, 0.8)
    q = np.random.default_rng(712)
    for j in range(14):
        a, d = q.uniform(0, TAU), q.uniform(0.0, 0.3)
        x = d * math.cos(a) + 0.3 * desfaz * math.cos(a)
        y = -0.05 + d * math.sin(a) * 1.3 + 0.3 * desfaz * math.sin(a) - 0.2 * desfaz
        G += T.gauss(x, y, 0.06 + 0.06 * desfaz) * (0.6 + 0.4 * (1 - desfaz)) * 0.7
    g, h = _olhos_aku(T, 0.0, -0.35, 0.2, 1 - desfaz * 0.8)
    G, H = G + g, H + h
    p = surge(t, 0.5, 0.7) * (1 - rel(t, 0.85, 1))
    if p > 0:
        G += T.ring(0.38 * p, 0.016, 0.0, -0.05, 0.9) * 1.1
    return G * env, H * env


def aku_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _olhos_aku(T, 0.0, -0.4, 0.25, 1.0)
    G, H = G + g, H + h
    for j in range(3):
        a = -t * TAU * 1.5 + TAU * j / 3
        G += T.arc_band(0.18 + 0.08 * j, 0.025, a, a + 3.5, 0.7, 0, 0.0, 0.1, 1.0) * 1.0
    G += T.gauss(0.0, 0.1, 0.15) * 0.4
    return G, H


def portal_do_tempo_aku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.8, 0.95)
    if abre > 0:
        G += T.ring(0.4 * abre, 0.03, 0.0, -0.1, 1.0) * k * 1.3 + T.gauss(0.0, -0.1, 0.3 * abre) * k * 0.5
        for j in range(5):
            a = -t * 12 + TAU * j / 5
            G += T.arc_band(0.1 + 0.06 * j * abre, 0.02, a, a + 3.0, 1.0, 0, 0.0, -0.1, 1.0) * k * 1.1
        # as engrenagens do tempo em volta
        for lado in (-1, 1):
            g, h = icone(T, poe(engrenagem(8), lado * 0.42 * abre, -0.45, 0.08 * abre, t * 3 * lado), k, 0.4)
            G, H = G + g, H + h
    # os rivais sendo puxados para o portal
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        u = rel(t, 0.35 + 0.05 * i, 0.75)
        if 0 < u < 1 and abs(cx) > 0.01:
            x = cx * (1 - 0.3 * ease_in(u))
            G += T.tapered([(cx, 0.1, x, 0.0, 0.8)], 0.025) * (1 - u) * 1.2
        g, h = clarao(T, t, 0.5 + 0.05 * i, 0.72 + 0.05 * i, cx, 0.05, 0.6, 0.9)
        G, H = G + g, H + h
    G += particulas(T, t, 0.3, 1.0, 22, 713, 0.0, -0.1, 0.6, -0.3, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Megamente

def arma_de_desidratar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.55, 0.68))
    if k > 0:
        g, h = _pistola_raio(T, -0.65, -0.05, 0.42, k)
        G, H = G + g, H + h
    u = rel(t, 0.2, 0.45)
    if 0 < u < 1:
        for j in range(5):
            v = (u * 2 + j / 5) % 1
            G += T.ring(0.03 + 0.03 * v, 0.008, -0.35 + 0.8 * v, -0.05, 0.6) * (1 - v) * 1.3
        G += T.tapered([(-0.35, -0.05, -0.35 + 0.8 * u, -0.05, 1.0)], 0.03) * 1.1
    cubo = surge(t, 0.45, 0.62) * (1 - rel(t, 0.88, 1))
    if cubo > 0:
        s = 0.12 * cubo
        G += T.polyline([(0.45 - s, -0.05 - s), (0.45 + s, -0.05 - s), (0.45 + s, -0.05 + s), (0.45 - s, -0.05 + s), (0.45 - s, -0.05 - s)], 0.014) * 1.3
        G += T.polys([([(0.45 - s, -0.05 - s), (0.45 + s, -0.05 - s), (0.45 + s, -0.05 + s), (0.45 - s, -0.05 + s)], 1.0)], 0.003) * 0.4
        G += T.lines([(0.45 - s, -0.05 - s, 0.45 - s * 0.6, -0.05 - s * 1.4, 1.0), (0.45 + s, -0.05 - s, 0.45 + s * 1.4, -0.05 - s * 1.4, 1.0),
                      (0.45 - s * 0.6, -0.05 - s * 1.4, 0.45 + s * 1.4, -0.05 - s * 1.4, 1.0)], 0.01) * 1.1
    g, h = clarao(T, t, 0.4, 0.58, 0.45, -0.05, 0.9, 1.0)
    G, H = G + g, H + h
    return G * env, H * env


def disfarce_megamente(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    # o relógio do disfarce no pulso
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        G += T.ring(0.12, 0.02, -0.2, 0.1) * k * 1.3 + T.lines([(-0.45, 0.1, 0.05, 0.1, 1.0)], 0.05) * k
        H += T.gauss(-0.2, 0.1, 0.03) * k * (0.5 + 0.5 * math.sin(t * 40)) * 2.0
    # a imagem piscando (as faixas horizontais de holograma)
    p = pulso(t, 0.15, 0.85)
    if p > 0:
        for j in range(8):
            y = -0.4 + 0.1 * j
            o = 0.05 * math.sin(t * 50 + j * 2)
            G += T.lines([(-0.2 + o, y, 0.2 + o, y, 1.0)], 0.012) * p * (0.4 + 0.6 * ((j + int(t * 20)) % 2))
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        pts = [(0.5 + 0.12 * u2 * math.cos(-t * 9 + u2 * 9), -0.45 + 0.05 * u2 * math.sin(-t * 9 + u2 * 9)) for u2 in np.linspace(0.05, 1, 24)]
        G += T.polyline(pts, 0.012) * m * 1.3
    return G * env, H * env


def megamente_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _cabecona(T, 0.0, -0.05, 0.32, 1.0)
    G, H = G + g, H + h
    for lado in (-1, 1):
        g, h = icone(T, poe(engrenagem(8), lado * 0.45, -0.3, 0.12, t * 4 * lado), 1.0, 0.4)
        G, H = G + g, H + h
    return G, H


def robo_mecha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    u = ease_in(rel(t, 0.1, 0.35), 2.3)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        x = -0.6 + 0.85 * u
        # o braço de metal em segmentos e a garra
        for j in range(3):
            G += T.lines([(x - 0.55 + 0.17 * j, -0.05, x - 0.4 + 0.17 * j, -0.05, 1.0)], 0.07) * k * (0.8 + 0.2 * j)
            G += T.ring(0.04, 0.01, x - 0.4 + 0.17 * j, -0.05) * k
        for lado in (-1, 1):
            G += T.polyline([(x - 0.05, -0.05), (x + 0.08, -0.05 + lado * 0.1), (x + 0.15, -0.05 + lado * 0.04)], 0.025) * k * 1.2
    g, h = clarao(T, t, 0.33, 0.58, 0.45, -0.05, 1.7, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.35, 0.75, 0.05, 0.7, 0.05, -0.05, 1.0, 1.5)
    G += estouro(T, t, 0.35, 0.8, 16, 714, 0.45, -0.05, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Vilgax

def tentaculos_vilgax(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    u = ease_out(rel(t, 0.05, 0.4), 2)
    k = 1 - rel(t, 0.85, 0.97)
    if u > 0 and k > 0:
        for j in range(4):
            y0 = -0.15 + 0.05 * (j - 1.5)
            tx = -0.5 + 0.95 * u
            ty = -0.05 + 0.12 * (j - 1.5) * (1 - rel(t, 0.4, 0.6))
            G += _tentaculo(T, -0.55, y0, tx, ty, t * 5 + j, k) * 1.2
    m = pulso(t, 0.45, 1.0)
    if m > 0:
        for j in range(3):
            G += T.ring(0.13, 0.012, 0.45, -0.2 + 0.15 * j, 3.0) * m * 1.2
    g, h = clarao(T, t, 0.38, 0.58, 0.45, -0.05, 0.8, 1.0)
    G, H = G + g, H + h
    return G * env, H * env


def armadura_de_batalha_vilgax(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(5):
        u = ease_out(rel(t, 0.05 + 0.06 * j, 0.3 + 0.06 * j), 2.5)
        if u > 0:
            lado = -1 if j % 2 else 1
            y = -0.35 + 0.15 * j
            x0 = lado * (0.6 - 0.45 * u)
            G += T.polys([([(x0 - 0.15, y - 0.06), (x0 + 0.15, y - 0.06), (x0 + 0.12, y + 0.06), (x0 - 0.12, y + 0.06)], 1.0)], 0.003) * (1 - rel(t, 0.85, 0.97)) * 0.9
            G += T.polyline([(x0 - 0.15, y - 0.06), (x0 + 0.15, y - 0.06), (x0 + 0.12, y + 0.06), (x0 - 0.12, y + 0.06), (x0 - 0.15, y - 0.06)], 0.008) * (1 - rel(t, 0.85, 0.97)) * 1.2
            if 0.9 < u < 1:
                H += T.gauss(x0, y, 0.03) * 2.0
    s = surge(t, 0.4, 0.6) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = icone(T, poe(ESCUDO, 0.0, -0.05, 0.4 * s), 0.8, 0.25)
        G, H = G + g, H + h
    G += T.gauss(0.0, -0.05, 0.3, 0.4) * pulso(t, 0.4, 1.0) * 0.3
    return G * env, H * env


def vilgax_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.05, -0.05, 2.6, 0)
    G += P * (0.85 + 0.15 * math.sin(t * TAU * 2))
    H += nos * 0.5
    for j in range(3):
        pts = [(-0.25 + 0.1 * u, -0.1 + 0.05 * j + 0.03 * math.sin(u * 10 + j)) for u in np.linspace(0, 1, 10)]
        H += T.polyline(pts, 0.005) * (0.6 + 0.4 * math.sin(t * TAU * 3 + j)) * 1.5
    G += T.gauss(0.05, -0.05, 0.3) * (0.3 + 0.15 * math.sin(t * TAU * 2))
    return G, H


def soco_planetario(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    u = ease_in(rel(t, 0.1, 0.38), 2.4)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.5 + 0.8 * u, -0.05, 3.6, 0)
        G += P * k
        H += nos * 0.5 * k
        G += T.tapered([(-1.0, -0.05, -0.7 + 0.8 * u, -0.05, 1.0)], 0.18) * k * 0.6
    g, h = clarao(T, t, 0.35, 0.62, 0.45, -0.05, 2.0, 1.9)
    G, H = G + g, H + h
    # a cratera: os anéis no chão e as pedras subindo
    cr = ease_out(rel(t, 0.38, 0.65), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if cr > 0:
        G += (T.ring(0.25 * cr, 0.03, 0.45, 0.38, 3.0) + T.ring(0.4 * cr, 0.02, 0.45, 0.38, 3.0)) * kk * 1.2
    G += onda_no_chao(T, t, 0.38, 0.95, 1.1, 0.38, 1.8)
    G += estouro(T, t, 0.38, 0.9, 20, 715, 0.45, -0.05, 0.8, 0.016)
    G += particulas(T, t, 0.4, 1.0, 22, 716, 0.45, 0.3, 0.4, 0.7, 0.016)
    return G * env, H * env


# ------------------------------------------------------------------ Cosmo e Wanda

def desejo_de_forca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        for lado in (-1, 1):
            g, h = _varinha(T, -0.55 + lado * 0.1, 0.1, -math.pi / 2 + lado * 0.4 + 0.3 * math.sin(t * 20), 0.3, k)
            G, H = G + g, H + h
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = _puf(T, t, 0.25 + 0.06 * i, 0.6 + 0.06 * i, cx, -0.1, 0.25, 717 + i)
        G, H = G + g, H + h
        m = surge(t, 0.35 + 0.06 * i, 0.55 + 0.06 * i) * (1 - rel(t, 0.85, 1))
        if m > 0:
            for lado in (-1, 1):
                pts = [(0, 0.3), (0.5 * lado, 0.25), (0.75 * lado, 0.0), (0.7 * lado, -0.45), (0.85 * lado, -0.75), (0.6 * lado, -0.8), (0.5 * lado, -0.4),
                       (0.3 * lado, -0.35), (0.15 * lado, -0.15), (0, -0.1)]
                g, h = icone(T, poe(pts, cx + lado * 0.04, -0.4, 0.1 * m), 1.0, 0.5)
                G, H = G + g, H + h
    return G * env, H * env


def desejo_de_protecao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        for lado in (-1, 1):
            g, h = icone(T, poe(COROA, -0.55 + lado * 0.12, -0.45, 0.07), k, 0.6)
            G, H = G + g, H + h
            g, h = _varinha(T, -0.55 + lado * 0.12, 0.05, -math.pi / 2 + lado * 0.3, 0.25, k)
            G, H = G + g, H + h
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = _puf(T, t, 0.25 + 0.06 * i, 0.6 + 0.06 * i, cx, -0.05, 0.22, 720 + i)
        G, H = G + g, H + h
        b = surge(t, 0.35 + 0.06 * i, 0.55 + 0.06 * i) * (1 - rel(t, 0.85, 0.97))
        if b > 0:
            G += T.ring(0.24 * b, 0.016, cx, -0.05) * 1.2 + T.gauss(cx, -0.05, 0.2 * b) * 0.2
            H += T.arc_band(0.18 * b, 0.008, -2.4, -1.6, 1.0, 0, cx, -0.05, 0.0) * 1.4
    for j in range(6):
        r = (t * 1.2 + j / 6) % 1
        G += T.splats([(-0.6 + 0.24 * j, 0.3 - 0.6 * r, math.sin(math.pi * r))], 0.012) * pulso(t, 0.4, 1.0) * 1.3
    return G * env, H * env


def cosmowanda_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        g, h = _varinha(T, lado * 0.12, 0.3, -math.pi / 2 - lado * 0.5, 0.45, 1.0)
        G, H = G + g, H + h
    for j in range(5):
        r = (t + j / 5) % 1
        a = TAU * j / 5
        g, h = icone(T, poe(ESTRELA, 0.3 * r * math.cos(a), -0.15 + 0.3 * r * math.sin(a) - 0.2 * r, 0.04), 1 - r, 0.8)
        G, H = G + g, H + h
    return G, H


def desejo_do_timmy(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.35, 0.45))
    if k > 0:
        for lado in (-1, 1):
            g, h = _varinha(T, -0.55 + lado * 0.1, 0.1, -math.pi / 2 + lado * 0.4, 0.3, k)
            G, H = G + g, H + h
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = _puf(T, t, 0.3 + 0.05 * i, 0.75 + 0.05 * i, cx, -0.05, 0.35, 723 + i)
        G, H = G + g, H + h
        m = pulso(t, 0.5, 1.0)
        if m > 0:
            pts = [(cx + 0.11 * u2 * math.cos(-t * 9 + u2 * 9 + i), -0.45 + 0.05 * u2 * math.sin(-t * 9 + u2 * 9 + i)) for u2 in np.linspace(0.05, 1, 24)]
            G += T.polyline(pts, 0.012) * m * 1.3
            G += T.lines([(cx - 0.1, 0.25, cx + 0.1, 0.25, 1.0)], 0.012) * m
            G += T.lines([(cx + 0.08, 0.2, cx + 0.12, 0.25, 1.0), (cx + 0.08, 0.3, cx + 0.12, 0.25, 1.0)], 0.01) * m
    G += particulas(T, t, 0.3, 1.0, 26, 726, 0.0, 0.0, 0.8, 0.5, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Steve

def espada_de_diamante_steve(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.5, 0.6))
    if k > 0:
        ang = -2.2 + 2.3 * ease_in(rel(t, 0.12, 0.3), 2)
        g, h = _espada_pixel(T, -0.3, 0.15, ang, 0.7, k)
        G, H = G + g, H + h
    g, h = corte(T, t, 0.25, 0.48, 0.75, 1.1, 0.06, 0.45, -0.05, 0.05)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.48, 0.45, -0.05, 1.2, 1.2)
    G, H = G + g, H + h
    # os pixelzinhos voando do golpe
    d = rel(t, 0.3, 0.85)
    if 0 < d < 1:
        q = np.random.default_rng(727)
        for _ in range(10):
            a, v = q.uniform(0, TAU), q.uniform(0.4, 1)
            x, y = 0.45 + 0.4 * v * d * math.cos(a), -0.05 + 0.35 * v * d * math.sin(a) + 0.3 * d * d
            s = 0.02 * (1 - d) + 0.004
            G += T.polys([([(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)], 1.0)], 0.002) * (1 - d) * 1.3
    return G * env, H * env


def muro_de_blocos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    for j in range(12):
        col, lin = j % 4, j // 4
        a0 = 0.05 + 0.05 * j
        u = ease_in(rel(t, a0, a0 + 0.15), 2)
        if u > 0:
            x = -0.45 + 0.3 * col
            y_final = 0.3 - 0.2 * lin
            y = -1.0 + (y_final + 1.0) * u
            g, h = _bloco(T, x, y, 0.1, kk)
            G, H = G + g, H + h
            if 0.95 < u <= 1 and rel(t, a0, a0 + 0.2) < 1:
                G += T.splats([(x - 0.1, y_final + 0.1, 1.0), (x + 0.1, y_final + 0.1, 1.0)], 0.012) * 1.2
    m = surge(t, 0.65, 0.8) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for cx in (-0.45, 0.0, 0.45):
            G += T.ring(0.22 * m, 0.012, cx, -0.05, 0.9)
    return G * env, H * env


def golem_de_ferro_steve(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    # os blocos de ferro em T e a abóbora por cima (como se monta o Golem)
    pos = [(0.0, 0.3), (0.0, 0.1), (-0.2, 0.1), (0.2, 0.1)]
    for j, (bx, by) in enumerate(pos):
        u = ease_out(rel(t, 0.05 + 0.08 * j, 0.25 + 0.08 * j), 2.5)
        if u > 0:
            g, h = _bloco(T, bx, by - 0.3 * (1 - u), 0.1, kk, 0.6)
            G, H = G + g, H + h
    a = surge(t, 0.4, 0.55)
    if a > 0:
        g, h = _bloco(T, 0.0, -0.1, 0.1 * a, kk, 0.3)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(lado * 0.04, -0.12, 0.012) * a * kk * 2.0
    g, h = clarao(T, t, 0.5, 0.7, 0.0, 0.0, 1.2, 1.2)
    G, H = G + g, H + h
    G += anel(T, t, 0.55, 0.9, 0.1, 0.7, 0.03, 0.38, 3.0, 1.3)
    G += particulas(T, t, 0.5, 1.0, 14, 728, 0.0, 0.1, 0.3, 0.5, 0.011)
    return G * env, H * env


REGISTRO = [
    ("raio_do_laboratorio", raio_do_laboratorio, GRANDE, "Dexter · a pistola de raio e o choque", False),
    ("gerador_de_carga", gerador_de_carga, GRANDE, "Dexter · o gerador e os raios no trio", False),
    ("dexter_preparo", dexter_preparo, MEDIA, "Dexter · o controle e as barras (Preparo, laço)", True),
    ("robo_gigante_dexter", robo_gigante_dexter, GRANDE, "Dexter · o punho do robô descendo", False),
    ("olhos_de_laser_aku", olhos_de_laser_aku, GRANDE, "Aku · os olhos de fogo e os lasers", False),
    ("forma_sem_forma", forma_sem_forma, GRANDE, "Aku · o corpo de sombra se desfazendo", False),
    ("aku_preparo", aku_preparo, MEDIA, "Aku · os olhos e o redemoinho (Preparo, laço)", True),
    ("portal_do_tempo_aku", portal_do_tempo_aku, GRANDE, "Aku · o portal do tempo puxando", False),
    ("arma_de_desidratar", arma_de_desidratar, GRANDE, "Megamente · o raio e o cubinho", False),
    ("disfarce_megamente", disfarce_megamente, GRANDE, "Megamente · o relógio e o holograma", False),
    ("megamente_preparo", megamente_preparo, MEDIA, "Megamente · a cabeçona e as engrenagens (Preparo, laço)", True),
    ("robo_mecha", robo_mecha, GRANDE, "Megamente · o braço do mecha e a garra", False),
    ("tentaculos_vilgax", tentaculos_vilgax, GRANDE, "Vilgax · os tentáculos agarrando", False),
    ("armadura_de_batalha_vilgax", armadura_de_batalha_vilgax, GRANDE, "Vilgax · as placas fechando", False),
    ("vilgax_preparo", vilgax_preparo, MEDIA, "Vilgax · o punho e as veias (Preparo, laço)", True),
    ("soco_planetario", soco_planetario, GRANDE, "Vilgax · o soco e a cratera", False),
    ("desejo_de_forca", desejo_de_forca, GRANDE, "Cosmo e Wanda · o puf e os músculos de luz", False),
    ("desejo_de_protecao", desejo_de_protecao, GRANDE, "Cosmo e Wanda · as coroas e as bolhas", False),
    ("cosmowanda_preparo", cosmowanda_preparo, MEDIA, "Cosmo e Wanda · as varinhas e as estrelas (Preparo, laço)", True),
    ("desejo_do_timmy", desejo_do_timmy, GRANDE, "Cosmo e Wanda · os puf nos rivais", False),
    ("espada_de_diamante_steve", espada_de_diamante_steve, GRANDE, "Steve · a espada de pixels", False),
    ("muro_de_blocos", muro_de_blocos, GRANDE, "Steve · os blocos caindo e empilhando", False),
    ("golem_de_ferro_steve", golem_de_ferro_steve, GRANDE, "Steve · os blocos formando o Golem", False),
]
