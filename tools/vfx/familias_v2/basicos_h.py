"""Ataques básicos com animação própria, lote h.

Cada folha conta o golpe básico do personagem: as dezenas de chutes da Chun-Li,
a kunai na corda do Scorpion, o chute voador com o dragão de fogo do Liu Kang,
o soco com os raios do Gene do Diabo do Kazuya, a chave-espada do Sora, o
"clang" de aparar e o corte do Sekiro, a Dança da Ave Aquática da Malenia, o
corte rúnico gelado da Frostmourne, a mira de três pontos do cortador de plasma
do Isaac, a arma da gravidade do Gordon, a Grande Faca arrastada do Pyramid
Head, a adaga com a areia do tempo voltando e o corte da espada do Alucard
virando morcegos.
"""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, apaga, back, contorno, ease_in, ease_out, estrela, faiscas, forma, girado,  # noqa: F401
                   jagged, janela, lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


# ------------------------------------------------------------------ ajudantes
def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.26, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.4
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.6 * k + 0.01, ang=ang + math.pi / 2, thin=0.012)) * k * 1.5
    return g, h


def _estouro(T, k, cx=0.0, cy=0.0, r=0.3, ang=0.3, n=7):
    """Estrela de impacto (desenho de quadrinho)."""
    if k <= 0:
        return T.zero()
    return T.polys([(estrela(cx, cy, r * k + 0.01, ang, n, 0.38), 1.0)], 0.006) * k


def _chama(cx, base, alt, larg, fase, ondula=0.25):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    pts = []
    for k in range(13):
        u = k / 12
        w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
        pts.append((cx + w + ondula * larg * math.sin(fase + 6 * u) * u, base - alt * u))
    for k in range(12, -1, -1):
        u = k / 12
        w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
        pts.append((cx - w + ondula * larg * math.sin(fase + 6 * u) * u, base - alt * u))
    return pts


def _faixa(pts, larguras):
    """Polígono de uma linha grossa com largura variável (corpo de serpente, corda grossa)."""
    cima, baixo = [], []
    for i, ((x, y), w) in enumerate(zip(pts, larguras)):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        cima.append((x + nx * w, y + ny * w))
        baixo.append((x - nx * w, y - ny * w))
    return cima + baixo[::-1]


# ================================================================== Chun-Li
def _perna(hx, hy, fx, fy, larg):
    """Silhueta de perna esticada: coxa grossa, joelho, canela fina e o pé em ponta."""
    dx, dy = fx - hx, fy - hy
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    cima, baixo = [], []
    for k in range(9):
        u = k / 8
        w = larg * (1.0 - 0.6 * u) * (1 - 0.12 * math.sin(math.pi * min(1, u * 2)))
        x, y = hx + dx * u, hy + dy * u
        cima.append((x + nx * w, y + ny * w))
        baixo.append((x - nx * w, y - ny * w))
    # o pé: peito do pé para cima, ponta adiante
    pe = [(fx + nx * larg * 0.55, fy + ny * larg * 0.55), (fx + ux * larg * 1.5 + nx * larg * 0.15, fy + uy * larg * 1.5 + ny * larg * 0.15),
          (fx + ux * larg * 1.2 - nx * larg * 0.4, fy + uy * larg * 1.2 - ny * larg * 0.4)]
    return cima + pe + baixo[::-1]


def chute_relampago(T, t, rng):
    """Chute relâmpago (Hyakuretsukyaku): a perna vira um leque de borrões, dezenas de chutes
    por segundo saindo do quadril à esquerda; cada pé estala no alvo e o último chute estoura."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    ativo = janela(t, 0.0, 0.06) * (1 - rel(t, 0.72, 0.8))
    hx, hy = -1.05, 0.08
    # o leque: borrão de todas as posições da perna
    leque = []
    for k in range(17):
        a = -0.5 + k / 16
        leque.append((hx + math.cos(a) * 0.35, hy + math.sin(a) * 0.35))
    for k in range(16, -1, -1):
        a = -0.5 + k / 16
        leque.append((hx + math.cos(a) * 1.05, hy + math.sin(a) * 1.05))
    L = T.blur(T.polys([(leque, 1.0)], 0.0), 0.05) * 0.45 * ativo
    # as pernas do quadro: três a quatro chutes ao mesmo tempo, mudando a cada quadro
    q = int(round(t * 11))
    sub = np.random.default_rng(700 + q * 13)
    pernas, pes, est = [], [], T.zero()
    if ativo > 0.05:
        for j in range(6):
            a = sub.uniform(-0.45, 0.45)
            comp = sub.uniform(0.98, 1.08)
            fx, fy = hx + math.cos(a) * comp, hy + math.sin(a) * comp
            peso = 1.0 if j == 0 else (0.6 if j < 3 else 0.3)
            pernas.append((_perna(hx, hy, fx, fy, 0.1 if j == 0 else 0.085), peso))
            pes.append((fx + math.cos(a) * 0.08, fy + math.sin(a) * 0.08))
        for j, (px, py) in enumerate(pes[:3]):
            est += _estouro(T, 1.0 if j == 0 else 0.6, px, py, 0.13, sub.uniform(0, 1), 6)
    P = T.polys(pernas, 0.006) * ativo
    # linhas de velocidade em leque
    rl = []
    for k in range(9):
        a = -0.45 + 0.9 * k / 8 + 0.03 * math.sin(q * 3.1 + k)
        rl.append((hx + math.cos(a) * 0.45, hy + math.sin(a) * 0.45, hx + math.cos(a) * 0.95, hy + math.sin(a) * 0.95, 0.6))
    R = T.lines(rl, 0.008, 0.004) * ativo * (0.5 + 0.5 * (q % 2))
    # o último chute: estrela grande, clarão e anel
    k2 = pulso(t, 0.7, 0.98)
    g, h = _clarao(T, k2, 0.05, 0.0, 0.25, 0.85)
    fim = _estouro(T, k2, 0.05, 0.0, 0.36, 0.2, 8)
    anel = T.ring(0.1 + 0.55 * ease_out(rel(t, 0.7, 0.98), 2), 0.035) * pulso(t, 0.7, 1.0)
    G += (L + P * 1.25 + T.blur(P, 0.03) * 0.5 + est * 1.3 + R + g + fim * 1.2 + anel) * env
    H += (P * 0.35 + est * 0.9 + R * 0.4 + h + fim * 0.8 + anel * 0.4) * env
    return G, H


# ================================================================== Scorpion
def _kunai(tx, ty, esc=1.0):
    """Ponta de lança (kunai) apontando para +x, com a ponta em (tx, ty)."""
    folha = [(0.0, 0.0), (-0.08, -0.06), (-0.17, -0.022), (-0.17, 0.022), (-0.08, 0.06)]
    cabo = [(-0.17, -0.016), (-0.27, -0.016), (-0.27, 0.016), (-0.17, 0.016)]
    return [(_move(folha, tx, ty, esc), 1.0), (_move(cabo, tx, ty, esc), 0.8)]


def kunai_do_inferno(T, t, rng):
    """Kunai do inferno: a kunai voa presa à corda ondulando, crava no alvo com um estalo e
    chamas do inferno; a corda estica, treme e puxa a kunai de volta deixando fogo no caminho."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    esc = 1.9
    voa = ease_in(rel(t, 0.0, 0.26), 1.4)
    volta = ease_in(rel(t, 0.56, 0.84), 2.0)
    kx = -0.95 + 1.1 * voa - 1.3 * volta
    ky = -0.06 + 0.06 * voa - 0.05 * math.sin(math.pi * voa)
    kx += 0.02 * math.sin(t * 90) * pulso(t, 0.44, 0.6)
    vis_k = 1 - rel(t, 0.82, 0.88)
    K = T.polys(_kunai(kx, ky, esc), 0.004) * vis_k
    argola = T.ring(0.035, 0.012, cx=kx - 0.31 * esc, cy=ky) * vis_k
    # a corda: ondula no voo, fica reta e tensa no puxão
    cx0 = kx - 0.33 * esc
    tensa = janela(t, 0.4, 0.5)
    amp = 0.09 * (1 - tensa) * (1 - 0.6 * voa)
    pts = []
    for k in range(40):
        u = k / 39
        x = -1.1 + (cx0 + 1.1) * u
        y = ky + amp * math.sin(u * math.pi * 3.2 - t * 24) * math.sin(math.pi * u) + (1 - tensa) * 0.06 * math.sin(math.pi * u)
        y += tensa * 0.012 * math.sin(u * 40 + t * 120) * pulso(t, 0.44, 0.62)
        pts.append((x, y))
    corda = T.polyline(pts, 0.024 + 0.008 * tensa) * (1 - rel(t, 0.82, 0.9))
    # fogo na kunai durante o voo e no puxão
    ch = []
    for j in range(3):
        ch.append((_gira(_chama(0.0, 0.0, 0.3 + 0.08 * j, 0.08, t * 40 + j * 2, 0.5), -math.pi / 2, kx - 0.3 - 0.1 * j, ky), 0.9))
    fogo_k = T.polys(ch, 0.02) * (pulso(t, 0.0, 0.3) + pulso(t, 0.56, 0.86)) * 1.3
    # cravou: estalo, clarão e chamas do inferno subindo em volta
    k = pulso(t, 0.24, 0.5)
    g, h = _clarao(T, k, 0.12, -0.02, 0.2, 0.6)
    crav = _estouro(T, k, 0.12, -0.02, 0.24, 0.5, 6)
    chamas = []
    for j in range(7):
        x = -0.45 + 0.9 * j / 6
        a0 = 0.27 + 0.025 * abs(j - 3)
        alt = 0.72 * ease_out(rel(t, a0, a0 + 0.14), 2) * (1 - 0.4 * abs(j - 3) / 3) * (0.8 + 0.25 * abs(math.sin(t * 27 + j * 1.9)))
        if alt > 0.02:
            chamas.append((_chama(x, 0.5, alt, 0.11, t * 33 + j * 1.4, 0.6), 0.75))
    C = T.polys(chamas, 0.018) * (1 - rel(t, 0.62, 0.86))
    # o puxão: rastro de fogo atrás da kunai voltando
    rastro = T.polys([(lamina(kx + 0.05, ky, min(kx + 1.0, 0.5), ky, 0.05, 1.0, 0.0), 1.0)], 0.02) * pulso(t, 0.58, 0.88)
    G += (K * 1.3 + argola + corda * 1.1 + fogo_k + crav * 1.2 + g + C * 1.1 + rastro * 0.9) * env
    H += (K * 0.8 + argola * 0.5 + corda * 0.35 + crav * 0.8 + h + C * 0.35 + rastro * 0.5) * env
    return G, H


