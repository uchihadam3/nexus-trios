"""Ataques básicos com animação própria, lote m (personagens novos).

Leorio, Byakuya, Kitana, Shao Kahn, Snorlax, Patrick, Flecha, Gwen, Viúva Negra, Gavião Arqueiro, Gamora,
Drax, Mulher-Aranha, Mulher-Gato e Espantalho: a maletada, o corte com as pétalas da Senbonzakura, o leque de
aço que vai e volta, a marreta do imperador, a barrigada do Snorlax caindo de cima, o tapão de estrela, a
rajada de socos supersônicos, o raio de mana em hexágonos, o chute giratório com a picada elétrica, a
flecha, a Godslayer, as duas facas, o soco bioelétrico, o chicote e as unhas e o gás do medo com os rostos.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + k * math.pi / 3), cy + r * math.sin(ang + k * math.pi / 3)) for k in range(6)]


# ================================================================== Leorio
def maletada(T, t, rng):
    """A maletada do Leorio: a maleta gira num arco pela alça e bate de lado no rival (o "tum" com as linhas),
    e uns papéis escapam voando."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    gira = ease_out(rel(t, 0.0, 0.3), 2)
    if t < 0.5:
        ang = -2.5 + 2.4 * gira
        px, py = -0.6, 0.0
        cx, cy = px + 0.55 * math.cos(ang), py + 0.55 * math.sin(ang)
        caixa = _gira([(-0.15, -0.1), (0.15, -0.1), (0.15, 0.1), (-0.15, 0.1)], ang + math.pi / 2, cx, cy)
        alca = _gira([(-0.06, -0.1), (-0.05, -0.15), (0.05, -0.15), (0.06, -0.1)], ang + math.pi / 2, cx, cy)
        C = T.polys([(caixa, 1.0)])
        G += (C * 0.5 + _borda(T, C, 0.007) * 1.3 + T.polyline(alca, 0.012) * 1.1) * (1 - rel(t, 0.38, 0.5))
        G += T.arc_band(0.55, 0.04, -2.5, ang, cx=px, cy=py, taper=0.8) * 0.5
    g, h = _estouro(T, t, 0.28, 0.58, 0, 0, 0.32, 9, 3)
    G += g
    H += h
    papel = rel(t, 0.3, 0.95)
    if 0 < papel < 1:
        q = np.random.default_rng(5)
        shapes = []
        for _ in range(5):
            a = q.uniform(-2.6, -0.5)
            d = 0.5 * ease_out(papel, 2) * q.uniform(0.5, 1)
            cx, cy = d * math.cos(a), d * math.sin(a) + 0.3 * papel ** 2
            shapes.append((_gira([(-0.05, -0.035), (0.05, -0.035), (0.05, 0.035), (-0.05, 0.035)], papel * 5 + a, cx, cy), 1 - papel))
        G += T.lines(sum((_contorno(s, w) for s, w in shapes), []), 0.008) * 1.1
    return G * env, H * env


