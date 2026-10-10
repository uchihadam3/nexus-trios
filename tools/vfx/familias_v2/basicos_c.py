"""Ataques básicos com animação própria, lote c.

Gon (Jajanken pedra), Killua (garras de relâmpago), Edward (punho de pedra que
sobe do círculo de alquimia), Roy (estalo de dedos que vira linha de fogo),
Guts (a Matadora de Dragões descendo), Jotaro (o punho fantasma do Stand),
Giorno (soco que faz brotar galhos e a joaninha), Power (martelo de sangue),
Makima (o "bang" invisível), Frieren (Zoltraak), Anya (golpes de pânico),
Loid (mira e cutelada precisa) e Yor (os estiletes cruzados e as rosas).
"""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, apaga, back, contorno, ease_in, ease_out, estrela, faiscas, forma, girado,  # noqa: F401
                   jagged, janela, lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


# ================================================================== ajudantes
def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.28, tam=0.75, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.4
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.6 * k + 0.01, ang=ang + math.pi / 2, thin=0.012)) * k * 1.5
    return g, h


def _elipse(cx, cy, rx, ry, rot=0.0, n=64, a0=0.0, a1=TAU):
    pts = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        x, y = math.cos(a) * rx, math.sin(a) * ry
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    return pts


def _chama(cx, base, alt, larg, fase, ondula=0.25):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    lado_d, lado_e = [], []
    for k in range(13):
        u = k / 12
        y = base - alt * u
        w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
        b = ondula * larg * math.sin(fase + 6 * u) * u
        lado_d.append((cx + w + b, y))
        lado_e.append((cx - w + b, y))
    return lado_d + lado_e[::-1]


def _gota(cx, cy, r, ang):
    """Gota (lágrima): redonda de um lado, ponta apontando para `ang`."""
    pts = []
    for k in range(20):
        a = k / 20 * TAU
        rr = r * (1 + 1.4 * max(0.0, math.cos(a)) ** 6)
        pts.append((math.cos(a) * rr, math.sin(a) * r * (1 - 0.15 * max(0.0, math.cos(a)))))
    return _gira(pts, ang, cx, cy)


# o punho de lado, nós dos dedos para +x (unidade: ~0.32 de largura): quatro dedos dobrados
# em "bolinhas" na frente, o pulso atrás e o polegar por cima
def _contorno_punho():
    pts = [(-0.15, -0.12), (-0.02, -0.14), (0.09, -0.135)]
    for i in range(4):
        yc = -0.1 + i * 0.067
        for k in range(9):
            a = -math.pi / 2 + math.pi * k / 8
            pts.append((0.11 + math.cos(a) * 0.05, yc + math.sin(a) * 0.034))
    pts += [(0.07, 0.14), (-0.06, 0.135), (-0.15, 0.11), (-0.18, 0.06), (-0.18, -0.07)]
    return pts


_PUNHO = _contorno_punho()
_PULSO = [(-0.16, -0.08), (-0.44, -0.065), (-0.44, 0.065), (-0.16, 0.085)]


def _punho(T, cx, cy, esc=1.0, ang=0.0, braco=True, blur=0.004):
    """Silhueta do punho fechado (com o pulso) e os riscos entre os dedos e do polegar."""
    formas = [(_move(_gira(_PUNHO, ang), cx, cy, esc), 1.0)]
    if braco:
        formas.append((_move(_gira(_PULSO, ang), cx, cy, esc), 0.85))
    corpo = np.minimum(T.polys(formas, blur), 1.0)
    vincos = []
    for i in range(3):
        y = -0.1 + 0.0335 + i * 0.067
        vincos.append(_move(_gira([(0.035, y), (0.14, y)], ang), cx, cy, esc))
    vincos.append(_move(_gira([(-0.1, 0.02), (-0.02, 0.05), (0.06, 0.06)], ang), cx, cy, esc))   # polegar
    vincos.append(_move(_gira([(-0.15, -0.075), (-0.15, 0.075)], ang), cx, cy, esc))              # dobra do pulso
    linhas = sum(T.polyline(p, 0.014 * esc) for p in vincos)
    return corpo, np.minimum(linhas, 1.0)


def _sub(seed):
    return np.random.default_rng(seed)


