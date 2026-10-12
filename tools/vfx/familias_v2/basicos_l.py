"""Ataques básicos com animação própria, lote l (personagens novos).

Marceline, Robin, Luigi, Peach, Zoro, Nami, Sanji, Chopper, Nero, L, Morty, Tails, Knuckles, Velma e Fred:
a mordida que chupa o vermelho, o bastão retrátil, o pulo do Luigi, o tapa real, os três cortes do
Santoryu, a nuvenzinha do Clima-Tact, o chute do Sanji com a fumaça, a chifrada do Chopper, os dois tiros
juntos da Blue Rose, o chute de capoeira de ponta-cabeça, o tiro tremido do Morty, as duas caudas
girando, a luva de espinhos, o livro na cabeça e a ombrada com a rede da armadilha.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas


def _estrelinhas(T, t, t0, dur, cx, cy, n, r, seed):
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    q = np.random.default_rng(seed)
    shapes = []
    for k in range(n):
        a = TAU * k / n + q.uniform(-0.3, 0.3) + u * 2
        d = r * (0.4 + 0.6 * ease_out(u, 2))
        shapes.append((estrela(cx + d * math.cos(a), cy + d * 0.7 * math.sin(a), 0.045, u * 4, 5, 0.45), 1 - u))
    return T.polys(shapes)


# ================================================================== Marceline
def mordida_vampira(T, t, rng):
    """A mordiscada da Marceline: as duas presas descem e a mandíbula fecha no rival (os dentes de cima e de
    baixo), e o vermelho é chupado dele em fios que voltam para a esquerda."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    fecha = ease_in(rel(t, 0.05, 0.3), 2)
    if t < 0.55:
        abre = 0.4 * (1 - fecha)
        shapes = []
        for lado in (-1, 1):
            x = 0.18 * lado
            shapes.append(([(x - 0.08, -0.1 - abre), (x + 0.08, -0.1 - abre), (x, 0.2 - abre)], 1.0))
            shapes.append(([(x - 0.05, 0.14 + abre), (x + 0.05, 0.14 + abre), (x, -0.02 + abre)], 0.7))
        D = T.polys(shapes)
        G += (D * 0.7 + _borda(T, D, 0.005) * 1.2) * (1 - rel(t, 0.4, 0.55))
        G += T.arc_band(0.42, 0.025, 0.4, math.pi - 0.4, squash=0.5, cx=0, cy=-0.2 - abre) * 0.8 * (1 - rel(t, 0.4, 0.55))
    g, h = _estouro(T, t, 0.28, 0.55, 0, 0, 0.25, 6, 3, 0.014)
    G += g * 0.7
    H += h * 0.7
    chupa = rel(t, 0.35, 0.95)
    if 0 < chupa < 1:
        pts = []
        for k in range(3):
            for j in range(18):
                u = (chupa * 1.4 + j / 18 * 0.5) % 1
                x = -0.9 * u
                y = (k - 1) * 0.1 * (1 - u) + 0.08 * math.sin(TAU * u * 2 + k)
                pts.append((x, y, math.sin(math.pi * u) * (1 - chupa * 0.5)))
        G += T.splats(pts, 0.018) * 1.3
    return G * env, H * env