# ================================================================== Byakuya
def senbonzakura_corte(T, t, rng):
    """O corte do Byakuya: um risco fino e elegante atravessa o rival, e dele se soltam centenas de pétalas
    afiadas que brilham e se espalham como poeira de cerejeira."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    p = ease_out(rel(t, 0.05, 0.2), 3)
    ini = rel(t, 0.22, 0.5)
    if p > 0 and ini < 1:
        L = T.polys([(lamina(-0.75, 0.3, 0.75, -0.25, 0.025, prog=p, inicio=ini), 1.0)])
        G += L * 1.5
        H += L * 0.8
    sol = rel(t, 0.15, 0.95)
    if 0 < sol < 1:
        q = np.random.default_rng(9)
        shapes = []
        brilhos = []
        for k in range(40):
            u0 = q.uniform(0, 1)
            bx, by = -0.75 + 1.5 * u0, 0.3 - 0.55 * u0
            a = q.uniform(0, TAU)
            d = 0.45 * ease_out(sol, 2) * q.uniform(0.2, 1)
            x, y = bx + d * math.cos(a), by + d * math.sin(a) + 0.15 * sol
            vida = (1 - sol) * q.uniform(0.5, 1)
            shapes.append((_folha(x, y, 0.022, a + sol * 8), vida))
            if k % 4 == 0:
                brilhos.append((x, y, vida))
        G += T.polys(shapes) * 1.2
        H += T.splats(brilhos, 0.01) * 1.2
    return G * env, H * env


# ================================================================== Kitana
def _leque(cx, cy, r, ang, abre=1.0):
    """O leque de aço aberto: o arco da lâmina e as varetas saindo do eixo."""
    segs = []
    a0, a1 = ang - 0.9 * abre, ang + 0.9 * abre
    arco = [(cx + r * math.cos(a0 + (a1 - a0) * k / 10), cy + r * math.sin(a0 + (a1 - a0) * k / 10)) for k in range(11)]
    for k in range(len(arco) - 1):
        segs.append((arco[k][0], arco[k][1], arco[k + 1][0], arco[k + 1][1], 1.0))
    for k in range(0, 11, 2):
        segs.append((cx, cy, arco[k][0], arco[k][1], 0.6))
    return segs, arco


def leque_de_aco(T, t, rng):
    """O leque da Kitana: o leque de aço aberto voa girando como bumerangue da esquerda, corta o rival ao passar
    (o fio do leque brilha) e volta fazendo a curva."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voo = rel(t, 0.0, 0.7)
    if 0 < voo < 1:
        a = math.pi * voo
        x = -0.8 + 0.85 * math.sin(a) + 0.0
        y = -0.35 * math.cos(a) * 0 + 0.25 * math.sin(2 * a)
        x = -0.85 * math.cos(a)
        y = -0.3 * math.sin(a) + 0.15
        segs, arco = _leque(x, y, 0.3, t * 25)
        G += T.lines(segs, 0.018) * 1.3
        H += T.polyline(arco, 0.01) * 1.2
        rastro = []
        for k in range(1, 6):
            vv = max(0.0, voo - 0.03 * k)
            aa = math.pi * vv
            rastro.append((-0.85 * math.cos(aa), -0.3 * math.sin(aa) + 0.15, 1 - k / 6))
        G += T.splats(rastro, 0.04) * 0.5
    for t0 in (0.3, 0.38):
        u = rel(t, t0, t0 + 0.2)
        if 0 < u < 1:
            dy = (t0 - 0.34) * 2
            G += T.polys([(lamina(-0.35, -0.25 + dy, 0.35, 0.2 + dy, 0.025, prog=min(1, u * 3)), 1.0)]) * (1 - u) * 1.4
    g, h = _estouro(T, t, 0.32, 0.6, 0, 0, 0.25, 7, 7, 0.014)
    G += g * 0.7
    H += h * 0.7
    return G * env, H * env


