"""Ataques básicos com animação própria, lote t (personagens novos, fecha os 150).

Megamente, Vilgax, Cosmo e Wanda, Steve, Creeper, Pac-Man, Crash, Arthur Morgan, Ellie, Sans, Cuphead, Dovahkiin,
O Cavaleiro, Goro e Yoshi: o raio azul da pistola desidratadora que espreme o rival num cubinho, o soco verde com
os tentáculos do Vilgax, as varinhas com estrela soltando o "puf", a espada de diamante em pixels, o Creeper
piscando branco e explodindo em blocos, o Pac-Man comendo as pastilhas até o rival, o giro tornado do Crash com
as frutas Wumpa, os X vermelhos do Dead Eye, o canivete da Ellie, os ossos do Sans com o olho azul, a ervilha
disparada do dedo do Cuphead, o Fus Ro Dah em ondas com as runas, o ferrão do Cavaleiro com a alma branca, os
quatro punhos do Goro e a língua comprida do Yoshi com o ovo.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .basicos_k import _borda, _estouro, _gira, _gotas
from .basicos_l import _estrelinhas


def _quadrado(cx, cy, r, ang=0.0):
    return _gira([(-r, -r), (r, -r), (r, r), (-r, r)], ang, cx, cy)


def _blocos(T, t, t0, dur, cx, cy, n, alcance, seed, tam=0.035, cai=0.35):
    """Os cubinhos que voam girando (a explosão de blocos, estilo pixel)."""
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    q = np.random.default_rng(seed)
    shapes = []
    for _ in range(n):
        a = q.uniform(0, TAU)
        d = q.uniform(0.3, 1.0) * alcance * ease_out(u, 2)
        r = tam * q.uniform(0.6, 1.2)
        shapes.append((_quadrado(cx + d * math.cos(a), cy + d * math.sin(a) + cai * u * u, r, q.uniform(0, 1) + u * q.uniform(-4, 4)), (1 - u) * q.uniform(0.6, 1)))
    return T.polys(shapes)


# ================================================================== Megamente
def pistola_de_megamente(T, t, rng):
    """A pistola desidratadora do Megamente: o raio azul em espiral com os anéis correndo dentro sai do cano, envolve o
    rival e o espreme num cubinho azul que brilha e cai."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cano = (-0.75, 0.0)
    carga = pulso(t, 0.0, 0.25)
    H += T.gauss(cano[0], cano[1], 0.04 + 0.03 * carga) * carga * 1.5
    G += T.ring(0.06 + 0.04 * carga, 0.01, cano[0], cano[1]) * carga
    vai = ease_out(rel(t, 0.15, 0.3), 2)
    some = 1 - rel(t, 0.42, 0.55)
    if vai > 0 and some > 0:
        x = cano[0] + (0 - cano[0]) * vai
        R = T.lines([(cano[0], 0, x, 0, 1.0)], 0.05)
        G += (R * 0.7 + T.blur(R, 0.02) * 0.5) * some
        H += T.lines([(cano[0], 0, x, 0, 1.0)], 0.008) * some
        hel = [(cano[0] + (x - cano[0]) * u, 0.09 * math.sin(u * 22 - t * 50)) for u in np.linspace(0, 1, 40)]
        G += T.polyline(hel, 0.01) * some * 1.1
        for k in range(4):
            u = (t * 4 + k / 4) % 1
            if u < vai:
                G += T.ring(0.09, 0.012, cano[0] + (0 - cano[0]) * u, 0, squash=2.5) * some * 1.1
    # o rival envolto: o campo azul que aperta e vira o cubo
    aperta = rel(t, 0.28, 0.5)
    if 0 < aperta and t < 0.62:
        r = 0.35 * (1 - ease_in(aperta, 2)) + 0.05
        G += T.ring(r, 0.02, 0, 0) * (1 - aperta * 0.5)
        H += T.gauss(0, 0, r * 0.7) * 0.4 * (1 - aperta)
    cubo = rel(t, 0.45, 0.95)
    if 0 < cubo < 1:
        y = 0.4 * ease_in(rel(t, 0.62, 0.85), 2)
        b = 1 - rel(t, 0.8, 0.95)
        C = T.polys([(_quadrado(0, y, 0.11, 0.3 + cubo * 2), 1.0)])
        G += (C * 0.6 + _borda(T, C, 0.006) * 1.6) * b
        H += T.gauss(0, y, 0.09) * pulso(cubo, 0.0, 0.4) * 1.4
    g, h = _estouro(T, t, 0.42, 0.62, 0, 0, 0.25, 8, 41, 0.014)
    G += g * 0.7
    H += h * 0.7
    return G * env, H * env