# ================================================================== Gon
def jajanken(T, t, rng):
    """Jajanken (pedra): o punho de Gon puxa para trás e junta a aura (chamas e fagulhas que
    entram), fica branco de tanto brilho, avança e explode no alvo com estilhaços de pedra."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    junta = janela(t, 0.0, 0.3)
    avanca = ease_in(rel(t, 0.32, 0.42), 2.0)
    px = -0.42 - 0.08 * ease_out(rel(t, 0.0, 0.3)) + 0.36 * avanca + 0.012 * math.sin(t * 90) * junta
    py = 0.02
    vivo = 1 - rel(t, 0.42, 0.5)
    P, V = _punho(T, px, py, 1.75)
    # aura subindo em volta do punho
    chamas = []
    for k in range(8):
        x = px - 0.3 + 0.55 * k / 7
        alt = (0.42 + 0.14 * math.sin(t * 40 + k * 1.9)) * (1 - 0.45 * abs(k - 3.5) / 3.5) * junta
        chamas.append((_chama(x, py + 0.24, alt + 0.01, 0.1, t * 50 + k, 0.5), 0.55))
    A = T.polys(chamas, 0.02) * vivo
    halo = T.gauss(px + 0.05, py, 0.26, 0.22) * (0.3 + 0.9 * junta) * vivo
    # fagulhas que entram no punho
    sub = _sub(11)
    entra = []
    for _ in range(16):
        a = sub.uniform(0, TAU)
        f = (rel(t, 0.0, 0.32) * 1.6 + sub.uniform(0, 1)) % 1.0
        d = 0.5 * (1 - f) + 0.08
        entra.append((px + math.cos(a) * d, py + math.sin(a) * d * 0.8, f * (1 - rel(t, 0.3, 0.36))))
    E = T.splats(entra, 0.012)
    traco = T.polys([(lamina(-0.9, py, px + 0.1, py, 0.09, 1.0, 0.0), 1.0)], 0.02) * pulso(t, 0.32, 0.5)
    # o estouro
    k = pulso(t, 0.4, 0.82)
    g, h = _clarao(T, k, 0.0, 0.0, 0.33, 0.95)
    est = T.polys([(estrela(0, 0, 0.42 * back(rel(t, 0.4, 0.55)) + 0.01, 0.15, 9, 0.42), 1.0)], 0.008) * pulso(t, 0.4, 0.8)
    anel = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.41, 0.85), 2.2), 0.05) * pulso(t, 0.41, 0.9) * 1.2
    sub = _sub(23)
    cacos = []
    for _ in range(12):
        a = sub.uniform(0, TAU)
        d = 0.15 + 0.65 * ease_out(rel(t, 0.42, 0.9), 2) * sub.uniform(0.6, 1)
        r = sub.uniform(0.03, 0.055)
        pedra = [(math.cos(b) * r * sub.uniform(0.7, 1.2), math.sin(b) * r * sub.uniform(0.7, 1.2)) for b in np.linspace(0, TAU, 6, endpoint=False)]
        cacos.append((_gira(pedra, t * 9 + a, math.cos(a) * d, math.sin(a) * d + 0.3 * rel(t, 0.45, 1) ** 2), 1.0))
    C = T.polys(cacos, 0.004) * pulso(t, 0.42, 1.0) if t > 0.42 else T.zero()
    brilho_punho = 0.25 + 1.1 * junta
    G += (P * 1.1 * vivo + A * 1.1 + halo + E * 1.5 + traco * 0.8 + g + est * 1.1 + anel + C * 1.1) * env
    H += ((P * brilho_punho - V * 0.9 * (1 - junta * 0.5)) * vivo + A * 0.3 + halo * junta * 0.6 + E + traco * 0.6 + h + est + anel * 0.5 + C * 0.4) * env
    return G, H


# ================================================================== Killua
def garras_de_killua(T, t, rng):
    """Garras de Killua: três riscos de garra feitos de relâmpago, um logo depois do outro,
    em diagonal; cada um estala com galhos elétricos e fica crepitando antes de sumir."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    fase = int(t * 11 + 0.5)
    sub_f = _sub(500 + fase)       # o raio muda a cada quadro (crepita)
    ang = 0.75
    c, s = math.cos(ang), math.sin(ang)
    nx, ny = -s, c
    for k in range(3):
        a0 = 0.04 + 0.07 * k
        prog = ease_out(rel(t, a0, a0 + 0.12), 2)
        if prog <= 0:
            continue
        off = (k - 1) * 0.24
        L = 0.72 - 0.08 * abs(k - 1)
        x1, y1 = -c * L + nx * off, -s * L + ny * off
        x2, y2 = c * L + nx * off, s * L + ny * off
        fio = T.polys([(lamina(x1, y1, x2, y2, 0.055, prog, rel(t, a0 + 0.14, a0 + 0.55) * 0.9), 1.0)], 0.006)
        vivo = 1 - rel(t, a0 + 0.3, 0.95)
        ex, ey = x1 + (x2 - x1) * prog, y1 + (y2 - y1) * prog
        pts = jagged(sub_f, x1, y1, ex, ey, 6, 0.1)
        raio = T.polyline(pts, 0.016) * vivo
        galhos = T.zero()
        for _ in range(3):
            u = sub_f.uniform(0.15, 0.9) * prog
            bx, by = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
            lado = sub_f.choice([-1, 1])
            comp = sub_f.uniform(0.12, 0.25)
            dx, dy = c * 0.5 + nx * lado, s * 0.5 + ny * lado
            galhos += T.polyline(jagged(sub_f, bx, by, bx + dx * comp, by + dy * comp, 4, 0.3), 0.008)
        galhos *= vivo * (0.6 + 0.4 * sub_f.uniform())
        cabeca = T.gauss(ex, ey, 0.05, 0.05) * pulso(t, a0, a0 + 0.16) * 2
        G += (fio * 1.3 + T.blur(raio, 0.025) * 1.6 + raio * 0.8 + galhos * 1.2 + cabeca) * env
        H += (fio * 0.9 + raio * 1.2 + galhos * 0.7 + cabeca * 1.3) * env
    G += faiscas(T, _sub(77), t, 14, 0.6, 0.03, cone=(-2.6, -0.3), gravidade=0.15, inicio=0.12) * 1.3 * env
    H += faiscas(T, _sub(77), t, 14, 0.6, 0.03, cone=(-2.6, -0.3), gravidade=0.15, inicio=0.12) * 0.8 * env
    return G, H


