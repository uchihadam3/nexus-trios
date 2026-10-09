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


# ----------------------------------------------------------------- Cão divino
def inv_cao(T, t, rng):
    """Cão divino: um lobo de sombra salta de cima, abre a boca e morde o alvo; a névoa negra fica."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    salto = ease_in(rel(t, 0.0, 0.42), 1.6)
    cx, cy = -0.75 + 0.75 * salto, -0.7 + 0.62 * salto
    esc = 0.75 + 0.35 * salto
    abre = 0.55 * pulso(t, 0.18, 0.5) if t < 0.42 else 0.55 * (1 - ease_out(rel(t, 0.42, 0.5), 2))
    cranio = [(-0.34, -0.08), (-0.22, -0.3), (-0.12, -0.2), (0.0, -0.24), (0.1, -0.42), (0.16, -0.18), (0.3, -0.12), (0.62, -0.04), (0.64, 0.02), (0.3, 0.04), (-0.3, 0.12)]
    mandibula = [(-0.28, 0.1), (0.3, 0.06), (0.58, 0.1), (0.3, 0.2), (-0.2, 0.24)]
    ang = -0.45 + 0.45 * salto
    cab = _move(_gira(cranio, -abre * 0.5 + ang), cx, cy, esc)
    mand = _move(_gira(mandibula, abre * 0.6 + ang), cx, cy, esc)
    dentes = []
    for k in range(5):
        x = 0.05 + 0.1 * k
        dentes.append((_move(_gira([(x, 0.02), (x + 0.04, 0.02), (x + 0.02, 0.1)], -abre * 0.5 + ang), cx, cy, esc), 1.0))
    olho = T.gauss(cx + 0.12 * esc, cy - 0.14 * esc, 0.03, 0.03) * 2.2
    corpo = T.polys([(cab, 1.0), (mand, 1.0)], 0.01)
    rastro = sum(T.gauss(cx - 0.18 * k * esc, cy - 0.12 * k * esc, 0.16, 0.11) * (0.55 - 0.1 * k) for k in range(1, 5)) * (1 - rel(t, 0.42, 0.8))
    mordida = T.ring(0.08 + 0.4 * ease_out(rel(t, 0.42, 0.7), 2), 0.04) * pulso(t, 0.42, 0.75) * 1.4
    nevoa = T.gauss(0, 0.05, 0.45, 0.25) * some(t, 0.45, 1.0) * 0.5
    G += (corpo * 1.1 + rastro + olho + mordida + nevoa + T.polys(dentes, 0.004) * 0.6) * env
    H += (olho * 1.6 + mordida * 0.9 + T.polys(dentes, 0.004) * 1.2) * env
    return G, H


# -------------------------------------------------------- Soldados das sombras
def _soldado(cx, cy, s):
    cabeca = _elipse(cx, cy - 0.32 * s, 0.09 * s, 0.1 * s)
    tronco = [(cx - 0.14 * s, cy - 0.2 * s), (cx + 0.14 * s, cy - 0.2 * s), (cx + 0.1 * s, cy + 0.3 * s), (cx - 0.1 * s, cy + 0.3 * s)]
    lamina_ = [(cx + 0.16 * s, cy - 0.12 * s), (cx + 0.22 * s, cy - 0.16 * s), (cx + 0.46 * s, cy - 0.62 * s), (cx + 0.4 * s, cy - 0.6 * s)]
    return [(cabeca, 1.0), (tronco, 1.0), (lamina_, 1.0)]


def inv_sombras(T, t, rng):
    """Soldados das sombras: rachaduras roxas no chão, quatro soldados sobem do escuro e cortam juntos."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    chao = 0.62
    rachas = T.ring(0.55 * ease_out(rel(t, 0.0, 0.25), 2) + 0.05, 0.03, cy=chao, squash=3.2) * pulso(t, 0.0, 0.6) * 1.2
    soldados, olhos = [], 0
    for k, x in enumerate((-0.6, -0.2, 0.2, 0.6)):
        sobe = ease_out(rel(t, 0.1 + 0.06 * k, 0.45 + 0.06 * k), 2.2)
        y = chao + 0.1 - 0.55 * sobe
        s = 0.9 + 0.15 * (k % 2)
        soldados += _soldado(x, y, s)
        olhos = olhos + T.gauss(x - 0.03 * s, y - 0.33 * s, 0.018, 0.012) * sobe * 2.5 + T.gauss(x + 0.03 * s, y - 0.33 * s, 0.018, 0.012) * sobe * 2.5
    cortes = [(lamina(-0.7 + 0.1 * k, -0.45 + 0.2 * k, 0.7 - 0.1 * k, 0.25 - 0.2 * k, 0.02), 1.0) for k in range(3)]
    corte = T.polys(cortes, 0.004) * pulso(t, 0.52, 0.78) * 1.5
    S = T.polys(soldados, 0.008)
    G += (rachas + S * 0.95 + olhos + corte) * env
    H += (olhos * 1.4 + corte * 1.0 + rachas * 0.4) * env
    return G, H


