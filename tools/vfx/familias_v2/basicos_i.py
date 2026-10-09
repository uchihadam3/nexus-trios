"""Ataques básicos com animação própria, lote i.

Cada folha conta o golpe do personagem: os dois sais do Raphael estocando, os
nunchakus do Michelangelo girando e batendo duas vezes, a bicada-britadeira do
Pica-Pau (e do Patolino), o clarão da ampulheta do Omnitrix antes do golpe do
alien, a manivela do Popeye com a âncora estampada, o machado de energon do
Optimus, o caratê do Bob Esponja com bolhas, o laço do Woody, o fogo azul da
Azula, a bigorna ACME do Coiote (com a sombra crescendo antes), a frigideira do
Tom, o Cajado da Caveira do Esqueleto e a Espada de Augúrio do Lion-O.
"""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, apaga, back, contorno, ease_in, ease_out, estrela, faiscas, forma, girado,  # noqa: F401
                   jagged, janela, lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


# ------------------------------------------------------------------ peças comuns
def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.26, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.4
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.6 * k + 0.01, ang=ang + math.pi / 2, thin=0.012)) * k * 1.5
    return g, h


def _barra(x1, y1, x2, y2, w1, w2=None):
    """Barra reta (cabo, braço, bastão) de largura w1 numa ponta e w2 na outra."""
    w2 = w1 if w2 is None else w2
    dx, dy = x2 - x1, y2 - y1
    c = math.hypot(dx, dy) or 1
    nx, ny = -dy / c, dx / c
    return [(x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2),
            (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2)]


def _elipse(cx, cy, rx, ry, rot=0.0, n=40, a0=0.0, a1=TAU):
    pts = [(rx * math.cos(a0 + (a1 - a0) * k / n), ry * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
    return _gira(pts, rot, cx, cy)


def _chama(cx, base, alt, larg, fase, ondula=0.25):
    """Língua de fogo que sobe (gota que afina para cima, com a ponta balançando)."""
    pts = []
    for lado in (1, -1):
        ks = range(13) if lado == 1 else range(12, -1, -1)
        for k in ks:
            u = k / 12
            y = base - alt * u
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, y))
    return pts


def _estrelinhas(T, t, a, b, cx, cy, raio, n=3, tam=0.075, vel=9.0):
    """Estrelinhas de desenho girando em volta (o tonto)."""
    k = janela(t, a, a + 0.06) * apaga(t, b - 0.12, b)
    if k <= 0:
        return T.zero()
    formas = []
    for j in range(n):
        ang = j / n * TAU + t * vel
        x, y = cx + raio * math.cos(ang), cy + raio * 0.38 * math.sin(ang)
        formas.append((estrela(x, y, tam * (0.85 + 0.2 * math.sin(ang)), -math.pi / 2 + t * 5, 5, 0.45), 1.0))
    return T.polys(formas, 0.004) * k


def _linhas_de_impacto(T, cx, cy, r0, r1, n, ang0=0.0, larg=0.022):
    """Tracinhos de impacto de quadrinho em volta de um ponto (grossos por fora)."""
    segs = []
    for j in range(n):
        a = ang0 + j / n * TAU
        segs.append((cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r1, cy + math.sin(a) * r1, 1.0))
    return T.tapered(segs, larg)


def _luz(T, G, H, S, g=1.2, halo=0.8, h=0.7, sigma=0.03, k=1.0):
    """Soma uma forma como luz: corpo + halo na cor, núcleo branco por cima."""
    if k <= 0:
        return
    G += (S * g + T.blur(S, sigma) * halo) * k
    H += S * h * k


# ------------------------------------------------------------------ Raphael: Sais
def _sai(tx, ty, ang, esc=1.0):
    """Sai com a ponta em (tx, ty) apontando para `ang`: (polígonos, as duas pontas laterais)."""
    lam = [(-0.52, -0.036), (-0.14, -0.03), (0.0, 0.0), (-0.14, 0.03), (-0.52, 0.036)]
    cabo = _barra(-0.52, 0, -0.84, 0, 0.075)
    pomo = _elipse(-0.87, 0, 0.04, 0.045, n=16)
    pontas = [[(-0.5, 0.0), (-0.55, 0.075 * s), (-0.5, 0.16 * s), (-0.39, 0.185 * s), (-0.29, 0.15 * s)] for s in (-1, 1)]

    def tf(pts):
        return _gira([(x * esc, y * esc) for x, y in pts], ang, tx, ty)
    return [tf(lam), tf(cabo), tf(pomo)], [tf(p) for p in pontas]