# ================================================================== Edward
def punho_transmutado(T, t, rng):
    """Punho de aço transmutado: o círculo de alquimia se desenha no chão sob o alvo, com
    faíscas azuis estalando; dele sobe um pilar de pedra com um punho na ponta que acerta
    o alvo de baixo para cima, e depois desmorona em pedaços."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cy, R, sq = 0.52, 0.66, 3.2
    desenha = ease_out(rel(t, 0.0, 0.25), 1.6)
    luz_c = janela(t, 0.0, 0.05) * (1 - rel(t, 0.55, 0.95))
    dentro_ang = np.mod(np.arctan2((T.V - cy) * sq, T.U) + math.pi / 2, TAU) / TAU
    mascara = smooth(desenha * 1.02 - dentro_ang, -0.01, 0.01)
    aros = (T.ring(R, 0.022, 0, cy, sq) + T.ring(R * 0.86, 0.014, 0, cy, sq) + T.ring(R * 0.4, 0.014, 0, cy, sq)) * mascara
    tri = [(math.cos(a) * R * 0.86, cy + math.sin(a) * R * 0.86 / sq) for a in (-math.pi / 2, math.pi / 6, 5 * math.pi / 6, -math.pi / 2)]
    tri2 = [(math.cos(a) * R * 0.86, cy + math.sin(a) * R * 0.86 / sq) for a in (math.pi / 2, -math.pi / 6, -5 * math.pi / 6, math.pi / 2)]
    figura = (T.polyline(tri, 0.012) + T.polyline(tri2, 0.012)) * janela(t, 0.12, 0.26)
    runas = []
    for k in range(16):
        a = k / 16 * TAU
        if (k / 16) > desenha:
            continue
        r1, r2 = R * 0.88, R * 0.98
        runas.append((math.cos(a) * r1, cy + math.sin(a) * r1 / sq, math.cos(a) * r2, cy + math.sin(a) * r2 / sq, 1.0))
    circ = (aros + figura + (T.lines(runas, 0.012) if runas else T.zero())) * luz_c
    # faíscas azuis subindo do aro (estalos)
    sub_f = _sub(900 + int(t * 11 + 0.5))
    estalos = T.zero()
    for _ in range(5):
        a = sub_f.uniform(0, TAU)
        bx, by = math.cos(a) * R, cy + math.sin(a) * R / sq
        estalos += T.polyline(jagged(sub_f, bx, by, bx + sub_f.uniform(-0.1, 0.1), by - sub_f.uniform(0.15, 0.35), 4, 0.35), 0.01)
    estalos *= pulso(t, 0.02, 0.6)
    # o pilar com o punho de pedra subindo
    sobe = ease_out(rel(t, 0.26, 0.42), 2.2)
    desaba = rel(t, 0.62, 0.9)
    topo = cy - 0.02 - 0.82 * sobe
    pedra = T.zero()
    vinco = T.zero()
    if sobe > 0:
        larg = 0.16
        coluna = [(-larg, cy + 0.02), (-larg * 0.9, topo + 0.22), (-larg * 0.75, topo + 0.12), (larg * 0.75, topo + 0.12),
                  (larg * 0.95, topo + 0.25), (larg * 1.05, cy + 0.02)]
        P, V = _punho(T, 0.0, topo + 0.02, 1.25, -math.pi / 2, braco=False)
        pedra = (np.minimum(T.polys([(coluna, 1.0)], 0.004), 1) + P) * (1 - desaba)
        sub = _sub(5)
        rach = [jagged(sub, sub.uniform(-0.1, 0.1), cy, sub.uniform(-0.12, 0.12), topo + 0.3, 3, 0.25) for _ in range(3)]
        vinco = (sum(T.polyline(r, 0.01) for r in rach) + V) * (1 - desaba)
    # pedaços caindo quando desmorona
    sub = _sub(17)
    cacos = []
    for _ in range(12):
        x0 = sub.uniform(-0.18, 0.18)
        y0 = sub.uniform(-0.3, 0.45)
        d = desaba
        r = sub.uniform(0.03, 0.06)
        pts = [(math.cos(b) * r * sub.uniform(0.7, 1.2), math.sin(b) * r * sub.uniform(0.7, 1.2)) for b in np.linspace(0, TAU, 5, endpoint=False)]
        cacos.append((_gira(pts, d * 4 + x0 * 9, x0 * (1 + 1.5 * d), y0 + 0.7 * d * d), 1.0))
    C = T.polys(cacos, 0.004) * (pulso(desaba, 0.0, 1.0) if desaba > 0 else 0)
    k = pulso(t, 0.36, 0.66)
    g, h = _clarao(T, k, 0.0, -0.32, 0.25, 0.75)
    poe_ = poeira(T, _sub(8), t, 18, 0, cy, 0.6, 0.15, 0.035, 0.3) * janela(t, 0.3, 0.35)
    G += (circ * 1.3 + T.blur(circ, 0.03) * 0.8 + estalos * 1.2 + pedra * 0.85 + C * 0.9 + g + poe_ * 0.5) * env
    H += (circ * 1.0 + estalos * 1.0 + np.maximum(pedra * 0.35 - vinco * 0.5, 0) + T.blur(pedra, 0.01) * 0.1 + C * 0.3 + h) * env
    return G, H


# ================================================================== Roy
def estalo_de_dedos(T, t, rng):
    """Estalo de dedos: a faísca pequena do estalo à esquerda, uma linha de fogo fina que corre
    rente até o alvo e a explosão de chamas que sobe em bola."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sx, sy = -0.78, -0.05
    k0 = pulso(t, 0.0, 0.16)
    fa = T.flare(sx, sy, 0.3 * k0 + 0.01, ang=0.4, thin=0.02) * k0 * 2 + T.gauss(sx, sy, 0.04, 0.04) * k0 * 2
    # a linha de fogo correndo
    corre = ease_in(rel(t, 0.08, 0.3), 1.3)
    pts = []
    n = int(30 * corre) + 2
    for i in range(n):
        u = i / 29
        x = sx + (0.0 - sx) * u
        pts.append((x, sy + (0.0 - sy) * u + 0.025 * math.sin(u * 22 - t * 60)))
    linha = T.polyline(pts, 0.03) * (1 - rel(t, 0.3, 0.55)) if corre > 0 else T.zero()
    ponta = T.gauss(pts[-1][0], pts[-1][1], 0.05, 0.04) * pulso(t, 0.08, 0.34) * 2
    lingua = []
    for i in range(0, n, 3):
        x, y = pts[i]
        alt = 0.13 + 0.06 * math.sin(i * 1.7 + t * 50)
        lingua.append((_chama(x, y + 0.02, alt * (1 - rel(t, 0.3, 0.55)), 0.045, t * 40 + i), 0.6))
    Lc = T.polys(lingua, 0.01) if lingua and corre > 0 else T.zero()
    # a explosão de chamas: línguas de fogo saindo para todo lado (mais altas para cima)
    ex = rel(t, 0.3, 1.0)
    k = pulso(t, 0.3, 0.6)
    g, h = _clarao(T, k, 0, 0, 0.3, 0.8)
    bola = T.gauss(0, -0.04 - 0.12 * ex, 0.16 + 0.12 * ease_out(ex, 2), 0.15 + 0.12 * ease_out(ex, 2)) * janela(t, 0.3, 0.36) * (1 - ex ** 1.3) * 1.6
    chamas = []
    if t > 0.3:
        sub = _sub(33)
        cresce = back(rel(t, 0.3, 0.46), 1.4)
        for i in range(13):
            ang = -math.pi / 2 + (i / 13) * TAU + sub.uniform(-0.15, 0.15)
            pra_cima = 0.6 + 0.4 * max(0.0, -math.sin(ang))
            alt = (0.32 + 0.22 * sub.uniform()) * pra_cima * cresce * (1 - ex ** 1.6) + 0.01
            lingua = _chama(0, 0.0, alt, 0.1 + 0.03 * sub.uniform(), t * 45 + i * 1.3, 0.5)
            lingua = _gira(lingua, ang + math.pi / 2, 0, -0.12 * ex)
            chamas.append((_move(lingua, math.cos(ang) * 0.04 * cresce, math.sin(ang) * 0.04 * cresce), 0.7))
    Ch = T.polys(chamas, 0.015) if chamas else T.zero()
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.3, 0.6), 2), 0.03) * pulso(t, 0.3, 0.6) * 0.7
    sub = _sub(44)
    br = []
    for _ in range(18):
        a = sub.uniform(-math.pi, 0)
        d = 0.3 + 0.5 * ease_out(ex, 2) * sub.uniform(0.4, 1)
        br.append((math.cos(a) * d, math.sin(a) * d - 0.25 * ex, pulso(t, 0.36, 1.0) * sub.uniform(0.3, 1)))
    Bz = T.splats(br, 0.01)
    G += (fa + T.blur(linha, 0.02) * 1.5 + linha * 0.8 + Lc * 0.9 + ponta + g + bola + Ch * 1.2 + anel + Bz * 1.5) * env
    H += (fa * 1.3 + linha * 1.1 + ponta * 1.2 + h + bola * 0.5 * (1 - ex) + T.blur(Ch, 0.01) * 0.45 + anel * 0.4 + Bz) * env
    return G, H


