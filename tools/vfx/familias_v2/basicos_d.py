"""Ataques básicos com animação própria, lote d.

Jinwoo (adagas de Kamish e fumaça de sombra), Kaneki (quatro kagune que perfuram),
Yugi (carta que vira e solta a estrela mágica), Kaiba (carta e o raio branco do dragão),
os Cavaleiros (meteoros de Pégaso, dragão subindo, pó de diamante, corrente de
Andrômeda, asas da fênix, lótus e roda de luz do Shaka), a tiara lunar, as garras de
fogo do Charizard e o triângulo de olho que solta chama azul do Bill Cipher.
"""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, _subindo, apaga, back, contorno, ease_in, ease_out, estrela, faiscas, forma, girado,  # noqa: F401
                   jagged, janela, lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


# ------------------------------------------------------------------ ajudantes
def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


def _elipse(cx, cy, rx, ry, n=28, ang=0.0):
    return _gira([(rx * math.cos(TAU * k / n), ry * math.sin(TAU * k / n)) for k in range(n)], ang, cx, cy)


def _fechado(pts):
    return pts + [pts[0]]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.5
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.65 * k + 0.01, ang=ang + math.pi / 4, thin=0.012)) * k * 1.6
    return g, h


def _chama(cx, base, alt, larg, fase, ondula=0.25):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    lado1, lado2 = [], []
    for k in range(13):
        u = k / 12
        y = base - alt * u
        w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9 + larg * 0.35 * (1 - u) ** 3
        bal = ondula * larg * math.sin(fase + 6 * u) * u
        lado1.append((cx + w + bal, y))
        lado2.append((cx - w + bal, y))
    return lado1 + lado2[::-1]


def _chama_dir(x0, y0, ang, alt, larg, fase, ondula=0.3):
    """Língua de fogo que nasce em (x0, y0) e se estende na direção `ang`."""
    pts = _chama(0.0, 0.0, alt, larg, fase, ondula)      # sobe para −y
    # eixo da chama (−y) vira a direção ang
    return _gira(pts, ang + math.pi / 2, x0, y0)


def _desenha_carta(T, cx, cy, esc_x, ang=0.0, alt=0.56, larg=0.38):
    """Carta de duelo (borda, janela da arte, caixa de texto e faixa do nome), achatada em x ao virar."""
    w, h = larg / 2 * esc_x, alt / 2
    borda = _gira([(-w, -h), (w, -h), (w, h), (-w, h)], ang, cx, cy)
    arte = _gira([(-w * 0.78, -h * 0.7), (w * 0.78, -h * 0.7), (w * 0.78, h * 0.18), (-w * 0.78, h * 0.18)], ang, cx, cy)
    texto = _gira([(-w * 0.78, h * 0.32), (w * 0.78, h * 0.32), (w * 0.78, h * 0.8), (-w * 0.78, h * 0.8)], ang, cx, cy)
    nome = _gira([(-w * 0.78, -h * 0.9), (w * 0.4, -h * 0.9), (w * 0.4, -h * 0.8), (-w * 0.78, -h * 0.8)], ang, cx, cy)
    corpo = T.polys([(borda, 0.5)], 0.006)
    linhas = (T.polyline(_fechado(borda), 0.024) + T.polyline(_fechado(arte), 0.013) * 0.85
              + T.polyline(_fechado(texto), 0.01) * 0.6 + T.polys([(nome, 0.8)], 0.004))
    return corpo, linhas