# ================================================================== Vilgax
def soco_de_vilgax(T, t, rng):
    """O soco do Vilgax: o punho enorme e escamoso vem com os tentáculos do rosto chicoteando junto, acerta com força
    bruta e o chão treme (as ondas e as rachaduras)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    vai = ease_in(rel(t, 0.05, 0.3), 2.2)
    if t < 0.5:
        some = 1 - rel(t, 0.38, 0.5)
        x = -0.85 + 0.75 * vai
        P, nos = _punho(T, x, 0.0, 2.1)
        escamas = T.splats([(x - 0.15 + 0.08 * (k % 3), -0.08 + 0.08 * (k // 3), 0.7) for k in range(9)], 0.012)
        G += (P * 0.55 + _borda(T, P, 0.008) * 1.5 + escamas * P * 0.6) * some
        H += nos * some * 0.8
        for k in range(4):
            fase = k * 1.3
            pts = [(x - 0.35 - 0.4 * u, -0.25 + 0.06 * k + 0.08 * math.sin(u * 7 + t * 25 + fase) * u, ) for u in np.linspace(0, 1, 16)]
            G += T.polyline(pts, 0.022 - 0.004 * k) * some * 0.9
    tremor = rel(t, 0.3, 0.75)
    if 0 < tremor < 1:
        for k in range(3):
            r = 0.15 + 0.6 * ease_out(rel(tremor, 0.12 * k, 1), 2)
            G += T.ring(r, 0.012, 0, 0.3, squash=4.0) * (1 - tremor) * 1.1
        q = np.random.default_rng(43)
        for k in range(5):
            a = math.pi * (0.1 + 0.8 * k / 4)
            pts = jagged(q, 0, 0.3, 0.5 * math.cos(a) * 1.4, 0.3 + 0.12 * math.sin(a), 4, 0.25)
            G += T.polyline(pts, 0.012) * (1 - tremor) * min(1, tremor * 4)
    g, h = _estouro(T, t, 0.28, 0.6, 0.05, 0, 0.45, 12, 45, 0.026)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Cosmo e Wanda
def puf_das_varinhas(T, t, rng):
    """As varinhas de Cosmo e Wanda: as duas varinhas com estrela na ponta giram e soltam as faíscas, e o desejo
    estoura no rival num "puf" de nuvem com estrelinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    gira = pulso(t, 0.0, 0.4)
    if gira > 0:
        for k, (bx, by, cor) in enumerate(((-0.72, -0.15, 1.0), (-0.58, 0.12, 1.0))):
            a = -0.9 + 0.6 * math.sin(t * 25 + k * 2)
            tx, ty = bx + 0.25 * math.cos(a), by + 0.25 * math.sin(a)
            G += T.lines([(bx, by, tx, ty, 1.0)], 0.012) * gira
            S = T.polys([(estrela(tx, ty, 0.07, t * 6, 5, 0.45), 1.0)])
            G += (S * 0.8 + _borda(T, S, 0.005)) * gira
            H += T.gauss(tx, ty, 0.035) * gira * 1.2
            q = np.random.default_rng(47 + k)
            pts = [(tx + q.uniform(-0.1, 0.25), ty + q.uniform(-0.12, 0.12), q.uniform(0.3, 1) * gira) for _ in range(10)]
            H += T.splats(pts, 0.01)
    vai = ease_out(rel(t, 0.2, 0.35), 2)
    if 0 < vai and t < 0.42:
        pts = [(-0.55 + 0.55 * u, -0.05 - 0.15 * math.sin(u * math.pi), 1.0) for u in np.linspace(0, vai, 12)]
        H += T.splats(pts, 0.018) * 1.2
    puf = rel(t, 0.35, 0.8)
    if 0 < puf < 1:
        e = ease_out(puf, 3)
        q = np.random.default_rng(51)
        bolas = [(0.25 * e * math.cos(TAU * k / 8 + q.uniform(-0.2, 0.2)), 0.2 * e * math.sin(TAU * k / 8), 1.0) for k in range(8)]
        N = sum(T.gauss(x, y, 0.1 + 0.05 * e) for x, y, _ in bolas) + T.gauss(0, 0, 0.15 * e + 0.02)
        G += np.clip(N, 0, 1) * (1 - puf) * 0.9 + _borda(T, np.clip(N, 0, 1), 0.01) * (1 - puf) * 1.2
    G += _estrelinhas(T, t, 0.38, 0.5, 0, 0, 7, 0.45, 53)
    H += T.flare(0, 0, 0.5 * pulso(t, 0.35, 0.55) + 0.01, 0.3, 0.012) * pulso(t, 0.35, 0.55)
    return G * env, H * env