def sais(T, t, rng):
    """Sais do Raphael: um sai entra estocando por cima, o outro por baixo, um logo depois do
    outro; cada estocada fura com um clarão de três pontas (o garfo) e faíscas de metal."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    golpes = [((0.12, -0.14), 0.32, 0.0, 11, 0.5), ((0.1, 0.15), -0.3, 0.3, 23, 0.64)]
    for (ax, ay), ang, s0, seed, solta in golpes:
        if t < s0:
            continue
        dx, dy = math.cos(ang), math.sin(ang)
        p = ease_out(rel(t, s0, s0 + 0.12), 2.6)
        volta = ease_in(rel(t, solta, solta + 0.16), 1.5)
        rec = 0.9 * (1 - p) + 0.35 * volta
        tx, ty = ax - dx * rec, ay - dy * rec
        vis = janela(t, s0, s0 + 0.02) * (1 - rel(t, solta, solta + 0.14))
        if vis > 0.01:
            polys, pontas = _sai(tx, ty, ang, 1.05)
            S = T.polys([(q, 1.0) for q in polys], 0.004) + sum(T.polyline(q, 0.042) for q in pontas)
            _luz(T, G, H, S, 1.3, 0.9, 0.85, 0.03, vis * env)
        rk = pulso(t, s0, s0 + 0.22)
        if rk > 0:
            R = rastro_de_velocidade(T, rng, 7, ang, 0.55, 0.24, 0.55, tx, ty, 0.016, seed=seed)
            G += R * rk * 1.1 * env
            H += R * rk * 0.4 * env
        k = pulso(t, s0 + 0.1, s0 + 0.36)
        if k > 0:
            g, h = _clarao(T, k, ax, ay, 0.15, 0.6, ang)
            cresce = ease_out(rel(t, s0 + 0.1, s0 + 0.3), 2)
            garfo = T.polys([(lamina(ax, ay, ax + math.cos(ang + o) * (0.16 + 0.3 * cresce), ay + math.sin(ang + o) * (0.16 + 0.3 * cresce), 0.045), 1.0)
                             for o in (-0.55, 0.0, 0.55)], 0.006) * k
            anel = T.ring(0.05 + 0.24 * cresce, 0.022, ax, ay) * k
            sub = np.random.default_rng(seed + 100)
            F = faiscas(T, sub, t, 9, 0.5, 0.022, cone=(ang - 1.3, ang + 1.3), gravidade=0.25, cx=ax, cy=ay, inicio=s0 + 0.1) * (1 - rel(t, s0 + 0.4, s0 + 0.6))
            G += (g + garfo * 1.3 + anel * 0.9 + F * 1.4) * env
            H += (h + garfo * 0.9 + anel * 0.4 + F) * env
    return G, H


# ------------------------------------------------------------------ Michelangelo: Nunchakus
def nunchakus(T, t, rng):
    """Nunchakus do Michelangelo: o bastão gira preso pela corrente (com o rastro do giro),
    bate no alvo, volta girando mais uma vez e bate de novo, um pouco mais abaixo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    px = -0.52
    if t < 0.36:
        th = -3.4 * math.pi * (1 - rel(t, 0.0, 0.36))
        py = -0.1
    elif t < 0.62:
        u = rel(t, 0.36, 0.62)
        th = TAU * ease_in(u, 1.3)
        py = -0.1 + 0.24 * (u * u * (3 - 2 * u))
    else:
        u = rel(t, 0.62, 1.0)
        th = TAU + 1.1 * ease_out(u, 2.2)
        py = 0.14
    r0, r1, larg = 0.19, 0.64, 0.085
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.74, 0.92))
    # rastro do giro: vultos do bastão logo atrás e o risco da ponta
    gira = 1 - rel(t, 0.64, 0.74)
    vultos = [(_barra(px + math.cos(th - j * 0.17) * r0, py + math.sin(th - j * 0.17) * r0,
                      px + math.cos(th - j * 0.17) * r1, py + math.sin(th - j * 0.17) * r1, larg * 0.9), 0.55 * (1 - j / 7))
              for j in range(1, 7)]
    V = T.polys(vultos, 0.012) * gira
    risco = T.arc_band(r1 - 0.03, 0.05, th - 1.9, th, cx=px, cy=py) * gira
    bast = T.polys([(_barra(px + math.cos(th) * r0, py + math.sin(th) * r0, px + math.cos(th) * r1, py + math.sin(th) * r1, larg), 1.0)], 0.004)
    # o bastão da mão e a corrente
    thm = math.pi * 0.78 + 0.25 * math.sin(th)
    mao = T.polys([(_barra(px + math.cos(thm) * 0.03, py + math.sin(thm) * 0.03, px + math.cos(thm) * 0.45, py + math.sin(thm) * 0.45, larg), 1.0)], 0.004)
    elos = T.splats([(px + math.cos(th) * r0 * f, py + math.sin(th) * r0 * f, 1.0) for f in (0.15, 0.45, 0.75)], 0.014)
    S = bast + mao * 0.85
    G += (S * 1.3 + T.blur(S, 0.03) * 0.7 + V * 0.9 + risco * 1.1 + elos * 1.2) * vis * env
    H += (S * 0.75 + V * 0.25 + risco * 0.6 + elos * 0.8) * vis * env
    # as duas pancadas
    for hit, (cx, cy), ang0 in ((0.36, (0.12, -0.1), 0.2), (0.62, (0.12, 0.14), 0.0)):
        k = pulso(t, hit - 0.06, hit + 0.24)
        if k <= 0:
            continue
        g, h = _clarao(T, k, cx, cy, 0.17, 0.6, 0.4)
        est = T.polys([(estrela(cx, cy, 0.3 * k + 0.01, ang0, 8, 0.42), 1.0)], 0.006) * k
        tr = _linhas_de_impacto(T, cx, cy, 0.2 + 0.12 * rel(t, hit, hit + 0.2), 0.36 + 0.12 * rel(t, hit, hit + 0.2), 7, ang0 + 0.2, 0.05) * k
        G += (g + est * 1.3 + tr * 1.1) * env
        H += (h + est * 0.9 + tr * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Pica-Pau / Patolino: Bicada
def _bico(tx, ty, ang=0.0):
    sup = [(0.0, -0.004), (-0.82, -0.2), (-0.9, -0.012)]
    inf = [(-0.03, 0.014), (-0.8, 0.15), (-0.9, 0.024)]
    return _gira(sup, ang, tx, ty), _gira(inf, ang, tx, ty)


def bicada(T, t, rng):
    """Bicada: o bico bate e volta como uma britadeira (um quadro dentro, outro fora, com o
    vulto da outra posição), cada bicada estala no alvo, o buraco racha e as lascas de
    madeira voam para trás."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    ativo = 1 - rel(t, 0.68, 0.84)
    dentro = 0.5 - 0.5 * math.cos(math.pi * t * 11) if t < 0.68 else 0.0

    def pos(e):
        return -0.02 - 0.24 * (1 - e), 0.015 * math.sin(t * 61)
    tx, ty = pos(dentro)
    ox, oy = pos(1 - dentro)
    b1, b2 = _bico(tx, ty)
    v1, v2 = _bico(ox, oy)
    B = T.polys([(b1, 1.0), (b2, 1.0)], 0.004)
    V = T.polys([(v1, 1.0), (v2, 1.0)], 0.01)
    # tremido: tracinhos em cima e embaixo do bico
    tremido = T.lines([(-0.42 + 0.06 * j, -0.27 - 0.02 * j, -0.38 + 0.06 * j, -0.21 - 0.02 * j, 1.0) for j in range(3)]
                      + [(-0.42 + 0.06 * j, 0.24 + 0.02 * j, -0.38 + 0.06 * j, 0.18 + 0.02 * j, 1.0) for j in range(3)], 0.018) * (t < 0.68)
    G += (B * 1.3 + T.blur(B, 0.03) * 0.7 + V * 0.45 + tremido * 0.8) * ativo * env
    H += (B * 0.75 + V * 0.12 + tremido * 0.4) * ativo * env
    # o estalo de cada bicada
    k = dentro * ativo
    if k > 0:
        g, h = _clarao(T, k, 0.02, 0.0, 0.12, 0.45, 0.6)
        est = T.polys([(estrela(0.03, 0.0, 0.2, 0.3 + t * 7, 6, 0.42), 1.0)], 0.006) * k
        G += (g + est * 1.1) * env
        H += (h + est * 0.8) * env
    # o buraco que vai rachando
    prog = rel(t, 0.06, 0.66)
    if prog > 0:
        sub = np.random.default_rng(301)
        rachas = T.zero()
        for j in range(7):
            a = j / 7 * TAU + sub.uniform(-0.3, 0.3)
            pts = jagged(sub, 0.02, 0.0, 0.02 + math.cos(a) * 0.42, math.sin(a) * 0.42, 4, 0.3)
            n = max(2, int(len(pts) * prog))
            rachas += T.polyline(pts[:n], 0.016)
        buraco = T.ring(0.05 + 0.06 * prog, 0.022, 0.02, 0.0) * janela(t, 0.06, 0.12)
        fim = 1 - rel(t, 0.75, 0.98)
        G += (rachas * 0.9 + buraco * 1.2) * fim * env
        H += (rachas * 0.35 + buraco * 0.6) * fim * env
    # lascas de madeira
    lascas = []
    sub = np.random.default_rng(77)
    for j in range(4):
        nasce = (2 * j + 1) / 11
        for _ in range(4):
            a = sub.uniform(math.pi * 0.62, math.pi * 1.38)
            sp = sub.uniform(1.0, 1.7)
            giro = sub.uniform(-14, 14)
            comp = sub.uniform(0.07, 0.11)
            dt = t - nasce
            if dt <= 0 or dt > 0.42:
                continue
            x = 0.02 + math.cos(a) * sp * dt
            y = math.sin(a) * sp * dt + 2.2 * dt * dt
            peca = [(-comp, -0.012), (-comp * 0.3, -0.024), (comp, -0.006), (comp * 0.3, 0.022)]
            lascas.append((_gira(peca, a + giro * dt, x, y), (1 - dt / 0.42) ** 0.8))
    if lascas:
        L = T.polys(lascas, 0.004)
        G += (L * 1.3 + T.blur(L, 0.02) * 0.6) * env
        H += L * 0.5 * env
    return G, H


# ------------------------------------------------------------------ Ben 10: Golpe alienígena
def _ampulheta(cx, cy, r):
    return [(cx - 0.6 * r, cy - 0.8 * r), (cx + 0.6 * r, cy - 0.8 * r), (cx + 0.11 * r, cy), (cx + 0.6 * r, cy + 0.8 * r),
            (cx - 0.6 * r, cy + 0.8 * r), (cx - 0.11 * r, cy)]


def _punho(fx, fy, ang=0.0, esc=1.0):
    """Punho fechado com a frente em (fx, fy) apontando para `ang`."""
    p = [(0.0, -0.1), (-0.03, -0.15), (-0.27, -0.15), (-0.31, -0.1), (-0.31, 0.11), (-0.26, 0.15), (-0.03, 0.15), (0.0, 0.11)]
    return _gira([(x * esc, y * esc) for x, y in p], ang, fx, fy)


def golpe_alienigena(T, t, rng):
    """Golpe alienígena: a ampulheta do Omnitrix aparece no mostrador, carrega com raios
    girando, estoura no clarão verde da transformação e o punho do alien entra com tudo
    (estrela de impacto com a ampulheta estampada no meio)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pop = back(rel(t, 0.0, 0.16), 2.0)
    vis = janela(t, 0.0, 0.03) * (1 - rel(t, 0.36, 0.46))
    if vis > 0 and pop > 0.02:
        r = 0.42 * pop
        mostrador = T.ring(r, 0.032) + T.ring(r * 0.8, 0.012) * 0.6
        amp = T.polys([(_ampulheta(0, 0, r * 0.78), 1.0)], 0.005)
        carga = janela(t, 0.12, 0.34)
        segs = []
        for j in range(10):
            a = j / 10 * TAU + t * 9
            segs.append((math.cos(a) * r * 1.05, math.sin(a) * r * 1.05, math.cos(a) * r * (1.25 + 0.4 * carga), math.sin(a) * r * (1.25 + 0.4 * carga), 1.0))
        raios = T.lines(segs, 0.024, 0.006)
        G += (mostrador * 1.2 + amp * (1.0 + 0.6 * carga) + T.blur(amp, 0.04) * 0.8 + raios * carga * 0.9) * vis * env
        H += (mostrador * 0.6 + amp * (0.35 + 0.9 * carga) + raios * carga * 0.5) * vis * env
    # o clarão da transformação
    k = pulso(t, 0.3, 0.5)
    if k > 0:
        g, h = _clarao(T, k, 0, 0, 0.36, 1.0, 0.0)
        onda = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.32, 0.52), 2), 0.05) * k
        G += (g * 1.3 + onda) * env
        H += (h + T.gauss(0, 0, 0.2, 0.2) * k * 1.4 + onda * 0.5) * env
    # o punho do alien
    if 0.38 <= t < 0.64:
        u = ease_in(rel(t, 0.38, 0.47), 1.6)
        fx = -1.1 + 1.08 * u
        pv = 1 - rel(t, 0.52, 0.64)
        P = T.polys([(_punho(fx, 0.0, 0.0, 1.25), 1.0), (_barra(fx - 0.38, 0.0, fx - 1.2, 0.0, 0.26, 0.22), 0.8)], 0.005)
        dedos = T.lines([(fx - 0.06, -0.18 + 0.09 * j, fx - 0.06 - 0.12, -0.18 + 0.09 * j, 1.0) for j in (1, 2, 3)], 0.016)
        banda = T.polys([(_barra(fx - 0.43, -0.16, fx - 0.43, 0.16, 0.08), 1.0)], 0.004)
        sinal = T.polys([(_ampulheta(fx - 0.43, 0.0, 0.07), 1.0)], 0.003)
        R = rastro_de_velocidade(T, rng, 8, 0.0, 0.7, 0.3, 0.45, fx, 0.0, 0.016, seed=5) * (1 - rel(t, 0.47, 0.56))
        G += (P * 1.2 + T.blur(P, 0.03) * 0.6 + banda * 0.6 + R) * pv * env
        H += (P * 0.4 + dedos * 0.7 + sinal * 1.2 + R * 0.4) * pv * env
    k = pulso(t, 0.45, 0.8)
    if k > 0:
        g, h = _clarao(T, k, 0.04, 0, 0.26, 0.85, 0.35)
        est = T.polys([(estrela(0.04, 0, 0.42 * k + 0.01, 0.2, 8, 0.4), 1.0)], 0.006) * k
        marca = T.polys([(_ampulheta(0.04, 0, 0.17 * k + 0.01), 1.0)], 0.004) * k
        anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.46, 0.8), 2.2), 0.04) * k
        sub = np.random.default_rng(42)
        F = faiscas(T, sub, t, 12, 0.75, 0.024, cone=(-math.pi, math.pi), gravidade=0.2, cx=0.04, inicio=0.46)
        G += (g + est * 1.2 + anel + F * 1.3) * env
        H += (h + est * 0.5 + marca * 1.5 + anel * 0.4 + F * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Popeye: Soco de marinheiro
def _ancora(cx, cy, s):
    """Âncora em traços: haste, cepo, braços em U, as unhas e a argola (cx, cy, raio)."""
    linhas = [[(0, -0.34), (0, 0.42)], [(-0.24, -0.2), (0.24, -0.2)]]
    arco = [(0.34 * math.cos(a), 0.08 + 0.34 * math.sin(a)) for a in np.linspace(0.12 * math.pi, 0.88 * math.pi, 20)]
    linhas.append(arco)
    unhas = []
    for lado in (1, -1):
        ex, ey = arco[0] if lado == 1 else arco[-1]
        unhas.append([(ex + lado * 0.1, ey - 0.15), (ex - lado * 0.07, ey + 0.0), (ex + lado * 0.09, ey + 0.05)])

    def tf(pts):
        return [(cx + x * s, cy + y * s) for x, y in pts]
    return [tf(lin) for lin in linhas], [tf(u) for u in unhas], (cx, cy - 0.43 * s, 0.085 * s)


def soco_de_marinheiro(T, t, rng):
    """Soco de marinheiro: o braço do Popeye gira como manivela (cada vez mais rápido), o
    soco sai esticado, explode numa estrela com estrelinhas voando e uma âncora estampada."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sx, sy, R = -0.6, 0.06, 0.3
    if t < 0.42:
        u = rel(t, 0.0, 0.42)
        phi = -1.75 * TAU + 1.75 * TAU * ease_in(u, 1.4)
        fx, fy = sx + R * math.cos(phi), sy + R * math.sin(phi)
        manivela = 1.0
    else:
        u = ease_out(rel(t, 0.42, 0.5), 2.2)
        fx, fy = sx + R + (0.02 - sx - R) * u, sy + (0.0 - sy) * u
        manivela = 1 - rel(t, 0.42, 0.5)
        phi = 0.0
    vis = janela(t, 0.0, 0.03) * (1 - rel(t, 0.58, 0.7))
    braco = T.polys([(_barra(sx, sy, fx, fy, 0.08, 0.2), 1.0)], 0.005)
    punho = T.polys([(_elipse(fx, fy, 0.12, 0.11, n=20), 1.0)], 0.004)
    S = braco * 0.9 + punho
    G += (S * 1.2 + T.blur(S, 0.03) * 0.7) * vis * env
    H += (punho * 0.8 + braco * 0.35) * vis * env
    if manivela > 0:
        giro = T.ring(R, 0.02, sx, sy) * 0.5 + T.arc_band(R, 0.08, phi - 2.2, phi, cx=sx, cy=sy) * 1.1
        G += giro * manivela * vis * env
        H += giro * 0.4 * manivela * vis * env
    if 0.42 <= t < 0.56:
        Rv = rastro_de_velocidade(T, rng, 7, 0.0, 0.6, 0.25, 0.25, fx, fy, 0.016, seed=17) * pulso(t, 0.42, 0.56)
        G += Rv * env
        H += Rv * 0.4 * env
    # pancada
    k = pulso(t, 0.48, 0.76)
    if k > 0:
        g, h = _clarao(T, k, 0.04, 0, 0.26, 0.8)
        est = T.polys([(estrela(0.04, 0, 0.44 * k + 0.01, 0.15, 10, 0.5), 1.0)], 0.006) * k
        anel = T.ring(0.15 + 0.55 * ease_out(rel(t, 0.49, 0.8), 2), 0.035) * k
        G += (g + est * 1.0 + anel) * env
        H += (h + est * 0.5 + anel * 0.4) * env
    # âncora estampada
    a = back(rel(t, 0.5, 0.62), 2.2)
    av = 1 - rel(t, 0.8, 0.96)
    if a > 0.02 and av > 0:
        linhas, unhas, (rcx, rcy, rr) = _ancora(0.04, 0.02, 0.62 * a)
        A = sum(T.polyline(lin, 0.075 * a) for lin in linhas) + T.polys([(u, 1.0) for u in unhas], 0.004) + T.ring(rr, 0.03 * a, rcx, rcy) * 1.2
        G += (A * 1.3 + T.blur(A, 0.03) * 0.8) * av * env
        H += A * 0.9 * av * env
    # estrelinhas voando
    sub = np.random.default_rng(8)
    voo = rel(t, 0.5, 0.95)
    if voo > 0:
        formas = []
        for j in range(5):
            ang = -math.pi / 2 + (j - 2) * 0.62 + sub.uniform(-0.15, 0.15)
            d = 0.25 + 0.5 * ease_out(voo, 2) * sub.uniform(0.8, 1.1)
            x, y = 0.04 + math.cos(ang) * d, math.sin(ang) * d + 0.35 * voo * voo
            formas.append((estrela(x, y, 0.075, -math.pi / 2 + voo * 6 * (1 if j % 2 else -1), 5, 0.45), (1 - voo) ** 0.7))
        E = T.polys(formas, 0.004)
        G += (E * 1.3 + T.blur(E, 0.02) * 0.5) * env
        H += E * 0.8 * env
    return G, H


# ------------------------------------------------------------------ Optimus: Machado de energon
def _machado(px, py, phi, L):
    """Cabo e lâmina do machado; a lâmina fica do lado para onde o golpe anda."""
    dx, dy = math.cos(phi), math.sin(phi)
    nx, ny = -dy, dx

    def tf(u, w):
        return (px + u * dx + w * nx, py + u * dy + w * ny)
    cabo = [tf(-0.12, -0.03), tf(L + 0.06, -0.03), tf(L + 0.06, 0.03), tf(-0.12, 0.03)]
    fio = [tf(L - 0.06 + 0.3 * s, 0.3 + 0.12 * (1 - s * s)) for s in np.linspace(-1, 1, 11)]
    lam = [tf(L - 0.19, 0.03)] + fio + [tf(L + 0.06, 0.03)]
    contra = [tf(L - 0.1, -0.03), tf(L - 0.16, -0.12), tf(L + 0.0, -0.1), tf(L + 0.02, -0.03)]
    return cabo, lam, contra, fio


def machado_de_energon(T, t, rng):
    """Machado de energon do Optimus: o machado de energia sobe por trás e desce num arco
    pesado (rastro largo), crava no alvo com um talho grosso, onda de choque achatada e
    faíscas de energon espirrando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    px, py, L = -0.68, 0.32, 0.72
    u = ease_in(rel(t, 0.04, 0.32), 1.8)
    phi = -2.05 + (2.05 - 0.9) * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.62, 0.8))
    cabo, lam, contra, fio = _machado(px, py, phi, L)
    Cb = T.polys([(cabo, 1.0)], 0.004)
    Lm = T.polys([(lam, 1.0), (contra, 0.8)], 0.005)
    F = T.polyline(fio, 0.03)
    G += (Cb * 0.9 + Lm * 1.3 + T.blur(Lm, 0.05) * 1.1 + F * 0.6) * vis * env
    H += (Cb * 0.3 + Lm * 0.55 + F * 1.2) * vis * env
    corre = pulso(t, 0.04, 0.42)
    if corre > 0:
        ra = math.hypot(L - 0.06, 0.3)
        da = math.atan2(0.3, L - 0.06)
        arco = T.arc_band(ra, 0.13, phi + da - 1.3, phi + da, cx=px, cy=py)
        G += arco * corre * 1.3 * env
        H += T.arc_band(ra + 0.04, 0.03, phi + da - 1.0, phi + da, cx=px, cy=py) * corre * 0.9 * env
    k = pulso(t, 0.29, 0.66)
    if k > 0:
        nx, ny = -math.sin(-0.9), math.cos(-0.9)
        cresce = ease_out(rel(t, 0.29, 0.4), 2)
        talho = T.polys([(lamina(-nx * 0.5, -ny * 0.5, nx * 0.55, ny * 0.55, 0.075, cresce, 0.0), 1.0)], 0.006)
        g, h = _clarao(T, k * 0.7, 0.0, 0.02, 0.3, 0.9, -0.9)
        onda = T.ring(0.15 + 0.62 * ease_out(rel(t, 0.3, 0.7), 2.2), 0.05, 0, 0.12, squash=2.4) * k
        sub = np.random.default_rng(64)
        Fa = faiscas(T, sub, t, 16, 0.85, 0.026, cone=(-math.pi * 0.95, -0.05), gravidade=0.7, cx=0.0, cy=0.0, inicio=0.3)
        tk = 1 - rel(t, 0.55, 0.85)
        G += (talho * 1.4 * tk + T.blur(talho, 0.04) * tk + g * 1.1 + onda + Fa * 1.4) * env
        H += (talho * 1.1 * tk + h + onda * 0.4 + Fa) * env
    return G, H


