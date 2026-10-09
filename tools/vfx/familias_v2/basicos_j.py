"""Ataques básicos com animação própria, lote j.

Homer (barrigada), Bart (estilingue), Bugiganga (gadget surpresa), Danny Phantom
(raio fantasma), Coringa (flor de lapela), Arlequina (taco de beisebol), Capitão
Planeta (raio de Gaia) e Scooby/Coragem (mordida de desenho). Tudo vem da
esquerda e acerta o centro; objetos (barriga, pedra, luva, flor, taco, dentes)
são silhuetas cheias com contorno colorido, para lerem bem em 100–160 px.
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


def _elipse(cx, cy, rx, ry, n=40, onda=0.0, k=5, fase=0.0, a0=0.0, a1=TAU):
    pts = []
    for j in range(n + 1 if a1 - a0 < TAU - 1e-3 else n):
        a = a0 + (a1 - a0) * j / n
        r = 1 + onda * math.sin(k * a + fase)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def _solido(T, shapes, blur=0.004, larg=0.025):
    """Silhueta cheia + só a borda dela (o traço de desenho animado)."""
    corpo = np.minimum(T.polys(shapes, blur), 1.0)
    borda = corpo * (1 - smooth(T.blur(corpo, larg), 0.78, 0.97))
    return corpo, borda


def _clarao(T, k, cx=0.0, cy=0.0, r=0.2, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.4
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.6 * k + 0.01, ang=ang + math.pi / 4, thin=0.012)) * k * 1.4
    return g, h


def _estouro(T, t, t0, t1, cx, cy, r, n=9, interno=0.5, seed=5):
    """Balão de estouro em zigue-zague (o "TOCK!", o "POW!") com contorno."""
    k = back(rel(t, t0, t0 + 0.12), 2.2) * apaga(t, t0 + 0.12, t1)
    if k <= 0.01:
        return T.zero(), T.zero()
    sub = np.random.default_rng(seed)
    raios = [sub.uniform(0.75, 1.0) for _ in range(n)]
    pts = []
    for j in range(2 * n):
        a = TAU * j / (2 * n) + 0.2
        rr = (raios[j // 2] if j % 2 == 0 else interno) * r * k
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return _solido(T, [(pts, 1.0)], 0.004, 0.03)


def _linhas_de_acao(T, t, t0, t1, cx, cy, r0, comp, n=12, ang0=0.2, larg=0.016, a_ini=0.0, a_fim=TAU):
    k = pulso(t, t0, t1)
    if k <= 0:
        return T.zero()
    abre = ease_out(rel(t, t0, t1), 2)
    segs = []
    for j in range(n):
        a = a_ini + (a_fim - a_ini) * (j + 0.5) / n + ang0
        r1 = r0 + 0.12 * abre
        segs.append((cx + math.cos(a) * r1, cy + math.sin(a) * r1, cx + math.cos(a) * (r1 + comp), cy + math.sin(a) * (r1 + comp), 1))
    return T.lines(segs, larg, 0.002) * k


def _estrelinhas(T, t, t0, cx, cy, n, r, dist, seed, a0=-2.6, a1=-0.5, vida=0.55):
    """Estrelinhas de desenho que pulam do contato, giram e caem um pouco."""
    if t < t0:
        return T.zero()
    sub = np.random.default_rng(seed)
    tt = rel(t, t0, t0 + vida)
    s = back(rel(t, t0, t0 + 0.14), 2.0) * (1 - rel(t, t0 + vida * 0.6, t0 + vida))
    shapes = []
    for j in range(n):
        a = a0 + (a1 - a0) * (j + 0.5) / n + sub.uniform(-0.15, 0.15)
        d = dist * ease_out(tt, 2.6) * sub.uniform(0.75, 1.05)
        rr = r * s * sub.uniform(0.8, 1.2)
        if rr < 0.012:
            continue
        shapes.append((estrela(cx + math.cos(a) * d, cy + math.sin(a) * d + 0.12 * tt * tt, rr, t * 9 + j, 5, 0.45), 1.0))
    return T.polys(shapes, 0.003)


def _orbita_de_estrelas(T, t, t0, cx, cy, rx, ry, n, r, giro=1.4):
    """Estrelinhas tontas girando em volta da cabeça de quem levou."""
    if t < t0:
        return T.zero()
    sai = back(rel(t, t0, t0 + 0.18))
    shapes = []
    for j in range(n):
        a = TAU * j / n + t * TAU * giro
        frente = 0.75 + 0.35 * (math.sin(a) > 0)
        shapes.append((estrela(cx + math.cos(a) * rx, cy + math.sin(a) * ry, r * sai * frente + 0.003, a * 2), 1.0))
    return T.polys(shapes, 0.003) * apaga(t, 0.82, 1)


def _coracao(cx, cy, r, ang=0.0, n=32):
    pts = []
    for j in range(n):
        u = TAU * j / n
        x = 16 * math.sin(u) ** 3
        y = -(13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u))
        pts.append((x / 17 * r, y / 17 * r))
    return _gira(pts, ang, cx, cy)


def _gota(cx, cy, r, ang, n=20):
    """Gota (lágrima/suor): bolinha com a ponta apontando para `ang`."""
    pts = []
    for j in range(n):
        u = TAU * j / n
        rr = r * (1 + 1.3 * max(0.0, math.cos(u)) ** 6)
        pts.append((rr * math.cos(u), rr * math.sin(u) * (1 - 0.35 * max(0.0, math.cos(u)))))
    return _gira(pts, ang, cx, cy)


def _bezier(p0, p1, p2, u):
    a = (1 - u) ** 2
    b = 2 * (1 - u) * u
    c = u * u
    return a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]


# ------------------------------------------------------------------ Homer: Barrigada
def barrigada(T, t, rng):
    """Barrigada do Homer: a barriga redonda (com umbigo e as dobrinhas) entra da esquerda,
    amassa no alvo e balança como gelatina; ondas achatadas tremendo saem do contato e
    estrelinhas pulam."""
    G, H = vazio(T)
    bate = 0.24
    rx0, ry0 = 0.5, 0.6
    if t < bate:
        u = ease_in(rel(t, 0.0, bate), 1.4)
        frente = -0.8 + 0.86 * u
        sq = 0.0
    else:
        tt = t - bate
        sq = math.exp(-tt * 7) * math.cos(tt * 34)                 # o balanço da barriga
        recua = ease_in(rel(t, 0.58, 0.9), 1.6)
        frente = 0.06 * (1 - sq) - 0.9 * recua
    rx = rx0 * (1 - 0.2 * sq)
    ry = ry0 * (1 + 0.12 * sq)
    cx, cy = frente - rx, 0.1
    vivo = apaga(t, 0.62, 0.9)
    barriga = _elipse(cx, cy, rx, ry, 56, 0.025 * abs(sq), 3, t * 30)
    corpo, borda = _solido(T, [(barriga, 1.0)], 0.004, 0.035)
    # volume: brilho no alto da frente da barriga (parece redonda)
    luz = T.gauss(cx + rx * 0.45, cy - ry * 0.35, rx * 0.35, ry * 0.3) * corpo
    # umbigo: um "c" fundo no meio da frente
    ux, uy = cx + rx * 0.62, cy + 0.08 + 0.03 * sq
    umbigo = T.polyline(_elipse(ux, uy, 0.04, 0.05, 16, a0=-2.4, a1=2.4), 0.022) * corpo
    # tremidas: parênteses fora da barriga enquanto ela balança
    tre = T.zero()
    if t >= bate:
        k_t = pulso(t, bate, 0.62)
        for yy in (-0.38, 0.42):
            for m in (0, 1):
                d = 0.07 + 0.07 * m
                arco = _elipse(cx, cy + yy * ry / 0.6 * 0.0, rx + d, ry + d, 30, a0=(-1.25 if yy < 0 else 0.75), a1=(-0.75 if yy < 0 else 1.25))
                tre += T.polyline(arco, 0.022) * (1 - 0.3 * m)
        tre *= k_t
    G += (corpo * 0.5 + borda * 1.7 + luz * 0.5 - umbigo * 0.45 + tre * 1.2) * vivo
    H += ((corpo * 0.45 + luz * 0.6) - umbigo * 0.7).clip(0, None) * vivo + tre * 0.5 * vivo
    # linhas de velocidade atrás da barriga, enquanto chega
    if t < bate + 0.08:
        segs = []
        for j, y in enumerate((-0.32, -0.08, 0.16, 0.4)):
            x2 = cx - rx * 0.4 - 0.06 * (j % 2)
            segs.append((x2 - 0.45, cy + y, x2, cy + y, 1))
        L = T.tapered(segs, 0.03) * janela(t, 0.02, 0.08) * (1 - rel(t, bate, bate + 0.08)) * (1 - corpo)
        G += L * 1.1
        H += L * 0.5
    if t >= bate:
        k = pulso(t, bate, 0.5)
        g, h = _clarao(T, k, 0.04, 0.06, 0.16, 0.6, 0.0)
        G += g
        H += h
        # ondas de balanço: círculos achatados que saem do contato, crescem e tremem
        ondas = T.zero()
        for j in range(3):
            t0 = bate + 0.07 * j
            if t < t0:
                continue
            uu = rel(t, t0, t0 + 0.5)
            R = 0.16 + 0.6 * ease_out(uu, 2.0)
            treme = 0.07 * (1 - uu)
            anel = _elipse(0.02, 0.1, R * 0.55, R, 40, treme, 6, t * 60 + 2 * j, -1.25, 1.25)
            ondas += T.polyline(anel, 0.034 * (1 - uu) + 0.012) * (1 - uu) ** 1.1
        ondas *= 1 - corpo * 0.9
        G += T.glow(ondas, 1.3, 0.8, 0.02)
        H += ondas * 0.5
        E = _estrelinhas(T, t, bate + 0.02, 0.05, -0.2, 4, 0.1, 0.62, 3, -2.5, -0.1)
        G += T.glow(E, 1.3, 0.9, 0.02)
        H += E * 0.9
    return G, H


# ------------------------------------------------------------------ Bart: Estilingue
def _pedra(cx, cy, r, giro):
    sub = np.random.default_rng(17)
    raios = [sub.uniform(0.78, 1.0) for _ in range(9)]
    return [(cx + math.cos(giro + TAU * j / 9) * r * raios[j], cy + math.sin(giro + TAU * j / 9) * r * raios[j] * 0.85) for j in range(9)]


def estilingue(T, t, rng):
    """Estilingue do Bart: a pedrinha sai da esquerda num arco (com o rastro pontilhado),
    acerta o alvo com um "TOCK" em estrela, quica para trás e deixa estrelinhas girando."""
    G, H = vazio(T)
    bate = 0.3
    p0, p1, p2 = (-1.0, 0.12), (-0.48, -0.62), (0.0, 0.0)
    if t <= bate:
        u = rel(t, 0.0, bate) ** 1.15
        px, py = _bezier(p0, p1, p2, u)
        giro = -t * 26
        vis = janela(t, 0.0, 0.04)
    else:
        tt = rel(t, bate, 0.78)
        px, py = -0.42 * ease_out(tt, 1.6), -0.38 * math.sin(math.pi * min(1, tt * 1.1)) + 0.25 * tt * tt
        giro = -bate * 26 + (t - bate) * 30
        vis = 1 - rel(t, 0.55, 0.78)
    P, Pb = _solido(T, [(_pedra(px, py, 0.105, giro), 1.0)], 0.003, 0.02)
    G += (P * 0.6 + Pb * 1.7 + T.blur(P, 0.04) * 0.6) * vis
    H += P * 0.75 * vis
    # rastro: pontinhos ao longo do arco já percorrido
    if 0.02 < t < bate + 0.18:
        pts = []
        uu = rel(min(t, bate), 0.0, bate) ** 1.15
        for j in range(14):
            v = uu * j / 13
            if uu - v < 0.04:
                continue
            x, y = _bezier(p0, p1, p2, v)
            pts.append((x, y, 0.4 + 0.6 * v / max(uu, 1e-3)))
        tr = T.splats(pts, 0.014) * (1 - rel(t, bate, bate + 0.18))
        ini = max(0.0, uu - 0.25)
        cauda = T.polyline([_bezier(p0, p1, p2, ini + (uu - ini) * j / 12) for j in range(13)], 0.02)
        cauda = T.blur(cauda, 0.012) * (1 - rel(t, bate - 0.02, bate + 0.1))
        G += tr * 1.4 + cauda * 1.3
        H += tr * 0.7 + cauda * 0.5
    if t >= bate:
        k = pulso(t, bate, 0.55)
        g, h = _clarao(T, k, 0.0, 0.0, 0.14, 0.5)
        cheio, borda = _estouro(T, t, bate, 0.62, 0.02, 0.0, 0.34, 8, 0.48, 9)
        L = _linhas_de_acao(T, t, bate, 0.6, 0.02, 0.0, 0.36, 0.16, 10)
        # lasquinhas da pedra
        sub = np.random.default_rng(21)
        lascas = []
        for j in range(4):
            a = sub.uniform(-2.6, -0.4)
            d = 0.15 + 0.45 * ease_out(rel(t, bate, 0.7), 2)
            lascas.append((_pedra(math.cos(a) * d, math.sin(a) * d + 0.3 * rel(t, bate, 0.8) ** 2, 0.03, t * 20 + j), 1.0))
        La = T.polys(lascas, 0.003) * (1 - rel(t, 0.5, 0.75))
        O = _orbita_de_estrelas(T, t, 0.42, 0.0, -0.5, 0.36, 0.1, 4, 0.085)
        G += g + cheio * 0.45 + borda * 1.5 + L * 1.1 + La * 1.4 + T.glow(O, 1.3, 1, 0.02)
        H += h + cheio * 0.8 + borda * 0.4 + L * 0.5 + La * 0.6 + O * 0.9
    return G, H


# ------------------------------------------------------------------ Bugiganga: Gadget surpresa
def _luva(gx, gy, esc=1.0, achata=1.0):
    """Luva de boxe virada para a direita: punho redondo, polegar em cima e o punho da luva atrás."""
    rx, ry = 0.21 * esc * achata, 0.18 * esc * (2 - achata) ** 0.5
    punho = _elipse(gx, gy, rx, ry, 36)
    polegar = _elipse(gx - 0.03 * esc, gy - ry * 0.85, 0.12 * esc, 0.065 * esc, 24)
    cx0, cx1 = gx - rx - 0.12 * esc, gx - rx * 0.55
    cano = [(cx0, gy - 0.12 * esc), (cx1, gy - 0.14 * esc), (cx1, gy + 0.14 * esc), (cx0, gy + 0.12 * esc)]
    return punho, polegar, cano, cx0


def gadget_surpresa(T, t, rng):
    """Gadget surpresa: uma luva de boxe numa mola em zigue-zague dispara da esquerda,
    acerta com um POW, a mola balança e recolhe."""
    G, H = vazio(T)
    bate = 0.2
    if t < bate:
        frente = -0.95 + 1.11 * ease_out(rel(t, 0.0, bate), 1.6)
        achata = 1.0
    else:
        tt = t - bate
        mola = math.exp(-tt * 8) * math.sin(tt * 40)
        recolhe = ease_in(rel(t, 0.6, 0.86), 1.8)
        frente = 0.16 - 0.04 * mola - 1.5 * recolhe
        achata = 1 - 0.18 * math.exp(-tt * 14)
    esc = 1.25
    rx = 0.21 * esc * achata
    gx, gy = frente - rx, 0.02
    punho, polegar, cano, cx0 = _luva(gx, gy, esc, achata)
    vivo = 1 - rel(t, 0.78, 0.9)
    C, Cb = _solido(T, [(punho, 1.0)], 0.003, 0.026)
    Po, Pob = _solido(T, [(polegar, 1.0)], 0.003, 0.022)
    Po = Po * (1 - C * 0.0)
    K, Kb = _solido(T, [(cano, 1.0)], 0.003, 0.02)
    tudo = np.minimum(C + Po + K, 1)
    # a costura do polegar (passa por cima do punho), o vinco dos dedos e a faixa do cano
    costura = T.polyline(_elipse(gx - 0.03 * esc, gy - 0.18 * esc * 0.85, 0.12 * esc, 0.065 * esc, 24, a0=0.2, a1=math.pi - 0.2), 0.02)
    vinco = T.polyline(_elipse(gx + rx * 0.25, gy + 0.02, rx * 0.6, 0.1 * esc, 18, a0=-0.9, a1=0.9), 0.016) * C
    faixa = T.polyline([(cx0 + 0.06, gy - 0.16), (cx0 + 0.06, gy + 0.16)], 0.026) * K
    linhas = np.minimum(costura * tudo + vinco + faixa, 1)
    luva = (tudo * 0.5 + np.maximum(Cb, np.maximum(Pob * (1 - C), Kb * (1 - C))) * 1.7 + linhas * 1.2)
    G += luva * vivo
    H += (tudo * 0.75 - linhas * 0.75).clip(0, None) * vivo
    C = tudo
    # a mola: zigue-zague do canto até o cano da luva
    x0, x1 = -1.08, cx0 + 0.02
    if x1 > x0 + 0.02:
        voltas = 7
        pts = []
        for j in range(voltas * 2 + 1):
            x = x0 + (x1 - x0) * j / (voltas * 2)
            y = gy + (0.0 if j in (0, voltas * 2) else (0.1 if j % 2 else -0.1))
            pts.append((x, y))
        M = T.polyline(pts, 0.026)
        G += T.glow(M, 1.3, 0.6, 0.015) * vivo
        H += M * 0.55 * vivo
    if t < bate + 0.05:
        segs = [(frente - 0.75, gy + y, frente - 0.3, gy + y, 1) for y in (-0.24, 0.0, 0.24)]
        L = T.tapered(segs, 0.025) * janela(t, 0.03, 0.08) * (1 - rel(t, bate, bate + 0.05))
        G += L
        H += L * 0.4
    if t >= bate:
        cheio, borda = _estouro(T, t, bate, 0.58, 0.18, 0.02, 0.42, 10, 0.55, 13)
        fora = 1 - C * 0.85
        L = _linhas_de_acao(T, t, bate, 0.55, 0.18, 0.02, 0.44, 0.18, 12)
        g, h = _clarao(T, pulso(t, bate, 0.45), 0.18, 0.02, 0.15, 0.55)
        E = _estrelinhas(T, t, bate + 0.04, 0.25, -0.15, 3, 0.09, 0.55, 7, -2.0, -0.2)
        G += (cheio * 0.4 + borda * 1.5) * fora + L * 1.1 + g * fora + T.glow(E, 1.3, 0.9, 0.02)
        H += (cheio * 0.75 + borda * 0.4) * fora + L * 0.5 + h * fora + E * 0.9
    return G, H


# ------------------------------------------------------------------ Danny Phantom: Raio fantasma
def raio_fantasma(T, t, rng):
    """Raio fantasma: o raio de ectoplasma corre da esquerda com fiapos fantasmagóricos
    ondulando em volta; no alvo espirra em caudas de fantasma que se enrolam e somem."""
    G, H = vazio(T)
    x0 = -1.0
    cab = -0.72 + 0.72 * ease_out(rel(t, 0.0, 0.18), 1.6)
    cauda = x0 + 1.0 * ease_in(rel(t, 0.42, 0.66), 1.5)
    larg = 0.08 * (1 - 0.5 * rel(t, 0.3, 0.6))
    if cab - cauda > 0.02:
        n = 40
        nucleo = []
        for j in range(n + 1):
            x = cauda + (cab - cauda) * j / n
            nucleo.append((x, 0.012 * math.sin(x * 14 - t * 40)))
        Rn = T.polyline(nucleo, larg)
        Rf = T.polyline(nucleo, larg * 0.4)
        fiapos = T.zero()
        for s in range(3):
            pts = []
            for j in range(n + 1):
                x = cauda + (cab - cauda) * j / n
                amp = 0.13 + 0.05 * math.sin(x * 3 + s)
                pts.append((x, amp * math.sin(x * 7.5 - t * 34 + s * TAU / 3)))
            fiapos += T.polyline(pts, 0.02) * (0.6 + 0.4 * (s == 0))
        fiapos = T.blur(fiapos, 0.006)
        G += T.glow(Rn, 1.2, 1.2, 0.04) + fiapos * 1.3 + T.blur(fiapos, 0.03) * 0.8
        H += Rf * 1.3 + Rn * 0.5 + fiapos * 0.35
        cg = T.gauss(cab, 0.0, 0.09, 0.09) * 1.6 * (1 - rel(t, 0.5, 0.66))
        G += cg
        H += cg * 0.6
    bate = 0.18
    if t >= bate:
        tt = rel(t, bate, 0.95)
        k = pulso(t, bate, 0.6)
        g, h = _clarao(T, k, 0.0, 0.0, 0.2, 0.7, 0.0)
        anel = T.ring(0.12 + 0.5 * ease_out(rel(t, bate, 0.7), 2.2), 0.04) * pulso(t, bate, 0.75)
        # caudas de fantasma: fitas grossas que saem do contato, sobem ondulando e afinam na ponta
        formas = []
        sub = np.random.default_rng(29)
        for j in range(4):
            a = -2.9 + 2.6 * (j + 0.5) / 4 + sub.uniform(-0.1, 0.1)
            comp = (0.38 + 0.2 * sub.uniform(0, 1)) * ease_out(tt, 1.8)
            enrola = 1.3 + 0.6 * sub.uniform(0, 1)
            eixo = []
            for m in range(14):
                v = m / 13
                r = 0.14 + comp * v
                aa = a + enrola * v * v + 0.3 * math.sin(v * 5 - t * 22 + j)
                eixo.append((r * math.cos(aa), r * math.sin(aa) - 0.3 * tt * v))
            esq, dir_ = [], []
            for m in range(14):
                x1, y1 = eixo[max(0, m - 1)]
                x2, y2 = eixo[min(13, m + 1)]
                dx, dy = x2 - x1, y2 - y1
                nn = math.hypot(dx, dy) or 1
                w = 0.04 * (1 - m / 13) ** 0.9 * (1 - 0.5 * tt) + 0.003
                esq.append((eixo[m][0] - dy / nn * w, eixo[m][1] + dx / nn * w))
                dir_.append((eixo[m][0] + dy / nn * w, eixo[m][1] - dx / nn * w))
            formas.append((esq + dir_[::-1], 1.0))
        Cf = np.minimum(T.polys(formas, 0.012), 1.0)
        caudas = Cf * apaga(t, 0.6, 0.95)
        # o fantasminha de ectoplasma que escapa do alvo e sobe ondulando
        sobe = rel(t, bate + 0.1, 1.0)
        fa = back(rel(t, bate + 0.1, bate + 0.3), 1.6) * apaga(t, 0.7, 1.0)
        Fg = T.zero()
        if fa > 0.02:
            fx, fy, fr = 0.12 + 0.06 * math.sin(sobe * 7), -0.2 - 0.4 * ease_out(sobe, 1.5), 0.15 * fa
            corpo_f = _elipse(fx, fy, fr, fr, 24, a0=math.pi, a1=TAU)
            for m in range(13):
                v = m / 12
                corpo_f.append((fx + fr - 2 * fr * v, fy + fr * 1.15 + 0.045 * fa * math.sin(v * TAU * 1.5 + t * 30)))
            Fc, Fb = _solido(T, [(corpo_f, 1.0)], 0.004, 0.02)
            olhos = T.gauss(fx - fr * 0.35, fy - fr * 0.05, fr * 0.13, fr * 0.2) + T.gauss(fx + fr * 0.35, fy - fr * 0.05, fr * 0.13, fr * 0.2)
            Fg = (Fc * 0.7 + Fb * 1.3) * (1 - np.minimum(olhos * 1.5, 1))
        G += g + anel * 1.1 + caudas * 1.0 + T.blur(caudas, 0.04) * 1.0 + T.glow(Fg, 1.0, 0.7, 0.03)
        H += h + anel * 0.4 + caudas * 0.25 + Fg * 0.35
    return G, H


# ------------------------------------------------------------------ Coringa: Flor de lapela
def _flor(cx, cy, r, giro):
    petalas = []
    for j in range(6):
        a = giro + TAU * j / 6
        px, py = cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62
        petalas.append(_gira([(x - px, y - py) for x, y in _elipse(px, py, r * 0.5, r * 0.32, 18)], a, px, py))
    return petalas


def flor_de_lapela(T, t, rng):
    """Flor de lapela do Coringa: a florzinha aparece, incha e esguicha um jato em arco
    que acerta o alvo; o líquido respinga, chia e borbulha (bolhas e fumacinha subindo)."""
    G, H = vazio(T)
    fx, fy = -0.62, 0.12
    abre = back(rel(t, 0.0, 0.12), 2.0)
    incha = 1 + 0.15 * pulso(t, 0.08, 0.2)
    vivo_f = apaga(t, 0.5, 0.75)
    r = 0.22 * abre * incha + 0.005
    pet = _flor(fx, fy, r, 0.3 + t * 2)
    P, Pb = _solido(T, [(p, 1.0) for p in pet], 0.003, 0.018)
    miolo = T.gauss(fx, fy, r * 0.28, r * 0.28)
    caule = T.polyline([(fx - 0.02, fy + r * 0.5), (fx - 0.06, fy + 0.34), (fx - 0.14, fy + 0.48)], 0.022) * abre
    G += (P * 0.45 + Pb * 1.6 + miolo * 1.2 + caule) * vivo_f
    H += (P * 0.6 + miolo * 1.4) * vivo_f
    # o jato em arco
    p0, p1, p2 = (fx + 0.02, fy - 0.02), (-0.32, -0.42), (0.0, 0.0)
    cab = ease_out(rel(t, 0.12, 0.28), 1.4)
    cau = ease_in(rel(t, 0.36, 0.55), 1.3)
    if cab - cau > 0.02:
        pts = [_bezier(p0, p1, p2, cau + (cab - cau) * j / 24) for j in range(25)]
        segs = [(pts[j][0], pts[j][1], pts[j + 1][0], pts[j + 1][1], 1) for j in range(24)]
        J = T.blur(T.tapered(segs, 0.05), 0.006)
        gotas = []
        sub = np.random.default_rng(33)
        for j in range(10):
            v = cau + (cab - cau) * sub.uniform(0, 1)
            x, y = _bezier(p0, p1, p2, v)
            gotas.append((x + sub.uniform(-0.04, 0.04), y + sub.uniform(-0.03, 0.05), sub.uniform(0.5, 1)))
        Gt = T.splats(gotas, 0.014)
        G += J * 1.4 + T.blur(J, 0.025) * 0.8 + Gt * 1.6
        H += J * 0.7 + Gt * 0.6
    bate = 0.28
    if t >= bate:
        k = pulso(t, bate, 0.55)
        respingo = T.gauss(0.02, 0.02, 0.12 + 0.05 * k, 0.1) * k * 1.6
        # gotas em leque espirrando do contato
        gs = []
        sub = np.random.default_rng(41)
        for j in range(7):
            a = -math.pi * 0.85 + math.pi * 1.1 * (j + 0.5) / 7 + sub.uniform(-0.1, 0.1)
            d = 0.12 + 0.42 * ease_out(rel(t, bate, 0.65), 2) * sub.uniform(0.7, 1)
            gy = 0.35 * rel(t, bate, 0.75) ** 2
            rg = 0.035 * (1 - rel(t, 0.5, 0.75))
            if rg > 0.008:
                gs.append((_gota(math.cos(a) * d, math.sin(a) * d + gy, rg, a + math.pi + 0.3 * rel(t, bate, 0.75)), 1.0))
        Gs = T.polys(gs, 0.004) if gs else T.zero()
        # bolhas que borbulham e sobem chiando
        bol = T.zero()
        sub = np.random.default_rng(47)
        for j in range(8):
            t0 = bate + 0.05 + 0.06 * j
            x0 = sub.uniform(-0.32, 0.32)
            y0 = sub.uniform(-0.05, 0.15)
            r0 = 0.035 + 0.04 * sub.uniform(0, 1)
            vida = 0.4 + 0.15 * sub.uniform(0, 1)
            if t < t0:
                continue
            uu = rel(t, t0, t0 + vida)
            if uu >= 1:
                continue
            x = x0 + 0.04 * math.sin(uu * 10 + j)
            y = y0 - 0.5 * uu
            rr = r0 * back(min(1, uu * 4), 2.0)
            estoura = uu > 0.85
            bol += T.ring(rr * (1.4 if estoura else 1), 0.012, x, y) * (0.4 if estoura else 1.0)
            if not estoura:
                bol += T.gauss(x - rr * 0.35, y - rr * 0.35, 0.01, 0.01) * 0.8
        bol *= apaga(t, 0.85, 1)
        fumo = T.zero()
        for j in range(3):
            t0 = bate + 0.1 * j
            if t > t0:
                uu = rel(t, t0, t0 + 0.6)
                fumo += T.gauss(-0.15 + 0.15 * j + 0.05 * math.sin(uu * 6), -0.05 - 0.4 * uu, 0.07 + 0.06 * uu, 0.06 + 0.04 * uu) * (1 - uu) ** 1.3 * 0.5
        G += respingo + Gs * 1.5 + T.blur(Gs, 0.02) * 0.6 + T.glow(bol, 1.4, 0.7, 0.015) + fumo
        H += respingo * 0.6 + Gs * 0.6 + bol * 0.6
    return G, H


# ------------------------------------------------------------------ Arlequina: Taco de beisebol
def _taco(px, py, ang, L=0.8):
    """Taco de beisebol saindo da mão (px, py): pomo, cabo fino e a ponta grossa arredondada."""
    perfil = []
    for j in range(25):
        u = j / 24
        if u < 0.05:
            w = 0.042
        elif u < 0.38:
            w = 0.026
        else:
            w = 0.026 + 0.05 * float(smooth(u, 0.38, 0.88))
        perfil.append((u * L, w))
    cima = [(x, -w) for x, w in perfil]
    ponta = [(L + 0.076 * math.sin(a), -0.076 * math.cos(a)) for a in np.linspace(0.3, math.pi - 0.3, 8)]
    baixo = [(x, w) for x, w in perfil[::-1]]
    return _gira(cima + ponta + baixo, ang, px, py)


def taco_de_beisebol(T, t, rng):
    """Taco de beisebol da Arlequina: o taco gira por cima num arco com rastro e acerta o
    alvo de lado — CRACK em estrela, estrelinhas e um coraçãozinho que sobe."""
    G, H = vazio(T)
    mx, my = -0.66, 0.22
    a0, a1 = -3.6, -0.05
    bate = 0.26
    L = 0.8
    if t < bate:
        ang = a0 + (a1 - a0) * ease_in(rel(t, 0.0, bate), 1.6)
    else:
        tt = t - bate
        ang = a1 - 0.28 * math.sin(min(math.pi, tt * 9)) * math.exp(-tt * 3) - 0.6 * ease_in(rel(t, 0.5, 0.8), 1.5)
    vivo = 1 - rel(t, 0.55, 0.8)
    C, Cb = _solido(T, [(_taco(mx, my, ang, L), 1.0)], 0.003, 0.022)
    G += (C * 0.5 + Cb * 1.6) * vivo
    H += C * 0.75 * vivo
    # rastro do giro: faixa curva atrás da ponta e cópias fantasmas
    if 0.04 < t < bate + 0.1:
        tr = 1 - rel(t, bate, bate + 0.1)
        span = min(1.6, ang - a0)
        R = T.arc_band(L * 0.82, 0.07, ang - span, ang, cx=mx, cy=my, taper=1.2) * tr
        fantasmas = T.zero()
        for j in range(1, 4):
            aj = ang - 0.32 * j
            if aj > a0:
                fantasmas += T.polys([(_taco(mx, my, aj, L), 1.0)], 0.012) * (0.4 / j)
        G += R * 1.3 + T.blur(R, 0.03) * 0.6 + fantasmas * tr
        H += R * 0.5 + fantasmas * 0.2 * tr
    if t >= bate:
        cx, cy = mx + math.cos(a1) * L * 0.85, my + math.sin(a1) * L * 0.85
        cheio, borda = _estouro(T, t, bate, 0.6, cx + 0.06, cy - 0.04, 0.36, 9, 0.45, 19)
        fora = 1 - C * 0.85 * vivo
        g, h = _clarao(T, pulso(t, bate, 0.5), cx, cy, 0.14, 0.55)
        Ln = _linhas_de_acao(T, t, bate, 0.55, cx + 0.06, cy - 0.04, 0.38, 0.15, 9, 0.0, 0.016, -1.9, 1.5)
        E = _estrelinhas(T, t, bate + 0.03, cx + 0.05, cy - 0.1, 4, 0.085, 0.55, 23, -2.6, -0.2)
        # o coraçãozinho: pula do contato, sobe balançando e some
        hc = back(rel(t, bate + 0.06, bate + 0.24), 2.2)
        uu = rel(t, bate + 0.06, 1.0)
        Co = T.zero()
        if hc > 0.01:
            hx, hy = 0.12 + 0.05 * math.sin(uu * 9), -0.42 - 0.3 * uu
            Cc, Ccb = _solido(T, [(_coracao(hx, hy, 0.12 * hc, 0.2 * math.sin(uu * 9)), 1.0)], 0.003, 0.02)
            Co = (Cc * 0.6 + Ccb * 1.4) * apaga(t, 0.82, 1)
        G += (cheio * 0.4 + borda * 1.5) * fora + g * fora + Ln * 1.1 + T.glow(E, 1.3, 0.9, 0.02) + T.glow(Co, 1.2, 0.6, 0.02)
        H += (cheio * 0.8 + borda * 0.4) * fora + h * fora + Ln * 0.5 + E * 0.9 + Co * 0.55
    return G, H


# ------------------------------------------------------------------ Capitão Planeta: Raio de Gaia
def raio_de_gaia(T, t, rng):
    """Raio de Gaia: os cinco pontos de luz (terra, fogo, vento, água, coração) acendem num
    pentágono, se unem e disparam um raio só, trançado pelos cinco fios; no alvo abre um
    planeta de luz (meridianos girando) com clarão limpo."""
    G, H = vazio(T)
    ox, oy = -0.7, 0.0
    junta = ease_in(rel(t, 0.12, 0.26), 1.4)
    rp = 0.2 * (1 - junta) + 0.02
    pts5 = []
    pontos = T.zero()
    for j in range(5):
        a = -math.pi / 2 + TAU * j / 5
        x, y = ox + math.cos(a) * rp, oy + math.sin(a) * rp
        pts5.append((x, y))
        ac = (0.35 + 0.65 * janela(t, 0.02 * j, 0.02 * j + 0.04)) * (1 - rel(t, 0.3, 0.45))
        pontos += (T.gauss(x, y, 0.035, 0.035) * 1.6 + T.flare(x, y, 0.28, 0.0, 0.02) * 0.9) * ac
    une = janela(t, 0.08, 0.14) * (1 - rel(t, 0.26, 0.36))
    laco = T.polyline(pts5 + [pts5[0]], 0.012) * une
    G += pontos * 1.2 + laco * 1.2
    H += pontos * 0.9 + laco * 0.6
    # o raio trançado
    cab = ox + (0.0 - ox) * ease_out(rel(t, 0.18, 0.32), 1.6)
    cau = ox + (0.0 - ox) * ease_in(rel(t, 0.5, 0.68), 1.4)
    if cab - cau > 0.02:
        nucleo = [(cau + (cab - cau) * j / 30, 0.0) for j in range(31)]
        larg = 0.075 * (1 - 0.5 * rel(t, 0.4, 0.68))
        R = T.polyline(nucleo, larg)
        Rc = T.polyline(nucleo, larg * 0.4)
        fios = T.zero()
        for s in range(5):
            pts = []
            for j in range(31):
                x = cau + (cab - cau) * j / 30
                pts.append((x, 0.07 * math.sin((x - ox) * 11 - t * 30 + s * TAU / 5)))
            fios += T.polyline(pts, 0.012)
        G += T.glow(R, 1.1, 1.3, 0.04) + fios * 1.2
        H += Rc * 1.4 + R * 0.4 + fios * 0.5
    bate = 0.3
    if t >= bate:
        k = pulso(t, bate, 0.65)
        g, h = _clarao(T, k, 0.0, 0.0, 0.2, 0.9, 0.0)
        s = back(rel(t, bate, bate + 0.16), 1.8) * apaga(t, 0.65, 0.92)
        R0 = 0.34 * s + 0.005
        globo = T.ring(R0, 0.028)
        giro = (t - bate) * 9
        mer = T.zero()
        for j in range(3):
            fase = giro + j * math.pi / 3
            mer += T.polyline(_elipse(0, 0, abs(math.cos(fase)) * R0 + 0.02, R0, 40), 0.014)
        eq = T.polyline(_elipse(0, 0, R0, R0 * 0.28, 40), 0.016)
        lat = T.polyline(_elipse(0, -R0 * 0.55, R0 * 0.83, R0 * 0.2, 40), 0.012) + T.polyline(_elipse(0, R0 * 0.55, R0 * 0.83, R0 * 0.2, 40), 0.012)
        dentro = T.gauss(0, 0, R0 * 0.75 + 0.01, R0 * 0.75 + 0.01)
        P_ = (globo * 1.4 + (mer + eq + lat) * 0.9) * min(1.0, s * 5)
        anel = T.ring(0.15 + 0.7 * ease_out(rel(t, bate, 0.85), 2.2), 0.03) * pulso(t, bate, 0.9)
        # os cinco pontos reaparecem girando em volta do planeta
        cinco = T.zero()
        for j in range(5):
            a = -math.pi / 2 + TAU * j / 5 + (t - bate) * 5
            cinco += T.gauss(math.cos(a) * (R0 + 0.12), math.sin(a) * (R0 + 0.12), 0.03, 0.03)
        cinco *= janela(t, bate + 0.08, bate + 0.16) * apaga(t, 0.7, 0.92) * 1.6
        G += g + P_ * 1.1 + T.blur(P_, 0.03) * 0.6 + dentro * 0.5 * s + anel + cinco * 1.2
        H += h + P_ * 0.55 + anel * 0.4 + cinco * 0.9
    return G, H


# ------------------------------------------------------------------ Scooby / Coragem: Mordida de desenho
def _arcada(cy, dir_, n=4, larg=1.08, curva=0.2):
    """Uma fileira de dentes grandes de desenho (quadradões de ponta redonda) presos numa gengiva curva.
    dir_ = +1 dentes para baixo (arcada de cima), -1 para cima (arcada de baixo)."""
    dentes = []
    w = larg / n
    desloca = w * 0.25 if dir_ < 0 else -w * 0.25
    for j in range(n):
        x = -larg / 2 + w * (j + 0.5) + desloca
        base = cy + dir_ * curva * (2 * x / larg) ** 2
        h = 0.27 * (0.62 if j in (0, n - 1) else 1.0)
        meia = w * 0.42
        pts = [(x - meia, base), (x + meia, base)]
        for m in range(9):
            a = math.pi * m / 8
            pts.append((x + meia * math.cos(a), base + dir_ * (h - meia + meia * math.sin(a))))
        dentes.append(pts)
    gengiva = []
    for j in range(25):
        x = -larg / 2 - 0.06 + (larg + 0.12) * j / 24
        gengiva.append((x, cy + dir_ * curva * (2 * x / larg) ** 2 - dir_ * 0.04))
    return dentes, gengiva


def mordida_cartoon(T, t, rng):
    """Mordida de desenho (Scooby e Coragem): duas arcadas de dentões abrem e fecham com um
    CHOMP no alvo, as mandíbulas tremem, gotas de suor pulam e ficam as marquinhas da mordida."""
    G, H = vazio(T)
    bate = 0.26
    if t < bate:
        abre = 0.03 + 0.24 * (1 - ease_in(rel(t, 0.0, bate), 2.2))
        aparece = 0.6 + 0.4 * janela(t, 0.0, 0.06)
    else:
        tt = t - bate
        abre = 0.03 - 0.03 * math.exp(-tt * 10) * abs(math.cos(tt * 45)) + 0.16 * ease_out(rel(t, 0.5, 0.7), 2)
        aparece = 1.0
    vivo = aparece * (1 - rel(t, 0.55, 0.72))
    esc = 1 + 0.08 * pulso(t, bate, bate + 0.12)
    cima, g1 = _arcada(-0.27 - abre, 1)
    baixo, g2 = _arcada(0.27 + abre, -1)
    cima = [[(x * esc, y) for x, y in d] for d in cima]
    baixo = [[(x * esc, y) for x, y in d] for d in baixo]
    D, Db = _solido(T, [(d, 1.0) for d in cima + baixo], 0.003, 0.02)
    Gg = T.polyline(g1, 0.045) + T.polyline(g2, 0.045)
    G += (D * 0.5 + Db * 1.8 + Gg * 1.3 + T.blur(Gg, 0.03) * 0.5) * vivo
    H += (D * 0.85 + Gg * 0.3) * vivo
    if t >= bate:
        k = pulso(t, bate, 0.5)
        g, h = _clarao(T, k, 0.0, 0.0, 0.16, 0.6, 0.0)
        # marquinhas de impacto: tracinhos em três grupos em volta
        marc = []
        for cx, cy, a in ((-0.62, -0.3, -2.6), (0.62, -0.3, -0.55), (0.0, -0.6, -math.pi / 2)):
            for d in (-0.3, 0.0, 0.3):
                aa = a + d
                r0 = 0.06 + 0.08 * ease_out(rel(t, bate, 0.5), 2)
                marc.append((cx + math.cos(aa) * r0, cy + math.sin(aa) * r0, cx + math.cos(aa) * (r0 + 0.12), cy + math.sin(aa) * (r0 + 0.12), 1))
        M = T.lines(marc, 0.022, 0.002) * pulso(t, bate, 0.6)
        # gotas de suor pulando para os lados
        gotas = []
        for j, (vx, vy) in enumerate(((-0.5, -0.65), (-0.3, -0.85), (0.35, -0.8), (0.55, -0.6))):
            uu = rel(t, bate + 0.03 * j, 0.85)
            if 0 < uu < 1:
                x = vx * ease_out(uu, 1.5) * 0.9
                y = -0.2 + vy * uu * 0.9 + 0.9 * uu * uu
                ang = math.atan2(vy + 1.8 * uu, vx)
                gotas.append((_gota(x, y, 0.055 * (1 - 0.3 * uu), ang + math.pi), 1.0 - uu ** 3))
        Su, Sub = _solido(T, gotas, 0.003, 0.02) if gotas else (T.zero(), T.zero())
        # as marcas da mordida que ficam (duas fileiras de entalhes)
        fica = janela(t, 0.58, 0.68) * apaga(t, 0.8, 1)
        Ent = T.zero()
        if fica > 0:
            for fila, yy in ((1, -0.1), (-1, 0.1)):
                for j in range(4):
                    x = -0.42 + 0.24 * j + (0.0 if fila > 0 else 0.12)
                    arco = _elipse(x, yy, 0.065, 0.05, 14, a0=0.0 if fila > 0 else math.pi, a1=math.pi if fila > 0 else TAU)
                    Ent += T.polyline(arco, 0.026)
            Ent *= fica
        G += g + M * 1.2 + Su * 0.5 + Sub * 1.5 + Ent * 1.3 + T.blur(Ent, 0.02) * 0.5
        H += h + M * 0.5 + Su * 0.8 + Ent * 0.6
    return G, H


REGISTRO = [
    ("barrigada", barrigada, GRANDE, "Barrigada do Homer: a barriga amassa no alvo e balança, ondas achatadas e estrelinhas", False),
    ("estilingue", estilingue, GRANDE, "Estilingue do Bart: a pedrinha vem em arco, TOCK em estrela e estrelinhas girando", False),
    ("gadget_surpresa", gadget_surpresa, GRANDE, "Gadget surpresa: luva de boxe numa mola sai da esquerda e acerta com POW", False),
    ("raio_fantasma", raio_fantasma, GRANDE, "Raio fantasma: raio de ectoplasma com fiapos ondulando e caudas de fantasma no alvo", False),
    ("flor_de_lapela", flor_de_lapela, GRANDE, "Flor de lapela do Coringa: esguicho em arco que respinga, chia e borbulha", False),
    ("taco_de_beisebol", taco_de_beisebol, GRANDE, "Taco de beisebol da Arlequina: giro com rastro, CRACK, estrelinhas e um coração", False),
    ("raio_de_gaia", raio_de_gaia, GRANDE, "Raio de Gaia: cinco pontos de luz se unem num raio trançado que abre um planeta de luz", False),
    ("mordida_cartoon", mordida_cartoon, GRANDE, "Mordida de desenho: dentões fecham com CHOMP, gotas de suor e marquinhas", False),
]
