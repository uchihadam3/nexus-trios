"""Ataques básicos com animação própria, lote e.

Batman, Superman, Homem-Aranha, Doutor Estranho, Mulher-Maravilha, Homem de
Ferro, Capitão América, Ravena, Thanos, Feiticeira Escarlate, Homem-Formiga,
Capitã Marvel e Motoqueiro Fantasma: cada folha conta o golpe normal do
personagem com a forma que o identifica (o morcego do batarangue, o escudo
com a estrela, a mandala de runas, o corvo da alma, a corrente em chamas…),
grande o bastante para se ler pequena na tela do celular.
"""
from __future__ import annotations

import math

import numpy as np

from .assinaturas import _chama, _clarao, _gira, _move
from .base import (GRANDE, MEDIA, TAU, apaga, back, contorno, ease_in, ease_out, estrela, faiscas, forma, girado,  # noqa: F401
                   jagged, janela, lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


# ------------------------------------------------------------------ peças comuns
def _elipse(cx, cy, rx, ry, ang=0.0, n=28):
    c, s = math.cos(ang), math.sin(ang)
    pts = []
    for k in range(n):
        a = k / n * TAU
        x, y = math.cos(a) * rx, math.sin(a) * ry
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return pts


def _contorno_segs(pts, w=1.0):
    """Polígono fechado → segmentos (para desenhar muitos contornos numa só imagem)."""
    return [(x1, y1, x2, y2, w) for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])]


_PUNHO = [(-0.10, -0.12), (0.04, -0.14), (0.10, -0.13), (0.14, -0.10), (0.155, -0.06), (0.14, -0.035), (0.16, -0.01),
          (0.145, 0.02), (0.16, 0.045), (0.14, 0.075), (0.10, 0.10), (0.03, 0.11), (-0.02, 0.09), (-0.10, 0.10)]
_DEDOS = [((0.07, -0.062), (0.148, -0.058)), ((0.07, -0.012), (0.155, -0.012)), ((0.07, 0.036), (0.152, 0.042)),
          ((-0.03, 0.05), (0.09, 0.07))]


def _punho(T, cx, cy, esc=1.0, ang=0.0, braco=0.25, vinco=0.012):
    """Punho fechado virado para +x (os nós dos dedos na frente), com antebraço e os vincos dos dedos.

    Devolve (cheio, vincos): o cheio já vem com os vincos cavados, para o punho se ler pequeno."""
    corpo = _move(_gira(_PUNHO, ang), cx, cy, esc)
    pts_braco = [(-0.08, -0.085), (-0.08 - braco, -0.075), (-0.08 - braco, 0.075), (-0.08, 0.085)]
    formas = [(corpo, 1.0)]
    if braco > 0:
        formas.append((_move(_gira(pts_braco, ang), cx, cy, esc), 0.85))
    cheio = T.polys(formas, 0.004)
    segs = []
    for (x1, y1), (x2, y2) in _DEDOS:
        (a, b), (c, d) = _move(_gira([(x1, y1), (x2, y2)], ang), cx, cy, esc)
        segs.append((a, b, c, d, 1.0))
    vincos = T.lines(segs, vinco * esc, 0.003)
    return np.maximum(cheio - vincos * 0.8, 0), vincos


def _estouro(T, t, a, b, cx=0.0, cy=0.0, r=0.3, n=8, interno=0.38, ang=0.25):
    """Estrela de impacto que estoura e encolhe entre a e b."""
    k = pulso(t, a, b)
    return T.polys([(estrela(cx, cy, r * k + 0.01, ang, n, interno), 1.0)], 0.006) * k, k


# ------------------------------------------------------------------ Batman
_MORCEGO = [(-0.50, -0.06), (-0.30, -0.10), (-0.14, -0.10), (-0.09, -0.21), (-0.05, -0.10), (0.05, -0.10), (0.09, -0.21),
            (0.14, -0.10), (0.30, -0.10), (0.50, -0.06), (0.40, 0.00), (0.33, 0.06), (0.28, 0.01), (0.20, 0.08), (0.13, 0.03),
            (0.06, 0.10), (0.00, 0.19), (-0.06, 0.10), (-0.13, 0.03), (-0.20, 0.08), (-0.28, 0.01), (-0.33, 0.06), (-0.40, 0.00)]


