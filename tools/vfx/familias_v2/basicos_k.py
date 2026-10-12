"""Ataques básicos com animação própria, lote k (os personagens novos, 251 em diante).

Senhor Frio, Hera Venenosa, Homem de Gelo, Gengar, Tenshinhan, Deidara, Violeta, Orihime, Aerith, Katara,
Sailor Mercury, Kurama, Ken, Heihachi e Jake: cada folha conta o golpe normal do personagem (o jato da arma
congelante que cristaliza, o chicote de vinha com as folhas, a bola de neve que espatifa, a lambida do
fantasma, o kiai invisível, o passarinho de argila que explode, a bolha de força, o Tsubaki cortando, o
cajado da Cetra, o chicote de água, as bolhas geladas, as pétalas que cortam, o soco em chamas do Ken, o
soco com trovão do Heihachi e o braço de borracha do Jake).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, janela, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _borda(T, a, s=0.008):
    return np.clip(a - T.blur(a, s), 0, 1)


def _contorno(pts, w=1.0):
    return [(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], w) for i in range(len(pts))]


def _estouro(T, t, t0, t1, cx=0.0, cy=0.0, r=0.4, n=10, seed=3, larg=0.022):
    """O impacto padrão: o clarão, o anel que abre e os riscos que saem."""
    u = rel(t, t0, t1)
    if u <= 0 or u >= 1:
        return T.zero(), T.zero()
    e = ease_out(u, 3)
    q = np.random.default_rng(seed)
    riscos = []
    for k in range(n):
        a = TAU * k / n + q.uniform(-0.2, 0.2)
        riscos.append((cx + 0.08 * math.cos(a), cy + 0.08 * math.sin(a), cx + r * (0.4 + 0.6 * e) * math.cos(a), cy + r * (0.4 + 0.6 * e) * math.sin(a), 1 - u))
    G = T.ring(0.05 + r * e, 0.025, cx, cy) * (1 - u) * 1.2 + T.tapered(riscos, larg) * 1.1
    H = T.gauss(cx, cy, 0.06 + 0.06 * e) * (1 - u) ** 2 * 1.8 + T.flare(cx, cy, 0.5 * (1 - u) + 0.01, 0.4, 0.012) * (1 - u)
    return G, H


def _gotas(T, t, t0, dur, cx, cy, n, alcance, seed, a0=0.0, a1=TAU, tam=0.016, cai=0.3):
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    q = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = q.uniform(a0, a1)
        d = q.uniform(0.3, 1.0) * alcance * ease_out(u, 2)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a) + cai * u * u, (1 - u) * q.uniform(0.5, 1)))
    return T.splats(pts, tam)


def _cristal(cx, cy, r, ang):
    """O cristal de gelo: o losango comprido."""
    return _gira([(0, -r), (r * 0.28, 0), (0, r), (-r * 0.28, 0)], ang, cx, cy)


def _folha(cx, cy, tam, ang):
    dx, dy = math.cos(ang) * tam, math.sin(ang) * tam
    return lamina(cx - dx, cy - dy, cx + dx, cy + dy, tam * 0.5)


# ================================================================== Senhor Frio
def jato_criogenico(T, t, rng):
    """O jato da arma congelante: o feixe frio sai da esquerda com o vapor girando em volta, e no rival os
    cristais de gelo crescem de dentro para fora em estrela, com a névoa fria."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vai = ease_out(rel(t, 0.0, 0.2), 2)
    some = 1 - rel(t, 0.35, 0.55)
    if vai > 0 and some > 0:
        x1 = -0.95 + 0.95 * vai
        R = T.lines([(-0.95, 0.0, x1, 0.0, 1.0)], 0.045)
        G += (T.blur(R, 0.02) * 0.9 + R * 0.7) * some
        H += T.lines([(-0.95, 0.0, x1, 0.0, 1.0)], 0.012) * some * 1.3
        pts = [(-0.95 + (x1 + 0.95) * ((k / 14 + t * 2) % 1), 0.07 * math.sin(TAU * ((k / 14 + t * 2) % 1) * 3 + t * 30), 0.7) for k in range(14)]
        G += T.splats(pts, 0.02) * some
    cresce = back(rel(t, 0.18, 0.45), 1.4) * (1 - rel(t, 0.75, 0.95))
    if cresce > 0:
        shapes = []
        for k in range(8):
            a = TAU * k / 8 + 0.2
            r = (0.18 + 0.12 * (k % 2)) * cresce
            shapes.append((_cristal(r * math.cos(a), r * math.sin(a), r, a + math.pi / 2), 1.0))
        C = T.polys(shapes)
        G += C * 0.5 + _borda(T, C, 0.006) * 1.5
        H += _borda(T, C, 0.004) * 0.5 + T.gauss(0, 0, 0.05) * cresce
    G += T.gauss(0, 0.1, 0.4, 0.25) * pulso(t, 0.3, 1.0) * 0.4
    return G * env, H * env