# ================================================================== Shao Kahn
def martelo_do_imperador(T, t, rng):
    """A marretada do Shao Kahn: a marreta enorme (a cabeça quadrada com os cravos) sobe e desce com tudo em cima
    do rival, o chão racha em volta e a poeira levanta."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    ergue = ease_out(rel(t, 0.0, 0.2), 2)
    desce = ease_in(rel(t, 0.2, 0.36), 3)
    if t < 0.5:
        ang = -math.pi / 2 - 0.9 * ergue + 1.6 * desce
        px, py = -0.35, 0.55
        cx, cy = px + 0.8 * math.cos(ang), py + 0.8 * math.sin(ang)
        G += T.lines([(px, py, cx, cy, 1.0)], 0.03) * 1.1
        cab = _gira([(-0.14, -0.1), (0.14, -0.1), (0.14, 0.1), (-0.14, 0.1)], ang, cx, cy)
        C = T.polys([(cab, 1.0)])
        cravos = [(_gira([(-0.04, -0.1), (0.04, -0.1), (0.0, -0.18)], ang + math.pi / 2 * s, cx, cy), 1.0) for s in (1, -1)]
        G += (C * 0.7 + _borda(T, C, 0.008) * 1.3 + T.polys(cravos) * 1.2) * (1 - rel(t, 0.4, 0.5))
    bate = rel(t, 0.35, 0.85)
    if 0 < bate < 1:
        b = ease_out(bate, 3)
        H += T.gauss(0.1, 0.0, 0.12) * (1 - bate) ** 2 * 2.0
        G += T.ring(0.1 + 0.6 * b, 0.04, 0.1, 0.2, squash=2.2) * (1 - bate) * 1.4
        q = np.random.default_rng(13)
        for k in range(7):
            a = math.pi * k / 6
            G += T.polyline(jagged(q, 0.1, 0.2, 0.1 + 0.7 * b * math.cos(a), 0.2 + 0.25 * b * math.sin(a) * 0.5, 4, 0.3), 0.012) * (1 - rel(t, 0.75, 1.0))
        pts = [(0.1 + q.uniform(-0.6, 0.6) * b, 0.2 - q.uniform(0, 0.4) * b, (1 - bate) * 0.6) for _ in range(14)]
        G += T.splats(pts, 0.05) * 0.8
    return G * env, H * env


# ================================================================== Snorlax
def esmagada_do_snorlax(T, t, rng):
    """A barrigada do Snorlax: a barriga enorme e redonda cai do alto em cima do rival, achata com o peso (o
    contorno espalhando), o chão treme em ondas e saem os "Z" de sono."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cai = ease_in(rel(t, 0.0, 0.3), 2.5)
    if t < 0.62:
        y = -1.1 + 1.1 * cai
        achata = 1 + 0.5 * pulso(t, 0.28, 0.55)
        B = T.ring(0.42, 0.03, 0, y, squash=achata)
        barriga = T.arc_band(0.25, 0.025, 0.3, math.pi - 0.3, squash=0.6 / achata, cx=0, cy=y - 0.05)
        G += (B * 1.2 + barriga * 0.8 + T.gauss(0, y, 0.35, 0.35 / achata) * 0.2) * (1 - rel(t, 0.5, 0.62))
    for k in range(3):
        u = rel(t, 0.3 + 0.08 * k, 0.75 + 0.08 * k)
        if 0 < u < 1:
            G += T.ring(0.3 + 0.7 * ease_out(u, 2), 0.03, 0, 0.45, squash=3.0) * (1 - u) * 1.2
    H += T.gauss(0, 0.3, 0.2, 0.08) * pulso(t, 0.28, 0.5) * 1.5
    z = rel(t, 0.45, 1.0)
    if 0 < z < 1:
        segs = []
        for k in range(3):
            s = 0.05 + 0.025 * k
            cx, cy = 0.35 + 0.1 * k, -0.35 - 0.15 * k - 0.2 * z
            segs += [(cx - s, cy - s, cx + s, cy - s, 1 - z), (cx + s, cy - s, cx - s, cy + s, 1 - z), (cx - s, cy + s, cx + s, cy + s, 1 - z)]
        G += T.lines(segs, 0.014) * 1.2
    return G * env, H * env


# ================================================================== Patrick
def tapao_estrela(T, t, rng):
    """O tapão do Patrick: a mão de estrela-do-mar (a estrela gordinha, de pontas redondas) vem de cima e bate
    achatando no rival, e ficam as linhas de tremedeira e o "duh" das estrelinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.28), 2)
    if t < 0.55:
        x = -0.5 + 0.5 * vem
        y = -0.7 + 0.7 * vem
        achata = 1 + 0.4 * pulso(t, 0.26, 0.45)
        E = T.polys([(estrela(x, y, 0.3, -math.pi / 2 + 0.3 * (1 - vem), 5, 0.55, 1 / achata), 1.0)], 0.02)
        G += (E * 0.6 + _borda(T, E, 0.01) * 1.3) * (1 - rel(t, 0.45, 0.55))
    g, h = _estouro(T, t, 0.26, 0.55, 0, 0, 0.35, 10, 9)
    G += g
    H += h
    treme = pulso(t, 0.35, 0.9)
    if treme > 0:
        for lado in (-1, 1):
            pts = [(0.45 * lado + 0.04 * math.sin(j * 1.5 + t * 50), -0.2 + 0.05 * j) for j in range(9)]
            G += T.polyline(pts, 0.012) * treme
    G += _estrelinhas(T, t, 0.35, 0.6, 0, -0.35, 4, 0.3, 30)
    return G * env, H * env


# ================================================================== Flecha
def socos_supersonicos(T, t, rng):
    """O soco relâmpago do Flecha: ele chega num risco de velocidade e solta uma rajada de socos tão rápida que
    os punhos ficam em vários lugares ao mesmo tempo (os fantasmas dos punhos), com os acertos estourando
    um atrás do outro."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    chega = rel(t, 0.0, 0.15)
    if chega < 1:
        G += T.tapered([(-1.0, 0.0, -1.0 + 0.7 * chega, 0.0, 1.0), (-1.0, 0.1, -1.0 + 0.6 * chega, 0.1, 0.6), (-1.0, -0.1, -1.0 + 0.6 * chega, -0.1, 0.6)], 0.03) * 1.2
    rajada = rel(t, 0.12, 0.6)
    if 0 < rajada < 1:
        q = np.random.default_rng(int(t * 60) % 11)
        for k in range(4):
            x = -0.3 + q.uniform(-0.05, 0.1)
            y = q.uniform(-0.25, 0.25)
            P, _ = _punho(T, x, y, 1.0)
            G += P * 0.35 + _borda(T, P, 0.005) * 0.6
            G += T.tapered([(x - 0.35, y, x - 0.1, y, 0.7)], 0.02) * 0.7
        for k in range(6):
            tk = 0.15 + 0.07 * k
            b = rel(t, tk, tk + 0.12)
            if 0 < b < 1:
                bx, by = 0.05 + 0.06 * math.sin(k * 2.1), 0.2 * math.cos(k * 1.7)
                H += T.flare(bx, by, 0.2 * (1 - b) + 0.01, k, 0.01) * (1 - b) * 1.4
                G += T.ring(0.03 + 0.12 * b, 0.012, bx, by) * (1 - b)
    return G * env, H * env


