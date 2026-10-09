"""Ataques básicos com animação própria, lote a.

Goku, Vegeta, Gohan, Piccolo, Broly, Beerus, Yusuke, Saitama, Gojo, Yuji,
Sukuna, Pikachu e Flash: cada folha conta o golpe normal do personagem (a
rajada de ki, o braço que estica, o peteleco do Hakai, o Rei Gun, o soco
casual com o vendaval atrasado, o Infinito que para o punho, o Black Flash,
o Desmanche, o choque e os mil socos do Flash).
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


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


# punho fechado visto de lado, apontando para +x (nós dos dedos na frente)
_PUNHO = [(-0.13, -0.07), (-0.02, -0.1), (0.07, -0.1), (0.11, -0.07), (0.13, -0.02), (0.13, 0.03),
          (0.11, 0.07), (0.05, 0.1), (-0.04, 0.1), (-0.13, 0.08)]


def _punho(T, cx, cy, esc=1.0, ang=0.0):
    """Punho cheio + o risco dos nós dos dedos (no H)."""
    P = T.polys([(_move(_gira(_PUNHO, ang), cx, cy, esc), 1.0)], 0.006)
    dedos = [_move(_gira([(0.06, -0.09 + 0.06 * k), (0.12, -0.075 + 0.06 * k)], ang), cx, cy, esc) for k in range(3)]
    nos = sum(T.polyline(d, 0.012 * esc) for d in dedos)
    return P, nos


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.5
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.65 * k + 0.01, ang=ang + math.pi / 4, thin=0.012)) * k * 1.6
    return g, h


def _nuvem(T, seed, cx, cy, tam, cresce, n=7, sobe=0.0, alonga=1.0):
    """Baforada de fumaça: bolotas agrupadas que incham (silhueta cheia de nuvem)."""
    sub = np.random.default_rng(seed)
    campo = T.zero()
    for _ in range(n):
        a = sub.uniform(0, TAU)
        d = sub.uniform(0.3, 1.0) * tam * (0.6 + 0.8 * cresce)
        s = sub.uniform(0.45, 0.75) * tam * (0.55 + 0.7 * cresce)
        campo += T.gauss(cx + math.cos(a) * d * alonga, cy + math.sin(a) * d * 0.8 - sobe * cresce, s * (1 + 0.5 * (alonga - 1)), s)
    return campo


def _zigue(x1, y1, x2, y2, n, amp, fase=1.0):
    """Zigue-zague de desenho animado (raio do Pikachu): pontas alternadas, ângulos duros."""
    dx, dy = x2 - x1, y2 - y1
    comp = math.hypot(dx, dy) or 1
    nx, ny = -dy / comp, dx / comp
    pts = [(x1, y1)]
    for k in range(1, n):
        u = k / n
        s = amp * (1 if k % 2 else -1) * fase
        pts.append((x1 + dx * u + nx * s, y1 + dy * u + ny * s))
    pts.append((x2, y2))
    return pts


def _aura_espinhos(T, t, R, seed, n=16, puxa_cima=0.6, ponta=0.55, vel=30.0):
    """Aura de Super Saiyajin: chama em espinhos que tremem, altos em cima e curtos embaixo."""
    sub = np.random.default_rng(seed)
    pts = []
    for k in range(2 * n):
        a = -math.pi / 2 + math.pi * k / n
        cima = (1 - math.sin(a)) / 2
        if k % 2 == 0:
            r = R * (1 + ponta * (0.25 + 0.75 * cima ** 1.5) * (0.7 + 0.3 * sub.uniform()) * (1 + puxa_cima * cima)) * (1 + 0.14 * math.sin(t * vel + k * 1.9))
        else:
            r = R * (0.95 + 0.08 * sub.uniform())
        pts.append((math.cos(a) * r * 0.85, math.sin(a) * r - 0.25 * R * cima))
    return pts


# ------------------------------------------------------------------ Goku
def ki_dourado(T, t, rng):
    """Rajada de ki (Goku): três esferinhas douradas chegam em sequência da esquerda e
    estouram no alvo, cada uma soltando uma baforada de fumaça branca."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    alvos = [(-0.12, -0.16), (0.12, 0.13), (0.0, 0.0)]
    saidas = [-0.32, 0.3, 0.02]
    for k, (tx, ty) in enumerate(alvos):
        a0 = 0.0 + 0.13 * k
        chega = a0 + 0.15
        oy = saidas[k]
        if a0 <= t < chega:
            u = ease_in(rel(t, a0, chega), 1.15)
            x, y = -1.08 + (tx + 1.08) * u, oy + (ty - oy) * u
            ux, uy = tx + 1.08, ty - oy
            c = math.hypot(ux, uy)
            cauda = T.tapered([(x - ux / c * 0.5, y - uy / c * 0.5, x, y, 1.0)], 0.15)
            G += T.gauss(x, y, 0.08) * 2.2 + T.gauss(x, y, 0.16) * 0.7 + T.blur(cauda, 0.015) * 1.2
            H += T.gauss(x, y, 0.048) * 2.6 + T.blur(cauda, 0.008) * 0.5
        if t >= chega - 0.01:
            e = rel(t, chega, chega + 0.2)
            k1 = pulso(t, chega - 0.01, chega + 0.14)
            g, h = _clarao(T, k1, tx, ty, 0.15, 0.55)
            anel = T.ring(0.06 + 0.32 * ease_out(e, 2), 0.028 * (1 - e) + 0.006, tx, ty) * (1 - e) ** 1.2 * 1.3
            est = T.polys([(estrela(tx, ty, 0.22 * k1 + 0.01, 0.3 + k, 7, 0.42), 1.0)], 0.005) * k1
            cresce = ease_out(rel(t, chega, 0.95), 2.2)
            vida = janela(t, chega, chega + 0.06) * apaga(t, chega + 0.25, 1.0, 1.2)
            nuvem = _nuvem(T, 70 + k, tx, ty, 0.11 + 0.03 * (k == 2), cresce, 8, 0.14)
            fum = (forma(nuvem, 0.45, 0.85) * 0.75 + nuvem * 0.25) * vida
            G += g + anel + est * 1.3 + fum * 0.75
            H += h + anel * 0.6 + est * 0.9 + fum * 0.8
    return G * env, H * env