# ================================================================== Steve
def espada_de_diamante(T, t, rng):
    """A espada de diamante do Steve: a espada pixelada (lâmina em degraus, guarda e cabo quadrados) desce num golpe e
    o rival pisca, soltando as partículas quadradas do dano."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    desce = ease_in(rel(t, 0.05, 0.3), 1.8)
    if t < 0.5:
        some = 1 - rel(t, 0.38, 0.5)
        ang = -2.2 + 2.0 * desce
        px, py = -0.35, 0.35
        c, s = math.cos(ang), math.sin(ang)
        quad = []
        passo = 0.06
        for k in range(12):
            d = 0.12 + passo * k
            quad.append((_quadrado(px + d * c, py + d * s, 0.032, ang), 1.0))
            if k < 10:
                quad.append((_quadrado(px + d * c - 0.04 * s, py + d * s + 0.04 * c, 0.02, ang), 0.7))
        for k in (-2, -1, 1, 2):
            quad.append((_quadrado(px + 0.12 * c - k * 0.045 * s, py + 0.12 * s + k * 0.045 * c, 0.025, ang), 0.9))
        quad.append((_quadrado(px + 0.04 * c, py + 0.04 * s, 0.028, ang), 0.7))
        E = T.polys(quad)
        G += (E * 0.6 + _borda(T, E, 0.006) * 1.4) * some
        H += T.splats([(px + (0.2 + 0.55 * u) * c, py + (0.2 + 0.55 * u) * s, 0.6) for u in (0.2, 0.6)], 0.02) * some
        if desce > 0.2:
            A = T.arc_band(0.75, 0.05, ang - 1.2, ang, cx=px, cy=py, crescente=True)
            G += A * some * 0.7
    pisca = pulso(t, 0.3, 0.5)
    H += T.gauss(0, 0, 0.18) * pisca * 1.3 * (0.5 + 0.5 * math.cos(t * 80))
    G += _blocos(T, t, 0.3, 0.45, 0, 0, 12, 0.4, 55, 0.025)
    g, h = _estouro(T, t, 0.3, 0.55, 0, 0, 0.3, 8, 57)
    G += g * 0.7
    H += h * 0.6
    return G * env, H * env


# ================================================================== Creeper
def ssss_do_creeper(T, t, rng):
    """O Creeper: chega silencioso, o rosto quadrado (os olhos e a boca em blocos) incha piscando branco cada vez mais
    rápido — "ssss" — e explode em blocos e fumaça."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    infla = rel(t, 0.0, 0.42)
    if t < 0.45:
        esc = 1 + 0.25 * ease_in(infla, 2)
        cx, cy = 0.0, -0.05
        r = 0.2 * esc
        rosto = T.polys([(_quadrado(cx, cy, r), 1.0)])
        olhos = T.polys([(_quadrado(cx - 0.08 * esc, cy - 0.06 * esc, 0.04 * esc), 1.0), (_quadrado(cx + 0.08 * esc, cy - 0.06 * esc, 0.04 * esc), 1.0)])
        boca = T.polys([(_quadrado(cx, cy + 0.04 * esc, 0.035 * esc), 1.0), (_quadrado(cx - 0.05 * esc, cy + 0.1 * esc, 0.03 * esc), 1.0), (_quadrado(cx + 0.05 * esc, cy + 0.1 * esc, 0.03 * esc), 1.0)])
        G += np.clip(_borda(T, rosto, 0.008) * 1.5 + rosto * 0.3 - (olhos + boca) * 0.4, 0, None) + (olhos + boca) * 0.2
        freq = 6 + 40 * infla
        pisca = 0.5 + 0.5 * math.sin(t * freq * TAU / 2)
        H += rosto * pisca * (0.3 + 0.9 * infla)
    boom = rel(t, 0.42, 0.85)
    if 0 < boom < 1:
        e = ease_out(boom, 3)
        H += T.gauss(0, -0.05, 0.1 + 0.3 * e) * (1 - boom) ** 1.5 * 2.2
        G += T.ring(0.1 + 0.55 * e, 0.04, 0, -0.05) * (1 - boom) * 1.2
        q = np.random.default_rng(59)
        fumo = [(0.5 * e * math.cos(a) * q.uniform(0.6, 1), -0.05 + 0.4 * e * math.sin(a) * q.uniform(0.6, 1) - 0.15 * boom, 1 - boom) for a in np.linspace(0, TAU, 12, endpoint=False)]
        G += T.splats(fumo, 0.06) * 0.7
    G += _blocos(T, t, 0.42, 0.5, 0, -0.05, 18, 0.65, 61, 0.035)
    return G * env, H * env