# ================================================================== Robin
def bastao_do_robin(T, t, rng):
    """O bastão retrátil do Robin: o bastão gira na frente e estica de uma vez (os gomos saindo um do outro),
    estocando o rival com a ponta."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    gira = rel(t, 0.0, 0.25)
    estica = ease_out(rel(t, 0.25, 0.4), 3)
    if t < 0.6:
        some = 1 - rel(t, 0.45, 0.6)
        if estica <= 0:
            ang = TAU * 2 * gira
            cx, cy = -0.5, 0.0
            G += T.lines([(cx - 0.35 * math.cos(ang), cy - 0.35 * math.sin(ang), cx + 0.35 * math.cos(ang), cy + 0.35 * math.sin(ang), 1.0)], 0.05) * 1.2
            G += T.ring(0.35, 0.02, cx, cy) * 0.6 * gira
        else:
            x0 = -0.95
            comp = 0.4 + 0.75 * estica
            segs = []
            for k in range(3):
                a = x0 + comp * k / 3
                b = x0 + comp * (k + 1) / 3
                segs.append((a, 0.0, b, 0.0, 1.0))
            G += T.lines(segs, 0.06) * some * 1.1
            G += T.lines([(x0 + comp * k / 3, -0.04, x0 + comp * k / 3, 0.04, 1.0) for k in range(1, 3)], 0.016) * some * 1.3
            H += T.gauss(x0 + comp, 0.0, 0.03) * some * 1.3
    g, h = _estouro(T, t, 0.35, 0.65, 0.1, 0, 0.3, 8, 5)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Luigi
def pulo_do_luigi(T, t, rng):
    """O pulo do Luigi: a poeira no chão do impulso, o rastro alto em arco (com as pernas batendo, as voltinhas
    do pulo dele), e a pisada que desce em cima do rival com as estrelinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    poeira = rel(t, 0.0, 0.4)
    if 0 < poeira < 1:
        q = np.random.default_rng(4)
        pts = [(-0.6 + q.uniform(-0.15, 0.15) * (1 + poeira), 0.6 - 0.1 * poeira * q.uniform(), (1 - poeira) * 0.7) for _ in range(10)]
        G += T.splats(pts, 0.05) * 0.7
    voa = rel(t, 0.05, 0.45)
    if 0 < voa and t < 0.6:
        pts = []
        for j in range(30):
            u = j / 29 * min(voa, 1)
            x = -0.6 + 0.6 * u
            y = 0.6 - 1.4 * math.sin(math.pi * u * 0.9) + 0.5 * u * u
            pts.append((x + 0.04 * math.sin(u * 30), y))
        G += T.polyline(pts, 0.016) * (1 - rel(t, 0.45, 0.6)) * 1.1
        if voa < 1:
            sx, sy = pts[-1]
            for lado in (-1, 1):
                G += T.gauss(sx + 0.05 * lado, sy + 0.08 + 0.03 * math.sin(t * 60 + lado), 0.035, 0.022) * 1.3
    g, h = _estouro(T, t, 0.45, 0.75, 0, -0.1, 0.32, 8, 7)
    G += g
    H += h
    G += _estrelinhas(T, t, 0.48, 0.45, 0, -0.25, 5, 0.35, 8) * 1.1
    return G * env, H * env


# ================================================================== Peach
def _mao_aberta(cx, cy, s, ang):
    pts = [(-0.12, 0.08), (-0.12, -0.04), (-0.08, -0.06), (-0.06, -0.2), (-0.03, -0.2), (-0.02, -0.07), (0.0, -0.24),
           (0.03, -0.24), (0.04, -0.07), (0.06, -0.22), (0.09, -0.22), (0.09, -0.05), (0.12, -0.16), (0.15, -0.15),
           (0.12, 0.04), (0.06, 0.12), (-0.06, 0.12)]
    return _gira([(x * s, y * s) for x, y in pts], ang, cx, cy)