# ------------------------------------------------------------------ Vegeta
def rajada_continua(T, t, rng):
    """Rajada contínua (Vegeta): dezenas de esferas de ki pequenas martelam o alvo em pontos
    diferentes; cada estouro deixa fumaça e tudo vira uma nuvem grande no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(404)
    orbes, cabecas, estouros, clareia = [], [], [], []
    nuvem = T.zero()
    for k in range(26):
        a0 = 0.0 + 0.021 * k
        voo = 0.08
        a = sub.uniform(0, TAU)
        r = 0.42 * math.sqrt(sub.uniform(0.05, 1))
        tx, ty = math.cos(a) * r * 0.9, math.sin(a) * r
        oy = ty * 0.4 + sub.uniform(-0.3, 0.3)
        if a0 <= t < a0 + voo:
            u = rel(t, a0, a0 + voo)
            x, y = -1.1 + (tx + 1.1) * u, oy + (ty - oy) * u
            orbes.append((x - 0.26, y - (ty - oy) * 0.12, x, y, 1.0))
            cabecas.append((x, y, 1.0))
        hit = a0 + voo
        if t >= hit:
            k1 = pulso(t, hit - 0.01, hit + 0.12)
            estouros.append((estrela(tx, ty, 0.11 * k1 + 0.005, a, 6, 0.45), k1))
            clareia.append((tx, ty, k1))
            cresce = rel(t, hit, 1.0)
            s = 0.05 + 0.08 * ease_out(cresce, 1.8)
            nuvem += T.gauss(tx + 0.05 * cresce, ty - 0.12 * cresce, s, s * 0.9) * janela(t, hit, hit + 0.05)
    O = T.tapered(orbes, 0.07) if orbes else T.zero()
    C = T.splats(cabecas, 0.035)
    E = T.polys(estouros, 0.006) if estouros else T.zero()
    L = T.splats(clareia, 0.08)
    ronda = T.noise(np.random.default_rng(12), 0.12)
    corpo = forma(nuvem * (1 + 0.18 * ronda), 0.55, 1.1)
    fum = (corpo * 0.8 + nuvem * 0.15) * janela(t, 0.25, 0.6)
    final = pulso(t, 0.6, 0.86)
    g, h = _clarao(T, final, 0, 0, 0.32, 0.8)
    G += (T.blur(O, 0.01) * 1.4 + C * 1.6 + E * 1.3 + L * 0.9 + fum * 0.7 + g * 0.7) * env
    H += (T.blur(O, 0.006) * 0.6 + C * 2.0 + E * 0.9 + L * 0.7 + fum * 0.35 + h * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Gohan
def golpe_do_potencial(T, t, rng):
    """Golpe do potencial (Gohan SSJ2): o soco acerta com um clarão de aura branca em espinhos
    e raios elétricos finos estalando em volta, como no Super Saiyajin 2."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    hit = 0.17
    # o punho chega com linhas de velocidade
    vem = ease_in(rel(t, 0.0, hit), 1.4)
    px = -1.05 + 0.95 * vem
    vis = 1 - rel(t, hit + 0.04, hit + 0.16)
    P, nos = _punho(T, px, 0.0, 1.9)
    linhas = rastro_de_velocidade(T, rng, 9, 0.0, 0.7, 0.2, -px - 0.2, cx=0.0, seed=21) * janela(t, 0.0, 0.05) * (1 - rel(t, hit, hit + 0.12))
    G += (P * 1.2 + linhas * 0.7) * vis
    H += (P * 0.5 + nos * 0.9 + linhas * 0.4) * vis
    # aura branca que explode
    k = pulso(t, hit - 0.01, hit + 0.22)
    cresce = ease_out(rel(t, hit, hit + 0.18), 2)
    acesa = janela(t, hit, hit + 0.04) * apaga(t, 0.55, 0.9)
    R = 0.18 + 0.2 * cresce
    aura = T.polys([(_aura_espinhos(T, t, R, 77, 13, 1.0, 1.1), 1.0)], 0.012)
    miolo = T.polys([(_aura_espinhos(T, t + 0.3, R * 0.7, 78, 10, 0.9, 0.9), 1.0)], 0.02)
    borda = contorno(T.blur(aura, 0.01), 0.25, 0.45, 0.55, 0.85)
    G += (aura * 0.4 + borda * 1.2 + T.blur(aura, 0.05) * 0.5 + miolo * 0.35) * acesa
    H += (borda * 0.9 + miolo * 0.8 * k + aura * 0.9 * k + T.blur(miolo, 0.03) * 0.25) * acesa
    g, h = _clarao(T, k, 0, 0, 0.26, 0.85)
    anel = T.ring(0.1 + 0.62 * ease_out(rel(t, hit, hit + 0.3), 2), 0.03) * pulso(t, hit, hit + 0.32) * 1.2
    G += g + anel
    H += h * 1.2 + anel * 0.6
    # raios finos (mudam a cada quadro, como o SSJ2 crepitando)
    q = int(round(t * 11))
    sub = np.random.default_rng(900 + q)
    raios = T.zero()
    ligado = janela(t, hit, hit + 0.03) * apaga(t, 0.62, 0.92)
    if ligado > 0:
        for _ in range(4):
            a = sub.uniform(0, TAU)
            r1 = sub.uniform(0.15, 0.3)
            r2 = r1 + sub.uniform(0.3, 0.5)
            da = sub.uniform(-0.7, 0.7)
            pts = jagged(sub, math.cos(a) * r1, math.sin(a) * r1, math.cos(a + da) * r2, math.sin(a + da) * r2, 4, 0.35)
            raios += T.polyline(pts, 0.016)
            if sub.uniform() < 0.6:
                m = pts[len(pts) // 2]
                b = a + sub.uniform(-1.2, 1.2)
                raios += T.polyline(jagged(sub, m[0], m[1], m[0] + math.cos(b) * 0.2, m[1] + math.sin(b) * 0.2, 3, 0.4), 0.01)
    G += (raios * 1.2 + T.blur(raios, 0.02) * 1.0) * ligado
    H += raios * 1.3 * ligado
    return G * env, H * env


# ------------------------------------------------------------------ Piccolo
def braco_namekiano(T, t, rng):
    """Golpe namekiano (Piccolo): o braço verde estica da esquerda, segmentado, com o punho
    e a munhequeira, acerta o alvo e volta encolhendo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    hit = 0.26
    estica = ease_out(rel(t, 0.0, hit), 1.6)
    volta = ease_in(rel(t, 0.55, 0.85), 1.8)
    ox, oy = -1.12, 0.12
    ponta = ox + (-0.12 - ox) * estica * (1 - volta)
    # recuo elástico logo depois do contato
    ponta -= 0.06 * math.sin(math.pi * rel(t, hit, hit + 0.14)) * (t > hit)
    vis = 1 - rel(t, 0.78, 0.88)
    if ponta > ox + 0.02 and vis > 0:
        comp = ponta - ox
        ondula = 0.035 * (1 - janela(t, hit, hit + 0.1)) + 0.012

        def y_de(x):
            u = (x - ox) / comp
            return oy - 0.1 * u + ondula * math.sin(u * 3 * math.pi + t * 30)
        # segmentos (o braço de namekiano com as dobras)
        segs = []
        passo = 0.15
        x = ponta - 0.22
        while x > ox - 0.1:
            x0 = max(ox - 0.1, x - passo + 0.022)
            l = []
            for xx in np.linspace(x0, x, 6):
                l.append((xx, y_de(xx) - 0.072))
            for xx in np.linspace(x, x0, 6):
                l.append((xx, y_de(xx) + 0.072))
            segs.append((l, 1.0))
            x -= passo
        braco = T.polys(segs, 0.006)
        # munhequeira e o punho
        wx = ponta - 0.19
        wy = y_de(min(wx, ponta))
        cuff = T.polys([([(wx - 0.045, wy - 0.1), (wx + 0.045, wy - 0.1), (wx + 0.045, wy + 0.1), (wx - 0.045, wy + 0.1)], 1.0)], 0.005)
        P, nos = _punho(T, ponta - 0.04, wy - 0.01, 1.35)
        dobra = T.polyline([(xx, y_de(xx) - 0.04) for xx in np.linspace(ox, wx - 0.06, 20)], 0.013)
        G += (braco * 1.0 + cuff * 1.3 + P * 1.2 + T.blur(braco + P, 0.03) * 0.35) * vis
        H += (dobra * 0.45 + cuff * 0.85 + nos * 0.9 + P * 0.25) * vis
    # impacto
    k = pulso(t, hit - 0.01, hit + 0.24)
    est = T.polys([(estrela(0.05, 0.0, 0.3 * k + 0.01, 0.3, 8, 0.4), 1.0)], 0.006) * k
    anel = T.ring(0.1 + 0.55 * ease_out(rel(t, hit, hit + 0.32), 2), 0.035) * pulso(t, hit, hit + 0.36) * 1.2
    g, h = _clarao(T, k, 0.05, 0, 0.2, 0.6)
    fa = faiscas(T, np.random.default_rng(31), t, 12, 0.6, 0.03, cone=(-1.3, 1.3), cx=0.05, inicio=hit)
    G += est * 1.2 + anel + g + fa * 1.2
    H += est * 0.8 + anel * 0.5 + h + fa * 0.7
    return G * env, H * env


# ------------------------------------------------------------------ Broly
def _chama(cx, base, alt, larg, fase, ondula=0.3):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    lado = []
    for k in range(13):
        u = k / 12
        w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
        lado.append((u, w, ondula * larg * math.sin(fase + 6 * u) * u))
    dir_ = [(cx + w + bal, base - alt * u) for u, w, bal in lado]
    esq = [(cx - w + bal, base - alt * u) for u, w, bal in lado[::-1]]
    return dir_ + esq


def punho_lendario(T, t, rng):
    """Punho lendário (Broly): um punho enorme acerta, o estouro em estrela, a aura verde
    explode em labaredas subindo em volta, o chão afunda em rachaduras e voam pedras."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    hit = 0.15
    vem = ease_in(rel(t, 0.0, hit), 1.6)
    px = -1.25 + 1.0 * vem
    vis = 1 - rel(t, hit + 0.05, hit + 0.18)
    P, nos = _punho(T, px, 0.0, 2.6)
    linhas = rastro_de_velocidade(T, rng, 12, 0.0, 0.9, 0.3, -px - 0.25, seed=33, largura=0.02) * (1 - rel(t, hit, hit + 0.12))
    G += (P * 1.3 + linhas * 0.8) * vis
    H += (P * 0.35 + nos * 1.0 + linhas * 0.3) * vis
    # estouro em estrela irregular
    k = pulso(t, hit - 0.01, hit + 0.3)
    sub = np.random.default_rng(88)
    pts = []
    for j in range(22):
        a = j / 22 * TAU
        r = (0.5 if j % 2 == 0 else 0.22) * (0.7 + 0.5 * sub.uniform()) * (0.25 + 0.75 * ease_out(rel(t, hit, hit + 0.12), 2))
        pts.append((math.cos(a) * r, math.sin(a) * r))
    estouro = T.polys([(pts, 1.0)], 0.01) * k
    g, h = _clarao(T, k, 0, 0, 0.35, 1.0)
    onda = T.ring(0.15 + 0.75 * ease_out(rel(t, hit, hit + 0.4), 2), 0.07 * (1 - rel(t, hit, 0.6)) + 0.01) * pulso(t, hit, hit + 0.45) * 1.4
    # aura verde em labaredas que sobem em volta (fica até o fim)
    acende = janela(t, hit + 0.02, hit + 0.15) * apaga(t, 0.62, 0.92)
    formas = []
    sub = np.random.default_rng(401)
    for j in range(11):
        x = (j / 10 * 2 - 1) * 0.55
        alt = 0.95 * (0.5 + 0.5 * math.cos(x / 0.55 * math.pi / 2)) * (0.85 + 0.25 * math.sin(t * 26 + j * 1.7)) * (0.6 + 0.4 * acende)
        formas.append((_chama(x, 0.42, alt, 0.13 + 0.05 * sub.uniform(), t * 30 + j), 0.6 + 0.3 * sub.uniform()))
    aura = T.polys(formas, 0.02) * acende
    # rachaduras no chão (perspectiva achatada, embaixo do alvo)
    rach = T.zero()
    sub = np.random.default_rng(17)
    abre = ease_out(rel(t, hit, hit + 0.15), 2)
    for j in range(9):
        a = j / 9 * TAU + sub.uniform(-0.25, 0.25)
        r = (0.5 + 0.4 * sub.uniform()) * abre
        cam = jagged(sub, 0, 0.42, math.cos(a) * r, 0.42 + math.sin(a) * r * 0.32, 4, 0.25)
        rach += T.polyline(cam, 0.02)
        m = cam[len(cam) // 2]
        b = a + sub.uniform(-0.8, 0.8)
        rach += T.polyline(jagged(sub, m[0], m[1], m[0] + math.cos(b) * 0.22 * abre, m[1] + math.sin(b) * 0.07 * abre, 3, 0.3), 0.012)
    cratera = T.ring(0.2 * abre + 0.01, 0.02, 0, 0.42, squash=3.0)
    rach = (rach + cratera) * janela(t, hit, hit + 0.03)
    # pedras voando
    pedras = []
    sub = np.random.default_rng(55)
    voa = rel(t, hit, 0.9)
    for _ in range(10):
        a = sub.uniform(-math.pi * 0.9, -math.pi * 0.1)
        d = (0.3 + 0.6 * sub.uniform()) * ease_out(voa, 2)
        pedras.append((estrela(math.cos(a) * d, 0.35 + math.sin(a) * d + 0.9 * voa ** 2, 0.045 + 0.025 * sub.uniform(), sub.uniform(0, 3) + t * 8, 3, 0.65),
                       (1 - voa) ** 0.8 * (t > hit)))
    Pd = T.polys(pedras, 0.004)
    G += (estouro * 1.3 + g + onda + aura * 1.0 + T.blur(aura, 0.04) * 0.4 + T.blur(rach, 0.02) * 0.9 + rach * 1.0 + Pd * 1.3) * env
    H += (estouro * 0.9 + h + onda * 0.5 + T.blur(aura, 0.015) * 0.3 * acende + rach * 1.2 + Pd * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Beerus
def toque_da_destruicao(T, t, rng):
    """Toque da destruição (Beerus): o dedo chega e dá um peteleco; nasce uma esferinha roxa
    de destruição que pulsa e implode o ponto, sugando fragmentos que somem."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    toque = 0.14
    # dedo indicador
    vem = ease_out(rel(t, 0.0, toque), 2) * (1 - ease_in(rel(t, 0.22, 0.38), 1.5))
    ponta = -1.05 + 0.88 * vem
    if vem > 0.02:
        d = T.polys([(lamina(ponta - 0.75, 0.04, ponta + 0.02, 0.0, 0.06, 1.0), 1.0),
                     ([(ponta - 0.75, -0.02), (ponta - 0.08, -0.04), (ponta - 0.03, 0.0), (ponta - 0.08, 0.04), (ponta - 0.75, 0.1)], 1.0)], 0.006)
        unha = T.polyline([(ponta - 0.07, -0.025), (ponta - 0.02, -0.01)], 0.012)
        G += d * 0.9
        H += unha * 0.8 + d * 0.15
    tic = pulso(t, toque - 0.01, toque + 0.07)
    G += T.flare(-0.15, 0.0, 0.35 * tic + 0.01, 0.0, 0.02) * tic * 1.5 + T.gauss(-0.15, 0, 0.04) * tic * 2
    H += T.flare(-0.15, 0.0, 0.35 * tic + 0.01, 0.0, 0.02) * tic * 1.5
    # a esfera
    nasce = back(rel(t, toque, toque + 0.12), 2.2)
    implode = ease_in(rel(t, 0.58, 0.72), 2.2)
    bate = 1 + 0.16 * math.sin(t * 46) * janela(t, 0.25, 0.3)
    R = 0.17 * nasce * bate * (1 - implode)
    if R > 0.004:
        esfera = forma(T.gauss(0, 0, R * 0.85, R * 0.85), 0.35, 0.6)
        borda = T.ring(R, 0.018 + 0.01 * R)
        G += (esfera * 1.2 + T.gauss(0, 0, R * 1.7) * 0.9 + borda * 0.5)
        H += borda * 0.9 + T.gauss(-R * 0.3, -R * 0.3, R * 0.25) * 0.8 * (R > 0.03)
        # anel que se fecha (suga)
        fecha = rel(t, 0.32, 0.7)
        G += T.ring(0.75 * (1 - ease_in(fecha, 1.6)) + R, 0.02) * pulso(t, 0.32, 0.72) * 0.9
    # fragmentos do ponto: aparecem rachando e são sugados
    sub = np.random.default_rng(66)
    frags = []
    surge = janela(t, 0.3, 0.4)
    puxa = ease_in(rel(t, 0.45, 0.72), 2.0)
    for _ in range(14):
        a = sub.uniform(0, TAU)
        r0 = 0.24 + 0.32 * sub.uniform()
        r = r0 * (1 - puxa) + 0.01
        gira = a + puxa * 2.2
        tam = (0.045 + 0.03 * sub.uniform()) * (1 - 0.7 * puxa)
        frags.append((estrela(math.cos(gira) * r, math.sin(gira) * r, tam, sub.uniform(0, 3) + puxa * 6, 3, 0.55),
                      surge * (1 - rel(t, 0.66, 0.74))))
    F = T.polys(frags, 0.004)
    G += F * 1.2
    H += F * 0.45
    # a implosão: ponto de luz e um último pulso que some
    k = pulso(t, 0.68, 0.86)
    G += T.gauss(0, 0, 0.05 + 0.12 * k) * k * 1.8 + T.ring(0.05 + 0.3 * rel(t, 0.7, 0.9), 0.015) * k * 0.8
    H += T.flare(0, 0, 0.5 * k + 0.01, 0.8, 0.012) * k * 1.6 + T.gauss(0, 0, 0.04) * k * 1.5
    return G * env, H * env


# ------------------------------------------------------------------ Yusuke
def rei_gun(T, t, rng):
    """Rei Gun (Yusuke): a ponta do dedo carrega, dispara uma bala de energia espiritual que
    atravessa a folha e estoura no alvo num anel largo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    fx, fy = -0.82, 0.0
    carga = janela(t, 0.0, 0.12) * (1 - rel(t, 0.15, 0.22))
    G += T.gauss(fx, fy, 0.04 + 0.05 * carga) * carga * 2.0
    H += T.gauss(fx, fy, 0.03 + 0.02 * carga) * carga * 2.0 + T.flare(fx, fy, 0.3 * carga + 0.01, 0.0, 0.02) * carga
    # anel do disparo
    tiro = pulso(t, 0.13, 0.3)
    G += T.ring(0.05 + 0.15 * rel(t, 0.13, 0.3), 0.02, fx, fy) * tiro
    hit = 0.3
    if 0.14 <= t < hit + 0.01:
        u = ease_in(rel(t, 0.14, hit), 1.3)
        x = fx + (0.0 - fx) * u
        cauda = T.tapered([(x - 0.55, 0.0, x, 0.0, 1.0)], 0.2)
        G += T.gauss(x, 0, 0.1) * 2.0 + T.gauss(x, 0, 0.18) * 0.6 + T.blur(cauda, 0.02) * 1.2
        H += T.gauss(x, 0, 0.065) * 2.5 + T.blur(cauda, 0.01) * 0.5
    # estouro em anel
    e = rel(t, hit, 0.85)
    k = pulso(t, hit - 0.01, hit + 0.22)
    g, h = _clarao(T, k, 0, 0, 0.22, 0.75, 0.0)
    anel1 = T.ring(0.12 + 0.62 * ease_out(e, 2.2), 0.07 * (1 - e) + 0.01) * (1 - e) ** 0.9 * (t >= hit) * 1.5
    anel2 = T.ring(0.08 + 0.4 * ease_out(rel(t, hit + 0.06, 0.85), 2), 0.03) * pulso(t, hit + 0.06, 0.85) * 0.9
    fa = faiscas(T, np.random.default_rng(14), t, 14, 0.75, 0.03, inicio=hit)
    G += g + anel1 + anel2 + fa * 1.1
    H += h + anel1 * 0.8 + anel2 * 0.5 + fa * 0.6
    return G * env, H * env


# ------------------------------------------------------------------ Saitama
def soco_casual(T, t, rng):
    """Soco casual (Saitama): um soquinho com um clarão pequeno... uma pausa... e então um
    vendaval enorme de vento e poeira atravessa a tela inteira (a piada do One Punch)."""
    G, H = vazio(T)
    vem = ease_out(rel(t, 0.0, 0.08), 2)
    vis = 1 - rel(t, 0.12, 0.2)
    P, nos = _punho(T, -0.8 + 0.62 * vem, 0.0, 1.35)
    G += P * 1.1 * vis
    H += (nos * 0.9 + P * 0.3) * vis
    k = pulso(t, 0.07, 0.2)
    G += T.polys([(estrela(0.0, 0.0, 0.17 * k + 0.01, 0.4, 5, 0.45), 1.0)], 0.005) * k * 1.2 + T.gauss(0, 0, 0.08) * k
    H += T.polys([(estrela(0.0, 0.0, 0.17 * k + 0.01, 0.4, 5, 0.45), 1.0)], 0.005) * k * 0.8
    # a pausa: só uma fumacinha boba no ponto do soco
    pft = pulso(t, 0.14, 0.38)
    G += T.ring(0.05 + 0.08 * rel(t, 0.14, 0.38), 0.012) * pft * 0.8 + T.gauss(0.02, -0.03 * rel(t, 0.14, 0.38), 0.035) * pft * 0.6
    H += T.gauss(0.02, -0.03 * rel(t, 0.14, 0.38), 0.025) * pft * 0.4
    # a pausa... e o vendaval
    vento = rel(t, 0.36, 1.0)
    if vento > 0:
        env = apaga(t, 0.78, 1.0, 1.1)
        k2 = pulso(t, 0.35, 0.55)
        frente = T.arc_band(0.25 + 1.3 * ease_out(vento, 1.6), 0.09, -1.1, 1.1, squash=1.4, cx=-0.35, crescente=True)
        frente2 = T.arc_band(0.15 + 1.0 * ease_out(rel(t, 0.42, 1.0), 1.6), 0.06, -1.0, 1.0, squash=1.3, cx=-0.35, crescente=True)
        riscos = []
        sub = np.random.default_rng(81)
        for _ in range(16):
            y = sub.uniform(-0.8, 0.8)
            d = sub.uniform(0, 0.25)
            cab = -0.9 + 2.4 * ease_out(rel(t, 0.36 + d * 0.3, 0.95), 1.4)
            riscos.append((cab - 0.6 * sub.uniform(0.5, 1), y, cab, y + 0.02 * sub.uniform(-1, 1), sub.uniform(0.5, 1)))
        R = T.tapered(riscos, 0.025)
        sub = np.random.default_rng(90)
        po = T.zero()
        for j in range(16):
            y0 = -0.62 + 1.3 * (j % 8) / 7 + sub.uniform(-0.07, 0.07)
            x0 = sub.uniform(-0.95, -0.55) + 0.35 * (j // 8)
            atraso = sub.uniform(0, 0.3)
            u = rel(vento, atraso, 1.0)
            if u <= 0:
                continue
            nv = _nuvem(T, 500 + j, x0 + 1.3 * ease_out(u, 1.5), y0 - 0.1 * u, 0.07 + 0.04 * sub.uniform(), ease_out(u, 1.4), 7, alonga=2.0)
            po += (forma(nv, 0.4, 0.9) * 0.55 + nv * 0.25) * janela(u, 0.0, 0.12) * (1 - 0.4 * u)
        g, h = _clarao(T, k2, -0.2, 0, 0.3, 1.1, 0.0)
        G += (frente * 1.4 + frente2 * 0.9 + R * 1.0 + po * 0.85 + g * 0.6) * env
        H += (frente * 0.8 + frente2 * 0.4 + R * 0.7 + po * 0.35 + h * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Gojo
def infinito(T, t, rng):
    """Golpe do Infinito (Gojo): o punho chega e trava no ar diante do alvo; anéis azuis
    concêntricos se comprimem sem fim (o espaço desacelerando), depois um pulso empurra."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    trava = -0.36
    vem = ease_out(rel(t, 0.0, 0.2), 4.0)
    px = -1.05 + (trava + 1.05) * vem
    treme = 0.008 * math.sin(t * 90) * janela(t, 0.18, 0.22)
    solto = 1 - rel(t, 0.6, 0.7)
    P, nos = _punho(T, px + treme - 0.1 * ease_in(rel(t, 0.6, 0.7), 2), treme, 1.25)
    G += P * 1.0 * solto
    H += (nos + P * 0.3) * solto
    # a parede invisível: anéis em elipse (de frente para o punho) que se fecham para o centro
    cx = trava + 0.2
    U = (T.U - cx) * 2.6
    V = T.V - 0.0
    r = np.sqrt(U * U + V * V)
    liga = janela(t, 0.12, 0.22) * (1 - rel(t, 0.6, 0.66))
    fase = rel(t, 0.12, 0.6) * 2.2
    aneis = T.zero()
    for k in range(8):
        e = k + fase % 1.0
        rk = 0.85 * 0.62 ** e
        w = 0.012 + 0.03 * rk
        aneis += np.exp(-(((r - rk) / w) ** 2)) * min(1.0, e * 1.2) * (0.4 + 0.6 * rk / 0.85)
    G += (aneis * 1.2 + T.blur(aneis, 0.02) * 0.5) * liga
    H += aneis * 0.7 * liga
    G += T.gauss(cx, 0, 0.04, 0.12) * liga * 1.3
    H += T.gauss(cx, 0, 0.02, 0.07) * liga * 1.5
    # o pulso que empurra: anel que estoura e uma meia-lua para a frente
    k = pulso(t, 0.58, 0.82)
    e = rel(t, 0.6, 0.95)
    estouro = T.ring(0.05 + 0.6 * ease_out(e, 2), 0.05 * (1 - e) + 0.008, cx, 0, squash=0.8) * (1 - e) ** 0.8 * (t > 0.6) * 1.4
    empurra = T.arc_band(0.15 + 0.7 * ease_out(e, 2), 0.08, -1.0, 1.0, squash=1.6, cx=cx, crescente=True) * (1 - e) * (t > 0.6) * 1.4
    g, h = _clarao(T, k, cx, 0, 0.2, 0.7, 0.0)
    G += g + estouro + empurra
    H += h + estouro * 0.6 + empurra * 0.7
    return G * env, H * env


# ------------------------------------------------------------------ Yuji
def punho_amaldicoado(T, t, rng):
    """Socos de energia amaldiçoada (Yuji / Black Flash): o soco acerta, o ponto fica negativo:
    faíscas negras e tortas atravessam um clarão vermelho, o espaço racha e treme."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    hit = 0.14
    vem = ease_in(rel(t, 0.0, hit), 1.3)
    vis = 1 - rel(t, hit + 0.04, hit + 0.14)
    P, nos = _punho(T, -1.0 + 0.9 * vem, 0.02, 1.5)
    G += P * 1.1 * vis
    H += (nos + P * 0.3) * vis
    # brilho vermelho do impacto
    k = pulso(t, hit - 0.01, hit + 0.45)
    brilho = T.gauss(0, 0, 0.2 + 0.22 * k) * k * 2.0
    # faíscas negras: raios tortos grossos, escuros no miolo e com borda vermelha
    sub = np.random.default_rng(13 + int(round(t * 11)) // 2)
    nucleo = T.zero()
    abre = ease_out(rel(t, hit, hit + 0.12), 2)
    for j in range(5):
        a = j / 5 * TAU + sub.uniform(-0.4, 0.4)
        r = (0.55 + 0.3 * sub.uniform()) * abre
        pts = jagged(sub, 0, 0, math.cos(a) * r, math.sin(a) * r, 4, 0.4)
        nucleo += T.polyline(pts, 0.04)
        m = pts[len(pts) // 2]
        b = a + sub.uniform(-1.2, 1.2)
        nucleo += T.polyline(jagged(sub, m[0], m[1], m[0] + math.cos(b) * 0.25 * abre, m[1] + math.sin(b) * 0.25 * abre, 3, 0.4), 0.024)
    nucleo = np.clip(nucleo, 0, 1) * janela(t, hit, hit + 0.02) * apaga(t, 0.5, 0.8)
    borda = T.blur(nucleo, 0.03) * 2.6
    escuro = 1 - 0.95 * smooth(nucleo, 0.2, 0.8)
    # rachadura do espaço: estilhaço branco em teia
    rach = T.zero()
    sub2 = np.random.default_rng(29)
    for j in range(5):
        a = sub2.uniform(0, TAU)
        pts = jagged(sub2, 0, 0, math.cos(a) * 0.75 * abre, math.sin(a) * 0.75 * abre, 3, 0.18)
        rach += T.polyline(pts, 0.008)
    rach *= janela(t, hit + 0.02, hit + 0.06) * apaga(t, 0.45, 0.7)
    campo = (brilho + borda) * escuro + rach * 0.6
    # o espaço ondula em volta (distorção)
    d = pulso(t, hit, 0.7) * 0.05
    if d > 0.001:
        n1 = T.noise(np.random.default_rng(7 + int(t * 22)), 0.08, 2)
        n2 = T.noise(np.random.default_rng(8 + int(t * 22)), 0.08, 2)
        campo = T.warp(campo, n1 * d, n2 * d)
        rach = T.warp(rach, n1 * d, n2 * d)
    anel = T.ring(0.1 + 0.65 * ease_out(rel(t, hit, 0.7), 2), 0.04) * pulso(t, hit, 0.72) * 1.1
    flash = pulso(t, hit - 0.01, hit + 0.08)
    G += campo + anel + T.gauss(0, 0, 0.35) * flash * 1.5
    H += rach * 1.4 + borda * escuro * 0.25 + anel * 0.4 + T.flare(0, 0, 1.0 * flash + 0.01, 0.6, 0.012) * flash * 2
    return G * env, H * env


# ------------------------------------------------------------------ Sukuna
def desmanche(T, t, rng):
    """Desmanche (Sukuna): cortes finos invisíveis aparecem quase todos de uma vez, em grade e
    em direções diferentes por cima do alvo; abrem um fio branco e somem."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    sub = np.random.default_rng(1919)
    cortes = []
    for fam, ang0 in enumerate((0.55, -0.7, 1.45)):
        n = 4 if fam < 2 else 2
        for j in range(n):
            ang = ang0 + sub.uniform(-0.08, 0.08)
            off = (j - (n - 1) / 2) * 0.2 + sub.uniform(-0.03, 0.03)
            comp = sub.uniform(0.5, 0.75)
            cx, cy = -math.sin(ang) * off + sub.uniform(-0.05, 0.05), math.cos(ang) * off + sub.uniform(-0.05, 0.05)
            cortes.append((cx, cy, ang, comp))
    ordem = sub.permutation(len(cortes))
    linhas, fios = [], T.zero()
    for pos, i in enumerate(ordem):
        cx, cy, ang, comp = cortes[i]
        a0 = 0.02 + 0.018 * pos
        if t < a0:
            continue
        prog = ease_out(rel(t, a0, a0 + 0.05), 2)
        come = ease_in(rel(t, a0 + 0.22, a0 + 0.5), 1.4)
        c, s = math.cos(ang), math.sin(ang)
        x1, y1, x2, y2 = cx - c * comp, cy - s * comp, cx + c * comp, cy + s * comp
        linhas.append((lamina(x1, y1, x2, y2, 0.018 + 0.006 * pulso(t, a0, a0 + 0.3), prog, come), 1.0))
        brilho = pulso(t, a0, a0 + 0.12)
        if brilho > 0:
            hx, hy = x1 + (x2 - x1) * prog, y1 + (y2 - y1) * prog
            fios += T.gauss(hx, hy, 0.03) * brilho
    L = T.polys(linhas, 0.003) if linhas else T.zero()
    grade = T.blur(L, 0.025)
    flash = pulso(t, 0.08, 0.35)
    G += (L * 1.3 + grade * 1.2 + fios * 1.5 + T.gauss(0, 0, 0.4) * flash * 0.35) * env
    H += (L * 1.4 + fios * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Pikachu
def choque_do_pikachu(T, t, rng):
    """Choque (Pikachu): um raio em zigue-zague chega da esquerda e o alvo fica cercado de
    faíscas amarelas estalando, com círculos de bochecha crepitando em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = int(round(t * 11))
    sub = np.random.default_rng(250 + q)
    # o raio que chega
    chega = ease_out(rel(t, 0.0, 0.14), 1.5)
    if 0 < t < 0.3:
        pts = _zigue(-1.05, -0.05, -1.05 + 1.05 * chega, 0.0, 7, 0.09, 1 if q % 2 else -1)
        z = T.polyline(pts, 0.035) * (1 - rel(t, 0.18, 0.3))
        G += z * 1.3 + T.blur(z, 0.03) * 1.1
        H += z * 1.2
    liga = janela(t, 0.1, 0.16) * apaga(t, 0.62, 0.9)
    # faíscas em zigue-zague em volta do alvo (trocam a cada quadro)
    Z = T.zero()
    if liga > 0:
        for _ in range(5):
            a = sub.uniform(0, TAU)
            r1 = sub.uniform(0.08, 0.25)
            r2 = sub.uniform(0.45, 0.75)
            b = a + sub.uniform(-0.5, 0.5)
            pts = _zigue(math.cos(a) * r1, math.sin(a) * r1, math.cos(b) * r2, math.sin(b) * r2, int(sub.integers(4, 7)), 0.07)
            Z += T.polyline(pts, 0.028)
    G += (Z * 1.3 + T.blur(Z, 0.03) * 1.2) * liga
    H += Z * 1.1 * liga
    # círculos de bochecha crepitando
    C = T.zero()
    for j, (bx, by) in enumerate(((-0.42, -0.42), (0.45, -0.3), (0.3, 0.48))):
        a0 = 0.14 + 0.08 * j
        on = janela(t, a0, a0 + 0.05) * apaga(t, 0.6, 0.85)
        if on <= 0:
            continue
        rr = 0.085 * (1 + 0.12 * math.sin(t * 50 + j * 2))
        disco = forma(T.gauss(bx, by, rr * 0.9), 0.35, 0.6)
        C += (disco * 0.8 + T.ring(rr * 1.4, 0.012, bx, by) * 0.9) * on
        for _ in range(3):
            a = sub.uniform(0, TAU)
            pts = _zigue(bx + math.cos(a) * rr, by + math.sin(a) * rr, bx + math.cos(a) * rr * 2.6, by + math.sin(a) * rr * 2.6, 3, 0.025)
            C += T.polyline(pts, 0.014) * on
    G += C * 1.3 + T.blur(C, 0.03) * 0.6
    H += C * 0.8
    # estalo central
    k = pulso(t, 0.1, 0.32)
    g, h = _clarao(T, k, 0, 0, 0.18, 0.6)
    G += g + T.gauss(0, 0, 0.1) * liga * 0.8 * (0.6 + 0.4 * math.sin(t * 60))
    H += h + T.gauss(0, 0, 0.05) * liga * 0.8
    return G * env, H * env


# ------------------------------------------------------------------ Flash
def soco_relampago(T, t, rng):
    """Soco à velocidade da luz (Flash): riscos de relâmpago convergem de vários lados, uma
    rajada de socos aparece em pontos diferentes no mesmo instante e um impacto final."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sub = np.random.default_rng(777)
    # relâmpagos convergindo (a cabeça corre para o centro)
    R = T.zero()
    for j in range(7):
        a = j / 7 * TAU + sub.uniform(-0.25, 0.25) + math.pi
        a0 = 0.0 + 0.03 * j
        u = ease_in(rel(t, a0, a0 + 0.14), 1.2)
        if u <= 0 or t > a0 + 0.3:
            continue
        cab = 1.05 * (1 - u) + 0.08
        cauda = min(1.1, cab + 0.55)
        come = rel(t, a0 + 0.14, a0 + 0.3)
        cauda = cauda - (cauda - cab) * come
        seg = jagged(np.random.default_rng(300 + j + 7 * int(t * 22)), math.cos(a) * cauda, math.sin(a) * cauda, math.cos(a) * cab, math.sin(a) * cab, 4, 0.22)
        R += T.polyline(seg, 0.022)
    G += R * 1.3 + T.blur(R, 0.03) * 1.2
    H += R * 1.1
    # rastro de velocidade vindo da esquerda
    rs = rastro_de_velocidade(T, rng, 10, 0.0, 0.8, 0.45, 0.2, seed=52, largura=0.014) * pulso(t, 0.1, 0.6)
    G += rs * 0.8
    H += rs * 0.4
    # a saraivada de socos: vultos de punho e estrelinhas em pontos diferentes
    vultos, est = [], []
    sub = np.random.default_rng(91)
    for j in range(16):
        a0 = 0.18 + 0.026 * j
        tx, ty = sub.uniform(-0.3, 0.3), sub.uniform(-0.38, 0.38)
        k = pulso(t, a0, a0 + 0.1)
        if k <= 0:
            continue
        vultos.append((_move(_PUNHO, tx - 0.17 + 0.05 * rel(t, a0, a0 + 0.05), ty, 1.2), k * 0.7))
        est.append((estrela(tx + 0.03, ty, 0.11 * k + 0.01, j * 0.7, 5, 0.42), k))
    if vultos:
        V = T.polys(vultos, 0.01)
        E = T.polys(est, 0.004)
        G += V * 0.9 + E * 1.3
        H += V * 0.25 + E * 0.9
    # impacto final
    k = pulso(t, 0.58, 0.85)
    g, h = _clarao(T, k, 0, 0, 0.3, 0.95)
    anel = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.58, 0.9), 2), 0.04) * pulso(t, 0.58, 0.92) * 1.2
    fa = faiscas(T, np.random.default_rng(5), t, 14, 0.8, 0.03, inicio=0.58)
    G += g + anel + fa * 1.2
    H += h + anel * 0.5 + fa * 0.7
    return G * env, H * env



# ------------------------------------------------------------------ golpes simples (o básico de quem só bate)
def _elipse_pts(cx, cy, rx, ry, ang=0.0, n=16):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(a) * c - ry * math.sin(a) * s, cy + rx * math.cos(a) * s + ry * math.sin(a) * c)
            for a in (TAU * k / n for k in range(n))]


def _punho_simples(T, cx, cy, esc):
    """Punho fechado de lado, os nós dos dedos para a frente (+x): o antebraço, a mão, quatro dedos
    dobrados separados por um vão (é o que faz ler como mão) e o polegar por cima."""
    formas = [([(cx - 0.42 * esc, cy - 0.1 * esc), (cx - 0.08 * esc, cy - 0.13 * esc), (cx - 0.08 * esc, cy + 0.13 * esc), (cx - 0.42 * esc, cy + 0.1 * esc)], 0.8),
              (_elipse_pts(cx - 0.02 * esc, cy, 0.12 * esc, 0.17 * esc), 1.0)]
    for k in range(4):
        formas.append((_elipse_pts(cx + 0.1 * esc, cy - 0.13 * esc + 0.087 * esc * k, 0.075 * esc, 0.038 * esc), 1.0))
    formas.append((_elipse_pts(cx + 0.0 * esc, cy - 0.17 * esc, 0.1 * esc, 0.035 * esc, 0.15), 1.0))
    return np.clip(T.polys(formas, 0.003), 0, 1)


def _pe_simples(cx, cy, esc, ang=0.0):
    """Pé de lado (canela, peito do pé e a sola), a ponta para a frente (+x)."""
    pts = [(-0.34, -0.10), (-0.06, -0.08), (0.10, -0.04), (0.22, -0.01), (0.26, 0.04), (0.22, 0.09), (-0.02, 0.10), (-0.34, 0.08)]
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + (x * c - y * s) * esc, cy + (x * s + y * c) * esc) for x, y in pts]


def _contato(T, t, t0, forca=1.0, seed=5):
    """O contato de um golpe limpo: clarão branco, estrela de impacto, anel de choque achatado e
    os riscos curtos que saem para os lados (o "tchak" visível do quadrinho)."""
    G, H = vazio(T)
    k = pulso(t, t0, t0 + 0.32)
    est = T.polys([(estrela(0.0, 0.0, 0.3 * forca * k + 0.01, 0.25, 8, 0.36), 1.0)], 0.005) * k
    clarao = T.gauss(0, 0, 0.16 * forca, 0.16 * forca) * pulso(t, t0, t0 + 0.18) * 2.2
    anel = T.ring(0.12 + 0.55 * forca * ease_out(rel(t, t0, t0 + 0.45), 2.3), 0.035, squash=1.25) * pulso(t, t0, t0 + 0.5)
    sub = np.random.default_rng(seed)
    segs = []
    u = ease_out(rel(t, t0 + 0.02, t0 + 0.32), 2)
    for j in range(7):
        a = -1.25 + 2.5 * j / 6 + sub.uniform(-0.1, 0.1)
        d0 = 0.22 + 0.25 * u
        d1 = d0 + 0.16 * forca * (1 - u * 0.6)
        segs.append((d0 * math.cos(a), d0 * math.sin(a), d1 * math.cos(a), d1 * math.sin(a), 1.0))
    riscos = T.tapered(segs, 0.022) * pulso(t, t0 + 0.02, t0 + 0.34)
    pts = []
    for _ in range(9):
        a = sub.uniform(-1.0, 1.0)
        d = 0.2 + 0.5 * ease_out(rel(t, t0, t0 + 0.5), 2) * sub.uniform(0.5, 1)
        pts.append((d * math.cos(a), d * math.sin(a) + 0.2 * rel(t, t0, t0 + 0.6) ** 2, pulso(t, t0, t0 + 0.55) * sub.uniform(0.4, 0.9)))
    G += est * 1.2 + clarao + anel + riscos * 1.2 + T.splats(pts, 0.014)
    H += est * 1.0 + clarao * 1.2 + anel * 0.35 + riscos * 0.9 + T.splats(pts, 0.009) * 0.6
    return G, H


def soco_basico(T, t, rng):
    """Soco simples: o punho entra pela esquerda com linhas de velocidade, acerta o centro (clarão,
    estrela e anel de choque), recua um pouco e some — o golpe de quem só dá um soco."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    vem = ease_in(rel(t, 0.0, 0.22), 1.6)
    volta = ease_out(rel(t, 0.26, 0.6), 2)
    px = -0.95 + 0.82 * vem - 0.22 * volta
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.45, 0.62))
    P = _punho_simples(T, px, 0.0, 1.15) * vis
    linhas = rastro_de_velocidade(T, rng, 7, 0.0, 0.55, 0.16, -px - 0.1, cx=0.0, cy=0.0, largura=0.016, seed=21) * (1 - rel(t, 0.2, 0.32)) * 0.8
    g, h = _contato(T, t, 0.2, 1.0, 11)
    G += (P * 1.1 + T.blur(P, 0.02) * 0.5 + linhas + g) * env
    H += (P * 0.55 + linhas * 0.5 + h) * env
    return G, H


def chute_basico(T, t, rng):
    """Chute simples: o pé sobe em arco de baixo para o alvo deixando o rastro do movimento, acerta
    (clarão, estrela, anel) e volta."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    u = ease_in(rel(t, 0.0, 0.24), 1.4)
    caminho = lambda uu: (-0.95 + 0.9 * uu, 0.55 - 0.55 * math.sin(math.pi * 0.5 * uu))
    px, py = caminho(u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.42, 0.6))
    Pe = T.polys([(_pe_simples(px, py, 1.15, -0.6 * (1 - u)), 1.0)], 0.006) * vis
    rastro = [caminho(max(0.0, u - 0.05 * k)) for k in range(10)]
    arco = T.polyline(rastro, 0.07) * (1 - rel(t, 0.22, 0.42)) * 0.7 if u > 0.02 else T.zero()
    g, h = _contato(T, t, 0.22, 1.05, 17)
    G += (Pe * 1.1 + T.blur(Pe, 0.02) * 0.5 + T.blur(arco, 0.01) + g) * env
    H += (Pe * 0.55 + arco * 0.4 + h) * env
    return G, H

REGISTRO = [
    ("soco_basico", soco_basico, GRANDE, "Soco simples: o punho entra, acerta com estrela e anel de choque e recua", False),
    ("chute_basico", chute_basico, GRANDE, "Chute simples: o pé sobe em arco, acerta com estrela e anel de choque e volta", False),
    ("golpe_do_potencial", golpe_do_potencial, GRANDE, "básico do Gohan: soco com aura branca e raios do SSJ2", False),
    ("braco_namekiano", braco_namekiano, GRANDE, "básico do Piccolo: o braço verde estica e acerta", False),
    ("punho_lendario", punho_lendario, GRANDE, "básico do Broly: soco brutal, aura verde explodindo e rachaduras", False),
    ("toque_da_destruicao", toque_da_destruicao, GRANDE, "básico do Beerus: peteleco e a esfera roxa que implode", False),
    ("rei_gun", rei_gun, GRANDE, "básico do Yusuke: tiro do dedo que estoura em anel", False),
    ("soco_casual", soco_casual, GRANDE, "básico do Saitama: soquinho e, depois, o vendaval exagerado", False),
    ("punho_amaldicoado", punho_amaldicoado, GRANDE, "básico do Yuji: Black Flash, faíscas negras e o espaço rachando", False),
    ("desmanche", desmanche, GRANDE, "básico do Sukuna: cortes finos em grade aparecendo de uma vez", False),
    ("choque_do_pikachu", choque_do_pikachu, GRANDE, "básico do Pikachu: faíscas em zigue-zague e bochechas crepitando", False),
    ("soco_relampago", soco_relampago, GRANDE, "básico do Flash: relâmpagos convergindo e mil socos num instante", False),
]
