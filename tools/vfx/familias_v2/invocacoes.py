"""Invocações (parte 8): cada criatura com a sua animação de ataque.

Pedido do jogador: a invocação tem que ser muito bem feita, com animação
própria para cada um que invoca. Cada folha mostra a criatura chegando e
atacando o alvo (no centro do quadro): o lobo de sombra que morde, os
soldados que sobem do chão, o Mago Negro com o círculo mágico, o Dragão
Branco soprando, as mandíbulas de Gomorrah, a chuva de socos do Star
Platinum, as feras do Caminho Animal, as vassouras do Mickey, o enxame de
Planktons e o soco-foguete do androide do Krang.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, some, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


def _elipse(cx, cy, rx, ry, n=28, ang=0.0):
    return _gira([(rx * math.cos(a), ry * math.sin(a)) for a in np.linspace(0, TAU, n, endpoint=False)], ang, cx, cy)


def _clarao(T, t, a, b, cx=0.0, cy=0.0, r=0.3):
    k = pulso(t, a, b)
    return T.gauss(cx, cy, r, r) * k * 1.6, (T.flare(cx, cy, 0.7 * k + 0.01, ang=0.3, thin=0.016) + T.flare(cx, cy, 0.45 * k + 0.01, ang=0.3 + math.pi / 2, thin=0.012)) * k * 1.6


# ===================================================================== as criaturas, desenhadas de novo
# (pedido do jogador: "faz as animações deles bem feitas… que nem os outros têm animações próprias bem
# feitas"). Cada uma acompanha o desenho da bolinha (tools/vfx/invocacoes_icones.py) e acontece no alvo
# (o centro do quadro): a bolinha já voou até ele (de perto) ou disparou de longe.

def _brilho(T, A, s=0.008):
    return np.clip(A - T.blur(A, s), 0, 1)


def _poeira(T, t, a, b, n, cx, cy, espalha, seed=3):
    sub = np.random.default_rng(seed)
    f = ease_out(rel(t, a, b), 2)
    pts = []
    for _ in range(n):
        ang = sub.uniform(math.pi * 0.95, math.pi * 2.05)
        d = espalha * f * sub.uniform(0.4, 1.0)
        pts.append((cx + d * math.cos(ang), cy + d * math.sin(ang) * 0.5, (1 - f) * sub.uniform(0.4, 1)))
    return T.splats(pts, 0.03) * (t > a)


def _cabeca_lobo(cx, cy, esc, abre, ang):
    """A cabeça do lobo de perfil (igual à bolinha), virada para a direita; `abre` gira a mandíbula."""
    cranio = [(-0.30, 0.02), (-0.24, -0.14), (-0.16, -0.22), (-0.14, -0.40), (-0.04, -0.26), (0.02, -0.34), (0.06, -0.20),
              (0.20, -0.16), (0.40, -0.10), (0.48, -0.04), (0.46, 0.0), (0.18, 0.02), (-0.10, 0.10)]
    mand = [(-0.08, 0.06), (0.16, 0.04), (0.40, 0.04), (0.38, 0.09), (0.12, 0.14), (-0.12, 0.16)]
    C = _move(_gira(cranio, ang - abre * 0.35), cx, cy, esc)
    M = _move(_gira(mand, ang + abre * 0.55), cx, cy, esc)
    dentes_c = [_move(_gira([(0.14 + 0.07 * k, 0.0), (0.17 + 0.07 * k, 0.0), (0.155 + 0.07 * k, 0.06)], ang - abre * 0.35), cx, cy, esc) for k in range(4)]
    dentes_m = [_move(_gira([(0.12 + 0.07 * k, 0.05), (0.15 + 0.07 * k, 0.05), (0.135 + 0.07 * k, -0.01)], ang + abre * 0.55), cx, cy, esc) for k in range(4)]
    olho = _move(_gira([(0.04, -0.14)], ang - abre * 0.35), cx, cy, esc)[0]
    return C, M, dentes_c + dentes_m, olho


def inv_cao(T, t, rng):
    """Cão divino (Megumi): o lobo branco salta de lado sobre o alvo, a boca abre grande e fecha
    na mordida; as três garras rasgam junto e a névoa de sombra fica para trás."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    salto = ease_out(rel(t, 0.0, 0.32), 1.8)
    cx, cy = -0.95 + 0.9 * salto, -0.05 - 0.35 * math.sin(math.pi * salto)
    esc = 0.9 + 0.5 * salto
    abre = 0.9 * rel(t, 0.12, 0.32) * (1 - ease_in(rel(t, 0.34, 0.42), 2))
    C, M, D, (ox, oy) = _cabeca_lobo(cx, cy, esc, abre, -0.15 + 0.2 * salto)
    vis = 1 - rel(t, 0.6, 0.75)
    corpo = T.polys([(C, 1.0), (M, 0.85)], 0.006) * vis
    dentes = T.polys([(d, 1.0) for d in D], 0.003) * vis
    rastro = sum(T.gauss(cx - 0.22 * k, cy + 0.04 * k, 0.12 + 0.03 * k, 0.08) * (0.5 - 0.08 * k) for k in range(1, 6)) * (1 - rel(t, 0.32, 0.55))
    garras = T.zero()
    for k in range(3):
        f = rel(t, 0.36 + 0.03 * k, 0.5 + 0.03 * k)
        if f > 0:
            x0, y0 = -0.32 + 0.16 * k, -0.34
            garras += T.tapered([(x0, y0, x0 + 0.34 * f, y0 + 0.62 * f, 1.0)], 0.035) * (1 - rel(t, 0.55, 0.8))
    mordida = T.ring(0.06 + 0.42 * ease_out(rel(t, 0.38, 0.65), 2), 0.035) * pulso(t, 0.38, 0.7) * 1.3
    nevoa = (T.gauss(-0.1, 0.1, 0.5, 0.22) + T.gauss(0.2, -0.05, 0.3, 0.16)) * some(t, 0.4, 1.0) * 0.45
    G += (corpo * 1.1 + rastro + dentes * 0.4 + garras * 1.1 + mordida + nevoa) * env
    H += (_brilho(T, corpo) * 0.9 + dentes * 1.3 + T.gauss(ox, oy, 0.025) * 2.4 * vis + garras * 0.9 + mordida * 0.7) * env
    return G, H