def tapa_real(T, t, rng):
    """O tapa real da Peach: a mão enluvada entra varrendo de lado, estala no rival (o clarão e a marca da mão
    que fica) e solta os brilhinhos de princesa."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.45:
        x = -0.9 + 0.9 * vem
        M = T.polys([(_mao_aberta(x, 0.0, 1.6, 0.25 - 0.4 * vem), 1.0)])
        G += M * 0.5 + _borda(T, M, 0.007) * 1.4
        G += T.tapered([(x - 0.5, 0.05, x - 0.1, 0.0, 1.0), (x - 0.45, -0.15, x - 0.1, -0.15, 0.7)], 0.025) * 0.8 * (vem < 1)
    estalo = rel(t, 0.25, 0.55)
    if 0 < estalo < 1:
        H += T.flare(0, 0, 0.5 * (1 - estalo), 0.3, 0.014) * (1 - estalo) * 1.4
        G += T.ring(0.08 + 0.3 * ease_out(estalo, 3), 0.025, 0, 0) * (1 - estalo) * 1.2
    marca = pulso(t, 0.3, 0.9)
    if marca > 0:
        M = T.polys([(_mao_aberta(0.05, 0.0, 1.2, 0.0), 1.0)])
        G += _borda(T, M, 0.006) * marca * 0.9
    G += _estrelinhas(T, t, 0.3, 0.6, 0, 0, 6, 0.45, 12) * 1.0
    return G * env, H * env


# ================================================================== Zoro
def corte_santoryu(T, t, rng):
    """O corte do Zoro em estilo de três espadas: as três lâminas cortam juntas, uma em cada ângulo (duas nas
    mãos e a da boca no meio), deixando três riscos paralelos que brilham e somem."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    for k, (dy, t0) in enumerate(((-0.18, 0.08), (0.0, 0.1), (0.18, 0.12))):
        p = ease_out(rel(t, t0, t0 + 0.12), 3)
        ini = rel(t, t0 + 0.15, t0 + 0.45)
        if p > 0 and ini < 1:
            L = T.polys([(lamina(-0.65, dy - 0.35, 0.65, dy + 0.35, 0.04, prog=p, inicio=ini), 1.0)])
            G += L * 1.4 + T.blur(L, 0.015) * 0.5
            H += L * 0.6
    H += T.flare(0, 0, 0.55 * pulso(t, 0.15, 0.45) + 0.01, 0.5, 0.012) * pulso(t, 0.15, 0.45)
    g, h = _estouro(T, t, 0.2, 0.5, 0, 0, 0.3, 8, 3, 0.014)
    G += g * 0.6
    H += h * 0.4
    return G * env, H * env


# ================================================================== Nami
def clima_tact(T, t, rng):
    """O Clima-Tact da Nami: a bolinha de nuvem sai do bastão, flutua até ficar em cima do rival, escurece e
    solta o raio que desce nele."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = ease_out(rel(t, 0.0, 0.35), 2)
    if t < 0.85:
        x = -0.75 + 0.75 * voa
        y = -0.1 - 0.45 * voa
        cresce = 0.5 + 0.5 * voa
        q = np.random.default_rng(3)
        pts = [(x + 0.18 * cresce * math.cos(a), y + 0.07 * cresce * math.sin(a), 1.0) for a in np.linspace(0, TAU, 9, endpoint=False)]
        pts += [(x + q.uniform(-0.1, 0.1) * cresce, y - 0.03, 1.0) for _ in range(4)]
        N = T.splats(pts, 0.06 * cresce)
        G += (np.clip(N, 0, 1) * 0.4 + _borda(T, np.clip(N, 0, 1), 0.02) * 1.2) * (1 - rel(t, 0.7, 0.85))
    raio = pulso(t, 0.38, 0.6)
    if raio > 0:
        q = np.random.default_rng(int(t * 40) % 6 + 2)
        R = T.polyline(jagged(q, 0.0, -0.5, 0.0, 0.0, 6, 0.25), 0.02)
        G += R * raio * 1.4 + T.blur(R, 0.02) * raio * 0.6
        H += R * raio
    g, h = _estouro(T, t, 0.4, 0.7, 0, 0, 0.3, 8, 6)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Sanji
def _sapato(cx, cy, s, ang):
    pts = [(-0.1, -0.04), (0.08, -0.04), (0.14, 0.0), (0.12, 0.04), (-0.1, 0.04)]
    return _gira([(x * s, y * s) for x, y in pts], ang, cx, cy)


def chute_de_sanji(T, t, rng):
    """O chute do Sanji: a perna varre num arco largo e rápido (a meia-lua com o sapato na ponta), acerta em
    cheio com o clarão, e a fumaça do cigarro fica fazendo uma voltinha."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    gira = ease_out(rel(t, 0.0, 0.28), 2.5)
    if gira > 0 and t < 0.5:
        some = 1 - rel(t, 0.3, 0.5)
        a1 = -2.7 + 2.9 * gira
        A = T.arc_band(0.55, 0.07, -2.7, a1, cx=-0.35, cy=0.15, crescente=True)
        G += (A * 1.3 + T.blur(A, 0.02) * 0.5) * some
        sx, sy = -0.35 + 0.55 * math.cos(a1), 0.15 + 0.55 * math.sin(a1)
        S = T.polys([(_sapato(sx, sy, 1.6, a1 + math.pi / 2), 1.0)])
        G += S * 1.2 * some
    g, h = _estouro(T, t, 0.25, 0.55, 0.15, 0.0, 0.35, 10, 4)
    G += g
    H += h
    fumo = rel(t, 0.15, 1.0)
    if 0 < fumo < 1:
        pts = []
        for j in range(30):
            u = j / 29
            a = TAU * 1.3 * u + t * 2
            pts.append((-0.6 + 0.08 * math.cos(a) + 0.1 * u, -0.25 - 0.4 * u * fumo + 0.06 * math.sin(a), (1 - u) * (1 - fumo) * 0.8))
        G += T.splats(pts, 0.025) * 0.9
    return G * env, H * env