# ================================================================== Gwen
def raio_de_mana(T, t, rng):
    """O raio de mana da Gwen: o raio de energia sai das mãos com o padrão de hexágonos correndo dentro dele, e
    no rival estoura em hexágonos que se soltam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vai = ease_out(rel(t, 0.0, 0.2), 2)
    some = 1 - rel(t, 0.38, 0.55)
    if vai > 0 and some > 0:
        x1 = -0.9 + 0.9 * vai
        R = T.lines([(-0.9, 0.0, x1, 0.0, 1.0)], 0.06)
        G += (T.blur(R, 0.02) * 0.8 + _borda(T, R, 0.008) * 1.0) * some
        H += T.lines([(-0.9, 0.0, x1, 0.0, 1.0)], 0.012) * some
        segs = []
        for k in range(8):
            cx = -0.9 + ((k / 8 + t * 2) % 1) * (x1 + 0.9)
            segs += _contorno(_hexagono(cx, 0.0, 0.04, 0.3), 0.9)
        G += T.lines(segs, 0.008) * some
    sai = rel(t, 0.2, 0.85)
    if 0 < sai < 1:
        q = np.random.default_rng(14)
        segs = []
        for _ in range(10):
            a = q.uniform(0, TAU)
            d = 0.1 + 0.5 * ease_out(sai, 2) * q.uniform(0.5, 1)
            segs += _contorno(_hexagono(d * math.cos(a), d * math.sin(a), 0.06 * (1 - 0.5 * sai), sai * 4 + a), 1 - sai)
        G += T.lines(segs, 0.012) * 1.3
        H += T.gauss(0, 0, 0.08) * (1 - sai) ** 2 * 1.6
        G += T.ring(0.08 + 0.3 * ease_out(sai, 3), 0.025, 0, 0) * (1 - sai)
    return G * env, H * env


# ================================================================== Viúva Negra
def chute_da_viuva(T, t, rng):
    """O chute giratório da Viúva Negra: a perna gira num arco largo, o pé acerta, e as Mordidas da Viúva nos
    pulsos dão o choque azul (os raios curtos estalando)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    gira = ease_out(rel(t, 0.0, 0.28), 2.2)
    if gira > 0 and t < 0.5:
        a1 = math.pi + 1.5 + 3.2 * gira
        A = T.arc_band(0.5, 0.06, a1 - 2.4, a1, squash=0.8, cx=-0.2, cy=0.05, crescente=True)
        G += (A * 1.3 + T.blur(A, 0.02) * 0.5) * (1 - rel(t, 0.3, 0.5))
    g, h = _estouro(T, t, 0.26, 0.55, 0.15, 0.0, 0.3, 9, 15)
    G += g
    H += h
    choque = pulso(t, 0.3, 0.75)
    if choque > 0:
        q = np.random.default_rng(int(t * 40) % 8 + 3)
        for k in range(5):
            a = TAU * k / 5 + t * 6
            R = T.polyline(jagged(q, 0.15 + 0.08 * math.cos(a), 0.08 * math.sin(a), 0.15 + 0.35 * math.cos(a), 0.35 * math.sin(a), 4, 0.5), 0.01)
            G += R * choque * 1.3
            H += R * choque * 0.5
    return G * env, H * env