def _cavaleiro(cx, cy, s, braco):
    """O cavaleiro de sombra (Igris): elmo com pluma, ombreiras, a capa e a espada longa."""
    elmo = [(cx - 0.09 * s, cy - 0.30 * s), (cx - 0.08 * s, cy - 0.44 * s), (cx, cy - 0.50 * s), (cx + 0.08 * s, cy - 0.44 * s), (cx + 0.09 * s, cy - 0.30 * s), (cx, cy - 0.26 * s)]
    pluma = [(cx, cy - 0.50 * s), (cx - 0.04 * s, cy - 0.66 * s), (cx + 0.10 * s, cy - 0.72 * s), (cx + 0.05 * s, cy - 0.56 * s)]
    tronco = [(cx - 0.22 * s, cy - 0.26 * s), (cx + 0.22 * s, cy - 0.26 * s), (cx + 0.16 * s, cy + 0.10 * s), (cx + 0.24 * s, cy + 0.50 * s), (cx - 0.24 * s, cy + 0.50 * s), (cx - 0.16 * s, cy + 0.10 * s)]
    ombro_e = _elipse(cx - 0.2 * s, cy - 0.24 * s, 0.09 * s, 0.06 * s)
    ombro_d = _elipse(cx + 0.2 * s, cy - 0.24 * s, 0.09 * s, 0.06 * s)
    mx, my = cx + 0.22 * s, cy - 0.18 * s
    ex, ey = mx + math.cos(braco) * 0.78 * s, my + math.sin(braco) * 0.78 * s
    espada = lamina(mx, my, ex, ey, 0.035 * s)
    guarda = lamina(mx + math.cos(braco + math.pi / 2) * 0.08 * s, my + math.sin(braco + math.pi / 2) * 0.08 * s,
                    mx - math.cos(braco + math.pi / 2) * 0.08 * s, my - math.sin(braco + math.pi / 2) * 0.08 * s, 0.025 * s)
    return [(tronco, 0.8), (ombro_e, 0.9), (ombro_d, 0.9), (elmo, 1.0), (pluma, 0.9)], [(espada, 1.0), (guarda, 1.0)], ((cx - 0.035 * s, cy - 0.37 * s), (cx + 0.035 * s, cy - 0.37 * s))