# ================================================================== Chopper
def _galhada(cx, cy, s):
    """Os chifres do Chopper: dois galhos com as pontas abertas."""
    segs = []
    for lado in (-1, 1):
        b = (cx, cy + 0.04 * lado * s)
        m = (cx + 0.18 * s, cy + 0.14 * lado * s)
        segs += [(b[0], b[1], m[0], m[1], 1.0), (m[0], m[1], m[0] + 0.12 * s, m[1] + 0.1 * lado * s, 1.0),
                 (m[0], m[1], m[0] + 0.15 * s, m[1] - 0.02 * lado * s, 1.0), (cx + 0.09 * s, cy + 0.09 * lado * s, cx + 0.16 * s, cy + 0.03 * lado * s, 0.8)]
    return segs


def chifrada_do_chopper(T, t, rng):
    """A chifrada do Chopper: a galhada vem correndo de cabeça baixa da esquerda (com o pó dos cascos), crava no
    rival e o empurra."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.3), 2)
    if t < 0.5:
        x = -0.85 + 0.75 * vem
        G += T.lines(_galhada(x, 0.0, 1.8), 0.026) * 1.3 * (1 - rel(t, 0.38, 0.5))
        G += T.gauss(x - 0.05, 0.0, 0.06) * 0.6
        q = np.random.default_rng(int(t * 30) % 5)
        pts = [(x - 0.2 - q.uniform(0, 0.3), 0.35 + q.uniform(-0.05, 0.05), 0.5) for _ in range(6)]
        G += T.splats(pts, 0.04) * 0.6
    g, h = _estouro(T, t, 0.28, 0.6, 0.0, 0.0, 0.35, 9, 6)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Nero
def blue_rose(T, t, rng):
    """A Blue Rose do Nero: o revólver de dois canos dispara as duas balas juntas (o clarão duplo, os dois traços
    lado a lado), e os dois furos acertam o rival quase no mesmo lugar."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    cano = -0.9
    clarao = pulso(t, 0.0, 0.12)
    for dy in (-0.035, 0.035):
        H += T.flare(cano, dy, 0.3 * clarao + 0.01, 0, 0.012) * clarao * 1.3
    voa = rel(t, 0.04, 0.16)
    if voa > 0 and t < 0.4:
        x = cano + 0.9 * voa
        G += T.tapered([(cano, -0.035, x, -0.035, 1.0), (cano, 0.035, x, 0.035, 1.0)], 0.014) * (1 - rel(t, 0.18, 0.4)) * 1.3
    bate = rel(t, 0.15, 0.5)
    if 0 < bate < 1:
        for k, (dx, dy) in enumerate(((0.0, -0.04), (0.03, 0.04))):
            H += T.gauss(dx, dy, 0.03) * (1 - bate) ** 2 * 1.8
            G += T.ring(0.03 + 0.12 * ease_out(bate, 3), 0.01, dx, dy) * (1 - bate) * 1.3
    g, h = _estouro(T, t, 0.16, 0.5, 0, 0, 0.25, 8, 9, 0.014)
    G += g * 0.8
    H += h * 0.6
    fum = rel(t, 0.05, 0.6)
    if 0 < fum < 1:
        pts = [(cano + 0.1 + 0.2 * fum, -0.1 * fum + 0.03 * k, (1 - fum) * 0.5) for k in range(4)]
        G += T.splats(pts, 0.05) * 0.6
    return G * env, H * env