# ------------------------------------------------------------------ Bob Esponja: Karatê
def _mao_de_faca(hx, hy, ang=0.0, esc=1.0):
    """Mão em faca (dedos juntos para +x, o fio da mão embaixo) com o polegar dobrado."""
    mao = [(-0.22, -0.07), (0.14, -0.075), (0.21, -0.055), (0.24, -0.015), (0.22, 0.03), (0.15, 0.06), (-0.22, 0.065)]
    polegar = [(-0.16, -0.06), (-0.1, -0.13), (0.0, -0.12), (0.03, -0.07)]
    mao = [(x * esc, y * esc) for x, y in mao]
    polegar = [(x * esc, y * esc) for x, y in polegar]
    return _gira(mao, ang, hx, hy), _gira(polegar, ang, hx, hy)


def karate(T, t, rng):
    """Karatê do Bob Esponja: a mão em faca desce num golpe seco, risca o alvo com o
    "tchop" e o impacto solta bolhas que sobem e estouram uma a uma."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    desce = ease_in(rel(t, 0.04, 0.28), 2.0)
    segue = ease_out(rel(t, 0.28, 0.38), 2)
    hx, hy = -0.08, -0.85 + 0.77 * desce + 0.06 * segue
    ang = 0.12 - 0.12 * desce
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    E = 1.7
    hy -= 0.045
    mao, pol = _mao_de_faca(hx, hy, ang, E)
    ombro = (-1.05, -0.35)
    pulsox, pulsoy = _gira([(-0.21 * E, 0.0)], ang, hx, hy)[0]
    braco = T.polys([(_barra(ombro[0], ombro[1], pulsox, pulsoy, 0.06, 0.07), 1.0)], 0.004)
    M = T.polys([(mao, 1.0), (pol, 0.85)], 0.004)
    dedos = T.lines([(hx - 0.06, hy - 0.045 + 0.05 * j, hx + 0.3, hy - 0.045 + 0.05 * j, 1.0) for j in (0, 1)], 0.012)
    G += (M * 1.3 + T.blur(M, 0.03) * 0.7 + braco * 0.8) * vis * env
    H += (M * 0.65 + braco * 0.3 + dedos * 0.25) * vis * env
    rk = pulso(t, 0.04, 0.36)
    if rk > 0:
        segs = [(hx + x, hy - 0.6, hx + x, hy - 0.14, 0.6 + 0.4 * math.cos(x * 4)) for x in np.linspace(-0.3, 0.32, 7)]
        Rv = T.tapered(segs, 0.025)
        G += Rv * rk * 0.9 * env
        H += Rv * rk * 0.3 * env
    k = pulso(t, 0.26, 0.56)
    if k > 0:
        g, h = _clarao(T, k, 0.0, 0.0, 0.22, 0.75, 0.0)
        risco = T.polys([(lamina(-0.62, 0.04, 0.62, -0.06, 0.06, ease_out(rel(t, 0.26, 0.34), 2), rel(t, 0.36, 0.56)), 1.0)], 0.005)
        tr = _linhas_de_impacto(T, 0.0, 0.0, 0.2, 0.36, 6, 0.3, 0.05) * k
        G += (g + risco * 1.4 + T.blur(risco, 0.03) * 0.8 + tr) * env
        H += (h + risco * 1.0 + tr * 0.5) * env
    # bolhas: nascem no impacto, sobem e estouram
    sub = np.random.default_rng(55)
    for j in range(9):
        nasce = 0.28 + sub.uniform(0, 0.12)
        estoura = sub.uniform(0.52, 0.92)
        r = sub.uniform(0.05, 0.11)
        x0, y0 = sub.uniform(-0.35, 0.35), sub.uniform(-0.15, 0.15)
        vx, vy = sub.uniform(-0.4, 0.4), sub.uniform(-0.9, -0.5)
        if t < nasce:
            continue
        dt = min(t, estoura) - nasce
        x, y = x0 + vx * dt * (1 - dt), y0 + vy * dt
        if t < estoura:
            rr = r * back(rel(t, nasce, nasce + 0.1), 2.2)
            bol = T.ring(rr, 0.016 + rr * 0.08, x, y) + T.gauss(x - rr * 0.38, y - rr * 0.4, rr * 0.18, rr * 0.18) * 1.2
            G += (bol * 1.2 + T.gauss(x, y, rr * 0.8, rr * 0.8) * 0.15) * env
            H += (bol * 0.6) * env
        else:
            q = rel(t, estoura, estoura + 0.09)
            if q < 1:
                aro = T.ring(r * (1 + 0.5 * q), 0.012, x, y) * (1 - q)
                pingos = _linhas_de_impacto(T, x, y, r * (1.1 + 0.4 * q), r * (1.6 + 0.6 * q), 6, 0.2, 0.02) * (1 - q)
                G += (aro + pingos * 1.3) * env
                H += (aro * 0.5 + pingos) * env
    return G, H


# ------------------------------------------------------------------ Woody: Laço
def _corda(T, pts, larg):
    """Corda: o traço e as marquinhas do trançado (essas vão no núcleo branco)."""
    linha = T.polyline(pts, larg)
    marcas = []
    for (ax, ay), (bx, by) in zip(pts[::2], pts[1::2]):
        mx, my = (ax + bx) / 2, (ay + by) / 2
        d = math.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        marcas.append((mx - ux * larg * 0.6 - uy * larg * 0.6, my - uy * larg * 0.6 + ux * larg * 0.6,
                       mx + ux * larg * 0.6 + uy * larg * 0.6, my + uy * larg * 0.6 - ux * larg * 0.6, 1.0))
    return linha, T.lines(marcas, larg * 0.35)


def _bezier(p0, p1, p2, n=26):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])
            for u in np.linspace(0, 1, n)]


def laco(T, t, rng):
    """Laço do Woody: a laçada gira no alto, voa até o alvo, cai em volta dele e a corda
    é puxada: o laço aperta, a corda estica reta e os tracinhos de força aparecem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    mao = (-1.05, 0.0)
    aperta = ease_in(rel(t, 0.58, 0.7), 2.0)
    cai = 0.0
    if t < 0.3:
        cx, cy, rx, ry = -0.45, -0.55, 0.28, 0.09
    elif t < 0.48:
        u = ease_in(rel(t, 0.3, 0.48), 1.2)
        cx, cy = -0.45 + 0.45 * u, -0.55 + 0.33 * u - 0.25 * math.sin(math.pi * u)
        rx, ry = 0.28 + 0.14 * u, 0.09 + 0.05 * u
    else:
        cai = ease_in(rel(t, 0.48, 0.58), 1.6)
        cx, cy = 0.0, -0.22 + 0.27 * cai
        rx, ry = 0.42 - 0.22 * aperta, 0.14 - 0.07 * aperta
    ang_giro = t * 40
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.78, 0.95))
    laca = _elipse(cx, cy, rx, ry, rot=-0.08 * (1 - cai), n=44)
    Lp, Lm = _corda(T, laca, 0.034)
    # nó (onde a corda encontra a laçada): corre na volta durante o giro, à esquerda depois
    if t < 0.3:
        nx, ny = cx + rx * math.cos(ang_giro), cy + ry * math.sin(ang_giro)
    else:
        nx, ny = cx - rx, cy
    folga = 0.28 * (1 - aperta) if t >= 0.3 else 0.2
    ctrl = ((mao[0] + nx) / 2, (mao[1] + ny) / 2 + folga - 0.04 * aperta)
    Cp, Cm = _corda(T, _bezier(mao, ctrl, (nx, ny)), 0.03)
    no = T.gauss(nx, ny, 0.035, 0.035)
    G += (Lp * 1.3 + T.blur(Lp, 0.03) * 0.7 + Cp * 1.1 + no * 1.3) * vis * env
    H += (Lp * 0.4 + Lm * 0.9 + Cp * 0.3 + Cm * 0.8 + no) * vis * env
    if t < 0.32:
        # o giro: vultos da laçada e o brilho correndo na volta
        gv = 1 - rel(t, 0.26, 0.32)
        vul = sum(T.polyline(_elipse(cx, cy, rx * (1 + 0.06 * j), ry * (1 + 0.1 * j), rot=-0.08, n=40), 0.012) for j in (1, 2)) * 0.5
        corre = T.arc_band(rx, 0.05, ang_giro - 2.4, ang_giro, squash=ry / rx, cx=cx, cy=cy)
        G += (vul + corre * 1.1) * gv * vis * env
        H += corre * 0.5 * gv * vis * env
    if 0.3 <= t < 0.5:
        R = rastro_de_velocidade(T, rng, 6, math.atan2(0.33, 0.45), 0.45, 0.2, 0.35, cx, cy, 0.014, seed=21) * pulso(t, 0.3, 0.5)
        G += R * env
    k = pulso(t, 0.6, 0.86)
    if k > 0:
        tr = T.zero()
        for lado in (-1, 1):
            bx = cx + lado * (rx + 0.04)
            tr += T.tapered([(bx + lado * 0.24, cy + o, bx + lado * 0.05, cy + o * 0.5, 1.0) for o in (-0.12, 0.0, 0.12)], 0.035)
        g, h = _clarao(T, k * 0.8, cx - rx, cy, 0.12, 0.5)
        aperto = T.ring(rx * 1.05, 0.03, cx, cy, squash=rx / max(ry, 1e-3)) * k
        G += (tr * 1.2 + g + aperto * 0.8) * env
        H += (tr * 0.6 + h + aperto * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Azula: Fogo azul
def fogo_azul(T, t, rng):
    """Fogo azul da Azula: um jato fino e afiado sai da esquerda, em línguas de chama que
    correm e engrossam, bate no alvo e abre em labaredas pontudas que sobem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    jato = janela(t, 0.0, 0.03) * (1 - rel(t, 0.5, 0.64))
    frente = min(0.05, -1.05 + 6.0 * t)
    # o miolo do jato (cone que alarga até o alvo)
    if jato > 0 and frente > -1.0:
        pts_c = [(x, -(0.025 + 0.09 * (x + 1.05))) for x in np.linspace(-1.05, frente, 14)]
        pts_b = [(x, 0.025 + 0.09 * (x + 1.05)) for x in np.linspace(frente, -1.05, 14)]
        cone = T.polys([(pts_c + pts_b, 1.0)], 0.03)
        miolo = T.polys([(lamina(-1.05, 0.0, frente, 0.0, 0.035), 1.0)], 0.01)
        G += (cone * 1.1 + miolo * 0.8) * jato * env
        H += (miolo * 1.3 + cone * 0.35) * jato * env
    # línguas de fogo correndo no jato (a cauda para trás, pontudas)
    sub = np.random.default_rng(91)
    formas = []
    for j in range(34):
        nasce = j / 34 * 0.52 - 0.12
        lado = sub.uniform(-1, 1)
        fase = sub.uniform(0, 6)
        peso = 0.6 + 0.3 * sub.uniform()
        dt = t - nasce
        x = -1.05 + 6.0 * dt
        if dt < 0 or x > 0.12:
            continue
        a = (x + 1.05) / 1.1
        alt, larg = 0.14 + 0.3 * a, 0.035 + 0.075 * a
        y = lado * (0.02 + 0.1 * a)
        ch = _chama(0.0, 0.0, alt, larg, fase + t * 40, 0.5)
        formas.append((_gira(ch, -math.pi / 2 + math.pi + lado * 0.15, x + alt * 0.25, y), peso))
    if formas:
        Fl = T.polys(formas, 0.01)
        G += (Fl * 1.2 + T.blur(Fl, 0.03) * 0.6) * env
        H += Fl * 0.45 * env
    # chegou: labaredas pontudas subindo do alvo e espirrando para os lados
    if t > 0.13:
        lab = []
        sub = np.random.default_rng(17)
        cresce = ease_out(rel(t, 0.14, 0.34), 2)
        apaga_ = 1 - rel(t, 0.62, 0.92)
        for j in range(9):
            x = -0.32 + 0.64 * j / 8 + sub.uniform(-0.03, 0.03)
            alt = (0.35 + 0.35 * (1 - abs(x) / 0.4)) * cresce * apaga_ * (0.8 + 0.3 * math.sin(t * 31 + j * 2.3))
            if alt > 0.02:
                lab.append((_chama(x, 0.2, alt, 0.08 + 0.02 * (j % 2), t * 38 + j, 0.45), 0.85))
        for lado in (-1, 1):
            for j in range(2):
                alt = (0.3 + 0.08 * j) * cresce * apaga_
                if alt > 0.02:
                    ch = _chama(0.0, 0.0, alt, 0.07, t * 33 + j * 3 + lado, 0.4)
                    lab.append((_gira(ch, lado * (0.9 + 0.35 * j), 0.05, 0.05), 0.7))
        if lab:
            Lb = T.polys(lab, 0.012)
            G += (Lb * 1.25 + T.blur(Lb, 0.04) * 0.7) * env
            H += (Lb * 0.55) * env
        k = pulso(t, 0.12, 0.5)
        g, h = _clarao(T, k, 0.03, 0.02, 0.24, 0.7, 0.0)
        G += g * env
        H += (h + T.gauss(0.03, 0.02, 0.1, 0.1) * k * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Coiote: Bigorna ACME
def _bigorna(cx, base, ex=1.0, ey=1.0):
    """Silhueta da bigorna (chifre à esquerda), com a base em y=`base`."""
    p = [(-0.56, -0.36), (-0.2, -0.42), (0.36, -0.42), (0.36, -0.28), (0.18, -0.25), (0.12, -0.12), (0.14, -0.06),
         (0.32, 0.0), (-0.32, 0.0), (-0.14, -0.06), (-0.12, -0.12), (-0.2, -0.25), (-0.36, -0.27)]
    return [(cx + x * ex, base + y * ey) for x, y in p]


def bigorna(T, t, rng):
    """Bigorna ACME: a sombra cresce no chão, a bigorna cai do alto com linhas de queda,
    esmaga o alvo (achata e volta), e a poeira sobe dos dois lados com estrelinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chao = 0.42
    cai = ease_in(rel(t, 0.08, 0.42), 1.6)
    sombra_k = janela(t, 0.0, 0.08) * (1 - rel(t, 0.4, 0.46))
    if sombra_k > 0:
        rx = 0.08 + 0.38 * ease_in(rel(t, 0.0, 0.42), 1.6)
        sombra = T.polys([(_elipse(0.0, chao + 0.01, rx, rx * 0.22, n=30), 1.0)], 0.02)
        aro = T.ring(rx, 0.016, 0.0, chao + 0.01, squash=1 / 0.22)
        G += (sombra * (0.25 + 0.35 * cai) + aro * 0.5) * sombra_k * env
        H += aro * 0.15 * sombra_k * env
    base = chao - 2.0 * (1 - cai)
    bate = rel(t, 0.42, 0.62)
    if t >= 0.42:
        amassa = 1 - 0.28 * math.sin(math.pi * min(1.0, bate * 1.6)) * (1 - bate)
        ex, ey = 1.0 + (1 - amassa) * 0.8, amassa
    else:
        ex, ey = 0.95, 1.06
    vis = janela(t, 0.1, 0.14) * (1 - rel(t, 0.72, 0.86))
    if vis > 0:
        sil = _bigorna(0.0, base, ex * 1.25, ey * 1.25)
        Bg = T.polys([(sil, 1.0)], 0.004)
        borda = T.polyline(sil + [sil[0]], 0.022)
        topo = T.polyline([(-0.25 * ex, base - 0.5 * ey), (0.42 * ex, base - 0.5 * ey)], 0.02)
        faixa = T.polys([(_barra(-0.15 * ex, base - 0.2 * ey, 0.15 * ex, base - 0.2 * ey, 0.06 * ey), 1.0)], 0.003)
        G += (Bg * 0.95 + T.blur(Bg, 0.04) * 0.6 + borda * 0.8) * vis * env
        H += (borda * 0.75 + topo * 0.9 + faixa * 0.6 + Bg * 0.08) * vis * env
        if t < 0.44:
            linhas = T.tapered([(x, base - 0.65 - 0.35 * cai, x, base - 0.58, 1.0) for x in (-0.38, -0.12, 0.14, 0.38)], 0.03) * janela(t, 0.2, 0.3)
            G += linhas * env
            H += linhas * 0.4 * env
    k = pulso(t, 0.4, 0.68)
    if k > 0:
        g, h = _clarao(T, k, 0.0, chao, 0.22, 0.9, 0.0)
        tr = T.tapered([(lado * (0.5 + 0.1 * j), chao - 0.05 - 0.1 * j, lado * (0.82 + 0.1 * j), chao - 0.15 - 0.16 * j, 1.0)
                        for lado in (-1, 1) for j in range(3)], 0.04) * k
        G += (g * 0.8 + tr * 1.2) * env
        H += (h * 0.8 + tr * 0.6) * env
    if t > 0.42:
        sub = np.random.default_rng(12)
        nuvens = []
        q = rel(t, 0.42, 1.0)
        for lado in (-1, 1):
            for j in range(6):
                d = 0.45 + 0.42 * ease_out(q, 2) * sub.uniform(0.5, 1.1)
                x = lado * d * sub.uniform(0.7, 1.0)
                y = chao - 0.04 - 0.22 * ease_out(q, 1.5) * sub.uniform(0.2, 1)
                nuvens.append((x, y, (1 - q) ** 1.2 * sub.uniform(0.6, 1)))
        P = T.splats(nuvens, 0.07 + 0.05 * q)
        E = _estrelinhas(T, t, 0.5, 1.0, 0.0, -0.38, 0.3, 3, 0.075, 10)
        G += (P * 0.9 + E * 1.3) * env
        H += (P * 0.12 + E * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Tom: Frigideira
def frigideira(T, t, rng):
    """Frigideira do Tom: a frigideira vem girando de lado e acerta em cheio com um BONG;
    ela treme, as ondas de vibração saem em arcos e as estrelinhas rodam em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.02, 0.3), 1.7)
    piv = (-1.0, 0.25)
    ang = -1.3 + 1.05 * u
    dist = 1.0
    if t < 0.3:
        cx, cy = piv[0] + dist * math.cos(ang), piv[1] + dist * math.sin(ang)
        cabo_ang = ang + math.pi
        treme = 0.0
    else:
        cx, cy = piv[0] + dist * math.cos(-0.25), piv[1] + dist * math.sin(-0.25)
        cabo_ang = -0.25 + math.pi
        q = rel(t, 0.3, 0.75)
        treme = math.sin(t * 95) * (1 - q) ** 1.5
        cx += 0.035 * treme
    r = 0.27
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.7, 0.84))
    sq = 1.0 - 0.1 * abs(treme)
    disco = T.polys([(_elipse(cx, cy, r, r * sq, n=40), 1.0)], 0.004)
    aro = T.ring(r, 0.022, cx, cy, squash=1 / sq)
    fundo = T.ring(r * 0.72, 0.012, cx, cy, squash=1 / sq)
    hx2, hy2 = cx + math.cos(cabo_ang) * (r + 0.5), cy + math.sin(cabo_ang) * (r + 0.5)
    cabo = T.polys([(_barra(cx + math.cos(cabo_ang) * (r - 0.02), cy + math.sin(cabo_ang) * (r - 0.02), hx2, hy2, 0.085, 0.075), 1.0)], 0.004)
    furo = T.gauss(cx + math.cos(cabo_ang) * (r + 0.43), cy + math.sin(cabo_ang) * (r + 0.43), 0.018, 0.018)
    reflexo = T.arc_band(r * 0.82, 0.03, -2.6, -1.6, cx=cx, cy=cy)
    G += ((disco * 0.75 + aro * 0.9 + cabo * 1.0 + T.blur(disco, 0.04) * 0.5) * (1 - furo * 0.8) + fundo * 0.3) * vis * env
    H += (aro * 0.75 + reflexo * 1.1 + fundo * 0.25 + cabo * 0.3) * vis * env
    if t < 0.32:
        vult = []
        for j in range(1, 4):
            a = ang - 0.14 * j
            vult.append((_elipse(piv[0] + dist * math.cos(a), piv[1] + dist * math.sin(a), r, r, n=30), 0.35 * (1 - j / 4)))
        V = T.polys(vult, 0.015) * janela(t, 0.06, 0.12)
        G += V * env
    k = pulso(t, 0.28, 0.55)
    if k > 0:
        g, h = _clarao(T, k, cx + 0.12, cy, 0.22, 0.8, 0.5)
        G += g * env
        H += h * env
    # ondas de vibração: arcos ")" e "(" saindo da frigideira
    for j in range(3):
        a0 = 0.3 + 0.1 * j
        q = rel(t, a0, a0 + 0.32)
        if 0 < q < 1:
            rr = r + 0.06 + 0.42 * q
            ond = (T.arc_band(rr, 0.035, -0.75, 0.75, cx=cx, cy=cy, crescente=True) + T.arc_band(rr, 0.035, math.pi - 0.75, math.pi + 0.75, cx=cx, cy=cy, crescente=True)
                   + T.arc_band(rr, 0.035, -math.pi / 2 - 0.55, -math.pi / 2 + 0.55, cx=cx, cy=cy, crescente=True) * 0.7)
            G += ond * (1 - q) * 1.4 * env
            H += ond * (1 - q) * 0.6 * env
    E = _estrelinhas(T, t, 0.42, 1.0, cx, cy - r - 0.12, 0.34, 4, 0.07, 9)
    G += E * 1.3 * env
    H += E * 0.8 * env
    return G, H


# ------------------------------------------------------------------ Esqueleto: Cajado da Caveira
def _cranio_de_carneiro(T, cx, cy, s, olhos=0.0):
    """Crânio de carneiro: caixa craniana, focinho, órbitas vazadas e os chifres em espiral."""
    cranio = _elipse(cx, cy - 0.02 * s, 0.13 * s, 0.12 * s, n=24)
    focinho = [(cx - 0.07 * s, cy + 0.05 * s), (cx + 0.07 * s, cy + 0.05 * s), (cx + 0.045 * s, cy + 0.2 * s), (cx - 0.045 * s, cy + 0.2 * s)]
    C = T.polys([(cranio, 1.0), (focinho, 1.0)], 0.004)
    C = np.minimum(C, 1.0)
    orbitas = T.gauss(cx - 0.055 * s, cy, 0.03 * s, 0.026 * s) + T.gauss(cx + 0.055 * s, cy, 0.03 * s, 0.026 * s)
    narinas = T.gauss(cx - 0.02 * s, cy + 0.16 * s, 0.012 * s, 0.015 * s) + T.gauss(cx + 0.02 * s, cy + 0.16 * s, 0.012 * s, 0.015 * s)
    buracos = np.clip(orbitas * 1.6 + narinas * 1.3, 0, 1)
    chifres = T.zero()
    for lado in (-1, 1):
        ox, oy = cx + lado * 0.19 * s, cy - 0.01 * s
        pts = []
        for k in range(30):
            u = k / 29
            a = -math.pi / 2 + 1.8 * math.pi * u
            rr = 0.16 * s * (1 - 0.7 * u)
            pts.append((ox + lado * math.cos(a) * rr, oy + math.sin(a) * rr))
        chifres += T.polyline(pts, 0.042 * s)
    brilho_olhos = (T.gauss(cx - 0.055 * s, cy, 0.022 * s, 0.022 * s) + T.gauss(cx + 0.055 * s, cy, 0.022 * s, 0.022 * s)) * olhos
    return C * (1 - buracos), chifres, buracos, brilho_olhos


def cajado_da_caveira(T, t, rng):
    """Cajado da Caveira do Esqueleto: o cajado com o crânio de carneiro desce numa pancada,
    estala no alvo, os olhos da caveira acendem e faíscas mágicas saem girando num círculo
    de magia sinistra."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px, py, L = -0.62, 0.62, 0.86
    u = ease_in(rel(t, 0.03, 0.3), 1.9)
    fim = math.atan2(-0.62, 0.6)
    phi = -1.95 + (1.95 + fim) * u - 0.08 * pulso(t, 0.3, 0.5)
    hx, hy = px + L * math.cos(phi), py + L * math.sin(phi)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.72, 0.88))
    haste = T.polys([(_barra(px - math.cos(phi) * 0.4, py - math.sin(phi) * 0.4, hx - math.cos(phi) * 0.12, hy - math.sin(phi) * 0.12, 0.045, 0.055), 1.0)], 0.004)
    olhos = janela(t, 0.3, 0.38) * (1 - rel(t, 0.7, 0.85))
    C, ch, buracos, bo = _cranio_de_carneiro(T, hx, hy, 1.45, olhos)
    S = C + ch * 0.95
    G += ((S * 1.3 + T.blur(S, 0.03) * 0.7) * (1 - buracos * 0.85) + haste * 0.9 + bo * 2.2) * vis * env
    H += (C * 0.55 + ch * 0.45 + haste * 0.25 + bo * 2.4) * vis * env
    corre = pulso(t, 0.05, 0.36)
    if corre > 0:
        arco = T.arc_band(L, 0.11, phi - 1.1, phi, cx=px, cy=py)
        G += arco * corre * 1.0 * env
        H += arco * corre * 0.3 * env
    k = pulso(t, 0.28, 0.56)
    if k > 0:
        g, h = _clarao(T, k, 0.05, 0.02, 0.22, 0.75, 0.2)
        est = T.polys([(estrela(0.05, 0.02, 0.32 * k + 0.01, 0.1, 7, 0.4), 1.0)], 0.006) * k
        G += (g + est * 1.1) * env
        H += (h + est * 0.6) * env
    # o círculo de magia girando e as faíscas mágicas (cintilantes de quatro pontas)
    m = janela(t, 0.32, 0.42) * (1 - rel(t, 0.78, 0.96))
    if m > 0:
        rr = 0.5 + 0.06 * math.sin(t * 20)
        circ = T.zero()
        for j in range(8):
            a0 = j / 8 * TAU + t * 6
            circ += T.arc_band(rr, 0.03, a0, a0 + 0.5, cx=0.05, cy=0.02, crescente=True)
        G += circ * 1.2 * m * env
        H += circ * 0.5 * m * env
        sub = np.random.default_rng(66)
        brilhos = T.zero()
        nucleos = T.zero()
        q = rel(t, 0.3, 0.95)
        for j in range(11):
            a = sub.uniform(0, TAU) + q * 3.5 * (1 if j % 2 else -1)
            d = (0.12 + 0.6 * ease_out(q, 1.8)) * sub.uniform(0.6, 1.05)
            x, y = 0.05 + math.cos(a) * d, 0.02 + math.sin(a) * d - 0.15 * q
            pis = 0.5 + 0.5 * math.sin(t * 40 + j * 2.1)
            tam = 0.16 * (0.6 + 0.4 * pis) * (1 - q) ** 0.5
            brilhos += T.flare(x, y, tam, ang=a, thin=0.03) * (0.6 + 0.4 * pis)
            nucleos += T.gauss(x, y, 0.02, 0.02)
        G += (brilhos * 1.2 + nucleos * 1.2) * m * env
        H += (brilhos * 0.8 + nucleos) * m * env
    return G, H