# ================================================================== Pac-Man
def _pacman(cx, cy, r, abre, ang=0.0, n=30):
    a0 = abre * 0.8
    pts = [(cx, cy)]
    for a in np.linspace(a0, TAU - a0, n):
        pts.append((cx + r * math.cos(a + ang), cy + r * math.sin(a + ang)))
    return pts


def chomp_do_pacman(T, t, rng):
    """O Pac-Man: vem abrindo e fechando a boca e comendo a fileira de pastilhas até o rival, e dá a mordida final
    ("wakka") nele."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    anda = ease_out(rel(t, 0.0, 0.42), 1.3)
    x = -0.8 + 0.72 * anda
    if t < 0.6:
        some = 1 - rel(t, 0.5, 0.6)
        abre = abs(math.sin(t * 28))
        P = T.polys([(_pacman(x, 0, 0.15, abre), 1.0)])
        G += (P * 0.7 + _borda(T, P, 0.008) * 1.4) * some
        H += T.gauss(x - 0.02, -0.07, 0.015) * some * 0.4
        pas = [(px, 0, 1.0) for px in np.arange(-0.6, -0.05, 0.11) if px > x + 0.05]
        if pas:
            H += T.splats(pas, 0.018) * 1.3 * some
            G += T.splats(pas, 0.03) * 0.5 * some
    mord = rel(t, 0.38, 0.55)
    if 0 < mord < 1:
        fecha = 1 - abs(math.sin(mord * math.pi * 2))
        P = T.polys([(_pacman(-0.05, 0, 0.22, fecha * 0.9), 1.0)])
        G += (P * 0.5 + _borda(T, P, 0.008) * 1.4) * (1 - rel(t, 0.5, 0.58))
    g, h = _estouro(T, t, 0.45, 0.7, 0.05, 0, 0.32, 10, 63)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Crash
def giro_do_crash(T, t, rng):
    """O giro do Crash: o tornado laranja (as faixas em espiral girando com o rastro) vem rodopiando, bate no rival e
    as frutas Wumpa e as lascas de caixote voam."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    anda = ease_out(rel(t, 0.0, 0.38), 1.6)
    if t < 0.55:
        some = 1 - rel(t, 0.42, 0.55)
        cx = -0.75 + 0.7 * anda
        for k in range(5):
            a = t * 45 + k * TAU / 5
            y = -0.25 + 0.12 * k
            G += T.arc_band(0.17 - 0.015 * abs(k - 2), 0.025, a, a + 3.0, squash=0.35, cx=cx, cy=y, taper=0.7) * some * 1.2
        G += T.blur(T.lines([(cx, -0.3, cx, 0.3, 1.0)], 0.12), 0.03) * 0.25 * some
        for k in range(3):
            G += T.lines([(cx - 0.25 - 0.15 * k, -0.15 + 0.15 * k, cx - 0.2, -0.15 + 0.15 * k, 1.0)], 0.01) * some * 0.6
    u = rel(t, 0.35, 0.85)
    if 0 < u < 1:
        q = np.random.default_rng(65)
        for k in range(4):
            a = -math.pi * q.uniform(0.15, 0.85)
            d = 0.45 * ease_out(u, 2)
            fx, fy = d * math.cos(a), d * math.sin(a) + 0.5 * u * u
            G += T.ring(0.04, 0.012, fx, fy) * (1 - u)
            H += T.gauss(fx - 0.012, fy - 0.012, 0.012) * (1 - u)
        shapes = []
        for k in range(6):
            a = q.uniform(0, TAU)
            d = 0.5 * ease_out(u, 2) * q.uniform(0.5, 1)
            shapes.append((_gira([(-0.06, -0.012), (0.06, -0.012), (0.06, 0.012), (-0.06, 0.012)], q.uniform(0, 3) + u * 6, d * math.cos(a), d * math.sin(a) + 0.4 * u * u), 1 - u))
        G += T.polys(shapes) * 0.9
    g, h = _estouro(T, t, 0.35, 0.62, 0, 0, 0.35, 10, 67)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Arthur Morgan