# ================================================================== Guts
def matadora_de_dragoes(T, t, rng):
    """Golpe da Matadora de Dragões: a lâmina enorme de ferro bruto (larga, sem brilho, cheia de
    lascas) cai do alto num arco pesado, crava no alvo, o chão racha e voam faíscas e respingos."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    px, py = -0.95, -0.4
    a_ini, a_fim = -1.5, 0.35
    gira = 0.08 * ease_out(rel(t, 0.0, 0.08)) + 0.92 * ease_in(rel(t, 0.06, 0.3), 2.2)
    a = a_ini + (a_fim - a_ini) * gira
    a -= pulso(t, 0.3, 0.42) * 0.06              # o tranco do impacto
    c, s = math.cos(a), math.sin(a)
    nx, ny = -s, c
    r0, r1, w = 0.25, 1.5, 0.15
    lam = [(px + c * r0 + nx * w, py + s * r0 + ny * w), (px + c * (r1 - 0.22) + nx * w, py + s * (r1 - 0.22) + ny * w),
           (px + c * r1 - nx * w * 0.35, py + s * r1 - ny * w * 0.35), (px + c * (r1 - 0.06) - nx * w, py + s * (r1 - 0.06) - ny * w),
           (px + c * r0 - nx * w, py + s * r0 - ny * w)]
    some_l = 1 - rel(t, 0.6, 0.85)
    gx, gy = px + c * (r0 - 0.03), py + s * (r0 - 0.03)
    guarda = [(gx + nx * 0.24 + c * 0.035, gy + ny * 0.24 + s * 0.035), (gx + nx * 0.24 - c * 0.035, gy + ny * 0.24 - s * 0.035),
              (gx - nx * 0.24 - c * 0.035, gy - ny * 0.24 - s * 0.035), (gx - nx * 0.24 + c * 0.035, gy - ny * 0.24 + s * 0.035)]
    cabo = [(px + nx * 0.04, py + ny * 0.04), (gx + nx * 0.045, gy + ny * 0.045), (gx - nx * 0.045, gy - ny * 0.045), (px - nx * 0.04, py - ny * 0.04)]
    L = np.minimum(T.polys([(lam, 1.0), (guarda, 1.0), (cabo, 0.8)], 0.004), 1) * some_l
    # lascas e o vinco do meio (ferro bruto)
    meio = T.polyline([(px + c * (r0 + 0.05), py + s * (r0 + 0.05)), (px + c * (r1 - 0.15), py + s * (r1 - 0.15))], 0.012) * some_l
    sub = _sub(3)
    lascas = []
    for _ in range(6):
        u = sub.uniform(r0 + 0.2, r1 - 0.1)
        lado = sub.choice([-1, 1])
        bx, by = px + c * u + nx * w * lado, py + s * u + ny * w * lado
        lascas.append(([(bx + c * 0.04, by + s * 0.04), (bx - c * 0.04, by - s * 0.04), (bx - nx * lado * 0.035, by - ny * lado * 0.035)], 1.0))
    Ls = T.polys(lascas, 0.002) * some_l
    # o arco do movimento atrás da lâmina
    arco = T.arc_band(1.0, 0.32, a_ini + 0.15, a - 0.08, cx=px, cy=py, taper=1.2) * janela(t, 0.1, 0.18) * (1 - rel(t, 0.3, 0.55))
    # impacto: clarão, rachaduras, faíscas para cima, respingos
    k = pulso(t, 0.28, 0.6)
    g, h = _clarao(T, k, 0.05, 0.12, 0.3, 0.9, 0.0)
    sub = _sub(61)
    rach = T.zero()
    cresce = ease_out(rel(t, 0.3, 0.45), 2)
    for j in range(5):
        ang = math.pi * (0.1 + 0.8 * j / 4) + sub.uniform(-0.15, 0.15)
        comp = 0.55 * cresce * sub.uniform(0.6, 1)
        rach += T.polyline(jagged(sub, 0.05, 0.18, 0.05 + math.cos(ang) * comp * 1.5, 0.18 + math.sin(ang) * comp * 0.45, 4, 0.25), 0.016)
    rach *= janela(t, 0.3, 0.33) * (1 - rel(t, 0.7, 1.0))
    F = faiscas(T, _sub(71), t, 22, 0.9, 0.035, cone=(-math.pi + 0.2, -0.2), gravidade=0.5, cx=0.05, cy=0.12, inicio=0.3)
    resp = []
    sub = _sub(81)
    for _ in range(9):
        aa = sub.uniform(-math.pi + 0.3, -0.3)
        d = 0.1 + 0.5 * ease_out(rel(t, 0.3, 0.8), 2) * sub.uniform(0.5, 1)
        resp.append((_gota(0.05 + math.cos(aa) * d, 0.12 + math.sin(aa) * d + 0.5 * rel(t, 0.3, 1) ** 2, 0.022, aa + math.pi), 1.0))
    R = T.polys(resp, 0.004) * pulso(t, 0.3, 1.0) if t > 0.3 else T.zero()
    po = poeira(T, _sub(9), t, 20, 0.05, 0.2, 0.7, 0.2, 0.04, 0.3) * janela(t, 0.3, 0.34)
    G += (L * 0.95 + Ls * 0.4 + arco * 1.1 + g + rach * 1.3 + F * 1.6 + R * 1.1 + po * 0.55) * env
    H += (np.maximum(L * 0.28 - meio * 0.25 - Ls * 0.2, 0) + T.blur(L, 0.006) * 0.08 + arco * 0.35 + h + rach * 0.9 + F * 1.1 + R * 0.35) * env
    return G, H


# ================================================================== Jotaro
def soco_do_stand(T, t, rng):
    """Soco do Stand: o punho fantasma, grande e translúcido (só o contorno forte), atravessa da
    esquerda deixando vultos, acerta com estrela e dois anéis de eco, e um segundo punho
    fantasma ecoa o golpe logo depois."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)

    def pos(u):
        return -1.05 + 0.98 * ease_out(u, 2.5)
    fim_soco = 1 - rel(t, 0.38, 0.62)
    for j, (dt, alfa) in enumerate(((0.0, 1.0), (0.05, 0.45), (0.1, 0.25), (0.15, 0.14))):
        if t - dt < 0:
            continue
        uu = rel(t - dt, 0.0, 0.3)
        x = pos(uu)
        P, V = _punho(T, x, 0.0, 1.9, 0.0, blur=0.006)
        cont = contorno(T.blur(P, 0.01), 0.3, 0.45, 0.6, 0.85)
        vis = alfa * (fim_soco if j == 0 else (1 - rel(t, 0.3, 0.45)))
        G += (P * 0.4 + cont * 1.3 + V * 0.4) * vis * env
        H += (cont * 0.8 + V * 0.4 + P * 0.08) * vis * env
    # o eco: segundo punho fantasma, deslocado, que pisca e soca de novo
    k_e = pulso(t, 0.4, 0.7)
    if k_e > 0:
        xe = -0.3 + 0.2 * ease_out(rel(t, 0.4, 0.55), 2)
        P, V = _punho(T, xe, -0.12, 1.6, -0.12, blur=0.008)
        cont = contorno(T.blur(P, 0.01), 0.3, 0.45, 0.6, 0.85)
        G += (P * 0.25 + cont * 0.9) * k_e * env
        H += cont * 0.5 * k_e * env
    k = pulso(t, 0.26, 0.6)
    g, h = _clarao(T, k, 0.08, 0, 0.26, 0.8)
    est = T.polys([(estrela(0.08, 0, 0.36 * back(rel(t, 0.26, 0.4)) + 0.01, 0.0, 8, 0.4), 1.0)], 0.008) * pulso(t, 0.26, 0.55)
    anel1 = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.27, 0.6), 2), 0.035, 0.08, 0) * pulso(t, 0.27, 0.65)
    anel2 = T.ring(0.1 + 0.75 * ease_out(rel(t, 0.45, 0.85), 2), 0.03, 0.08, 0) * pulso(t, 0.45, 0.9) * 0.8
    vel = rastro_de_velocidade(T, rng, 9, 0.0, 0.7, 0.45, -0.05, 0.0, 0.0, 0.014, 21) * pulso(t, 0.1, 0.45)
    G += (g + est * 1.2 + anel1 * 1.1 + anel2 + vel * 0.8) * env
    H += (h + est + anel1 * 0.5 + anel2 * 0.35 + vel * 0.4) * env
    return G, H


