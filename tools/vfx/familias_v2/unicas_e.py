"""Rodada 4 das Mecânicas únicas ativando como habilidade: Surfista Prateado, Galactus, Groot, Rocket, Lanterna
Verde, Ciborgue, Shazam, Cloud, Tifa, Sephiroth, Kratos, Link, Ganondorf, Samus, Dante, Vergil, Bayonetta, Master
Chief, Doom Slayer, Snake, Raiden, Leon, Jill, Wesker, Lara, Ezio, Sonic e Shadow.

- planeta: a prancha prateada risca o céu e o planeta escolhido fica marcado.
- devorador: o planeta racha e os pedaços sobem, sugados para o alto.
- groot: os galhos crescem em volta e fecham uma cúpula, com as folhas.
- mina: a mina cai, a luz pisca cada vez mais rápido e explode.
- anel_lanterna: o símbolo da Lanterna acende e a bateria recarrega.
- hacker: as trilhas de circuito se espalham e o olho vermelho varre.
- shazam: o raio cai do céu e o emblema clareia.
- buster: a Buster Sword desce e racha o chão.
- combo_tifa: os socos estouram um atrás do outro, cada vez maiores.
- asa_negra: a asa negra abre e as penas caem.
- furia_esparta: as Lâminas do Caos giram nas correntes em chamas.
- espada_mestra: o feixe da Espada Mestra voa brilhando.
- poder_inabalavel: a Triforce do Poder acende sobre a aura escura.
- raio_de_gelo: o raio de gelo acerta e os cristais crescem.
- estilo: o selo de estilo sobe de nível com os disparos das pistolas.
- concentracao: o Corte do Julgamento — a esfera de cortes e a explosão.
- witch_time: o relógio roxo desacelera e a onda do Witch Time passa.
- escudo_mjolnir: o escudo de energia enche de baixo para cima e brilha.
- armadura_doom: os fragmentos de armadura voam até o Slayer.
- tranquilizante: o "!" do alerta e o dardo que voa.
- zandatsu: o Modo Lâmina — os cortes em grade e o núcleo arrancado.
- faca: a faca corta rápido e solta a faísca do aparo.
- erva: a erva verde aparece, é esmagada e a cura sobe.
- uroboros: os tentáculos negros saem e os olhos vermelhos acendem.
- terreno: a armadilha de dentes fecha no pé de quem bateu.
- proximo: a lâmina oculta salta e o símbolo da Irmandade brilha.
- aneis: os anéis dourados se espalham quicando.
- inibidores: os anéis inibidores caem dos pulsos e a energia do caos explode.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, CHAMA, DIAMANTE, ESCUDO, ESPADA, FOLHA, PENA, RAIO, anel, aura, cheio, chuva, circulo, clarao,
                         converge, corte, estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios, runas, surge, voa)


def planeta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        x, y = -1.0 + 2.0 * ease_in(u, 1.3), -0.6 + 0.3 * u
        prancha = poe([(-1, 0), (-0.6, -0.25), (0.6, -0.25), (1, 0), (0.6, 0.25), (-0.6, 0.25)], x, y, 0.14, 0.15)
        g, h = cheio(T, prancha, 1.2)
        G, H = G + g + T.tapered([(x - 0.8, y - 0.12, x, y, 1.0)], 0.06), H + h
    s = surge(t, 0.35, 0.6) * (1 - rel(t, 0.85, 1))
    if s > 0:
        r = 0.28 * s
        G += T.gauss(0, 0.1, r * 0.8) * 0.5 + T.ring(r, 0.02, 0, 0.1) * 1.3
        for j in range(3):
            G += T.ring(r * (0.4 + 0.25 * j), 0.008, 0, 0.1, 3.0) * 0.6
        G += T.ring(r * 1.5, 0.012, 0, 0.1, 3.5) * 1.0
        for j in range(4):
            a = TAU * j / 4 + t * 2
            G += T.lines([(r * 1.7 * math.cos(a), 0.1 + r * 1.7 * math.sin(a), r * 2.1 * math.cos(a), 0.1 + r * 2.1 * math.sin(a), 1.0)], 0.015) * 1.2
    G += particulas(T, t, 0.4, 1.0, 30, 7, 0, 0.1, 0.5, 0.2)
    return G * env, H * env


def devorador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(5)
    racha = rel(t, 0.15, 0.4)
    sobe = rel(t, 0.4, 1.0)
    if sobe < 1:
        r = 0.3
        k = 1 - sobe
        G += T.ring(r, 0.025, 0, 0.15) * k * 1.3 + T.gauss(0, 0.15, r * 0.7) * k * 0.4
        if racha > 0:
            for j in range(6):
                a = q.uniform(0, TAU)
                G += T.polyline(jagged(q, 0, 0.15, r * math.cos(a), 0.15 + r * math.sin(a), 3, 0.3), 0.012) * racha * k * 1.3
    if sobe > 0:
        pts = []
        for j in range(120):
            a, d = q.uniform(0, TAU), q.uniform(0, 0.3)
            atraso = q.uniform(0, 0.5)
            v = max(0, sobe - atraso) / (1 - atraso)
            x0, y0 = d * math.cos(a), 0.15 + d * math.sin(a)
            pts.append((x0 * (1 - v * 0.8), y0 - 1.1 * ease_in(v, 1.6), (1 - v) * 0.9 if v > 0 else 0.3))
        G += T.splats(pts, 0.016) * 1.2
        G += T.gauss(0, -0.75, 0.35, 0.12) * sobe * (1 - sobe) * 1.2
    return G * env, H * env


def groot(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.82, 1)
    q = np.random.default_rng(11)
    for j in range(7):
        u = ease_out(rel(t, 0.05 + 0.03 * j, 0.55 + 0.03 * j), 2)
        if u > 0:
            a0 = math.pi * (0.1 + 0.8 * j / 6)
            pts = []
            for v in np.linspace(0, u, 16):
                a = a0 + 0.5 * (math.pi / 2 - a0) * v
                r = 0.72 * v
                pts.append((r * math.cos(math.pi + a) * -1, 0.45 - r * math.sin(a) * 1.3))
            for i in range(len(pts) - 1):
                G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.04 * (1 - i / 16) + 0.01) * k
            if u > 0.6:
                for f in range(2):
                    px, py = pts[8 + 3 * f]
                    g, h = icone(T, poe(FOLHA, px + 0.04, py, 0.05, q.uniform(0, TAU)), (u - 0.6) / 0.4 * k, 0.6)
                    G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 20, 9, 0, -0.1, 0.45, -0.3, 0.012)
    g, h = aura(T, t, 0.4, 1.0, 0.3, -0.05, 0.6)
    return (G + g) * env, (H + h) * env


def mina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cai = ease_in(rel(t, 0.0, 0.2), 2)
    if t < 0.62:
        y = -0.7 + 0.95 * cai
        G += T.ring(0.17, 0.03, 0, y, 2.2) * 1.3 + T.gauss(0, y, 0.17, 0.07) * 0.8
        for j in range(6):
            a = TAU * j / 6
            G += T.lines([(0.17 * math.cos(a), y + 0.077 * math.sin(a), 0.25 * math.cos(a), y + 0.115 * math.sin(a), 1.0)], 0.018)
        pisca = (int((t ** 2) * 120) % 2) if t > 0.2 else 0
        H += T.gauss(0, y - 0.05, 0.04) * pisca * 2.2
        G += T.gauss(0, y - 0.05, 0.1) * pisca * 1.2
    g, h = clarao(T, t, 0.62, 0.82, 0, 0.25, 1.0, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.62, 0.95, 0.05, 0.8, 0.05, 0.25) + estouro(T, t, 0.62, 0.95, 18, 4, 0, 0.25, 0.7)
    G += particulas(T, t, 0.64, 1.0, 30, 6, 0, 0.25, 0.4, 0.3, 0.02)
    return G * env, H * env


def anel_lanterna(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    k = 1 - rel(t, 0.85, 1)
    if s > 0:
        r = 0.22 * s
        G += T.ring(r, 0.035 * s, 0, -0.05) * 1.4 * k
        G += T.lines([(-0.28 * s, -0.05 - 0.3 * s, 0.28 * s, -0.05 - 0.3 * s, 1.0), (-0.28 * s, -0.05 + 0.3 * s, 0.28 * s, -0.05 + 0.3 * s, 1.0)], 0.045 * s) * 1.3 * k
        G += T.lines([(-0.18 * s, -0.05 - 0.3 * s, -0.18 * s, -0.05 - r, 1.0), (0.18 * s, -0.05 - 0.3 * s, 0.18 * s, -0.05 - r, 1.0),
                      (-0.18 * s, -0.05 + 0.3 * s, -0.18 * s, -0.05 + r, 1.0), (0.18 * s, -0.05 + 0.3 * s, 0.18 * s, -0.05 + r, 1.0)], 0.03 * s) * 1.1 * k
        H += T.gauss(0, -0.05, 0.08 * s) * k
    G += converge(T, t, 0.3, 0.75, 22, 3, 0, -0.05, 0.7)
    enche = rel(t, 0.35, 0.8)
    G += T.gauss(0, -0.05, 0.12 + 0.25 * enche) * enche * 0.6 * k
    g, h = clarao(T, t, 0.75, 0.92, 0, -0.05, 0.7)
    return (G + g) * env, (H + h) * env


def hacker(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.82, 1)
    q = np.random.default_rng(13)
    for j in range(10):
        u = ease_out(rel(t, 0.0 + 0.02 * j, 0.5 + 0.02 * j), 2)
        if u > 0:
            x, y = 0.0, 0.0
            dx, dy = (1, 0) if j % 2 == 0 else (0, 1)
            sinal = 1 if j < 5 else -1
            pts = [(x, y)]
            for passo in range(4):
                comp = q.uniform(0.1, 0.22)
                x += dx * comp * sinal * (1 if passo % 2 == 0 else 0.6)
                y += dy * comp * sinal * (1 if passo % 2 == 0 else 0.6) * (1 if j % 3 else -1)
                dx, dy = dy, dx
                pts.append((x, y))
            n = max(2, int(len(pts) * u + 0.5))
            G += T.polyline(pts[:n], 0.012) * k * 1.2
            H += T.gauss(pts[n - 1][0], pts[n - 1][1], 0.018) * k * 1.5
    scan = rel(t, 0.35, 0.8)
    if 0 < scan < 1:
        a = -0.8 + 1.6 * scan
        G += T.lines([(0, -0.15, 0.8 * math.cos(a), -0.15 + 0.8 * math.sin(a), 1.0)], 0.03) * 0.8
        H += T.gauss(0, -0.15, 0.05) * 2.0
        G += T.gauss(0, -0.15, 0.1) * 1.0
    return G * env, H * env


def shazam(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.15, 0.55)
    if k > 0:
        q = np.random.default_rng(int(t * 30) % 4 + 1)
        raio = jagged(q, 0.05, -1.0, 0, 0.1, 6, 0.25)
        G += T.polyline(raio, 0.07) * k * 1.4 + T.polyline(raio, 0.03) * k
        H += T.polyline(raio, 0.015) * k * 2
    g, h = clarao(T, t, 0.15, 0.4, 0, 0.1, 1.2, 1.6)
    G, H = G + g, H + h
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = cheio(T, poe(RAIO, 0, 0.0, 0.3 * s, 0.25), 1.2)
        G, H = G + g + T.gauss(0, 0, 0.3) * 0.4 * s, H + h * 2
    G += onda_no_chao(T, t, 0.2, 0.6, 0.85, 0.15)
    return G * env, H * env


def buster(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    desce = ease_in(rel(t, 0.0, 0.35), 2.5)
    k = 1 - rel(t, 0.7, 0.9)
    if desce > 0 and k > 0:
        y = -1.0 + 1.0 * desce
        lamina_larga = [(-0.11, y - 0.55), (0.11, y - 0.55), (0.11, y + 0.25), (0.0, y + 0.38), (-0.11, y + 0.3)]
        g, h = icone(T, lamina_larga, k * 1.2, 0.45)
        G, H = G + g, H + h
        G += T.lines([(-0.22, y - 0.55, 0.22, y - 0.55, 1.0)], 0.04) * k + T.lines([(0, y - 0.55, 0, y - 0.8, 1.0)], 0.035) * k
        for j in range(2):
            G += T.ring(0.025, 0.008, 0, y - 0.35 + 0.12 * j) * k
    g, h = clarao(T, t, 0.33, 0.55, 0, 0.35, 1.0, 1.5)
    G, H = G + g, H + h
    q = np.random.default_rng(9)
    u = rel(t, 0.35, 0.7)
    if u > 0:
        for j in range(6):
            a = math.pi * (0.05 + 0.9 * j / 5)
            G += T.polyline(jagged(q, 0, 0.38, 0.7 * math.cos(a) * ease_out(u), 0.38 + 0.12 * math.sin(a) * ease_out(u), 3, 0.25), 0.014) * (1 - rel(t, 0.8, 1)) * 1.2
    G += onda_no_chao(T, t, 0.35, 0.8, 0.9, 0.38)
    return G * env, H * env


def combo_tifa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    pos = [(-0.3, -0.15), (0.25, -0.25), (-0.15, 0.2), (0.3, 0.15), (0.0, -0.05)]
    for j, (x, y) in enumerate(pos):
        a0 = 0.05 + 0.13 * j
        k = pulso(t, a0, a0 + 0.22)
        if k > 0:
            esc = 1.3 + 0.35 * j
            P, nos = _punho(T, x - 0.12 * esc * (1 - k), y, 0.9 * esc, 0.0 if j % 2 == 0 else math.pi)
            G += P * k * 0.8
            H += nos * k * 0.6
            g, h = cheio(T, poe(estrela_pts(8, 0.4), x + (0.12 if j % 2 == 0 else -0.12) * esc, y, 0.12 * esc * k, j), k)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.6, 0.85, 0, -0.05, 1.0, 1.4)
    G += anel(T, t, 0.6, 0.95, 0.05, 0.7, 0.05, -0.05)
    return (G + g) * env, (H + h) * env


def asa_negra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.45), 2.5)
    k = 1 - rel(t, 0.8, 1)
    if abre > 0:
        ang = -0.9 + 0.9 * abre
        asa = poe([(x * 0.85, y * 0.9) for x, y in ASA], 0.05, -0.1, 1.0 * abre, ang)
        g, h = icone(T, asa, k * 1.1, 0.5)
        G, H = G + g, H + h
        for j in range(5):
            a = ang - 0.9 + 0.22 * j
            G += T.polyline([(0.05, -0.1), (0.05 + 0.75 * abre * math.cos(a), -0.1 + 0.75 * abre * math.sin(a))], 0.008) * k * 0.7
    g, h = chuva(T, t, 0.3, 1.0, PENA, 12, 4, 0.06, -0.6, 0.5, 0.7, 3.0, 1.0)
    return (G + g) * env, (H + h) * env


def furia_esparta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.8, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    for lado in (0, math.pi):
        a = lado + t * 11
        r = 0.55 * abre
        x, y = r * math.cos(a), r * math.sin(a) * 0.6
        elos = [(x * v, y * v) for v in np.linspace(0.15, 1, 8)]
        for ex, ey in elos:
            G += T.ring(0.025, 0.008, ex, ey) * k
        P = T.polys([(lamina(x, y, x + 0.25 * math.cos(a + 1.6), y + 0.25 * math.sin(a + 1.6) * 0.6, 0.08), 1.0)])
        G += P * 1.3 * k
        H += P * 0.6 * k
        for j in range(5):
            aa = a - 0.15 * j
            g, h = icone(T, poe(CHAMA, r * math.cos(aa), r * math.sin(aa) * 0.6, 0.07 * (1 - j / 6), aa + math.pi / 2), k * (1 - j / 6), 0.6)
            G, H = G + g, H + h
    g, h = aura(T, t, 0.1, 1.0, 0.3, 0.0, 1.2)
    G += particulas(T, t, 0.1, 1.0, 30, 15, 0, 0.1, 0.5, 0.6)
    return (G + g) * env, (H + h) * env


def espada_mestra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25)
    if t < 0.35:
        g, h = icone(T, poe(ESPADA, -0.35, 0, 0.35 * s, 0), s * 1.2, 0.5)
        G, H = G + g + T.gauss(-0.35, -0.2, 0.08) * s, H + h
    g, h, _ = voa(T, t, 0.3, 0.7, poe(ESPADA, 0, 0, 1.0, math.pi / 2), -0.35, 0.0, 0.9, 0.0, 0.35, 0.0)
    G, H = G + g, H + h
    u = rel(t, 0.3, 0.7)
    if 0 < u < 1:
        x = -0.35 + 1.25 * ease_in(u, 1.4)
        G += particulas(T, (t - 0.3) / 0.4 * 0.5, 0, 0.5, 20, 3, x - 0.2, 0, 0.2, 0.1)
    for j in range(5):
        k = pulso(t, 0.2 + 0.1 * j, 0.45 + 0.1 * j)
        if k > 0:
            g, h = cheio(T, poe(estrela_pts(4, 0.3), -0.6 + 0.3 * j, -0.3 + 0.15 * (j % 2), 0.07 * k), k * 1.3)
            G, H = G + g, H + h * 2
    return G * env, H * env


def _triangulo(cx, cy, s):
    return [(cx, cy - s), (cx + s * 0.87, cy + s * 0.5), (cx - s * 0.87, cy + s * 0.5)]


def poder_inabalavel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.85, 1)
    g, h = aura(T, t, 0.0, 1.0, 0.4, 0.05, 1.0)
    G, H = G + g, H + h
    s = surge(t, 0.1, 0.35)
    if s > 0:
        tri = [_triangulo(0, -0.55, 0.12 * s), _triangulo(-0.105 * s, -0.37, 0.12 * s), _triangulo(0.105 * s, -0.37, 0.12 * s)]
        for j, pts in enumerate(tri):
            brilho = 1.6 if j == 0 else 0.5
            g, h = cheio(T, pts, brilho * k * s)
            G, H = G + g, H + h * (2 if j == 0 else 0.5)
        G += T.gauss(0, -0.5, 0.18) * k * 0.6 * s
    G += converge(T, t, 0.0, 0.5, 20, 7, 0, 0.0, 0.7)
    G += onda_no_chao(T, t, 0.45, 0.9, 0.8, 0.4)
    return G * env, H * env


def raio_de_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.3)
    if 0 < u < 1:
        G += T.lines([(-1.0, 0.0, -1.0 + 1.0 * ease_out(u), 0.0, 1.0)], 0.06) * 0.9 + T.lines([(-1.0, 0.0, -1.0 + 1.0 * ease_out(u), 0.0, 1.0)], 0.02) * 0.6
        H += T.gauss(-1.0 + 1.0 * ease_out(u), 0, 0.04) * 1.5
    q = np.random.default_rng(17)
    for j in range(9):
        a = q.uniform(0, TAU)
        g0 = ease_out(rel(t, 0.25 + 0.03 * j, 0.5 + 0.03 * j), 2) * (1 - rel(t, 0.85, 1))
        if g0 > 0:
            d = q.uniform(0.05, 0.25)
            comp = q.uniform(0.15, 0.3) * g0
            x0, y0 = d * math.cos(a), d * math.sin(a)
            g, h = icone(T, [(x0, y0), (x0 + comp * math.cos(a + 0.12), y0 + comp * math.sin(a + 0.12)), (x0 + comp * 1.3 * math.cos(a), y0 + comp * 1.3 * math.sin(a)),
                             (x0 + comp * math.cos(a - 0.12), y0 + comp * math.sin(a - 0.12))], 1.0, 0.5)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.25, 0.45, 0, 0, 0.6)
    G += particulas(T, t, 0.3, 1.0, 30, 3, 0, 0, 0.35, 0.2)
    return (G + g) * env, (H + h) * env


def estilo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j, lado in enumerate((-1, 1, -1, 1)):
        k = pulso(t, 0.05 + 0.1 * j, 0.2 + 0.1 * j)
        if k > 0:
            x = lado * 0.35
            G += T.gauss(x, -0.05, 0.06) * k * 1.4 + T.flare(x, -0.05, 0.25 * k, 0, 0.01) * k
            G += T.tapered([(x, -0.05, x + lado * 0.6, -0.1, 1.0)], 0.025) * k
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = icone(T, poe(DIAMANTE, 0, -0.35, 0.25 * s), 1.3, 0.4)
        G, H = G + g + T.gauss(0, -0.4, 0.2) * 0.5 * s, H + h
        G += T.ring(0.32 * s, 0.015, 0, -0.38) * 0.8
    G += particulas(T, t, 0.5, 1.0, 26, 3, 0, -0.35, 0.3, 0.3)
    return G * env, H * env


def concentracao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    cresce = ease_out(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.55, 0.62)
    if cresce > 0 and k > 0:
        r = 0.45 * cresce
        G += T.ring(r, 0.015, 0, 0) * k * 1.2 + T.gauss(0, 0, r * 0.8) * 0.25 * k
        q = np.random.default_rng(int(t * 30) % 5 + 2)
        segs = []
        for _ in range(24):
            a = q.uniform(0, math.pi)
            c = q.uniform(-r * 0.8, r * 0.8)
            dx, dy = math.cos(a), math.sin(a)
            nx, ny = -dy * c, dx * c
            meio = math.sqrt(max(r * r - c * c, 0))
            segs.append((nx - dx * meio, ny - dy * meio, nx + dx * meio, ny + dy * meio, 1.0))
        G += T.lines(segs, 0.006) * k * 1.4
        H += T.lines(segs, 0.003) * k
    g, h = clarao(T, t, 0.55, 0.78, 0, 0, 1.2, 1.6)
    G += anel(T, t, 0.55, 0.92, 0.1, 0.85, 0.05) + estouro(T, t, 0.55, 0.92, 24, 9, 0, 0, 0.8, 0.01)
    return (G + g) * env, (H + h) * env


def witch_time(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3)
    k = 1 - rel(t, 0.82, 1)
    if s > 0:
        r = 0.35 * s
        G += T.ring(r, 0.025, 0, 0) * 1.3 * k
        segs = []
        for j in range(12):
            a = TAU * j / 12
            segs.append((r * 0.82 * math.cos(a), r * 0.82 * math.sin(a), r * 0.95 * math.cos(a), r * 0.95 * math.sin(a), 1.0))
        G += T.lines(segs, 0.012) * k
        gira = 12 * (1 - (1 - min(1, t / 0.8)) ** 3)
        for comp, vel, larg in ((0.75, 1.0, 0.02), (0.5, 0.083, 0.03)):
            a = -math.pi / 2 + gira * vel * TAU / 12
            G += T.lines([(0, 0, r * comp * math.cos(a), r * comp * math.sin(a), 1.0)], larg) * 1.2 * k
        H += T.gauss(0, 0, 0.03) * k
    for j in range(3):
        G += anel(T, t, 0.3 + 0.12 * j, 0.95, 0.2, 1.0, 0.03)
    G += T.gauss(0, 0, 0.6) * pulso(t, 0.3, 0.9) * 0.2
    return G * env, H * env


def escudo_mjolnir(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    enche = ease_out(rel(t, 0.0, 0.55), 1.6)
    k = 1 - rel(t, 0.82, 1)
    nivel = 0.5 - 1.05 * enche
    casca = T.ring(0.38, 0.03, 0, -0.02, 0.75)
    mascara = np.clip((T.V - nivel) / 0.03, 0, 1)
    G += casca * mascara * 1.4 * k + T.gauss(0, -0.02, 0.3, 0.42) * mascara * 0.3 * k
    if 0 < enche < 1:
        G += T.lines([(-0.32, nivel, 0.32, nivel, 1.0)], 0.02) * 1.2
        H += T.lines([(-0.3, nivel, 0.3, nivel, 1.0)], 0.006)
    brilho = pulso(t, 0.55, 0.85)
    H += casca * brilho * 0.8
    G += anel(T, t, 0.55, 0.9, 0.38, 0.6, 0.03, -0.02, 0.75)
    return G * env, H * env


def armadura_doom(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(6):
        a = TAU * j / 6 + 0.3
        u = ease_in(rel(t, 0.0 + 0.04 * j, 0.45 + 0.04 * j), 1.8)
        if u < 1:
            d = 0.8 * (1 - u)
            g, h = icone(T, poe(ESCUDO, d * math.cos(a), d * math.sin(a), 0.06, a + u * 4), 1.2 if u > 0 else 0.5, 0.5)
            G, H = G + g, H + h
            if u > 0:
                G += T.tapered([(1.15 * d * math.cos(a) + 0.1 * math.cos(a), 1.15 * d * math.sin(a) + 0.1 * math.sin(a), d * math.cos(a), d * math.sin(a), 0.7)], 0.04)
    g, h = clarao(T, t, 0.45, 0.7, 0, 0, 0.8, 1.3)
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g2, h2 = icone(T, poe(ESCUDO, 0, 0, 0.3 * s), 1.2, 0.35)
        G, H = G + g2, H + h2
    G += anel(T, t, 0.5, 0.9, 0.1, 0.6, 0.03)
    return (G + g) * env, (H + h) * env


def tranquilizante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.65))
    if s > 0:
        barra = [(-0.04, -0.75), (0.04, -0.75), (0.025, -0.48), (-0.025, -0.48)]
        g, h = cheio(T, [(x * s * 1.7, -0.55 + (y + 0.55) * s * 1.7) for x, y in barra], 1.5)
        G, H = G + g, H + h * 2
        G += T.gauss(0, -0.55 + 0.27 * s, 0.05 * s) * 1.6
        H += T.gauss(0, -0.55 + 0.27 * s, 0.03 * s) * 1.6
    g, h, chegou = voa(T, t, 0.35, 0.6, [(-1, -0.12), (0.6, -0.12), (1, 0), (0.6, 0.12), (-1, 0.12)], -0.95, 0.0, 0.0, 0.0, 0.08)
    G, H = G + g, H + h
    G += anel(T, t, 0.6, 0.85, 0.03, 0.3, 0.02)
    for j in range(3):
        u = rel(t, 0.62 + 0.08 * j, 0.95)
        if 0 < u < 1:
            x, y, w = 0.1 + 0.14 * j, -0.15 - 0.3 * u - 0.1 * j, 0.06 + 0.025 * j
            G += T.polyline([(x - w, y - w), (x + w, y - w), (x - w, y + w), (x + w, y + w)], 0.015) * (1 - u) * 1.4
    return G * env, H * env


def zandatsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    G += T.gauss(0, 0, 0.7) * pulso(t, 0.0, 0.6) * 0.15
    for j in range(9):
        a0 = 0.05 + 0.04 * j
        ang = (0.3 if j % 2 == 0 else -0.4) + 0.12 * j
        u = rel(t, a0, a0 + 0.08)
        k = 1 - rel(t, 0.55, 0.65)
        if u > 0 and k > 0:
            c, s = math.cos(ang), math.sin(ang)
            off = (j - 4) * 0.06
            G += T.lines([(-0.7 * c - off * s, -0.7 * s + off * c, (-0.7 + 1.4 * u) * c - off * s, (-0.7 + 1.4 * u) * s + off * c, 1.0)], 0.008) * k * 1.4
            H += T.lines([(-0.7 * c - off * s, -0.7 * s + off * c, (-0.7 + 1.4 * u) * c - off * s, (-0.7 + 1.4 * u) * s + off * c, 1.0)], 0.003) * k
    nucleo = rel(t, 0.5, 0.9)
    if nucleo > 0:
        x, y = 0.0 + 0.3 * ease_out(nucleo), -0.05 - 0.25 * ease_out(nucleo)
        g, h = cheio(T, [(x - 0.04, y - 0.1), (x + 0.04, y - 0.1), (x + 0.05, y + 0.1), (x - 0.05, y + 0.1)], 1.3 * (1 - rel(t, 0.88, 1)))
        G, H = G + g + T.gauss(x, y, 0.1) * 0.8 * (1 - rel(t, 0.88, 1)), H + h * 2
    return G * env, H * env


def faca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    g, h = corte(T, t, 0.1, 0.35, -0.5, 1.3, 0.1, 0, 0, 0.1)
    G, H = G + g, H + h
    g, h = corte(T, t, 0.3, 0.55, 2.6, 1.2, 0.09, 0.05, 0.05, -0.1)
    G, H = G + g, H + h
    k = pulso(t, 0.5, 0.7)
    if k > 0:
        G += estouro(T, t, 0.5, 0.8, 16, 3, 0.05, 0.0, 0.5, 0.01)
        H += T.gauss(0.05, 0, 0.04) * k * 2
        G += T.flare(0.05, 0, 0.9 * k, 0.4, 0.014) * k * 1.5 + T.gauss(0.05, 0, 0.12) * k
    return G * env, H * env


def erva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    esmaga = rel(t, 0.4, 0.55)
    if s > 0 and esmaga < 1:
        for j in range(3):
            a = -math.pi / 2 + (j - 1) * 0.55
            g, h = icone(T, poe(FOLHA, 0.18 * s * math.cos(a), -0.05 + 0.18 * s * math.sin(a), 0.16 * s * (1 - 0.6 * esmaga), a + math.pi / 2), 1.2 * (1 - esmaga), 0.5)
            G, H = G + g, H + h
        G += T.lines([(0, -0.05, 0, 0.3, 1.0)], 0.02) * s * (1 - esmaga)
    G += particulas(T, t, 0.45, 0.8, 30, 4, 0, 0.0, 0.2, -0.1, 0.02)
    for j in range(7):
        u = rel(t, 0.5 + 0.04 * j, 0.9 + 0.02 * j)
        if 0 < u < 1:
            x, y = -0.3 + 0.1 * j, 0.25 - 0.7 * u
            G += T.lines([(x - 0.04, y, x + 0.04, y, 1.0), (x, y - 0.04, x, y + 0.04, 1.0)], 0.018) * (1 - u) * 1.3
    g, h = aura(T, t, 0.5, 1.0, 0.3)
    return (G + g) * env, (H + h) * env


def uroboros(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.82, 1)
    q = np.random.default_rng(29)
    for j in range(14):
        a = q.uniform(0, TAU)
        u = ease_out(rel(t, q.uniform(0, 0.25), 0.55), 2)
        if u > 0:
            pts = [(0.7 * v * u * math.cos(a + 0.5 * math.sin(v * 8 + t * 10 + j)), 0.7 * v * u * math.sin(a + 0.5 * math.sin(v * 8 + t * 10 + j))) for v in np.linspace(0, 1, 14)]
            G += T.polyline(pts, 0.014) * k * 0.9
    olhos = pulso(t, 0.35, 1.0)
    if olhos > 0:
        for lado in (-1, 1):
            G += T.lines([(lado * 0.04, -0.2, lado * 0.16, -0.21, 1.0)], 0.04) * olhos * 0.5
            H += T.gauss(lado * 0.1, -0.2, 0.025, 0.012) * olhos * 2.5
            G += T.gauss(lado * 0.1, -0.2, 0.06, 0.03) * olhos * 1.2
    return G * env, H * env


def terreno(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.2)
    fecha = ease_in(rel(t, 0.25, 0.4), 2)
    k = 1 - rel(t, 0.82, 1)
    if s > 0:
        for lado in (-1, 1):
            ang = lado * (1.3 * (1 - fecha) + 0.05)
            pts = []
            for j in range(9):
                v = j / 8
                x = -0.3 + 0.6 * v
                y = 0.25 + lado * (0.05 + (0.06 if j % 2 else 0.0)) * -1
                pts.append((x, y))
            base = [(-0.3, 0.25), (0.3, 0.25)]
            gira = [(x, 0.25 + (y - 0.25) * math.cos(ang) * 1.0 - 0.3 * math.sin(abs(ang)) * (1 if lado < 0 else 1) * (x * 0 + 1) * 0) for x, y in pts]
            arco = [(x, 0.25 - lado * 0.3 * (1 - fecha) * math.sin(math.pi * (x + 0.3) / 0.6) - (0 if j % 2 else lado * 0.06)) for j, (x, _) in enumerate(pts)]
            G += T.polyline(arco, 0.02) * s * k * 1.3
        G += T.ring(0.33, 0.015, 0, 0.25, 3.0) * s * k
    g, h = clarao(T, t, 0.38, 0.55, 0, 0.25, 0.6)
    G += anel(T, t, 0.38, 0.7, 0.05, 0.5, 0.03, 0.25, 2.5)
    return (G + g) * env, (H + h) * env


def proximo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_out(rel(t, 0.0, 0.15), 3)
    k = 1 - rel(t, 0.4, 0.55)
    if u > 0 and k > 0:
        P = T.polys([(lamina(-0.4, 0.1, -0.4 + 0.45 * u, 0.1 - 0.1 * u, 0.04), 1.0)])
        G += P * 1.4 * k
        H += P * 0.8 * k
        H += T.gauss(-0.4 + 0.45 * u, 0.1 - 0.1 * u, 0.03) * k * 1.5
    s = surge(t, 0.3, 0.55) * (1 - rel(t, 0.85, 1))
    if s > 0:
        insignia = [(0, -0.35), (0.22, 0.2), (0.12, 0.25), (0.06, 0.05), (-0.06, 0.05), (-0.12, 0.25), (-0.22, 0.2)]
        g, h = icone(T, poe(insignia, 0, -0.05, 1.0 * s), 1.3, 0.4)
        G, H = G + g, H + h
        G += T.lines([(-0.04, 0.12, 0.04, 0.12, 1.0)], 0.02) * s
    for lado in (-1, 1):
        G += corte(T, t, 0.55, 0.8, lado * 0.3 + math.pi / 2, 0.9, 0.04, lado * 0.4, 0.0)[0]
    return G * env, H * env


def aneis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(19)
    u = rel(t, 0.05, 0.95)
    if u > 0:
        for j in range(14):
            a = -math.pi / 2 + q.uniform(-1.3, 1.3)
            v0 = q.uniform(0.9, 1.5)
            tt = u * 1.2
            x = v0 * math.cos(a) * tt * 0.6
            y = 0.0 + v0 * math.sin(a) * tt * 0.9 + 2.2 * tt * tt * 0.5
            if y > 0.35:
                y = 0.35 - (y - 0.35) * 0.4
            pisca = 1.0 if (u < 0.65 or int(t * 40 + j) % 2 == 0) else 0.0
            sq = abs(math.cos(t * 14 + j)) * 0.8 + 0.2
            G += T.ring(0.075, 0.018, x, y, 1 / sq) * 1.4 * pisca * (1 - rel(u, 0.85, 1))
            H += T.ring(0.075, 0.006, x, y, 1 / sq) * 0.8 * pisca * (1 - rel(u, 0.85, 1))
    g, h = clarao(T, t, 0.0, 0.2, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def inibidores(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for lado in (-1, 1):
        cai = ease_in(rel(t, 0.05, 0.45), 2)
        if cai < 1:
            x, y = lado * (0.28 + 0.1 * cai), 0.0 + 0.45 * cai
            G += T.ring(0.12, 0.028, x, y, 2.2) * 1.4 * (1 - rel(t, 0.35, 0.45))
            H += T.ring(0.12, 0.009, x, y, 2.2) * (1 - rel(t, 0.35, 0.45))
    g, h = clarao(T, t, 0.4, 0.6, 0, -0.05, 1.1, 1.5)
    G, H = G + g, H + h
    q = np.random.default_rng(37)
    for j in range(10):
        a = q.uniform(0, TAU)
        u = ease_out(rel(t, 0.42, 0.65), 3)
        k = 1 - rel(t, 0.7, 0.92)
        if u > 0 and k > 0:
            d = q.uniform(0.4, 0.75) * u
            P = T.polys([(lamina(0, -0.05, d * math.cos(a), -0.05 + d * math.sin(a), 0.05), 1.0)])
            G += P * 1.2 * k
            H += P * 0.5 * k
    G += anel(T, t, 0.42, 0.85, 0.1, 0.8, 0.05, -0.05)
    g2, h2 = aura(T, t, 0.4, 1.0, 0.35, -0.05)
    return (G + g2) * env, (H + h2) * env


REGISTRO = [
    ("mu_planeta", planeta, GRANDE, "Surfista Prateado · a prancha e o planeta escolhido", False),
    ("mu_devorador", devorador, GRANDE, "Galactus · o planeta rachando e sugado para o alto", False),
    ("mu_groot", groot, GRANDE, "Groot · os galhos crescendo em cúpula", False),
    ("mu_mina", mina, GRANDE, "Rocket · a mina piscando e explodindo", False),
    ("mu_anel_lanterna", anel_lanterna, GRANDE, "Lanterna Verde · o símbolo e a bateria recarregando", False),
    ("mu_hacker", hacker, GRANDE, "Ciborgue · as trilhas de circuito e a varredura", False),
    ("mu_shazam", shazam, GRANDE, "Shazam · o raio do céu e o emblema", False),
    ("mu_buster", buster, GRANDE, "Cloud · a Buster Sword rachando o chão", False),
    ("mu_combo_tifa", combo_tifa, GRANDE, "Tifa · os socos em sequência", False),
    ("mu_asa_negra", asa_negra, GRANDE, "Sephiroth · a asa negra e as penas", False),
    ("mu_furia_esparta", furia_esparta, GRANDE, "Kratos · as Lâminas do Caos em chamas", False),
    ("mu_espada_mestra", espada_mestra, GRANDE, "Link · o feixe da Espada Mestra", False),
    ("mu_poder_inabalavel", poder_inabalavel, GRANDE, "Ganondorf · a Triforce do Poder", False),
    ("mu_raio_de_gelo", raio_de_gelo, GRANDE, "Samus · o raio de gelo e os cristais", False),
    ("mu_estilo", estilo, GRANDE, "Dante · os disparos e o selo de estilo", False),
    ("mu_concentracao", concentracao, GRANDE, "Vergil · o Corte do Julgamento", False),
    ("mu_witch_time", witch_time, GRANDE, "Bayonetta · o relógio do Witch Time", False),
    ("mu_escudo_mjolnir", escudo_mjolnir, GRANDE, "Master Chief · o escudo de energia recarregando", False),
    ("mu_armadura_doom", armadura_doom, GRANDE, "Doom Slayer · os fragmentos de armadura", False),
    ("mu_tranquilizante", tranquilizante, GRANDE, "Snake · o alerta e o dardo", False),
    ("mu_zandatsu", zandatsu, GRANDE, "Raiden · o Modo Lâmina e o núcleo", False),
    ("mu_faca", faca, GRANDE, "Leon · a faca e a faísca do aparo", False),
    ("mu_erva", erva, GRANDE, "Jill · a erva verde e a cura", False),
    ("mu_uroboros", uroboros, GRANDE, "Wesker · os tentáculos e os olhos vermelhos", False),
    ("mu_terreno", terreno, GRANDE, "Lara · a armadilha de dentes fechando", False),
    ("mu_proximo", proximo, GRANDE, "Ezio · a lâmina oculta e a insígnia", False),
    ("mu_aneis", aneis, GRANDE, "Sonic · os anéis se espalhando", False),
    ("mu_inibidores", inibidores, GRANDE, "Shadow · os inibidores caindo e o caos", False),
]