# ------------------------------------------------------------------ Jinwoo
def adaga_de_kamish(T, t, rng):
    """Adaga de Kamish: dois cortes rápidos em X (ida e volta da adaga) com o fio brilhando e,
    das feridas, fumaça de sombra que sobe em línguas escuras e esfiapadas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cortes, fios = T.zero(), T.zero()
    for x1, y1, x2, y2, a, b in ((-0.72, -0.6, 0.66, 0.5, 0.0, 0.13), (-0.66, 0.52, 0.7, -0.5, 0.17, 0.3)):
        p = ease_out(rel(t, a, b), 2.2)
        if p <= 0:
            continue
        fim = rel(t, b + 0.1, b + 0.45)
        cortes += T.polys([(lamina(x1, y1, x2, y2, 0.075, p, fim), 1)], 0.004)
        fios += T.polys([(lamina(x1, y1, x2, y2, 0.022, p, fim), 1)], 0.002)
        if p < 1:   # a adaga na ponta do corte
            hx, hy = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
            ang = math.atan2(y2 - y1, x2 - x1)
            adaga = _gira([(-0.2, 0.0), (-0.04, -0.035), (0.14, -0.012), (0.2, 0.012), (-0.04, 0.035)], ang, hx, hy)
            cortes += T.polys([(adaga, 1.6)], 0.003)
            fios += T.polys([(adaga, 1.2)], 0.003)
    k = pulso(t, 0.17, 0.42)
    g, h = _clarao(T, k, 0.0, 0.0, 0.16, 0.55, ang=0.0)
    # fumaça de sombra: fiapos sinuosos que nascem ao longo das feridas e sobem se enrolando,
    # sobre uma névoa rala que também sobe
    sobe = rel(t, 0.2, 1.0)
    sub = np.random.default_rng(71)
    fiapos = []
    for j in range(9):
        u0 = sub.uniform(0.15, 0.85)
        lado = j % 2
        x0 = -0.7 + 1.38 * u0
        y0 = (-0.6 + 1.1 * u0) if lado == 0 else (0.52 - 1.02 * u0)
        alt = (0.35 + 0.35 * sub.uniform()) * ease_out(rel(t, 0.2 + 0.03 * (j % 4), 0.75), 1.6)
        fase = sub.uniform(0, TAU)
        if alt < 0.02:
            continue
        pts = []
        for i in range(14):
            u = i / 13
            pts.append((x0 + 0.07 * math.sin(fase + u * 5 + t * 8) * (0.3 + u), y0 - alt * u - 0.25 * sobe))
        cima, baixo = [], []
        for i, (x, y) in enumerate(pts):
            w = 0.035 * math.sin(math.pi * min(1, (i + 1) / 14)) ** 0.5 * (1 - i / 14) ** 0.6 + 0.006
            cima.append((x + w, y))
            baixo.append((x - w, y))
        fiapos.append((cima + baixo[::-1], 0.8))
    F = T.polys(fiapos, 0.012) if fiapos else T.zero()
    n = _subindo(T, 717, t, 0.07, 0.9)
    nevoa = T.zero()
    for j in range(5):
        x0 = -0.4 + 0.2 * j
        nevoa += T.gauss(x0 * 0.8, 0.05 - 0.45 * sobe, 0.1, 0.24)
    nevoa = nevoa * np.clip(0.5 + 0.5 * n, 0, 1.4) * 0.28
    vis_f = janela(t, 0.2, 0.34) * (1 - rel(t, 0.7, 1.0))
    fumo = (F * (0.7 + 0.3 * np.clip(n, -1, 1)) + nevoa) * vis_f
    G += (T.glow(cortes, 1.0, 1.2, 0.025) + fios * 1.2 + g + fumo * 1.1) * env
    H += (fios * 1.6 + cortes * 0.25 + h) * env
    return G, H


# ------------------------------------------------------------------ Kaneki
def _kagune(T, pts, larg, prog):
    """Tentáculo rinkaku: tubo grosso que afina até a ponta de lança, com sulcos entre os segmentos
    (as "escamas") e um fio claro no meio."""
    n = len(pts) - 1
    ate = max(2, int(n * prog))
    cima, baixo, sulcos = [], [], []
    for i in range(ate + 1):
        x, y = pts[i]
        xa, ya = pts[max(0, i - 1)]
        xb, yb = pts[min(ate, i + 1)]
        a = math.atan2(yb - ya, xb - xa)
        u = i / max(ate, 1)
        w = larg * (1.0 - 0.55 * u)
        nx, ny = -math.sin(a) * w, math.cos(a) * w
        cima.append((x + nx, y + ny))
        baixo.append((x - nx, y - ny))
        if i % 3 == 1 and i < ate - 1:
            sulcos.append((x + nx * 1.1 - math.cos(a) * w * 0.4, y + ny * 1.1 - math.sin(a) * w * 0.4,
                           x - nx * 1.1 - math.cos(a) * w * 0.4, y - ny * 1.1 - math.sin(a) * w * 0.4, 1.0))
    (xa, ya), (xb, yb) = pts[ate - 1], pts[ate]
    a = math.atan2(yb - ya, xb - xa)
    w = larg * 0.5
    ponta = [(xb + math.cos(a + 1.6) * w * 1.3, yb + math.sin(a + 1.6) * w * 1.3), (xb + math.cos(a) * 0.24, yb + math.sin(a) * 0.24),
             (xb + math.cos(a - 1.6) * w * 1.3, yb + math.sin(a - 1.6) * w * 1.3)]
    corpo = T.polys([(cima + baixo[::-1], 1.0), (ponta, 1.1)], 0.005)
    S = T.lines(sulcos, 0.03, 0.004) if sulcos else T.zero()
    corpo = corpo * (1 - 0.85 * np.clip(S, 0, 1))
    fio = T.polyline(pts[: ate + 1], 0.012, blur=0.004) + T.polys([(ponta, 0.7)], 0.004)
    return corpo, fio


def kagune(T, t, rng):
    """Kagune: quatro tentáculos rinkaku vermelhos, feitos de escamas, descem do alto por trás do
    atacante em curva, perfuram o alvo um após o outro (respingos e rachadura) e recuam."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    alvos = [(0.0, -0.1), (-0.1, 0.06), (0.1, 0.02), (0.02, 0.12)]
    corpo, miolo, furos = T.zero(), T.zero(), T.zero()
    for k in range(4):
        a = 0.03 + 0.07 * k
        p = ease_out(rel(t, a, a + 0.2), 2.2) * (1 - 0.6 * ease_in(rel(t, 0.72, 0.95), 2))
        if p <= 0.02:
            continue
        x0, y0, cx1, cy1 = ((-0.75, -1.1, -0.35, -0.75), (-1.1, -0.75, -0.75, -0.05), (-0.2, -1.1, 0.25, -0.55), (-1.1, -0.15, -0.55, 0.5))[k]
        tx, ty = alvos[k]
        pts = []
        for i in range(25):
            u = i / 24
            x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx1 + u * u * tx
            y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy1 + u * u * ty
            pts.append((x + 0.025 * math.sin(u * 6 + t * 10 + k), y))
        c, m = _kagune(T, pts, 0.085, max(0.08, p))
        corpo += c
        miolo += m
        bate = pulso(t, a + 0.14, a + 0.4)
        furos += (T.gauss(tx, ty, 0.09, 0.09) * 1.6 + T.ring(0.05 + 0.2 * ease_out(rel(t, a + 0.14, a + 0.4), 2), 0.025, tx, ty)) * bate
    sub = np.random.default_rng(41)
    gotas = []
    tt = rel(t, 0.2, 1.0)
    if tt > 0:
        for _ in range(22):
            a = sub.uniform(-1.0, 1.2)
            v = sub.uniform(0.4, 0.8)
            gx = math.cos(a) * v * ease_out(tt, 2) + 0.05
            gy = math.sin(a) * v * ease_out(tt, 2) * 0.7 + 0.5 * tt * tt
            gotas.append((gx, gy, (1 - tt) ** 1.2 * sub.uniform(0.5, 1)))
    gotas = T.splats(gotas, 0.022) if gotas else T.zero()
    rach = T.zero()
    for k in range(6):
        a = k / 6 * TAU + 0.4
        rach += T.polyline(jagged(sub, 0, 0, 0.42 * math.cos(a), 0.42 * math.sin(a), 4, 0.3), 0.012)
    rach = rach * pulso(t, 0.3, 0.85)
    G += (corpo * 1.1 + T.blur(corpo, 0.03) * 0.35 + furos + T.glow(gotas, 1.0, 1.0, 0.02) + rach * 1.2) * env
    H += (miolo * 1.1 + furos * 0.7 + rach * 0.6 + gotas * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Yugi
def carta_magica(T, t, rng):
    """Carta de ataque: a carta surge de frente girando no próprio eixo, brilha com um olho na
    arte e se desfaz numa estrela mágica de cinco pontas que estoura no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    vira = rel(t, 0.0, 0.26)
    esc_x = abs(math.cos(math.pi * (1 - ease_out(vira, 2)))) * janela(t, 0, 0.04)
    some_carta = 1 - rel(t, 0.42, 0.55)
    cy = -0.05 - 0.08 * ease_out(vira, 2)
    corpo, linhas = _desenha_carta(T, 0.0, cy, max(esc_x, 0.03), 0.0, 0.62, 0.42)
    brilho = pulso(t, 0.22, 0.5)
    olho = T.zero()
    if esc_x > 0.3:
        el = _elipse(0.0, cy - 0.08, 0.09 * esc_x, 0.045, 24)
        olho = T.polyline(_fechado(el), 0.012) + T.gauss(0.0, cy - 0.08, 0.022 * esc_x + 0.003, 0.022) * 1.4
    carta = (corpo + linhas * 1.3 + olho * 1.2) * some_carta * (1 + brilho * 0.8)
    aura = T.gauss(0.0, cy, 0.26 * max(esc_x, 0.2), 0.36) * brilho * 1.2
    e = ease_out(rel(t, 0.42, 0.7), 2.4)
    ke = pulso(t, 0.4, 0.98)
    est, estH = T.zero(), T.zero()
    if ke > 0:
        r = 0.12 + 0.5 * e
        ang = -math.pi / 2 + 1.4 * rel(t, 0.42, 1)
        pts = estrela(0.0, -0.02, r, ang, 5, 0.42)
        est = (T.polys([(pts, 0.5)], 0.006) + T.polyline(_fechado(pts), 0.022) * 1.2) * ke
        estH = T.polyline(_fechado(pts), 0.012) * ke
    anel = T.ring(0.15 + 0.62 * ease_out(rel(t, 0.42, 0.85), 2), 0.03) * pulso(t, 0.42, 0.9)
    g, h = _clarao(T, pulso(t, 0.4, 0.68), 0, 0, 0.22, 0.85, ang=0.0)
    pequenas = []
    tt = rel(t, 0.45, 1)
    if tt > 0:
        for j in range(8):
            a = j / 8 * TAU + 0.2
            d = 0.25 + 0.5 * ease_out(tt, 2)
            pequenas.append((estrela(d * math.cos(a), d * math.sin(a), 0.06 * (1 - tt) + 0.01, a + tt * 4, 4, 0.35), 1.0))
    P = T.polys(pequenas, 0.004) if pequenas else T.zero()
    G += (carta * 1.1 + aura + est * 1.2 + anel + g + P * 1.3) * env
    H += (linhas * 0.5 * some_carta + olho * 0.8 * some_carta + estH * 1.2 + est * 0.4 + h + P * 0.7 + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Kaiba
def carta_dragao(T, t, rng):
    """Carta agressiva: a carta vira na frente do atacante, a arte se acende e dela sai o raio
    branco do dragão (feixe grosso com anéis de pressão) que explode no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cx, cy = -0.68, -0.18
    vira = rel(t, 0.0, 0.2)
    esc_x = abs(math.sin(math.pi / 2 * ease_out(vira, 2))) * janela(t, 0, 0.03)
    some_carta = 1 - rel(t, 0.62, 0.8)
    corpo, linhas = _desenha_carta(T, cx, cy, max(esc_x, 0.03), -0.12, 0.5, 0.34)
    acende = janela(t, 0.16, 0.26)
    nucleo_carta = T.gauss(cx, cy - 0.06, 0.07, 0.07) * acende * 2.2 * some_carta
    carta = (corpo + linhas * 1.3) * some_carta
    sai = ease_out(rel(t, 0.24, 0.4), 2)
    liga = janela(t, 0.24, 0.27) * (1 - rel(t, 0.62, 0.8))
    fx, fy = cx + (0.05 - cx) * sai, cy + (0.0 - cy) * sai
    ang = math.atan2(-cy, -cx)
    feixe = miolo = corpo_feixe = aneis = T.zero()
    if sai > 0:
        feixe = T.polys([(lamina(cx, cy, fx + (fx - cx) * 0.08, fy + (fy - cy) * 0.08, 0.17), 1.0)], 0.02)
        miolo = T.polyline([(cx, cy), (fx, fy)], 0.07, blur=0.012)
        corpo_feixe = T.polyline([(cx, cy), (fx, fy)], 0.22, blur=0.035)
        aneis = T.zero()
        for j in range(3):
            u = (rel(t, 0.28, 0.7) * 2 + j / 3) % 1
            if sai > u:
                px, py = cx + (fx - cx) * u, cy + (fy - cy) * u
                aneis = aneis + T.polyline(_fechado(_elipse(px, py, 0.04, 0.21 * (0.6 + 0.4 * u), 20, ang)), 0.014)
    feixe_tudo = (feixe + corpo_feixe + aneis) * liga
    k = pulso(t, 0.36, 0.86)
    g, h = _clarao(T, k, 0.0, 0.0, 0.3, 1.0, ang=ang)
    bum = T.ring(0.12 + 0.62 * ease_out(rel(t, 0.38, 0.85), 2), 0.05) * pulso(t, 0.38, 0.9) * 1.2
    fa = faiscas(T, np.random.default_rng(33), t, 20, 0.8, 0.03, cone=(-1.2, 1.2), gravidade=0.2, inicio=0.38)
    G += (carta * 1.1 + nucleo_carta + feixe_tudo * 1.3 + g + bum + T.glow(fa, 1, 1, 0.02)) * env
    H += (linhas * 0.5 * some_carta + nucleo_carta + (miolo * 2.0 + corpo_feixe * 0.8 + aneis * 0.6) * liga + h + bum * 0.5 + fa * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Seiya
def meteoros_de_pegaso(T, t, rng):
    """Meteoros de Pégaso: dezenas de socos viram meteoros azuis que riscam da esquerda em leque,
    cada um acerta um ponto do alvo com um estalo de luz; no fim um clarão de todos juntos."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(1234)
    rastros, cabecas, estalos = [], [], []
    n = 50
    for j in range(n):
        t0 = 0.0 + 0.58 * j / n + sub.uniform(-0.02, 0.02)
        dur = sub.uniform(0.1, 0.15)
        tx, ty = sub.normal(0, 0.2), sub.normal(0, 0.2)
        ang = sub.uniform(-0.35, 0.35)
        dist = sub.uniform(1.0, 1.4)
        cauda = 0.45 + 0.2 * sub.uniform()
        sx, sy = tx - math.cos(ang) * dist, ty - math.sin(ang) * dist
        p = rel(t, t0, t0 + dur)
        if 0 < p < 1:
            hx, hy = sx + (tx - sx) * p, sy + (ty - sy) * p
            rastros.append((hx - math.cos(ang) * cauda, hy - math.sin(ang) * cauda, hx, hy, 1.0))
            cabecas.append((hx, hy, 1.0))
        q = rel(t, t0 + dur, t0 + dur + 0.1)
        if 0 < q < 1 or (p >= 1 and q == 0):
            estalos.append((tx, ty, (1 - q) ** 1.5))
    R = T.tapered(rastros, 0.09) if rastros else T.zero()
    C = T.splats(cabecas, 0.045) if cabecas else T.zero()
    E = T.zero()
    for x, y, w in estalos:
        E += T.flare(x, y, 0.28 * w + 0.01, 0.3, 0.02) * w + T.gauss(x, y, 0.05, 0.05) * w
    k = pulso(t, 0.62, 0.95)
    g, h = _clarao(T, k, 0, 0, 0.3, 1.0, ang=0.0)
    anel = T.ring(0.15 + 0.55 * ease_out(rel(t, 0.64, 0.97), 2), 0.04) * pulso(t, 0.64, 0.99)
    G += (T.glow(R, 0.9, 1.1, 0.025) + C * 1.5 + E * 1.2 + g + anel) * env
    H += (R * 0.5 + C * 1.4 + E * 1.0 + h + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Shiryu
def _cabeca_dragao(hx, hy, ang, esc, abre=0.25):
    """Cabeça de dragão oriental de perfil apontando para `ang` (o eixo +x local é o focinho):
    testa com sobrancelha, focinho comprido, mandíbula que abre, chifres e juba para trás, bigodes."""
    cabeca = [(-0.22, -0.02), (-0.2, -0.12), (-0.08, -0.16), (0.0, -0.12), (0.05, -0.14), (0.12, -0.09), (0.28, -0.08),
              (0.36, -0.05), (0.37, -0.01), (0.3, 0.0), (0.06, 0.02), (-0.1, 0.06), (-0.2, 0.05)]
    mand = _gira([(0.0, 0.0), (0.24, 0.0), (0.27, 0.03), (0.16, 0.05), (-0.04, 0.06)], abre * 0.7, 0.05, 0.03)
    presa = [(0.22, 0.0), (0.245, 0.05), (0.26, 0.0)]
    chifre1 = [(-0.08, -0.14), (-0.24, -0.27), (-0.44, -0.31), (-0.27, -0.22), (-0.13, -0.1)]
    chifre2 = [(-0.15, -0.1), (-0.3, -0.16), (-0.47, -0.15), (-0.3, -0.1), (-0.17, -0.05)]
    juba = [[(-0.2, -0.04), (-0.42, -0.02), (-0.21, 0.02)], [(-0.19, 0.02), (-0.4, 0.1), (-0.17, 0.06)], [(-0.12, 0.06), (-0.28, 0.2), (-0.06, 0.07)]]

    def f(pts):
        return _gira([(x * esc, y * esc) for x, y in pts], ang, hx, hy)
    bigode = [f([(0.34, -0.03), (0.3, -0.13), (0.2, -0.2), (0.06, -0.24), (-0.06, -0.22)]),
              f([(0.32, 0.0), (0.26, 0.12), (0.12, 0.2), (-0.06, 0.22), (-0.24, 0.18)])]
    olho = f([(0.05, -0.09)])[0]
    return [f(cabeca), f(mand), f(presa), f(chifre1), f(chifre2)] + [f(j) for j in juba], bigode, olho


def punho_do_dragao(T, t, rng):
    """Punho do Dragão (Rozan Shoryuha): o gancho sobe de baixo e acerta o alvo; atrás dele a
    silhueta de um dragão verde-água sobe em espiral até o alto e ruge."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sobe = ease_out(rel(t, 0.0, 0.6), 1.5)
    topo = 0.95 - 1.42 * sobe
    pts = []
    for i in range(70):
        u = i / 69
        y = 1.15 - (1.15 - topo) * u
        a = u * 2.6 * math.pi + 0.6
        r = 0.5 * (1 - 0.4 * u)
        pts.append((r * math.sin(a), y + 0.08 * math.cos(a), u, math.cos(a)))
    corpo = T.zero()
    espinhos = []
    for (x1, y1, _, _), (x2, y2, u2, z2) in zip(pts, pts[1:]):
        w = 0.035 + 0.06 * math.sin(math.pi * min(1, u2 * 1.15)) ** 0.7
        corpo += T.lines([(x1, y1, x2, y2, 0.75 + 0.35 * z2)], w * 2, 0.008)
    for i in range(6, 66, 6):
        (x1, y1, _, _), (x2, y2, _, _) = pts[i], pts[i + 2]
        a = math.atan2(y2 - y1, x2 - x1) - math.pi / 2
        espinhos.append(([(x1, y1), ((x1 + x2) / 2 + math.cos(a) * 0.09, (y1 + y2) / 2 + math.sin(a) * 0.09), (x2, y2)], 0.9))
    corpo = np.clip(corpo, 0, 1.3)
    hx, hy = pts[-1][0], pts[-1][1]
    ang = -1.05 + 0.15 * math.sin(t * 9)
    abre = 0.2 + 0.6 * pulso(t, 0.45, 0.85)
    partes, bigode, olho = _cabeca_dragao(hx + 0.04, hy, ang, 0.9, abre)
    cab = T.polys([(pp, 1.0) for pp in partes], 0.005)
    big = sum(T.polyline(b, 0.012) for b in bigode)
    olhoG = T.gauss(olho[0], olho[1], 0.022, 0.022) * 2.4
    vis = janela(t, 0.04, 0.16) * (1 - rel(t, 0.72, 1.0))
    drag = (T.glow(corpo, 0.9, 1.0, 0.03) + T.polys(espinhos, 0.004) * 0.9 + cab * 1.3 + big) * vis
    dragH = (corpo * 0.25 + cab * 0.4 + olhoG) * vis
    py = 0.9 - 1.2 * ease_out(rel(t, 0.0, 0.3), 2)
    punho = [(-0.09, 0.05), (-0.11, -0.07), (-0.05, -0.14), (0.05, -0.14), (0.11, -0.07), (0.09, 0.05), (0.05, 0.18), (-0.05, 0.18)]
    P = T.polys([(_move(punho, 0.0, py), 1.0)], 0.006) * (1 - rel(t, 0.3, 0.42))
    rastro = T.polys([(lamina(0.0, 0.95, 0.0, py, 0.08), 1.0)], 0.02) * (1 - rel(t, 0.28, 0.5))
    k = pulso(t, 0.24, 0.55)
    g, h = _clarao(T, k, 0.0, -0.05, 0.22, 0.75, ang=0.0)
    est = T.polys([(estrela(0.0, -0.05, 0.28 * k + 0.01, -math.pi / 2, 8, 0.4), 1.0)], 0.006) * k
    G += (drag + P * 1.3 + rastro * 0.9 + g + est) * env
    H += (dragH + P * 0.6 + rastro * 0.4 + h + est * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Hyoga
def _floco(cx, cy, r, ang):
    """Estrela de gelo de seis pontas: seis raios com dois galhos cada."""
    segs = []
    for k in range(6):
        a = ang + k * math.pi / 3
        segs.append((cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r, 1.0))
        mx, my = cx + math.cos(a) * r * 0.58, cy + math.sin(a) * r * 0.58
        for s in (-1, 1):
            b = a + s * 0.75
            segs.append((mx, my, mx + math.cos(b) * r * 0.32, my + math.sin(b) * r * 0.32, 0.8))
    return segs



# ------------------------------------------------------------------ Shun
def corrente_de_andromeda(T, t, rng):
    """Corrente de Andrômeda: a corrente voa da esquerda em zigue-zague, elos ovais alternando de
    lado, com a ponta triangular na frente; a ponta crava no alvo com um estalo e a corrente recua."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    vai = ease_out(rel(t, 0.0, 0.34), 1.8)
    volta = ease_in(rel(t, 0.62, 0.95), 2)
    prog = vai * (1 - 0.85 * volta)
    zig = 0.32 * (1 - 0.6 * rel(t, 0.3, 0.5))
    caminho = []
    for i in range(121):
        u = i / 120
        caminho.append((-1.05 + 1.05 * u, zig * math.sin(u * 3 * math.pi) * (1 - u) ** 0.4))
    n = int(120 * prog)
    elos, elosH = T.zero(), T.zero()
    if n >= 4:
        lista = []
        for i in range(0, n - 2, 4):
            (x1, y1), (x2, y2) = caminho[i], caminho[i + 2]
            a = math.atan2(y2 - y1, x2 - x1)
            esp = 1.0 if (i // 4) % 2 == 0 else 0.45
            lista.append(_elipse((x1 + x2) / 2, (y1 + y2) / 2, 0.055, 0.03 * esp, 16, a))
        for el in lista:
            elos += T.polyline(_fechado(el), 0.016)
        elos = np.clip(elos, 0, 1.2)
        elosH = elos * 0.6
        hx, hy = caminho[n]
        bx, by = caminho[max(0, n - 4)]
        a = math.atan2(hy - by, hx - bx)
        ponta = _gira([(0.15, 0.0), (-0.06, -0.09), (-0.02, 0.0), (-0.06, 0.09)], a, hx, hy)
        P = T.polys([(ponta, 1.0)], 0.004)
        elos += P * 1.5 + T.gauss(hx, hy, 0.06, 0.06) * 0.8
        elosH += P * 0.8
    g, h = _clarao(T, pulso(t, 0.3, 0.6), 0.08, 0.0, 0.16, 0.6, ang=0.0)
    anel = T.ring(0.08 + 0.35 * ease_out(rel(t, 0.32, 0.65), 2), 0.025, 0.08, 0.0) * pulso(t, 0.32, 0.7)
    fa = faiscas(T, np.random.default_rng(66), t, 14, 0.55, 0.025, cone=(-1.0, 1.0), gravidade=0.2, cx=0.08, inicio=0.32)
    G += (T.glow(elos, 1.0, 0.9, 0.02) + g + anel + T.glow(fa, 1, 1, 0.02)) * env
    H += (elosH + h + anel * 0.4 + fa * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Ikki
def punho_da_fenix(T, t, rng):
    """Punho da Fênix: o soco em chamas vem da esquerda e acerta; no impacto duas asas de fogo de
    fênix se abrem do alvo e batem, com a cabeça da ave em chamas subindo e brasas caindo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vai = ease_in(rel(t, 0.0, 0.2), 1.6)
    px = -0.95 + 0.9 * vai
    punho = [(-0.1, -0.09), (0.06, -0.11), (0.12, -0.05), (0.12, 0.05), (0.06, 0.11), (-0.1, 0.09)]
    some_punho = 1 - rel(t, 0.2, 0.3)
    P = T.polys([(_move(punho, px, 0.0, 1.4), 1.0)], 0.006) * some_punho
    lingua = T.polys([(_chama_dir(px - 0.08, 0.0, math.pi, 0.7, 0.17, t * 30, 0.4), 0.8)], 0.02) * some_punho
    abre = back(rel(t, 0.2, 0.5), 1.4)
    bate = 0.22 * math.sin(rel(t, 0.5, 0.9) * math.pi)
    asas, nucleo = T.zero(), T.zero()
    if abre > 0:
        formas, fios = [], []
        for lado in (-1, 1):
            for k in range(6):
                a = -0.15 - k * 0.2 + bate
                comp = (0.78 + 0.16 * (k in (1, 2)) - 0.05 * k) * abre
                x2, y2 = lado * math.cos(a) * comp, math.sin(a) * comp * 0.95 - 0.08
                formas.append((lamina(lado * 0.06, -0.02, x2, y2, 0.085 - 0.006 * k), 1 - 0.08 * k))
                fios.append((lamina(lado * 0.06, -0.02, x2 * 0.75, y2 * 0.75, 0.018), 1.0))
        asas = T.polys(formas, 0.012)
        nucleo = T.polys(fios, 0.005)
        n = _subindo(T, 921, t, 0.05, 1.4)
        asas = asas * (0.75 + 0.25 * np.clip(n, -1, 1))
    # pescoço e cabeça da ave subindo do meio das asas, bico para a frente e crista de fogo
    cab_k = janela(t, 0.28, 0.42) * (1 - rel(t, 0.8, 1))
    hy = -0.18 - 0.3 * ease_out(rel(t, 0.28, 0.6), 2)
    C = T.zero()
    cauda = T.zero()
    if cab_k > 0:
        pesc = lamina(0.0, 0.08, 0.02, hy + 0.02, 0.07)
        cab = _elipse(0.03, hy, 0.075, 0.06, 18)
        bico = [(0.08, hy - 0.035), (0.24, hy + 0.02), (0.08, hy + 0.03)]
        crista = [(_chama_dir(-0.01 - 0.02 * j, hy - 0.03, -math.pi / 2 - 0.7 - 0.35 * j, 0.24 - 0.03 * j, 0.045, t * 30 + j, 0.5), 0.85) for j in range(3)]
        C = T.polys([(pesc, 0.9), (cab, 1.0), (bico, 1.0)] + crista, 0.006) * cab_k
        # cauda: línguas de fogo que caem do corpo para baixo, abrindo em leque
        cauda = T.polys([(_chama_dir(0.0, 0.08, math.pi / 2 + 0.35 * (j - 1), 0.5 * cab_k + 0.02, 0.08, t * 25 + j, 0.6), 0.7) for j in range(3)], 0.015)
    g, h = _clarao(T, pulso(t, 0.18, 0.5), 0.0, 0.0, 0.25, 0.85, ang=0.0)
    penas = []
    sub = np.random.default_rng(91)
    for _ in range(18):
        f = rel(t, 0.35 + sub.uniform(0, 0.2), 1.0)
        penas.append((sub.uniform(-0.75, 0.75), -0.35 + f * 0.9, math.sin(math.pi * f) * sub.uniform(0.4, 1)))
    G += (P * 1.3 + lingua + T.glow(asas, 1.1, 1.1, 0.03) + C * 1.2 + cauda + g + T.splats(penas, 0.014)) * env
    H += (P * 0.7 + lingua * 0.3 + nucleo * 1.2 + C * 0.5 + h + T.splats(penas, 0.008) * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Shaka
def rendicao(T, t, rng):
    """Rendição (Tesouro do Céu em miniatura): atrás do alvo gira uma roda de luz de oito raios e,
    sobre ele, uma flor de lótus dourada abre pétala por pétala; no fim um pulso de luz sai da flor."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    rr = ease_out(rel(t, 0.0, 0.3), 2.0)
    rot = 1.6 * t
    roda, rodaH = T.zero(), T.zero()
    cx, cy = 0.0, -0.08
    if rr > 0:
        R = 0.62 * rr
        roda = T.ring(R, 0.022, cx, cy) * 1.2 + T.ring(R * 0.3, 0.018, cx, cy)
        raios = []
        for k in range(8):
            a = rot + k * math.pi / 4
            raios.append((cx + math.cos(a) * R * 0.3, cy + math.sin(a) * R * 0.3, cx + math.cos(a) * R, cy + math.sin(a) * R, 1.0))
        roda += T.lines(raios, 0.014) * 0.9
        nos = [(cx + math.cos(rot + k * math.pi / 4 + math.pi / 8) * R, cy + math.sin(rot + k * math.pi / 4 + math.pi / 8) * R, 1.0) for k in range(8)]
        roda += T.splats(nos, 0.022) * 0.8
        rodaH = roda * 0.4
    vis_roda = janela(t, 0, 0.1) * (1 - rel(t, 0.75, 1))
    bx, by = 0.0, 0.3
    petalas, linhas = [], T.zero()
    for m, (n, comp, larg, a0, tom) in enumerate(((7, 0.62, 0.15, 0.12, 0.58), (5, 0.48, 0.13, 0.22, 0.8))):
        abre = back(rel(t, a0, a0 + 0.3), 1.5)
        if abre <= 0:
            continue
        leque = (2.4 if m == 0 else 1.7) * abre
        for k in range(n):
            a = -math.pi / 2 + (k / (n - 1) - 0.5) * leque
            c = comp * (0.6 + 0.4 * abre)
            pts = lamina(bx, by, bx + math.cos(a) * c, by + math.sin(a) * c, larg)
            petalas.append((pts, tom))
            linhas += T.polyline(_fechado(pts), 0.012)
    L = T.polys(petalas, 0.004) if petalas else T.zero()
    pulso_anel = T.ring(0.1 + 0.7 * ease_out(rel(t, 0.5, 0.95), 2), 0.04) * pulso(t, 0.5, 0.95)
    g, h = _clarao(T, pulso(t, 0.45, 0.75), 0.0, 0.0, 0.18, 0.75, ang=0.0)
    vis = apaga(t, 0.8, 1)
    G += (roda * vis_roda + (L + linhas * 0.9 + T.gauss(0, 0.05, 0.08, 0.06) * janela(t, 0.3, 0.5)) * vis + pulso_anel + g) * env
    H += (rodaH * vis_roda + (linhas * 0.8 + L * 0.25) * vis + pulso_anel * 0.4 + h) * env
    return G, H


# ------------------------------------------------------------------ Sailor Moon
def tiara_lunar(T, t, rng):
    """Tiara lunar: a tiara vira um disco de luz girando (aro com a lua crescente no centro) que
    voa da esquerda deixando rastro e acerta o alvo com um brilho em estrela e um anel."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    voa = ease_in(rel(t, 0.0, 0.32), 1.3)
    dx = -0.95 + 0.95 * voa
    dy = -0.22 * math.sin(math.pi * voa)
    esc = 1 + 0.4 * ease_out(rel(t, 0.32, 0.55), 2)
    vis_disco = 1 - rel(t, 0.42, 0.62)
    giro = t * 26
    sq = 0.82 + 0.08 * math.sin(giro)
    disco = T.ring(0.23 * esc, 0.035, dx, dy, squash=1 / sq) * 1.2 + T.ring(0.16 * esc, 0.018, dx, dy, squash=1 / sq) * 0.7
    lua = T.arc_band(0.13 * esc, 0.05, -2.3, 2.3, 1.0, math.pi - 0.5, dx, dy, crescente=True) * 1.8
    rad = [(dx + math.cos(giro + k * TAU / 3) * 0.23 * esc, dy + math.sin(giro + k * TAU / 3) * 0.23 * esc * sq, 1.0) for k in range(3)]
    D = (disco + lua + T.splats(rad, 0.02)) * vis_disco
    rastro = T.zero()
    if voa > 0 and t < 0.45:
        pts = []
        for i in range(20):
            v = max(0.0, voa - 0.3 * i / 19)
            pts.append((-0.95 + 0.95 * v, -0.22 * math.sin(math.pi * v)))
        rastro = (T.polyline(pts, 0.18, blur=0.04) * 0.5 + T.polyline(pts, 0.05, blur=0.01) * 0.6) * (1 - rel(t, 0.3, 0.45))
    k = pulso(t, 0.3, 0.7)
    g, h = _clarao(T, k, 0, 0, 0.2, 1.0, ang=0.0)
    estr = T.polys([(estrela(0.0, 0.0, 0.3 * k + 0.01, -math.pi / 2, 4, 0.25), 1.0)], 0.006) * k
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.33, 0.8), 2), 0.035) * pulso(t, 0.33, 0.85)
    sub = np.random.default_rng(23)
    brilhos = []
    tt = rel(t, 0.36, 1)
    for _ in range(10):
        a = sub.uniform(0, TAU)
        d = 0.2 + 0.5 * ease_out(tt, 2) * sub.uniform(0.6, 1)
        if tt > 0:
            brilhos.append((estrela(d * math.cos(a), d * math.sin(a), 0.05 * (1 - tt) + 0.005, 0.0, 4, 0.3), 1.0))
    Bp = T.polys(brilhos, 0.003) if brilhos else T.zero()
    kl = pulso(t, 0.36, 0.95)
    lua_grande = T.arc_band(0.3 + 0.08 * rel(t, 0.36, 1), 0.1, -2.3, 2.3, 1.0, math.pi - 0.5, 0, 0, crescente=True) * kl
    G += (D * 1.2 + rastro + g + estr * 1.2 + anel + Bp * 1.3 + lua_grande * 1.3) * env
    H += (D * 0.6 + lua * 0.6 * vis_disco + rastro * 0.4 + h + estr * 0.8 + anel * 0.4 + Bp * 0.8 + lua_grande * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Charizard


# ------------------------------------------------------------------ Bill Cipher
def chama_do_triangulo(T, t, rng):
    """Chama do triângulo: um triângulo de tijolos com um olho surge acima do alvo, pisca, o olho
    se abre e ele derrama chamas azuis que envolvem o alvo, com a imagem tremendo de leve."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    surge = back(rel(t, 0.0, 0.22), 1.8)
    tremor = 0.015 * math.sin(t * 90) * pulso(t, 0.3, 0.8)
    cx, cy = tremor, -0.4
    s = 0.38 * surge
    vis = 1 - rel(t, 0.72, 0.92)
    tri, triH = T.zero(), T.zero()
    if s > 0.01:
        vt = [(cx, cy - s), (cx + s * 1.05, cy + s * 0.68), (cx - s * 1.05, cy + s * 0.68)]
        tri = T.polyline(_fechado(vt), 0.026) * 1.3 + T.polys([(vt, 0.3)], 0.004)
        tij = []
        for j in range(2):
            yy = cy + s * (0.38 + 0.15 * j)
            meia = (yy - (cy - s)) / (s * 1.68) * s * 1.05
            tij.append((cx - meia * 0.92, yy, cx + meia * 0.92, yy, 0.6))
        tri += T.lines(tij, 0.008)
        # a cartola pequena no topo
        topo_y = cy - s
        aba = [(cx - s * 0.32, topo_y + 0.012), (cx + s * 0.32, topo_y + 0.012), (cx + s * 0.32, topo_y - 0.012), (cx - s * 0.32, topo_y - 0.012)]
        copa = [(cx - s * 0.18, topo_y - 0.01), (cx + s * 0.18, topo_y - 0.01), (cx + s * 0.18, topo_y - s * 0.42), (cx - s * 0.18, topo_y - s * 0.42)]
        tri += T.polys([(aba, 1.0), (copa, 0.85)], 0.004)
        abre = janela(t, 0.12, 0.2) * (1 - pulso(t, 0.22, 0.3))
        ey, ex = cy + s * 0.1, s * 0.42
        ab = max(0.05, abre) * s * 0.28
        cima = [(cx - ex + 2 * ex * k / 16, ey - ab * math.sin(math.pi * k / 16)) for k in range(17)]
        baixo = [(cx - ex + 2 * ex * k / 16, ey + ab * math.sin(math.pi * k / 16)) for k in range(17)]
        olho = T.polyline(cima, 0.014) + T.polyline(baixo, 0.014)
        pupila = T.polys([([(cx, ey - ab * 0.95), (cx + s * 0.05, ey), (cx, ey + ab * 0.95), (cx - s * 0.05, ey)], 1.0)], 0.003) * (abre > 0.3)
        tri += olho * 1.2 + pupila * 1.5
        triH = T.polyline(_fechado(vt), 0.01) * 0.8 + olho * 0.9 + pupila * 1.5
    cai = rel(t, 0.28, 0.45)
    jorro = T.zero()
    if cai > 0:
        jorro = T.polys([(lamina(cx, cy + 0.2, 0.0, 0.25, 0.22 * (1 - 0.5 * cai), min(1.0, cai * 1.5)), 0.6)], 0.03) * pulso(t, 0.28, 0.6)
    chamas = []
    for k in range(7):
        x = -0.42 + 0.84 * k / 6
        a0 = 0.36 + 0.02 * abs(k - 3)
        alt = 0.62 * ease_out(rel(t, a0, a0 + 0.18), 2) * (1 - 0.3 * abs(k - 3) / 3) * (0.75 + 0.3 * abs(math.sin(t * 27 + k * 2.3)))
        if alt > 0.01:
            chamas.append((_chama(x, 0.45, alt, 0.11, t * 33 + k * 1.7, 0.7), 0.8))
    C = T.polys(chamas, 0.015) if chamas else T.zero()
    n = _subindo(T, 1313, t, 0.05, 1.4)
    C = C * (0.75 + 0.3 * np.clip(n, -1, 1)) * (1 - rel(t, 0.78, 1))
    if 0.45 < t < 0.8:   # "glitch": uma faixa horizontal da chama escorrega para o lado
        desl = int(0.03 * T.W / 2) * (1 if int(t * 40) % 2 else -1)
        faixa = np.abs(T.V - 0.15 - 0.2 * math.sin(t * 13)) < 0.04
        C = np.where(faixa, np.roll(C, desl, axis=1), C)
    G += (tri * 1.1 * vis + jorro + C * 1.2 + T.gauss(0, 0.2, 0.3, 0.2) * pulso(t, 0.35, 0.85) * 0.6) * env
    H += (triH * vis + C * 0.3 + jorro * 0.4) * env
    return G, H


REGISTRO = [
    ("adaga_de_kamish", adaga_de_kamish, GRANDE, "Jinwoo: dois cortes de adaga em X e fumaça de sombra subindo", False),
    ("kagune", kagune, GRANDE, "Kaneki: quatro kagune segmentados descem e perfuram", False),
    ("carta_magica", carta_magica, GRANDE, "Yugi: carta vira, brilha e solta estrela mágica", False),
    ("carta_dragao", carta_dragao, GRANDE, "Kaiba: carta vira e solta o raio branco do dragão", False),
    ("meteoros_de_pegaso", meteoros_de_pegaso, GRANDE, "Seiya: dezenas de socos-meteoro azuis riscando o alvo", False),
    ("punho_do_dragao", punho_do_dragao, GRANDE, "Shiryu: gancho que sobe com o dragão em espiral", False),
    ("corrente_de_andromeda", corrente_de_andromeda, GRANDE, "Shun: corrente em zigue-zague com ponta triangular", False),
    ("rendicao", rendicao, GRANDE, "Shaka: lótus dourada abre sobre a roda de luz", False),
    ("tiara_lunar", tiara_lunar, GRANDE, "Sailor Moon: tiara-disco com lua crescente que acerta com brilho", False),
    ("chama_do_triangulo", chama_do_triangulo, GRANDE, "Bill Cipher: triângulo de olho que derrama chama azul", False),
]