# ================================================================== L
def chute_capoeira(T, t, rng):
    """O chute de capoeira do L: de ponta-cabeça, a perna gira num círculo inteiro (o rastro redondo, com o pé
    aceso na ponta) e acerta o rival de cima."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    gira = ease_out(rel(t, 0.0, 0.35), 1.8)
    if gira > 0 and t < 0.55:
        some = 1 - rel(t, 0.38, 0.55)
        cx, cy = -0.3, 0.1
        a1 = math.pi / 2 + TAU * 0.9 * gira
        A = T.arc_band(0.42, 0.06, a1 - 2.2, a1, cx=cx, cy=cy, taper=0.6)
        G += (A * 1.2 + T.blur(A, 0.02) * 0.4) * some
        px, py = cx + 0.42 * math.cos(a1), cy + 0.42 * math.sin(a1)
        H += T.gauss(px, py, 0.035) * 1.4 * some
        G += T.lines([(cx - 0.05, cy + 0.1, cx + 0.05, cy + 0.1, 1.0)], 0.02) * 0.6 * some
    g, h = _estouro(T, t, 0.33, 0.62, 0.05, -0.1, 0.32, 9, 10)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Morty
def tiro_nervoso(T, t, rng):
    """O tiro nervoso do Morty: a arma treme (o brilho no cano sacudindo), o primeiro raio sai torto e erra (passa
    por cima), o segundo acerta de raspão no rival, e as gotas de suor pulam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    treme = 0.03 * math.sin(t * 90)
    cano = (-0.85, 0.05 + treme)
    H += T.gauss(cano[0], cano[1], 0.03) * pulso(t, 0.0, 0.5) * 1.3
    erra = rel(t, 0.08, 0.3)
    if 0 < erra < 1:
        x = cano[0] + 1.9 * erra
        y = cano[1] - 0.6 * erra
        G += T.tapered([(x - 0.3, y + 0.09, x, y, 1.0)], 0.02) * 1.2
    acerta = rel(t, 0.3, 0.45)
    if 0 < acerta and t < 0.6:
        x = cano[0] + 0.85 * acerta
        y = cano[1] * (1 - acerta) + 0.05 * math.sin(acerta * 20)
        G += T.tapered([(x - 0.3, y, x, y, 1.0)], 0.02) * 1.2 * (1 - rel(t, 0.45, 0.6))
    g, h = _estouro(T, t, 0.44, 0.72, 0.05, 0.05, 0.25, 7, 11, 0.016)
    G += g
    H += h
    suor = rel(t, 0.1, 0.7)
    if 0 < suor < 1:
        for k in range(3):
            a = -2.4 + 0.4 * k
            d = 0.25 * ease_out(suor, 2)
            G += T.polys([(_folha(-0.75 + d * math.cos(a), -0.35 + d * math.sin(a) + 0.3 * suor * suor, 0.03, math.pi / 2), 1.0)]) * (1 - suor)
    return G * env, H * env


