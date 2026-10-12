"""Rodada 17 das Mecânicas únicas ativando como habilidade: Hellboy, Ben 10, Gelado, Azula, Inspetor Bugiganga, Jake,
Robin, Chopper, Leorio, Ísis, Hórus, Sekhmet, Jason, Rambo, Godzilla, Bakugo, Sesshomaru, Erza, Rem, Kirito e Megamente.

- chifres_serrados: os chifres serrados acendem e o punho de pedra.
- omnitrix: o relógio gira, a ampulheta verde e o clarão da transformação.
- pista_gelo: a pista de gelo deslizando e os cristais.
- prodigio_instavel: o fogo azul que fica instável (as chamas tremendo).
- penny: o computador-livro da Penny e o ponto de exclamação.
- estica: o braço elástico se esticando em volta do aliado.
- sempre_junto: o bastão bo e o "R" no escudo, o golpe em dupla.
- rumble_ball: a Rumble Ball e a transformação (as formas trocando).
- futuro_medico: a maleta médica e a cruz que cura em dobro.
- asas_protetoras: as asas abertas de Ísis em volta do aliado.
- olho_de_horus: o Olho de Hórus e a mira que nunca erra.
- cheiro_de_sangue: as gotas de sangue e a leoa (os olhos e as garras).
- implacavel: o facão e a máscara de hóquei.
- exercito: as balas e o arco explosivo, e a faixa vermelha.
- radiacao: as placas das costas acendem e o raio atômico.
- explosoes: as explosões nas mãos, cada vez maiores.
- orgulho_youkai: a lua crescente na testa e o chicote de luz.
- reequipar: as armaduras trocando (o brilho e as espadas em volta).
- furia_oni: o chifre de oni e a bola de ferro com espinhos.
- jogador_solo: as duas espadas (preta e branca) e o brilho da conexão.
- plano_mestre: a lousa com o plano e a cabeça azul brilhando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (AMPULHETA, ASA, CHAMA, CRUZ, ESPADA, GOTA, LUA, anel, aura, cheio, clarao, converge, corte, engrenagem, estouro,
                         estrela_pts, icone, onda_no_chao, particulas, poe, raios, surge)


def chifres_serrados(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        G += T.gauss(lado * 0.15, -0.45, 0.06 * s + 0.001, 0.04 * s + 0.001) * 1.5
        H += T.gauss(lado * 0.15, -0.45, 0.025 * s + 0.001) * 2.0 * s
    g, h = aura(T, t, 0.15, 1.0, 0.4, -0.05, 1.0)
    G, H = G + g, H + h
    k = pulso(t, 0.35, 0.85)
    if k > 0:
        P, nos = _punho(T, 0.2 + 0.15 * ease_out(rel(t, 0.35, 0.5)), 0.15, 3.0, math.pi)
        G += P * 0.9 * k
        H += nos * 0.6 * k
    g2, h2 = clarao(T, t, 0.45, 0.65, 0.35, 0.15, 0.8)
    return (G + g2) * env, (H + h2) * env


def omnitrix(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.5, 0.65))
    if s > 0:
        G += T.ring(0.22 * s, 0.04, 0, 0) * 1.2
        g, h = cheio(T, poe(AMPULHETA, 0, 0, 0.15 * s, t * 6 * (1 - rel(t, 0.2, 0.45))), 1.4)
        G, H = G + g, H + h * 2
    g2, h2 = clarao(T, t, 0.45, 0.75, 0, 0, 1.4, 1.6)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.5, 0.95, 0.1, 0.85, 0.05, 0.0)
    G += particulas(T, t, 0.5, 1.0, 30, 5, 0, 0, 0.7, 0.2, 0.013)
    return G * env, H * env


def pista_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.6), 2)
    if u > 0:
        pts = [(-0.9 + 1.8 * v, 0.35 - 0.6 * v + 0.1 * math.sin(v * 5)) for v in np.linspace(0, u, 40)]
        G += T.polyline(pts, 0.06) * 0.6 * (1 - rel(t, 0.88, 1))
        G += T.polyline(pts, 0.015) * 1.4 * (1 - rel(t, 0.88, 1))
        H += T.polyline(pts, 0.006) * (1 - rel(t, 0.88, 1))
    q = np.random.default_rng(6)
    for j in range(8):
        v = j / 8
        k = pulso(t, 0.1 + 0.6 * v, 0.95)
        if k > 0:
            x, y = -0.9 + 1.8 * v, 0.35 - 0.6 * v + 0.1 * math.sin(v * 5) - 0.1
            g, h = icone(T, poe(estrela_pts(6, 0.3), x, y, 0.06 * k, q.uniform(0, 1)), k * 1.2, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


def prodigio_instavel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(7):
        a = -math.pi / 2 + (j - 3) * 0.35
        k = pulso(t, 0.03 * j, 0.9)
        treme = 0.04 * math.sin(t * 50 + j * 3)
        g, h = icone(T, poe(CHAMA, 0.4 * math.cos(a) + treme, 0.15 + 0.4 * math.sin(a), 0.14 * k * (1 + 0.2 * math.sin(t * 30 + j)), 0), k * 1.1, 0.6)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.0, 0.25, 0, -0.1, 0.7)
    q = np.random.default_rng(int(t * 30) + 1)
    for _ in range(3):
        bolt = jagged(q, q.uniform(-0.3, 0.3), -0.1, q.uniform(-0.6, 0.6), q.uniform(-0.6, 0.1), 3, 0.1)
        G += T.polyline(bolt, 0.012) * pulso(t, 0.3, 0.8) * 0.9
    return (G + g2) * env, (H + h2) * env


def penny(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        livro = [(-0.3 * s, -0.15), (0, -0.2 * s - 0.05), (0.3 * s, -0.15), (0.3 * s, 0.2), (0, 0.15), (-0.3 * s, 0.2)]
        g, h = icone(T, livro, 1.0, 0.45)
        G, H = G + g, H + h
        for j in range(3):
            G += T.lines([(0.05, -0.05 + 0.08 * j, 0.25 * s, -0.05 + 0.08 * j, 1.0)], 0.008) * 1.2
        H += T.gauss(-0.15 * s, 0.0, 0.08 * s + 0.001) * 0.8
    e = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if e > 0:
        G += T.lines([(0, -0.7, 0, -0.42 * e - 0.15, 1.0)], 0.04) * 1.4 * e
        G += T.gauss(0, -0.3, 0.035) * 1.6 * e
    return G * env, H * env


def estica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.55), 2)
    if u > 0:
        pts = []
        for v in np.linspace(0, u, 40):
            a = math.pi + TAU * 0.9 * v
            r = 0.15 + 0.4 * min(1, v * 3)
            pts.append((-0.3 + r * math.cos(a) + 0.3, 0.05 + r * 0.7 * math.sin(a)))
        G += T.polyline(pts, 0.05) * 1.1 * (1 - rel(t, 0.88, 1))
        H += T.polyline(pts, 0.015) * 0.6 * (1 - rel(t, 0.88, 1))
    g, h = clarao(T, t, 0.5, 0.7, 0.3, 0.05, 0.6)
    return (G + g) * env, (H + h) * env


def sempre_junto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.15 * s, 0.03, -0.3, -0.1) * 1.2
        G += T.lines([(-0.35, -0.18, -0.35, -0.02, 1.0), (-0.35, -0.18, -0.27, -0.14, 1.0), (-0.27, -0.14, -0.35, -0.1, 1.0), (-0.35, -0.1, -0.26, -0.02, 1.0)], 0.018) * 1.4 * s
    ang = -1.0 + 2.0 * ease_out(rel(t, 0.2, 0.5))
    k = 1 - rel(t, 0.7, 0.85)
    if k > 0:
        c, n = math.cos(ang), math.sin(ang)
        G += T.lines([(0.3 - 0.4 * c, 0.05 - 0.4 * n, 0.3 + 0.4 * c, 0.05 + 0.4 * n, 1.0)], 0.03) * k * 1.3
    g, h = clarao(T, t, 0.45, 0.65, 0.6, 0.2, 0.6)
    return (G + g) * env, (H + h) * env


def rumble_ball(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    if t < 0.32:
        g, h = icone(T, poe([(math.cos(a), math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)], 0.5 - 0.5 * u, -0.5 + 0.5 * u, 0.07), 1.3, 0.7)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.3, 0.5, 0, 0, 1.0, 1.3)
    G, H = G + g2, H + h2
    for j in range(3):
        k = pulso(t, 0.4 + 0.15 * j, 0.6 + 0.15 * j)
        r = 0.2 + 0.1 * j
        forma = [(r * math.cos(a) * (1 + 0.2 * math.sin(a * (3 + j))), r * math.sin(a)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        G += T.polyline(forma + [forma[0]], 0.025) * k * 1.3
    G += estouro(T, t, 0.3, 0.7, 14, 3, 0, 0, 0.7, 0.012)
    return G * env, H * env


def futuro_medico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        maleta = [(-0.3 * s, -0.1), (0.3 * s, -0.1), (0.3 * s, 0.3), (-0.3 * s, 0.3)]
        g, h = icone(T, maleta, 1.0, 0.45)
        G, H = G + g, H + h
        G += T.arc_band(0.08 * s, 0.025, math.pi, TAU, 1.0, 0, 0, -0.1, 1.0) * 1.2
    for j in range(2):
        c = surge(t, 0.3 + 0.15 * j, 0.5 + 0.15 * j) * (1 - rel(t, 0.88, 1))
        g, h = cheio(T, poe(CRUZ, -0.2 + 0.4 * j, -0.45, 0.12 * c, 0), c * 1.4)
        G, H = G + g, H + h * 1.5
    G += particulas(T, t, 0.35, 1.0, 26, 7, 0, -0.3, 0.6, 0.4, 0.013)
    return G * env, H * env


def asas_protetoras(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.45), 2) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        asa = [(lado * x * 0.9 * s, -0.05 + y * 0.8 * s) for x, y in ASA]
        g, h = icone(T, asa, 1.0, 0.5)
        G, H = G + g, H + h
    g2, h2 = aura(T, t, 0.3, 1.0, 0.35, 0.0, 0.9)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.35, 0.85, 0.1, 0.6, 0.03, 0.0)
    return G * env, H * env


def olho_de_horus(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    if s > 0:
        olho = [(0.35 * s * math.cos(a), -0.1 + 0.15 * s * math.sin(a) * (1 if math.sin(a) < 0 else 0.7)) for a in np.linspace(0, TAU, 30)]
        G += T.polyline(olho, 0.025) * 1.3
        G += T.gauss(0, -0.1, 0.07 * s) * 1.3
        H += T.gauss(0, -0.1, 0.03 * s + 0.001) * 2
        G += T.polyline([(-0.05 * s, 0.0), (-0.1 * s, 0.25 * s), (0.0, 0.3 * s), (0.08 * s, 0.25 * s)], 0.02) * 1.2
        G += T.polyline([(0.3 * s, 0.0), (0.38 * s, 0.25 * s), (0.45 * s, 0.25 * s)], 0.02) * 1.2
    m = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.13, 0.015, 0.6, 0.25) * m * 1.3
        G += T.lines([(0.45, 0.25, 0.75, 0.25, 1.0), (0.6, 0.1, 0.6, 0.4, 1.0)], 0.012) * m * 1.3
    return G * env, H * env


def cheiro_de_sangue(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(8)
    for j in range(5):
        k = pulso(t, 0.03 * j, 0.6 + 0.04 * j)
        g, h = cheio(T, poe(GOTA, q.uniform(-0.6, 0.6), q.uniform(-0.1, 0.4), 0.1 * k), k * 1.3)
        G, H = G + g, H + h
    s = surge(t, 0.25, 0.45) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        G += T.gauss(lado * 0.14, -0.35, 0.08 * s + 0.001, 0.04 * s + 0.001) * 1.6
        H += T.gauss(lado * 0.14, -0.35, 0.03 * s + 0.001) * 2.2
    for m in range(3):
        g, h = corte(T, t, 0.45 + 0.03 * m, 0.8 + 0.03 * m, 1.2, 1.3, 0.06, -0.15 + 0.15 * m, 0.05)
        G, H = G + g, H + h
    return G * env, H * env


def implacavel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        mascara = [(0.22 * s * math.cos(a), -0.1 + 0.3 * s * math.sin(a)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, mascara, 1.1, 0.5)
        G, H = G + g, H + h
        q = np.random.default_rng(2)
        for _ in range(8):
            G -= T.gauss(q.uniform(-0.12, 0.12) * s, -0.1 + q.uniform(-0.2, 0.15) * s, 0.015) * 0.8
        for lado in (-1, 1):
            G -= T.gauss(lado * 0.08 * s, -0.15, 0.035, 0.025) * 0.9
    g2, h2 = corte(T, t, 0.4, 0.6, -0.6, 1.5, 0.08, 0.0, 0.1, 0.05)
    G, H = G + g2 * 1.2, H + h2
    return np.maximum(G, 0) * env, H * env


def exercito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.lines([(-0.45 * s, -0.5, 0.45 * s, -0.5, 1.0)], 0.04) * 1.2
        G += T.lines([(0.45 * s, -0.5, 0.6 * s, -0.4, 1.0)], 0.02) * 1.2
    for j in range(6):
        u = rel(t, 0.1 + 0.05 * j, 0.35 + 0.05 * j)
        if 0 < u < 1:
            y = -0.2 + 0.08 * (j % 3)
            x = -0.8 + 1.7 * u
            G += T.tapered([(x - 0.25, y, x, y, 1.0)], 0.035) * 1.4
    u = rel(t, 0.4, 0.6)
    if 0 < u < 1:
        x, y = -0.6 + 1.2 * u, 0.2 - 0.3 * math.sin(math.pi * u)
        G += T.lines([(x - 0.1, y, x, y, 1.0)], 0.015) * 1.3
    g, h = clarao(T, t, 0.6, 0.8, 0.6, 0.2, 1.1, 1.4)
    G, H = G + g, H + h
    G += estouro(T, t, 0.6, 0.95, 16, 5, 0.6, 0.2, 0.5, 0.015)
    return G * env, H * env


def radiacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(5):
        k = pulso(t, 0.05 * j, 0.5 + 0.05 * j)
        x = -0.4 + 0.2 * j
        y = -0.1 - 0.08 * math.sin(math.pi * j / 4)
        g, h = cheio(T, poe([(0, -1), (0.6, 0.3), (0, 0.8), (-0.6, 0.3)], x, y, 0.12 * k), k * 1.3)
        G, H = G + g, H + h * 1.5
    u = rel(t, 0.45, 0.95)
    if 0 < u < 1:
        G += T.lines([(-0.1, 0.1, -0.1 + 1.1 * ease_out(u, 3), 0.1, 1.0)], 0.09) * (1 - rel(u, 0.75, 1)) * 0.9
        H += T.lines([(-0.1, 0.1, -0.1 + 1.1 * ease_out(u, 3), 0.1, 1.0)], 0.03) * (1 - rel(u, 0.75, 1)) * 1.3
    g2, h2 = aura(T, t, 0.0, 0.6, 0.45, -0.1, 0.8)
    return (G + g2) * env, (H + h2) * env


def explosoes(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        a0 = 0.05 + 0.18 * j
        g, h = clarao(T, t, a0, a0 + 0.2, -0.45 + 0.3 * j, 0.1 - 0.1 * j, 0.4 + 0.3 * j, 1.0 + 0.2 * j)
        G, H = G + g, H + h
        G += estouro(T, t, a0, a0 + 0.3, 8 + 3 * j, j + 1, -0.45 + 0.3 * j, 0.1 - 0.1 * j, 0.2 + 0.12 * j, 0.012)
    return G * env, H * env


def orgulho_youkai(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    g, h = cheio(T, poe(LUA, 0, -0.4, 0.1 * s, -math.pi / 2), 1.4 * s)
    G, H = G + g, H + h * 2
    u = ease_out(rel(t, 0.3, 0.65), 2)
    if u > 0:
        pts = [(0.1 + 0.85 * v, 0.1 + 0.25 * math.sin(v * 7 - t * 10) * v) for v in np.linspace(0, u, 30)]
        G += T.polyline(pts, 0.025) * 1.3 * (1 - rel(t, 0.88, 1))
        H += T.polyline(pts, 0.008) * 1.2 * (1 - rel(t, 0.88, 1))
    g2, h2 = aura(T, t, 0.1, 1.0, 0.35, -0.1, 0.6)
    return (G + g2) * env, (H + h2) * env


def reequipar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = clarao(T, t, 0.0, 0.3, 0, -0.05, 1.0, 1.3)
    G, H = G + g, H + h
    s = ease_out(rel(t, 0.2, 0.55), 2) * (1 - rel(t, 0.88, 1))
    for j in range(8):
        a = TAU * j / 8 + t * 2
        g2, h2 = icone(T, poe(ESPADA, 0.55 * s * math.cos(a), -0.05 + 0.4 * s * math.sin(a), 0.18 * s, a + math.pi / 2), 1.0, 0.5)
        G, H = G + g2, H + h2
    G += anel(T, t, 0.2, 0.7, 0.1, 0.6, 0.03, -0.05)
    return G * env, H * env


def furia_oni(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = cheio(T, [(-0.04 * s, -0.4), (0.04 * s, -0.4), (0, -0.4 - 0.25 * s)], 1.5)
        G, H = G + g, H + h * 2
    u = rel(t, 0.25, 0.85)
    if 0 < u < 1:
        a = -math.pi * 0.9 + TAU * 1.2 * ease_out(u)
        bx, by = 0.55 * math.cos(a), 0.0 + 0.4 * math.sin(a)
        G += T.lines([(0, 0.0, bx, by, 1.0)], 0.01) * 1.2
        g2, h2 = icone(T, poe(estrela_pts(10, 0.7), bx, by, 0.12, u * 10), 1.2, 0.6)
        G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.1, 1.0, 0.35, -0.1, 0.8)
    return (G + g3) * env, (H + h3) * env


def jogador_solo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    for lado, k in ((-1, 0.6), (1, 1.4)):
        g, h = icone(T, poe(ESPADA, lado * 0.18 * s, 0.0, 0.42 * s, lado * 0.5), k, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.35, 0.55, 0, -0.25, 0.8)
    G, H = G + g2, H + h2
    G += particulas(T, t, 0.4, 1.0, 26, 3, 0, 0, 0.5, 0.4, 0.012)
    return G * env, H * env


def plano_mestre(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.polyline([(-0.5 * s, -0.4), (0.5 * s, -0.4), (0.5 * s, 0.2), (-0.5 * s, 0.2), (-0.5 * s, -0.4)], 0.02) * 1.2
    rab = ease_out(rel(t, 0.2, 0.7), 2)
    if rab > 0:
        caminho = [(-0.4 + 0.8 * v, -0.1 + 0.15 * math.sin(v * 9)) for v in np.linspace(0, rab, 30)]
        G += T.polyline(caminho, 0.012) * 1.3 * (1 - rel(t, 0.88, 1))
    x = surge(t, 0.65, 0.8) * (1 - rel(t, 0.88, 1))
    if x > 0:
        G += T.lines([(0.3, -0.25, 0.42, -0.1, 1.0), (0.42, -0.25, 0.3, -0.1, 1.0)], 0.025) * 1.4 * x
    g, h = aura(T, t, 0.1, 1.0, 0.3, -0.6, 0.6)
    G, H = G + g, H + h
    G += T.gauss(0, -0.65, 0.12 * s + 0.001, 0.14 * s + 0.001) * 0.8
    return G * env, H * env


REGISTRO = [
    ("mu_chifres_serrados", chifres_serrados, GRANDE, "Hellboy · os chifres e o punho", False),
    ("mu_omnitrix", omnitrix, GRANDE, "Ben 10 · o Omnitrix", False),
    ("mu_pista_gelo", pista_gelo, GRANDE, "Gelado · a pista de gelo", False),
    ("mu_prodigio_instavel", prodigio_instavel, GRANDE, "Azula · o fogo azul instável", False),
    ("mu_penny", penny, GRANDE, "Bugiganga · o livro da Penny", False),
    ("mu_estica_jake", estica, GRANDE, "Jake · estica e protege", False),
    ("mu_sempre_junto", sempre_junto, GRANDE, "Robin · o bastão e o R", False),
    ("mu_rumble_ball", rumble_ball, GRANDE, "Chopper · a Rumble Ball", False),
    ("mu_futuro_medico", futuro_medico, GRANDE, "Leorio · a maleta e a cruz", False),
    ("mu_asas_protetoras", asas_protetoras, GRANDE, "Ísis · as asas", False),
    ("mu_olho_de_horus", olho_de_horus, GRANDE, "Hórus · o olho e a mira", False),
    ("mu_cheiro_de_sangue", cheiro_de_sangue, GRANDE, "Sekhmet · o sangue e as garras", False),
    ("mu_implacavel", implacavel, GRANDE, "Jason · a máscara e o facão", False),
    ("mu_exercito", exercito, GRANDE, "Rambo · as balas e a flecha", False),
    ("mu_radiacao", radiacao, GRANDE, "Godzilla · as placas e o raio", False),
    ("mu_explosoes", explosoes, GRANDE, "Bakugo · as explosões crescentes", False),
    ("mu_orgulho_youkai", orgulho_youkai, GRANDE, "Sesshomaru · a lua e o chicote", False),
    ("mu_reequipar", reequipar, GRANDE, "Erza · as armaduras e as espadas", False),
    ("mu_furia_oni", furia_oni, GRANDE, "Rem · o chifre e a bola de ferro", False),
    ("mu_jogador_solo", jogador_solo, GRANDE, "Kirito · as duas espadas", False),
    ("mu_plano_mestre", plano_mestre, GRANDE, "Megamente · a lousa do plano", False),
]