# ================================================================== Hera Venenosa
def chicote_de_vinha(T, t, rng):
    """O chicote de vinha: a vinha sai curvando da esquerda com as folhas pelo caminho, estala no rival e
    solta a nuvem de esporos verdes."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2.2)
    some = 1 - rel(t, 0.4, 0.6)
    if vai > 0 and some > 0:
        pts = []
        for j in range(36):
            u = j / 35 * vai
            x = -0.95 + 0.95 * u
            y = 0.4 * math.sin(math.pi * u) * (1 - u) - 0.25 * u * (1 - u) * math.sin(TAU * u * 2 + t * 6)
            pts.append((x, y))
        V = T.polyline(pts, 0.022)
        G += (V * 1.2 + T.blur(V, 0.015) * 0.4) * some
        folhas = [(_folha(pts[j][0], pts[j][1] - 0.04 * (1 if j % 2 else -1), 0.05, 0.8 if j % 2 else -0.8), 1.0) for j in range(4, len(pts), 5)]
        G += T.polys(folhas) * some * 1.1
    g, h = _estouro(T, t, 0.28, 0.6, 0, 0, 0.3, 8, 4)
    G += g
    H += h
    esporos = rel(t, 0.3, 1.0)
    if 0 < esporos < 1:
        q = np.random.default_rng(9)
        pts = [(q.uniform(-0.35, 0.35) * (0.4 + esporos), q.uniform(-0.3, 0.2) - 0.25 * esporos, (1 - esporos) * q.uniform(0.4, 1)) for _ in range(26)]
        G += T.splats(pts, 0.03) * 0.9
    return G * env, H * env


# ================================================================== Homem de Gelo
def bola_de_neve(T, t, rng):
    """A bola de neve: a bola voa em arco da esquerda girando, espatifa no rival em pedaços de neve e os
    flocos ficam caindo."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    voa = rel(t, 0.0, 0.3)
    if voa < 1:
        x = -0.9 + 0.9 * voa
        y = -0.5 * math.sin(math.pi * voa) * 0.8
        B = T.gauss(x, y, 0.07)
        G += B * 1.3 + T.ring(0.07, 0.012, x, y) * 0.8
        G += T.lines([(x - 0.04, y, x + 0.04, y, 1.0)], 0.01) * 0.0
        G += T.tapered([(x - 0.3, y + 0.12 * (1 - voa), x - 0.06, y, 0.6)], 0.03)
    espatifa = rel(t, 0.3, 0.75)
    if 0 < espatifa < 1:
        q = np.random.default_rng(7)
        pedacos = []
        for _ in range(12):
            a = q.uniform(math.pi, TAU) if q.uniform() < 0.7 else q.uniform(0, math.pi)
            d = (0.1 + 0.5 * ease_out(espatifa, 2)) * q.uniform(0.5, 1)
            pedacos.append((d * math.cos(a), d * math.sin(a) + 0.4 * espatifa ** 2, (1 - espatifa)))
        G += T.splats(pedacos, 0.035) * 1.3
        H += T.gauss(0, 0, 0.1) * (1 - espatifa) ** 3 * 1.5
        G += T.ring(0.1 + 0.3 * espatifa, 0.03, 0, 0, squash=1.4) * (1 - espatifa)
    flocos = pulso(t, 0.35, 1.0)
    if flocos > 0:
        q = np.random.default_rng(11)
        est = []
        for _ in range(9):
            x0 = q.uniform(-0.6, 0.6)
            y = -0.5 + ((t * 0.8 + q.uniform(0, 1)) % 1) * 1.1
            est.append((estrela(x0 + 0.04 * math.sin(t * 8 + x0 * 5), y, 0.035, t * 3, 6, 0.4), flocos))
        G += T.polys(est) * 0.9
    return G * env, H * env


