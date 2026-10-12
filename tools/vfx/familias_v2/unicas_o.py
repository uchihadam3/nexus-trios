"""Rodada 14 das Mecânicas únicas ativando como habilidade: King Kong, Shrek, Elsa, Malévola, Gênio, Scar, Jack
Esqueleto, Úrsula, Deku, All Might, Todoroki, Mob, Rimuru, Ainz, Lelouch, Inuyasha, Kenshin, Natsu, Asta, Spike, Vash
e Senku.

- tita: os punhos batem no peito e as ondas de choque saem.
- cebola: as camadas da cebola descascam para fora.
- livre_estou: o floco de neve gigante se forma e o gelo gira em volta.
- dragao_malevola: os chifres aparecem e o fogo verde do dragão sai.
- desejo: a lâmpada solta a fumaça azul em espiral e as faíscas.
- hienas: os olhos das hienas acendem no escuro e as garras cortam.
- presentes: os presentes de laço voam diante da lua.
- voz_roubada: a concha dourada puxa a bolinha da voz e os tentáculos.
- one_for_all: os raios verdes do Full Cowl e a porcentagem subindo.
- plus_ultra: o soco do All Might com o tornado de vento.
- choque_termico: o gelo de um lado, o fogo do outro e o vapor no meio.
- cem_por_cento: a explosão psíquica de 100% e os destroços subindo.
- imune: o slime azul e os anéis da análise do Grande Sábio.
- corpo_morto: o crânio de olhos vermelhos e o círculo mágico.
- geass: o símbolo do Geass acende vermelho e o raio da ordem.
- bakuryuha: a Tessaiga desce e os redemoinhos da Ferida do Vento.
- battojutsu: o saque da espada — o corte rapidíssimo e a cicatriz em X.
- come_fogo: as chamas entram na boca e o rugido de fogo sai.
- anulou: a espada negra da antimagia corta os símbolos mágicos.
- seja_agua: as ondas da gota e a fumaça em espiral.
- pacifista: as balas param no ar e as penas brancas caem.
- invento: o frasco borbulha, a engrenagem gira e a ciência brilha.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, CHAMA, ESPADA, GOTA, LUA, PENA, anel, aura, cheio, chuva, circulo, clarao, converge, corte,
                         engrenagem, estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios, runas, surge, voa)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _floco(cx, cy, s, ang):
    segs = []
    for j in range(6):
        a = ang + TAU * j / 6
        c, n = math.cos(a), math.sin(a)
        segs.append((cx, cy, cx + s * c, cy + s * n, 1.0))
        for f in (0.4, 0.65, 0.85):
            bx, by = cx + s * f * c, cy + s * f * n
            for lado in (-1, 1):
                aa = a + lado * 0.8
                segs.append((bx, by, bx + s * 0.25 * (1 - f * 0.5) * math.cos(aa), by + s * 0.25 * (1 - f * 0.5) * math.sin(aa), 1.0))
    return segs


def tita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        a0 = 0.05 + 0.12 * j
        k = pulso(t, a0, a0 + 0.14)
        if k > 0:
            lado = -1 if j % 2 == 0 else 1
            P, nos = _punho(T, lado * (0.3 - 0.12 * k), 0.0, 2.6, 0 if lado < 0 else math.pi)
            G += P * 0.8 * k
            H += nos * 0.5 * k
            G += anel(T, t, a0 + 0.05, a0 + 0.4, 0.1, 0.6, 0.04, 0.0)
    g, h = clarao(T, t, 0.5, 0.7, 0, 0, 0.8)
    G += onda_no_chao(T, t, 0.5, 0.95, 0.95, 0.38)
    return (G + g) * env, (H + h) * env


def cebola(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        u = ease_out(rel(t, 0.1 + 0.12 * j, 0.6 + 0.12 * j), 2)
        r = 0.15 + 0.08 * j + 0.3 * u
        k = (1 - u) if u > 0 else 1.0
        base = [(r * 0.85 * math.cos(a), -0.05 + r * math.sin(a) * (1.2 if math.sin(a) < 0 else 1.0)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        G += T.polyline(base + [base[0]], 0.02) * k * (1 - rel(t, 0.85, 1)) * 1.2
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    G += T.polyline([(0, -0.3), (0.02, -0.45), (-0.03, -0.55)], 0.02) * s
    return G * env, H * env


def livre_estou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.5), 2) * (1 - rel(t, 0.85, 1))
    if s > 0:
        segs = _floco(0, -0.05, 0.55 * s, t * 1.5)
        G += T.lines(segs, 0.018) * 1.3
        H += T.lines(segs, 0.006) * 0.8
    for j in range(2):
        pts = _espiral(0, -0.05, 0.3, 0.75, 0.8, j * math.pi + t * 5)
        G += T.polyline(pts, 0.02) * pulso(t, 0.2, 1.0) * 0.8
    G += particulas(T, t, 0.1, 1.0, 50, 7, 0, 0, 0.6, -0.1, 0.012)
    return G * env, H * env


def dragao_malevola(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            chifre = [(lado * (0.08 + 0.2 * v) * s, -0.35 - (0.35 * v - 0.25 * v ** 3) * s) for v in np.linspace(0, 1, 12)]
            G += T.polyline(chifre, 0.04 * s * (1.0)) * 1.3
        for lado in (-1, 1):
            asa = [(lado * x * 0.7 * s, 0.05 + y * 0.5 * s) for x, y in ASA]
            g, h = icone(T, asa, 0.8, 0.4)
            G, H = G + g, H + h
    u = rel(t, 0.35, 0.95)
    if 0 < u < 1:
        q = np.random.default_rng(7)
        for j in range(24):
            v = (u * 1.4 + j / 24) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            x = -0.1 + 1.0 * v
            y = -0.2 + q.normal(0, 0.06) * v + 0.1 * v
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.1 * v, math.pi / 2), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.2, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


def desejo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        lampada = [(x * 1.6, 0.35 + (y - 0.35) * 1.6) for x, y in [(-0.2 * s, 0.35), (0.2 * s, 0.35), (0.28 * s, 0.25), (0.45 * s, 0.18), (0.22 * s, 0.2), (0.1 * s, 0.15), (-0.12 * s, 0.15), (-0.25 * s, 0.25)]]
        g, h = icone(T, lampada, 1.2, 0.45)
        G, H = G + g, H + h
    fumo = ease_out(rel(t, 0.2, 0.75), 1.5)
    if fumo > 0:
        pts = []
        for v in np.linspace(0, fumo, 30):
            a = v * TAU * 2 + t * 3
            r = 0.05 + 0.25 * v
            pts.append((0.42 * s * 0 + 0.4 - 0.4 * v + r * math.cos(a) * 0.6, 0.15 - 0.8 * v + r * math.sin(a) * 0.3, 0.5 + 0.5 * v))
        G += T.splats(pts, 0.05) * (1 - rel(t, 0.85, 1)) * 0.8
    G += particulas(T, t, 0.4, 1.0, 30, 3, 0, -0.4, 0.45, 0.2)
    for j in range(3):
        k = pulso(t, 0.5 + 0.1 * j, 0.8 + 0.06 * j)
        g, h = cheio(T, poe(estrela_pts(4, 0.3), -0.3 + 0.3 * j, -0.6, 0.08 * k), k * 1.4)
        G, H = G + g, H + h * 2
    return G * env, H * env


def hienas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(13)
    for j in range(5):
        x, y = q.uniform(-0.7, 0.7), q.uniform(-0.5, 0.2)
        k = pulso(t, 0.05 * j, 0.5 + 0.05 * j)
        for lado in (-1, 1):
            H += T.gauss(x + lado * 0.07, y, 0.03, 0.018) * k * 2.5
            G += T.gauss(x + lado * 0.07, y, 0.07, 0.04) * k * 1.2
    for j in range(3):
        a0 = 0.45 + 0.08 * j
        for m in range(3):
            g, h = corte(T, t, a0 + 0.02 * m, a0 + 0.2 + 0.02 * m, 1.1 + 0.6 * j, 0.6, 0.04, -0.3 + 0.3 * j + 0.06 * m, 0.1)
            G, H = G + g, H + h
    return G * env, H * env


def _presente(cx, cy, s, ang):
    caixa = poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], cx, cy, s, ang)
    fitas = [poe([(0, -1), (0, 1)], cx, cy, s, ang), poe([(-1, 0), (1, 0)], cx, cy, s, ang)]
    laco = [poe([(0, -1), (-0.6, -1.6), (-0.3, -1.1), (0, -1), (0.6, -1.6), (0.3, -1.1)], cx, cy, s, ang)]
    return caixa, fitas, laco


def presentes(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = icone(T, poe(LUA, 0.3, -0.45, 0.25 * s, 0.4), 0.8, 0.3)
        G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.15 + 0.1 * j, 0.75 + 0.08 * j)
        if 0 < u < 1:
            x0 = -0.2 + 0.2 * j
            x, y = x0 + (-0.6 + 0.6 * j - x0) * u, -0.1 - 0.4 * math.sin(math.pi * u) + 0.3 * u
            caixa, fitas, laco = _presente(x, y, 0.13, u * 4)
            g, h = icone(T, caixa, 1.1, 0.4)
            G, H = G + g, H + h
            for f in fitas:
                G += T.polyline(f, 0.018) * 1.3
            G += T.polyline(laco[0], 0.018) * 1.3
    return G * env, H * env


def voz_roubada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        concha = _espiral(-0.35, 0.0, 0.01, 0.15 * s, 2.2, 0)
        G += T.polyline(concha, 0.025) * 1.3
        G += T.gauss(-0.35, 0.0, 0.12 * s) * 0.6
    u = ease_in(rel(t, 0.25, 0.7), 1.6)
    if 0 < u < 1:
        x, y = 0.45 - 0.8 * u, -0.25 + 0.25 * u + 0.1 * math.sin(u * 8)
        G += T.gauss(x, y, 0.05) * 1.3
        H += T.gauss(x, y, 0.025) * 1.8
        G += T.tapered([(x + 0.25, y - 0.04, x, y, 0.7)], 0.05)
    for j in range(4):
        tent = ease_out(rel(t, 0.1 + 0.05 * j, 0.5 + 0.05 * j), 2)
        if tent > 0:
            a = math.pi * (0.55 + 0.3 * j / 3)
            pts = [(-0.35 + 0.5 * v * tent * math.cos(a + 0.6 * math.sin(v * 4 + t * 6)), 0.4 - 0.3 * v * tent + 0.0) for v in np.linspace(0, 1, 14)]
            for i in range(len(pts) - 1):
                G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.04 * (1 - i / 14) + 0.008) * (1 - rel(t, 0.85, 1)) * 0.9
    return G * env, H * env


def one_for_all(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.9)
    q = np.random.default_rng(int(t * 40) % 7 + 1)
    for _ in range(7):
        a1, a2 = q.uniform(0, TAU), q.uniform(0, TAU)
        bolt = jagged(q, 0.22 * math.cos(a1), 0.05 + 0.35 * math.sin(a1), 0.22 * math.cos(a2), 0.05 + 0.35 * math.sin(a2), 4, 0.35)
        G += T.polyline(bolt, 0.018) * k * 1.3
        H += T.polyline(bolt, 0.006) * k
    enche = ease_out(rel(t, 0.2, 0.7), 2)
    for j in range(5):
        aceso = 1.0 if enche > (j + 1) / 5 else 0.25
        G += T.lines([(-0.35 + 0.15 * j, -0.6, -0.25 + 0.15 * j, -0.6, 1.0)], 0.04) * aceso * (1 - rel(t, 0.85, 1)) * 1.1
    g, h = aura(T, t, 0.0, 0.9, 0.32, 0.05)
    return (G + g) * env, (H + h) * env


def plus_ultra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        P, nos = _punho(T, -0.55 + 0.4 * u, 0.0, 2.6, 0)
        G += P * 0.9 * k
        H += nos * 0.6 * k
    g, h = clarao(T, t, 0.28, 0.5, 0.0, 0.0, 1.2, 1.6)
    G, H = G + g, H + h
    tornado = rel(t, 0.3, 0.95)
    if 0 < tornado < 1:
        for j in range(6):
            x = 0.1 + 0.15 * j * ease_out(tornado)
            r = 0.08 + 0.05 * j
            G += T.arc_band(r, 0.025, t * 20 + j, t * 20 + j + 4.5, 0.4, 0.0, x, 0.0, 1.0) * (1 - tornado) * 1.3
    return G * env, H * env


def choque_termico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(5)
    for j in range(8):
        cresce = ease_out(rel(t, 0.03 * j, 0.35 + 0.03 * j), 2.5)
        if cresce > 0:
            y0 = q.uniform(-0.4, 0.3)
            comp = q.uniform(0.15, 0.3) * cresce
            x0 = -0.75 + 0.5 * cresce * q.uniform(0.6, 1)
            g, h = icone(T, [(x0, y0 - 0.04), (x0 + comp, y0), (x0, y0 + 0.04)], 1.1 * (1 - rel(t, 0.85, 1)), 0.5)
            G, H = G + g, H + h
    for j in range(8):
        k = pulso(t, 0.05 + 0.03 * j, 0.85)
        if k > 0:
            g, h = icone(T, poe(CHAMA, 0.3 + 0.08 * (j % 4), -0.35 + 0.2 * (j // 4) + 0.05 * math.sin(t * 20 + j), 0.1), k, 0.6)
            G, H = G + g, H + h
    vapor = rel(t, 0.35, 1.0)
    if 0 < vapor < 1:
        pts = [(q.normal(0, 0.08), q.normal(-0.05, 0.1) - 0.4 * vapor, (1 - vapor) * q.uniform(0.3, 1)) for _ in range(30)]
        G += T.splats(pts, 0.06) * 0.8
    return G * env, H * env


def cem_por_cento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = clarao(T, t, 0.0, 0.3, 0, 0, 1.3, 1.8)
    G, H = G + g, H + h
    s = ease_out(rel(t, 0.05, 0.45), 2)
    if s > 0:
        g, h = icone(T, poe(estrela_pts(20, 0.55), 0, 0, 0.75 * s * (1 + 0.03 * math.sin(t * 60)), t * 2), (1 - rel(t, 0.75, 1)) * 0.9, 0.2)
        G, H = G + g, H + h
    q = np.random.default_rng(9)
    for j in range(10):
        u = rel(t, 0.2 + q.uniform(0, 0.2), 1.0)
        if 0 < u < 1:
            x = q.uniform(-0.7, 0.7)
            y = 0.45 - 1.0 * u * q.uniform(0.6, 1)
            g2, h2 = icone(T, poe([(-1, -0.6), (1, -0.8), (0.8, 0.7), (-0.9, 0.6)], x, y, 0.05, u * 3 + j), (1 - rel(u, 0.85, 1)), 0.5)
            G, H = G + g2, H + h2
    return G * env, H * env


def imune(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        balanca = 1 + 0.05 * math.sin(t * 14)
        slime = [(0.28 * s * balanca * math.cos(a), 0.15 + 0.22 * s / balanca * math.sin(a) * (1.4 if math.sin(a) < 0 else 0.6)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, slime, 1.1, 0.4)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.lines([(lado * 0.08 * s, 0.05, lado * 0.08 * s, 0.1, 1.0)], 0.02) * 1.3
    for j in range(3):
        G += anel(T, t, 0.3 + 0.12 * j, 0.8 + 0.06 * j, 0.15, 0.7, 0.025, 0.1)
    g, h = runas(T, t, 0.35, 1.0, 0.5, 8, 0.1, 1.0, 2.0)
    return (G + g * 0.7) * env, (H + h) * env


def corpo_morto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = runas(T, t, 0.0, 1.0, 0.65, 12, 0.0, 1.0, 1.2)
    G, H = G + g, H + h
    s = surge(t, 0.2, 0.45) * (1 - rel(t, 0.85, 1))
    if s > 0:
        cranio = [(0.17 * s * math.cos(a), -0.05 + 0.2 * s * math.sin(a)) for a in np.linspace(math.pi * 0.85, math.pi * 2.15, 16)] + [(0.1 * s, 0.15 * s), (-0.1 * s, 0.15 * s)]
        G += T.polyline(cranio + [cranio[0]], 0.02) * 1.2
        for lado in (-1, 1):
            H += T.gauss(lado * 0.06 * s, -0.07, 0.025) * 2.5 * s
            G += T.gauss(lado * 0.06 * s, -0.07, 0.06) * 1.2 * s
    g2, h2 = aura(T, t, 0.2, 1.0, 0.35, 0, 0.7)
    return (G + g2) * env, (H + h2) * env


def geass(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        simbolo = [(-0.25 * s, -0.15 * s - 0.1), (0, 0.1 * s - 0.1), (0.25 * s, -0.15 * s - 0.1), (0.12 * s, -0.12 * s - 0.1), (0, -0.02 - 0.1), (-0.12 * s, -0.12 * s - 0.1)]
        g, h = cheio(T, simbolo, 1.3)
        G, H = G + g, H + h
        G += T.gauss(0, -0.25 * s - 0.1, 0.03) * 1.5
        G += T.ring(0.35 * s, 0.015, 0, -0.1) * 0.8
    u = rel(t, 0.4, 0.75)
    if 0 < u < 1:
        G += T.lines([(0, -0.1, 0.95, -0.1, 1.0)], 0.05) * pulso(u, 0, 1) * 1.1
        H += T.lines([(0, -0.1, 0.95, -0.1, 1.0)], 0.015) * pulso(u, 0, 1)
    return G * env, H * env


def bakuryuha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    desce = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.6)
    if k > 0:
        ang = -1.2 + 1.2 * desce
        lamina_ = [(0, -0.12), (0.85, -0.18), (1.0, 0.0), (0.85, 0.12), (0, 0.1)]
        g, h = icone(T, poe(lamina_, -0.6, 0.1, 0.65, ang), k * 1.2, 0.45)
        G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.3 + 0.05 * j, 0.95)
        if 0 < u < 1:
            x = -0.2 + 1.0 * ease_out(u) * (0.6 + 0.15 * j)
            y = -0.3 + 0.2 * j
            pts = _espiral(x, y, 0.02, 0.15, 2, t * 20 + j)
            G += T.polyline(pts, 0.02) * (1 - u) * 1.3
    g, h = clarao(T, t, 0.28, 0.45, 0, 0.15, 0.8)
    return (G + g) * env, (H + h) * env


def battojutsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    pausa = pulso(t, 0.0, 0.25)
    H += T.gauss(-0.4, 0.1, 0.02) * pausa * 2
    g, h = corte(T, t, 0.25, 0.35, 0.0, 1.9, 0.12, 0, 0.05, 0.05)
    G, H = G + g * 1.3, H + h
    linha = pulso(t, 0.32, 0.7)
    G += T.lines([(-0.95, 0.05, 0.95, 0.05, 1.0)], 0.015) * linha * 1.4
    H += T.lines([(-0.95, 0.05, 0.95, 0.05, 1.0)], 0.005) * linha
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.lines([(-0.12 * s, -0.4, 0.12 * s, -0.2, 1.0), (0.12 * s, -0.4, -0.12 * s, -0.2, 1.0)], 0.03) * 1.3
    return G * env, H * env


def come_fogo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(3)
    for j in range(10):
        a = q.uniform(0, TAU)
        u = ease_in(rel(t, 0.0 + 0.02 * j, 0.4 + 0.02 * j), 1.6)
        if 0 < u < 1:
            d = 0.8 * (1 - u)
            g, h = icone(T, poe(CHAMA, d * math.cos(a), -0.2 + d * math.sin(a), 0.08 * (1 - 0.5 * u), a - math.pi / 2), 1.1, 0.6)
            G, H = G + g, H + h
    G += T.gauss(0, -0.2, 0.08) * pulso(t, 0.2, 0.5) * 1.4
    u = rel(t, 0.5, 0.95)
    if 0 < u < 1:
        for j in range(20):
            v = (u * 1.4 + j / 20) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            x = 0.0 + 0.95 * v
            y = -0.2 + q.normal(0, 0.06) * v
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.13 * v, math.pi / 2), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


def anulou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.8, 0.95)
    for j in range(3):
        quebra = rel(t, 0.35 + 0.05 * j, 0.6 + 0.05 * j)
        x = -0.4 + 0.4 * j
        if quebra < 1:
            G += T.ring(0.1, 0.012, x, -0.35) * (1 - quebra) * 1.2
            segs = [(x + 0.07 * math.cos(a), -0.35 + 0.07 * math.sin(a), x + 0.07 * math.cos(a + 2.1), -0.35 + 0.07 * math.sin(a + 2.1), 1.0) for a in (0, 2.1, 4.2)]
            G += T.lines(segs, 0.008) * (1 - quebra)
    s = surge(t, 0.0, 0.3)
    if s > 0:
        lam = jagged(np.random.default_rng(3), -0.1, 0.45, 0.25, -0.6, 3, 0.08)
        G += T.polyline(lam, 0.09 * s) * 0.6 * k + T.polyline(lam, 0.03) * 1.2 * k
    g, h = corte(T, t, 0.35, 0.6, 0.0, 1.4, 0.08, 0, -0.35)
    G, H = G + g, H + h
    for j in range(5):
        pts = [(0.1 * math.sin(v * 6 + j + t * 8) + (-0.4 + 0.2 * j), 0.3 - 0.4 * v, (1 - v) * pulso(t, 0.1, 0.9)) for v in np.linspace(0, 1, 8)]
        G += T.splats(pts, 0.035) * 0.6
    return G * env, H * env


def seja_agua(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    cai = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.3:
        g, h = cheio(T, poe(GOTA, 0, -0.6 + 0.9 * cai, 0.08), 1.3)
        G, H = G + g, H + h
    for j in range(4):
        G += anel(T, t, 0.25 + 0.12 * j, 0.85 + 0.05 * j, 0.05, 0.8, 0.02, 0.3, 3.0)
    q = np.random.default_rng(5)
    for j in range(3):
        u = rel(t, 0.3 + 0.1 * j, 1.0)
        if 0 < u < 1:
            pts = [(-0.3 + 0.2 * j + 0.06 * math.sin(v * 8 + t * 4 + j), 0.1 - 0.6 * v * u, (1 - v) * (1 - u)) for v in np.linspace(0, 1, 12)]
            G += T.splats(pts, 0.04) * 0.8
    return G * env, H * env


def pacifista(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = clarao(T, t, 0.0, 0.15, -0.7, 0.0, 0.5)
    G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.05 + 0.05 * j, 0.35 + 0.05 * j)
        if u > 0:
            x = -0.7 + 0.95 * ease_out(u, 3)
            y = -0.15 + 0.15 * j
            k = 1 - rel(t, 0.7, 0.85)
            g2, h2 = cheio(T, poe([(1, 0), (0.5, -0.4), (-1, -0.4), (-1, 0.4), (0.5, 0.4)], x, y, 0.1), k * 1.3)
            G, H = G + g2, H + h2
            if u >= 1:
                G += T.ring(0.08, 0.01, x + 0.08, y, 0.5) * k
    g3, h3 = chuva(T, t, 0.35, 1.0, PENA, 10, 7, 0.06, -0.8, 0.4, 0.6, 3.0, 1.0)
    return (G + g3) * env, (H + h3) * env


def invento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        frasco = [(-0.04, -0.3), (0.04, -0.3), (0.04, -0.12), (0.2, 0.2), (-0.2, 0.2), (-0.04, -0.12)]
        g, h = icone(T, [(x * s * 1.3, y * s * 1.3 + 0.05) for x, y in frasco], 1.2, 0.4)
        G, H = G + g, H + h
        q = np.random.default_rng(int(t * 20))
        for j in range(5):
            u = (t * 3 + j / 5) % 1
            G += T.ring(0.02 + 0.01 * j % 2, 0.008, q.uniform(-0.1, 0.1) * s, 0.25 - 0.5 * u) * (1 - u) * s
    g2, h2 = icone(T, poe(engrenagem(10, 1.0, 0.75), 0.45, -0.3, 0.15 * s, t * 4), s, 0.4)
    G, H = G + g2, H + h2
    for j in range(4):
        k = pulso(t, 0.4 + 0.08 * j, 0.7 + 0.06 * j)
        g3, h3 = cheio(T, poe(estrela_pts(4, 0.3), -0.4 + 0.25 * j, -0.6 + 0.1 * (j % 2), 0.07 * k), k * 1.4)
        G, H = G + g3, H + h3 * 2
    return G * env, H * env


REGISTRO = [
    ("mu_tita", tita, GRANDE, "King Kong · os punhos no peito", False),
    ("mu_cebola", cebola, GRANDE, "Shrek · as camadas da cebola", False),
    ("mu_livre_estou", livre_estou, GRANDE, "Elsa · o floco de neve gigante", False),
    ("mu_dragao_malevola", dragao_malevola, GRANDE, "Malévola · os chifres e o fogo verde", False),
    ("mu_desejo", desejo, GRANDE, "Gênio · a lâmpada e a fumaça", False),
    ("mu_hienas", hienas, GRANDE, "Scar · os olhos e as garras das hienas", False),
    ("mu_presentes", presentes, GRANDE, "Jack Esqueleto · os presentes e a lua", False),
    ("mu_voz_roubada", voz_roubada, GRANDE, "Úrsula · a concha e a voz roubada", False),
    ("mu_one_for_all", one_for_all, GRANDE, "Deku · os raios verdes do One For All", False),
    ("mu_plus_ultra", plus_ultra, GRANDE, "All Might · o soco e o tornado", False),
    ("mu_choque_termico", choque_termico, GRANDE, "Todoroki · gelo e fogo", False),
    ("mu_cem_por_cento", cem_por_cento, GRANDE, "Mob · 100%", False),
    ("mu_imune", imune, GRANDE, "Rimuru · o slime e a análise", False),
    ("mu_corpo_morto", corpo_morto, GRANDE, "Ainz · o crânio e o círculo mágico", False),
    ("mu_geass", geass, GRANDE, "Lelouch · o Geass", False),
    ("mu_bakuryuha", bakuryuha, GRANDE, "Inuyasha · a Tessaiga e os redemoinhos", False),
    ("mu_battojutsu", battojutsu, GRANDE, "Kenshin · o saque da espada", False),
    ("mu_come_fogo", come_fogo, GRANDE, "Natsu · come o fogo e ruge", False),
    ("mu_anulou", anulou, GRANDE, "Asta · a espada da antimagia", False),
    ("mu_seja_agua", seja_agua, GRANDE, "Spike · seja água", False),
    ("mu_pacifista", pacifista, GRANDE, "Vash · as balas paradas e as penas", False),
    ("mu_invento", invento, GRANDE, "Senku · o frasco e a engrenagem", False),
]