# ---------------------------------------------------------------- Mago Negro
def inv_mago(T, t, rng):
    """Mago Negro: um círculo mágico gira no chão, a silhueta de chapéu pontudo surge e o cajado dispara
    uma esfera escura que estoura no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    circulo = (T.ring(0.5 * abre, 0.025, cy=0.55, squash=3.0) + T.ring(0.38 * abre, 0.015, cy=0.55, squash=3.0)) * (1 - rel(t, 0.6, 0.9))
    runas = []
    for k in range(8):
        a = k / 8 * TAU + t * 3
        x, y = 0.44 * abre * math.cos(a), 0.55 + 0.44 * abre * math.sin(a) / 3.0
        runas.append(([(x, y - 0.03), (x + 0.02, y), (x, y + 0.03), (x - 0.02, y)], 1.0))
    surge = ease_out(rel(t, 0.12, 0.4), 2)
    mx, my = -0.42, 0.55 - 0.65 * surge
    manto = [(mx - 0.2, my + 0.5), (mx + 0.2, my + 0.5), (mx + 0.08, my), (mx - 0.08, my)]
    chapeu = [(mx - 0.14, my + 0.02), (mx + 0.14, my + 0.02), (mx + 0.22, my - 0.34), (mx + 0.02, my - 0.08)]
    cajado = lamina(mx + 0.16, my + 0.45, mx + 0.32, my - 0.12, 0.02)
    mago = T.polys([(manto, 1.0), (chapeu, 1.0), (cajado, 1.0)], 0.006) * surge
    voa = ease_in(rel(t, 0.38, 0.58), 1.4)
    ox, oy = mx + 0.32 + (0.0 - mx - 0.32) * voa, my - 0.12 + (0.0 - my + 0.12) * voa
    orbe = T.gauss(ox, oy, 0.08, 0.08) * janela(t, 0.36, 0.4) * (1 - rel(t, 0.58, 0.62)) * 2.0
    estoura = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.58, 0.85), 2), 0.05) * pulso(t, 0.58, 0.9) * 1.4
    g, h = _clarao(T, t, 0.56, 0.75)
    G += (circulo * 1.2 + T.polys(runas, 0.003) * janela(t, 0.05, 0.2) + mago * 0.9 + orbe + estoura + g) * env
    H += (circulo * 0.5 + orbe * 1.3 + estoura * 0.7 + h) * env
    return G, H


# ------------------------------------------------------- Dragão Branco
def inv_dragao(T, t, rng):
    """Dragão Branco de Olhos Azuis: a cabeça do dragão surge no alto, abre a boca e solta um raio
    branco que explode no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    surge = back(rel(t, 0.0, 0.3), 1.6)
    hx, hy = -0.72, -0.62
    cabeca = [(-0.3, -0.06), (-0.12, -0.18), (0.12, -0.14), (0.42, -0.06), (0.46, 0.0), (0.12, 0.04), (-0.2, 0.12)]
    chifres = [[(-0.2, -0.12), (-0.38, -0.36), (-0.12, -0.16)], [(-0.04, -0.16), (-0.12, -0.42), (0.04, -0.17)]]
    abre = 0.4 * janela(t, 0.25, 0.35)
    ang = 0.62
    cab = _move(_gira(cabeca, ang - abre * 0.3), hx, hy, surge * 1.0)
    mand = _move(_gira([(-0.15, 0.1), (0.4, 0.05), (0.42, 0.1), (0.1, 0.16)], ang + abre * 0.6), hx, hy, surge * 1.0)
    ch = [(_move(_gira(c, ang), hx, hy, surge * 1.0), 1.0) for c in chifres]
    olho = T.gauss(hx + 0.16 * math.cos(ang) + 0.04, hy + 0.16 * math.sin(ang) - 0.12, 0.035, 0.028) * surge * 2.6
    D = T.polys([(cab, 1.0), (mand, 1.0)] + ch, 0.006)
    bx, by = hx + 0.44 * math.cos(ang), hy + 0.44 * math.sin(ang)
    sopro = rel(t, 0.33, 0.5)
    fx, fy = bx + (0.0 - bx) * ease_out(sopro, 2), by + (0.0 - by) * ease_out(sopro, 2)
    feixe = T.polyline([(bx, by), (fx, fy)], 0.13, blur=0.03) * janela(t, 0.33, 0.36) * (1 - rel(t, 0.68, 0.82)) * 1.5
    miolo = T.polyline([(bx, by), (fx, fy)], 0.05, blur=0.01) * janela(t, 0.33, 0.36) * (1 - rel(t, 0.68, 0.82)) * 1.8
    bum = T.ring(0.1 + 0.7 * ease_out(rel(t, 0.6, 0.9), 2), 0.06) * pulso(t, 0.6, 0.95) * 1.3
    g, h = _clarao(T, t, 0.58, 0.82, r=0.34)
    G += (D * 1.2 + olho + feixe + bum + g) * env
    H += (D * 0.5 + olho * 1.5 + miolo * 1.6 + feixe * 0.6 + bum * 0.6 + h) * env
    return G, H