# ================================================================== Liu Kang
_CABECA_DRAGAO = [
    # mandíbula de cima, mandíbula de baixo, chifres e juba; boca aberta para +x
    ([(-0.14, -0.02), (-0.1, -0.09), (0.0, -0.105), (0.14, -0.065), (0.17, -0.035), (0.03, -0.025)], 1.0),
    ([(-0.12, 0.01), (0.03, 0.02), (0.14, 0.065), (0.11, 0.09), (-0.06, 0.075)], 1.0),
    ([(-0.07, -0.085), (-0.27, -0.21), (-0.12, -0.06)], 0.9),
    ([(-0.12, -0.06), (-0.32, -0.12), (-0.15, -0.03)], 0.8),
    ([(-0.12, 0.05), (-0.3, 0.15), (-0.15, 0.015)], 0.8),
]


def chute_do_dragao(T, t, rng):
    """Chute do dragão: o chute voador vem envolto num dragão de fogo — cabeça de boca aberta
    na frente do pé, corpo serpenteando com cristas de chama — e explode no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    p = ease_out(rel(t, 0.0, 0.32), 1.6)

    def caminho(u):
        return -1.25 + 1.3 * u, -0.22 + 0.22 * u

    hx, hy = caminho(p)
    vivo = 1 - rel(t, 0.36, 0.5)
    ang = math.atan2(0.22, 1.3)
    # o corpo: atrás da cabeça, ondulando
    pts, ws = [], []
    for k in range(34):
        d = k / 33 * 0.95
        bx, by = caminho(p - d / 1.32)
        onda = 0.11 * math.sin(d * 8.5 - t * 26) * min(1, d * 3)
        pts.append((bx - math.sin(ang) * onda, by + math.cos(ang) * onda))
        ws.append(0.11 * (1 - d / 0.95) ** 0.7 + 0.015)
    corpo = T.polys([(_faixa(pts, ws), 1.0)], 0.008) * vivo
    cristas = []
    for k in range(3, 30, 4):
        x, y = pts[k]
        cristas.append((_chama(x, y - ws[k] * 0.6, 0.12 + 0.12 * ws[k] / 0.09, ws[k] * 0.8, t * 40 + k, 0.7), 0.7))
    C = T.polys(cristas, 0.012) * vivo
    cab = [(_move(_gira(f, ang, 0, 0), hx, hy, 1.8), w) for f, w in _CABECA_DRAGAO]
    Cb = T.polys(cab, 0.004) * vivo
    ox, oy = _gira([(-0.03, -0.06)], ang)[0]
    olho = T.gauss(hx + ox * 1.8, hy + oy * 1.8, 0.022) * vivo * 2
    # a perna dentro do dragão (núcleo)
    perna = T.polys([(lamina(hx - 0.85, hy + 0.08, hx + 0.05, hy + 0.02, 0.05, 1.0), 1.0)], 0.01) * vivo * janela(t, 0.04, 0.12)
    # impacto: o dragão estoura em fogo
    k = pulso(t, 0.3, 0.68)
    g, h = _clarao(T, k, 0.05, 0.0, 0.28, 0.85)
    est = _estouro(T, k, 0.05, 0.0, 0.34, 0.1, 8)
    labaredas = []
    for j in range(9):
        a = j / 9 * TAU + 0.3
        alt = 0.55 * ease_out(rel(t, 0.32, 0.55), 2) * (0.75 + 0.3 * math.sin(j * 2.3))
        if alt > 0.02:
            labaredas.append((_gira(_chama(0.0, -0.12, alt, 0.11, t * 30 + j, 0.5), a + math.pi / 2, 0.05, 0.0), 0.7))
    L = T.polys(labaredas, 0.02) * pulso(t, 0.32, 0.85)
    sub = np.random.default_rng(55)
    br = []
    tt = rel(t, 0.34, 1.0)
    for _ in range(22):
        a = sub.uniform(0, TAU)
        d = 0.15 + 0.6 * ease_out(tt, 2) * sub.uniform(0.4, 1)
        br.append((0.05 + d * math.cos(a), d * math.sin(a) - 0.2 * tt, (1 - tt) * sub.uniform(0.5, 1) * (tt > 0)))
    B = T.splats(br, 0.013)
    G += (corpo * 1.1 + T.blur(corpo, 0.03) * 0.6 + C + Cb * 1.3 + olho + perna * 0.6 + g + est * 1.1 + L * 1.1 + B * 1.5) * env
    H += (corpo * 0.25 + Cb * 0.5 + olho * 1.5 + perna * 0.9 + h + est * 0.7 + L * 0.35 + B) * env
    return G, H


# ================================================================== Kazuya
_PUNHO = [(0.13, -0.1), (0.17, -0.04), (0.17, 0.05), (0.11, 0.11), (-0.06, 0.11), (-0.1, 0.06), (-0.1, -0.08), (-0.04, -0.12)]


def soco_do_diabo(T, t, rng):
    """Soco do Diabo: o punho vem envolto em raios roxos crepitando pelo braço, acerta com um
    estrondo elétrico e os raios do Gene do Diabo se abrem em garras em volta do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    p = ease_in(rel(t, 0.0, 0.2), 1.5)
    fx = -0.85 + 0.85 * p
    voo = 1 - rel(t, 0.5, 0.62)
    esc = 1.45
    P = T.polys([(_move(_PUNHO, fx - 0.1, 0.0, esc), 1.0)], 0.005) * voo
    dx = fx - 0.1 + 0.17 * esc
    dedos = T.lines([(dx - 0.09, -0.1 + 0.065 * k, dx - 0.01, -0.1 + 0.065 * k, 1) for k in range(4)], 0.008) * voo
    braco = T.polys([(lamina(-1.2, 0.03, fx - 0.18, 0.02, 0.09, 1.0), 1.0)], 0.01) * voo
    q = int(round(t * 11))
    sub = np.random.default_rng(300 + q * 7)
    # raios correndo pelo braço
    rb = T.zero()
    if voo > 0:
        for _ in range(3):
            rb += T.polyline(jagged(sub, -1.0, sub.uniform(-0.05, 0.05), fx + 0.1, sub.uniform(-0.08, 0.08), 5, 0.22), 0.013)
        rb *= voo
    # impacto
    k = pulso(t, 0.18, 0.5)
    g, h = _clarao(T, k, 0.08, 0.0, 0.3, 0.95)
    est = _estouro(T, k, 0.08, 0.0, 0.34, 0.15, 7)
    anel = T.ring(0.12 + 0.6 * ease_out(rel(t, 0.18, 0.6), 2), 0.04) * pulso(t, 0.18, 0.66)
    # garras de raio para fora, com galhos
    gar = T.zero()
    if 0.2 < t < 0.82:
        abre = ease_out(rel(t, 0.2, 0.42), 2)
        for j in range(7):
            a = j / 7 * TAU + 0.2 + sub.uniform(-0.15, 0.15)
            r = (0.35 + 0.45 * sub.uniform(0.6, 1)) * abre
            ex, ey = 0.08 + r * math.cos(a), r * math.sin(a)
            gar += T.polyline(jagged(sub, 0.08, 0.0, ex, ey, 4, 0.32), 0.016)
            mx, my = 0.08 + r * 0.55 * math.cos(a), r * 0.55 * math.sin(a)
            gar += T.polyline(jagged(sub, mx, my, mx + 0.25 * r * math.cos(a + 0.7), my + 0.25 * r * math.sin(a + 0.7), 3, 0.3), 0.01) * 0.8
        gar *= (0.6 + 0.4 * sub.uniform()) * (1 - rel(t, 0.62, 0.82))
    G += (P * 1.3 + braco * 0.5 + T.glow(rb, 1.3, 1.5, 0.025) + g + est * 1.2 + anel + T.glow(gar, 1.3, 1.6, 0.025)) * env
    H += (P * 0.45 + dedos * 0.6 + braco * 0.2 + rb * 1.2 + h + est * 0.8 + anel * 0.4 + gar * 1.3) * env
    return G, H