def inv_sombras(T, t, rng):
    """Soldados das Sombras (Jinwoo): a poça negra abre sob o alvo, o cavaleiro de sombra sobe dela de
    olhos acesos, ergue a espada e desce o corte em meia-lua; a fumaça roxa sobe."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.7, 0.95))
    poca = T.ring(0.42 * abre, 0.05, 0, 0.5, 3.2) * 1.2 + T.gauss(0, 0.5, 0.4 * abre + 0.01, 0.1 * abre + 0.01) * 0.7
    sobe = ease_out(rel(t, 0.08, 0.36), 2)
    braco = -2.3 + 2.9 * ease_in(rel(t, 0.36, 0.5), 2)
    corpo, espada, (o1, o2) = _cavaleiro(-0.2, 0.5 - 0.62 * sobe, 0.95, braco)
    vis = sobe * (1 - rel(t, 0.66, 0.82))
    K = T.polys(corpo, 0.006) * vis
    E = T.polys(espada, 0.004) * vis
    olhos = (T.gauss(*o1, 0.02) + T.gauss(*o2, 0.02)) * 2.4 * vis
    corte = T.arc_band(0.5, 0.06, -2.2, -2.2 + 2.6 * ease_out(rel(t, 0.38, 0.52), 2), cx=-0.05, cy=-0.05, crescente=True) * pulso(t, 0.38, 0.7) * 1.4 if t > 0.38 else T.zero()
    sub = np.random.default_rng(7)
    fumo = T.splats([(sub.uniform(-0.5, 0.5), 0.5 - (((t * 0.9 + sub.uniform()) % 1) * 0.9), 0.6) for _ in range(18)], 0.05) * abre
    G += (poca * 0.8 + K * 0.75 + E * 1.0 + olhos + corte + fumo * 0.6) * env
    H += (_brilho(T, K) * 0.7 + _brilho(T, E) * 1.2 + olhos * 1.4 + corte * 0.8) * env
    return G, H


def inv_mago(T, t, rng):
    """Mago Negro (Yugi): o mago de chapéu dobrado e manto aparece de lado, aponta o cajado; o círculo
    mágico abre na frente do alvo e o Ataque de Magia Negra — a esfera escura em espiral — estoura nele."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    surge = ease_out(rel(t, 0.0, 0.22), 2) * (1 - rel(t, 0.62, 0.8))
    mx, my = -0.62, -0.05
    manto = [(mx - 0.2, my + 0.5), (mx - 0.1, my + 0.02), (mx + 0.1, my + 0.02), (mx + 0.22, my + 0.5)]
    rosto = _elipse(mx, my - 0.04, 0.07, 0.08)
    chapeu = [(mx - 0.16, my - 0.06), (mx - 0.06, my - 0.24), (mx + 0.02, my - 0.44), (mx + 0.18, my - 0.50), (mx + 0.12, my - 0.40), (mx + 0.10, my - 0.22), (mx + 0.18, my - 0.06)]
    cajado = lamina(mx + 0.06, my + 0.42, mx + 0.34, my - 0.30, 0.022)
    M = T.polys([(manto, 0.8), (rosto, 0.6), (chapeu, 1.0), (cajado, 1.0)], 0.005) * surge
    ponta = (mx + 0.34, my - 0.30)
    carga = pulso(t, 0.14, 0.42)
    circulo = rel(t, 0.18, 0.36)
    aneis = (T.ring(0.34 * circulo, 0.012, 0.05, -0.05) + T.ring(0.26 * circulo, 0.008, 0.05, -0.05)) * (1 - rel(t, 0.6, 0.8))
    runas = []
    for k in range(10):
        a = k / 10 * TAU + t * 4
        x, y = 0.05 + 0.30 * circulo * math.cos(a), -0.05 + 0.30 * circulo * math.sin(a)
        runas.append(([(x, y - 0.025), (x + 0.018, y), (x, y + 0.025), (x - 0.018, y)], 1.0))
    R = T.polys(runas, 0.003) * (1 - rel(t, 0.6, 0.8)) * (circulo > 0)
    voa = ease_in(rel(t, 0.36, 0.52), 1.5)
    bx, by = ponta[0] + (0.05 - ponta[0]) * voa, ponta[1] + (-0.05 - ponta[1]) * voa
    espiral = T.zero()
    if 0.3 < t < 0.56:
        for k in range(3):
            a0 = t * 22 + k * TAU / 3
            pts = [(bx + 0.09 * (1 - u) * math.cos(a0 + 5 * u), by + 0.09 * (1 - u) * math.sin(a0 + 5 * u)) for u in np.linspace(0, 1, 14)]
            espiral += T.polyline(pts, 0.012)
    esfera = T.gauss(bx, by, 0.07) * janela(t, 0.3, 0.36) * (1 - rel(t, 0.52, 0.56)) * 2.2
    bum = ease_out(rel(t, 0.52, 0.85), 2)
    estoura = (T.ring(0.06 + 0.62 * bum, 0.045, 0.05, -0.05) + T.ring(0.03 + 0.38 * bum, 0.025, 0.05, -0.05)) * pulso(t, 0.52, 0.9) * 1.3
    g, h = _clarao(T, t, 0.5, 0.72, 0.05, -0.05, 0.26)
    G += (M * 0.9 + T.gauss(*ponta, 0.05) * carga * 1.6 + aneis * 1.1 + R * 0.9 + espiral * 0.9 + esfera + estoura + g) * env
    H += (_brilho(T, M) * 0.6 + T.gauss(*ponta, 0.025) * carga * 2 + aneis * 0.5 + esfera * 0.8 + estoura * 0.6 + h) * env
    return G, H