# ------------------------------------------------------------------ Lion-O: Espada de Augúrio
def _olho_de_thundera(T, cx, cy, abre, s=1.0):
    """O Olho de Thundera: olho amendoado com íris redonda e pupila de gato (vazada)."""
    w, h = 0.3 * s, 0.17 * s * abre
    cima = [(cx + w * math.cos(a), cy - h * math.sin(a)) for a in np.linspace(0, math.pi, 20)]
    baixo = [(cx - w * math.cos(a), cy + h * math.sin(a)) for a in np.linspace(0, math.pi, 20)]
    amend = np.minimum(T.polys([(cima + baixo, 1.0)], 0.004), 1.0)
    iris = T.ring(0.11 * s, 0.02 * s, cx, cy) * amend
    pupila = np.clip(T.gauss(cx, cy, 0.024 * s, 0.1 * s * abre + 1e-3) * 1.6, 0, 1)
    borda = T.polyline(cima + baixo + [cima[0]], 0.024 * s)
    return amend * (1 - pupila) + borda * 0.8, borda + iris * 0.8


def espada_de_augurio(T, t, rng):
    """Espada de Augúrio do Lion-O: a espada corta de cima para baixo num arco largo, o
    rastro do corte fica no ar e, no meio dele, o Olho de Thundera abre brilhando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px, py, L = -0.72, 0.18, 1.05
    u = ease_out(rel(t, 0.04, 0.3), 2.2)
    phi = -1.75 + 2.45 * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.4, 0.55))
    dx, dy = math.cos(phi), math.sin(phi)
    nx, ny = -dy, dx
    lam = T.polys([(lamina(px + dx * 0.2, py + dy * 0.2, px + dx * L, py + dy * L, 0.05), 1.0)], 0.004)
    guarda = T.zero()
    g0 = (px + dx * 0.2, py + dy * 0.2)
    for lado in (-1, 1):
        pts = [g0, (g0[0] + nx * lado * 0.09, g0[1] + ny * lado * 0.09),
               (g0[0] + nx * lado * 0.14 + dx * 0.07, g0[1] + ny * lado * 0.14 + dy * 0.07)]
        guarda += T.polyline(pts, 0.03)
    cabo = T.polys([(_barra(px - dx * 0.05, py - dy * 0.05, px + dx * 0.2, py + dy * 0.2, 0.045), 1.0)], 0.004)
    gema = T.gauss(px + dx * 0.21, py + dy * 0.21, 0.025, 0.025)
    S = lam + guarda * 0.9 + cabo * 0.8
    G += (S * 1.3 + T.blur(S, 0.03) * 0.7 + gema * 1.5) * vis * env
    H += (lam * 0.9 + guarda * 0.4 + gema * 1.6) * vis * env
    # o rastro do corte: meia-lua larga que fica e é comida da cauda
    cauda_ = -1.75 + 2.45 * ease_out(rel(t, 0.12, 0.6), 1.6)
    if phi - cauda_ > 0.05 and t < 0.75:
        arco = T.arc_band(L * 0.78, 0.17, cauda_, phi, cx=px, cy=py, crescente=True)
        fino = T.arc_band(L * 0.93, 0.03, cauda_, phi, cx=px, cy=py)
        sumir = 1 - rel(t, 0.4, 0.75)
        G += (arco * 1.2 + fino * 1.2) * sumir * env
        H += (arco * 0.5 + fino * 0.9) * sumir * env
    k = pulso(t, 0.2, 0.46)
    if k > 0:
        g, h = _clarao(T, k, 0.02, 0.0, 0.18, 0.6, 0.6)
        G += g * env
        H += h * env
    # o Olho de Thundera abre no rastro
    abre = ease_out(rel(t, 0.34, 0.5), 2) * (1 - ease_in(rel(t, 0.78, 0.92), 2))
    if abre > 0.02:
        O, Oh = _olho_de_thundera(T, 0.0, -0.02, abre, 1.25)
        kk = janela(t, 0.34, 0.4)
        raio = (T.flare(0.0, -0.02, 0.9 * abre, ang=0.0, thin=0.012) + T.flare(0.0, -0.02, 0.5 * abre, ang=math.pi / 4, thin=0.012) * 0.6) * pulso(t, 0.36, 0.86)
        G += (O * 1.3 + T.blur(O, 0.05) * 0.9 + raio * 0.8) * kk * env
        H += (Oh * 1.0 + O * 0.25 + raio * 1.1) * kk * env
    return G, H


REGISTRO = [
    ("sais", sais, GRANDE, "Sais do Raphael: dois sais estocam em sequência, cada um com clarão de três pontas", False),
    ("nunchakus", nunchakus, GRANDE, "Nunchakus do Michelangelo: giram na corrente e batem duas vezes", False),
    ("bicada", bicada, GRANDE, "Bicada-britadeira: o bico bate e volta, o buraco racha e as lascas voam", False),
    ("golpe_alienigena", golpe_alienigena, GRANDE, "Golpe alienígena: a ampulheta do Omnitrix estoura em verde e o punho do alien acerta", False),
    ("soco_de_marinheiro", soco_de_marinheiro, GRANDE, "Soco de marinheiro: o braço gira como manivela, soco com estrelas e âncora estampada", False),
    ("machado_de_energon", machado_de_energon, GRANDE, "Machado de energon: o machado de energia desce num arco pesado e crava no alvo", False),
    ("karate", karate, GRANDE, "Karatê: mão em faca desce num tchop e as bolhas estouram", False),
    ("laco", laco, GRANDE, "Laço: a laçada gira, voa, cai em volta do alvo e aperta", False),
    ("fogo_azul", fogo_azul, GRANDE, "Fogo azul: jato afiado de chamas que abre em labaredas no alvo", False),
    ("bigorna", bigorna, GRANDE, "Bigorna ACME: a sombra cresce, a bigorna cai, esmaga e levanta poeira", False),
    ("frigideira", frigideira, GRANDE, "Frigideira: acerta de lado com um BONG, treme em ondas e estrelinhas", False),
    ("cajado_da_caveira", cajado_da_caveira, GRANDE, "Cajado da Caveira: o crânio de carneiro bate e solta faíscas mágicas num círculo", False),
    ("espada_de_augurio", espada_de_augurio, GRANDE, "Espada de Augúrio: corte em arco e o Olho de Thundera abre brilhando no rastro", False),
]