# ================================================================== Sora
def _chave(ang, px, py, esc=1.0):
    """A chave-espada: cabo com guarda em arco, lâmina reta e os dentes da chave na ponta."""
    cabo = [(-0.13, -0.022), (0.12, -0.022), (0.12, 0.022), (-0.13, 0.022)]
    lam = [(0.12, -0.03), (0.86, -0.03), (0.86, 0.03), (0.12, 0.03)]
    dentes = [(0.7, 0.02), (0.93, 0.02), (0.93, 0.22), (0.86, 0.22), (0.86, 0.13), (0.8, 0.13), (0.8, 0.18), (0.7, 0.18)]
    topo = [(0.86, -0.06), (0.95, -0.06), (0.95, 0.03), (0.86, 0.03)]
    formas = [(cabo, 0.9), (lam, 1.0), (dentes, 1.0), (topo, 1.0)]
    guarda = []
    for k in range(15):
        a = math.pi / 2 + math.pi * k / 14
        guarda.append((0.04 - 0.1 * math.cos(a), 0.11 * math.sin(a)))
    return [(_move(_gira(f, ang), px, py, esc), w) for f, w in formas], _move(_gira(guarda, ang), px, py, esc)


def keyblade(T, t, rng):
    """Chave-espada: a chave grande (cabo com guarda, lâmina e os dentes na ponta) desce num arco
    brilhante, acerta o alvo e solta estrelinhas mágicas que piscam em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    pvx, pvy = -0.62, 0.4
    a0, a1 = -2.5, -0.08
    p = ease_out(rel(t, 0.0, 0.3), 2.2)
    ang = a0 + (a1 - a0) * p
    vis = 1 - rel(t, 0.55, 0.8)
    formas, guarda = _chave(ang, pvx, pvy, 1.0)
    K = T.polys(formas, 0.004) * vis
    Gd = T.polyline(guarda, 0.022) * vis
    arco = T.arc_band(0.8, 0.13, a0, ang + 0.01, cx=pvx, cy=pvy, crescente=True) * (1 - rel(t, 0.3, 0.6)) if p > 0.02 else T.zero()
    # impacto quando a lâmina passa pelo centro
    k = pulso(t, 0.16, 0.48)
    g, h = _clarao(T, k, 0.0, 0.0, 0.22, 0.8, 0.0)
    est = T.polys([(estrela(0.0, 0.0, 0.3 * k + 0.01, -math.pi / 2, 5, 0.45), 1.0)], 0.006) * k
    # estrelinhas: cruzes de quatro pontas que piscam em volta
    sub = np.random.default_rng(81)
    br, bh = T.zero(), T.zero()
    for j in range(11):
        a = sub.uniform(0, TAU)
        d = sub.uniform(0.28, 0.72)
        t0 = 0.2 + 0.4 * j / 10
        kk = pulso(t, t0, t0 + 0.28)
        if kk <= 0:
            continue
        x, y = d * math.cos(a), d * math.sin(a) - 0.12 * rel(t, t0, 1)
        tam = sub.uniform(0.35, 0.55) * kk
        f = T.flare(x, y, tam, 0.0, 0.03)
        br += f + T.gauss(x, y, 0.025) * kk * 1.5
        bh += f * 0.9
    # estrelas de cinco pontas ao longo do arco
    est5 = []
    for j in range(4):
        u = 0.25 + 0.2 * j
        a = a0 + (ang - a0) * u
        x, y = pvx + 0.8 * math.cos(a), pvy + 0.8 * math.sin(a)
        est5.append((estrela(x, y, 0.06, t * 6 + j, 5, 0.45), pulso(t, 0.1 + 0.05 * j, 0.6 + 0.05 * j)))
    E5 = T.polys(est5, 0.004)
    G += (K * 1.3 + Gd * 1.2 + T.glow(arco, 1.0, 1.0, 0.03) + g + est * 1.2 + br * 1.3 + E5 * 1.2) * env
    H += (K * 0.6 + Gd * 0.5 + arco * 0.6 + h + est * 0.8 + bh + E5 * 0.8) * env
    return G, H


# ================================================================== Sekiro
def aparar_e_cortar(T, t, rng):
    """Kusabimaru: as lâminas se cruzam e a deflexão solta o "clang" — clarão em cruz e um leque
    de faíscas —, e logo depois o contra-corte risca o alvo na diagonal."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    # as duas lâminas se cruzando (a nossa vem da esquerda, a do rival de cima à direita)
    cr = 1 - rel(t, 0.18, 0.34)
    nossa = T.polys([(lamina(-0.95, 0.35, 0.25, -0.35, 0.03, 1.0), 1.0)], 0.003) * cr
    dele = T.polys([(lamina(0.7, -0.75, -0.2, 0.2, 0.03, 1.0), 1.0)], 0.003) * cr * 0.7
    cx, cy = -0.05, -0.05
    k = pulso(t, 0.0, 0.32)
    flash = T.flare(cx, cy, 1.5 * k + 0.01, 0.15, 0.012) + T.flare(cx, cy, 0.9 * k + 0.01, 0.15 + math.pi / 4, 0.01) * 0.6
    nucleo = T.gauss(cx, cy, 0.09) * k * 2.4
    anel = T.ring(0.06 + 0.42 * ease_out(rel(t, 0.0, 0.3), 2.5), 0.02, cx, cy) * pulso(t, 0.0, 0.34) * 1.4
    fa = faiscas(T, np.random.default_rng(17), t, 26, 0.85, 0.035, cone=(-math.pi + 0.2, -0.2), gravidade=0.5, cx=cx, cy=cy)
    fa2 = faiscas(T, np.random.default_rng(18), t, 10, 0.6, 0.03, cone=(0.3, 2.8), gravidade=0.4, cx=cx, cy=cy, inicio=0.02)
    F = (fa + fa2 * 0.7) * apaga(t, 0.55, 0.8)
    # o contra-corte
    pc = ease_out(rel(t, 0.4, 0.52), 2.5)
    corte, fio = T.zero(), T.zero()
    if pc > 0:
        ini = rel(t, 0.6, 0.92)
        corte = T.polys([(lamina(-0.78, -0.62, 0.78, 0.6, 0.075, pc, ini), 1.0)], 0.004)
        fio = T.polys([(lamina(-0.78, -0.62, 0.78, 0.6, 0.022, pc, ini), 1.0)], 0.002)
    g2 = T.gauss(0, 0, 0.32, 0.07) * pulso(t, 0.44, 0.7) * 1.2
    G += (nossa + dele + flash * 1.3 + nucleo + anel + T.glow(F, 1.1, 1.2, 0.02) + T.glow(corte, 1.1, 1.3, 0.025) + fio + g2) * env
    H += (nossa * 0.6 + dele * 0.4 + flash * 1.3 + nucleo + anel * 0.5 + F * 0.8 + fio * 1.6 + corte * 0.3 + g2 * 0.5) * env
    return G, H