# ================================================================== Gavião Arqueiro
def _flecha(x, y, ang, comp=0.5):
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    tx, ty = x - ux * comp, y - uy * comp
    segs = [(tx, ty, x, y, 1.0)]
    for lado in (-1, 1):
        segs.append((x, y, x - ux * 0.07 + nx * 0.04 * lado, y - uy * 0.07 + ny * 0.04 * lado, 1.0))
        segs.append((tx + ux * 0.08, ty + uy * 0.08, tx - ux * 0.0 + nx * 0.05 * lado, ty + ny * 0.05 * lado, 0.8))
        segs.append((tx + ux * 0.13, ty + uy * 0.13, tx + ux * 0.05 + nx * 0.05 * lado, ty + uy * 0.05 + ny * 0.05 * lado, 0.8))
    return segs


def flecha_do_gaviao(T, t, rng):
    """A flecha do Gavião Arqueiro: a corda solta, a flecha atravessa reta (com as penas atrás e o assobio), crava
    no rival e a ponta-surpresa estoura numa explosãozinha."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = ease_in(rel(t, 0.0, 0.22), 1.3)
    if t < 0.6:
        x = -0.9 + 0.9 * voa
        G += T.lines(_flecha(x, 0.0, 0.0), 0.014) * 1.3 * (1 - rel(t, 0.45, 0.6))
        if voa < 1:
            G += T.tapered([(x - 0.9, 0.0, x - 0.5, 0.0, 0.6)], 0.012)
    bum = rel(t, 0.3, 0.75)
    if 0 < bum < 1:
        b = ease_out(bum, 3)
        H += T.gauss(0.05, 0, 0.06 + 0.1 * b) * (1 - bum) ** 2 * 2.0
        G += T.ring(0.08 + 0.35 * b, 0.03, 0.05, 0) * (1 - bum) * 1.3 + T.gauss(0.05, 0, 0.1 + 0.15 * b) * (1 - bum) * 0.9
    g, h = _estouro(T, t, 0.22, 0.5, 0.0, 0.0, 0.2, 6, 17, 0.014)
    G += g * 0.6
    H += h * 0.5
    return G * env, H * env


# ================================================================== Gamora
def godslayer(T, t, rng):
    """A Godslayer da Gamora: a espada curva estica a lâmina (o fio se alongando) no meio do giro e corta o rival
    num arco amplo e afiado."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    gira = ease_out(rel(t, 0.0, 0.3), 2.5)
    if gira > 0 and t < 0.55:
        comp = 0.35 + 0.35 * ease_out(rel(t, 0.05, 0.2), 2)
        a1 = -2.4 + 2.8 * gira
        px, py = -0.4, 0.25
        tip = (px + comp * 1.3 * math.cos(a1), py + comp * 1.3 * math.sin(a1))
        L = T.polys([(lamina(px, py, tip[0], tip[1], 0.04), 1.0)])
        G += (L * 1.2 + _borda(T, L, 0.005) * 0.8) * (1 - rel(t, 0.35, 0.55))
        A = T.arc_band(comp * 1.3, 0.07, -2.4, a1, cx=px, cy=py, crescente=True)
        G += A * 1.1 * (1 - rel(t, 0.32, 0.55))
        H += T.gauss(tip[0], tip[1], 0.03) * 1.2
    g, h = _estouro(T, t, 0.25, 0.55, 0.1, -0.1, 0.3, 8, 19, 0.015)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Drax