def inv_dragao(T, t, rng):
    """Dragão Branco de Olhos Azuis (Kaiba): a cabeça do dragão entra pelo alto, abre a boca e solta a
    Explosão de Luz Ardente — um raio branco com relâmpagos em volta — que estoura no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    entra = ease_out(rel(t, 0.0, 0.25), 2) * (1 - rel(t, 0.7, 0.88))
    hx, hy, e = -0.85 + 0.3 * entra, -0.55 + 0.1 * entra, 1.25
    abre = 0.5 * rel(t, 0.2, 0.32)
    cranio = [(-0.30, 0.10), (-0.22, -0.08), (-0.06, -0.16), (0.12, -0.14), (0.30, -0.10), (0.46, -0.04), (0.48, 0.0), (0.20, 0.02)]
    mand = [(0.0, 0.04), (0.22, 0.04), (0.42, 0.06), (0.40, 0.10), (0.10, 0.14), (-0.20, 0.14)]
    chifres = [[(-0.12, -0.14), (-0.34, -0.40), (-0.20, -0.36), (-0.02, -0.15)], [(0.02, -0.15), (-0.08, -0.44), (0.06, -0.38), (0.12, -0.14)]]
    ang = 0.5
    C = _move(_gira(cranio, ang - abre * 0.3), hx, hy, e)
    M = _move(_gira(mand, ang + abre * 0.5), hx, hy, e)
    Ch = [_move(_gira(c, ang - abre * 0.3), hx, hy, e) for c in chifres]
    D = T.polys([(C, 1.0), (M, 0.85)] + [(c, 0.9) for c in Ch], 0.006) * entra
    olho = _move(_gira([(0.10, -0.08)], ang - abre * 0.3), hx, hy, e)[0]
    bx, by = _move(_gira([(0.44, 0.04)], ang), hx, hy, e)[0]
    raio_f = rel(t, 0.3, 0.42) * (1 - rel(t, 0.62, 0.72))
    feixe = T.zero()
    if raio_f > 0:
        ex, ey = bx + (0.0 - bx) * min(1, rel(t, 0.3, 0.4) * 1.0), by + (0.0 - by) * min(1, rel(t, 0.3, 0.4))
        feixe = T.polyline([(bx, by), (ex, ey)], 0.16, blur=0.03) * raio_f * 1.2 + T.polyline([(bx, by), (ex, ey)], 0.05) * raio_f * 1.6
        sub = np.random.default_rng(int(t * 40))
        for k in range(3):
            pts = [(bx + (ex - bx) * u + sub.uniform(-0.06, 0.06), by + (ey - by) * u + sub.uniform(-0.06, 0.06)) for u in np.linspace(0, 1, 9)]
            feixe += T.polyline(pts, 0.008) * raio_f * 0.9
    bum = ease_out(rel(t, 0.42, 0.8), 2)
    estoura = T.ring(0.08 + 0.6 * bum, 0.06) * pulso(t, 0.42, 0.85) * 1.3
    g, h = _clarao(T, t, 0.4, 0.66, r=0.3)
    G += (D * 0.95 + feixe + estoura + g) * env
    H += (_brilho(T, D) * 0.8 + T.gauss(*olho, 0.022) * 2.6 * entra + feixe * 0.8 + estoura * 0.6 + h) * env
    return G, H


def inv_gomorrah(T, t, rng):
    """Gomorrah (Bayonetta): a bocarra do demônio surge sobre o alvo com os olhos vermelhos acesos,
    as presas curvas se abrem e fecham com força; o tranco espirra e fica a marca da mordida."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    surge = ease_out(rel(t, 0.0, 0.22), 2) * (1 - rel(t, 0.66, 0.82))
    fecha = ease_in(rel(t, 0.3, 0.42), 2.2)
    gap = 0.42 * (1 - fecha) + 0.04
    cima, baixo = [], []
    for k in range(8):
        x = -0.56 + 0.16 * k
        h = 0.16 + 0.08 * math.sin(k * 1.3) ** 2
        cima.append(([(x - 0.06, -gap), (x + 0.06, -gap), (x + 0.015, -gap + h)], 1.0))
        baixo.append(([(x + 0.02, gap), (x + 0.14, gap), (x + 0.07, gap - h)], 1.0))
    labio_c = [(-0.72, -gap - 0.02), (-0.5, -gap - 0.18), (0.0, -gap - 0.26), (0.5, -gap - 0.18), (0.72, -gap - 0.02)]
    labio_b = [(-0.72, gap + 0.02), (-0.5, gap + 0.18), (0.0, gap + 0.26), (0.5, gap + 0.18), (0.72, gap + 0.02)]
    J = T.polys([(labio_c, 0.75), (labio_b, 0.75)], 0.008) * surge
    P = T.polys(cima + baixo, 0.003) * surge
    olhos = (T.gauss(-0.28, -gap - 0.34, 0.035) + T.gauss(0.28, -gap - 0.34, 0.035)) * 2.4 * surge
    chifres = T.polys([(lamina(-0.4, -gap - 0.24, -0.6, -gap - 0.56, 0.03), 1.0), (lamina(0.4, -gap - 0.24, 0.6, -gap - 0.56, 0.03), 1.0)], 0.004) * surge
    bum = ease_out(rel(t, 0.42, 0.75), 2)
    tranco = T.ring(0.08 + 0.55 * bum, 0.05, 0, 0, 1.6) * pulso(t, 0.42, 0.78) * 1.3
    sub = np.random.default_rng(5)
    gotas = T.splats([(sub.uniform(-0.6, 0.6) * bum, sub.uniform(-0.3, 0.3) * bum + 0.4 * bum ** 2, pulso(t, 0.42, 0.9)) for _ in range(16)], 0.018)
    G += (J * 0.9 + P * 0.5 + chifres * 0.8 + olhos + tranco + gotas * 1.2) * env
    H += (P * 1.2 + olhos * 1.5 + _brilho(T, J) * 0.6 + tranco * 0.6) * env
    return G, H