def dead_eye(T, t, rng):
    """O Dead Eye do Arthur Morgan: o tempo para (a vinheta sépia fecha), os X vermelhos são marcados um a um no rival
    e os tiros saem todos de uma vez, em sequência rápida."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    lento = pulso(t, 0.0, 0.6)
    mira = 0.55 - 0.3 * ease_out(rel(t, 0.0, 0.25), 2)
    G += T.ring(mira, 0.012, 0, 0) * lento * 0.9 + T.lines([(-mira - 0.08, 0, -mira + 0.06, 0, 1.0), (mira - 0.06, 0, mira + 0.08, 0, 1.0), (0, -mira - 0.08, 0, -mira + 0.06, 1.0), (0, mira - 0.06, 0, mira + 0.08, 1.0)], 0.01) * lento * 0.8
    marcas = ((-0.06, -0.12), (0.08, 0.0), (-0.04, 0.1))
    for k, (mx, my) in enumerate(marcas):
        aparece = rel(t, 0.05 + 0.07 * k, 0.1 + 0.07 * k)
        tiro = 0.32 + 0.05 * k
        if aparece > 0 and t < tiro + 0.04:
            s = 0.06 * ease_out(aparece, 3)
            X = T.lines([(mx - s, my - s, mx + s, my + s, 1.0), (mx - s, my + s, mx + s, my - s, 1.0)], 0.022)
            G += X * 1.3
            H += X * 0.5
        c = pulso(t, tiro - 0.02, tiro + 0.06)
        if c > 0:
            H += T.flare(-0.8, 0.0, 0.3 * c + 0.01, 0, 0.012) * c
            G += T.tapered([(-0.8, 0, mx, my, 1.0)], 0.014) * c * 1.4
            H += T.gauss(mx, my, 0.04) * c * 1.5
    for k, (mx, my) in enumerate(marcas):
        g, h = _estouro(T, t, 0.33 + 0.05 * k, 0.55 + 0.05 * k, mx, my, 0.18, 7, 69 + k, 0.014)
        G += g * 0.8
        H += h * 0.7
    return G * env, H * env


# ================================================================== Ellie
def canivete_de_ellie(T, t, rng):
    """O canivete da Ellie: a lâmina abre com o estalo, ela avança abaixada e dá duas facadas rápidas e sujas (o
    risco curto e o golpe de baixo para cima)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    abre = ease_out(rel(t, 0.0, 0.1), 3)
    if t < 0.2:
        a = -0.5 - 1.6 * (1 - abre)
        bx, by = -0.75, 0.1
        G += T.lines([(bx - 0.1, by + 0.05, bx, by, 1.0)], 0.022)
        L = T.polys([(lamina(bx, by, bx + 0.2 * math.cos(a), by + 0.2 * math.sin(a), 0.022), 1.0)])
        G += L * 1.2
        H += T.flare(bx + 0.2 * math.cos(a), by + 0.2 * math.sin(a), 0.2, 0.3, 0.01) * pulso(t, 0.06, 0.16)
    for k, (x1, y1, x2, y2, t0) in enumerate(((-0.35, -0.1, 0.25, 0.1, 0.2), (-0.15, 0.3, 0.15, -0.3, 0.32))):
        p = ease_out(rel(t, t0, t0 + 0.07), 3)
        ini = rel(t, t0 + 0.08, t0 + 0.25)
        if p > 0 and ini < 1:
            L = T.polys([(lamina(x1, y1, x2, y2, 0.045, prog=p, inicio=ini), 1.0)])
            G += L * 1.4
            H += L * 0.5
        G += _gotas(T, t, t0 + 0.05, 0.4, (x1 + x2) / 2, (y1 + y2) / 2, 7, 0.25, 71 + k, tam=0.014)
    g, h = _estouro(T, t, 0.34, 0.58, 0, 0, 0.25, 8, 73, 0.016)
    G += g * 0.8
    H += h * 0.7
    return G * env, H * env


# ================================================================== Sans
def _osso(x1, y1, x2, y2, r=0.035):
    ang = math.atan2(y2 - y1, x2 - x1)
    c, s = math.cos(ang), math.sin(ang)
    nx, ny = -s, c
    w = r * 0.45
    return [(x1 + nx * w, y1 + ny * w), (x2 + nx * w, y2 + ny * w), (x2 - nx * w, y2 - ny * w), (x1 - nx * w, y1 - ny * w)]


