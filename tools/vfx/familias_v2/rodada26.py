"""Rodada 26 das habilidades próprias: Majin Boo, Shiryu, Shun, Saga de Gêmeos, Camus de Aquário, Hades e Minato.

Majin Boo
- raio_de_doce: o raio da antena que transforma em doce (Confuso e Enfraquecido).
- absorcao_boo: a gosma rosa envolvendo e sendo absorvida (Vida, Fortalecido e Provocado).
- boo_preparo: o Preparo da Regeneração total — o corpo virando gosma e borbulhando (laço).
- regeneracao_total: as gotas rosas se juntam de novo e o soco elástico (Exposto).

Shiryu
- escudo_do_dragao: o escudo redondo com o dragão verde e o golpe refletido (Escudo e Refletir).

Shun
- corrente_nebular: a corrente de Andrômeda girando em espiral e prendendo todos (Preso e Lento).
- tempestade_nebular: o vento rosa da Tempestade Nebular girando em volta do trio (Escudo e Protegido).
- corrente_interceptadora: a corrente reta e pontuda que corta o Preparo do rival (Silenciado).

Saga de Gêmeos
- explosao_galactica: as galáxias girando e colidindo em uma explosão (Confuso e Enfraquecido).
- outra_dimensao: o rasgo no espaço que engole o rival (Preparo interrompido, Preso e Confuso).
- sata_imperial: o dedo apontado e o raio que domina a mente (Exposto).

Camus de Aquário
- po_de_diamante: os cristais de gelo brilhantes em rajada (Lento e Marcado).
- circulo_polar: o anel de gelo que se fecha em volta do rival (Preparo reduzido e Silenciado).
- camus_preparo: o Preparo da Execução Aurora — as mãos juntas em forma de jarro com o frio girando (laço).
- execucao_aurora: o jarro de Aquário derramando o frio absoluto em todos (Lento e Congelado).

Hades
- elisios: os campos Elísios: as flores e a luz fria, os rivais presos (Preso e Amaldiçoado).
- sono_eterno: a névoa do sono e as pálpebras se fechando (Dormindo).
- hades_preparo: o Preparo do Juízo dos mortos — a espada erguida e as almas girando (laço).
- juizo_dos_mortos: a espada desce e as almas caem sobre todos (Silenciado e Lento).

Minato
- hiraishin: o raio amarelo do Deus do Trovão Voador: some e aparece na marca (Esquiva).
- marca_voadora: as kunais de três pontas cravam e o Minato aparece em cada uma (Exposto).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (DIAMANTE, ESCUDO, ESPADA, GOTA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, flor, icone,
                         onda_no_chao, particulas, poe, raios, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _elos(T, pts, k=1.0, r=0.022):
    out = 0
    for i in range(0, len(pts) - 1, 1):
        out = out + T.ring(r, r * 0.35, pts[i][0], pts[i][1], 0.6 if i % 2 else 1.0)
    return out * k * 1.3


def _cristal(cx, cy, s, ang):
    return poe([(0, -1), (0.3, -0.3), (0.2, 0.6), (-0.2, 0.6), (-0.3, -0.3)], cx, cy, s, ang)


def _kunai(cx, cy, s, ang):
    return poe([(1.0, 0), (0.3, -0.2), (-0.4, -0.06), (-0.4, 0.06), (0.3, 0.2)], cx, cy, s, ang)


# ------------------------------------------------------------------ Majin Boo

def raio_de_doce(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.05, 0.4)
    k = 1 - rel(t, 0.5, 0.65)
    if u > 0:
        pts = [(-0.6 + 1.25 * v * u, -0.35 + 0.35 * v * u + 0.06 * math.sin(v * 20 + t * 30)) for v in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.03) * k * 1.3
        H += T.polyline(pts, 0.01) * k * 1.2
    s = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    if s > 0:
        doce = [(0.65 + 0.12 * s * math.cos(a), 0.0 + 0.12 * s * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        g, h = icone(T, doce, 1.2, 0.5)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.polys([([(0.65 + lado * 0.12 * s, 0), (0.65 + lado * 0.24 * s, -0.08 * s), (0.65 + lado * 0.24 * s, 0.08 * s)], 1.0)]) * 1.1
        G += T.polyline(_espiral(0.65, 0.0, 0.0, 0.1 * s, 1.5, 0), 0.01) * 0.8
    G += particulas(T, t, 0.4, 1.0, 20, 3, 0.65, 0.0, 0.3, 0.3, 0.012)
    return G * env, H * env


def absorcao_boo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.6)
    q = np.random.default_rng(5)
    for j in range(10):
        a = q.uniform(0, TAU)
        d = 0.8 * (1 - ease_in(u, 1.5))
        if u < 1:
            G += T.gauss(d * math.cos(a), d * math.sin(a) * 0.7, 0.07 * (1 - 0.5 * u)) * 1.2
    g, h = aura(T, t, 0.4, 1.0, 0.4, 0.0, 1.0)
    G, H = G + g, H + h
    for j in range(5):
        k = pulso(t, 0.45 + 0.06 * j, 0.95)
        G += T.ring(0.03 + 0.01 * j, 0.008, -0.25 + 0.12 * j, -0.45 - 0.2 * k) * k * 1.2
    return G * env, H * env


def boo_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(6):
        a = TAU * j / 6 + t * 2
        r = 0.2 + 0.04 * math.sin(t * 6 + j)
        G += T.gauss(r * math.cos(a), r * math.sin(a) * 0.8, 0.12) * 0.8
    for j in range(4):
        u = (t * 1.5 + j / 4) % 1
        G += T.ring(0.03 + 0.03 * u, 0.008, -0.15 + 0.1 * j, 0.2 - 0.5 * u) * (1 - u) * 1.3
    return G, H


def regeneracao_total(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(8)
    junta = ease_out(rel(t, 0.0, 0.35), 2)
    for j in range(12):
        a = q.uniform(0, TAU)
        d = 0.7 * (1 - junta) * q.uniform(0.5, 1)
        if junta < 1:
            g, h = cheio(T, poe(GOTA, -0.3 + d * math.cos(a), d * math.sin(a), 0.06, a), 1.2)
            G, H = G + g, H + h
    u = rel(t, 0.35, 0.6)
    k = 1 - rel(t, 0.65, 0.8)
    if u > 0 and k > 0:
        x = -0.3 + 0.9 * ease_out(u, 2)
        G += T.lines([(-0.3, 0.0, x, 0.0, 1.0)], 0.07) * k * 1.0
        P, nos = _punho(T, x, 0.0, 2.2, 0)
        G += P * 0.9 * k
        H += nos * 0.5 * k
    g2, h2 = clarao(T, t, 0.55, 0.75, 0.65, 0.0, 1.1)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.55, 0.95, 0.08, 0.5, 0.04, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ Shiryu

def escudo_do_dragao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = icone(T, poe(_circ(30), 0, 0, 0.42 * s), 0.9, 0.5)
        G, H = G + g, H + h
        corpo = [(0.25 * s * math.cos(a) * (1 - 0.3 * a / TAU), 0.25 * s * math.sin(a) * (1 - 0.3 * a / TAU)) for a in np.linspace(0, TAU * 1.3, 30)]
        G += T.polyline(corpo, 0.025) * 1.3
        H += T.polyline(corpo, 0.008) * 1.0
    fa = pulso(t, 0.45, 0.7)
    if fa > 0:
        G += T.flare(0.35, -0.1, 0.5 * fa + 0.01, 0.3, 0.02) * 1.3
        G += T.tapered([(0.35, -0.1, 0.9, -0.35, 1.0)], 0.04) * fa * 1.2
    G += anel(T, t, 0.35, 0.85, 0.42, 0.75, 0.03, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ Shun

def corrente_nebular(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.5), 2)
    k = 1 - rel(t, 0.85, 1)
    if u > 0:
        pts = _espiral(0, 0, 0.05, 0.85, 1.5 * u, t * 4, 50)
        G += _elos(T, pts[::1], k)
    for x in (-0.5, 0.0, 0.5):
        e = ease_out(rel(t, 0.5, 0.8), 2)
        if e > 0:
            G += T.arc_band(0.12, 0.015, 0, TAU * e, 0.4, 0, x, 0.1, 1.0) * k * 1.3
            G += T.arc_band(0.12, 0.015, 0, TAU * e, 0.4, 0, x, 0.22, 1.0) * k * 1.3
    return G * env, H * env


def tempestade_nebular(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        pts = _espiral(0, 0.0, 0.1, 0.8, 0.9, j * TAU / 4 + t * 7)
        G += T.polyline([(x, y * 0.6) for x, y in pts], 0.025) * pulso(t, 0.0, 0.9) * 1.2
    G += particulas(T, t, 0.0, 1.0, 40, 6, 0, 0, 0.8, 0.2, 0.014, 0.5)
    G += T.ring(0.6, 0.035, 0, 0, 0.7) * surge(t, 0.35, 0.6) * (1 - rel(t, 0.85, 1)) * 1.1
    return G * env, H * env


def corrente_interceptadora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.3), 3)
    k = 1 - rel(t, 0.55, 0.75)
    if u > 0:
        x1 = -0.7 + 1.4 * u
        pts = [(-0.7 + (x1 + 0.7) * v, 0.0 + 0.04 * math.sin(v * 30)) for v in np.linspace(0, 1, 28)]
        G += _elos(T, pts, k)
        g, h = cheio(T, poe([(1, 0), (0, -0.5), (-0.3, 0), (0, 0.5)], x1, 0.0, 0.1, 0), k * 1.4)
        G, H = G + g, H + h * 1.5
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.7, 0.0, 0.8)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.28, 0.6, 12, 3, 0.7, 0.0, 0.4, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Saga

def _galaxia(T, cx, cy, r, fase, k):
    G = 0
    for j in range(2):
        pts = _espiral(cx, cy, 0.02, r, 0.8, fase + j * math.pi)
        G = G + T.polyline([(x, cy + (y - cy) * 0.6) for x, y in pts], 0.02) * k
    return G + T.gauss(cx, cy, r * 0.3) * k * 1.2


def explosao_galactica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.45), 1.5)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        G += _galaxia(T, -0.6 + 0.6 * u, -0.1, 0.3, t * 10, k * 1.2)
        G += _galaxia(T, 0.6 - 0.6 * u, 0.1, 0.25, -t * 12, k * 1.2)
    g, h = clarao(T, t, 0.42, 0.65, 0, 0, 1.5, 1.6)
    G, H = G + g, H + h
    G += estouro(T, t, 0.42, 0.9, 24, 9, 0, 0, 0.8, 0.015)
    G += particulas(T, t, 0.45, 1.0, 40, 9, 0, 0, 0.9, 0.0, 0.012)
    return G * env, H * env


def outra_dimensao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.7, 0.9))
    if abre > 0:
        fenda = [(0.3 + 0.5 * abre * 0.5 * math.sin(math.pi * v) * (1 if j else -1), -0.6 + 1.2 * v) for j in (0, 1) for v in np.linspace(0, 1, 16)]
        lado_a = fenda[:16]
        lado_b = fenda[16:][::-1]
        g, h = icone(T, lado_a + lado_b, 0.9, 0.6)
        G, H = G + g, H + h
        H += T.gauss(0.3, 0.0, 0.05, 0.4) * abre * 0.8
        q = np.random.default_rng(3)
        for _ in range(12):
            G += T.gauss(0.3 + q.normal(0, 0.05) * abre, q.uniform(-0.5, 0.5), 0.012) * abre * 1.5
    u = ease_in(rel(t, 0.3, 0.7), 2)
    if 0 < u < 1:
        G += T.gauss(-0.4 + 0.7 * u, 0.0, 0.1 * (1 - u) + 0.001) * 1.2
    return G * env, H * env


def sata_imperial(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.6, 0.75))
    if s > 0:
        G += T.lines([(-0.7, 0.0, -0.45, -0.05, 1.0)], 0.04 * s) * 1.3
        H += T.gauss(-0.42, -0.05, 0.03) * 2 * s
    u = rel(t, 0.3, 0.55)
    if 0 < u < 1:
        G += T.lines([(-0.42, -0.05, 0.65, -0.05, 1.0)], 0.05) * pulso(u, 0, 1) * 1.3
        H += T.lines([(-0.42, -0.05, 0.65, -0.05, 1.0)], 0.01) * pulso(u, 0, 1) * 1.5
    for j in range(3):
        G += anel(T, t, 0.5 + 0.08 * j, 0.95, 0.05, 0.35, 0.02, -0.05, 1.0, 1.2)
    k = pulso(t, 0.55, 1.0)
    if k > 0:
        G += T.polyline(_espiral(0.65, -0.05, 0.02, 0.18, 2, -t * 10), 0.012) * k * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Camus

def po_de_diamante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(4)
    for j in range(22):
        a0 = q.uniform(0, 0.3)
        u = rel(t, a0, a0 + 0.4)
        if 0 < u < 1:
            y0 = q.uniform(-0.3, 0.3)
            x = -0.7 + 1.5 * ease_in(u, 1.3)
            y = y0 * (1 - u)
            g, h = icone(T, poe(DIAMANTE, x, y, 0.08, u * 8 + j), (1 - rel(u, 0.8, 1)) * 1.3, 0.7)
            G, H = G + g, H + h * 2
    g2, h2 = clarao(T, t, 0.45, 0.7, 0.75, 0.0, 0.8)
    return (G + g2) * env, (H + h2) * env


def circulo_polar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_out(rel(t, 0.0, 0.45), 2)
    k = 1 - rel(t, 0.85, 1)
    for j in range(10):
        a = TAU * j / 10 + t * 2
        r = 0.6 - 0.25 * fecha
        g, h = icone(T, _cristal(r * math.cos(a), r * 0.7 * math.sin(a), 0.08, a + math.pi / 2), k * 1.2, 0.6)
        G, H = G + g, H + h
    G += T.ring(0.35, 0.03, 0, 0, 0.7) * surge(t, 0.35, 0.55) * k * 1.3
    G += particulas(T, t, 0.3, 1.0, 26, 2, 0, 0, 0.4, 0.3, 0.012)
    return G * env, H * env


def camus_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        P, nos = _punho(T, lado * 0.08, -0.35, 1.4, -math.pi / 2)
        G += P * 0.6
    for j in range(6):
        a = t * 4 + TAU * j / 6
        g, h = icone(T, _cristal(0.3 * math.cos(a), -0.1 + 0.2 * math.sin(a), 0.05, a), 1.1, 0.6)
        G, H = G + g, H + h
    G += T.gauss(0, -0.2, 0.15) * (0.6 + 0.2 * math.sin(t * 8))
    return G, H


def execucao_aurora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.5, 0.65))
    jarro = [(-0.15, -0.75), (0.15, -0.75), (0.1, -0.65), (0.22, -0.5), (0.15, -0.35), (-0.15, -0.35), (-0.22, -0.5), (-0.1, -0.65)]
    if s > 0:
        g, h = icone(T, [(x * s, y) for x, y in jarro], 1.0, 0.5)
        G, H = G + g, H + h
    u = rel(t, 0.2, 0.8)
    if 0 < u < 1:
        q = np.random.default_rng(7)
        pts = []
        for _ in range(200):
            v = q.uniform(0, ease_out(u))
            pts.append((q.normal(0, 0.05 + 0.5 * v), -0.35 + 0.8 * v, (1 - v) * q.uniform(0.4, 1)))
        G += T.splats(pts, 0.016) * 1.3
    for j in range(7):
        c = ease_out(rel(t, 0.5 + 0.03 * j, 0.7 + 0.03 * j), 2) * (1 - rel(t, 0.88, 1))
        if c > 0:
            g2, h2 = icone(T, _cristal(-0.7 + 0.23 * j, 0.35, 0.18 * c, 0), 1.1, 0.6)
            G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Hades

def elisios(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(11)
    for j in range(9):
        k = surge(t, 0.04 * j, 0.35 + 0.04 * j) * (1 - rel(t, 0.88, 1))
        if k > 0:
            g, h = icone(T, poe(flor(5, 1.0, 0.3), q.uniform(-0.8, 0.8), 0.3 + q.uniform(-0.05, 0.1), 0.07 * k, q.uniform(0, 1)), 1.1, 0.5)
            G, H = G + g, H + h
    G += T.gauss(0, -0.3, 0.9, 0.5) * 0.25 * pulso(t, 0.0, 0.95)
    for x in (-0.5, 0.0, 0.5):
        e = ease_out(rel(t, 0.4, 0.75), 2)
        if e > 0:
            G += T.arc_band(0.13, 0.012, 0, TAU * e, 0.4, 0, x, 0.15, 1.0) * (1 - rel(t, 0.88, 1)) * 1.3
    return G * env, H * env


def sono_eterno(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(3)
    k = pulso(t, 0.0, 0.95)
    pts = [(q.normal(0.3, 0.3) + 0.1 * math.sin(t * 2 + j), q.normal(0, 0.15), k * q.uniform(0.3, 0.8)) for j in range(30)]
    G += T.splats(pts, 0.1) * 0.5
    fecha = ease_in(rel(t, 0.3, 0.7), 2)
    for lado in (-1, 1):
        cx = 0.3 + lado * 0.15
        G += T.arc_band(0.1, 0.02, 0.2, math.pi - 0.2, 0.3 + 0.7 * (1 - fecha), 0, cx, -0.1, 1.0) * k * 1.3
    for j in range(3):
        u = rel(t, 0.5 + 0.1 * j, 0.9 + 0.05 * j)
        if 0 < u < 1:
            x, y = 0.5 + 0.1 * j, -0.3 - 0.3 * u
            G += T.lines([(x, y, x + 0.06, y, 1.0), (x + 0.06, y, x, y + 0.06, 1.0), (x, y + 0.06, x + 0.06, y + 0.06, 1.0)], 0.01) * (1 - u) * 1.4
    return G * env, H * env


def hades_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(ESPADA, 0, -0.15, 0.4, 0), 1.0, 0.5)
    G, H = G + g, H + h
    H += T.gauss(0, -0.5, 0.04) * (1.5 + 0.5 * math.sin(t * 8))
    for j in range(5):
        a = t * 3 + TAU * j / 5
        G += T.gauss(0.4 * math.cos(a), 0.0 + 0.25 * math.sin(a), 0.04) * 1.2
    return G, H


def juizo_dos_mortos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.4, 0.55)
    if k > 0:
        g, h = icone(T, poe(ESPADA, 0, -0.8 + 0.7 * desce, 0.5, math.pi), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.22, 0.45, 0, 0.0, 1.3, 1.5)
    G, H = G + g2, H + h2
    q = np.random.default_rng(15)
    for j in range(12):
        a0 = 0.25 + q.uniform(0, 0.3)
        u = rel(t, a0, a0 + 0.35)
        if 0 < u < 1:
            x = q.uniform(-0.8, 0.8)
            y = -0.9 + 1.2 * ease_in(u, 1.5)
            G += T.gauss(x, y, 0.05) * 1.2
            H += T.gauss(x, y, 0.02) * 1.3
            G += T.tapered([(x, y - 0.25, x, y, 0.4)], 0.04)
    G += onda_no_chao(T, t, 0.3, 0.9, 1.0, 0.35, 1.5)
    return G * env, H * env


# ------------------------------------------------------------------ Minato

def hiraishin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k1 = pulso(t, 0.0, 0.25)
    G += T.gauss(-0.6, 0.0, 0.12, 0.25) * k1 * 1.0
    q = np.random.default_rng(int(t * 30))
    kb = pulso(t, 0.15, 0.4)
    if kb > 0:
        bolt = jagged(q, -0.6, 0.0, 0.6, 0.0, 6, 0.08)
        G += T.polyline(bolt, 0.03) * kb * 1.4
        H += T.polyline(bolt, 0.01) * kb * 1.5
    k2 = pulso(t, 0.3, 0.7)
    G += T.gauss(0.6, 0.0, 0.12, 0.25) * k2 * 1.1
    g, h = icone(T, _kunai(0.6, 0.35, 0.25, -math.pi / 2), pulso(t, 0.0, 0.9) * 1.2, 0.6)
    G, H = G + g, H + h
    G += T.lines([(0.55, 0.42, 0.65, 0.42, 1.0)], 0.01) * pulso(t, 0.0, 0.9)
    return G * env, H * env


def marca_voadora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    alvos = [(-0.4, 0.15), (0.2, -0.2), (0.6, 0.2)]
    for j, (x, y) in enumerate(alvos):
        u = rel(t, 0.03 * j, 0.25 + 0.03 * j)
        if u > 0:
            px = -0.85 + (x + 0.85) * min(1, u)
            g, h = icone(T, _kunai(px, y, 0.2, 0), (1 - rel(t, 0.85, 1)) * 1.2, 0.6)
            G, H = G + g, H + h
        aparece = pulso(t, 0.3 + 0.12 * j, 0.5 + 0.12 * j)
        if aparece > 0:
            G += T.flare(x, y, 0.3 * aparece + 0.01, 0.4, 0.02) * 1.2
            g2, h2 = corte(T, t, 0.32 + 0.12 * j, 0.5 + 0.12 * j, 0.7, 0.5, 0.05, x, y)
            G, H = G + g2, H + h2
    return G * env, H * env


REGISTRO = [
    ("raio_de_doce", raio_de_doce, GRANDE, "Boo · o raio que vira doce", False),
    ("absorcao_boo", absorcao_boo, GRANDE, "Boo · a gosma sendo absorvida", False),
    ("boo_preparo", boo_preparo, MEDIA, "Boo · o corpo borbulhando (Preparo, laço)", True),
    ("regeneracao_total", regeneracao_total, GRANDE, "Boo · as gotas se juntando e o soco", False),
    ("escudo_do_dragao", escudo_do_dragao, GRANDE, "Shiryu · o escudo do dragão", False),
    ("corrente_nebular", corrente_nebular, GRANDE, "Shun · a corrente em espiral", False),
    ("tempestade_nebular", tempestade_nebular, GRANDE, "Shun · o vento rosa em volta", False),
    ("corrente_interceptadora", corrente_interceptadora, GRANDE, "Shun · a corrente reta", False),
    ("explosao_galactica", explosao_galactica, GRANDE, "Saga · as galáxias colidindo", False),
    ("outra_dimensao", outra_dimensao, GRANDE, "Saga · o rasgo no espaço", False),
    ("sata_imperial", sata_imperial, GRANDE, "Saga · o dedo e o raio da mente", False),
    ("po_de_diamante", po_de_diamante, GRANDE, "Camus · os cristais em rajada", False),
    ("circulo_polar", circulo_polar, GRANDE, "Camus · o anel de gelo", False),
    ("camus_preparo", camus_preparo, MEDIA, "Camus · as mãos em jarro (Preparo, laço)", True),
    ("aurora_de_camus", execucao_aurora, GRANDE, "Camus · o jarro de Aquário", False),
    ("elisios", elisios, GRANDE, "Hades · os campos Elísios", False),
    ("sono_eterno", sono_eterno, GRANDE, "Hades · a névoa do sono", False),
    ("hades_preparo", hades_preparo, MEDIA, "Hades · a espada e as almas (Preparo, laço)", True),
    ("juizo_dos_mortos", juizo_dos_mortos, GRANDE, "Hades · a espada e as almas caindo", False),
    ("hiraishin", hiraishin, GRANDE, "Minato · o Deus do Trovão Voador", False),
    ("marca_voadora", marca_voadora, GRANDE, "Minato · as kunais e as aparições", False),
]
