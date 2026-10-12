"""Rodada 21 das habilidades próprias: Jill Valentine, Albert Wesker, Lara Croft, Ezio Auditore, Sonic, Shadow, Zero e
Mario.

Jill Valentine
- kit_primeiros_socorros: a maleta com a cruz abre, o spray verde e a cura subindo (Escudo e o aliado levantando).
- cobertura_tatica: o sinal de mão e as setas de avanço do trio (Acelerado e Fortalecido).
- jill_preparo: o Preparo da Resistência adquirida — a seringa da vacina enchendo (laço).
- resistencia_adquirida: a vacina injetada, o DNA girando e o escudo em volta do trio (Protegido).

Albert Wesker
- deslocamento_wesker: o borrão de velocidade sobre-humana em zigue-zague e os óculos escuros brilhando.
- golpe_cruzado: os dois golpes cruzados em X e o sangue (Silenciado e Sangrando).
- supremacia_wesker: os olhos vermelhos de gato acendem e o soco que paralisa.

Lara Croft
- arco_recurvo: o arco tenso, a flecha cruza e a marca do alvo (Marcado e Exposto).
- armadilha_de_cabo: o cabo de escalada dispara e enrola o rival (Preso).
- lara_preparo: o Preparo do Tiro perfeito — a mira do rifle respirando (laço).
- tiro_perfeito: o tiro único e enorme com o rastro e o impacto.

Ezio Auditore
- multidao: a multidão de capuzes brancos em volta e o rival confuso (Confuso e Enfraquecido).
- execucao_em_cadeia: os saltos de um rival ao outro com a lâmina oculta e a águia (Exposto).

Sonic
- homing_attack: a bola azul mirando e acertando, com o escudo de anel dourado no aliado.
- sonic_preparo: o Preparo do Super Sonic — as sete Esmeraldas do Caos girando (laço).
- super_sonic: a explosão dourada do Super Sonic e o rastro de velocidade.

Shadow
- chaos_spear: as lanças de energia amarela voando.
- chaos_control: o relógio do tempo para, o brilho verde da Esmeralda (Preparo atrasado e Lento).
- shadow_preparo: o Preparo da Lança das Esmeraldas — a Esmeralda vermelha pulsando (laço).
- lanca_das_esmeraldas: a chuva de lanças do Caos sobre todos os rivais.

Zero
- raikousen: o avanço relâmpago com o sabre e o rastro elétrico.
- zero_preparo: o Preparo da Sequência final — o Z-Saber verde carregando (laço).
- sequencia_final: o grande corte verde em meia-lua e os raios que paralisam.

Mario
- flor_de_fogo: a flor de fogo e as bolas de fogo quicando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, CHAMA, CRUZ, DIAMANTE, GEMA, SETA, anel, aura, cheio, clarao, converge, corte, estouro, estrela_pts, flor, icone,
                         onda_no_chao, particulas, poe, raios, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


# ------------------------------------------------------------------ Jill

def kit_primeiros_socorros(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = icone(T, [(-0.3 * s, 0.0), (0.3 * s, 0.0), (0.3 * s, 0.35), (-0.3 * s, 0.35)], 1.0, 0.45)
        G, H = G + g, H + h
        g, h = cheio(T, poe(CRUZ, 0, 0.17, 0.1 * s), 1.4)
        G, H = G + g, H + h * 1.5
    spray = rel(t, 0.3, 0.7)
    if 0 < spray < 1:
        q = np.random.default_rng(2)
        pts = [(q.normal(0, 0.12) * spray, -0.05 - 0.6 * spray * q.uniform(0.5, 1), (1 - spray) * q.uniform(0.4, 1)) for _ in range(40)]
        G += T.splats(pts, 0.03) * 1.1
    G += particulas(T, t, 0.4, 1.0, 30, 3, 0, -0.1, 0.5, 0.6, 0.014)
    G += anel(T, t, 0.5, 0.95, 0.1, 0.6, 0.03, 0.0)
    return G * env, H * env


def cobertura_tatica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.5, 0.65))
    if s > 0:
        mao = [(-0.08, 0.2), (-0.1, -0.15), (-0.03, -0.2), (0.0, -0.4), (0.06, -0.38), (0.06, -0.15), (0.12, -0.1), (0.1, 0.2)]
        g, h = icone(T, [(x * 1.5 * s, y * 1.5 * s) for x, y in mao], 1.1, 0.45)
        G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.3 + 0.08 * j, 0.8 + 0.06 * j)
        if 0 < u < 1:
            x = -0.5 + 0.5 * j
            g, h = cheio(T, poe(SETA, x + 0.2 * ease_out(u), 0.3 - 0.1 * j, 0.12, 0), (1 - rel(u, 0.75, 1)) * 1.3)
            G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.35, 0.9, 0.9, 0.38)
    return G * env, H * env


def jill_preparo(T, t, rng):
    G, H = vazio(T)
    corpo = [(-0.5, -0.08), (0.3, -0.08), (0.3, 0.08), (-0.5, 0.08)]
    G += T.polyline(corpo + [corpo[0]], 0.02) * 1.3
    G += T.lines([(0.3, 0.0, 0.6, 0.0, 1.0), (-0.5, -0.14, -0.5, 0.14, 1.0), (-0.7, 0.0, -0.5, 0.0, 1.0)], 0.02) * 1.3
    u = (t * 1.2) % 1
    G += T.polys([([(-0.48, -0.06), (-0.48 + 0.76 * u, -0.06), (-0.48 + 0.76 * u, 0.06), (-0.48, 0.06)], 1.0)]) * 1.0
    H += T.gauss(0.6, 0.0, 0.035) * (0.5 + 0.5 * math.sin(t * 20)) * 2
    return G, H


def resistencia_adquirida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    for fase in (0, math.pi):
        pts = [(0.1 * math.sin(v * 9 + fase + t * 8), -0.5 + v) for v in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.018) * k * 1.2
    for j in range(9):
        y = -0.5 + j / 8
        x = 0.1 * math.sin(y * 9 + 4.5 + t * 8)
        G += T.lines([(-x, y, x, y, 1.0)], 0.008) * k
    g, h = clarao(T, t, 0.0, 0.25, 0, 0, 0.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.35, 0.95, 0.2, 0.85, 0.04, 0.0)
    G += T.ring(0.75, 0.03, 0, 0.0, 0.85) * surge(t, 0.4, 0.7) * (1 - rel(t, 0.85, 1)) * 0.8
    return G * env, H * env


# ------------------------------------------------------------------ Wesker

def deslocamento_wesker(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    pontos = [(-0.75, 0.2), (-0.35, -0.25), (0.05, 0.2), (0.45, -0.2), (0.75, 0.05)]
    u = rel(t, 0.0, 0.55)
    if u > 0:
        total = ease_out(u, 2) * (len(pontos) - 1)
        for i in range(int(total) + 1):
            if i >= len(pontos) - 1:
                break
            f = min(1.0, total - i)
            (x0, y0), (x1, y1) = pontos[i], pontos[i + 1]
            G += T.tapered([(x0, y0, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 1.0)], 0.05) * (1 - rel(t, 0.7, 0.9))
            G += T.gauss(x0, y0, 0.08) * 0.5 * (1 - rel(t, 0.5, 0.8))
    s = surge(t, 0.5, 0.65) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        G += T.polys([([(0.75 + lado * 0.03, 0.0), (0.75 + lado * 0.13, 0.0), (0.75 + lado * 0.12, 0.05), (0.75 + lado * 0.04, 0.05)], 1.0)]) * s * 1.3
    H += T.flare(0.85, 0.0, 0.2 * s + 0.01, 0.4, 0.02) * s
    return G * env, H * env


def golpe_cruzado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for k, (a, t0) in enumerate(((0.8, 0.0), (-0.8, 0.12))):
        g, h = corte(T, t, t0, t0 + 0.35, a, 1.4, 0.09, 0.0, 0.0)
        G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.15, 0.35, 0, 0, 0.9)
    G, H = G + g2, H + h2
    q = np.random.default_rng(5)
    for j in range(8):
        u = rel(t, 0.2, 0.8)
        if 0 < u < 1:
            a = q.uniform(0, TAU)
            d = 0.5 * ease_out(u) * q.uniform(0.5, 1)
            g3, h3 = cheio(T, poe([(0, -1), (0.55, 0.35), (0, 0.8), (-0.55, 0.35)], d * math.cos(a), d * math.sin(a) + 0.3 * u * u, 0.035), (1 - u) * 1.3)
            G, H = G + g3, H + h3
    return G * env, H * env


def supremacia_wesker(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.6, 0.75))
    for lado in (-1, 1):
        olho = [(lado * 0.15 + 0.1 * math.cos(a), -0.2 + 0.05 * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        g, h = cheio(T, olho, 1.3 * s)
        G, H = G + g, H + h * 1.5
        G -= T.lines([(lado * 0.15, -0.25, lado * 0.15, -0.15, 1.0)], 0.015) * s
    k = pulso(t, 0.4, 0.8)
    if k > 0:
        P, nos = _punho(T, -0.2 + 0.4 * ease_out(rel(t, 0.4, 0.55)), 0.15, 3.0, 0)
        G += P * 0.9 * k
        H += nos * 0.5 * k
    g2, h2 = clarao(T, t, 0.5, 0.7, 0.3, 0.15, 1.0)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.5, 0.95, 0.1, 0.6, 0.035, 0.15)
    return np.maximum(G, 0) * env, H * env


# ------------------------------------------------------------------ Lara

def arco_recurvo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    tensao = ease_out(rel(t, 0.0, 0.3), 2)
    solta = rel(t, 0.3, 0.35)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        arco = [(-0.55 + 0.15 * math.cos(a), 0.4 * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 20)]
        G += T.polyline(arco, 0.025) * 1.2 * k
        puxa = 0.2 * tensao * (1 - solta)
        G += T.lines([(-0.55, -0.4, -0.55 - puxa, 0.0, 1.0), (-0.55 - puxa, 0.0, -0.55, 0.4, 1.0)], 0.008) * 1.2 * k
    u = rel(t, 0.33, 0.6)
    if 0 < u < 1:
        x = -0.5 + 1.25 * ease_in(u, 1.4)
        G += T.lines([(x - 0.3, 0.0, x, 0.0, 1.0)], 0.015) * 1.4
        G += T.tapered([(x - 0.6, 0.0, x - 0.3, 0.0, 0.4)], 0.03)
    m = surge(t, 0.6, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.02, 0.7, 0.0) * 1.3 + T.ring(0.07 * m, 0.015, 0.7, 0.0) * 1.3
    g, h = clarao(T, t, 0.58, 0.75, 0.7, 0.0, 0.6)
    return (G + g) * env, (H + h) * env


def armadilha_de_cabo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    if u > 0:
        G += T.lines([(-0.8, 0.1, -0.8 + 1.3 * u, 0.0, 1.0)], 0.012) * 1.3 * (1 - rel(t, 0.5, 0.65))
        G += T.gauss(-0.8 + 1.3 * u, 0.0, 0.04) * 1.3 * (1 - rel(t, 0.3, 0.4))
    enrola = ease_out(rel(t, 0.3, 0.75), 2)
    if enrola > 0:
        for j in range(4):
            y = -0.3 + 0.18 * j
            G += T.arc_band(0.22, 0.02, 0, TAU * enrola, 0.35, 0, 0.5, y, 1.0) * 1.3 * (1 - rel(t, 0.88, 1))
    return G * env, H * env


def lara_preparo(T, t, rng):
    G, H = vazio(T)
    resp = 0.03 * math.sin(t * 6)
    G += T.ring(0.25, 0.015, resp, resp * 0.5) * 1.2
    G += T.lines([(-0.35 + resp, resp * 0.5, -0.1 + resp, resp * 0.5, 1.0), (0.1 + resp, resp * 0.5, 0.35 + resp, resp * 0.5, 1.0),
                  (resp, -0.35 + resp * 0.5, resp, -0.1 + resp * 0.5, 1.0), (resp, 0.1 + resp * 0.5, resp, 0.35 + resp * 0.5, 1.0)], 0.012) * 1.2
    H += T.gauss(resp, resp * 0.5, 0.02) * 2.0
    return G, H


def tiro_perfeito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = clarao(T, t, 0.0, 0.2, -0.75, 0.0, 0.8)
    G, H = G + g, H + h
    u = rel(t, 0.05, 0.25)
    if u > 0:
        k = 1 - rel(t, 0.4, 0.8)
        G += T.lines([(-0.75, 0.0, -0.75 + 1.5 * ease_out(u, 3), 0.0, 1.0)], 0.06) * k * 0.7
        H += T.lines([(-0.75, 0.0, -0.75 + 1.5 * ease_out(u, 3), 0.0, 1.0)], 0.015) * k * 1.4
    g2, h2 = clarao(T, t, 0.2, 0.45, 0.75, 0.0, 1.2, 1.5)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.22, 0.6, 16, 3, 0.75, 0.0, 0.5, 0.015)
    G += anel(T, t, 0.22, 0.7, 0.05, 0.45, 0.04, 0.0)
    return G * env, H * env


# ------------------------------------------------------------------ Ezio

def _capuz(cx, cy, s):
    return [(cx - 0.12 * s, cy + 0.3 * s), (cx - 0.12 * s, cy), (cx - 0.08 * s, cy - 0.12 * s), (cx, cy - 0.2 * s), (cx + 0.08 * s, cy - 0.12 * s),
            (cx + 0.12 * s, cy), (cx + 0.12 * s, cy + 0.3 * s)]


def multidao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(7):
        a = TAU * j / 7 + 0.3
        u = surge(t, 0.04 * j, 0.3 + 0.04 * j) * (1 - rel(t, 0.85, 1))
        if u > 0:
            g, h = icone(T, _capuz(0.6 * math.cos(a), -0.05 + 0.35 * math.sin(a), 1.2 * u), 0.9, 0.5)
            G, H = G + g, H + h
    for j in range(3):
        a = t * 6 + j * TAU / 3
        k = pulso(t, 0.35, 0.95)
        G += T.gauss(0.12 * math.cos(a), -0.35 + 0.05 * math.sin(a), 0.03) * k * 1.4
    return G * env, H * env


def execucao_em_cadeia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    alvos = [(-0.55, 0.1), (0.0, -0.05), (0.55, 0.1)]
    for j, (x, y) in enumerate(alvos):
        a0 = 0.08 + 0.18 * j
        if j > 0:
            u = rel(t, a0 - 0.12, a0)
            if 0 < u < 1:
                (px, py) = alvos[j - 1]
                mx, my = px + (x - px) * u, py + (y - py) * u - 0.3 * math.sin(math.pi * u)
                G += T.gauss(mx, my, 0.05) * 1.2
        g, h = corte(T, t, a0, a0 + 0.3, -1.1, 1.0, 0.09, x, y)
        G, H = G + g * 1.2, H + h
        g2, h2 = clarao(T, t, a0 + 0.02, a0 + 0.2, x, y, 0.5)
        G, H = G + g2, H + h2
    s = surge(t, 0.6, 0.8) * (1 - rel(t, 0.88, 1))
    if s > 0:
        for lado in (-1, 1):
            asa = [(lado * x * 0.4 * s, -0.5 + y * 0.3 * s) for x, y in ASA]
            g3, h3 = icone(T, asa, 1.0, 0.5)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Sonic

def homing_attack(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    m = pulso(t, 0.0, 0.3)
    G += T.ring(0.1, 0.015, 0.6, -0.1) * m * 1.3
    u = rel(t, 0.15, 0.45)
    if 0 < u < 1:
        x, y = -0.6 + 1.2 * ease_in(u, 1.5), 0.2 - 0.3 * u - 0.15 * math.sin(math.pi * u)
        G += T.gauss(x, y, 0.15) * 1.3
        G += T.arc_band(0.16, 0.04, t * 40, t * 40 + 4, 1.0, 0, x, y, 1.0) * 1.3
        G += T.tapered([(x - 0.5, y + 0.12, x, y, 0.6)], 0.12)
    g, h = clarao(T, t, 0.43, 0.6, 0.6, -0.1, 0.8)
    G, H = G + g, H + h
    s = surge(t, 0.5, 0.75) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.3 * s, 0.04, -0.3, 0.1) * 1.3
        H += T.ring(0.3 * s, 0.012, -0.3, 0.1) * 1.0
    return G * env, H * env


def sonic_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(7):
        a = t * 3 + TAU * j / 7
        g, h = icone(T, poe(GEMA, 0.4 * math.cos(a), 0.25 * math.sin(a), 0.07, a), 1.2, 0.6)
        G, H = G + g, H + h * 1.4
    G += T.gauss(0, 0, 0.18) * (0.4 + 0.2 * math.sin(t * 10))
    return G, H


def super_sonic(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = clarao(T, t, 0.0, 0.35, 0, 0, 1.4, 1.6)
    G, H = G + g, H + h
    s = surge(t, 0.1, 0.4) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        espinhos = []
        for j in range(5):
            a = math.pi * 0.75 + 0.18 * j
            espinhos += [(0.15 * math.cos(a - 0.15), 0.15 * math.sin(a - 0.15)), (0.45 * s * math.cos(a), -0.05 + 0.4 * s * math.sin(a)),
                         (0.15 * math.cos(a + 0.15), 0.15 * math.sin(a + 0.15))]
        g2, h2 = cheio(T, espinhos, 1.3)
        G, H = G + g2, H + h2 * 1.5
    u = rel(t, 0.5, 0.95)
    if 0 < u < 1:
        x = -0.2 + 1.1 * ease_in(u, 1.6)
        for j in range(4):
            G += T.tapered([(x - 0.6, -0.2 + 0.13 * j, x, -0.2 + 0.13 * j, 0.8)], 0.025) * (1 - u) * 1.3
    G += estouro(T, t, 0.05, 0.5, 18, 6, 0, 0, 0.8, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Shadow

def chaos_spear(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        u = rel(t, 0.05 + 0.08 * j, 0.45 + 0.08 * j)
        if 0 < u < 1:
            y = -0.2 + 0.2 * j
            x = -0.7 + 1.5 * ease_in(u, 1.4)
            lanca = [(x, y), (x - 0.24, y - 0.08), (x - 0.55, y), (x - 0.24, y + 0.08)]
            g, h = cheio(T, lanca, 1.4)
            G, H = G + g, H + h * 2
            G += T.tapered([(x - 0.7, y, x - 0.3, y, 0.4)], 0.03)
    G += estouro(T, t, 0.45, 0.8, 12, 2, 0.75, 0.0, 0.4, 0.013)
    return G * env, H * env


def chaos_control(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.4 * s, 0.03, 0, 0) * 1.2
        for j in range(12):
            a = TAU * j / 12
            G += T.lines([(0.34 * s * math.cos(a), 0.34 * s * math.sin(a), 0.4 * s * math.cos(a), 0.4 * s * math.sin(a), 1.0)], 0.01) * 1.2
        para = 1 - rel(t, 0.25, 0.45)
        a = -math.pi / 2 + t * 30 * para + 2.5 * (1 - para)
        G += T.lines([(0, 0, 0.3 * s * math.cos(a), 0.3 * s * math.sin(a), 1.0)], 0.018) * 1.3
    g, h = cheio(T, poe(GEMA, 0, 0.0, 0.08 * s, 0), 1.3 * s)
    G, H = G + g, H + h * 2
    tinge = pulso(t, 0.3, 0.9)
    G += T.gauss(0, 0, 0.9, 0.7) * 0.2 * tinge
    G += anel(T, t, 0.3, 0.8, 0.4, 0.95, 0.03, 0.0)
    return G * env, H * env


def shadow_preparo(T, t, rng):
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(t * 9)
    g, h = icone(T, poe(GEMA, 0, 0, 0.14 * (1 + 0.1 * p), 0), 1.2, 0.6)
    G, H = G + g, H + h * (1 + p)
    G += T.gauss(0, 0, 0.25) * 0.4 * p
    G += T.ring(0.25 + 0.1 * p, 0.012, 0, 0) * (1 - p) * 1.2
    return G, H


def lanca_das_esmeraldas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(14)
    for j in range(14):
        a0 = q.uniform(0, 0.45)
        u = rel(t, a0, a0 + 0.3)
        x = q.uniform(-0.75, 0.75)
        if 0 < u < 1:
            y = -0.9 + 1.2 * ease_in(u, 1.5)
            lanca = [(x, y), (x - 0.03, y - 0.1), (x, y - 0.22), (x + 0.03, y - 0.1)]
            g, h = cheio(T, lanca, 1.3)
            G, H = G + g, H + h * 1.5
        if u >= 1:
            G += T.gauss(x, 0.3, 0.06) * (1 - rel(t, a0 + 0.3, a0 + 0.5)) * 0.9
    G += onda_no_chao(T, t, 0.4, 0.95, 0.95, 0.35)
    return G * env, H * env


# ------------------------------------------------------------------ Zero

def raikousen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.05, 0.3)
    if u > 0:
        x = -0.75 + 1.5 * ease_out(u, 3)
        k = 1 - rel(t, 0.45, 0.7)
        q = np.random.default_rng(int(t * 30))
        bolt = jagged(q, -0.75, 0.05, x, 0.05, 6, 0.06)
        G += T.polyline(bolt, 0.02) * k * 1.4
        H += T.polyline(bolt, 0.007) * k * 1.4
        G += T.tapered([(-0.75, 0.05, x, 0.05, 1.0)], 0.07) * k * 0.6
    g, h = corte(T, t, 0.25, 0.5, 0.15, 1.3, 0.08, 0.5, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.5, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


def zero_preparo(T, t, rng):
    G, H = vazio(T)
    vib = 0.01 * math.sin(t * 60)
    L = T.polys([(lamina(-0.05 + vib, 0.3, 0.3 + vib, -0.35, 0.05, 1.0), 1.0)])
    G += L * 0.9
    H += T.lines([(-0.05 + vib, 0.3, 0.3 + vib, -0.35, 1.0)], 0.006) * (0.8 + 0.4 * math.sin(t * 12))
    G += T.lines([(-0.12, 0.42, -0.05, 0.3, 1.0)], 0.03) * 0.7
    G += particulas(T, (t * 0.8) % 1, 0.0, 1.0, 12, 5, 0.12, -0.05, 0.25, 0.3, 0.012) * 0.8
    return G, H


def sequencia_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.35)
    if u > 0:
        k = 1 - rel(t, 0.5, 0.8)
        G += T.arc_band(0.6, 0.12, -2.6, -2.6 + 3.6 * ease_out(u, 3), 0.6, 0, 0, 0.1, 1.0, True) * k * 1.3
        H += T.arc_band(0.6, 0.03, -2.6, -2.6 + 3.6 * ease_out(u, 3), 0.6, 0, 0, 0.1, 1.0) * k * 1.2
    q = np.random.default_rng(int(t * 25) + 3)
    k2 = pulso(t, 0.35, 0.85)
    for x in (-0.55, 0.0, 0.55):
        bolt = jagged(q, x, -0.6, x + q.uniform(-0.1, 0.1), 0.3, 5, 0.1)
        G += T.polyline(bolt, 0.015) * k2 * 1.2
        H += T.polyline(bolt, 0.005) * k2 * 1.2
    G += onda_no_chao(T, t, 0.3, 0.85, 0.95, 0.35)
    return G * env, H * env


# ------------------------------------------------------------------ Mario

def flor_de_fogo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.5, 0.65))
    if s > 0:
        g, h = icone(T, poe(flor(5, 1.0, 0.35), -0.55, -0.25, 0.24 * s, 0), 1.2, 0.5)
        G, H = G + g, H + h
        G += T.lines([(-0.55, -0.05, -0.55, 0.3 * s, 1.0)], 0.02) * 1.2
    for j in range(3):
        u = rel(t, 0.2 + 0.1 * j, 0.75 + 0.08 * j)
        if 0 < u < 1:
            x = -0.45 + 1.2 * u
            y = 0.25 - 0.3 * abs(math.sin(math.pi * 2.5 * u)) * (1 - 0.4 * u)
            g, h = cheio(T, poe(_circ(16), x, y, 0.1), 1.4)
            G, H = G + g, H + h * 1.5
            G += T.tapered([(x - 0.15, y, x, y, 0.5)], 0.03)
    g2, h2 = clarao(T, t, 0.7, 0.9, 0.75, 0.1, 0.6)
    return (G + g2) * env, (H + h2) * env


REGISTRO = [
    ("kit_primeiros_socorros", kit_primeiros_socorros, GRANDE, "Jill · a maleta e o spray de cura", False),
    ("cobertura_tatica", cobertura_tatica, GRANDE, "Jill · o sinal de mão e as setas", False),
    ("jill_preparo", jill_preparo, MEDIA, "Jill · a seringa enchendo (Preparo, laço)", True),
    ("resistencia_adquirida", resistencia_adquirida, GRANDE, "Jill · o DNA e o escudo", False),
    ("deslocamento_wesker", deslocamento_wesker, GRANDE, "Wesker · o borrão em zigue-zague", False),
    ("golpe_cruzado", golpe_cruzado, GRANDE, "Wesker · os golpes em X e o sangue", False),
    ("supremacia_wesker", supremacia_wesker, GRANDE, "Wesker · os olhos vermelhos e o soco", False),
    ("arco_recurvo", arco_recurvo, GRANDE, "Lara · o arco, a flecha e a marca", False),
    ("armadilha_de_cabo", armadilha_de_cabo, GRANDE, "Lara · o cabo enrolando", False),
    ("lara_preparo", lara_preparo, MEDIA, "Lara · a mira respirando (Preparo, laço)", True),
    ("tiro_perfeito", tiro_perfeito, GRANDE, "Lara · o tiro perfeito", False),
    ("multidao", multidao, GRANDE, "Ezio · a multidão de capuzes", False),
    ("execucao_em_cadeia", execucao_em_cadeia, GRANDE, "Ezio · os saltos e a águia", False),
    ("homing_attack", homing_attack, GRANDE, "Sonic · a bola azul e o anel", False),
    ("sonic_preparo", sonic_preparo, MEDIA, "Sonic · as Esmeraldas girando (Preparo, laço)", True),
    ("super_sonic", super_sonic, GRANDE, "Sonic · a explosão dourada", False),
    ("chaos_spear", chaos_spear, GRANDE, "Shadow · as lanças do Caos", False),
    ("chaos_control", chaos_control, GRANDE, "Shadow · o relógio que para", False),
    ("shadow_preparo", shadow_preparo, MEDIA, "Shadow · a Esmeralda pulsando (Preparo, laço)", True),
    ("lanca_das_esmeraldas", lanca_das_esmeraldas, GRANDE, "Shadow · a chuva de lanças", False),
    ("raikousen", raikousen, GRANDE, "Zero · o avanço relâmpago", False),
    ("zeromm_preparo", zero_preparo, MEDIA, "Zero · o Z-Saber carregando (Preparo, laço)", True),
    ("sequencia_final", sequencia_final, GRANDE, "Zero · o corte em meia-lua e os raios", False),
    ("flor_de_fogo", flor_de_fogo, GRANDE, "Mario · a flor e as bolas de fogo", False),
]