# ------------------------------------------------------------- Gomorrah
def _arcada(sinal, abre, dentes=6):
    """Mandíbula em crescente: borda de fora curva, borda de dentro com presas."""
    fora, dentro = [], []
    for k in range(25):
        u = k / 24
        x = -0.78 + 1.56 * u
        curva = 0.22 * math.sin(math.pi * u)
        fora.append((x, sinal * (abre + 0.12 + curva + 0.16 * math.sin(math.pi * u) ** 0.6)))
    for k in range(dentes * 2 + 1):
        u = 1 - k / (dentes * 2)
        x = -0.7 + 1.4 * u
        curva = 0.22 * math.sin(math.pi * u)
        presa = 0.0 if k % 2 else -0.17 * math.sin(math.pi * u) ** 0.3
        dentro.append((x, sinal * (abre + curva * 0.6 + presa)))
    return fora + dentro


def inv_gomorrah(T, t, rng):
    """Gomorrah: um portal se abre, mandíbulas enormes de cima e de baixo se fecham sobre o alvo com
    um estalo, e dois olhos vermelhos acendem no escuro."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    portal = T.gauss(0, 0, 0.6, 0.45) * janela(t, 0.0, 0.2) * (1 - rel(t, 0.65, 0.95)) * 0.5
    fecha = ease_in(rel(t, 0.15, 0.48), 2.0)
    abre = 0.55 * (1 - fecha) + 0.02
    cima = _arcada(-1, abre)
    baixo = _arcada(1, abre)
    M = T.polys([(cima, 1.0), (baixo, 1.0)], 0.008) * janela(t, 0.08, 0.18)
    olhos = (T.gauss(-0.28, -0.6, 0.05, 0.03) + T.gauss(0.28, -0.6, 0.05, 0.03)) * janela(t, 0.05, 0.15) * 2.4
    estalo = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.48, 0.75), 2), 0.05) * pulso(t, 0.48, 0.78) * 1.4
    g, h = _clarao(T, t, 0.46, 0.66, r=0.25)
    G += (portal + M * 1.1 + olhos + estalo + g) * env
    H += (olhos * 1.4 + estalo * 0.7 + h) * env
    return G, H


# -------------------------------------------------------- Star Platinum
def _punho(cx, cy, s, ang):
    mao = [(-0.1, -0.11), (0.08, -0.13), (0.15, -0.07), (0.16, 0.06), (0.09, 0.12), (-0.1, 0.11)]
    nos = [[(0.15, -0.1 + 0.055 * k), (0.2, -0.1 + 0.055 * k), (0.2, -0.06 + 0.055 * k), (0.15, -0.06 + 0.055 * k)] for k in range(4)]
    punho = [(-0.34, -0.07), (-0.1, -0.09), (-0.1, 0.09), (-0.34, 0.07)]
    return [(_move(_gira(p, ang), cx, cy, s), 1.0) for p in [mao, punho] + nos]


def inv_ora(T, t, rng):
    """Star Platinum: o vulto do Stand aparece atrás e solta uma chuva de socos ("ORA ORA ORA"): punhos
    em leque, riscos de velocidade e estrelinhas de impacto no alvo; o último soco, maior, estoura."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(1177)
    vulto = (T.gauss(-0.72, -0.1, 0.22, 0.42) + T.gauss(-0.72, -0.5, 0.12, 0.12)) * janela(t, 0.0, 0.12) * (1 - rel(t, 0.62, 0.8)) * 0.45
    punhos, estrelas, riscos = [], [], []
    for k in range(22):
        a0 = 0.03 + 0.024 * k
        f = rel(t, a0, a0 + 0.07)
        if t < a0 or t > a0 + 0.14:
            continue
        alvo_x, alvo_y = sub.uniform(-0.3, 0.3), sub.uniform(-0.4, 0.4)
        ang = math.atan2(alvo_y - sub.uniform(-0.5, 0.3), alvo_x + 0.7)
        d = 0.6 * (1 - ease_out(f, 2))
        cx, cy = alvo_x - d * math.cos(ang) - 0.16 * math.cos(ang), alvo_y - d * math.sin(ang) - 0.16 * math.sin(ang)
        vis = 1.0 - rel(t, a0 + 0.08, a0 + 0.14)
        punhos += [(p, vis) for p, _ in _punho(cx, cy, 0.85, ang)]
        riscos.append((lamina(cx - 0.55 * math.cos(ang), cy - 0.55 * math.sin(ang), cx - 0.18 * math.cos(ang), cy - 0.18 * math.sin(ang), 0.025), vis * 0.7))
        if f >= 1.0:
            estrelas.append((estrela(alvo_x, alvo_y, 0.09 + 0.04 * (k % 3), k * 0.7, 4, 0.32), vis))
    ultimo = rel(t, 0.58, 0.68)
    if 0 < ultimo and t < 0.78:
        d = 0.8 * (1 - ease_in(ultimo, 2))
        punhos += [(p, 1 - rel(t, 0.7, 0.78)) for p, _ in _punho(-0.22 - d, 0.0, 1.6, 0.0)]
    final = T.ring(0.1 + 0.65 * ease_out(rel(t, 0.68, 0.95), 2), 0.05) * pulso(t, 0.68, 0.97) * 1.5
    g, h = _clarao(T, t, 0.66, 0.84, r=0.3)
    P, E, R = T.polys(punhos, 0.006), T.polys(estrelas, 0.004), T.polys(riscos, 0.006)
    G += (vulto + P * 1.1 + R * 0.8 + E * 1.5 + final + g) * env
    H += (P * 0.35 + R * 0.4 + E * 1.1 + final * 0.6 + h) * env
    return G, H