# ================================================================== Malenia
def _petala(cx, cy, tam, ang):
    return _move(_gira(lamina(-tam, 0.0, tam, 0.0, tam * 0.42, 1.0, 0.0, 12), ang), cx, cy)


def lamina_protetica(T, t, rng):
    """Lâmina protética: a Dança da Ave Aquática — uma rajada de cortes em meia-lua girando em
    volta do alvo, um atrás do outro, e pétalas escarlates se soltando e caindo girando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    sub = np.random.default_rng(29)
    cortes = T.zero()
    for j in range(13):
        t0 = 0.02 + j * 0.045
        rot = j * 2.35 + sub.uniform(-0.3, 0.3)
        raio = sub.uniform(0.45, 0.68)
        span = sub.uniform(1.9, 2.5)
        sq = sub.uniform(0.45, 0.7)
        ox, oy = sub.uniform(-0.08, 0.08), sub.uniform(-0.08, 0.08)
        p = ease_out(rel(t, t0, t0 + 0.07), 2.2)
        vida = 1 - rel(t, t0 + 0.06, t0 + 0.2)
        if p <= 0 or vida <= 0:
            continue
        cortes += T.arc_band(raio, 0.07, -span / 2, -span / 2 + span * p + 0.01, squash=sq, rot=rot, cx=ox, cy=oy, crescente=True) * vida
    giro = T.ring(0.6, 0.05, squash=1.7) * pulso(t, 0.0, 0.72) * 0.35
    # pétalas: saem do centro em espiral, giram e caem
    pet = []
    tt = rel(t, 0.1, 1.0)
    for j in range(16):
        a = j / 16 * TAU + sub.uniform(-0.2, 0.2)
        nasce = sub.uniform(0.0, 0.35)
        dist = sub.uniform(0.25, 1)
        u = rel(tt, nasce, 1.0)
        if u <= 0:
            continue
        d = 0.12 + 0.62 * ease_out(u, 2) * dist
        x = d * math.cos(a + u * 1.2)
        y = d * math.sin(a + u * 1.2) * 0.8 + 0.35 * u * u
        pet.append((_petala(x, y, 0.08, a + u * 9 + j), (1 - u) ** 0.8))
    Pt = T.polys(pet, 0.004)
    k = pulso(t, 0.55, 0.85)
    g, h = _clarao(T, k * 0.8, 0.0, 0.0, 0.2, 0.6, 0.6)
    G += (T.glow(cortes, 1.2, 1.1, 0.02) + giro + Pt * 1.4 + T.blur(Pt, 0.02) * 0.5 + g) * env
    H += (cortes * 0.8 + Pt * 0.35 + h) * env
    return G, H


# ================================================================== Arthas
_RUNAS = [
    [[(0, -1), (0, 1)], [(0, -0.3), (0.6, -0.9)], [(0, 0.2), (0.6, -0.4)]],
    [[(0, -1), (0, 1)], [(0, -0.2), (-0.6, -0.9)], [(0, -0.2), (0.6, -0.9)]],
    [[(0, -1), (0.5, -0.4), (0, 0.2), (-0.5, -0.4), (0, -1)], [(-0.45, 0.9), (0.25, 0.0)], [(0.45, 0.9), (-0.25, 0.0)]],
    [[(0, -1), (0, 1)], [(-0.55, -0.45), (0, -1), (0.55, -0.45)]],
    [[(0, -1), (0, 1)], [(0, -1), (0.5, -0.6), (0, -0.2), (0.5, 1)]],
    [[(-0.4, -1), (-0.4, 1)], [(0.4, -1), (0.4, 1)], [(-0.4, -0.6), (0.4, 0.2)]],
]


def frostmourne(T, t, rng):
    """Frostmourne: o corte largo da espada rúnica deixa runas acesas no rastro, a névoa de gelo
    se espalha pelo arco e cristais de gelo brotam do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    a0, a1 = -2.6, 0.55
    p = ease_out(rel(t, 0.0, 0.26), 2.2)
    cab = a0 + (a1 - a0) * p + 0.01
    vivo = 1 - rel(t, 0.32, 0.62)
    arco = T.arc_band(0.66, 0.17, a0, cab, squash=0.8, rot=0.15, crescente=True) * vivo
    fio = T.arc_band(0.74, 0.025, a0, cab, squash=0.8, rot=0.15) * vivo
    # névoa: o arco borrado e esgarçado pelo ruído, crescendo e subindo
    n = T.noise(np.random.default_rng(141), 0.06, 3)
    larga = T.arc_band(0.6, 0.32, a0, cab, squash=0.8, rot=0.15)
    nev = T.blur(T.warp(larga, n * 0.05, n * 0.05 - 0.08 * rel(t, 0.15, 1)), 0.03) * np.clip(0.7 + 0.3 * n, 0.25, 1)
    nev *= janela(t, 0.05, 0.25) * apaga(t, 0.5, 1) * 0.75
    # runas acesas ao longo do arco, que aparecem depois da lâmina e se apagam
    run = T.zero()
    ca, sa = math.cos(0.15), math.sin(0.15)
    for j in range(5):
        u = 0.15 + 0.7 * j / 4
        if p < u:
            continue
        a = a0 + (a1 - a0) * u
        ux, uy = 0.5 * math.cos(a), 0.5 * math.sin(a) * 0.8
        x, y = ux * ca - uy * sa, ux * sa + uy * ca
        kk = janela(t, 0.08 + 0.05 * j, 0.14 + 0.05 * j) * apaga(t, 0.55 + 0.04 * j, 0.85)
        for traco in _RUNAS[j % len(_RUNAS)]:
            run += T.polyline([(x + px * 0.06, y + py * 0.075 - 0.05 * rel(t, 0.3, 1)) for px, py in traco], 0.016) * kk
    # cristais de gelo brotando do alvo
    cri = []
    sub = np.random.default_rng(43)
    cresce = back(rel(t, 0.22, 0.42), 1.4)
    facetas = []
    for j in range(9):
        a = -math.pi / 2 + (j - 4) * 0.36 + sub.uniform(-0.12, 0.12)
        L = (0.14 + 0.36 * sub.uniform() * (1 - abs(j - 4) / 6)) * cresce
        w = 0.03 + 0.015 * sub.uniform()
        bx, by = 0.05 + 0.06 * math.cos(a), 0.22 + 0.04 * math.sin(a)
        tx, ty = bx + L * math.cos(a), by + L * math.sin(a)
        nx, ny = -math.sin(a) * w, math.cos(a) * w
        cri.append(([(bx + nx, by + ny), (bx + (tx - bx) * 0.75 + nx, by + (ty - by) * 0.75 + ny), (tx, ty),
                     (bx + (tx - bx) * 0.75 - nx, by + (ty - by) * 0.75 - ny), (bx - nx, by - ny)], 1.0))
        facetas.append((bx, by, tx, ty, 1.0))
    Cr = T.polys(cri, 0.004) * float(cresce > 0.01) * apaga(t, 0.7, 0.95)
    Cr_borda = contorno(T.blur(Cr, 0.006), 0.2, 0.35, 0.6, 0.85) * apaga(t, 0.7, 0.95)
    Cr_borda += T.lines(facetas, 0.008, 0.002) * float(cresce > 0.01) * apaga(t, 0.7, 0.95) * 0.8
    k = pulso(t, 0.14, 0.45)
    g, h = _clarao(T, k, 0.0, 0.05, 0.22, 0.7, 0.785)
    G += (T.glow(arco, 1.1, 1.1, 0.025) + fio * 1.4 + nev + T.glow(run, 1.4, 1.4, 0.02) + Cr * 0.9 + Cr_borda * 0.8 + g) * env
    H += (fio * 1.4 + arco * 0.35 + run * 1.2 + Cr_borda * 0.9 + Cr * 0.2 + h + nev * 0.15) * env
    return G, H