def _punho(cx, cy, esc, ang):
    """O punho fechado (como a bolinha do Star Platinum), apontando na direção `ang`: a mão, os quatro
    nós dos dedos na frente e o polegar dobrado por baixo."""
    mao = [(-0.30, -0.13), (0.02, -0.18), (0.12, -0.17), (0.12, 0.17), (0.02, 0.18), (-0.30, 0.13)]
    nos = [_elipse(0.15, -0.135 + 0.09 * k, 0.065, 0.048) for k in range(4)]
    polegar = [(-0.06, 0.10), (0.10, 0.12), (0.12, 0.20), (-0.04, 0.22)]
    return [(_move(_gira(p, ang), cx, cy, esc), w) for p, w in [(mao, 0.8), (polegar, 0.9)] + [(n, 1.0) for n in nos]]


def inv_ora(T, t, rng):
    """Star Platinum (Jotaro): a rajada de socos — ORA ORA ORA — punhos em sequência vindo de vários
    ângulos, cada um com o estalo do impacto, e o último soco maior com a estrela de choque."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sub = np.random.default_rng(12)
    punhos, estalos = [], T.zero()
    for k in range(9):
        ini = 0.02 + 0.055 * k
        f = rel(t, ini, ini + 0.12)
        if f <= 0 or f >= 1.0 and t > ini + 0.2:
            continue
        ang = sub.uniform(-0.6, 0.6)
        alvo = (sub.uniform(-0.18, 0.18), sub.uniform(-0.18, 0.18))
        d = 0.75 * (1 - ease_out(f, 2))
        cx, cy = alvo[0] - math.cos(ang) * d, alvo[1] - math.sin(ang) * d
        punhos += [(p, w * (1 - rel(t, ini + 0.12, ini + 0.22))) for p, w in _punho(cx, cy, 0.85, ang)]
        estalos += T.ring(0.04 + 0.16 * rel(t, ini + 0.1, ini + 0.22), 0.02, *alvo) * pulso(t, ini + 0.1, ini + 0.24)
    final = rel(t, 0.52, 0.62)
    if final > 0:
        d = 0.9 * (1 - ease_out(final, 2))
        punhos += [(p, w * (1 - rel(t, 0.66, 0.8))) for p, w in _punho(-d - 0.1, 0, 1.4, 0.0)]
    F = T.polys(punhos, 0.005)
    linhas = T.zero()
    for k in range(6):
        y = -0.4 + 0.16 * k
        linhas += T.polyline([(-1.0, y), (-0.45 - 0.08 * (k % 2), y)], 0.006) * janela(t, 0.0, 0.08) * (1 - rel(t, 0.55, 0.7)) * 0.5
    estrela_ = T.polys([(estrela(0.05, 0, 0.32 * pulso(t, 0.6, 0.85) + 0.01, 0.2, 8, 0.4), 1.0)], 0.006) * pulso(t, 0.6, 0.85)
    G += (F * 1.0 + estalos * 1.2 + linhas + estrela_ * 1.2) * env
    H += (_brilho(T, F) * 0.8 + estalos * 0.6 + estrela_ * 0.6) * env
    return G, H


def inv_feras(T, t, rng):
    """Caminho Animal (Pain): o rinoceronte invocado sai da fumaça, investe de chifre baixo contra o
    alvo e o chão racha; os olhos de Rinnegan brilham."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    fumo = (T.gauss(-0.75, 0.1, 0.25, 0.22) + T.gauss(-0.6, -0.1, 0.18, 0.16)) * pulso(t, 0.0, 0.4) * 0.9
    corre = ease_in(rel(t, 0.08, 0.38), 1.6)
    cx, cy, e = -0.95 + 0.85 * corre, 0.05, 0.85
    cabeca = [(-0.28, -0.16), (-0.08, -0.22), (0.18, -0.16), (0.36, -0.04), (0.40, 0.12), (0.24, 0.24), (-0.10, 0.24), (-0.30, 0.10)]
    chifre = [(0.26, -0.06), (0.56, -0.30), (0.40, 0.02)]
    chifre2 = [(0.08, -0.18), (0.22, -0.34), (0.20, -0.14)]
    orelha = [(-0.16, -0.20), (-0.24, -0.38), (-0.06, -0.22)]
    vis = 1 - rel(t, 0.62, 0.78)
    R = T.polys([(_move(cabeca, cx, cy, e), 0.85), (_move(orelha, cx, cy, e), 0.8)], 0.006) * vis
    H_ = T.polys([(_move(chifre, cx, cy, e), 1.0), (_move(chifre2, cx, cy, e), 1.0)], 0.004) * vis
    ox, oy = cx + 0.06 * e, cy - 0.06 * e
    olho = (T.ring(0.03, 0.006, ox, oy) + T.ring(0.016, 0.005, ox, oy)) * vis
    choque = rel(t, 0.36, 0.7)
    racha = T.zero()
    if choque > 0:
        sub = np.random.default_rng(9)
        for k in range(7):
            a = math.pi * (0.1 + 0.8 * k / 6)
            pts = [(0.0, 0.3)]
            for j in range(1, 5):
                r = 0.13 * j * ease_out(choque, 2)
                pts.append((math.cos(a) * r + sub.uniform(-0.03, 0.03), 0.3 + math.sin(a) * r * 0.35 + sub.uniform(-0.01, 0.01)))
            racha += T.polyline(pts, 0.01)
        racha *= (1 - rel(t, 0.75, 1.0))
    onda = T.ring(0.1 + 0.6 * ease_out(choque, 2), 0.05, 0, 0.3, 3.0) * pulso(t, 0.36, 0.8) * 1.3
    poeira = _poeira(T, t, 0.36, 0.9, 22, 0.0, 0.3, 0.7)
    G += (fumo + R * 0.9 + H_ * 1.1 + olho * 1.5 + racha * 1.1 + onda + poeira * 0.8) * env
    H += (_brilho(T, R) * 0.6 + _brilho(T, H_) * 1.2 + olho * 1.4 + onda * 0.5) * env
    return G, H


