"""Rodada 6 das Mecânicas únicas ativando como habilidade: Hayabusa, Cabeça de Pirâmide, Kirby, Donkey Kong,
Simon Belmont, Príncipe da Pérsia, Seiya, Majin Boo, Kuririn, Shiryu, Hyoga, Ikki, Aiolia, Camus, Hades, Madara,
Pain, Minato, Trunks, Broly, Beerus, Charizard, Garou, Genos, Yusuke e Hiei.

- primeiro: as quatro shurikens saem girando e o corte da Espada do Dragão.
- punicao: o capacete de pirâmide aparece e a Grande Faca desce arrastando.
- inalar: o redemoinho de sucção puxa as estrelas para a boca.
- banana: a casca de banana voa em arco, cai e faz o rival rodopiar.
- vampire_killer: o chicote estala ondulando e a cruz sagrada acende.
- areias: a ampulheta escorre a areia dourada e os anéis do tempo desaceleram.
- pegaso: a constelação de Pégaso liga as estrelas e os meteoros saem.
- absorcao: a gosma rosa engole e os furos soltam vapor.
- kuririn_nao: os seis pontos da testa brilham e a fúria dourada explode nos aliados.
- escudo_dragao: o escudo redondo do Dragão segura o golpe com as faíscas.
- zero_absoluto: o Pó de Diamante — os flocos de neve giram e a aurora fecha.
- fenix_ikki: as asas de fogo da Fênix abrem e as chamas sobem.
- rugido_leao: o Relâmpago de Plasma — os raios de luz retos para todo lado.
- esquife: o Esquife de Gelo cresce em prisma em volta do rival.
- juizo: o eclipse negro com a coroa de espinhos (o juízo de Hades).
- meteoro: o meteoro cai do céu em chamas e abre a cratera.
- shinra_tensei: o Rinnegan pulsa e a onda de repulsão empurra tudo para fora.
- selo_ceifador: os kunais voam e o selo em espiral acende.
- futuro: a fenda do tempo se abre em pé, com as faíscas da viagem.
- lendario: a aura verde lendária incha em camadas, com os raios.
- hakai: a mão aberta acende roxo e o alvo se desfaz em pó que sobe girando.
- fogo_espalha: a explosão de fogo se divide em dois rastros para os lados.
- evoluiu: o Punho da Água Corrente — as correntes que fluem em volta.
- sacrificio: o núcleo do Genos racha, brilha e explode.
- briga_de_rua: a Arma Espiritual carrega na ponta do dedo e dispara.
- nao_estava_la: as imagens que ficam para trás e o Jagan abrindo.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_b import _silhueta
from .rodada13 import _borda
from .unicas_kit import (AMPULHETA, ASA, CHAMA, CRUZ, LUA, anel, aura, cheio, chuva, circulo, clarao, converge, corte,
                         estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def primeiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(4):
        a = TAU * j / 4 + 0.4
        u = ease_out(rel(t, 0.0 + 0.04 * j, 0.45 + 0.04 * j), 1.6)
        if 0 < u < 1:
            d = 0.75 * u
            g, h = cheio(T, poe(estrela_pts(4, 0.3), d * math.cos(a), d * math.sin(a), 0.09, t * 30), 1.3 * (1 - rel(u, 0.8, 1)))
            G, H = G + g, H + h
            G += T.tapered([(0.7 * d * math.cos(a), 0.7 * d * math.sin(a), d * math.cos(a), d * math.sin(a), 0.6)], 0.05)
    g, h = corte(T, t, 0.4, 0.7, 0.35, 1.4, 0.1, 0, 0, 0.15)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.55, 0.75, 0, 0, 0.7)
    return (G + g) * env, (H + h) * env


def punicao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.45, 0.6))
    if s > 0:
        tri = [(0, -0.75), (0.28 * s, -0.25), (-0.28 * s, -0.25)]
        g, h = icone(T, tri, s * 1.2, 0.4)
        G, H = G + g, H + h
        G += T.gauss(0, -0.4, 0.3) * 0.3 * s
    desce = ease_in(rel(t, 0.3, 0.55), 2.5)
    k = 1 - rel(t, 0.75, 0.9)
    if desce > 0 and k > 0:
        ang = -1.2 + 1.1 * desce
        c, sn = math.cos(ang), math.sin(ang)
        faca = [(0.0, 0.0), (0.95, -0.1), (1.0, 0.08), (0.05, 0.12)]
        pts = [(0.5 + x * c * 0.9 - y * sn * 0.9 - 0.9 * c * 0.5, 0.35 + x * sn * 0.9 + y * c * 0.9 - 0.9 * sn * 0.5) for x, y in faca]
        g, h = icone(T, pts, k * 1.2, 0.5)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.53, 0.72, 0, 0.35, 0.9, 1.3)
    G += onda_no_chao(T, t, 0.55, 0.9, 0.85, 0.38)
    G += particulas(T, t, 0.55, 1.0, 30, 3, 0, 0.35, 0.5, 0.25, 0.018)
    return (G + g) * env, (H + h) * env


def inalar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    G += converge(T, t, 0.0, 0.7, 34, 3, 0, 0, 0.9, 0.018)
    q = np.random.default_rng(5)
    for j in range(7):
        a0 = q.uniform(0, TAU)
        u = ease_in(rel(t, 0.05 + 0.06 * j, 0.6 + 0.04 * j), 1.6)
        if 0 < u < 1:
            d = 0.75 * (1 - u)
            a = a0 + 3 * u
            g, h = cheio(T, poe(estrela_pts(5, 0.45), d * math.cos(a), d * math.sin(a), 0.07 * (1 - 0.6 * u), u * 8), 1.2)
            G, H = G + g, H + h
    boca = pulso(t, 0.05, 0.85)
    G += T.ring(0.12, 0.03, 0, 0, 1.6) * boca * 1.2 + T.gauss(0, 0, 0.09, 0.06) * boca * 0.6
    g, h = clarao(T, t, 0.75, 0.92, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def banana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.4)
    if u < 1:
        x, y = -0.7 + 0.7 * u, 0.3 - 0.8 * math.sin(math.pi * u)
        g, h = icone(T, poe(LUA, x, y, 0.2, t * 14), 1.3, 0.5)
        G, H = G + g, H + h
    elif t < 0.85:
        g, h = icone(T, poe(LUA, 0, 0.3, 0.2, 2.6), 1.0 - rel(t, 0.7, 0.85), 0.5)
        G, H = G + g, H + h
    gira = rel(t, 0.42, 0.95)
    if 0 < gira < 1:
        for j in range(3):
            a = TAU * j / 3 + t * 14
            g, h = cheio(T, poe(estrela_pts(5, 0.45), 0.3 * math.cos(a), -0.3 + 0.1 * math.sin(a), 0.06), 1.3 * (1 - gira))
            G, H = G + g, H + h
        G += T.arc_band(0.3, 0.03, t * 14, t * 14 + 4, 0.33, 0.0, 0, -0.3, 1.0) * (1 - gira) * 1.3
    G += anel(T, t, 0.38, 0.65, 0.05, 0.4, 0.03, 0.3, 2.5)
    return G * env, H * env


def vampire_killer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if u > 0 and k > 0:
        pts = [(-0.7 + 1.5 * v * u, -0.1 + 0.12 * math.sin(v * 12 - t * 30) * v) for v in np.linspace(0, 1, 30)]
        for p0, p1 in zip(pts[:-1], pts[1:]):
            G += T.ring(0.018, 0.006, p0[0], p0[1]) * k
        G += T.polyline(pts, 0.012) * k
        H += T.gauss(pts[-1][0], pts[-1][1], 0.04) * k * 1.6
    g, h = clarao(T, t, 0.32, 0.5, 0.8, -0.1, 0.7)
    G, H = G + g, H + h
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        cruz = [(-0.05, -0.32), (0.05, -0.32), (0.05, -0.2), (0.15, -0.2), (0.15, -0.1), (0.05, -0.1), (0.05, 0.2), (-0.05, 0.2),
                (-0.05, -0.1), (-0.15, -0.1), (-0.15, -0.2), (-0.05, -0.2)]
        g, h = cheio(T, [(x * s * 1.6, y * s * 1.6) for x, y in cruz], 1.3)
        G, H = G + g + T.gauss(0, -0.1, 0.3) * 0.5 * s, H + h * 2
    return G * env, H * env


def areias(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = icone(T, poe(AMPULHETA, 0, -0.1, 0.32 * s), 1.1, 0.25)
        G, H = G + g, H + h
        escorre = rel(t, 0.15, 0.85)
        G += T.polys([([(-0.15 * (1 - escorre), -0.38 + 0.25 * escorre), (0.15 * (1 - escorre), -0.38 + 0.25 * escorre), (0.0, -0.12)], 1.0)]) * s * 0.8
        G += T.polys([([(-0.17 * escorre, 0.2), (0.17 * escorre, 0.2), (0.0, 0.2 - 0.12 * escorre)], 1.0)]) * s * 0.8
        G += T.lines([(0, -0.12, 0, 0.2, 1.0)], 0.008) * s
    for j in range(3):
        G += anel(T, t, 0.2 + 0.2 * j, 0.95, 0.2, 0.9 - 0.1 * j, 0.025)
    q = np.random.default_rng(7)
    u = rel(t, 0.1, 1.0)
    if u > 0:
        pts = []
        for j in range(60):
            a = q.uniform(0, TAU) + u * 2 * (1 - u)
            r = q.uniform(0.3, 0.6)
            pts.append((r * math.cos(a), -0.1 + r * math.sin(a) * 0.5, (1 - u) * q.uniform(0.3, 1)))
        G += T.splats(pts, 0.012) * 1.2
    return G * env, H * env


def pegaso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    estrelas = [(-0.3, -0.35), (-0.1, -0.45), (0.1, -0.3), (0.3, -0.4), (0.15, -0.1), (-0.15, -0.05), (0.35, 0.05), (-0.35, 0.1), (0.0, 0.15)]
    liga = [(0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (4, 6), (5, 7), (5, 8)]
    k = 1 - rel(t, 0.55, 0.7)
    for j, (x, y) in enumerate(estrelas):
        a = surge(t, 0.03 * j, 0.15 + 0.03 * j) * k
        if a > 0:
            g, h = cheio(T, poe(estrela_pts(4, 0.3), x * 1.4, y * 1.4, 0.08 * a), 1.4)
            G, H = G + g, H + h * 2
    segs = []
    for j, (i1, i2) in enumerate(liga):
        u = rel(t, 0.25 + 0.03 * j, 0.35 + 0.03 * j)
        if u > 0:
            x1, y1 = estrelas[i1]
            x2, y2 = estrelas[i2]
            segs.append((x1 * 1.4, y1 * 1.4, (x1 + (x2 - x1) * u) * 1.4, (y1 + (y2 - y1) * u) * 1.4, 1.0))
    if segs:
        G += T.lines(segs, 0.016) * k * 1.3
    q = np.random.default_rng(17)
    for j in range(14):
        a0 = 0.5 + q.uniform(0, 0.25)
        u = rel(t, a0, a0 + 0.2)
        if 0 < u < 1:
            y = q.uniform(-0.5, 0.4)
            x = -0.2 + 1.3 * u
            G += T.tapered([(x - 0.35, y, x, y, 1.0)], 0.04) * 1.2
            H += T.gauss(x, y, 0.02) * 1.5
    return G * env, H * env


def absorcao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cresce = ease_out(rel(t, 0.0, 0.45), 2)
    fecha = ease_in(rel(t, 0.45, 0.75), 2)
    k = 1 - rel(t, 0.82, 1)
    if cresce > 0:
        r = 0.45 * cresce * (1 - 0.6 * fecha)
        pts = [((r * (1 + 0.12 * math.sin(5 * a + t * 12) + 0.06 * math.sin(9 * a - t * 20))) * math.cos(a),
                (r * (1 + 0.12 * math.sin(5 * a + t * 12) + 0.06 * math.sin(9 * a - t * 20))) * math.sin(a) * 0.85) for a in np.linspace(0, TAU, 40, endpoint=False)]
        g, h = icone(T, pts, k * 1.1, 0.45)
        G, H = G + g, H + h
    for j in range(3):
        a = -math.pi / 2 + (j - 1) * 0.6
        u = pulso(t, 0.5 + 0.08 * j, 0.95)
        if u > 0:
            x, y = 0.3 * math.cos(a), -0.15 + 0.3 * math.sin(a)
            pts = [(x + 0.04 * math.sin(v * 6 + j), y - 0.4 * v, (1 - v) * u) for v in np.linspace(0, 1, 8)]
            G += T.splats(pts, 0.04) * 0.9
    g, h = clarao(T, t, 0.72, 0.9, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def kuririn_nao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.4, 0.5)
    for j in range(6):
        x, y = -0.08 + 0.08 * (j % 3), -0.45 + 0.07 * (j // 3)
        a = surge(t, 0.03 * j, 0.15 + 0.03 * j) * k
        H += T.gauss(x, y, 0.018) * a * 2
        G += T.gauss(x, y, 0.035) * a * 1.2
    g, h = clarao(T, t, 0.38, 0.6, 0, 0, 1.3, 1.8)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.4 + 0.1 * j, 0.9 + 0.05 * j, 0.1, 0.95, 0.06)
    G += raios(T, t, 0.4, 0.95, 5, 7, 0, 0, 0.8)
    g2, h2 = aura(T, t, 0.4, 1.0, 0.45, 0, 1.2)
    return (G + g2) * env, (H + h2) * env


def escudo_dragao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    k = 1 - rel(t, 0.82, 1)
    if s > 0:
        r = 0.4 * s
        G += T.ring(r, 0.035, 0, 0) * 1.3 * k + T.gauss(0, 0, r * 0.8) * 0.25 * k
        corpo = [(r * 0.75 * (0.25 + 0.75 * v) * math.cos(v * TAU * 1.1 + 0.3), r * 0.75 * (0.25 + 0.75 * v) * math.sin(v * TAU * 1.1 + 0.3)) for v in np.linspace(0, 1, 30)]
        G += T.polyline(corpo, 0.03 * s) * k * 1.1
        H += T.gauss(corpo[-1][0], corpo[-1][1], 0.035) * k
        for j in range(10):
            v = j / 10
            x, y = corpo[int(v * 29)]
            G += T.ring(0.02, 0.006, x, y) * k * 0.8
    u = rel(t, 0.35, 0.55)
    if 0 < u < 1:
        G += T.tapered([(0.9 - 0.45 * u, -0.05, 0.9 - 0.4 * u - 0.05, -0.05, 1.0)], 0.04) + T.tapered([(0.95, -0.05, 0.42, -0.05, 0.8)], 0.06) * (1 - u)
    g, h = clarao(T, t, 0.5, 0.7, 0.4, -0.05, 0.8, 1.3)
    G += estouro(T, t, 0.5, 0.8, 16, 5, 0.4, -0.05, 0.4)
    return (G + g) * env, (H + h) * env


def _floco(cx, cy, s, ang):
    segs = []
    for j in range(6):
        a = ang + TAU * j / 6
        c, n = math.cos(a), math.sin(a)
        segs.append((cx, cy, cx + s * c, cy + s * n, 1.0))
        for f in (0.5, 0.75):
            bx, by = cx + s * f * c, cy + s * f * n
            for lado in (-1, 1):
                aa = a + lado * 0.7
                segs.append((bx, by, bx + s * 0.28 * math.cos(aa), by + s * 0.28 * math.sin(aa), 1.0))
    return segs


def zero_absoluto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(11)
    segs = []
    for j in range(10):
        a0 = q.uniform(0, TAU)
        r0 = q.uniform(0.15, 0.6)
        u = rel(t, 0.0 + 0.03 * j, 0.9)
        if u > 0:
            a = a0 + 2.5 * u
            r = r0 * (1 - 0.3 * u)
            segs += _floco(r * math.cos(a), r * math.sin(a) * 0.7, 0.07 * surge(t, 0.03 * j, 0.15 + 0.03 * j), a * 2)
    if segs:
        G += T.lines(segs, 0.01) * 1.3 * (1 - rel(t, 0.85, 1))
        H += T.lines(segs, 0.004) * (1 - rel(t, 0.85, 1))
    G += particulas(T, t, 0.0, 1.0, 60, 3, 0, 0, 0.6, -0.15, 0.01)
    aur = pulso(t, 0.3, 1.0)
    G += T.arc_band(0.55, 0.06, math.pi * 1.1, math.pi * 1.9, 1.0, 0.0, 0, 0.1, 0.0) * aur * 0.9
    G += T.arc_band(0.45, 0.04, math.pi * 1.15, math.pi * 1.85, 1.0, 0.0, 0, 0.1, 0.0) * aur * 0.6
    return G * env, H * env


def fenix_ikki(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.45), 2.2)
    k = 1 - rel(t, 0.8, 1)
    if abre > 0:
        bate = 0.1 * math.sin(t * 16)
        for lado in (-1, 1):
            asa = [(lado * x * 0.85 * abre, -0.05 + (y + bate * x) * 0.75 * abre) for x, y in ASA]
            g, h = icone(T, asa, k, 0.5)
            G, H = G + g, H + h
            for j in range(5):
                x, y = ASA[2 + j]
                g, h = icone(T, poe(CHAMA, lado * x * 0.85 * abre, -0.05 + (y + bate * x) * 0.75 * abre, 0.08 * abre), k, 0.6)
                G, H = G + g, H + h
        G += T.gauss(0, 0, 0.25 * abre) * 0.5 * k
    G += particulas(T, t, 0.2, 1.0, 40, 21, 0, 0.1, 0.5, 0.9, 0.016)
    return G * env, H * env


def rugido_leao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    g, h = clarao(T, t, 0.0, 0.25, 0, 0, 0.8)
    G, H = G + g, H + h
    q = np.random.default_rng(int(t * 25) % 5 + 3)
    k = pulso(t, 0.1, 0.8)
    if k > 0:
        segs = []
        for _ in range(26):
            a = q.uniform(0, TAU)
            d0, d1 = q.uniform(0.0, 0.2), q.uniform(0.5, 0.95)
            segs.append((d0 * math.cos(a), d0 * math.sin(a), d1 * math.cos(a), d1 * math.sin(a), q.uniform(0.5, 1)))
        G += T.lines(segs, 0.012) * k * 1.4
        H += T.lines(segs, 0.004) * k
    for j in range(3):
        G += T.arc_band(0.25 + 0.2 * j, 0.04, -0.6, 0.6, 1.0, 0.0, 0, 0, 0.0) * pulso(t, 0.1 + 0.1 * j, 0.5 + 0.1 * j) * 1.2
    return G * env, H * env


def esquife(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    cresce = ease_out(rel(t, 0.0, 0.5), 2)
    k = 1 - rel(t, 0.85, 1)
    if cresce > 0:
        w, alto = 0.3, 0.9 * cresce
        topo = 0.42 - alto
        prisma = [(-w, 0.42), (-w, topo + 0.12), (0, topo), (w, topo + 0.12), (w, 0.42)]
        g, h = icone(T, prisma, k, 0.3)
        G, H = G + g, H + h
        G += T.lines([(0, topo, 0, 0.42, 1.0), (-w, topo + 0.12, -w * 0.4, 0.42, 1.0), (w, topo + 0.12, w * 0.4, 0.42, 1.0)], 0.008) * 0.8 * k
        y = 0.42 - alto * ((t * 2) % 1)
        H += T.lines([(-w, y, w, y - 0.1, 1.0)], 0.01) * k * 0.8
    G += particulas(T, t, 0.0, 1.0, 40, 9, 0, 0.35, 0.45, -0.1, 0.02)
    g, h = clarao(T, t, 0.48, 0.65, 0, -0.1, 0.6)
    return (G + g) * env, (H + h) * env


def juizo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2)
    k = 1 - rel(t, 0.82, 1)
    if s > 0:
        r = 0.32 * s
        G += T.ring(r, 0.03, 0, -0.1) * 1.4 * k
        H += T.ring(r, 0.008, 0, -0.1) * k
        for j in range(16):
            a = TAU * j / 16 + t * 0.8
            comp = (0.12 + 0.08 * (j % 2)) * s
            G += T.polys([(lamina(r * math.cos(a), -0.1 + r * math.sin(a), (r + comp) * math.cos(a), -0.1 + (r + comp) * math.sin(a), 0.04), 1.0)]) * k
    q = np.random.default_rng(15)
    for j in range(5):
        u = rel(t, 0.4 + 0.06 * j, 0.75 + 0.06 * j)
        if 0 < u < 1:
            x = q.uniform(-0.5, 0.5)
            y = -0.9 + 1.2 * ease_in(u, 2)
            G += T.polys([(lamina(x, y - 0.25, x, y, 0.035), 1.0)]) * 1.2
    return G * env, H * env


def meteoro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.45), 1.8)
    if u < 1:
        x, y = -0.7 + 0.7 * u, -1.0 + 1.25 * u
        r = 0.13 + 0.05 * u
        G += T.gauss(x, y, r) * 1.3
        H += T.gauss(x, y, r * 0.5) * 1.5
        G += T.tapered([(x - 0.5, y - 0.85, x, y, 1.0)], r * 2.2) * 0.8
        q = np.random.default_rng(3)
        for j in range(8):
            g, h = icone(T, poe(CHAMA, x - 0.1 * j * 0.6 + q.normal(0, 0.03), y - 0.17 * j * 0.6 + q.normal(0, 0.03), 0.07 * (1 - j / 9), 2.5), 1 - j / 9, 0.6)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.43, 0.65, 0, 0.25, 1.3, 1.8)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.45, 0.9, 0.95, 0.3) + estouro(T, t, 0.45, 0.85, 22, 8, 0, 0.25, 0.8)
    G += particulas(T, t, 0.48, 1.0, 40, 9, 0, 0.25, 0.55, 0.4, 0.02)
    return G * env, H * env


def shinra_tensei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.35, 0.45))
    for j in range(5):
        G += T.ring(0.04 + 0.035 * j, 0.008, 0, -0.1) * s * 1.2
    H += T.gauss(0, -0.1, 0.02) * s * 2
    u = ease_out(rel(t, 0.35, 0.85), 2.2)
    if 0 < u < 1:
        r = 0.08 + 0.85 * u
        G += T.ring(r, 0.08 * (1 - u) + 0.02, 0, -0.1) * (1 - u) * 1.6 + T.gauss(0, -0.1, r * 0.7) * (1 - u) * 0.5
        H += T.ring(r, 0.015, 0, -0.1) * (1 - u)
        q = np.random.default_rng(9)
        pts = [(q.uniform(-1, 1) * 0.2 + (r + 0.1) * math.cos(a), -0.1 + (r + 0.1) * math.sin(a) + q.uniform(-1, 1) * 0.05, 1 - u) for a in q.uniform(0, TAU, 40)]
        G += T.splats(pts, 0.015) * 1.2
    g, h = clarao(T, t, 0.33, 0.5, 0, -0.1, 0.9)
    return (G + g) * env, (H + h) * env


def _kunai(cx, cy, s, ang):
    return poe([(1, 0), (0.3, -0.25), (0.25, -0.08), (-0.6, -0.08), (-0.6, 0.08), (0.25, 0.08), (0.3, 0.25)], cx, cy, s, ang)


def selo_ceifador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        a = -0.4 + 0.4 * j
        g, h, _ = voa(T, t, 0.0 + 0.05 * j, 0.3 + 0.05 * j, _kunai(0, 0, 1, 0), -0.95, -0.4 + 0.4 * j, -0.15, -0.05 + 0.15 * (j - 1), 0.17)
        G, H = G + g, H + h
    s = ease_out(rel(t, 0.35, 0.7), 2)
    k = 1 - rel(t, 0.85, 1)
    if s > 0:
        pts = [((0.04 + 0.3 * v * s) * math.cos(v * TAU * 2.5 + t * 2), (0.04 + 0.3 * v * s) * math.sin(v * TAU * 2.5 + t * 2)) for v in np.linspace(0, 1, 60)]
        G += T.polyline(pts, 0.016) * k * 1.3
        segs = []
        for j in range(8):
            a = TAU * j / 8
            segs.append((0.36 * s * math.cos(a), 0.36 * s * math.sin(a), 0.5 * s * math.cos(a), 0.5 * s * math.sin(a), 1.0))
        G += T.lines(segs, 0.014) * k + T.ring(0.36 * s, 0.012, 0, 0) * k
        H += T.gauss(0, 0, 0.05) * k * s
    return G * env, H * env


def futuro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2.2) * (1 - ease_in(rel(t, 0.7, 0.95), 2))
    if abre > 0:
        w = 0.18 * abre
        G += T.ring(1.0, 0.0, 0, 0) * 0
        fenda = [(w * math.sin(math.pi * v) * (1 + 0.15 * math.sin(v * 20 + t * 30)), -0.55 + 1.1 * v) for v in np.linspace(0, 1, 24)]
        fenda += [(-x, y) for x, y in reversed(fenda)]
        g, h = icone(T, fenda, 1.3, 0.6)
        G, H = G + g + T.gauss(0, 0, w * 1.5, 0.5) * 0.5, H + h + T.gauss(0, 0, w * 0.4, 0.4) * abre
    G += raios(T, t, 0.1, 0.8, 4, 5, 0, 0, 0.5)
    G += particulas(T, t, 0.2, 0.9, 30, 7, 0, 0, 0.3, 0.0, 0.012, 0.3)
    g, h = clarao(T, t, 0.85, 0.98, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def lendario(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(3):
        s = ease_out(rel(t, 0.0 + 0.12 * j, 0.5 + 0.12 * j), 2) * (1 - rel(t, 0.8, 1))
        if s > 0:
            r = (0.3 + 0.15 * j) * s * (1 + 0.04 * math.sin(t * 50 + j))
            pts = [(r * 0.8 * math.cos(a), -0.05 + r * math.sin(a) * (1.3 if math.sin(a) < 0 else 0.9)) for a in np.linspace(0, TAU, 40, endpoint=False)]
            pts = [(x * (1 + 0.15 * max(0, -y) * math.sin(y * 30 + t * 40)), y) for x, y in pts]
            G += T.polyline(pts + [pts[0]], 0.025) * (1 - 0.25 * j) * 1.2
            G += T.gauss(0, -0.05, r * 0.6) * 0.15
    G += raios(T, t, 0.1, 0.9, 5, 3, 0, 0, 0.6)
    G += particulas(T, t, 0.1, 1.0, 40, 31, 0, 0.2, 0.5, 0.9)
    return G * env, H * env


def hakai(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        palma = [(-0.12, 0.0), (0.12, 0.0), (0.13, -0.18), (0.08, -0.35), (0.04, -0.2), (0.02, -0.38), (-0.02, -0.2), (-0.05, -0.37),
                 (-0.08, -0.2), (-0.12, -0.3), (-0.13, -0.12)]
        g, h = icone(T, [(-0.45 + x * s * 1.4, 0.1 + y * s * 1.4) for x, y in palma], 1.2, 0.5)
        G, H = G + g + T.gauss(-0.45, -0.1, 0.18) * s * 0.8, H + h
    g, h = clarao(T, t, 0.35, 0.5, 0.2, 0, 0.6)
    G, H = G + g, H + h
    u = rel(t, 0.4, 1.0)
    if u > 0:
        q = np.random.default_rng(23)
        pts = []
        for j in range(140):
            a, d = q.uniform(0, TAU), q.uniform(0, 0.3)
            v = max(0, u - q.uniform(0, 0.4))
            x0, y0 = 0.2 + d * math.cos(a), d * math.sin(a) * 1.3
            gira = v * 3
            pts.append((0.2 + (x0 - 0.2) * math.cos(gira) * (1 + v), y0 - 0.8 * v * v - 0.1 * v, (1 - v) * (0.9 if v > 0 else 0.4)))
        G += T.splats(pts, 0.014) * 1.3
    return G * env, H * env


def fogo_espalha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    g, h = clarao(T, t, 0.0, 0.25, 0, 0, 0.9, 1.3)
    G, H = G + g, H + h
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.45, 0.6))
    for j in range(8):
        a = TAU * j / 8
        g, h = icone(T, poe(CHAMA, 0.15 * s * math.cos(a), 0.15 * s * math.sin(a), 0.12 * s, a + math.pi / 2), s, 0.6)
        G, H = G + g, H + h
    for lado in (-1, 1):
        u = ease_out(rel(t, 0.3, 0.85), 1.6)
        if 0 < u < 1:
            for j in range(8):
                v = u - j * 0.05
                if v <= 0:
                    continue
                x, y = lado * 0.85 * v, -0.15 * math.sin(math.pi * v)
                g, h = icone(T, poe(CHAMA, x, y, 0.15 * (1 - j / 9)), (1 - j / 9) * (1 - rel(u, 0.8, 1)) * 1.3, 0.6)
                G, H = G + g, H + h
    return G * env, H * env


def evoluiu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.9)
    for j in range(5):
        fase = TAU * j / 5 + t * 8
        r = 0.35 + 0.08 * math.sin(j * 1.3)
        pts = [(r * math.cos(fase + 1.6 * v), r * math.sin(fase + 1.6 * v) * 0.8 + 0.05 * math.sin(v * 9)) for v in np.linspace(0, 1, 20)]
        for i in range(len(pts) - 1):
            G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.06 * (i / 20) + 0.01) * k * 1.4
        H += T.gauss(pts[-1][0], pts[-1][1], 0.025) * k
    for j in range(3):
        u = rel(t, 0.5 + 0.08 * j, 0.8 + 0.08 * j)
        if 0 < u < 1:
            y = 0.1 - 0.5 * u - 0.1 * j
            G += T.polyline([(-0.1, y + 0.07), (0, y), (0.1, y + 0.07)], 0.025) * (1 - u) * 1.4
    return G * env, H * env


def sacrificio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    carga = ease_in(rel(t, 0.0, 0.45), 1.6)
    k = 1 - rel(t, 0.45, 0.5)
    G += T.gauss(0, -0.05, 0.06 + 0.1 * carga) * (0.6 + carga) * k
    H += T.gauss(0, -0.05, 0.03 + 0.04 * carga) * (0.8 + carga) * k
    G += T.ring(0.09, 0.02, 0, -0.05) * k * 1.3
    q = np.random.default_rng(29)
    if carga > 0.3:
        for j in range(6):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0, -0.05, 0.35 * carga * math.cos(a), -0.05 + 0.35 * carga * math.sin(a), 3, 0.3), 0.01) * k * 1.2
    g, h = clarao(T, t, 0.45, 0.7, 0, -0.05, 1.2, 1.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.45, 0.9, 0.1, 0.9, 0.06, -0.05) + estouro(T, t, 0.45, 0.9, 24, 3, 0, -0.05, 0.85)
    return G * env, H * env


def briga_de_rua(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cx, cy = -0.45, -0.05
    carga = ease_in(rel(t, 0.0, 0.45), 1.5)
    if t < 0.5:
        G += T.gauss(cx, cy, 0.04 + 0.08 * carga) * (0.6 + carga)
        H += T.gauss(cx, cy, 0.02 + 0.04 * carga) * (0.7 + carga)
        G += converge(T, t, 0.0, 0.45, 14, 5, cx, cy, 0.4)
    u = rel(t, 0.45, 0.7)
    if 0 < u < 1:
        x = cx + 1.35 * ease_in(u, 1.3)
        G += T.gauss(x, cy, 0.14) * 1.3 + T.tapered([(cx, cy, x, cy, 0.7)], 0.18) * 0.6
        H += T.gauss(x, cy, 0.07) * 1.6
    g, h = clarao(T, t, 0.42, 0.55, cx, cy, 0.6)
    G += anel(T, t, 0.45, 0.7, 0.05, 0.3, 0.03, cy, 1.0) * 0
    return (G + g) * env, (H + h) * env


def nao_estava_la(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(4):
        u = rel(t, 0.0 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            x = -0.5 + 0.3 * j
            S = T.polys([(_silhueta(x, 0.05, 1.1), 1.0)])
            G += (S * 0.35 + _borda(T, S, 0.008) * 1.3) * (1 - u) * (0.6 + 0.4 * (j == 3))
    olho = pulso(t, 0.45, 1.0)
    if olho > 0:
        abre = ease_out(rel(t, 0.45, 0.65), 2)
        pts = [(0.2 * math.cos(a), -0.42 + 0.08 * abre * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        G += T.polyline(pts + [pts[0]], 0.014) * olho * 1.4
        H += T.gauss(0, -0.42, 0.025, 0.02 * abre + 0.001) * olho * 2
        G += T.gauss(0, -0.42, 0.12, 0.06) * olho * 0.7
    return G * env, H * env


REGISTRO = [
    ("mu_primeiro", primeiro, GRANDE, "Hayabusa · as shurikens e o corte", False),
    ("mu_punicao", punicao, GRANDE, "Cabeça de Pirâmide · o capacete e a Grande Faca", False),
    ("mu_inalar", inalar, GRANDE, "Kirby · o redemoinho que inala", False),
    ("mu_banana", banana, GRANDE, "Donkey Kong · a casca de banana", False),
    ("mu_vampire_killer", vampire_killer, GRANDE, "Simon Belmont · o chicote e a cruz", False),
    ("mu_areias", areias, GRANDE, "Príncipe da Pérsia · a ampulheta das Areias do Tempo", False),
    ("mu_pegaso", pegaso, GRANDE, "Seiya · a constelação e os meteoros de Pégaso", False),
    ("mu_absorcao", absorcao, GRANDE, "Majin Boo · a gosma rosa que absorve", False),
    ("mu_kuririn_nao", kuririn_nao, GRANDE, "Kuririn · os seis pontos e a fúria dourada", False),
    ("mu_escudo_dragao", escudo_dragao, GRANDE, "Shiryu · o Escudo do Dragão", False),
    ("mu_zero_absoluto", zero_absoluto, GRANDE, "Hyoga · o Pó de Diamante e a aurora", False),
    ("mu_fenix_ikki", fenix_ikki, GRANDE, "Ikki · as asas de fogo da Fênix", False),
    ("mu_rugido_leao", rugido_leao, GRANDE, "Aiolia · o Relâmpago de Plasma", False),
    ("mu_esquife", esquife, GRANDE, "Camus · o Esquife de Gelo", False),
    ("mu_juizo", juizo, GRANDE, "Hades · o eclipse negro do juízo", False),
    ("mu_meteoro", meteoro, GRANDE, "Madara · o meteoro em chamas", False),
    ("mu_shinra_tensei", shinra_tensei, GRANDE, "Pain · o Shinra Tensei", False),
    ("mu_selo_ceifador", selo_ceifador, GRANDE, "Minato · os kunais e o selo do Ceifador", False),
    ("mu_futuro", futuro, GRANDE, "Trunks · a fenda do tempo", False),
    ("mu_lendario", lendario, GRANDE, "Broly · a aura lendária", False),
    ("mu_hakai", hakai, GRANDE, "Beerus · o Hakai", False),
    ("mu_fogo_espalha", fogo_espalha, GRANDE, "Charizard · o fogo que se espalha", False),
    ("mu_evoluiu", evoluiu, GRANDE, "Garou · o Punho da Água Corrente", False),
    ("mu_sacrificio", sacrificio, GRANDE, "Genos · o núcleo que explode", False),
    ("mu_briga_de_rua", briga_de_rua, GRANDE, "Yusuke · a Arma Espiritual", False),
    ("mu_nao_estava_la", nao_estava_la, GRANDE, "Hiei · as imagens para trás e o Jagan", False),
]