# ================================================================== Giorno
def _joaninha(T, cx, cy, r):
    """A joaninha da Gold Experience: corpo oval, cabeça, antenas; o risco do meio e as pintas
    voltam como "furos" (desenhados escuros por cima)."""
    corpo = forma(T.gauss(cx, cy, r * 0.8, r), 0.45, 0.55)
    hx, hy = cx, cy - r * 1.05
    cabeca = forma(T.gauss(hx, hy, r * 0.45, r * 0.38), 0.45, 0.55)
    risco = T.polyline([(cx, cy - r * 0.9), (cx, cy + r * 1.1)], r * 0.12)
    pintas = T.zero()
    for dx, dy in ((-0.45, -0.3), (0.45, -0.3), (-0.5, 0.35), (0.5, 0.35), (-0.25, 0.75), (0.25, 0.75)):
        pintas += forma(T.gauss(cx + dx * r, cy + dy * r, r * 0.13, r * 0.13), 0.45, 0.6)
    antenas = T.polyline([(hx - r * 0.12, hy - r * 0.25), (hx - r * 0.35, hy - r * 0.6)], r * 0.06) + \
        T.polyline([(hx + r * 0.12, hy - r * 0.25), (hx + r * 0.35, hy - r * 0.6)], r * 0.06)
    return np.minimum(corpo + cabeca + antenas, 1.0), np.minimum(risco + pintas, 1.0)


def soco_da_vida(T, t, rng):
    """Soco da vida (Gold Experience): o soco acerta com um estalo dourado, e do ponto do golpe
    brotam galhos que se enrolam, folhas que se abrem e uma joaninha dourada que pousa."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.3)
    g, h = _clarao(T, k, 0, 0, 0.24, 0.65)
    est = T.polys([(estrela(0, 0, 0.3 * back(rel(t, 0.0, 0.15)) + 0.01, 0.2, 7, 0.4), 1.0)], 0.008) * pulso(t, 0.0, 0.26)
    anel = T.ring(0.1 + 0.4 * ease_out(rel(t, 0.02, 0.3), 2), 0.03) * pulso(t, 0.02, 0.35)
    cresce = ease_out(rel(t, 0.14, 0.6), 1.8)
    galhos, folhas = T.zero(), []
    sub = _sub(7)
    for j in range(6):
        a = j / 6 * TAU + 0.3 + sub.uniform(-0.2, 0.2)
        curva = sub.choice([-1, 1]) * sub.uniform(1.2, 2.0)
        comp = sub.uniform(0.55, 0.72)
        pts = []
        n = int(24 * cresce) + 2
        for i in range(n):
            u = i / 23
            aa = a + curva * u * u
            d = 0.14 + comp * u
            pts.append((math.cos(aa) * d, math.sin(aa) * d * 0.9))
        if cresce > 0.02:
            galhos += T.polyline(pts, 0.028 * (1 - 0.5 * cresce) + 0.008)
            for i in range(6, n, 7):
                fx, fy = pts[i]
                bx, by = pts[i - 1]
                dir_ = math.atan2(fy - by, fx - bx) + (0.9 if (i // 7) % 2 else -0.9)
                abre = back(rel(t, 0.14 + 0.45 * i / 23, 0.28 + 0.45 * i / 23))
                comp_f = 0.13 * abre
                if comp_f > 0.005:
                    folhas.append((lamina(fx, fy, fx + math.cos(dir_) * comp_f, fy + math.sin(dir_) * comp_f, 0.045 * abre, 1.0), 1.0))
            if cresce > 0.85:
                ex, ey = pts[-1]
                galhos += T.ring(0.035, 0.01, ex, ey) * janela(cresce, 0.85, 1.0)
    F = T.polys(folhas, 0.004) if folhas else T.zero()
    pousa = back(rel(t, 0.36, 0.52), 2.2)
    J, furos = T.zero(), T.zero()
    if pousa > 0:
        J, furos = _joaninha(T, 0.0, -0.02 - 0.08 * (1 - pousa), 0.16 * pousa + 0.001)
    halo_j = T.gauss(0, -0.02, 0.24, 0.24) * janela(t, 0.36, 0.45) * (0.6 + 0.2 * math.sin(t * 30))
    sub = _sub(19)
    br = [(sub.uniform(-0.7, 0.7), sub.uniform(-0.7, 0.7), max(0.0, math.sin(t * 14 + i * 1.3)) * janela(t, 0.3, 0.45)) for i in range(16)]
    Br = T.splats(br, 0.01)
    corpo_j = J * (1 - furos * 0.95)
    G += (g + est * 1.1 + anel + galhos * 1.2 + F * 1.1 + corpo_j * 1.3 + halo_j * 0.6 + Br * 1.4) * env
    H += (h + est * 0.9 + anel * 0.4 + galhos * 0.45 + F * 0.35 + corpo_j * 0.85 + Br * 1.1) * env
    return G, H


# ================================================================== Power
def pancada_de_sangue(T, t, rng):
    """Pancada de sangue: o martelo feito de sangue (cabeça grossa com espinhos, gotejando)
    desce num arco, esmaga o alvo e espirra gotas para todo lado, com a poça em coroa."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    px, py = -0.8, 0.5
    a_ini, a_fim = -2.3, -0.576
    gira = ease_in(rel(t, 0.0, 0.28), 2.0)
    a = a_ini + (a_fim - a_ini) * gira
    some_m = 1 - rel(t, 0.5, 0.72)
    c, s = math.cos(a), math.sin(a)
    nx, ny = -s, c
    R = 0.95
    cabo = T.polyline([(px, py), (px + c * R, py + s * R)], 0.065)
    hx, hy = px + c * R, py + s * R
    larg, prof = 0.3, 0.19
    cab = [(hx + nx * larg - c * prof, hy + ny * larg - s * prof), (hx + nx * larg + c * prof, hy + ny * larg + s * prof),
           (hx - nx * larg + c * prof, hy - ny * larg + s * prof), (hx - nx * larg - c * prof, hy - ny * larg - s * prof)]
    esp = []
    for lado in (-1, 1):
        for d in (-0.12, 0.0, 0.12):
            bx, by = hx + nx * larg * lado + c * d, hy + ny * larg * lado + s * d
            esp.append(([(bx + c * 0.045, by + s * 0.045), (bx - c * 0.045, by - s * 0.045), (bx + nx * lado * 0.09, by + ny * lado * 0.09)], 1.0))
    # o sangue escorrendo da frente da cabeça (gotas penduradas)
    for d, comp in ((-0.14, 0.09), (-0.02, 0.14), (0.1, 0.07)):
        bx, by = hx + c * prof + nx * d, hy + s * prof + ny * d
        esp.append((_gota(bx + c * comp * 0.5, by + s * comp * 0.5, 0.03, a + math.pi), 1.0))
    M = np.minimum(T.polys([(cab, 1.0)] + esp, 0.006) + cabo, 1.0) * some_m
    rastro = T.arc_band(R, 0.3, a_ini + 0.4, a, cx=px, cy=py, taper=1.5) * janela(t, 0.05, 0.12) * (1 - rel(t, 0.28, 0.45))
    # gotas pingando do martelo durante o arco
    sub = _sub(13)
    pingos = []
    for i in range(7):
        aa = a_ini + (a_fim - a_ini) * (i + 0.5) / 7
        solta = (i + 0.5) / 7 * 0.28
        if t < solta:
            continue
        u = t - solta
        gx = px + math.cos(aa) * R + sub.uniform(-0.05, 0.05)
        gy = py + math.sin(aa) * R + 2.2 * u * u
        pingos.append((_gota(gx, gy, 0.022, -math.pi / 2), max(0.0, 1 - u * 2.5)))
    Pg = T.polys(pingos, 0.004) if pingos else T.zero()
    # o impacto
    k = pulso(t, 0.27, 0.55)
    g, h = _clarao(T, k, 0.0, 0.0, 0.28, 0.6, 0.0)
    poca = T.ring(0.08 + 0.55 * ease_out(rel(t, 0.28, 0.6), 2), 0.05, 0, 0.12, 2.6) * pulso(t, 0.28, 0.95) * 1.1
    sub = _sub(29)
    gotas = []
    for _ in range(16):
        aa = sub.uniform(-math.pi + 0.15, -0.15)
        vel = sub.uniform(0.5, 1.0)
        u = rel(t, 0.28, 0.95)
        d = 0.15 + 0.7 * vel * ease_out(u, 1.6)
        gx, gy = math.cos(aa) * d, math.sin(aa) * d * 0.9 + 0.9 * u * u
        vy = math.sin(aa) * vel + 1.8 * u
        dir_ = math.atan2(vy, math.cos(aa) * vel)
        gotas.append((_gota(gx, gy, 0.03 * sub.uniform(0.7, 1.2), dir_ + math.pi), 1.0))
    Go = T.polys(gotas, 0.004) * pulso(t, 0.28, 1.0) if t > 0.28 else T.zero()
    coroa = []
    if t > 0.28:
        for j in range(9):
            aa = math.pi + j / 8 * math.pi
            alt = 0.2 * back(rel(t, 0.28, 0.42)) * (1 - rel(t, 0.55, 0.85))
            coroa.append((_chama(math.cos(aa) * 0.3, 0.14, alt + 0.01, 0.05, j * 2.0, 0.2), 1.0))
    Co = T.polys(coroa, 0.006) if coroa else T.zero()
    G += (M * 1.15 + rastro * 0.9 + Pg * 1.1 + g + poca + Go * 1.2 + Co * 1.1) * env
    H += (M * 0.45 + rastro * 0.3 + Pg * 0.4 + h + poca * 0.3 + Go * 0.55 + Co * 0.4) * env
    return G, H