def facas_de_drax(T, t, rng):
    """As facas do Drax: as duas facas entram cruzadas e cravam, uma depois da outra (o X), com o estalo de cada
    uma."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    for k, (ang, t0) in enumerate(((0.6, 0.0), (-0.6, 0.12))):
        vem = ease_in(rel(t, t0, t0 + 0.18), 2)
        if vem <= 0 or t > 0.6:
            continue
        d = 0.6 * (1 - vem)
        ux, uy = math.cos(ang), math.sin(ang)
        tip = (0.05 - ux * d, -uy * d)
        base = (tip[0] - ux * 0.4, tip[1] - uy * 0.4)
        L = T.polys([(lamina(base[0], base[1], tip[0], tip[1], 0.035), 1.0)])
        cabo = T.lines([(base[0], base[1], base[0] - ux * 0.15, base[1] - uy * 0.15, 1.0)], 0.03)
        G += (L * 1.2 + cabo * 0.9) * (1 - rel(t, 0.45, 0.6))
        b = rel(t, t0 + 0.18, t0 + 0.4)
        if 0 < b < 1:
            H += T.flare(tip[0], tip[1], 0.3 * (1 - b) + 0.01, ang, 0.01) * (1 - b) * 1.4
            G += T.ring(0.04 + 0.15 * b, 0.015, tip[0], tip[1]) * (1 - b)
    G += _gotas(T, t, 0.3, 0.5, 0.05, 0.0, 10, 0.4, 23, -2.6, -0.4, 0.016, 0.4)
    return G * env, H * env


# ================================================================== Mulher-Aranha
def soco_bioeletrico(T, t, rng):
    """O soco da Mulher-Aranha: o punho carregado de bioeletricidade (os raios curtos envolvendo a mão) avança e
    descarrega no rival num clarão elétrico."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vai = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.45:
        x = -0.8 + 0.72 * vai
        P, nos = _punho(T, x, 0.0, 1.6)
        G += P * 0.6 + _borda(T, P, 0.007) * 1.1
        q = np.random.default_rng(int(t * 50) % 9 + 1)
        for k in range(4):
            a = TAU * k / 4 + t * 20
            G += T.polyline(jagged(q, x + 0.1 * math.cos(a), 0.1 * math.sin(a), x + 0.25 * math.cos(a + 0.5), 0.25 * math.sin(a + 0.5), 3, 0.5), 0.01) * 1.3
    g, h = _estouro(T, t, 0.25, 0.55, 0.05, 0, 0.35, 10, 25)
    G += g
    H += h
    descarga = pulso(t, 0.28, 0.6)
    if descarga > 0:
        q = np.random.default_rng(int(t * 30) % 6 + 40)
        for k in range(6):
            a = TAU * k / 6 + 0.3
            G += T.polyline(jagged(q, 0.05, 0, 0.05 + 0.5 * math.cos(a), 0.5 * math.sin(a), 5, 0.4), 0.012) * descarga * 1.2
    return G * env, H * env