# ================================================================== Tails
def caudas_giratorias(T, t, rng):
    """As caudas do Tails: as duas caudas giram como hélice (os dois lóbulos rodando com o borrão), e ele
    chicoteia o rival com elas em dois golpes."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cx, cy = -0.35, -0.05
    vel = rel(t, 0.0, 0.6)
    if t < 0.7:
        some = 1 - rel(t, 0.55, 0.7)
        ang = TAU * 3.5 * vel
        for k in range(2):
            a = ang + math.pi * k
            for j, rr in enumerate((0.0, 0.18, 0.36)):
                G += T.polys([(lamina(cx, cy, cx + 0.38 * math.cos(a - 0.25 * j), cy + 0.38 * math.sin(a - 0.25 * j), 0.08), 1.0)]) * (1.0 if j == 0 else 0.25) * some
        G += T.ring(0.38, 0.015, cx, cy) * 0.5 * some
    for t0 in (0.3, 0.45):
        g, h = _estouro(T, t, t0, t0 + 0.25, 0.1, 0.0, 0.25, 7, int(t0 * 100))
        G += g
        H += h
    return G * env, H * env


# ================================================================== Knuckles
def punho_espinhoso(T, t, rng):
    """O soco de luva do Knuckles: o punho com os dois espinhos da luva avança, atravessa a defesa e as pedrinhas
    voam do impacto."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vai = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.45:
        x = -0.8 + 0.72 * vai
        P, nos = _punho(T, x, 0.0, 1.8)
        G += P * 0.6 + _borda(T, P, 0.007) * 1.2
        esp = [([(x + 0.12, -0.12), (x + 0.32, -0.08), (x + 0.14, -0.04)], 1.0), ([(x + 0.12, 0.04), (x + 0.32, 0.08), (x + 0.14, 0.12)], 1.0)]
        E = T.polys(esp)
        G += E * 1.3
        H += E * 0.5
        G += T.tapered([(x - 0.4, -0.1, x - 0.1, -0.1, 1.0), (x - 0.45, 0.1, x - 0.1, 0.1, 1.0)], 0.02) * 0.8
    g, h = _estouro(T, t, 0.25, 0.55, 0.05, 0, 0.38, 10, 13)
    G += g
    H += h
    pedras = rel(t, 0.27, 0.8)
    if 0 < pedras < 1:
        q = np.random.default_rng(17)
        shapes = []
        for _ in range(10):
            a = q.uniform(-1.2, 1.2)
            d = (0.15 + 0.55 * ease_out(pedras, 2)) * q.uniform(0.6, 1)
            cx, cy = d * math.cos(a), d * math.sin(a) + 0.4 * pedras ** 2
            s = 0.035 * q.uniform(0.7, 1.3)
            shapes.append((_gira([(-s, -s * 0.6), (s * 0.8, -s), (s, s * 0.7), (-s * 0.6, s)], pedras * 6 + a, cx, cy), 1 - pedras))
        G += T.polys(shapes) * 1.2
    return G * env, H * env