# ------------------------------------------------------- Caminho Animal
def inv_feras(T, t, rng):
    """Caminho Animal: três nuvens de invocação estouram e de cada uma sai uma fera (um chifre de
    rinoceronte, a cabeça de um cão e as asas de um pássaro) investindo contra o alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    fumacas = 0
    feras = []
    for k, (x, y) in enumerate(((-0.65, -0.45), (0.65, -0.4), (0.0, 0.62))):
        a0 = 0.04 * k
        fumacas = fumacas + sum(T.gauss(x + 0.12 * math.cos(j * 2.1), y + 0.08 * math.sin(j * 2.1), 0.14, 0.1) for j in range(4)) * pulso(t, a0, a0 + 0.4) * 0.6
        vai = ease_in(rel(t, a0 + 0.2, a0 + 0.5), 1.6)
        fx, fy = x * (1 - vai * 0.85), y * (1 - vai * 0.85)
        ang = math.atan2(-y, -x)
        if k == 0:
            forma = [(-0.2, -0.12), (0.12, -0.14), (0.32, -0.02), (0.12, 0.12), (-0.2, 0.14)]
            chifre = [(0.26, -0.06), (0.46, -0.2), (0.32, 0.0)]
            feras += [(_move(_gira(forma, ang), fx, fy), 1.0), (_move(_gira(chifre, ang), fx, fy), 1.0)]
        elif k == 1:
            forma = [(-0.2, -0.06), (-0.08, -0.22), (0.0, -0.1), (0.3, -0.04), (0.3, 0.06), (-0.18, 0.12)]
            feras.append((_move(_gira(forma, ang), fx, fy), 1.0))
        else:
            asa = [(-0.36, -0.14), (0.0, 0.0), (0.36, -0.14), (0.14, 0.06), (0.0, 0.14), (-0.14, 0.06)]
            feras.append((_move(_gira(asa, ang + math.pi / 2), fx, fy), 1.0))
    F = T.polys(feras, 0.006) * janela(t, 0.15, 0.25) * (1 - rel(t, 0.6, 0.7))
    impacto = T.ring(0.1 + 0.55 * ease_out(rel(t, 0.55, 0.85), 2), 0.05) * pulso(t, 0.55, 0.9) * 1.3
    g, h = _clarao(T, t, 0.55, 0.75, r=0.26)
    G += (fumacas + F * 1.2 + impacto + g) * env
    H += (F * 0.4 + impacto * 0.6 + h) * env
    return G, H


# --------------------------------------------------- Vassouras encantadas
def _vassoura(cx, cy, ang, s=1.0):
    cabo = lamina(0, -0.55, 0, 0.1, 0.03)
    palha = [(-0.12, 0.1), (0.12, 0.1), (0.2, 0.42), (-0.2, 0.42)]
    balde = [(-0.2, -0.3), (-0.06, -0.3), (-0.08, -0.16), (-0.18, -0.16)]
    return [(_move(_gira(p, ang), cx, cy, s), 1.0) for p in (cabo, palha, balde)]


def inv_vassouras(T, t, rng):
    """Vassouras encantadas: três vassouras com baldes marcham, giram e batem no alvo, espirrando água."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    peças = []
    for k, x0 in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.08 * k
        bate = ease_in(rel(t, a0 + 0.15, a0 + 0.38), 2)
        ang = (-1.1 if x0 < 0 else 1.1 if x0 > 0 else 0.0) * (1 - bate) + (0.6 if x0 < 0 else -0.6 if x0 > 0 else 0.0) * bate
        y = -0.25 + 0.05 * math.sin(t * 20 + k) * (1 - bate)
        peças += _vassoura(x0 * (1 - 0.45 * bate), y, ang, 0.85) if t > a0 else []
    V = T.polys(peças, 0.006) * janela(t, 0.0, 0.1) * (1 - rel(t, 0.62, 0.75))
    gotas = []
    sub = np.random.default_rng(55)
    espirra = ease_out(rel(t, 0.42, 0.85), 2)
    for k in range(18):
        a = sub.uniform(-math.pi, 0)
        d = 0.1 + 0.6 * espirra * sub.uniform(0.5, 1.0)
        x, y = d * math.cos(a), 0.15 + d * math.sin(a) + 0.5 * espirra ** 2
        gotas.append(([(x, y - 0.035), (x + 0.02, y), (x, y + 0.025), (x - 0.02, y)], pulso(t, 0.42, 0.95)))
    respingo = T.ring(0.1 + 0.45 * espirra, 0.04, cy=0.15, squash=1.8) * pulso(t, 0.42, 0.85)
    G += (V * 1.1 + T.polys(gotas, 0.004) * 1.4 + respingo) * env
    H += (T.polys(gotas, 0.004) * 0.8 + respingo * 0.5) * env
    return G, H