# ================================================================== Isaac
def cortador_de_plasma(T, t, rng):
    """Cortador de plasma: três feixes de mira acendem e marcam três pontos alinhados no alvo;
    o tiro sai como uma lâmina de plasma em pé que voa na horizontal, corta e deixa a marca
    incandescente pingando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ys = (-0.3, 0.0, 0.3)
    mira = janela(t, 0.0, 0.08) * (1 - rel(t, 0.38, 0.44))
    fe, pt = T.zero(), T.zero()
    for y in ys:
        fe += T.lines([(-1.05, y * 0.12, 0.0, y, 1.0)], 0.007, 0.002)
        pt += T.gauss(0.0, y, 0.022) * 2.2 + T.flare(0.0, y, 0.22, 0.0, 0.03) * 0.7
    fe *= mira * 0.8
    pt *= mira * (0.8 + 0.2 * math.sin(t * 60))
    # o disparo: lâmina vertical de plasma com três nós quentes
    p = ease_in(rel(t, 0.32, 0.44), 1.3)
    voo = float(t > 0.32) * (1 - rel(t, 0.43, 0.46))
    bx = -0.95 + 0.95 * p
    lam = T.polys([(lamina(bx, -0.45, bx, 0.45, 0.075, 1.0), 1.0)], 0.006) * voo
    nos = sum(T.gauss(bx, y, 0.045) for y in ys) * 2.2 * voo
    cauda = T.tapered([(bx - 0.5, y * 0.9, bx, y, 1.0) for y in ys], 0.05) * voo * 0.7
    cauda += T.blur(T.polys([([(bx - 0.4, -0.3), (bx, -0.42), (bx, 0.42), (bx - 0.4, 0.3)], 1.0)], 0.0), 0.03) * voo * 0.3
    # o corte: marca vertical incandescente, faíscas para os dois lados e pingos derretidos
    k = pulso(t, 0.43, 0.7)
    corte = T.polys([(lamina(0.0, -0.45, 0.0, 0.45, 0.04, 1.0), 1.0)], 0.004) * float(t > 0.43) * apaga(t, 0.55, 0.92)
    g = T.gauss(0.0, 0.0, 0.12, 0.45) * k * 1.4
    h = T.flare(0.0, 0.0, 1.2 * k + 0.01, 0.0, 0.01) * k * 1.2
    fa = faiscas(T, np.random.default_rng(61), t, 18, 0.65, 0.03, cone=(-0.9, 0.9), gravidade=0.35, inicio=0.43)
    fa += faiscas(T, np.random.default_rng(62), t, 12, 0.5, 0.03, cone=(math.pi - 0.9, math.pi + 0.9), gravidade=0.35, inicio=0.43)
    sub = np.random.default_rng(63)
    pingos = []
    for j in range(7):
        y0 = sub.uniform(-0.35, 0.35)
        t0 = 0.48 + sub.uniform(0, 0.2)
        dx = sub.uniform(-0.02, 0.02)
        u = rel(t, t0, t0 + 0.4)
        if u > 0:
            pingos.append((dx, y0 + 0.5 * u * u, (1 - u) * 0.8))
    Pg = T.splats(pingos, 0.016)
    G += (fe + pt * 1.2 + lam * 1.4 + T.blur(lam, 0.03) * 0.8 + nos + cauda + T.glow(corte, 1.1, 1.0, 0.025) + g + T.glow(fa, 1, 1.1, 0.02) + Pg * 1.4) * env
    H += (fe * 0.6 + pt + lam * 0.8 + nos * 0.8 + corte * 0.9 + h + fa * 0.7 + Pg * 0.8) * env
    return G, H


# ================================================================== Gordon
def _caixa(cx, cy, s, ang):
    return _move(_gira([(-s, -s), (s, -s), (s, s), (-s, s)], ang), cx, cy)


def arma_da_gravidade(T, t, rng):
    """Arma da gravidade: o feixe laranja de fios trançados pega uma caixa e a puxa no ar
    girando; o disparo dá um tranco (onda de choque) e lança a caixa no alvo, que se despedaça."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gx, gy = -1.05, 0.08
    # caminho da caixa: sobe do chão até a frente da arma, depois é lançada no alvo
    puxa = ease_out(rel(t, 0.0, 0.3), 2)
    lanca = ease_in(rel(t, 0.4, 0.5), 1.3)
    cx = -0.15 - 0.4 * puxa + 0.55 * lanca + 0.01 * math.sin(t * 70) * pulso(t, 0.28, 0.4)
    cy = 0.45 - 0.45 * puxa
    giro = 0.6 * t + 2.5 * lanca
    viva = float(t < 0.5)
    cantos = _caixa(cx, cy, 0.15, giro)
    caixa = T.polys([(cantos, 1.0)], 0.004) * viva
    tabuas = T.polyline(cantos + [cantos[0]], 0.016) * viva
    xis = T.lines([(*cantos[0], *cantos[2], 1.0), (*cantos[1], *cantos[3], 0.6)], 0.012) * viva
    # o feixe: três fios trançando da arma até a caixa
    feixe = janela(t, 0.0, 0.05) * (1 - rel(t, 0.42, 0.5))
    F = T.zero()
    if feixe > 0:
        for j in range(3):
            pts = []
            for k in range(36):
                u = k / 35
                x = gx + (cx - gx) * u
                y = gy + (cy - gy) * u + 0.085 * math.sin(u * 10 + t * 40 + j * TAU / 3) * math.sin(math.pi * u) ** 0.6
                pts.append((x, y))
            F += T.polyline(pts, 0.012)
        F += T.polys([(lamina(gx, gy, cx, cy, 0.05, 1.0), 1.0)], 0.03) * 0.5
        F *= feixe
    # anéis que correm pelo feixe (para a arma ao puxar)
    an = T.zero()
    for j in range(3):
        u = 1 - ((t * 4 + j / 3) % 1)
        an += T.ring(0.05, 0.012, gx + (cx - gx) * u, gy + (cy - gy) * u, squash=0.45) * math.sin(math.pi * u)
    an *= feixe * (1 - janela(t, 0.32, 0.38))
    # o tranco do disparo
    k = pulso(t, 0.36, 0.56)
    choque = T.ring(0.05 + 0.3 * ease_out(rel(t, 0.36, 0.56), 2), 0.03, -0.55, 0.0, squash=0.6) * k * 1.4
    boca = T.gauss(-0.6, 0.0, 0.1) * pulso(t, 0.34, 0.46) * 1.8
    vel = rastro_de_velocidade(T, rng, 7, 0.0, 0.5, 0.14, -0.12, cx=cx + 0.12, cy=cy, largura=0.015) * pulso(t, 0.4, 0.56)
    # o choque no alvo: clarão e a caixa em pedaços
    k2 = pulso(t, 0.49, 0.8)
    g, h = _clarao(T, k2, 0.05, 0.0, 0.26, 0.8)
    est = _estouro(T, k2, 0.05, 0.0, 0.3, 0.4, 7)
    sub = np.random.default_rng(91)
    tt = rel(t, 0.5, 1.0)
    pedacos = []
    for j in range(9):
        a = sub.uniform(-math.pi * 0.95, math.pi * 0.35)
        dist = sub.uniform(0.5, 1)
        a0 = sub.uniform(0, 3)
        gv = sub.uniform(-1, 1)
        L = sub.uniform(0.07, 0.11)
        if tt <= 0:
            continue
        d = 0.1 + 0.6 * ease_out(tt, 2) * dist
        x, y = 0.08 + d * math.cos(a), d * math.sin(a) + 0.5 * tt * tt
        pedacos.append((_move(_gira([(-L, -0.025), (L, -0.025), (L, 0.025), (-L, 0.025)], a0 + tt * 8 * gv), x, y), 1 - tt))
    Pd = T.polys(pedacos, 0.004)
    po = poeira(T, np.random.default_rng(92), t, 10, 0.08, 0.0, 0.5, 0.15, 0.05, 0.5) * 0.5 if t > 0.5 else T.zero()
    G += (caixa * 0.7 + tabuas * 0.9 + xis * 0.6 + T.glow(F, 1.2, 1.2, 0.025) + an * 0.9 + choque + boca + vel + g + est + Pd * 1.2 + po) * env
    H += (tabuas * 0.5 + F * 0.8 + an * 0.4 + choque * 0.5 + boca + vel * 0.4 + h + est * 0.7 + Pd * 0.5) * env
    return G, H