def ossos_de_sans(T, t, rng):
    """Os ossos do Sans: o olho esquerdo acende azul e amarelo, uma fileira de ossos brancos brota do chão debaixo do
    rival, e um osso azul atravessa por cima."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    olho = pulso(t, 0.0, 0.45)
    if olho > 0:
        ox, oy = -0.72, -0.3
        H += T.gauss(ox, oy, 0.035) * olho * 1.8
        G += T.ring(0.05, 0.012, ox, oy) * olho
        for k in range(5):
            a = t * 20 + k * 1.3
            G += T.splats([(ox + 0.04 * k * math.cos(a) * 0.2 - 0.03 * k, oy - 0.03 * k, (1 - k / 5) * olho)], 0.015)
    for k in range(6):
        bx = -0.32 + 0.13 * k
        t0 = 0.18 + 0.025 * k
        sobe = ease_out(rel(t, t0, t0 + 0.08), 3) * (1 - ease_in(rel(t, 0.55, 0.7), 2))
        if sobe > 0:
            alt = 0.38 + 0.08 * math.sin(k * 2.1)
            topo = 0.4 - alt * sobe
            O = T.polys([(_osso(bx, 0.4, bx, topo), 1.0)])
            pontas = T.splats([(bx - 0.02, topo, 1), (bx + 0.02, topo, 1)], 0.017)
            G += np.clip(O + pontas, 0, 1) * 0.9 + _borda(T, np.clip(O + pontas, 0, 1), 0.005) * 0.8
    G += T.lines([(-0.45, 0.42, 0.45, 0.42, 1.0)], 0.006) * pulso(t, 0.15, 0.7)
    azul = rel(t, 0.3, 0.55)
    if 0 < azul < 1:
        x = -0.9 + 1.8 * azul
        O = T.polys([(_osso(x - 0.1, -0.15, x + 0.1, -0.15), 1.0)])
        H += O * 1.1
        G += O * 0.4 + T.lines([(x - 0.4, -0.15, x - 0.1, -0.15, 1.0)], 0.01) * 0.4
    g, h = _estouro(T, t, 0.25, 0.5, 0, 0.0, 0.3, 8, 75)
    G += g * 0.8
    H += h * 0.6
    return G * env, H * env


# ================================================================== Cuphead
def dedo_de_ervilha(T, t, rng):
    """O tiro do Cuphead: a mão de luva aponta o dedo, as ervilhas azuis saem em rajada com o rastro de cartum e
    estouram no rival em "splats" com as gotinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    mao = pulso(t, 0.0, 0.62)
    dx, dy = -0.72, 0.0
    if mao > 0:
        luva = T.gauss(dx - 0.06, dy, 0.05) + T.lines([(dx - 0.04, dy, dx + 0.06, dy, 1.0)], 0.018)
        G += np.clip(luva, 0, 1) * mao * 1.1
        G += T.lines([(dx - 0.08, dy + 0.05, dx - 0.18, dy + 0.12, 1.0)], 0.02) * mao * 0.6
    for k in range(4):
        t0 = 0.12 + 0.07 * k
        u = rel(t, t0, t0 + 0.16)
        if 0 < u < 1:
            x = dx + 0.06 + (0 - dx) * u
            y = dy + 0.03 * math.sin(k * 2.3) * u
            H += T.gauss(x, y, 0.045) * 1.5
            G += T.ring(0.055, 0.014, x, y) + T.tapered([(x - 0.3, y, x - 0.05, y, 1.0)], 0.03) * 0.7
        if u >= 1 or t > t0 + 0.16:
            s = rel(t, t0 + 0.16, t0 + 0.34)
            if 0 < s < 1:
                pts = estrela(0.03 * math.sin(k * 3), 0.03 * math.cos(k * 2), 0.14 + 0.1 * s, k, 7, 0.5)
                G += T.polys([(pts, 1.0)]) * (1 - s) * 0.6
                G += _gotas(T, t, t0 + 0.16, 0.25, 0, 0, 6, 0.22, 77 + k, tam=0.013)
    H += T.flare(dx + 0.06, dy, 0.18, 0, 0.012) * (pulso(t, 0.1, 0.16) + pulso(t, 0.17, 0.23) + pulso(t, 0.24, 0.3) + pulso(t, 0.31, 0.37))
    return G * env, H * env