# ================================================================== Makima
def dedo_apontado(T, t, rng):
    """Dedo apontado: nada voa. Anéis concêntricos (os olhos dela) se fecham sobre o alvo,
    a pressão invisível amassa o ar e, de repente, um estouro seco em forma de "BANG" com
    anel de choque e um esguicho de gotas para o lado de lá."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    fecha = ease_in(rel(t, 0.0, 0.26), 1.6)
    aneis = T.zero()
    for j in range(3):
        r = (0.75 - 0.18 * j) * (1 - fecha) + 0.06 * (j + 1)
        aneis += T.ring(r, 0.012 + 0.004 * j)
    aneis *= janela(t, 0.0, 0.08) * (1 - rel(t, 0.24, 0.3))
    segs = []
    for j in range(10):
        a = j / 10 * TAU + 0.15
        d = 0.5 - 0.3 * fecha
        segs.append((math.cos(a) * (d + 0.18), math.sin(a) * (d + 0.18), math.cos(a) * d, math.sin(a) * d, 1.0))
    press = T.tapered(segs, 0.025) * pulso(t, 0.05, 0.3)
    nucleo = T.gauss(0, 0, 0.04, 0.04) * janela(t, 0.15, 0.27) * (1 - rel(t, 0.27, 0.3)) * 2
    k = pulso(t, 0.27, 0.7)
    pop = back(rel(t, 0.27, 0.38), 2.5)
    sub = _sub(66)
    pts = []
    for j in range(22):
        a = j / 22 * TAU
        rr = (0.42 if j % 2 == 0 else 0.22) * sub.uniform(0.75, 1.15)
        pts.append((math.cos(a) * rr * pop * 1.15, math.sin(a) * rr * pop * 0.9))
    if pop > 0:
        bang = np.minimum(T.polys([(pts, 1.0)], 0.006), 1) * (1 - rel(t, 0.45, 0.7))
        miolo = np.minimum(T.polys([([(x * 0.62, y * 0.62) for x, y in pts], 1.0)], 0.01), 1) * (1 - rel(t, 0.4, 0.6))
    else:
        bang, miolo = T.zero(), T.zero()
    choque = T.ring(0.2 + 0.7 * ease_out(rel(t, 0.28, 0.75), 2.2), 0.035) * pulso(t, 0.28, 0.8) * 1.2
    sub = _sub(67)
    gotas = []
    for _ in range(13):
        aa = sub.uniform(-0.75, 0.75)
        vel = sub.uniform(0.5, 1.0)
        u = rel(t, 0.28, 1.0)
        d = 0.25 + 0.65 * vel * ease_out(u, 1.8)
        gotas.append((_gota(math.cos(aa) * d, math.sin(aa) * d + 0.35 * u * u, 0.024 * sub.uniform(0.7, 1.2), aa + math.pi), 1.0))
    Go = T.polys(gotas, 0.004) * pulso(t, 0.28, 1.0) if t > 0.28 else T.zero()
    g, h = _clarao(T, k, 0, 0, 0.22, 0.5, 0.0)
    G += (aneis * 1.2 + press * 0.9 + nucleo + bang * 1.15 + choque + Go * 1.15 + g * 0.6) * env
    H += (aneis * 0.5 + press * 0.4 + nucleo * 1.5 + miolo * 1.1 + bang * 0.2 + choque * 0.5 + Go * 0.4 + h * 0.6) * env
    return G, H


# ================================================================== Frieren
def feitico_comum(T, t, rng):
    """Feitiço de ataque comum (Zoltraak): um círculo mágico pequeno se acende à esquerda,
    visto de lado (girando, com runas), e dispara um raio branco reto que atravessa até o
    alvo e estoura em luz."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cx, cy = -0.66, 0.0
    abre = back(rel(t, 0.0, 0.2), 1.6)
    vivo = 1 - rel(t, 0.5, 0.8)
    rx, ry = 0.1 * abre + 0.001, 0.32 * abre + 0.001
    circ = T.polyline(_elipse(cx, cy, rx, ry), 0.014) + T.polyline(_elipse(cx, cy, rx * 0.78, ry * 0.78), 0.009) * 0.8
    gira = t * 7
    star = [(cx + math.cos(gira + j * 2 * TAU / 5) * rx * 0.75, cy + math.sin(gira + j * 2 * TAU / 5) * ry * 0.75) for j in range(6)]
    est = T.polyline(star, 0.008)
    runas = []
    for j in range(12):
        a = gira * 0.6 + j / 12 * TAU
        r1, r2 = 1.05, 1.22
        runas.append((cx + math.cos(a) * rx * r1, cy + math.sin(a) * ry * r1, cx + math.cos(a) * rx * r2, cy + math.sin(a) * ry * r2, 1.0 if j % 3 else 0.5))
    Ru = T.lines(runas, 0.012)
    C = (circ + est * 0.8 + Ru * 0.8) * vivo * janela(t, 0.0, 0.04)
    centro = T.gauss(cx, cy, 0.05, 0.12) * janela(t, 0.12, 0.24) * vivo * 1.5
    sai = ease_out(rel(t, 0.22, 0.34), 2)
    if sai > 0:
        x_fim = cx + (0.0 - cx) * sai
        k_b = 1 - rel(t, 0.45, 0.72)
        largura = 0.05 * (1 + 0.15 * math.sin(t * 60))
        dist_y = np.abs(T.V - cy)
        dentro = smooth(T.U, cx - 0.02, cx + 0.03) * (1 - smooth(T.U, x_fim, x_fim + 0.04))
        beam = np.exp(-(dist_y / largura) ** 2) * dentro * k_b
        nucleo_b = np.exp(-(dist_y / (largura * 0.35)) ** 2) * dentro * k_b
        G += (beam * 1.3 + T.blur(beam, 0.04) * 0.8) * env
        H += (nucleo_b * 1.6 + beam * 0.3) * env
    k = pulso(t, 0.32, 0.7)
    g, h = _clarao(T, k, 0, 0, 0.26, 0.9, 0.0)
    anel = T.ring(0.08 + 0.5 * ease_out(rel(t, 0.33, 0.7), 2), 0.03, squash=0.8) * pulso(t, 0.33, 0.75)
    F = faiscas(T, _sub(8), t, 16, 0.6, 0.025, cone=(-1.1, 1.1), gravidade=0.0, inicio=0.33)
    G += (C * 1.3 + T.blur(C, 0.025) * 0.8 + centro + g + anel + F * 1.4) * env
    H += (C * 1.0 + centro * 1.2 + h + anel * 0.5 + F) * env
    return G, H