def _vassoura(px, py, ang, s):
    """A vassoura encantada pendurada do alto (px, py): o cabo comprido e a palha em leque na ponta,
    com as fitas da amarração. `ang` gira tudo em volta do alto do cabo."""
    cabo = lamina(0, 0, 0, 0.62, 0.035)
    palha = [(-0.06, 0.60), (0.06, 0.60), (0.20, 0.98), (-0.20, 0.98)]
    amarra = lamina(-0.08, 0.64, 0.08, 0.64, 0.02)
    fios = [lamina(-0.12 + 0.06 * k, 0.70, -0.16 + 0.08 * k, 0.96, 0.006) for k in range(5)]
    return [(_move(_gira(p, ang), px, py, s), w) for p, w in [(cabo, 1.0), (palha, 0.8), (amarra, 1.0)] + [(f, 0.5) for f in fios]]


def inv_vassouras(T, t, rng):
    """As vassouras encantadas (Mickey): duas vassouras entram marchando pelos lados, batem no alvo em
    sequência — paf, paf — e os baldes viram, espirrando água em gotas que caem."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    partes = []
    for k, (lado, ini) in enumerate(((-1, 0.0), (1, 0.12))):
        entra = ease_out(rel(t, ini, ini + 0.18), 2)
        bate = math.sin(math.pi * rel(t, ini + 0.2, ini + 0.36))
        px, py = lado * (1.1 - 0.5 * entra), -0.78
        # parada, a vassoura pende para fora; na batida, a palha varre até o alvo
        ang = lado * (0.35 - 0.95 * bate)
        vis = (entra > 0) * (1 - rel(t, 0.66, 0.8))
        partes += [(p, w * vis) for p, w in _vassoura(px, py, ang, 0.85)]
    V = T.polys(partes, 0.005)
    paf = (T.ring(0.05 + 0.22 * rel(t, 0.3, 0.45), 0.03, -0.12, 0.05) * pulso(t, 0.3, 0.48) + T.ring(0.05 + 0.22 * rel(t, 0.42, 0.57), 0.03, 0.12, 0.05) * pulso(t, 0.42, 0.6)) * 1.3
    espirra = rel(t, 0.5, 0.95)
    sub = np.random.default_rng(14)
    gotas = []
    for _ in range(26):
        vx, vy = sub.uniform(-0.9, 0.9), sub.uniform(-1.1, -0.4)
        x, y = vx * espirra * 0.6, -0.25 + vy * espirra * 0.6 + 1.4 * espirra ** 2
        gotas.append((x, y, (1 - espirra) * (espirra > 0)))
    Gt = T.splats(gotas, 0.016)
    agua = T.polyline([(-0.3, -0.25), (-0.15, -0.35), (0.0, -0.3), (0.15, -0.36), (0.3, -0.25)], 0.03) * pulso(t, 0.48, 0.66)
    G += (V * 1.0 + paf + Gt * 1.6 + agua * 1.1) * env
    H += (_brilho(T, V) * 0.6 + paf * 0.6 + Gt * 1.2 + agua * 0.8) * env
    return G, H


def _plankton(cx, cy, s):
    corpo = [(cx - 0.05 * s, cy + 0.13 * s), (cx - 0.06 * s, cy - 0.01 * s), (cx - 0.04 * s, cy - 0.07 * s), (cx, cy - 0.09 * s),
             (cx + 0.04 * s, cy - 0.07 * s), (cx + 0.06 * s, cy - 0.01 * s), (cx + 0.05 * s, cy + 0.13 * s)]
    antena1 = lamina(cx - 0.02 * s, cy - 0.08 * s, cx - 0.06 * s, cy - 0.18 * s, 0.008 * s)
    antena2 = lamina(cx + 0.02 * s, cy - 0.08 * s, cx + 0.06 * s, cy - 0.18 * s, 0.008 * s)
    return [(corpo, 0.8), (antena1, 1.0), (antena2, 1.0)], (cx, cy - 0.02 * s)


def inv_clones(T, t, rng):
    """O exército do Plankton: os clones (corpinho de um olho só e antenas) chegam pulando de todos os
    lados, se amontoam no alvo e o monte se desfaz num estouro de estrelinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(21)
    formas, olhos = [], T.zero()
    for k in range(14):
        ini = sub.uniform(0.0, 0.25)
        f = ease_out(rel(t, ini, ini + 0.3), 1.6)
        a0 = sub.uniform(0, TAU)
        x0, y0 = math.cos(a0) * 1.0, math.sin(a0) * 0.8
        x1, y1 = sub.uniform(-0.22, 0.22), sub.uniform(-0.1, 0.25)
        x = x0 + (x1 - x0) * f
        y = y0 + (y1 - y0) * f - 0.35 * math.sin(math.pi * f)
        vis = (f > 0) * (1 - rel(t, 0.58, 0.68))
        partes, (ex, ey) = _plankton(x, y, 1.3)
        formas += [(p, w * vis) for p, w in partes]
        olhos += T.gauss(ex, ey, 0.018) * vis
    C = T.polys(formas, 0.004)
    bum = rel(t, 0.58, 0.95)
    est = []
    for k in range(10):
        a = k / 10 * TAU
        d = 0.08 + 0.55 * ease_out(bum, 2)
        est.append((estrela(math.cos(a) * d, math.sin(a) * d * 0.8, 0.04, a, 5, 0.45), pulso(t, 0.58, 0.95)))
    S_ = T.polys(est, 0.004)
    G += (C * 1.0 + olhos * 1.5 + S_ * 1.1 + T.ring(0.08 + 0.4 * bum, 0.04) * pulso(t, 0.58, 0.85)) * env
    H += (_brilho(T, C) * 0.6 + olhos * 2.2 + S_ * 0.6) * env
    return G, H