# ================================================================== Dovahkiin
def fus_ro_dah(T, t, rng):
    """O Fus Ro Dah do Dovahkiin: as três palavras do Thu'um saem em três ondas que crescem (os arcos de som com as
    runas de dragão riscadas dentro) e empurram o rival para trás."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    bx, by = -0.78, 0.0
    H += T.gauss(bx, by, 0.05) * pulso(t, 0.0, 0.5) * 1.2
    for k in range(3):
        t0 = 0.05 + 0.1 * k
        u = rel(t, t0, t0 + 0.4)
        if 0 < u < 1:
            r = 0.1 + 0.95 * ease_out(u, 1.8)
            forte = (1 - u) * (0.7 + 0.2 * k)
            A = T.arc_band(r, 0.035 + 0.02 * k, -0.55, 0.55, cx=bx, cy=by, crescente=True)
            G += (A * 1.3 + T.blur(A, 0.025) * 0.5) * forte
            H += A * forte * 0.5
            q = np.random.default_rng(79 + k)
            for j in range(3):
                a = -0.3 + 0.3 * j
                rx, ry = bx + r * math.cos(a), by + r * math.sin(a)
                s = 0.035
                traco = [(rx - s, ry - s, rx + s * q.uniform(-1, 1), ry, 1.0), (rx + s * q.uniform(-1, 1), ry, rx + s, ry + s, 1.0), (rx, ry - s, rx, ry + s, 0.7)]
                G += T.lines(traco, 0.007) * forte * 0.9
    empurra = rel(t, 0.3, 0.7)
    if 0 < empurra < 1:
        for k in range(6):
            y = -0.3 + 0.12 * k
            x0 = 0.05 + 0.3 * ease_out(empurra, 2)
            G += T.tapered([(x0 - 0.3, y, x0, y, 1.0)], 0.012) * (1 - empurra)
    g, h = _estouro(T, t, 0.3, 0.6, 0.05, 0, 0.35, 10, 83)
    G += g * 0.7
    H += h * 0.6
    return G * env, H * env


# ================================================================== O Cavaleiro
def golpe_de_ferrao(T, t, rng):
    """O ferrão do Cavaleiro: o pequeno vulto de chifres avança e dá o corte curto e preciso com o Ferrão (a meia-lua
    branca), o rival solta a essência branca e o Cavaleiro absorve um fio de Alma."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    anda = ease_out(rel(t, 0.0, 0.18), 2)
    if t < 0.42:
        some = 1 - rel(t, 0.32, 0.42)
        cx, cy = -0.7 + 0.35 * anda, 0.05
        cabeca = T.gauss(cx, cy - 0.05, 0.055, 0.06)
        chifres = T.polyline([(cx - 0.035, cy - 0.09), (cx - 0.06, cy - 0.18), (cx - 0.04, cy - 0.24)], 0.012) + T.polyline([(cx + 0.035, cy - 0.09), (cx + 0.06, cy - 0.18), (cx + 0.04, cy - 0.24)], 0.012)
        olhos = T.splats([(cx - 0.02, cy - 0.05, 1), (cx + 0.02, cy - 0.05, 1)], 0.012)
        G += np.clip(cabeca * 1.2 + chifres - olhos * 1.4, 0, 1) * some
        manto = T.polys([([(cx - 0.06, cy + 0.0), (cx + 0.06, cy + 0.0), (cx + 0.08, cy + 0.15), (cx - 0.08, cy + 0.15)], 1.0)])
        G += _borda(T, manto, 0.006) * some * 0.8
    corte = ease_out(rel(t, 0.18, 0.3), 3)
    ini = rel(t, 0.3, 0.48)
    if corte > 0 and ini < 1:
        a1 = -1.6 + 2.6 * corte
        A = T.arc_band(0.32, 0.07, a1 - 2.0 * corte, a1, cx=-0.1, cy=0.0, crescente=True)
        G += (A * 1.5 + T.blur(A, 0.02) * 0.5) * (1 - ini)
        H += A * 0.7 * (1 - ini)
    G += _gotas(T, t, 0.28, 0.45, 0.05, 0, 10, 0.35, 85, tam=0.018, cai=0.15)
    alma = rel(t, 0.35, 0.8)
    if 0 < alma < 1:
        pts = [(0.05 + (-0.4 - 0.05) * min(1, alma * 1.3 - u * 0.3), -0.2 * math.sin(math.pi * u) * (1 - alma), (1 - u) * (1 - alma)) for u in np.linspace(0, 1, 12)]
        H += T.splats(pts, 0.016) * 1.2
    g, h = _estouro(T, t, 0.28, 0.52, 0.05, 0, 0.25, 8, 87, 0.016)
    G += g * 0.7
    H += h * 0.6
    return G * env, H * env