def batarangue(T, t, rng):
    """Batarangue rápido: o batarangue em forma de morcego entra girando pela esquerda com um
    rastro em arco, crava no alvo (para de girar e treme), estala em rachaduras e some."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    voa = ease_in(rel(t, 0.0, 0.3), 1.2)

    def caminho(u):
        return -1.0 + 1.0 * u, -0.35 * math.sin(math.pi * u) * (1 - u) * 1.6

    px, py = caminho(voa)
    cravou = t >= 0.3
    esc = 1.2
    if not cravou:
        giro = t * 38
    else:
        giro = -0.35 + 0.08 * math.sin(t * 90) * (1 - rel(t, 0.3, 0.5))
        px, py = 0.04, 0.0
    M = T.polys([(_move(_gira(_MORCEGO, giro), px, py, esc), 1.0)], 0.004)
    vultos = []
    if not cravou:
        for j in range(1, 3):
            u = voa - 0.08 * j
            if u > 0:
                vx, vy = caminho(u)
                vultos.append((_move(_gira(_MORCEGO, giro - 0.5 * j), vx, vy, esc), 0.3 - 0.1 * j))
    V = T.polys(vultos, 0.012) if vultos else T.zero()
    trilha = T.polyline([caminho(voa * k / 24) for k in range(25)], 0.02) * janela(t, 0.03, 0.08) * (1 - rel(t, 0.28, 0.5))
    # o "tchak": estrela curta, rachaduras saindo do ponto onde cravou
    est, k = _estouro(T, t, 0.29, 0.5, 0.0, 0.0, 0.32, 6, 0.32, 0.6)
    # traços de impacto em volta (o "tchak"), por fora do morcego
    rach = T.zero()
    if 0.3 < t < 0.6:
        u = ease_out(rel(t, 0.3, 0.45), 2)
        segs = []
        for j in range(8):
            a = j / 8 * TAU + 0.2
            r0 = 0.36 + 0.12 * u
            segs.append((math.cos(a) * (r0 + 0.16), math.sin(a) * (r0 + 0.16) * 0.8, math.cos(a) * r0, math.sin(a) * r0 * 0.8, 1.0))
        rach = T.tapered(segs, 0.035) * pulso(t, 0.3, 0.6)
    g, h = _clarao(T, k, 0.0, 0.0, 0.2, 0.6)
    fa = faiscas(T, np.random.default_rng(7), t, 10, 0.55, 0.03, (-math.pi, 0.2), 0.3, inicio=0.3)
    some_m = 1 - rel(t, 0.62, 0.9)
    G += (M * 1.3 * some_m + V + T.blur(trilha, 0.015) * 1.1 + est * 0.9 + rach * 1.2 + g * 0.8 + fa * 1.2) * env
    H += (M * 0.45 * some_m + V * 0.15 + trilha * 0.4 + est * 0.8 + rach * 0.8 + h + fa) * env
    return G, H


# ------------------------------------------------------------------ Superman
def soco_de_aco(T, t, rng):
    """Soco de aço: o punho chega rompendo a barreira do som (cone de vapor em volta do braço e
    linhas de velocidade), acerta com um clarão e solta anéis de onda de choque em sequência."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vem = ease_in(rel(t, 0.0, 0.24), 1.6)
    fx = -0.95 + 0.82 * vem - 0.25 * ease_out(rel(t, 0.3, 0.55), 2)
    vis = 1 - rel(t, 0.42, 0.6)
    P, vinco = _punho(T, fx, 0.0, 1.35, 0.0, 0.6)
    linhas = rastro_de_velocidade(T, rng, 12, 0.0, 0.7, 0.32, 0.12, cx=fx - 0.05, largura=0.016, seed=11) * janela(t, 0.02, 0.08) * (1 - rel(t, 0.25, 0.45))
    # cone de vapor: crescentes à frente do punho e um anel em volta do braço
    cone = 0
    for j in range(3):
        cone = cone + T.arc_band(0.24 + 0.09 * j, 0.022, -1.05, 1.05, 1.0, 0.0, fx - 0.08 - 0.07 * j, 0.0, crescente=True) * (0.9 - 0.25 * j)
    cone = cone * pulso(t, 0.06, 0.32)
    anel_braco = T.ring(0.05, 0.016, cx=fx - 0.22, squash=0.28) * pulso(t, 0.1, 0.3) * 1.3
    est, k = _estouro(T, t, 0.22, 0.46, 0.06, 0.0, 0.36, 8, 0.33, 0.2)
    g, h = _clarao(T, k, 0.06, 0.0, 0.3, 0.95)
    ondas = 0
    for j, a0 in enumerate((0.24, 0.32, 0.41)):
        u = rel(t, a0, a0 + 0.42)
        ondas = ondas + T.ring(0.08 + 0.8 * ease_out(u, 2.2), 0.04 - 0.008 * j) * pulso(t, a0, a0 + 0.45) * (1.3 - 0.25 * j)
    # anéis achatados correndo para a frente (o estrondo que atravessa o alvo)
    frente = 0
    for j, a0 in enumerate((0.24, 0.3)):
        u = ease_out(rel(t, a0, a0 + 0.4), 1.8)
        frente = frente + T.ring(0.06 + 0.06 * u, 0.02, cx=0.1 + 0.65 * u, squash=0.18 + 0.1 * u) * pulso(t, a0, a0 + 0.4)
    G += ((P * 1.2 + anel_braco) * vis + linhas * 0.9 + cone * 1.2 + est + g + ondas + frente * 1.2) * env
    H += ((P * 0.35 + vinco * 0.2 + anel_braco * 0.8) * vis + linhas * 0.5 + cone * 0.6 + est * 0.8 + h + ondas * 0.45 + frente * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Homem-Aranha
def _teia_radial(cx, cy, r, prog, n=8, voltas=3, giro=0.2):
    """Teia de aranha: raios saindo do centro e voltas de fio ligando os raios (com a curvinha)."""
    segs = []
    for j in range(n):
        a = giro + j / n * TAU
        rr = r * (0.85 + 0.15 * ((j * 7) % 3) / 2)
        segs.append((cx, cy, cx + math.cos(a) * rr * prog, cy + math.sin(a) * rr * prog, 1.0))
    for v in range(1, voltas + 1):
        rv = r * v / (voltas + 0.4) * prog
        for j in range(n):
            a0, a1 = giro + j / n * TAU, giro + (j + 1) / n * TAU
            am = (a0 + a1) / 2
            p0 = (cx + math.cos(a0) * rv, cy + math.sin(a0) * rv)
            pm = (cx + math.cos(am) * rv * 0.86, cy + math.sin(am) * rv * 0.86)
            p1 = (cx + math.cos(a1) * rv, cy + math.sin(a1) * rv)
            segs += [(p0[0], p0[1], pm[0], pm[1], 0.8), (pm[0], pm[1], p1[0], p1[1], 0.8)]
    return segs


def teia_e_soco(T, t, rng):
    """Teia e soco: o fio de teia dispara da esquerda e gruda no alvo abrindo a teia em estrela;
    o fio estica (o puxão) e o soco chega no meio da teia com estrela de impacto."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vai = ease_out(rel(t, 0.0, 0.16), 1.6)
    ox, oy = -1.0, -0.32
    hx, hy = ox + (0.0 - ox) * vai, oy + (0.0 - oy) * vai
    estica = rel(t, 0.3, 0.42)
    pts = []
    for k in range(17):
        u = k / 16
        sag = 0.08 * math.sin(math.pi * u) * (1 - estica)
        pts.append((ox + (hx - ox) * u, oy + (hy - oy) * u + sag))
    fio = T.polyline(pts, 0.014) * janela(t, 0.0, 0.03) * (1 - rel(t, 0.4, 0.5))
    bolota = T.gauss(hx, hy, 0.04, 0.04) * (1 - rel(t, 0.15, 0.2)) * 1.5
    abre = back(rel(t, 0.15, 0.3), 1.6)
    W = T.lines(_teia_radial(0.0, 0.0, 0.48, max(abre, 0.01)), 0.012, 0.002) * janela(t, 0.15, 0.17) * (1 - rel(t, 0.62, 0.88))
    splat = T.gauss(0, 0, 0.09, 0.09) * pulso(t, 0.14, 0.32) * 1.5
    # o soco
    vem = ease_in(rel(t, 0.38, 0.48), 1.5)
    pv = janela(t, 0.38, 0.4) * (1 - rel(t, 0.52, 0.62))
    P, vinco = _punho(T, -0.95 + 0.82 * vem, 0.02, 1.25, 0.0, 0.5)
    linhas = rastro_de_velocidade(T, rng, 8, 0.0, 0.5, 0.25, 0.1, cx=-0.95 + 0.82 * vem - 0.1, largura=0.014, seed=5) * pulso(t, 0.38, 0.52)
    est, k = _estouro(T, t, 0.46, 0.7, 0.06, 0.0, 0.34, 7, 0.36, 0.1)
    g, h = _clarao(T, k, 0.06, 0.0, 0.26, 0.85)
    anel = T.ring(0.1 + 0.62 * ease_out(rel(t, 0.47, 0.85), 2), 0.04) * pulso(t, 0.47, 0.9)
    G += (fio * 1.4 + bolota + W * 1.4 + splat + P * 1.2 * pv + linhas + est + g + anel) * env
    H += (fio * 1.1 + bolota + W * 1.0 + splat * 0.6 + P * 0.35 * pv + linhas * 0.5 + est * 0.8 + h + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Doutor Estranho
def _mandala(T, cx, cy, r, giro):
    """Mandala de runas: dois aros com marcas de runa entre eles, dois quadrados girando ao contrário
    (a estrela de oito pontas) e um aro pequeno no meio."""
    segs = []
    for j in range(24):
        a = giro + j / 24 * TAU
        r0, r1 = r * 0.8, r * (0.95 if j % 2 else 0.88)
        segs.append((cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r1, cy + math.sin(a) * r1, 0.9))
    for gq in (giro * -1.6, giro * -1.6 + math.pi / 4):
        quad = [(cx + math.cos(gq + m * math.pi / 2) * r * 0.74, cy + math.sin(gq + m * math.pi / 2) * r * 0.74) for m in range(4)]
        segs += _contorno_segs(quad, 1.0)
    linhas = T.lines(segs, 0.012, 0.002)
    aros = T.ring(r, 0.016, cx, cy) + T.ring(r * 0.8, 0.012, cx, cy) * 0.8 + T.ring(r * 0.3, 0.014, cx, cy) * 0.9
    return linhas + aros


def disparo_arcano(T, t, rng):
    """Disparo arcano: a mandala de runas acende girando à esquerda, cospe faíscas arcanas em
    curva que acertam o alvo uma atrás da outra, e uma mandala pequena marca o ponto."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    mx, my = -0.52, 0.0
    acende = back(rel(t, 0.0, 0.2), 1.5)
    giro = t * 7
    Mn = _mandala(T, mx, my, 0.4 * acende + 0.01, giro) * janela(t, 0.0, 0.05) * (1 - rel(t, 0.45, 0.7))
    miolo = T.gauss(mx, my, 0.1, 0.1) * pulso(t, 0.1, 0.5) * 1.2
    tiros = T.zero()
    cabecas, acertos = [], []
    for j in range(4):
        a0 = 0.2 + 0.05 * j
        u = rel(t, a0, a0 + 0.16)
        curva = (j - 1.5) * 0.28

        def cam(w, curva=curva):
            return mx + (0.0 - mx) * w, my + curva * math.sin(math.pi * w)
        if 0 < u < 1:
            u0 = max(0.0, u - 0.3)
            pts = [cam(u0 + (u - u0) * m / 8) for m in range(9)]
            segs = [(x1, y1, x2, y2, 0.4 + 0.6 * m / 8) for m, ((x1, y1), (x2, y2)) in enumerate(zip(pts, pts[1:]))]
            tiros += T.tapered(segs, 0.075)
            cabecas.append((*cam(u), 1.0))
        kk = pulso(t, a0 + 0.15, a0 + 0.32)
        if kk > 0:
            acertos.append((j, kk))
    C = T.splats(cabecas, 0.042) if cabecas else T.zero()
    hit = T.zero()
    hit_h = T.zero()
    for j, kk in acertos:
        hit += T.flare(0.0, 0.0, 0.5 * kk + 0.01, ang=0.4 + j * 0.7, thin=0.014) * kk
        hit_h += T.gauss(0, 0, 0.08, 0.08) * kk
    marca = _mandala(T, 0.0, 0.0, 0.34 * ease_out(rel(t, 0.38, 0.55), 2) + 0.01, -giro) * pulso(t, 0.38, 0.95)
    crep = T.zero()
    if 0.4 < t < 0.85:
        sub = np.random.default_rng(int(t * 40) * 7)
        for j in range(5):
            a = sub.uniform(0, TAU)
            crep += T.polyline(jagged(sub, 0.0, 0.0, 0.42 * math.cos(a), 0.42 * math.sin(a), 3, 0.35), 0.01)
        crep *= pulso(t, 0.4, 0.85)
    G += (Mn * 1.5 + miolo + tiros * 1.4 + C * 1.6 + hit * 1.4 + hit_h + marca * 1.2 + crep) * env
    H += (Mn * 0.7 + miolo * 0.5 + tiros * 0.7 + C * 1.5 + hit * 1.2 + hit_h * 1.2 + marca * 0.5 + crep * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Mulher-Maravilha
def _bracelete(cx, cy, ang, comp=0.2, larg=0.075):
    """O bracelete visto de lado: faixa de metal com as pontas arredondadas."""
    pts = []
    for k in range(9):
        a = -math.pi / 2 + math.pi * k / 8
        pts.append((comp / 2 + math.cos(a) * larg * 0.5, math.sin(a) * larg))
    for k in range(9):
        a = math.pi / 2 + math.pi * k / 8
        pts.append((-comp / 2 + math.cos(a) * larg * 0.5, math.sin(a) * larg))
    return _gira(pts, ang, cx, cy)


def bracelete(T, t, rng):
    """Golpe de bracelete: os dois braceletes se cruzam em X na frente do alvo e batem (o clarão e
    as faíscas do bloqueio); abrem, e o soco com o bracelete no pulso acerta o centro."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cruza = ease_out(rel(t, 0.0, 0.12), 2)
    abre = 0.0
    cx, cy = -0.1, -0.02
    vis = 1 - rel(t, 0.34, 0.44)
    formas, faixas = [], []
    for lado in (-1, 1):
        ang = lado * (math.pi / 4) * (0.5 + 0.5 * cruza) + math.pi / 2
        d = 0.55 * (1 - cruza) + 0.6 * abre
        bx, by = cx - 0.15 * d, cy + lado * d
        formas.append((_bracelete(bx, by, ang, 0.62, 0.095), 1.0))
        c, s = math.cos(ang), math.sin(ang)
        for off in (-0.04, 0.04):
            faixas.append((bx - c * 0.27 - s * off, by - s * 0.27 + c * off, bx + c * 0.27 - s * off, by + s * 0.27 + c * off, 1.0))
    B = T.polys(formas, 0.004) * vis
    faixa = T.lines(faixas, 0.014, 0.003) * vis
    kc = pulso(t, 0.1, 0.3)
    clang = T.flare(cx, cy, 0.9 * kc + 0.01, ang=0.0, thin=0.01) * kc * 1.5 + T.gauss(cx, cy, 0.06, 0.06) * kc * 1.4
    fa = faiscas(T, np.random.default_rng(84), t, 14, 0.75, 0.03, (-math.pi, math.pi), 0.35, cx=cx, cy=cy, inicio=0.11)
    # o soco com o bracelete no pulso
    vem = ease_in(rel(t, 0.42, 0.52), 1.5)
    px = -0.98 + 0.85 * vem
    pv = janela(t, 0.42, 0.44) * (1 - rel(t, 0.58, 0.68))
    P, vinco = _punho(T, px, 0.0, 1.25, 0.0, 0.5)
    cuff = T.polys([(_bracelete(px - 0.2, 0.0, math.pi / 2, 0.24, 0.05), 1.0)], 0.003)
    est, k = _estouro(T, t, 0.5, 0.74, 0.06, 0.0, 0.36, 8, 0.36, 0.2)
    g, h = _clarao(T, k, 0.06, 0.0, 0.26, 0.8)
    anel = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.51, 0.88), 2), 0.045) * pulso(t, 0.51, 0.92)
    G += (B * 1.2 + faixa * 0.5 + clang + fa * 1.3 + (P * 1.1 + cuff * 1.2) * pv + est + g + anel) * env
    H += (B * 0.5 + faixa * 1.2 + clang * 1.1 + fa + (P * 0.3 + cuff * 0.9) * pv + est * 0.8 + h + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Homem de Ferro

# ------------------------------------------------------------------ Capitão América
def _escudo(T, cx, cy, r, giro, sq=1.0):
    """O escudo redondo: aro externo, aro do meio, disco central e a estrela que gira."""
    disco = T.polys([(_elipse(cx, cy, r, r * sq, 0.0, 40), 0.55)], 0.004)
    aros = T.ring(r * 0.93, r * 0.07, cx, cy, 1 / sq) * 1.0 + T.ring(r * 0.66, r * 0.07, cx, cy, 1 / sq) * 0.9
    miolo = T.polys([(_elipse(cx, cy, r * 0.42, r * 0.42 * sq, 0.0, 32), 0.7)], 0.004)
    est = T.polys([([(x, cy + (y - cy) * sq) for x, y in estrela(cx, cy, r * 0.38, giro - math.pi / 2, 5, 0.4)], 1.0)], 0.003)
    return disco + aros + miolo, aros * 0.5 + est * 1.4


def escudo_do_capitao(T, t, rng):
    """Escudo arremessado: o escudo redondo com a estrela vem girando, bate no alvo com um clarão
    metálico e faíscas, e quica para o alto, de volta para quem jogou."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.3), 1.3)
    bate = t >= 0.3
    volta = ease_out(rel(t, 0.3, 0.8), 1.4)
    if not bate:
        sx, sy = -1.0 + 0.92 * vem, -0.15 + 0.15 * vem
        sq = 0.85
    else:
        sx, sy = -0.08 - 0.75 * volta, -0.95 * volta + 0.25 * volta * volta
        sq = 0.85 - 0.25 * volta
    giro = t * 26
    r = 0.3 * (1 - 0.3 * volta)
    corpo, estrela_h = _escudo(T, sx, sy, r, giro, sq)
    vis = 1 - rel(t, 0.7, 0.86)
    vultos = T.zero()
    if not bate:
        for j in range(1, 4):
            u = max(0.0, vem - 0.07 * j)
            vultos += T.gauss(-1.0 + 0.92 * u, -0.15 + 0.15 * u, 0.17, 0.15) * (0.45 - 0.12 * j)
    else:
        for j in range(1, 4):
            u = ease_out(max(0.0, rel(t, 0.3, 0.8) - 0.05 * j), 1.4)
            vultos += T.gauss(-0.08 - 0.75 * u, -0.95 * u + 0.25 * u * u, 0.14, 0.12) * (0.4 - 0.1 * j) * janela(t, 0.32, 0.38)
    est, k = _estouro(T, t, 0.28, 0.5, 0.08, 0.0, 0.36, 6, 0.3, 0.0)
    g, h = _clarao(T, k, 0.08, 0.0, 0.26, 1.0)
    fa = faiscas(T, np.random.default_rng(1941), t, 14, 0.7, 0.03, (-0.9, 1.4), 0.35, cx=0.12, cy=0.0, inicio=0.3)
    anel = T.ring(0.1 + 0.55 * ease_out(rel(t, 0.3, 0.7), 2), 0.035, 0.08) * pulso(t, 0.3, 0.75)
    G += (corpo * 1.3 * vis + vultos + est + g + fa * 1.3 + anel) * env
    H += ((corpo * 0.25 + estrela_h) * vis + vultos * 0.2 + est * 0.8 + h + fa + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Ravena
def _ave(cx, cy, esc, ang, bate):
    """Corvo grande de frente, de asas abertas (pontas das penas em dedos), cabeça com bico e cauda
    em leque; `bate` de 1 (asas no alto) a -0.5 (asas embaixo)."""
    asa = [(0.05, -0.08), (0.18, -0.2), (0.36, -0.27), (0.58, -0.26), (0.5, -0.18), (0.6, -0.14), (0.48, -0.1), (0.55, -0.04),
           (0.42, -0.04), (0.45, 0.03), (0.33, 0.0), (0.32, 0.07), (0.21, 0.03), (0.08, 0.06)]
    asa_b = [(x, -0.08 + (y + 0.08) * bate if x > 0.1 else y) for x, y in asa]
    corpo = _elipse(0.0, 0.0, 0.085, 0.17, 0.0, 20)
    cabeca = _elipse(0.0, -0.17, 0.065, 0.06, 0.0, 16)
    bico = [(-0.03, -0.14), (0.03, -0.14), (0.0, -0.06)]
    cauda = [(-0.06, 0.1), (0.06, 0.1), (0.14, 0.32), (0.07, 0.29), (0.0, 0.34), (-0.07, 0.29), (-0.14, 0.32)]
    formas = [asa_b, [(-x, y) for x, y in asa_b], corpo, cabeca, cauda]
    return [_move(_gira(f, ang), cx, cy, esc) for f in formas], _move(_gira(bico, ang), cx, cy, esc)


def corvo_da_alma(T, t, rng):
    """Energia da alma: o corvo de energia escura surge do alto à esquerda batendo as asas, mergulha
    sobre o alvo, fecha as asas em volta dele e se desfaz em fiapos de sombra."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    mergulho = ease_in(rel(t, 0.0, 0.36), 1.4)
    cx, cy = -0.55 + 0.55 * mergulho, -0.55 + 0.55 * mergulho
    ang = -0.45 * (1 - mergulho)
    bate = 0.62 + 0.38 * math.cos(t * 30) if t < 0.3 else 1.0
    esc = 1.15 + 0.45 * mergulho
    vis = 1 - rel(t, 0.4, 0.54)
    formas, bico = _ave(cx, cy, esc, ang, bate)
    A = np.minimum(T.polys([(f, 1.0) for f in formas]), 1.0)
    A = T.blur(A, 0.005) * janela(t, 0.0, 0.08) * vis
    # rastro de sombra atrás do corvo
    rastro = 0
    for j in range(1, 5):
        u = max(0.0, mergulho - 0.07 * j)
        rastro = rastro + T.gauss(-0.55 + 0.55 * u, -0.55 + 0.55 * u, 0.22, 0.14) * (0.4 - 0.08 * j)
    rastro = rastro * janela(t, 0.02, 0.1) * (1 - rel(t, 0.32, 0.5))
    hx, hy = _move(_gira([(0.0, -0.17)], ang), cx, cy, esc)[0]
    nx, ny = math.cos(ang) * 0.03 * esc, math.sin(ang) * 0.03 * esc
    olhos = (T.gauss(hx + nx, hy + ny, 0.016, 0.012) + T.gauss(hx - nx, hy - ny, 0.016, 0.012)) * vis * janela(t, 0.04, 0.1) * 2.2
    # a cabeça fica escura (o miolo do corvo é sombra), só os olhos acendem
    A = np.maximum(A - T.polys([(bico, 0.5)], 0.003), 0)
    # as asas se fecham em volta do alvo (duas faixas curvas que se encontram)
    fecha = ease_out(rel(t, 0.36, 0.56), 2)
    envolve = (T.arc_band(0.42, 0.07, -math.pi * 0.95, -math.pi * 0.95 + 1.6 * fecha + 0.01, 0.9, 0.0)
               + T.arc_band(0.42, 0.07, math.pi * 0.95, math.pi * 0.95 - 1.6 * fecha - 0.01, 0.9, 0.0)) * pulso(t, 0.36, 0.8)
    k = pulso(t, 0.5, 0.82)
    nucleo = T.gauss(0, 0, 0.2, 0.2) * k * 1.3
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.52, 0.92), 2), 0.05) * pulso(t, 0.52, 0.95)
    sub = np.random.default_rng(1980)
    fiapos = T.zero()
    for j in range(9):
        a = j / 9 * TAU + sub.uniform(-0.2, 0.2)
        u = ease_out(rel(t, 0.54, 0.95), 1.8)
        r0, r1 = 0.12 + 0.5 * u, 0.3 + 0.62 * u
        pts = [((r0 + (r1 - r0) * m / 6) * math.cos(a + 0.5 * m / 6), (r0 + (r1 - r0) * m / 6) * math.sin(a + 0.5 * m / 6)) for m in range(7)]
        fiapos += T.polyline(pts, 0.03)
    fiapos = T.blur(fiapos, 0.012) * pulso(t, 0.54, 1.0)
    G += (A * 1.4 + T.blur(A, 0.04) * 0.6 + rastro + olhos + envolve * 1.3 + nucleo + anel + fiapos * 1.6) * env
    H += (A * 0.12 + olhos * 1.6 + envolve * 0.35 + nucleo * 0.6 + anel * 0.35 + fiapos * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Thanos
def manopla(T, t, rng):
    """Punho do Titã: a manopla (o punho com as joias nos nós dos dedos) chega pesada, acerta com
    um clarão e as seis joias estouram em volta, cada uma num brilho de quatro pontas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.22), 1.8)
    fx = -0.98 + 0.84 * vem - 0.18 * ease_out(rel(t, 0.3, 0.55), 2)
    vis = 1 - rel(t, 0.4, 0.56)
    P, vinco = _punho(T, fx, 0.0, 1.55, 0.0, 0.55)
    joias_mao = [(fx + x * 1.55 - 0.02, y * 1.55, 1.0)
                 for x, y in ((0.15, -0.085), (0.155, -0.035), (0.155, 0.015), (0.15, 0.065), (0.04, 0.075), (-0.02, -0.02))]
    J = T.splats(joias_mao, 0.018)
    linhas = rastro_de_velocidade(T, rng, 10, 0.0, 0.6, 0.3, 0.1, cx=fx - 0.12, largura=0.018, seed=21) * pulso(t, 0.02, 0.32)
    est, k = _estouro(T, t, 0.2, 0.45, 0.08, 0.0, 0.4, 8, 0.32, 0.1)
    g, h = _clarao(T, k, 0.08, 0.0, 0.32, 1.0)
    anel = T.ring(0.12 + 0.55 * ease_out(rel(t, 0.22, 0.6), 2), 0.05, 0.08) * pulso(t, 0.22, 0.65) * 1.2
    gemas, gemas_h, caudas = [], T.zero(), []
    for j in range(6):
        a = -math.pi / 2 + j * TAU / 6
        a0 = 0.26 + 0.03 * j
        u = ease_out(rel(t, a0, a0 + 0.3), 2.2)
        if u <= 0:
            continue
        d = 0.15 + 0.48 * u
        gx, gy = 0.08 + d * math.cos(a), d * math.sin(a)
        vida = janela(t, a0, a0 + 0.02) * (1 - rel(t, 0.75, 0.95))
        gemas.append((_gira([(0.0, -0.1), (0.065, 0.0), (0.0, 0.1), (-0.065, 0.0)], a + math.pi / 2, gx, gy), vida))
        kk = pulso(t, a0 + 0.2, a0 + 0.45)
        gemas_h += T.flare(gx, gy, 0.32 * kk + 0.01, ang=0.0, thin=0.014) * kk
        caudas.append((0.08 + (d - 0.12) * math.cos(a), (d - 0.12) * math.sin(a), gx, gy, vida * 0.8 * (1 - u)))
    Gm = T.polys(gemas, 0.004) if gemas else T.zero()
    Cd = T.tapered(caudas, 0.035) if caudas else T.zero()
    G += ((P * 1.2 + J * 0.8) * vis + linhas * 0.9 + est + g + anel + Gm * 1.5 + T.blur(Gm, 0.02) * 1.2 + gemas_h + Cd * 0.6) * env
    H += ((P * 0.3 + J * 1.6) * vis + linhas * 0.4 + est * 0.8 + h + anel * 0.5 + Gm * 1.3 + gemas_h * 1.3 + Cd * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Feiticeira Escarlate
def magia_do_caos(T, t, rng):
    """Raio de caos: fios ondulados de magia do caos chegam girando em espiral, apertam em volta
    do alvo como um novelo, e estouram para fora em fiapos tortos."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    aperta = ease_in(rel(t, 0.0, 0.5), 1.3)
    vis = janela(t, 0.0, 0.06) * (1 - rel(t, 0.5, 0.62))
    fios = T.zero()
    for j in range(4):
        pts = []
        for m in range(46):
            u = m / 45
            a = j * TAU / 4 + u * 2.6 * math.pi + t * 9
            r = (0.85 - 0.55 * aperta) * (1 - 0.65 * u) + 0.05
            ond = 0.035 * math.sin(u * 22 + t * 30 + j)
            pts.append(((r + ond) * math.cos(a), (r + ond) * math.sin(a) * 0.9))
        fios += T.polyline(pts, 0.03 - 0.006 * (j % 2))
    noise_u = T.noise(np.random.default_rng(1964), 0.18, 2) * 0.03
    noise_v = T.noise(np.random.default_rng(1965), 0.18, 2) * 0.03
    fios = T.warp(fios, noise_u, noise_v) * vis
    novelo = T.gauss(0, 0, 0.12 + 0.1 * aperta, 0.12 + 0.1 * aperta) * aperta * vis * 0.9
    k = pulso(t, 0.5, 0.78)
    g, h = _clarao(T, k, 0.0, 0.0, 0.3, 0.8)
    est = T.zero()
    u = ease_out(rel(t, 0.5, 0.88), 2)
    for j in range(7):
        a0 = j / 7 * TAU + 0.3
        r0, r1 = 0.1 + 0.45 * u, 0.3 + 0.6 * u
        pts = []
        for m in range(14):
            w = m / 13
            r = r0 + (r1 - r0) * w
            pts.append((r * math.cos(a0 + 1.4 * w * w), r * math.sin(a0 + 1.4 * w * w)))
        est += T.polyline(pts, 0.03 * (1 - 0.5 * u))
    est = est * pulso(t, 0.5, 0.95)
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.5, 0.88), 2), 0.05) * pulso(t, 0.5, 0.9)
    anel = T.warp(anel, noise_u * 2, noise_v * 2)
    G += (T.blur(fios, 0.018) * 1.4 + fios * 1.2 + novelo + g + est * 1.3 + T.blur(est, 0.02) + anel) * env
    H += (fios * 0.75 + novelo * 0.6 + h + est * 0.8 + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Homem-Formiga
def soco_de_pym(T, t, rng):
    """Soco de Pym: um risquinho minúsculo zune até o alvo enquanto os anéis de partículas Pym se
    fecham nele (encolhe); de repente o punho cresce num estalo, e os anéis abrem com o impacto."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    zip_ = ease_in(rel(t, 0.0, 0.16), 1.2)
    zx = -1.0 + 0.82 * zip_
    risco = T.tapered([(zx - 0.45, 0.0, zx, 0.0, 1.0)], 0.03) * janela(t, 0.0, 0.03) * (1 - rel(t, 0.15, 0.22))
    pontinho = T.gauss(zx, 0.0, 0.025, 0.025) * (1 - rel(t, 0.3, 0.32)) * 1.6
    fecha = 0
    for j in range(3):
        a0 = 0.06 + 0.06 * j
        u = ease_in(rel(t, a0, a0 + 0.16), 1.5)
        if 0 < u < 1:
            fecha = fecha + T.ring(0.6 * (1 - u) + 0.04, 0.03, -0.18, 0.0) * (0.5 + 0.5 * u)
    # partículas Pym: pontos que correm nos anéis que se fecham
    sub = np.random.default_rng(1963)
    pts = []
    for j in range(18):
        a = sub.uniform(0, TAU) + t * 8
        a0 = sub.uniform(0.04, 0.16)
        u = ease_in(rel(t, a0, a0 + 0.14), 1.5)
        if 0 < u < 1:
            r = 0.55 * (1 - u) + 0.05
            pts.append((-0.18 + r * math.cos(a), r * math.sin(a), 1.0))
    Pp = T.splats(pts, 0.016) if pts else T.zero()
    cresce = back(rel(t, 0.3, 0.42), 2.2)
    vis = janela(t, 0.3, 0.31) * (1 - rel(t, 0.55, 0.68))
    esc = 0.12 + 1.38 * cresce
    P, vinco = _punho(T, -0.18 - 0.08 * cresce, 0.0, esc, 0.0, 0.35)
    est, k = _estouro(T, t, 0.38, 0.62, 0.06, 0.0, 0.38, 8, 0.34, 0.3)
    g, h = _clarao(T, k, 0.06, 0.0, 0.28, 0.9)
    abre = 0
    for j, a0 in enumerate((0.33, 0.39, 0.46)):
        u = ease_out(rel(t, a0, a0 + 0.38), 2)
        abre = abre + T.ring(0.08 + 0.7 * u, 0.035, 0.0, 0.0) * pulso(t, a0, a0 + 0.42) * (1.2 - 0.2 * j)
    sai = []
    for j in range(16):
        a = j / 16 * TAU + 0.2
        u = ease_out(rel(t, 0.36, 0.8), 2)
        r = 0.12 + 0.62 * u
        sai.append((r * math.cos(a), r * math.sin(a), pulso(t, 0.36, 0.9)))
    S = T.splats(sai, 0.016)
    G += (risco * 1.4 + pontinho + fecha * 1.2 + Pp * 1.5 + P * 1.2 * vis + est + g + abre + S * 1.3) * env
    H += (risco * 0.9 + pontinho * 1.2 + fecha * 0.6 + Pp * 1.2 + P * 0.35 * vis + est * 0.8 + h + abre * 0.45 + S) * env
    return G, H


# ------------------------------------------------------------------ Capitã Marvel
def punho_fotonico(T, t, rng):
    """Punho fotônico: o punho chega envolto numa chama de energia fotônica (o rastro brilhante para
    trás), acerta e estoura numa estrela de oito pontas com raios de luz para todos os lados."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.24), 1.6)
    fx = -0.98 + 0.84 * vem
    vis = 1 - rel(t, 0.3, 0.44)
    P, vinco = _punho(T, fx, 0.0, 1.3, 0.0, 0.45)
    aura = T.blur(P, 0.06) * 1.0
    linguas = []
    for j in range(7):
        y = (j - 3) * 0.055
        comp = 0.35 + 0.25 * abs(math.sin(t * 40 + j * 1.7))
        linguas.append((lamina(fx + 0.12, y, fx - 0.2 - comp, y * 1.6 + 0.04 * math.sin(t * 30 + j), 0.05), 0.6))
    L = T.polys(linguas, 0.015)
    brilhos = T.zero()
    sub = np.random.default_rng(2019)
    for j in range(5):
        bx, by = fx + sub.uniform(-0.45, 0.1), sub.uniform(-0.3, 0.3)
        kk = max(0.0, math.sin(t * 50 + j * 2.1))
        brilhos += T.flare(bx, by, 0.12 * kk + 0.01, ang=0.0, thin=0.02) * kk
    k = pulso(t, 0.22, 0.52)
    estrela8 = T.polys([(estrela(0.08, 0.0, 0.42 * back(rel(t, 0.22, 0.32), 1.5) + 0.01, -math.pi / 2, 8, 0.42), 1.0)], 0.005) * k
    g, h = _clarao(T, k, 0.08, 0.0, 0.3, 1.1)
    raios = []
    for j in range(16):
        a = j / 16 * TAU + 0.1
        u = ease_out(rel(t, 0.24, 0.55), 2)
        comp = (0.75 if j % 2 == 0 else 0.5) * u
        r0 = 0.12 + 0.35 * rel(t, 0.45, 0.85)
        raios.append((0.08 + math.cos(a) * (r0 + comp), math.sin(a) * (r0 + comp), 0.08 + math.cos(a) * r0, math.sin(a) * r0, 1.0))
    R = T.tapered(raios, 0.04) * pulso(t, 0.23, 0.85)
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.24, 0.7), 2), 0.04, 0.08) * pulso(t, 0.24, 0.75)
    G += ((P * 1.2 + aura + L * 1.2 + brilhos) * vis + estrela8 * 1.3 + g + R * 1.3 + anel) * env
    H += ((P * 0.45 + aura * 0.2 + L * 0.5 + brilhos) * vis + estrela8 * 1.1 + h + R * 0.9 + anel * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Motoqueiro Fantasma
def _elos(caminho_pts, tam=0.055):
    """Elos de corrente ao longo de um caminho: elipses de frente alternando com elos de lado (traço)."""
    segs = []
    for k in range(len(caminho_pts) - 1):
        (x1, y1), (x2, y2) = caminho_pts[k], caminho_pts[k + 1]
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        ang = math.atan2(y2 - y1, x2 - x1)
        if k % 2 == 0:
            segs += _contorno_segs(_elipse(cx, cy, tam * 1.15, tam * 0.62, ang, 14))
        else:
            segs.append((x1 + (x2 - x1) * 0.1, y1 + (y2 - y1) * 0.1, x2 - (x2 - x1) * 0.1, y2 - (y2 - y1) * 0.1, 1.0))
    return segs


def _reamostra(pts, passo):
    """Pontos igualmente espaçados ao longo de uma linha quebrada."""
    saida = [pts[0]]
    falta = passo
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d = math.hypot(x2 - x1, y2 - y1)
        pos = 0.0
        while d - pos >= falta:
            pos += falta
            saida.append((x1 + (x2 - x1) * pos / d, y1 + (y2 - y1) * pos / d))
            falta = passo
        falta -= d - pos
    return saida


def corrente_flamejante(T, t, rng):
    """Corrente flamejante: a corrente em chamas chicoteia da esquerda numa onda, enrola em volta do
    alvo (as voltas se fechando) e as chamas sobem dos elos antes de tudo estourar em brasas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    chicote = ease_out(rel(t, 0.0, 0.28), 1.6)
    enrola = ease_out(rel(t, 0.26, 0.5), 1.8)
    pts = []
    if t < 0.28:
        # a onda do chicote: o caminho cresce da mão até o alvo
        for k in range(26):
            u = k / 25 * chicote
            x = -1.05 + 1.05 * u
            y = -0.5 * math.sin(math.pi * u / max(chicote, 0.05)) * (1.25 - chicote) + 0.1 * math.sin(u * 12 - t * 40) * (1 - chicote)
            pts.append((x, y))
    else:
        # parte reta até perto do alvo, depois voltas em volta do centro
        reta = [(-1.05 + 0.7 * k / 7, 0.18 * k / 7) for k in range(8)]
        voltas = []
        tot = 1.4 + 2.4 * enrola
        for k in range(30):
            u = k / 29
            a = math.pi + u * tot * math.pi
            r = 0.4 - 0.06 * u
            voltas.append((r * math.cos(a), r * math.sin(a) * 0.55 + 0.18 * (1 - u) * (1 - enrola) + (u - 0.5) * 0.18))
        pts = reta + voltas
    elos = _reamostra(pts, 0.1)
    vis = janela(t, 0.0, 0.03) * (1 - rel(t, 0.66, 0.8))
    C = T.lines(_elos(elos, 0.068), 0.028, 0.002) * vis
    # chamas que sobem dos elos
    chamas = []
    for k, (x, y) in enumerate(elos[::2]):
        alt = 0.12 + 0.12 * abs(math.sin(t * 31 + k * 1.9)) + 0.12 * janela(t, 0.3, 0.5)
        chamas.append((_chama(x, y + 0.03, alt, 0.05, t * 40 + k, 0.5), 0.55))
    F = T.polys(chamas, 0.015) * vis if chamas else T.zero()
    kk = pulso(t, 0.6, 0.92)
    g, h = _clarao(T, kk, 0.0, 0.0, 0.32, 0.7)
    fogareu = T.polys([(_chama(x, 0.35, 0.75 * kk * (1 - abs(x) * 0.9) + 0.01, 0.12, t * 30 + x * 9, 0.4), 0.8) for x in (-0.36, -0.18, 0.0, 0.18, 0.36)], 0.02) * kk
    brasas = faiscas(T, np.random.default_rng(1972), t, 16, 0.7, 0.03, (-math.pi * 0.95, -0.05), -0.3, inicio=0.62)
    G += (C * 1.3 + T.blur(C, 0.02) * 0.8 + F * 1.3 + g * 0.8 + fogareu * 1.2 + brasas * 1.3) * env
    H += (C * 1.0 + F * 0.35 + h * 0.8 + fogareu * 0.4 + brasas) * env
    return G, H


REGISTRO = [
    ("batarangue", batarangue, GRANDE, "Batarangue: o morcego girando que crava no alvo", False),
    ("soco_de_aco", soco_de_aco, GRANDE, "Soco de aço: barreira do som e anéis de choque", False),
    ("teia_e_soco", teia_e_soco, GRANDE, "Teia e soco: o fio gruda em teia e o soco chega", False),
    ("disparo_arcano", disparo_arcano, GRANDE, "Disparo arcano: mandala de runas e faíscas arcanas", False),
    ("bracelete", bracelete, GRANDE, "Golpe de bracelete: braceletes em X e o soco", False),
    ("escudo_do_capitao", escudo_do_capitao, GRANDE, "Escudo arremessado: o escudo da estrela que quica", False),
    ("corvo_da_alma", corvo_da_alma, GRANDE, "Energia da alma: o corvo escuro que mergulha", False),
    ("manopla", manopla, GRANDE, "Punho do Titã: a manopla e as seis joias", False),
    ("magia_do_caos", magia_do_caos, GRANDE, "Raio de caos: fios em espiral que estouram", False),
    ("soco_de_pym", soco_de_pym, GRANDE, "Soco de Pym: o soco minúsculo que cresce", False),
    ("punho_fotonico", punho_fotonico, GRANDE, "Punho fotônico: o punho em luz e a estrela de oito pontas", False),
    ("corrente_flamejante", corrente_flamejante, GRANDE, "Corrente flamejante: a corrente em chamas que enrola", False),
]