# ================================================================== Velma
def livro_na_cabeca(T, t, rng):
    """O livro na cabeça da Velma: o livro grosso voa girando da esquerda (a capa e a lombada), bate na cabeça
    do rival com o "tum" e as estrelinhas giram; as páginas abrem um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = rel(t, 0.0, 0.3)
    if t < 0.5:
        x = -0.85 + 0.85 * ease_in(voa, 1.4)
        y = -0.3 - 0.25 * math.sin(math.pi * voa)
        ang = TAU * 1.5 * voa
        capa = _gira([(-0.12, -0.09), (0.12, -0.09), (0.12, 0.09), (-0.12, 0.09)], ang, x, y)
        G += T.lines(_contorno(capa), 0.014) * 1.3 * (1 - rel(t, 0.38, 0.5))
        lomb = _gira([(-0.12, -0.09), (-0.12, 0.09)], ang, x, y)
        G += T.lines([(lomb[0][0], lomb[0][1], lomb[1][0], lomb[1][1], 1.0)], 0.03) * 1.2 * (1 - rel(t, 0.38, 0.5))
    abre = pulso(t, 0.3, 0.6)
    if abre > 0:
        for k in range(4):
            a = -math.pi / 2 + (k - 1.5) * 0.35 * abre
            G += T.lines([(0, -0.3, 0.2 * math.cos(a), -0.3 + 0.2 * math.sin(a), 1.0)], 0.01) * abre * 1.1
    g, h = _estouro(T, t, 0.28, 0.55, 0, -0.3, 0.25, 7, 15, 0.016)
    G += g
    H += h
    G += _estrelinhas(T, t, 0.3, 0.65, 0, -0.42, 5, 0.3, 21) * 1.2
    return G * env, H * env


# ================================================================== Fred
def ombrada(T, t, rng):
    """A ombrada do Fred: ele entra de ombro baixo da esquerda (a curva do ombro com os riscos de corrida), bate
    no rival, e a rede da armadilha cai em cima dele."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.28), 2)
    if t < 0.45:
        x = -0.85 + 0.7 * vem
        O = T.arc_band(0.18, 0.06, -1.6, 1.6, cx=x, cy=0.0, taper=0.0)
        G += O * 1.2 * (1 - rel(t, 0.32, 0.45))
        G += T.tapered([(x - 0.5, -0.12 + 0.12 * k, x - 0.15, -0.12 + 0.12 * k, 1.0) for k in range(3)], 0.018) * 0.9
    g, h = _estouro(T, t, 0.27, 0.55, 0.05, 0, 0.35, 9, 19)
    G += g
    H += h
    cai = ease_in(rel(t, 0.4, 0.62), 2)
    if cai > 0:
        y0 = -1.0 + 0.85 * cai
        segs = []
        for k in range(7):
            x = -0.45 + 0.15 * k
            segs.append((x, y0, x + 0.05 * (k - 3) * cai, y0 + 0.8, 1.0))
        for k in range(6):
            y = y0 + 0.14 * k
            segs.append((-0.45 - 0.02 * k, y, 0.45 + 0.02 * k, y, 1.0))
        G += T.lines(segs, 0.01) * 1.1 * (1 - rel(t, 0.85, 1.0))
    return G * env, H * env


REGISTRO = [
    ("mordida_vampira", mordida_vampira, GRANDE, "Básico da Marceline: as presas e o vermelho chupado", False),
    ("bastao_do_robin", bastao_do_robin, GRANDE, "Básico do Robin: o bastão gira e estica", False),
    ("pulo_do_luigi", pulo_do_luigi, GRANDE, "Básico do Luigi: o pulo alto e a pisada", False),
    ("tapa_real", tapa_real, GRANDE, "Básico da Peach: a luva, o tapa e os brilhinhos", False),
    ("corte_santoryu", corte_santoryu, GRANDE, "Básico do Zoro: os três cortes juntos", False),
    ("clima_tact", clima_tact, GRANDE, "Básico da Nami: a nuvenzinha e o raio", False),
    ("chute_de_sanji", chute_de_sanji, GRANDE, "Básico do Sanji: o chute em arco e a fumaça", False),
    ("chifrada_do_chopper", chifrada_do_chopper, GRANDE, "Básico do Chopper: a galhada correndo", False),
    ("blue_rose", blue_rose, GRANDE, "Básico do Nero: os dois tiros da Blue Rose", False),
    ("chute_capoeira", chute_capoeira, GRANDE, "Básico do L: o giro de ponta-cabeça", False),
    ("tiro_nervoso", tiro_nervoso, GRANDE, "Básico do Morty: o tiro que erra e o de raspão", False),
    ("caudas_giratorias", caudas_giratorias, GRANDE, "Básico do Tails: as duas caudas girando", False),
    ("punho_espinhoso", punho_espinhoso, GRANDE, "Básico do Knuckles: a luva de espinhos e as pedras", False),
    ("livro_na_cabeca", livro_na_cabeca, GRANDE, "Básico da Velma: o livro voando e as estrelinhas", False),
    ("ombrada", ombrada, GRANDE, "Básico do Fred: a ombrada e a rede", False),
]