# ================================================================== Pyramid Head
def _faca(ang, px, py, esc=1.0):
    """A Grande Faca: cabo curto e uma lâmina enorme e larga, com dentes de ferrugem no fio."""
    sub = np.random.default_rng(7)
    cabo = [(-0.16, -0.025), (0.06, -0.025), (0.06, 0.025), (-0.16, 0.025)]
    cima = [(0.06, -0.09)]
    for k in range(1, 12):
        u = k / 11
        cima.append((0.06 + 1.0 * u, -0.09 - 0.04 * u + sub.uniform(-0.012, 0.012)))
    ponta = [(1.15, -0.06), (1.12, 0.11)]
    baixo = []
    for k in range(11, -1, -1):
        u = k / 11
        baixo.append((0.06 + 1.0 * u, 0.12 + sub.uniform(-0.03, 0.0) * (k % 2)))
    lam = cima + ponta + baixo
    return [(_move(_gira(cabo, ang), px, py, esc), 0.8), (_move(_gira(lam, ang), px, py, esc), 1.0)]


def grande_faca(T, t, rng):
    """Grande Faca: a lâmina enorme e enferrujada vem arrastada no chão soltando faíscas,
    sobe e desce pesada sobre o alvo — estrondo, chão rachado, faíscas e poeira."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chao = 0.52
    ferrugem = np.clip(0.62 + 0.38 * T.noise(np.random.default_rng(5), 0.03, 3), 0.2, 1.0)
    if t < 0.38:
        d = ease_out(rel(t, 0.0, 0.36), 1.4)
        px, py, ang = -1.45 + 0.5 * d, chao - 0.11, 0.07
    elif t < 0.44:
        u = ease_out(rel(t, 0.38, 0.44), 2)
        px, py, ang = -0.95 + 0.1 * u, chao - 0.11 - 0.4 * u, 0.07 + (-1.45 - 0.07) * u
    else:
        u = ease_in(rel(t, 0.44, 0.54), 2.2)
        px, py, ang = -0.85, chao - 0.51, -1.45 + (1.45 + 0.42) * u
    vis = 1 - rel(t, 0.72, 0.92)
    lam = T.polys(_faca(ang, px, py, 1.0), 0.004) * vis
    tx = px + 1.13 * math.cos(ang)
    # o arrasto: risco no chão e faíscas para trás da ponta
    arr = janela(t, 0.0, 0.06) * (1 - rel(t, 0.34, 0.42))
    risco = T.lines([(tx - 0.6, chao, tx, chao, 1.0)], 0.012, 0.004) * arr
    fa = faiscas(T, np.random.default_rng(int(round(t * 11)) + 40), 0.45, 22, 0.6, 0.035, cone=(-math.pi + 0.25, -math.pi + 1.0), gravidade=0.4, cx=tx, cy=chao) * arr
    # o arco do golpe pesado
    sw = T.arc_band(0.9, 0.2, -1.45, ang + 0.01, cx=-0.85, cy=chao - 0.51, crescente=True) * pulso(t, 0.44, 0.62) if t > 0.45 else T.zero()
    # o estrondo
    k = pulso(t, 0.52, 0.85)
    ix, iy = 0.05, chao - 0.05
    g, h = _clarao(T, k, ix, iy, 0.3, 1.0, 0.0)
    onda = T.ring(0.1 + 0.75 * ease_out(rel(t, 0.53, 0.85), 2), 0.04, ix, chao, squash=3.0) * pulso(t, 0.53, 0.9) * 1.3
    sub = np.random.default_rng(23)
    rach = T.zero()
    if t > 0.53:
        for j in range(6):
            pts = jagged(sub, ix, chao, ix + sub.uniform(-0.9, 0.9), chao + sub.uniform(-0.02, 0.06), 4, 0.25)
            rach += T.polyline([(x, chao + (y - chao) * 0.3) for x, y in pts], 0.013)
        rach *= janela(t, 0.53, 0.6) * apaga(t, 0.75, 1)
    fa2 = faiscas(T, np.random.default_rng(24), t, 24, 0.85, 0.035, cone=(-math.pi + 0.15, -0.15), gravidade=0.6, cx=ix, cy=iy, inicio=0.53)
    po = poeira(T, np.random.default_rng(25), t, 16, ix, chao, 0.7, 0.2, 0.06, 0.53) * 0.6 if t > 0.53 else T.zero()
    G += (lam * ferrugem * 1.2 + T.glow(risco, 1, 1.2, 0.02) + T.glow(fa, 1, 1.2, 0.02) + sw * 0.6 + g + onda + rach * 1.2 + T.glow(fa2, 1, 1.2, 0.02) + po) * env
    H += (contorno(T.blur(lam, 0.006), 0.3, 0.5, 0.75, 0.95) * 0.5 + risco * 0.8 + fa * 0.8 + sw * 0.2 + h + onda * 0.4 + rach * 0.6 + fa2 * 0.8) * env
    return G, H


# ================================================================== Prince of Persia
def _adaga(ang, px, py, esc=1.0):
    lam = lamina(0.0, 0.0, 0.42, 0.0, 0.05, 1.0, 0.0, 14)
    guarda = [(-0.01, -0.09), (0.02, -0.09), (0.02, 0.09), (-0.01, 0.09)]
    cabo = [(-0.16, -0.022), (0.0, -0.022), (0.0, 0.022), (-0.16, 0.022)]
    return [(_move(_gira(f, ang), px, py, esc), w) for f, w in ((lam, 1.0), (guarda, 0.9), (cabo, 0.8))]


def adaga_do_tempo(T, t, rng):
    """Adaga do tempo: o corte rápido da adaga e, em seguida, o tempo volta — a areia gira em
    espiral ao contrário, o rastro do corte se desfaz de trás para a frente e um mostrador
    gira para trás em volta do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    a0, a1 = -2.5, 0.45
    p = ease_out(rel(t, 0.0, 0.2), 2.2)
    # o rastro do corte: aparece com a adaga e depois "rebobina" (encolhe da cabeça para a cauda)
    volta = ease_in(rel(t, 0.32, 0.75), 1.5)
    cab = a0 + (a1 - a0) * p * (1 - volta)
    arco = T.arc_band(0.58, 0.12, a0, cab + 0.01, squash=0.8, crescente=True) * float(cab - a0 > 0.05) * (1 - rel(t, 0.7, 0.8))
    ax, ay = 0.58 * math.cos(cab) * 0.95, 0.58 * math.sin(cab) * 0.8 * 0.95
    adaga = T.polys(_adaga(math.atan2(math.cos(cab) * 0.8, -math.sin(cab)), ax - 0.08 * math.cos(cab), ay - 0.08 * math.sin(cab), 0.9), 0.004) * (1 - rel(t, 0.78, 0.9))
    # areia em espiral girando ao contrário (anti-horário), em três braços que se fecham no centro
    sub = np.random.default_rng(37)
    graos = []
    fios = T.zero()
    gira = janela(t, 0.18, 0.3) * apaga(t, 0.72, 0.95)
    if gira > 0:
        for braco in range(3):
            pts = []
            for k in range(30):
                u = k / 29
                r = 0.82 * (1 - u) ** 0.9 + 0.05
                a = braco * TAU / 3 - u * 4.2 - t * 9
                pts.append((r * math.cos(a), r * math.sin(a) * 0.85))
            fios += T.polyline(pts, 0.012)
        for j in range(60):
            fase = sub.uniform(0, 1)
            u = (fase + t * 1.6) % 1
            braco = j % 3
            r = 0.85 * (1 - u) ** 0.9 + 0.04
            a = braco * TAU / 3 - u * 4.2 - t * 9 + sub.uniform(-0.25, 0.25)
            graos.append((r * math.cos(a), r * math.sin(a) * 0.85, sub.uniform(0.4, 1) * math.sin(math.pi * u) ** 0.5))
    Gr = T.splats(graos, 0.012) * gira
    fios *= gira * 0.5
    # o mostrador: anel com 12 marcas e um ponteiro girando para trás
    mostra = pulso(t, 0.22, 0.95)
    dial = T.ring(0.9, 0.012, squash=1.0 / 0.85) * mostra * 0.6
    marcas = []
    for k in range(12):
        a = k / 12 * TAU
        marcas.append((0.82 * math.cos(a), 0.82 * math.sin(a) * 0.85, 0.94 * math.cos(a), 0.94 * math.sin(a) * 0.85, 1.0))
    Mc = T.lines(marcas, 0.016, 0.003) * mostra * 0.8
    pa = -math.pi / 2 - t * 9
    pont = T.polys([(lamina(0.0, 0.0, 0.62 * math.cos(pa), 0.62 * math.sin(pa) * 0.85, 0.03, 1.0), 1.0)], 0.004) * mostra * 0.8
    k = pulso(t, 0.12, 0.4)
    g, h = _clarao(T, k, 0.0, 0.0, 0.2, 0.6, 0.5)
    brilho_fim = T.gauss(0, 0, 0.1) * pulso(t, 0.62, 0.92) * 1.8
    G += (T.glow(arco, 1.2, 1.1, 0.025) + adaga * 1.3 + Gr * 1.5 + fios + dial + Mc + pont + g + brilho_fim) * env
    H += (arco * 0.6 + adaga * 0.8 + Gr * 0.8 + Mc * 0.4 + pont * 0.4 + h + brilho_fim) * env
    return G, H