# ================================================================== Mulher-Gato
def arranhao_felino(T, t, rng):
    """O arranhão da Mulher-Gato: o chicote estala primeiro (a curva fina que se estica e quebra na ponta) e logo
    as garras rasgam em três riscos."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    chicote = ease_out(rel(t, 0.0, 0.2), 2)
    if chicote > 0 and t < 0.4:
        pts = []
        for j in range(30):
            u = j / 29 * chicote
            pts.append((-0.95 + 1.0 * u, -0.2 * math.sin(math.pi * u) + 0.1 * math.sin(TAU * u * 2 + t * 30) * (1 - u)))
        G += T.polyline(pts, 0.012) * 1.2 * (1 - rel(t, 0.25, 0.4))
        H += T.flare(pts[-1][0], pts[-1][1], 0.2 * pulso(t, 0.15, 0.3) + 0.01, 0.3, 0.008) * pulso(t, 0.15, 0.3)
    for k in range(3):
        t0 = 0.25 + 0.03 * k
        p = ease_out(rel(t, t0, t0 + 0.1), 3)
        ini = rel(t, t0 + 0.15, t0 + 0.45)
        if p > 0 and ini < 1:
            dx = (k - 1) * 0.13
            L = T.polys([(lamina(dx - 0.2, -0.4, dx + 0.15, 0.4, 0.03, prog=p, inicio=ini), 1.0)])
            G += L * 1.4
            H += L * 0.5
    return G * env, H * env


# ================================================================== Espantalho
def gas_do_medo(T, t, rng):
    """O gás do medo do Espantalho: o borrifo sai do pulso em jato, vira uma nuvem que envolve o rival girando, e
    dentro dela aparecem rostos de pavor (os olhos e a boca gritando) que se desfazem."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    jato = rel(t, 0.0, 0.3)
    if 0 < jato < 1:
        q = np.random.default_rng(int(t * 30) % 7)
        pts = [(-0.85 + 0.85 * u, 0.05 * math.sin(u * 10 + t * 30) + q.uniform(-0.04, 0.04) * u * 3, 0.8) for u in np.linspace(0, jato, 14)]
        G += T.splats(pts, 0.035) * 1.0
    nuvem = rel(t, 0.2, 1.0)
    if 0 < nuvem < 1:
        q = np.random.default_rng(31)
        pts = []
        for k in range(22):
            a = q.uniform(0, TAU) + nuvem * 2.5
            r = q.uniform(0.15, 0.55) * (0.5 + 0.5 * ease_out(nuvem, 2))
            pts.append((r * math.cos(a), r * 0.75 * math.sin(a), math.sin(math.pi * nuvem) * 0.7))
        N = T.splats(pts, 0.08)
        G += T.blur(N, 0.03) * 0.4 + _borda(T, N, 0.03) * 0.35
    rostos = pulso(t, 0.35, 0.9)
    if rostos > 0:
        segs = []
        for k, (cx, cy) in enumerate(((-0.28, -0.18), (0.25, 0.02), (-0.05, 0.3))):
            e = 1.9 * (0.85 + 0.15 * math.sin(t * 8 + k))
            for lado in (-1, 1):
                olho = [(cx + lado * 0.06 * e + 0.03 * e * math.cos(a), cy - 0.04 * e + 0.045 * e * math.sin(a)) for a in np.linspace(0, TAU, 12, endpoint=False)]
                segs += _contorno(olho)
            boca = [(cx + 0.04 * e * math.cos(a), cy + 0.08 * e + 0.07 * e * math.sin(a)) for a in np.linspace(0, TAU, 14, endpoint=False)]
            segs += _contorno(boca)
        Rf = T.lines(segs, 0.014)
        G += Rf * rostos * 1.5
        H += Rf * rostos * 0.6
    return G * env, H * env


REGISTRO = [
    ("maletada", maletada, GRANDE, "Básico do Leorio: a maleta e os papéis", False),
    ("senbonzakura_corte", senbonzakura_corte, GRANDE, "Básico do Byakuya: o corte e as pétalas afiadas", False),
    ("leque_de_aco", leque_de_aco, GRANDE, "Básico da Kitana: o leque que vai e volta", False),
    ("martelo_do_imperador", martelo_do_imperador, GRANDE, "Básico do Shao Kahn: a marreta e o chão rachado", False),
    ("esmagada_do_snorlax", esmagada_do_snorlax, GRANDE, "Básico do Snorlax: a barriga caindo e os Z", False),
    ("tapao_estrela", tapao_estrela, GRANDE, "Básico do Patrick: o tapão de estrela", False),
    ("socos_supersonicos", socos_supersonicos, GRANDE, "Básico do Flecha: a rajada de socos", False),
    ("raio_de_mana", raio_de_mana, GRANDE, "Básico da Gwen: o raio e os hexágonos", False),
    ("chute_da_viuva", chute_da_viuva, GRANDE, "Básico da Viúva Negra: o chute e o choque", False),
    ("flecha_do_gaviao", flecha_do_gaviao, GRANDE, "Básico do Gavião Arqueiro: a flecha e a ponta explosiva", False),
    ("godslayer", godslayer, GRANDE, "Básico da Gamora: a Godslayer esticando", False),
    ("facas_de_drax", facas_de_drax, GRANDE, "Básico do Drax: as duas facas em X", False),
    ("soco_bioeletrico", soco_bioeletrico, GRANDE, "Básico da Mulher-Aranha: o soco elétrico", False),
    ("arranhao_felino", arranhao_felino, GRANDE, "Básico da Mulher-Gato: o chicote e as garras", False),
    ("gas_do_medo", gas_do_medo, GRANDE, "Básico do Espantalho: o gás e os rostos de pavor", False),
]