# ================================================================== Gengar
def lambida_fantasma(T, t, rng):
    """A lambida do Gengar: a língua enorme sobe varrendo o rival de baixo para cima, as gotas de baba
    voam, os fiapos de fantasma giram em volta e os riscos do arrepio (o susto que paralisa) tremem."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    lambe = ease_out(rel(t, 0.05, 0.4), 2)
    some = 1 - rel(t, 0.45, 0.65)
    if lambe > 0 and some > 0:
        base = (-0.3, 0.75)
        ponta = (-0.3 + 0.5 * lambe, 0.75 - 1.2 * lambe)
        meio = (-0.45 + 0.2 * lambe, 0.2 - 0.3 * lambe)
        cima, baixo = [], []
        for j in range(24):
            u = j / 23
            x = (1 - u) ** 2 * base[0] + 2 * (1 - u) * u * meio[0] + u * u * ponta[0]
            y = (1 - u) ** 2 * base[1] + 2 * (1 - u) * u * meio[1] + u * u * ponta[1]
            w = 0.13 * (1 - 0.4 * u) * (1 if u < 0.92 else (1 - u) / 0.08)
            cima.append((x - w * 0.8, y))
            baixo.append((x + w * 0.8, y))
        L = T.polys([(cima + baixo[::-1], 1.0)])
        G += (L * 0.6 + _borda(T, L, 0.01) * 1.4) * some
        G += T.lines([((cima[j][0] + baixo[j][0]) / 2, (cima[j][1] + baixo[j][1]) / 2,
                       (cima[j + 3][0] + baixo[j + 3][0]) / 2, (cima[j + 3][1] + baixo[j + 3][1]) / 2, 0.6) for j in range(0, 18, 3)], 0.01) * some
    G += _gotas(T, t, 0.3, 0.5, 0.15, -0.35, 12, 0.5, 21, -2.8, -0.3, 0.02, 0.5) * 1.2
    fios = pulso(t, 0.1, 0.9)
    if fios > 0:
        pts = []
        for k in range(3):
            for j in range(20):
                u = j / 19
                a = TAU * (k / 3 + t * 0.8) + 2.5 * u
                r = 0.55 - 0.2 * u
                pts.append((r * math.cos(a), r * 0.7 * math.sin(a), math.sin(math.pi * u) * 0.8))
        G += T.splats(pts, 0.018) * fios
    arrepio = pulso(t, 0.5, 1.0)
    if arrepio > 0:
        q = np.random.default_rng(int(t * 30) % 5 + 2)
        for lado in (-1, 1):
            G += T.polyline(jagged(q, 0.35 * lado, -0.35, 0.42 * lado, 0.1, 5, 0.6), 0.012) * arrepio * 1.1
    return G * env, H * env


# ================================================================== Tenshinhan
def kiai_invisivel(T, t, rng):
    """O golpe de kiai: o terceiro olho brilha um instante, e a força invisível vem da esquerda como ar
    entortado (os anéis ondulando que avançam) e bate no rival, que é empurrado (os riscos para trás)."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    olho = pulso(t, 0.0, 0.2)
    if olho > 0:
        O = [(-0.75 + 0.06 * math.cos(a), -0.55 + 0.11 * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        G += T.lines(_contorno(O), 0.012) * olho * 1.3
        H += T.gauss(-0.75, -0.55, 0.025) * olho * 1.6 + T.flare(-0.75, -0.55, 0.25 * olho, 0, 0.008) * olho
    for k in range(3):
        u = rel(t, 0.1 + 0.06 * k, 0.4 + 0.06 * k)
        if 0 < u < 1:
            x = -0.85 + 0.85 * ease_in(u, 1.5)
            A = T.arc_band(0.22 + 0.1 * u, 0.035, -1.0, 1.0, cx=x - 0.2, cy=0, taper=0.0)
            du = 0.02 * np.sin(T.V * 30 + t * 40)
            A = T.warp(A, du, du * 0)
            G += A * (1 - u * 0.5) * 1.1
    g, h = _estouro(T, t, 0.38, 0.7, 0, 0, 0.35, 8, 6, 0.018)
    G += g * 0.8
    H += h * 0.6
    empurra = pulso(t, 0.4, 0.85)
    if empurra > 0:
        G += T.tapered([(0.15, -0.3 + 0.15 * k, 0.55 + 0.1 * (k % 2), -0.3 + 0.15 * k, 1.0) for k in range(5)], 0.016) * empurra
    return G * env, H * env


# ================================================================== Deidara
def _passaro(cx, cy, s, bate):
    """O passarinho de argila: o corpo, o bico, a cauda e as asas que batem."""
    corpo = [(cx + 0.12 * s, cy), (cx + 0.04 * s, cy - 0.04 * s), (cx - 0.1 * s, cy - 0.02 * s), (cx - 0.16 * s, cy - 0.06 * s),
             (cx - 0.14 * s, cy + 0.02 * s), (cx - 0.04 * s, cy + 0.05 * s)]
    asa = [(cx + 0.02 * s, cy - 0.02 * s), (cx - 0.08 * s, cy - (0.05 + 0.13 * bate) * s), (cx - 0.04 * s, cy - 0.02 * s)]
    return [corpo, asa]


def argila_explosiva(T, t, rng):
    """A argila explosiva: o passarinho branco de argila voa batendo as asas da esquerda até o rival, para um
    instante, e "Katsu!" — a explosão abre em bola com as faíscas e a fumaça."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = ease_in(rel(t, 0.0, 0.35), 1.3)
    if t < 0.42:
        x = -0.85 + 0.85 * voa
        y = -0.25 * math.sin(math.pi * voa) + 0.02 * math.sin(t * 40)
        bate = 0.5 + 0.5 * math.sin(t * 50)
        shapes = [(p, 1.0) for p in _passaro(x, y, 1.6, bate)]
        P = T.polys(shapes)
        G += P * 0.6 + _borda(T, P, 0.006) * 1.3
    bum = rel(t, 0.4, 0.95)
    if 0 < bum < 1:
        b = ease_out(bum, 3)
        H += T.gauss(0, 0, 0.08 + 0.2 * b) * (1 - bum) ** 2 * 2.2
        G += T.gauss(0, 0, 0.15 + 0.3 * b) * (1 - bum) * 1.3 + T.ring(0.1 + 0.55 * b, 0.04, 0, 0) * (1 - bum) * 1.3
        q = np.random.default_rng(13)
        fa = []
        for _ in range(16):
            a = q.uniform(0, TAU)
            d = (0.2 + 0.6 * b) * q.uniform(0.6, 1.1)
            fa.append((d * 0.7 * math.cos(a), d * 0.7 * math.sin(a), d * math.cos(a), d * math.sin(a), 1 - bum))
        G += T.tapered(fa, 0.016) * 1.2
        fum = [(q.uniform(-0.4, 0.4) * b, q.uniform(-0.3, 0.2) * b - 0.2 * bum, (1 - bum) * 0.6) for _ in range(12)]
        G += T.splats(fum, 0.08) * 0.7
    return G * env, H * env


# ================================================================== Violeta
def empurrao_de_campo(T, t, rng):
    """O empurrão de força da Violeta: o campo de força redondo se forma na frente dela (a bolha com o brilho na
    borda), avança e bate no rival, achatando e soltando a onda."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    forma = back(rel(t, 0.0, 0.2), 1.5)
    vai = ease_in(rel(t, 0.2, 0.42), 2)
    if forma > 0 and t < 0.55:
        x = -0.6 + 0.45 * vai
        r = 0.3 * forma
        achata = 1 + 0.5 * pulso(t, 0.4, 0.55)
        B = T.ring(r / achata, 0.025, x, 0, squash=1 / achata) + T.ring(r * 0.85 / achata, 0.01, x, 0, squash=1 / achata) * 0.6
        G += B * 1.3 + T.gauss(x, 0, r * 0.7) * 0.3
        H += T.arc_band(r * 0.8, 0.02, -2.4, -1.6, cx=x, cy=0, taper=0.0) * 0.9
    onda = rel(t, 0.42, 0.85)
    if 0 < onda < 1:
        G += T.ring(0.2 + 0.5 * ease_out(onda, 2), 0.035, 0.0, 0, squash=0.8) * (1 - onda) * 1.3
        H += T.gauss(0, 0, 0.1) * (1 - onda) ** 2 * 1.4
    return G * env, H * env


# ================================================================== Orihime
def tsubaki(T, t, rng):
    """O Tsubaki da Orihime: o grampo de flor de seis pétalas brilha, a fadinha dispara como uma lâmina fina de
    luz (o escudo pontudo) e corta o rival de lado a lado."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    flor = pulso(t, 0.0, 0.3)
    if flor > 0:
        shapes = [(_folha(-0.7 + 0.07 * math.cos(TAU * k / 6), -0.5 + 0.07 * math.sin(TAU * k / 6), 0.05, TAU * k / 6), 1.0) for k in range(6)]
        F = T.polys(shapes)
        G += (F * 0.6 + _borda(T, F, 0.006) * 1.2) * flor
        H += T.gauss(-0.7, -0.5, 0.025) * flor * 1.6
    voa = ease_in(rel(t, 0.15, 0.35), 1.8)
    if 0 < voa and t < 0.5:
        x = -0.7 + 1.2 * voa
        y = -0.5 + 0.55 * voa
        cunha = _gira([(0.1, 0), (-0.06, -0.05), (-0.03, 0), (-0.06, 0.05)], math.atan2(0.55, 1.2), x, y)
        W = T.polys([(cunha, 1.0)])
        G += W * 1.3 + T.tapered([(x - 0.4, y - 0.18, x, y, 1.0)], 0.03) * 0.9
        H += T.gauss(x, y, 0.03) * 1.3
    corta = rel(t, 0.28, 0.75)
    if 0 < corta < 1:
        L = T.polys([(lamina(-0.7, -0.4, 0.7, 0.35, 0.05, prog=min(1, corta * 4), inicio=max(0, corta * 1.3 - 0.3)), 1.0)])
        G += L * 1.5 + T.blur(L, 0.02) * 0.6
        H += L * 0.7
    g, h = _estouro(T, t, 0.32, 0.7, 0, 0, 0.32, 8, 12, 0.016)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Aerith
def cajado_da_cetra(T, t, rng):
    """O golpe de cajado da Aerith: o cajado gira num arco por cima e bate, e as luzinhas verdes da Corrente da
    Vida sobem do ponto do golpe junto com duas pétalas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    gira = ease_out(rel(t, 0.0, 0.3), 2)
    if 0 < gira and t < 0.5:
        ang = -2.6 + 2.2 * gira
        px, py = -0.45, 0.35
        tip = (px + 0.85 * math.cos(ang), py + 0.85 * math.sin(ang))
        C = T.lines([(px, py, tip[0], tip[1], 1.0)], 0.022)
        G += C * 1.2 * (1 - rel(t, 0.35, 0.5))
        G += T.ring(0.05, 0.012, tip[0], tip[1]) * 1.2 + T.gauss(tip[0], tip[1], 0.03) * 1.0
        G += T.arc_band(0.85, 0.03, -2.6, ang, cx=px, cy=py, taper=0.8) * 0.6
    g, h = _estouro(T, t, 0.28, 0.6, 0.15, -0.05, 0.28, 8, 8, 0.016)
    G += g * 0.9
    H += h * 0.8
    sobe = rel(t, 0.3, 1.0)
    if 0 < sobe < 1:
        q = np.random.default_rng(15)
        pts = []
        for _ in range(16):
            f = (sobe + q.uniform(0, 0.6)) % 1
            pts.append((0.15 + q.uniform(-0.3, 0.3) + 0.04 * math.sin(t * 10 + f * 6), -0.05 - 0.7 * f, math.sin(math.pi * f) * (1 - sobe * 0.5)))
        G += T.splats(pts, 0.018) * 1.2
        H += T.splats(pts, 0.007) * 0.8
        for k in range(2):
            G += T.polys([(_folha(0.3 * (k - 0.5) + 0.15, -0.1 - 0.4 * sobe, 0.04, t * 5 + k), 1.0)]) * (1 - sobe)
    return G * env, H * env


# ================================================================== Katara
def chicote_de_agua(T, t, rng):
    """O jato de água da Katara: a fita de água sai serpenteando da esquerda (grossa e com o brilho correndo),
    estala no rival e espirra em gotas para todo lado."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2)
    some = 1 - rel(t, 0.38, 0.58)
    if vai > 0 and some > 0:
        cima, baixo, meio = [], [], []
        for j in range(30):
            u = j / 29 * vai
            x = -0.95 + 0.95 * u
            y = 0.18 * math.sin(TAU * u * 1.5 - t * 10) * (1 - u)
            w = 0.05 * (0.4 + 0.6 * math.sin(math.pi * min(1, u / max(vai, 1e-3))))
            cima.append((x, y - w))
            baixo.append((x, y + w))
            meio.append((x, y - w * 0.4))
        A = T.polys([(cima + baixo[::-1], 1.0)])
        G += (A * 0.7 + _borda(T, A, 0.008) * 1.2) * some
        H += T.polyline(meio, 0.008) * some * 0.8
    G += _gotas(T, t, 0.28, 0.55, 0.0, 0.0, 22, 0.6, 19, 0, TAU, 0.018, 0.4) * 1.3
    g, h = _estouro(T, t, 0.28, 0.55, 0, 0, 0.22, 6, 3, 0.014)
    G += g * 0.6
    H += h * 0.6
    return G * env, H * env


# ================================================================== Sailor Mercury
def bolhas_de_mercurio(T, t, rng):
    """As bolhas da Sailor Mercury: as bolhas saem da esquerda boiando e crescendo (o contorno e o brilhinho de
    cada uma), chegam no rival e estouram em névoa fria."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = np.random.default_rng(31)
    for k in range(9):
        t0 = 0.02 * k
        u = rel(t, t0, t0 + 0.45)
        estoura = rel(t, t0 + 0.45, t0 + 0.6)
        if u <= 0:
            continue
        y0 = q.uniform(-0.35, 0.35)
        r = q.uniform(0.05, 0.1) * (0.4 + 0.6 * u)
        x = -0.85 + (0.85 + q.uniform(-0.2, 0.2)) * ease_out(u, 1.5)
        y = y0 * (1 - u) + 0.04 * math.sin(t * 12 + k)
        if estoura <= 0:
            G += T.ring(r, 0.008, x, y) * 1.3
            H += T.gauss(x - r * 0.4, y - r * 0.4, r * 0.18) * 0.9
        elif estoura < 1:
            G += T.ring(r * (1 + estoura), 0.006, x, y) * (1 - estoura) * 1.2
    nevoa = pulso(t, 0.45, 1.0)
    G += T.gauss(0, 0, 0.45, 0.3) * nevoa * 0.45
    return G * env, H * env


# ================================================================== Kurama
def petalas_cortantes(T, t, rng):
    """As pétalas cortantes do Kurama: as pétalas de rosa vêm girando em espiral da esquerda, afiadas, e cortam
    o rival em vários riscos finos ao passar; depois caem devagar."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = np.random.default_rng(41)
    shapes = []
    for k in range(14):
        t0 = 0.015 * k
        u = rel(t, t0, t0 + 0.4)
        if u <= 0:
            continue
        fase = q.uniform(0, TAU)
        if u < 1:
            x = -0.95 + 1.3 * u
            y = 0.25 * math.sin(fase + u * 7) * (1 - u * 0.5)
        else:
            cai = rel(t, t0 + 0.4, 1.0)
            x = 0.35 + 0.1 * math.sin(fase + t * 5)
            y = 0.25 * math.sin(fase + 7) * 0.5 + 0.6 * cai
        shapes.append((_folha(x, y, 0.045, fase + t * 12), 1.0 - rel(t, 0.75, 1.0)))
    P = T.polys(shapes)
    G += P * 0.8 + _borda(T, P, 0.005) * 1.0
    for k, t0 in enumerate((0.2, 0.26, 0.32)):
        u = rel(t, t0, t0 + 0.2)
        if 0 < u < 1:
            y = -0.2 + 0.2 * k
            G += T.polys([(lamina(-0.45, y - 0.1, 0.45, y + 0.1, 0.018, prog=min(1, u * 3)), 1.0)]) * (1 - u) * 1.4
    return G * env, H * env


# ================================================================== Ken
def punho_flamejante_ken(T, t, rng):
    """O soco do Ken: o punho avança da esquerda com a chama envolvendo e a esteira de fogo atrás, acerta com o
    clarão e solta as brasas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vai = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.45:
        x = -0.8 + 0.7 * vai
        P, nos = _punho(T, x, 0.0, 1.5)
        G += P * 0.8 + _borda(T, P, 0.006) * 1.0
        H += nos * 0.5
        q = np.random.default_rng(int(t * 40) % 7)
        chamas = []
        for k in range(7):
            yy = (k - 3) * 0.04
            L = 0.25 + 0.2 * q.uniform()
            chamas.append((lamina(x - L, yy + q.uniform(-0.03, 0.03), x + 0.1, yy * 0.5, 0.035), 1.0))
        F = T.polys(chamas)
        G += F * 0.8 + T.blur(F, 0.02) * 0.6
        H += F * 0.3
    g, h = _estouro(T, t, 0.25, 0.6, 0.0, 0, 0.38, 10, 5)
    G += g
    H += h
    G += _gotas(T, t, 0.3, 0.6, 0.0, 0.0, 14, 0.55, 23, -2.8, 0.4, 0.014, -0.2) * 1.3
    return G * env, H * env


# ================================================================== Heihachi
def punho_do_trovao(T, t, rng):
    """O soco do trovão do Heihachi: o punho sobe em gancho de baixo, os raios curtos estalam em volta do braço,
    e no acerto o trovão desce no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sobe = ease_out(rel(t, 0.0, 0.28), 2)
    if t < 0.45:
        x, y = -0.35 + 0.35 * sobe, 0.7 - 0.75 * sobe
        P, nos = _punho(T, x, y, 1.5, -math.pi / 2 + 0.3)
        G += P * 0.8 + _borda(T, P, 0.006) * 1.0
        H += nos * 0.5
        G += T.tapered([(x - 0.15, y + 0.45, x, y + 0.05, 1.0)], 0.05) * 0.7
        q = np.random.default_rng(int(t * 40) % 9 + 1)
        for k in range(3):
            G += T.polyline(jagged(q, x - 0.12, y + 0.1 + 0.12 * k, x + 0.12, y + 0.05 + 0.12 * k, 4, 0.5), 0.01) * 1.2
    raio = pulso(t, 0.25, 0.55)
    if raio > 0:
        q = np.random.default_rng(int(t * 30) % 5 + 20)
        R = T.polyline(jagged(q, 0.05, -1.0, 0.0, -0.05, 7, 0.25), 0.02)
        G += R * raio * 1.3 + T.blur(R, 0.02) * raio * 0.6
        H += R * raio * 0.8
    g, h = _estouro(T, t, 0.28, 0.65, 0.0, -0.05, 0.38, 10, 7)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Jake
def punho_esticado(T, t, rng):
    """O soco esticado do Jake: o braço de borracha estica da esquerda ondulando (o tubo que se alonga), o punho
    gigante bate no rival com um "boing" (o punho achata e volta) e o braço volta encolhendo."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    estica = ease_out(rel(t, 0.0, 0.3), 2.5) * (1 - ease_in(rel(t, 0.55, 0.85), 2))
    if estica > 0.02:
        fim = -0.9 + 0.82 * estica
        pts = []
        for j in range(30):
            u = j / 29
            x = -0.9 + (fim + 0.9) * u
            y = 0.25 + 0.12 * math.sin(TAU * u * 2 + t * 20) * (1 - estica * 0.7) - 0.25 * u
            pts.append((x, y))
        Bc = T.polyline(pts, 0.05)
        G += Bc * 0.5 + _borda(T, Bc, 0.008) * 1.3
        achata = 1 + 0.4 * pulso(t, 0.28, 0.45)
        P = T.polys([(_move([(px / achata, py * achata) for px, py in _PUNHO], fim + 0.08, 0.0, 1.7), 1.0)])
        G += P * 0.5 + _borda(T, P, 0.008) * 1.3
    g, h = _estouro(T, t, 0.28, 0.6, 0.15, 0, 0.35, 8, 9)
    G += g
    H += h
    return G * env, H * env


REGISTRO = [
    ("jato_criogenico", jato_criogenico, GRANDE, "Básico do Senhor Frio: o jato frio e os cristais", False),
    ("chicote_de_vinha", chicote_de_vinha, GRANDE, "Básico da Hera Venenosa: a vinha com folhas e os esporos", False),
    ("bola_de_neve", bola_de_neve, GRANDE, "Básico do Homem de Gelo: a bola de neve espatifando", False),
    ("lambida_fantasma", lambida_fantasma, GRANDE, "Básico do Gengar: a lambida, a baba e o arrepio", False),
    ("kiai_invisivel", kiai_invisivel, GRANDE, "Básico do Tenshinhan: o terceiro olho e o kiai", False),
    ("argila_explosiva", argila_explosiva, GRANDE, "Básico do Deidara: o passarinho de argila e o Katsu", False),
    ("empurrao_de_campo", empurrao_de_campo, GRANDE, "Básico da Violeta: a bolha de força empurrando", False),
    ("tsubaki", tsubaki, GRANDE, "Básico da Orihime: a flor do grampo e o Tsubaki cortando", False),
    ("cajado_da_cetra", cajado_da_cetra, GRANDE, "Básico da Aerith: o cajado e as luzes da Corrente da Vida", False),
    ("chicote_de_agua", chicote_de_agua, GRANDE, "Básico da Katara: a fita de água e as gotas", False),
    ("bolhas_de_mercurio", bolhas_de_mercurio, GRANDE, "Básico da Sailor Mercury: as bolhas e a névoa fria", False),
    ("petalas_cortantes", petalas_cortantes, GRANDE, "Básico do Kurama: as pétalas em espiral cortando", False),
    ("punho_flamejante_ken", punho_flamejante_ken, GRANDE, "Básico do Ken: o soco em chamas", False),
    ("punho_do_trovao", punho_do_trovao, GRANDE, "Básico do Heihachi: o gancho e o trovão", False),
    ("punho_esticado", punho_esticado, GRANDE, "Básico do Jake: o braço de borracha e o boing", False),
]