# ================================================================== Goro
def quatro_punhos(T, t, rng):
    """Os quatro braços do Goro: os quatro punhos enormes socam em sequência, dois de cima e dois de baixo, com os
    estouros um atrás do outro."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ordem = ((-0.18, 0.08), (0.14, 0.12), (-0.14, 0.17), (0.16, 0.22))
    for k, (y, t0) in enumerate(ordem):
        vai = ease_in(rel(t, t0 - 0.08, t0), 2)
        volta = rel(t, t0 + 0.05, t0 + 0.15)
        if vai > 0 and volta < 1:
            x = -0.85 + 0.78 * vai - 0.3 * volta
            P, nos = _punho(T, x, y, 1.6)
            G += (P * 0.5 + _borda(T, P, 0.007) * 1.4) * (1 - volta)
            H += nos * (1 - volta) * 0.8
            G += T.tapered([(x - 0.5, y, x - 0.15, y, 1.0)], 0.02) * (1 - volta) * 0.5 * vai
        g, h = _estouro(T, t, t0, t0 + 0.2, 0.0, y, 0.22, 7, 89 + k, 0.018)
        G += g * 0.8
        H += h * 0.7
    return G * env, H * env


# ================================================================== Yoshi
def lingua_de_yoshi(T, t, rng):
    """A língua do Yoshi: a língua comprida dispara (a faixa grossa com a ponta redonda), estala no rival e volta
    puxando; no fim um ovo pintado de bolinhas sai quicando e quebra."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    bx, by = -0.75, -0.05
    vai = ease_out(rel(t, 0.05, 0.2), 2.5)
    volta = ease_in(rel(t, 0.3, 0.42), 2)
    est = vai * (1 - volta)
    if est > 0.01:
        x = bx + (0.0 - bx) * est
        pts = [(bx + (x - bx) * u, by + 0.04 * math.sin(u * math.pi) * (1 - est)) for u in np.linspace(0, 1, 14)]
        L = T.polyline(pts, 0.05)
        ponta = T.gauss(x, by, 0.065)
        F = np.clip(L + ponta, 0, 1)
        G += F * 0.7 + _borda(T, F, 0.007) * 1.3
        H += T.polyline(pts, 0.008) * 0.4
    g, h = _estouro(T, t, 0.2, 0.45, 0.02, by, 0.3, 9, 91)
    G += g
    H += h
    ovo = rel(t, 0.42, 0.8)
    if 0 < ovo < 1:
        x = -0.6 + 0.6 * ovo
        y = by - 0.35 * math.sin(math.pi * min(1, ovo * 1.2)) + 0.05
        ang = ovo * 8
        quebra = rel(t, 0.74, 0.8)
        if quebra <= 0:
            O = T.gauss(x, y, 0.08, 0.1)
            bol = T.splats([(x + 0.05 * math.cos(ang + k * 2.1), y + 0.06 * math.sin(ang + k * 2.1), 1.0) for k in range(3)], 0.02)
            G += np.clip(O * 1.3, 0, 1) * 0.6 + _borda(T, np.clip(O * 1.3, 0, 1), 0.008) * 1.2
            H += bol * 1.2
    G += _blocos(T, t, 0.78, 0.25, 0.0, -0.05, 9, 0.32, 93, 0.035, 0.2)
    G += _estrelinhas(T, t, 0.78, 0.22, 0.0, -0.05, 5, 0.25, 95)
    return G * env, H * env


REGISTRO = [
    ("pistola_de_megamente", pistola_de_megamente, GRANDE, "Básico do Megamente: a pistola desidratadora e o cubo", False),
    ("soco_de_vilgax", soco_de_vilgax, GRANDE, "Básico do Vilgax: o punho e os tentáculos", False),
    ("puf_das_varinhas", puf_das_varinhas, GRANDE, "Básico de Cosmo e Wanda: as varinhas e o puf", False),
    ("espada_de_diamante", espada_de_diamante, GRANDE, "Básico do Steve: a espada de diamante em pixels", False),
    ("ssss_do_creeper", ssss_do_creeper, GRANDE, "Básico do Creeper: pisca e explode em blocos", False),
    ("chomp_do_pacman", chomp_do_pacman, GRANDE, "Básico do Pac-Man: as pastilhas e a mordida", False),
    ("giro_do_crash", giro_do_crash, GRANDE, "Básico do Crash: o tornado e as frutas Wumpa", False),
    ("dead_eye", dead_eye, GRANDE, "Básico do Arthur Morgan: os X do Dead Eye", False),
    ("canivete_de_ellie", canivete_de_ellie, GRANDE, "Básico da Ellie: o canivete", False),
    ("ossos_de_sans", ossos_de_sans, GRANDE, "Básico do Sans: o olho azul e os ossos", False),
    ("dedo_de_ervilha", dedo_de_ervilha, GRANDE, "Básico do Cuphead: as ervilhas do dedo", False),
    ("fus_ro_dah", fus_ro_dah, GRANDE, "Básico do Dovahkiin: as três palavras do Thu'um", False),
    ("golpe_de_ferrao", golpe_de_ferrao, GRANDE, "Básico do Cavaleiro: o Ferrão e a Alma", False),
    ("quatro_punhos", quatro_punhos, GRANDE, "Básico do Goro: os quatro punhos", False),
    ("lingua_de_yoshi", lingua_de_yoshi, GRANDE, "Básico do Yoshi: a língua e o ovo", False),
]