def inv_androide(T, t, rng):
    """O androide do Krang: o braço-canhão do robô aparece de lado, carrega, e dispara o laser rosa
    que fura o alvo; faíscas elétricas e a explosão em anel."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    surge = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.64, 0.8))
    ax, ay = -0.72, -0.25
    braco = [(ax - 0.30, ay - 0.10), (ax + 0.10, ay - 0.10), (ax + 0.14, ay - 0.06), (ax + 0.14, ay + 0.06), (ax + 0.10, ay + 0.10), (ax - 0.30, ay + 0.10)]
    canhao = [(ax + 0.12, ay - 0.06), (ax + 0.28, ay - 0.05), (ax + 0.28, ay + 0.05), (ax + 0.12, ay + 0.06)]
    junta = _elipse(ax - 0.30, ay, 0.08, 0.1)
    B = T.polys([(braco, 0.85), (canhao, 1.0), (junta, 0.8)], 0.005) * surge
    bx, by = ax + 0.28, ay
    carga = pulso(t, 0.12, 0.36)
    tiro = rel(t, 0.32, 0.4) * (1 - rel(t, 0.58, 0.66))
    laser = T.zero()
    if tiro > 0:
        u = min(1, rel(t, 0.32, 0.38) * 1.0)
        ex, ey = bx + (0.0 - bx) * u, by + (0.0 - by) * u
        laser = (T.polyline([(bx, by), (ex, ey)], 0.07, blur=0.015) * 1.1 + T.polyline([(bx, by), (ex, ey)], 0.02) * 1.5) * tiro
    sub = np.random.default_rng(int(t * 30) + 3)
    faiscas = T.zero()
    if 0.36 < t < 0.75:
        for k in range(5):
            a = sub.uniform(0, TAU)
            pts = [(0, 0)] + [(math.cos(a) * 0.08 * j + sub.uniform(-0.03, 0.03), math.sin(a) * 0.08 * j + sub.uniform(-0.03, 0.03)) for j in range(1, 4)]
            faiscas += T.polyline(pts, 0.007)
    bum = ease_out(rel(t, 0.38, 0.8), 2)
    anel = T.ring(0.06 + 0.56 * bum, 0.05) * pulso(t, 0.38, 0.82) * 1.3
    g, h = _clarao(T, t, 0.36, 0.6, r=0.24)
    G += (B * 0.95 + T.gauss(bx, by, 0.06) * carga * 1.8 + laser + faiscas * 1.1 + anel + g) * env
    H += (_brilho(T, B) * 0.7 + T.gauss(bx, by, 0.03) * carga * 2 + laser * 0.9 + faiscas * 0.9 + anel * 0.6 + h) * env
    return G, H


REGISTRO = [
    ("inv_cao", inv_cao, GRANDE, "Cão divino: lobo de sombra que salta e morde", False),
    ("inv_sombras", inv_sombras, GRANDE, "Soldados das sombras: o cavaleiro sobe da poça negra e corta em meia-lua", False),
    ("inv_mago", inv_mago, GRANDE, "Mago Negro: o mago aponta o cajado e o Ataque de Magia Negra estoura", False),
    ("inv_dragao", inv_dragao, GRANDE, "Dragão Branco: cabeça do dragão e raio branco", False),
    ("inv_gomorrah", inv_gomorrah, GRANDE, "Gomorrah: mandíbulas que se fecham", False),
    ("inv_ora", inv_ora, GRANDE, "Star Platinum: chuva de socos", False),
    ("inv_feras", inv_feras, GRANDE, "Caminho Animal: o rinoceronte investe de chifre e racha o chão", False),
    ("inv_vassouras", inv_vassouras, GRANDE, "Vassouras encantadas: batem e espirram água", False),
    ("inv_clones", inv_clones, GRANDE, "Exército de clones: enxame de Planktons", False),
    ("inv_androide", inv_androide, GRANDE, "Androide de combate: o braço-canhão dispara o laser rosa", False),
]
