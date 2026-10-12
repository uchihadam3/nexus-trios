"""Rodada 5 das Mecânicas únicas ativando como habilidade: Mega Man, Zero, Mario, Bowser, Ryu, Chun-Li, Akuma,
Scorpion, Sub-Zero, Liu Kang, Raiden, Jin, Kazuya, Sora, Sekiro, Malenia, Agente 47, Arthas, Geralt, Isaac e Gordon.

- premio: o feixe de teletransporte desce e os blocos de pixel juntam (arma adquirida).
- raikousen: o sabre verde corta e o raio corre pela linha.
- cogumelo: o Super Cogumelo pula, e o corpo cresce em três piscadas.
- furia_bowser: o casco de espinhos gira e o fogo sai.
- hadouken: a bola de energia se forma entre as mãos, com os fios girando.
- spinning_bird: as pernas giram como hélice e os anéis de vento saem.
- messatsu: o símbolo do Céu acende nas costas e a aura escura sobe.
- venha_ca: a lança na corda voa, crava e puxa de volta, com as chamas.
- fatality: o gelo cresce em bloco em volta do rival e se parte.
- mortal_kombat: o dragão de fogo sobe em espiral.
- pele_trovao: os arcos elétricos estalam pela pele e o anel de trovão abre.
- devil_jin: as asas do Devil abrem e o raio da testa dispara.
- chute: o arco do chute passa e as faíscas roxas do gene Devil estalam.
- fusao: a Keyblade gira e as duas auras se juntam numa só.
- postura: a barra de postura enche, quebra e o vermelho do golpe mortal acende.
- florescer: a flor escarlate desabrocha enorme e solta os esporos.
- alvo: a mira vermelha fecha e o código de barras aparece.
- gelida: a Gélida brilha com as runas e as almas são puxadas para a lâmina.
- mutacoes: o medalhão do lobo vibra e o sinal Quen se acende.
- corte_lento: a mira de três pontos do cortador de plasma e o corte.
- hev: o símbolo lambda acende e a morfina entra (a cruz e as barras do traje).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (ASA, CHAMA, CHAVE, CRUZ, ESPADA, anel, aura, cheio, circulo, clarao, converge, corte, estouro,
                         estrela_pts, flor, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def premio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    feixe = pulso(t, 0.0, 0.4)
    if feixe > 0:
        G += T.gauss(0, -0.3, 0.06, 0.7) * feixe * 1.3
        H += T.gauss(0, -0.3, 0.02, 0.7) * feixe * 1.5
    q = np.random.default_rng(3)
    junta = ease_in(rel(t, 0.25, 0.6), 1.6)
    if t > 0.25:
        segs = []
        for j in range(24):
            a, d0 = q.uniform(0, TAU), q.uniform(0.4, 0.8)
            d = d0 * (1 - junta)
            x, y = d * math.cos(a), d * math.sin(a)
            g, h = cheio(T, [(x - 0.025, y - 0.025), (x + 0.025, y - 0.025), (x + 0.025, y + 0.025), (x - 0.025, y + 0.025)], (1 - rel(t, 0.6, 0.7)) * 1.2)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.58, 0.8, 0, 0, 0.9, 1.4)
    G += anel(T, t, 0.6, 0.95, 0.05, 0.6, 0.03)
    for j in range(3):
        G += anel(T, t, 0.62 + 0.06 * j, 0.95, 0.05, 0.35 + 0.1 * j, 0.015) * 0.6
    return (G + g) * env, (H + h) * env


def raikousen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    g, h = corte(T, t, 0.0, 0.3, -0.5, 1.4, 0.12, 0, 0, 0.2)
    G, H = G + g, H + h
    u = rel(t, 0.25, 0.6)
    if 0 < u < 1:
        q = np.random.default_rng(int(t * 30) % 4 + 2)
        x = -0.9 + 1.8 * ease_out(u)
        bolt = jagged(q, -0.9, 0.05, x, 0.05, 5, 0.15)
        G += T.polyline(bolt, 0.04) * 1.4 + T.gauss(x, 0.05, 0.1)
        H += T.polyline(bolt, 0.012) * 1.6
    G += raios(T, t, 0.55, 0.9, 5, 3, 0.9 * 0, 0.05, 0.5)
    g, h = clarao(T, t, 0.55, 0.75, 0, 0.05, 0.8)
    return (G + g) * env, (H + h) * env


def _cogumelo(cx, cy, s):
    chapeu = [(cx + s * math.cos(a), cy - s * 0.1 + s * 0.85 * math.sin(a)) for a in np.linspace(math.pi, TAU, 18)]
    chapeu += [(cx + s, cy + s * 0.05), (cx - s, cy + s * 0.05)]
    pe = [(cx - s * 0.45, cy + s * 0.05), (cx + s * 0.45, cy + s * 0.05), (cx + s * 0.4, cy + s * 0.6), (cx - s * 0.4, cy + s * 0.6)]
    return chapeu, pe


def cogumelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.6)
    if u < 1:
        y = -0.1 - 0.35 * math.sin(math.pi * u) - (0.15 * math.sin(2 * math.pi * u) if u > 0.5 else 0)
        s = 0.3 * surge(t, 0.0, 0.15)
        chapeu, pe = _cogumelo(0, y, s)
        g, h = icone(T, chapeu, 1.2, 0.5)
        G, H = G + g, H + h
        g, h = icone(T, pe, 0.9, 0.35)
        G, H = G + g, H + h
        for dx, dy, r in ((-0.45, -0.35, 0.22), (0.45, -0.35, 0.22), (0, -0.6, 0.25)):
            if s > 0:
                H += T.gauss(dx * s, y + dy * s, r * s) * 1.2
    for j in range(3):
        k = pulso(t, 0.58 + 0.1 * j, 0.7 + 0.1 * j)
        if k > 0:
            G += T.ring(0.25 + 0.1 * j, 0.03, 0, 0) * k * 1.3 + T.gauss(0, 0, 0.3 + 0.08 * j) * k * 0.4
    G += particulas(T, t, 0.5, 1.0, 26, 5, 0, 0, 0.45, 0.4)
    return G * env, H * env


def furia_bowser(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    k = 1 - rel(t, 0.6, 0.8)
    if s > 0 and k > 0:
        r = 0.3 * s
        G += T.ring(r, 0.04, 0, 0.0) * 1.3 * k + T.gauss(0, 0, r * 0.8) * 0.3 * k
        for j in range(8):
            a = TAU * j / 8 + t * 6
            espinho = [(r * math.cos(a - 0.15), r * math.sin(a - 0.15)), (r * 1.45 * math.cos(a), r * 1.45 * math.sin(a)), (r * math.cos(a + 0.15), r * math.sin(a + 0.15))]
            g, h = cheio(T, espinho, k * 1.1)
            G, H = G + g, H + h
    u = rel(t, 0.35, 0.95)
    if 0 < u < 1:
        q = np.random.default_rng(7)
        for j in range(16):
            v = (u * 1.5 + j / 16) % 1
            x = 0.1 + 0.9 * v
            y = -0.05 + q.normal(0, 0.08) * v
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.1 * v, math.pi / 2), (1 - v) * (1 - rel(u, 0.8, 1)) * 1.2, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


def hadouken(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cresce = ease_out(rel(t, 0.0, 0.6), 1.6)
    k = 1 - rel(t, 0.8, 0.95)
    if cresce > 0:
        r = 0.05 + 0.2 * cresce
        G += T.gauss(0, 0, r) * 1.3 * k + T.ring(r * 1.2, 0.02, 0, 0) * k
        H += T.gauss(0, 0, r * 0.5) * 1.6 * k
        for j in range(4):
            fase = TAU * j / 4 + t * 14
            pts = [(r * 1.4 * (1 - 0.4 * v) * math.cos(fase + 3 * v), r * 1.4 * (1 - 0.4 * v) * math.sin(fase + 3 * v) * 0.7) for v in np.linspace(0, 1, 12)]
            G += T.polyline(pts, 0.014) * k
    G += converge(T, t, 0.0, 0.55, 18, 3, 0, 0, 0.7)
    g, h = clarao(T, t, 0.6, 0.85, 0, 0, 0.8)
    return (G + g) * env, (H + h) * env


def spinning_bird(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.8)
    if k > 0:
        for j in range(2):
            a = t * 30 + math.pi * j
            x2, y2 = 0.55 * math.cos(a), -0.15 + 0.55 * math.sin(a) * 0.3
            P = T.polys([(lamina(0, -0.15, x2, y2, 0.09), 1.0)])
            G += P * 1.2 * k
            H += P * 0.4 * k
            for r in range(1, 4):
                aa = a - 0.25 * r
                G += T.polys([(lamina(0, -0.15, 0.55 * math.cos(aa), -0.15 + 0.55 * math.sin(aa) * 0.3, 0.07), 1.0)]) * 0.25 * k / r
    for j in range(4):
        G += anel(T, t, 0.1 + 0.15 * j, 0.5 + 0.15 * j, 0.2, 0.85, 0.025, -0.15, 3.2)
    return G * env, H * env


def messatsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = aura(T, t, 0.0, 1.0, 0.4, 0.0, 1.1)
    G, H = G + g, H + h
    tracos = [(-0.25, -0.35, 0.25, -0.35), (-0.32, -0.12, 0.32, -0.12), (0.0, -0.45, -0.3, 0.3), (0.0, -0.12, 0.3, 0.3)]
    k = 1 - rel(t, 0.85, 1)
    for j, (x1, y1, x2, y2) in enumerate(tracos):
        u = ease_out(rel(t, 0.1 + 0.1 * j, 0.25 + 0.1 * j), 2)
        if u > 0:
            P = T.polys([(lamina(x1, y1, x1 + (x2 - x1) * u, y1 + (y2 - y1) * u, 0.07), 1.0)])
            G += P * 1.4 * k
            H += P * 0.7 * k
    G += particulas(T, t, 0.3, 1.0, 36, 7, 0, 0.2, 0.5, 0.8)
    g, h = clarao(T, t, 0.5, 0.75, 0, -0.05, 0.8)
    return (G + g) * env, (H + h) * env


def venha_ca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2)
    volta = ease_in(rel(t, 0.45, 0.8), 2)
    x = -0.8 + 1.4 * vai - 1.4 * volta
    if t < 0.82:
        pts = [(-0.8 + (x + 0.8) * v, 0.04 * math.sin(v * 14 + t * 20) * (1 - vai * 0.6)) for v in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.024) * 1.2
        ponta = [(x + 0.22, 0), (x, -0.09), (x - 0.05, 0), (x, 0.09)]
        g, h = cheio(T, ponta, 1.4)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.45, 0.6, 0, 0.6)
    G, H = G + g, H + h
    for j in range(6):
        u = rel(t, 0.3 + 0.03 * j, 0.7 + 0.03 * j)
        if 0 < u < 1:
            g, h = icone(T, poe(CHAMA, 0.4 + 0.08 * j - 0.6 * volta, 0.06 * (j % 2), 0.14 * (1 - u * 0.5)), (1 - u) * 1.3, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


def fatality(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cresce = ease_out(rel(t, 0.0, 0.4), 2)
    quebra = rel(t, 0.55, 0.9)
    q = np.random.default_rng(23)
    if cresce > 0 and quebra < 1:
        w, hh = 0.32 * cresce, 0.5 * cresce
        bloco = [(-w, 0.4 - 2 * hh * 0.9), (w, 0.4 - 2 * hh), (w * 1.05, 0.4), (-w * 1.05, 0.4)]
        if quebra <= 0:
            g, h = icone(T, bloco, 1.0, 0.35)
            G, H = G + g, H + h
            for j in range(5):
                G += T.polyline(jagged(q, q.uniform(-w, w), 0.4 - 2 * hh * q.uniform(0.3, 1), q.uniform(-w, w), 0.4 - 2 * hh * q.uniform(0, 0.4), 3, 0.3), 0.008) * 0.8
        else:
            for j in range(12):
                a = q.uniform(0, TAU)
                cx, cy = q.uniform(-w, w), 0.4 - q.uniform(0, 2 * hh)
                d = 0.6 * ease_out(quebra)
                caco = poe([(-1, -0.6), (1, -0.8), (0.4, 1)], cx + d * math.cos(a), cy + d * math.sin(a) + 0.3 * quebra * quebra, 0.07, a + quebra * 5)
                g, h = icone(T, caco, 1 - quebra, 0.5)
                G, H = G + g, H + h
    g, h = clarao(T, t, 0.52, 0.7, 0, 0, 1.0, 1.4)
    G += particulas(T, t, 0.55, 1.0, 30, 9, 0, 0, 0.4, -0.2)
    return (G + g) * env, (H + h) * env


def mortal_kombat(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.7), 1.5)
    k = 1 - rel(t, 0.82, 1)
    n = 18
    for j in range(n):
        v = j / n
        if v > u:
            break
        a = v * TAU * 1.6 + t * 3
        r = 0.45 * (1 - 0.3 * v)
        x, y = r * math.cos(a), 0.4 - 0.95 * v
        tam = 0.05 + 0.05 * (v / max(u, 0.01))
        g, h = icone(T, poe(CHAMA, x, y, tam, a + math.pi), k * (0.5 + 0.5 * v / max(u, 0.01)), 0.6)
        G, H = G + g, H + h
    if u > 0.1:
        a = u * TAU * 1.6 + t * 3
        r = 0.45 * (1 - 0.3 * u)
        x, y = r * math.cos(a), 0.4 - 0.95 * u
        G += T.gauss(x, y, 0.12) * k
        H += T.gauss(x, y, 0.05) * k * 1.5
        for lado in (-1, 1):
            G += T.lines([(x, y, x + lado * 0.1, y - 0.12, 1.0)], 0.02) * k
    return G * env, H * env


def pele_trovao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.85)
    q = np.random.default_rng(int(t * 40) % 7 + 1)
    for j in range(6):
        a1, a2 = q.uniform(0, TAU), q.uniform(0, TAU)
        p1 = (0.22 * math.cos(a1), 0.3 * math.sin(a1))
        p2 = (0.22 * math.cos(a2), 0.3 * math.sin(a2))
        bolt = jagged(q, p1[0], p1[1], p2[0], p2[1], 4, 0.35)
        G += T.polyline(bolt, 0.014) * k * 1.3
        H += T.polyline(bolt, 0.005) * k
    G += raios(T, t, 0.2, 0.7, 4, 9, 0, 0, 0.65)
    G += anel(T, t, 0.25, 0.7, 0.2, 0.75, 0.04) + anel(T, t, 0.45, 0.9, 0.2, 0.75, 0.03)
    g, h = aura(T, t, 0.0, 0.9, 0.3)
    return (G + g) * env, (H + h) * env


def devil_jin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2.2)
    k = 1 - rel(t, 0.82, 1)
    if abre > 0:
        for lado in (-1, 1):
            asa = [(lado * (0.08 + x * 0.65 * abre), -0.15 + y * 0.55 * abre) for x, y in ASA]
            g, h = icone(T, asa, k, 0.45)
            G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.polyline([(lado * 0.06, -0.4), (lado * 0.12, -0.52), (lado * 0.1, -0.6)], 0.022) * k * abre
    u = rel(t, 0.45, 0.8)
    if 0 < u < 1:
        kk = pulso(u, 0, 1)
        G += T.lines([(0, -0.38, 0.95, -0.38, 1.0)], 0.11) * kk * 1.1
        H += T.lines([(0, -0.38, 0.95, -0.38, 1.0)], 0.03) * kk * 1.8
        H += T.gauss(0, -0.38, 0.03) * kk * 2
    return G * env, H * env


def chute(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_out(rel(t, 0.05, 0.4), 2)
    if 0 < u < 1:
        G += T.arc_band(0.5, 0.08, math.pi * 0.9, math.pi * 0.9 + math.pi * 1.2 * u, 1.0, 0.0, 0, 0.0, 1.0, True) * 1.4 * (1 - rel(t, 0.35, 0.5))
    g, h = clarao(T, t, 0.35, 0.55, 0.45, -0.1, 0.8, 1.3)
    G, H = G + g, H + h
    G += raios(T, t, 0.35, 0.9, 5, 13, 0.45, -0.1, 0.5)
    G += anel(T, t, 0.35, 0.8, 0.05, 0.6, 0.04, -0.1)
    return G * env, H * env


def fusao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    gira = rel(t, 0.0, 0.5)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        g, h = icone(T, poe(CHAVE, 0, -0.1, 0.35 * surge(t, 0.0, 0.2), t * 16), k * 1.2, 0.5)
        G, H = G + g, H + h
    junta = ease_in(rel(t, 0.3, 0.6), 2)
    if t > 0.25:
        for lado in (-1, 1):
            x = lado * 0.5 * (1 - junta)
            G += T.gauss(x, 0, 0.18) * 0.9 * (1 - rel(t, 0.62, 0.7))
            H += T.gauss(x, 0, 0.06) * (1 - rel(t, 0.62, 0.7))
    g, h = clarao(T, t, 0.58, 0.8, 0, 0, 1.0, 1.4)
    G += anel(T, t, 0.6, 0.95, 0.05, 0.7, 0.04)
    g2, h2 = aura(T, t, 0.6, 1.0, 0.35)
    return (G + g + g2) * env, (H + h + h2) * env


def postura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    enche = ease_in(rel(t, 0.0, 0.4), 1.3)
    k = 1 - rel(t, 0.42, 0.5)
    if k > 0:
        G += T.lines([(-0.6, -0.5, 0.6, -0.5, 1.0)], 0.08) * 0.3 * k
        G += T.lines([(-0.6 * enche, -0.5, 0.6 * enche, -0.5, 1.0)], 0.08) * 1.4 * k
        H += T.lines([(-0.6 * enche, -0.5, 0.6 * enche, -0.5, 1.0)], 0.025) * k
    g, h = clarao(T, t, 0.4, 0.6, 0, -0.5, 0.8, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.4, 0.75, 16, 5, 0, -0.5, 0.5)
    sinal = pulso(t, 0.5, 1.0)
    if sinal > 0:
        G += T.gauss(0, -0.05, 0.3) * sinal * 0.6
        tracos = [(-0.12, -0.25, 0.12, -0.25), (0.0, -0.25, -0.15, 0.15), (0.0, -0.05, 0.15, 0.15), (-0.18, 0.05, 0.18, 0.05)]
        for x1, y1, x2, y2 in tracos:
            P = T.polys([(lamina(x1, y1, x2, y2, 0.05), 1.0)])
            G += P * 1.3 * sinal
            H += P * 0.7 * sinal
    return G * env, H * env


def florescer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.5), 2.2)
    k = 1 - rel(t, 0.85, 1)
    if abre > 0:
        for j, (n, r, ang) in enumerate(((8, 0.55, 0.0), (8, 0.4, 0.2), (6, 0.25, 0.5))):
            g, h = icone(T, poe(flor(n, 1.0, 0.2), 0, 0, r * abre, ang + t * 0.8 * (1 if j % 2 else -1)), k * (1 - 0.15 * j), 0.35)
            G, H = G + g, H + h
        H += T.gauss(0, 0, 0.06 * abre) * k * 1.5
    G += estouro(T, t, 0.4, 0.9, 30, 3, 0, 0, 0.85, 0.008)
    G += particulas(T, t, 0.45, 1.0, 60, 5, 0, 0, 0.6, 0.35, 0.014)
    return G * env, H * env


def alvo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = ease_out(rel(t, 0.0, 0.4), 2.5)
    k = 1 - rel(t, 0.8, 1)
    r = 0.75 - 0.4 * fecha
    G += T.ring(r, 0.012, 0, -0.05) * k * 1.3
    segs = []
    for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        segs.append((r * 0.6 * math.cos(a), -0.05 + r * 0.6 * math.sin(a), r * 1.2 * math.cos(a), -0.05 + r * 1.2 * math.sin(a), 1.0))
    G += T.lines(segs, 0.012) * k * 1.3
    H += T.gauss(0, -0.05, 0.02) * k * 2 * fecha
    s = rel(t, 0.45, 0.65)
    if s > 0:
        q = np.random.default_rng(47)
        x = -0.4
        barras = []
        while x < 0.4:
            w = q.choice([0.006, 0.012, 0.02])
            barras.append((x, -0.75, x, -0.75 + 0.22 * s, 1.0) if q.uniform() > 0.3 else None)
            x += w * 2.6
        G += T.lines([b for b in barras if b], 0.014) * k * 1.4
    return G * env, H * env


def gelida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3)
    k = 1 - rel(t, 0.82, 1)
    if s > 0:
        g, h = icone(T, poe(ESPADA, 0, -0.05, 0.55 * s), k * 1.2, 0.4)
        G, H = G + g, H + h
        for j in range(5):
            y = -0.45 + 0.12 * j
            brilho = pulso(t, 0.2 + 0.08 * j, 0.6 + 0.08 * j)
            H += T.gauss(0, y * s, 0.02, 0.025) * brilho * 2
            G += T.gauss(0, y * s, 0.04) * brilho
    q = np.random.default_rng(31)
    for j in range(7):
        a = q.uniform(0, TAU)
        u = ease_in(rel(t, 0.3 + 0.04 * j, 0.75 + 0.04 * j), 1.5)
        if 0 < u < 1:
            d = 0.85 * (1 - u)
            x, y = d * math.cos(a), d * math.sin(a)
            G += T.gauss(x, y, 0.05) * 1.1 + T.tapered([(x + 0.15 * math.cos(a), y + 0.15 * math.sin(a), x, y, 0.8)], 0.06)
            H += T.gauss(x, y, 0.02)
    G += particulas(T, t, 0.3, 1.0, 26, 13, 0, 0, 0.35, 0.3)
    return G * env, H * env


def mutacoes(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25)
    k = 1 - rel(t, 0.5, 0.6)
    if s > 0 and k > 0:
        treme = 0.02 * math.sin(t * 90) * (1 - rel(t, 0.3, 0.5))
        r = 0.15 * s
        G += T.ring(r, 0.025, treme, -0.35) * 1.3 * k
        lobo = [(treme - r * 0.6, -0.35 - r * 0.2), (treme - r * 0.45, -0.35 - r * 0.75), (treme - r * 0.15, -0.35 - r * 0.35),
                (treme + r * 0.15, -0.35 - r * 0.35), (treme + r * 0.45, -0.35 - r * 0.75), (treme + r * 0.6, -0.35 - r * 0.2),
                (treme, -0.35 + r * 0.7)]
        g, h = cheio(T, lobo, k)
        G, H = G + g, H + h
    u = surge(t, 0.45, 0.65) * (1 - rel(t, 0.85, 1))
    if u > 0:
        tri = [(0, -0.3 * u), (0.26 * u, 0.15 * u), (-0.26 * u, 0.15 * u)]
        G += T.polyline(tri + [tri[0]], 0.03) * 1.4
        G += T.ring(0.35 * u, 0.02, 0, 0) * 1.2 + T.gauss(0, 0, 0.3 * u) * 0.35
        H += T.polyline(tri + [tri[0]], 0.01)
    G += anel(T, t, 0.5, 0.9, 0.1, 0.65, 0.03)
    return G * env, H * env


def corte_lento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.5, 0.6)
    junta = ease_out(rel(t, 0.0, 0.35), 2)
    if k > 0:
        for dy in (-0.12, 0.0, 0.12):
            y = dy * (1.5 - 0.5 * junta)
            G += T.lines([(-0.9, y, 0.0, y * 0.3, 1.0)], 0.008) * 0.8 * k
            H += T.gauss(0, y * 0.3, 0.018) * k * 2
            G += T.gauss(0, y * 0.3, 0.035) * k
    g, h = corte(T, t, 0.45, 0.7, math.pi / 2 + 0.1, 1.0, 0.08)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.5, 0.7, 0, 0, 0.6)
    G += particulas(T, t, 0.5, 1.0, 30, 3, 0, 0, 0.3, -0.3)
    return (G + g) * env, (H + h) * env


def hev(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    k = 1 - rel(t, 0.55, 0.7)
    if s > 0 and k > 0:
        r = 0.3 * s
        G += T.ring(r, 0.03, 0, -0.05) * 1.3 * k
        lam = [(-0.6 * r, 0.6 * r - 0.05), (0.0, -0.1 * r - 0.05), (-0.25 * r, -0.65 * r - 0.05), (0.0, -0.1 * r - 0.05), (0.6 * r, 0.6 * r - 0.05)]
        G += T.polyline(lam, 0.035 * s) * 1.4 * k
        H += T.polyline(lam, 0.01) * k
    u = surge(t, 0.5, 0.7) * (1 - rel(t, 0.85, 1))
    if u > 0:
        g, h = cheio(T, poe(CRUZ, 0, -0.05, 0.16 * u), 1.3)
        G, H = G + g, H + h
    for j in range(4):
        y = 0.35 - 0.06 * j
        enche = ease_out(rel(t, 0.55 + 0.05 * j, 0.8 + 0.05 * j))
        if enche > 0:
            G += T.lines([(-0.25, y, -0.25 + 0.5 * enche, y, 1.0)], 0.03) * (1 - rel(t, 0.88, 1))
    G += particulas(T, t, 0.55, 1.0, 20, 7, 0, 0, 0.35, 0.4)
    return G * env, H * env


REGISTRO = [
    ("mu_premio", premio, GRANDE, "Mega Man · o teletransporte e a arma adquirida", False),
    ("mu_raikousen", raikousen, GRANDE, "Zero · o sabre e o Raikousen", False),
    ("mu_cogumelo", cogumelo, GRANDE, "Mario · o Super Cogumelo", False),
    ("mu_furia_bowser", furia_bowser, GRANDE, "Bowser · o casco de espinhos e o fogo", False),
    ("mu_hadouken", hadouken, GRANDE, "Ryu · o Hadouken carregando", False),
    ("mu_spinning_bird", spinning_bird, GRANDE, "Chun-Li · o Spinning Bird Kick", False),
    ("mu_messatsu", messatsu, GRANDE, "Akuma · o símbolo do Céu e a aura", False),
    ("mu_venha_ca", venha_ca, GRANDE, "Scorpion · a lança na corda: Venha cá!", False),
    ("mu_fatality", fatality, GRANDE, "Sub-Zero · o bloco de gelo se partindo", False),
    ("mu_mortal_kombat", mortal_kombat, GRANDE, "Liu Kang · o dragão de fogo em espiral", False),
    ("mu_pele_trovao", pele_trovao, GRANDE, "Raiden · os arcos de trovão na pele", False),
    ("mu_devil_jin", devil_jin, GRANDE, "Jin · as asas do Devil e o raio da testa", False),
    ("mu_chute", chute, GRANDE, "Kazuya · o arco do chute e as faíscas roxas", False),
    ("mu_fusao", fusao, GRANDE, "Sora · a Keyblade e as auras se juntando", False),
    ("mu_postura", postura, GRANDE, "Sekiro · a postura quebrada e o golpe mortal", False),
    ("mu_florescer", florescer, GRANDE, "Malenia · a flor escarlate desabrochando", False),
    ("mu_alvo", alvo, GRANDE, "Agente 47 · a mira e o código de barras", False),
    ("mu_gelida", gelida, GRANDE, "Arthas · a Gélida puxando as almas", False),
    ("mu_mutacoes", mutacoes, GRANDE, "Geralt · o medalhão do lobo e o sinal Quen", False),
    ("mu_corte_lento", corte_lento, GRANDE, "Isaac · a mira do cortador de plasma", False),
    ("mu_hev", hev, GRANDE, "Gordon · o lambda e a morfina", False),
]