# ---------------------------------------------------- Exército de clones
def _plankton(cx, cy, s):
    corpo = _elipse(cx, cy, 0.05 * s, 0.075 * s, 16)
    antenas = [lamina(cx - 0.02 * s, cy - 0.06 * s, cx - 0.05 * s, cy - 0.14 * s, 0.008 * s), lamina(cx + 0.02 * s, cy - 0.06 * s, cx + 0.05 * s, cy - 0.14 * s, 0.008 * s)]
    return [(corpo, 1.0)] + [(a, 1.0) for a in antenas]


def inv_clones(T, t, rng):
    """Exército de clones: um enxame de Planktons minúsculos chega correndo de todos os lados, cada um
    com o olho único aceso, e se amontoa em cima do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    sub = np.random.default_rng(2024)
    bichos, olhos = [], 0
    for k in range(16):
        a = sub.uniform(0, TAU)
        a0 = sub.uniform(0.0, 0.22)
        f = ease_out(rel(t, a0, a0 + 0.42), 1.8)
        r = 0.95 - (0.95 - sub.uniform(0.05, 0.28)) * f
        x, y = r * math.cos(a), r * math.sin(a) * 0.8 + 0.06 * math.sin(t * 40 + k) * (1 - f)
        s = 1.0 + 0.3 * sub.uniform()
        bichos += _plankton(x, y, s)
        olhos = olhos + T.gauss(x, y - 0.015 * s, 0.014, 0.014) * 2.4
    B = T.polys(bichos, 0.004)
    pancada = T.ring(0.15 + 0.4 * ease_out(rel(t, 0.55, 0.85), 2), 0.04) * pulso(t, 0.55, 0.88) * 1.2
    G += (B * 1.0 + olhos + pancada) * env
    H += (olhos * 1.2 + pancada * 0.5) * env
    return G, H


# ------------------------------------------------- Androide de combate
def inv_androide(T, t, rng):
    """Androide de combate: um punho robótico sai como foguete pelo lado, com chama e fumaça,
    acerta o alvo e solta engrenagens e faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    voa = ease_in(rel(t, 0.0, 0.42), 1.8)
    px, py = -1.0 + 1.0 * voa, -0.15 + 0.15 * voa
    punho = [(-0.06, -0.14), (0.14, -0.14), (0.18, -0.08), (0.18, 0.08), (0.14, 0.14), (-0.06, 0.14)]
    dedos = [[(0.18, -0.12 + 0.065 * k), (0.24, -0.12 + 0.065 * k), (0.24, -0.08 + 0.065 * k), (0.18, -0.08 + 0.065 * k)] for k in range(4)]
    braco = [(-0.42, -0.08), (-0.06, -0.1), (-0.06, 0.1), (-0.42, 0.08)]
    partes = [(_move(punho, px, py), 1.0), (_move(braco, px, py), 1.0)] + [(_move(d, px, py), 1.0) for d in dedos]
    P = T.polys(partes, 0.004) * (1 - rel(t, 0.46, 0.55))
    chama = sum(T.gauss(px - 0.45 - 0.08 * k, py, 0.06 + 0.02 * k, 0.04 + 0.01 * k) * (0.9 - 0.15 * k) for k in range(5)) * (1 - rel(t, 0.4, 0.5)) * 1.4
    fumaca = sum(T.gauss(-0.9 + 0.2 * k, -0.15 + 0.03 * k, 0.1, 0.07) * pulso(t, 0.05 * k, 0.05 * k + 0.6) for k in range(5)) * 0.4
    sub = np.random.default_rng(88)
    sai = ease_out(rel(t, 0.42, 0.85), 2)
    pecas = []
    for k in range(7):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.6 * sai * sub.uniform(0.6, 1.0)
        pecas.append((estrela(d * math.cos(a), d * math.sin(a) + 0.3 * sai ** 2, 0.05, t * 10 + k, 6, 0.65), pulso(t, 0.42, 0.95)))
    bum = T.ring(0.1 + 0.5 * sai, 0.05) * pulso(t, 0.42, 0.8) * 1.3
    g, h = _clarao(T, t, 0.4, 0.62, r=0.24)
    G += (P * 1.2 + chama + fumaca + T.polys(pecas, 0.004) * 1.2 + bum + g) * env
    H += (P * 0.4 + chama * 0.9 + T.polys(pecas, 0.004) * 0.5 + bum * 0.6 + h) * env
    return G, H


REGISTRO = [
    ("inv_cao", inv_cao, GRANDE, "Cão divino: lobo de sombra que salta e morde", False),
    ("inv_sombras", inv_sombras, GRANDE, "Soldados das sombras: sobem do chão e cortam", False),
    ("inv_mago", inv_mago, GRANDE, "Mago Negro: círculo mágico e esfera escura", False),
    ("inv_dragao", inv_dragao, GRANDE, "Dragão Branco: cabeça do dragão e raio branco", False),
    ("inv_gomorrah", inv_gomorrah, GRANDE, "Gomorrah: mandíbulas que se fecham", False),
    ("inv_ora", inv_ora, GRANDE, "Star Platinum: chuva de socos", False),
    ("inv_feras", inv_feras, GRANDE, "Caminho Animal: feras saindo das nuvens", False),
    ("inv_vassouras", inv_vassouras, GRANDE, "Vassouras encantadas: batem e espirram água", False),
    ("inv_clones", inv_clones, GRANDE, "Exército de clones: enxame de Planktons", False),
    ("inv_androide", inv_androide, GRANDE, "Androide de combate: soco-foguete", False),
]