# ================================================================== Anya
def golpe_de_panico(T, t, rng):
    """Golpe de pânico: tapinhas desajeitados para todo lado (arquinhos de movimento e
    estrelinhas de impacto), um "!" de desenho que pula, gotas de suor voando e, no fim,
    estrelinhas tontas girando em volta do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    # quatro tapinhas rápidos, cada um num canto: o arquinho do braço e a estrela do tapa
    tapas = ((-0.22, -0.05, 0.0, 0.5), (0.2, 0.15, 0.1, -0.6), (-0.12, 0.25, 0.2, 0.2), (0.15, -0.12, 0.3, -2.6))
    for x, y, t0, ang in tapas:
        k = pulso(t, t0, t0 + 0.2)
        if k <= 0:
            continue
        r = 0.32
        cx, cy = x - math.cos(ang) * r, y - math.sin(ang) * r
        arc = T.arc_band(r, 0.07, ang - 1.5, ang, cx=cx, cy=cy, crescente=True) * pulso(t, t0 - 0.04, t0 + 0.14)
        pop = back(rel(t, t0 + 0.03, t0 + 0.1), 2.2)
        est = T.polys([(estrela(x, y, 0.2 * pop + 0.01, ang, 6, 0.42), 1.0)], 0.006) * k
        G += (arc * 1.3 + est * 1.3) * env
        H += (arc * 0.6 + est * 1.0) * env
    # o "!" que pula em cima, tremendo
    pula = back(rel(t, 0.06, 0.2), 2.4)
    sacode = math.sin(t * 50) * 0.06 * (1 - rel(t, 0.2, 0.5))
    ex, ey = 0.42, -0.5
    if pula > 0:
        esc = 1.5 * pula
        barra = _move(_gira([(-0.05, -0.2), (0.05, -0.2), (0.03, 0.06), (-0.03, 0.06)], sacode), ex, ey, esc)
        ponto = T.gauss(ex + sacode * 0.15, ey + 0.135 * esc, 0.032 * esc + 1e-3, 0.032 * esc + 1e-3)
        Ex = (np.minimum(T.polys([(barra, 1.0)], 0.005), 1) + forma(ponto, 0.4, 0.55)) * (1 - rel(t, 0.7, 0.9))
        G += (Ex * 1.4 + T.blur(Ex, 0.03) * 0.6) * env
        H += Ex * 1.0 * env
    # gotas de suor que voam da cabeça
    sub = _sub(5)
    gotas = []
    for j in range(6):
        t0 = 0.04 + 0.07 * j
        u = rel(t, t0, t0 + 0.4)
        aa = -math.pi / 2 + sub.uniform(-1.2, 1.2)
        if u <= 0 or u >= 1:
            continue
        d = 0.2 + 0.4 * ease_out(u, 2)
        gotas.append((_gota(-0.12 + math.cos(aa) * d, -0.3 + math.sin(aa) * d + 0.45 * u * u, 0.05, aa + math.pi), 1 - u ** 2))
    if gotas:
        Gs = T.polys(gotas, 0.004)
        G += Gs * 1.3 * env
        H += Gs * 0.8 * env
    # estrelinhas tontas girando
    tonto = janela(t, 0.42, 0.52)
    if tonto > 0:
        est = []
        for j in range(4):
            a = t * 12 + j / 4 * TAU
            est.append((estrela(math.cos(a) * 0.42, -0.32 + math.sin(a) * 0.12, 0.1, a, 5, 0.45), 1.0))
        Es = T.polys(est, 0.004) * tonto
        G += (Es * 1.4 + T.ring(0.42, 0.012, 0, -0.32, 3.5) * 0.5 * tonto) * env
        H += Es * 1.0 * env
    return G, H


# ================================================================== Loid
def golpe_do_espiao(T, t, rng):
    """Golpe do espião: a retícula de mira aparece larga e se fecha no alvo (colchetes girando
    até travar), pisca ao travar, e um golpe de mão seco e curto corta em diagonal com um
    brilho fino de precisão."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    trava = ease_out(rel(t, 0.0, 0.28), 2.4)
    r = 0.7 - 0.36 * trava
    vis_r = janela(t, 0.0, 0.06) * (1 - rel(t, 0.45, 0.7))
    pisca = 1 + 0.9 * pulso(t, 0.28, 0.36)
    anel = T.ring(r, 0.012)
    cruz = []
    for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        c, s = math.cos(a), math.sin(a)
        cruz.append((c * r * 0.45, s * r * 0.45, c * r * 1.2, s * r * 1.2, 1.0))
    Cz = T.lines(cruz, 0.012)
    gira = (1 - trava) * 0.8 + math.pi / 4
    colch = []
    for j in range(4):
        a = gira + j * math.pi / 2
        ca = (math.cos(a) * r * 1.35, math.sin(a) * r * 1.35)
        p1 = (ca[0] + math.cos(a + 2.3) * 0.12, ca[1] + math.sin(a + 2.3) * 0.12)
        p2 = (ca[0] + math.cos(a - 2.3) * 0.12, ca[1] + math.sin(a - 2.3) * 0.12)
        colch.append(T.polyline([p1, ca, p2], 0.016))
    Co = sum(colch)
    ponto = T.gauss(0, 0, 0.025, 0.025) * janela(t, 0.2, 0.28)
    Ret = (anel + Cz * 0.9 + Co * 1.1 + ponto * 2) * vis_r * pisca
    corta = ease_out(rel(t, 0.34, 0.42), 2)
    L = T.polys([(lamina(-0.45, -0.38, 0.45, 0.38, 0.06, corta, rel(t, 0.42, 0.62)), 1.0)], 0.004) if corta > 0 else T.zero()
    vel = rastro_de_velocidade(T, rng, 6, math.atan2(0.38, 0.45), 0.5, 0.15, 0.1, 0.0, 0.0, 0.01, 4) * pulso(t, 0.3, 0.45)
    k = pulso(t, 0.38, 0.7)
    brilho = T.flare(0, 0, 0.75 * k + 0.01, ang=-0.7, thin=0.012) * k * 2 + T.flare(0, 0, 0.35 * k + 0.01, ang=0.87, thin=0.012) * k * 1.4
    nucleo = T.gauss(0, 0, 0.12, 0.12) * k
    G += (Ret * 1.2 + T.blur(Ret, 0.02) * 0.5 + L * 1.3 + vel * 0.6 + brilho * 0.8 + nucleo) * env
    H += (Ret * 0.7 + L * 1.1 + vel * 0.3 + brilho * 1.1 + nucleo * 0.6) * env
    return G, H