# ================================================================== Alucard
def _morcego(cx, cy, esc, bate, ang=0.0):
    """Silhueta de morcego (asas abertas, recorte em arcos embaixo); `bate` −1..1 mexe as asas."""
    meia = [(0.0, -0.03), (0.012, -0.055), (0.02, -0.022)]
    ponta = (0.135, -0.01 - 0.075 * bate)
    meia += [(0.026, -0.012), (0.075, -0.04 - 0.045 * bate), ponta]
    base = (0.02, 0.035)
    for k in range(1, 13):
        u = k / 12
        x = ponta[0] + (base[0] - ponta[0]) * u
        y = ponta[1] + (base[1] - ponta[1]) * u + 0.021 * (1 - abs(2 * u - 1))
        y -= 0.022 * abs(math.sin(3 * math.pi * u))
        meia.append((x, y))
    meia.append((0.0, 0.05))
    corpo = meia + [(-x, y) for x, y in meia[::-1]]
    return _move(_gira(corpo, ang), cx, cy, esc)


def espada_de_alucard(T, t, rng):
    """Espada de Alucard: um corte longo e elegante, fino como fio de navalha, e do rastro saem
    morcegos batendo as asas, que se espalham para cima e somem."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    a0, a1 = -2.85, 0.15
    p = ease_out(rel(t, 0.0, 0.2), 2.6)
    vivo = 1 - rel(t, 0.3, 0.6)
    arco = T.arc_band(0.78, 0.09, a0, a0 + (a1 - a0) * p + 0.01, squash=0.5, rot=0.2, cy=0.3, crescente=True) * vivo
    fio = T.arc_band(0.8, 0.014, a0, a0 + (a1 - a0) * p + 0.01, squash=0.5, rot=0.2, cy=0.3) * vivo
    k = pulso(t, 0.1, 0.36)
    g = T.gauss(0.0, -0.08, 0.45, 0.06) * k * 1.2
    h = T.flare(0.25, -0.05, 1.1 * k + 0.01, 0.2, 0.01) * k * 1.5
    # morcegos saindo do rastro
    sub = np.random.default_rng(66)
    ca, sa = math.cos(0.2), math.sin(0.2)
    bats = []
    for j in range(8):
        u = 0.12 + 0.8 * j / 7
        a = a0 + (a1 - a0) * u
        ux, uy = 0.78 * math.cos(a), 0.78 * math.sin(a) * 0.5
        x0, y0 = ux * ca - uy * sa, ux * sa + uy * ca + 0.3
        t0 = 0.12 + 0.03 * j + sub.uniform(0, 0.05)
        dirx, diry = sub.uniform(-1.0, 1.0), -sub.uniform(0.3, 1.1)
        tam = sub.uniform(0.95, 1.25)
        incl = sub.uniform(-0.25, 0.25)
        v = rel(t, t0, t0 + 0.6)
        if v <= 0:
            continue
        x = x0 + dirx * 0.6 * ease_out(v, 1.5)
        y = y0 + diry * 0.75 * ease_out(v, 1.5)
        bate = math.sin(t * 70 + j * 1.7)
        esc = (0.7 + 1.2 * ease_out(rel(v, 0, 0.25), 2)) * tam
        bats.append((_morcego(x, y, esc, bate, incl + dirx * 0.3), (1 - v ** 1.6)))
    Bt = T.polys(bats, 0.004)
    G += (T.glow(arco, 1.1, 1.0, 0.02) + fio * 1.5 + g + Bt * 1.4 + T.blur(Bt, 0.025) * 0.5) * env
    H += (fio * 1.6 + arco * 0.4 + h + Bt * 0.15) * env
    return G, H


REGISTRO = [
    ("chute_relampago", chute_relampago, GRANDE, "Chun-Li: leque de chutes rápidos em borrão", False),
    ("kunai_do_inferno", kunai_do_inferno, GRANDE, "Scorpion: kunai na corda crava, queima e puxa", False),
    ("chute_do_dragao", chute_do_dragao, GRANDE, "Liu Kang: chute voador com dragão de fogo", False),
    ("soco_do_diabo", soco_do_diabo, GRANDE, "Kazuya: soco com raios do Gene do Diabo", False),
    ("keyblade", keyblade, GRANDE, "Sora: golpe de chave-espada com estrelinhas", False),
    ("aparar_e_cortar", aparar_e_cortar, GRANDE, "Sekiro: faísca de aparar e contra-corte", False),
    ("lamina_protetica", lamina_protetica, GRANDE, "Malenia: rajada de cortes e pétalas escarlates", False),
    ("frostmourne", frostmourne, GRANDE, "Arthas: corte rúnico gelado com runas e cristais", False),
    ("cortador_de_plasma", cortador_de_plasma, GRANDE, "Isaac: mira de três pontos e lâmina de plasma", False),
    ("arma_da_gravidade", arma_da_gravidade, GRANDE, "Gordon: feixe puxa a caixa e a lança no alvo", False),
    ("grande_faca", grande_faca, GRANDE, "Pyramid Head: faca arrastada e golpe pesado", False),
    ("adaga_do_tempo", adaga_do_tempo, GRANDE, "Príncipe: corte da adaga e areia do tempo voltando", False),
    ("espada_de_alucard", espada_de_alucard, GRANDE, "Alucard: corte elegante que vira morcegos", False),
]