# ================================================================== Yor
def _estilete(T, x, y, ang, esc=1.0):
    """O estilete da Princesa Espinho: lâmina fina e comprida, guarda em cruz e pomo no cabo."""
    c, s = math.cos(ang), math.sin(ang)
    gx, gy = x - c * 0.42 * esc, y - s * 0.42 * esc
    lam = lamina(gx, gy, x, y, 0.028 * esc, 1.0)
    nx, ny = -s, c
    guarda = T.polyline([(gx + nx * 0.07 * esc, gy + ny * 0.07 * esc), (gx - nx * 0.07 * esc, gy - ny * 0.07 * esc)], 0.022 * esc)
    cabo = T.polyline([(gx, gy), (gx - c * 0.12 * esc, gy - s * 0.12 * esc)], 0.026 * esc)
    pomo = T.gauss(gx - c * 0.13 * esc, gy - s * 0.13 * esc, 0.022 * esc, 0.022 * esc)
    return np.minimum(T.polys([(lam, 1.0)], 0.003) + guarda + cabo + forma(pomo, 0.4, 0.55), 1.0)


def _petala(cx, cy, r, rot, vira=1.0):
    """Pétala de rosa: larga e redonda, com o entalhe no topo e a base afinando."""
    pts = []
    for k in range(24):
        a = k / 24 * TAU
        rr = r * (1 - 0.3 * math.exp(-((a - 3 * math.pi / 2) / 0.35) ** 2))
        x, y = math.cos(a) * rr * vira, math.sin(a) * rr
        if y > 0:
            x *= 1 - 0.55 * (y / r)
            y *= 1.25
        pts.append((x, y))
    return _gira(pts, rot, cx, cy)


def agulha_de_espinho(T, t, rng):
    """Agulha de espinho: dois estiletes vêm da esquerda, um de cima e um de baixo, cruzam
    em X e cravam no alvo (dois estalos de brilho, um logo depois do outro); pétalas de rosa
    caem girando enquanto as lâminas somem."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vivo = 1 - rel(t, 0.6, 0.85)
    for t0, y0, alvo_y in ((0.0, -0.75, 0.142), (0.08, 0.75, -0.142)):
        u = ease_in(rel(t, t0, t0 + 0.18), 1.6)
        if u <= 0:
            continue
        sx, sy = -0.95, y0
        ex, ey = 0.18, alvo_y
        x, y = sx + (ex - sx) * u, sy + (ey - sy) * u
        ang = math.atan2(ey - sy, ex - sx)
        E = _estilete(T, x, y, ang, 1.2) * vivo
        u0 = max(0.0, u - 0.4)
        rastro = T.polys([(lamina(sx + (ex - sx) * u0, sy + (ey - sy) * u0, x, y, 0.02, 1.0), 1.0)], 0.01) * (1 - rel(t, t0 + 0.18, t0 + 0.3))
        k = pulso(t, t0 + 0.17, t0 + 0.4)
        bri = T.flare(0, 0, 0.55 * k + 0.01, ang=ang + 0.8, thin=0.014) * k * 1.8
        G += (E * 1.3 + rastro * 0.8 + bri * 0.7 + T.gauss(0, 0, 0.1, 0.1) * k) * env
        H += (E * 0.9 + rastro * 0.5 + bri * 1.2) * env
    sub = _sub(52)
    petalas = []
    for j in range(9):
        x0 = sub.uniform(-0.7, 0.7)
        t0 = 0.22 + sub.uniform(0, 0.25)
        dy = sub.uniform(-0.1, 0.1)
        sentido = sub.choice([-1, 1])
        u = rel(t, t0, 1.0)
        if u <= 0:
            continue
        y = -0.75 + 1.3 * u + dy
        x = x0 + 0.12 * math.sin(u * 7 + j)
        rot = u * 5 * sentido + j
        vira = 0.45 + 0.55 * abs(math.cos(u * 6 + j))   # a pétala vira no ar
        petalas.append((_petala(x, y, 0.075, rot, vira), janela(u, 0, 0.1) * (1 - u ** 3)))
    Pe = T.polys(petalas, 0.006) if petalas else T.zero()
    G += Pe * 1.3 * env
    H += Pe * 0.35 * env
    return G, H


REGISTRO = [
    ("garras_de_killua", garras_de_killua, GRANDE, "Garras de Killua: três riscos de garra feitos de relâmpago", False),
    ("punho_transmutado", punho_transmutado, GRANDE, "Punho transmutado de Edward: círculo de alquimia e punho de pedra que sobe", False),
    ("estalo_de_dedos", estalo_de_dedos, GRANDE, "Estalo de dedos de Roy: faísca, linha de fogo e explosão de chamas", False),
    ("matadora_de_dragoes", matadora_de_dragoes, GRANDE, "Matadora de Dragões de Guts: a lâmina gigante desce, faíscas e respingos", False),
    ("soco_do_stand", soco_do_stand, GRANDE, "Soco do Stand de Jotaro: punho fantasma com vultos e eco", False),
    ("soco_da_vida", soco_da_vida, GRANDE, "Soco da vida de Giorno: galhos, folhas e a joaninha dourada", False),
    ("pancada_de_sangue", pancada_de_sangue, GRANDE, "Pancada de sangue de Power: martelo de sangue e gotas espirrando", False),
    ("dedo_apontado", dedo_apontado, GRANDE, "Dedo apontado de Makima: pressão invisível e estouro em 'bang'", False),
    ("feitico_comum", feitico_comum, GRANDE, "Feitiço de ataque comum de Frieren: círculo mágico e raio Zoltraak", False),
    ("golpe_de_panico", golpe_de_panico, GRANDE, "Golpe de pânico de Anya: tapinhas, suor, '!' e estrelinhas", False),
    ("golpe_do_espiao", golpe_do_espiao, GRANDE, "Golpe do espião de Loid: retícula de mira e cutelada precisa", False),
    ("agulha_de_espinho", agulha_de_espinho, GRANDE, "Agulha de espinho de Yor: dois estiletes em X e pétalas de rosa", False),
]
