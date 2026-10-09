"""Ataques básicos com animação própria, lote b.

Naruto (clones na fumaça), Sasuke (Kusanagi com Chidori), Itachi (shurikens),
Sakura (soco que racha o chão), Nezuko (chute de sangue explosivo), Zenitsu
(Primeira Forma), Inosuke (lâminas serrilhadas), Nobara (pregos e ressonância),
Minato (kunai de Hiraishin), Madara (gunbai), Pain (Shinra Tensei curto),
Mikasa (equipamento de manobra) e Eren (soco de titã com vapor).
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


def _suave(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.5
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.65 * k + 0.01, ang=ang + math.pi / 2, thin=0.012)) * k * 1.6
    return g, h


def _puf(T, cx, cy, k, r=0.26, seed=1):
    """Baforada de fumaça de desenho (o clone aparecendo): bolotas que incham e se desfazem.

    Devolve (corpo, borda) já esmaecidos pelo tempo local `k` (0..1)."""
    if k <= 0 or k >= 1:
        return T.zero(), T.zero()
    sub = np.random.default_rng(seed)
    cresce = 0.4 + 0.6 * ease_out(k, 3)
    campo = T.zero()
    n = 8
    for i in range(n):
        a = i / n * TAU + sub.uniform(-0.25, 0.25)
        d = r * 0.74 * cresce
        s = r * (0.24 + 0.06 * sub.uniform()) * cresce
        campo += T.gauss(cx + math.cos(a) * d, cy + math.sin(a) * d * 0.85 - 0.08 * k, s, s)
    campo += T.gauss(cx, cy - 0.05 * k, r * 0.55 * cresce, r * 0.48 * cresce)
    vida = (1 - k) ** 1.2
    corpo = forma(campo, 0.5, 0.6) * vida
    borda = contorno(campo, 0.46, 0.54, 0.6, 0.8) * vida
    # o redemoinho dentro da baforada e os riscos do "puf" saltando para fora
    borda = borda + T.arc_band(r * 0.32 * cresce, 0.018, 0.3 + k * 3, 4.2 + k * 3, cx=cx, cy=cy - 0.05 * k, taper=0.6) * vida * 0.8
    pop = 1 - rel(k, 0.0, 0.4)
    if pop > 0:
        segs = []
        for i in range(6):
            a = i / 6 * TAU + 0.5
            d0 = r * (0.95 + 0.5 * ease_out(k / 0.4, 2))
            segs.append((cx + math.cos(a) * d0, cy + math.sin(a) * d0, cx + math.cos(a) * (d0 + r * 0.35), cy + math.sin(a) * (d0 + r * 0.35), 1.0))
        borda = borda + T.lines(segs, 0.022, 0.003) * pop
    return corpo, borda


def _punho(cx, cy, esc=1.0, ang=0.0):
    """Punho de perfil apontando para +x (contorno com nós dos dedos)."""
    pts = [(-0.3, -0.17), (0.02, -0.2), (0.12, -0.21), (0.2, -0.17), (0.24, -0.1), (0.25, -0.02), (0.24, 0.06),
           (0.22, 0.13), (0.15, 0.19), (0.0, 0.21), (-0.12, 0.18), (-0.3, 0.15)]
    return _gira([(x * esc, y * esc) for x, y in pts], ang, cx, cy)


def _punho_campo(T, cx, cy, esc=1.0):
    """Punho fechado visto de lado (para +x): palma, quatro nós dos dedos na frente, polegar e antebraço."""
    c = T.gauss(cx - 0.04 * esc, cy, 0.17 * esc, 0.15 * esc)
    for k in range(4):
        c += T.gauss(cx + 0.15 * esc, cy + (-0.135 + 0.09 * k) * esc, 0.05 * esc, 0.045 * esc) * 1.1
    c += T.gauss(cx + 0.03 * esc, cy + 0.16 * esc, 0.11 * esc, 0.04 * esc) * 0.9
    c += T.gauss(cx - 0.36 * esc, cy + 0.02 * esc, 0.22 * esc, 0.11 * esc) * 0.9
    return c


def _fenda(T, pts, w0):
    """Rachadura: polígono que afina do começo (w0) até a ponta."""
    n = len(pts)
    cima, baixo = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        w = w0 * (1 - i / max(n - 1, 1)) ** 0.8 + 0.002
        cima.append((x - dy / d * w, y + dx / d * w))
        baixo.append((x + dy / d * w, y - dx / d * w))
    return cima + baixo[::-1]


def _serrilhada(x1, y1, x2, y2, larg, prog, inicio=0.0, dentes=11, fundo=0.45, n=44):
    """Lâmina em lente com as duas bordas dentadas (serrote lascado)."""
    dx, dy = x2 - x1, y2 - y1
    comp = math.hypot(dx, dy) or 1
    nx, ny = -dy / comp, dx / comp
    a, b = inicio, max(inicio + 1e-3, prog)
    cima, baixo = [], []
    for k in range(n + 1):
        u = a + (b - a) * k / n
        w = larg * math.sin(math.pi * min(1, max(0, u))) ** 0.8
        dente = 1.0 if (int(u * dentes * 2) % 2 == 0) else fundo
        dente2 = 1.0 if (int(u * dentes * 2 + 1) % 2 == 0) else fundo
        x, y = x1 + dx * u, y1 + dy * u
        cima.append((x + nx * w * dente, y + ny * w * dente))
        baixo.append((x - nx * w * dente2, y - ny * w * dente2))
    return cima + baixo[::-1]


def _chama(cx, base, alt, larg, fase, ondula=0.25):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    pts = []
    for lado in (1, -1):
        ks = range(13) if lado == 1 else range(12, -1, -1)
        for k in ks:
            u = k / 12
            y = base - alt * u
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, y))
    return pts


# ------------------------------------------------------------------ Naruto
def combo_dos_clones(T, t, rng):
    """Combo do clone: três baforadas de fumaça (clones aparecendo) à esquerda, em cima e embaixo;
    três chutes convergem no alvo, um atrás do outro; um quarto clone surge embaixo e chuta para cima."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    clones = [(-0.68, 0.02, 0.0), (-0.42, -0.6, 0.06), (-0.42, 0.6, 0.12)]
    for i, (cx, cy, a0) in enumerate(clones):
        corpo, borda = _puf(T, cx, cy, rel(t, a0, a0 + 0.55), 0.3, seed=10 + i)
        G += (corpo * 0.7 + borda * 1.3) * env
        H += borda * 0.35 * env
        # o chute: risco grosso do clone até o alvo
        ch = rel(t, a0 + 0.08, a0 + 0.18)
        if 0 < ch:
            px, py = cx + (0 - cx) * ease_out(ch, 2) * 0.92, cy + (0 - cy) * ease_out(ch, 2) * 0.92
            vida = 1 - rel(t, a0 + 0.2, a0 + 0.34)
            if vida > 0:
                ri = T.tapered([(cx * 0.95, cy * 0.95, px, py, 1.0)], 0.2) * vida
                G += T.glow(ri, 0.9, 1.0, 0.02) * env
                H += ri * 0.5 * env
        k = pulso(t, a0 + 0.17, a0 + 0.33)
        if k > 0:
            ang = math.atan2(-cy, -cx)
            st = T.polys([(estrela(0.0, 0.0, 0.2 * k + 0.01, ang, 6, 0.42), 1.0)], 0.006) * k
            G += (st * 1.2 + T.gauss(0, 0, 0.16) * k) * env
            H += st * 0.9 * env
    # o último: clone embaixo, chute para cima levando o alvo
    corpo, borda = _puf(T, 0.0, 0.7, rel(t, 0.36, 0.86), 0.3, seed=21)
    G += (corpo * 0.7 + borda * 1.3) * env
    H += borda * 0.35 * env
    sb = ease_out(rel(t, 0.44, 0.56), 2)
    if sb > 0:
        vida = 1 - rel(t, 0.6, 0.85)
        topo = 0.6 - 1.45 * sb
        ri = T.polys([(lamina(0.0, 0.66, 0.0, topo, 0.12, 1.0), 1.0)], 0.01) * vida
        linhas = rastro_de_velocidade(T, rng, 9, -math.pi / 2, 0.55, 0.3, 0.1 + 0.4 * sb, 0.0, topo + 0.2, 0.02, seed=5) * vida
        G += (T.glow(ri, 0.9, 1.1, 0.03) + linhas * 0.9) * env
        H += (ri * 0.5 + linhas * 0.4) * env
    k = pulso(t, 0.5, 0.78)
    g, h = _clarao(T, k, 0.0, -0.05, 0.28, 0.9, ang=math.pi / 2)
    st = T.polys([(estrela(0.0, -0.05, 0.36 * k + 0.01, -math.pi / 2, 8, 0.38), 1.0)], 0.006) * k
    G += (g + st * 1.2 + T.ring(0.1 + 0.4 * ease_out(rel(t, 0.5, 0.8), 2), 0.03, 0, -0.05) * k) * env
    H += (h + st * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Sasuke
def kusanagi(T, t, rng):
    """Corte da Kusanagi: um risco de katana finíssimo cruza o alvo num instante, com estalos de raio
    (Chidori Nagashi) correndo pela lâmina e saltando para fora."""
    G, H = vazio(T)
    x1, y1, x2, y2 = -0.88, -0.5, 0.86, 0.46
    p = ease_out(rel(t, 0.0, 0.1), 2)
    fim = ease_in(rel(t, 0.32, 0.8), 1.4)
    corpo = T.polys([(lamina(x1, y1, x2, y2, 0.05, p, inicio=fim), 1)], 0.003)
    fio = T.polys([(lamina(x1, y1, x2, y2, 0.014, p, inicio=fim), 1)], 0.0015)
    G += T.glow(corpo, 1.0, 1.1, 0.03) + fio * 1.2
    H += fio * 2.0 + corpo * 0.4
    # estalos elétricos correndo pela lâmina: mudam a cada quadro (o raio pisca)
    viva = janela(t, 0.04, 0.1) * (1 - rel(t, 0.55, 0.85))
    if viva > 0:
        sub = np.random.default_rng(400 + int(t * 11 + 0.5))
        arcos = T.zero()
        dx, dy = x2 - x1, y2 - y1
        nn = math.hypot(dx, dy)
        nx, ny = -dy / nn, dx / nn
        lo = max(fim, 0.05)
        hi = max(lo + 0.05, min(p, 0.95))
        for _ in range(6):
            u0 = sub.uniform(lo, hi)
            u1 = min(0.98, u0 + sub.uniform(0.12, 0.25))
            if u1 <= u0:
                continue
            ax, ay = x1 + dx * u0, y1 + dy * u0
            bx, by = x1 + dx * u1, y1 + dy * u1
            arcos += T.polyline(jagged(sub, ax, ay, bx, by, 4, 0.3), 0.022)
        for _ in range(5):
            u = sub.uniform(lo, hi)
            ax, ay = x1 + dx * u, y1 + dy * u
            lado = sub.choice([-1, 1])
            d = sub.uniform(0.18, 0.38)
            bx, by = ax + nx * d * lado + sub.uniform(-0.1, 0.1), ay + ny * d * lado + sub.uniform(-0.1, 0.1)
            arcos += T.polyline(jagged(sub, ax, ay, bx, by, 3, 0.35), 0.016) * 0.85
        G += T.glow(arcos, 1.2, 1.3, 0.02) * viva
        H += arcos * 1.1 * viva
    k = pulso(t, 0.06, 0.38)
    g, h = _clarao(T, k, 0.0, 0.0, 0.2, 0.75, ang=math.atan2(y2 - y1, x2 - x1))
    G += g
    H += h
    fa = faiscas(T, rng, t, 16, 0.6, 0.025, cone=(-1.2, 0.5), gravidade=0.2, inicio=0.08)
    G += T.glow(fa, 1, 1, 0.02)
    H += fa * 0.6
    return G, H


# ------------------------------------------------------------------ Itachi
def _shuriken(cx, cy, r, ang):
    return estrela(cx, cy, r, ang, 4, 0.3)


def shuriken(T, t, rng):
    """Shuriken Uchiha: três shurikens de quatro pontas chegam girando pela esquerda, uma atrás da
    outra, cravam no alvo com uma faísca e param tremendo."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    voos = [(-0.12, -0.2, 0.0, -0.32), (0.06, 0.02, 0.07, 0.0), (-0.08, 0.24, 0.14, 0.3)]
    for i, (tx, ty, a0, y0) in enumerate(voos):
        chega = a0 + 0.24
        u = rel(t, a0, chega)
        if t < a0:
            continue
        x0 = -1.15
        if u < 1:
            x, y = x0 + (tx - x0) * u, y0 + (ty - y0) * u
            ang = -t * 70 - i
            rastro = T.tapered([(x - 0.5, y - (ty - y0) * 0.4, x, y, 1.0)], 0.12) * 0.45
            giro = T.ring(0.17, 0.02, x, y) * 0.5
        else:
            treme = 0.06 * math.sin(t * 90) * (1 - rel(t, chega, chega + 0.15))
            x, y, ang = tx, ty, 0.35 + treme + i * 0.4
            rastro = T.zero()
            giro = T.zero()
        s = T.polys([(_shuriken(x, y, 0.2, ang), 1.0)], 0.004)
        furo = T.gauss(x, y, 0.032, 0.032)
        s = np.clip(s - furo * 1.2, 0, None)
        G += (T.glow(s, 1.1, 0.7, 0.02) + rastro + giro) * env
        H += (s * 0.75 + rastro * 0.4) * env
        k = pulso(t, chega - 0.01, chega + 0.2)
        if k > 0:
            fa = faiscas(T, np.random.default_rng(70 + i), t, 10, 0.4, 0.022, cone=(-math.pi * 0.85, math.pi * 0.85), gravidade=0.3,
                         cx=tx, cy=ty, inicio=chega - 0.01)
            fl = T.flare(tx, ty, 0.45 * k + 0.01, 0.25, 0.02) * k
            G += (T.glow(fa, 1, 0.9, 0.02) + fl * 1.2 + T.gauss(tx, ty, 0.09) * k) * env
            H += (fa * 0.7 + fl * 1.4) * env
    return G, H


# ------------------------------------------------------------------ Sakura
def soco_de_chakra(T, t, rng):
    """Soco de chakra: o punho chega, acerta com um estouro de chakra e o chão racha em linhas que
    se espalham a partir do ponto do golpe, com pedras voando."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    vem = ease_in(rel(t, 0.0, 0.14), 1.6)
    if t < 0.2:
        px = -0.95 + 0.75 * vem
        P = forma(_punho_campo(T, px, 0.0, 1.1), 0.45, 0.58) * (1 - rel(t, 0.15, 0.2))
        linhas = rastro_de_velocidade(T, rng, 7, 0.0, 0.6, 0.18, 0.15 - 0.8 * vem + 0.75, px + 0.2, 0.0, 0.016, seed=3) * 0.7
        G += (T.glow(P, 1.0, 0.8, 0.02) + linhas) * env
        H += (P * 0.45 + linhas * 0.3) * env
    # rachaduras: crescem do centro para fora (achatadas, como no chão)
    cresce = ease_out(rel(t, 0.14, 0.42), 2)
    if cresce > 0:
        sub = np.random.default_rng(55)
        R = T.zero()
        for k in range(9):
            a = k / 9 * TAU + sub.uniform(-0.25, 0.25)
            L = sub.uniform(0.6, 0.95) * cresce
            pts = jagged(sub, 0.0, 0.05, math.cos(a) * L, 0.05 + math.sin(a) * L * 0.7, 3, 0.2)
            R += T.polys([(_fenda(T, pts, 0.045), 1.0)], 0.003)
            for _ in range(2):
                j = int(sub.integers(len(pts) // 3, len(pts) - 1))
                bx, by = pts[j]
                b = a + sub.choice([-1, 1]) * sub.uniform(0.5, 0.9)
                l2 = sub.uniform(0.15, 0.3) * cresce
                R += T.polys([(_fenda(T, jagged(sub, bx, by, bx + math.cos(b) * l2, by + math.sin(b) * l2 * 0.7, 2, 0.25), 0.022), 0.85)], 0.003)
        viva = 1 - rel(t, 0.6, 1.0)
        G += T.glow(R, 1.2, 1.3, 0.025) * viva
        H += R * 0.9 * viva
    # estouro de chakra
    k = pulso(t, 0.12, 0.45)
    g, h = _clarao(T, k, 0.0, 0.0, 0.3, 1.0)
    st = T.polys([(estrela(0.0, 0.0, 0.34 * k + 0.01, 0.1, 10, 0.45), 1.0)], 0.006) * k
    anel = T.ring(0.12 + 0.75 * ease_out(rel(t, 0.13, 0.55), 2), 0.05, 0, 0.05, squash=1.4) * pulso(t, 0.13, 0.6) * 1.2
    G += (g + st * 1.3 + anel) * env
    H += (h + st + anel * 0.35) * env
    # pedras voando
    pv = rel(t, 0.16, 0.85)
    if 0 < pv < 1:
        sub = np.random.default_rng(66)
        pedras = []
        for _ in range(9):
            a = sub.uniform(-math.pi * 0.95, -math.pi * 0.05)
            v = sub.uniform(0.6, 1.0)
            d = 0.9 * v * pv
            x, y = math.cos(a) * d, 0.05 + math.sin(a) * d + 1.1 * pv * pv
            r = sub.uniform(0.035, 0.06)
            pedras.append((estrela(x, y, r, sub.uniform(0, 6) + pv * 8, 3, 0.75), (1 - pv) ** 0.8))
        Pd = T.polys(pedras, 0.004)
        G += Pd * 1.2 * env
        H += Pd * 0.5 * env
    return G, H


# ------------------------------------------------------------------ Nezuko
def chute_demoniaco(T, t, rng):
    """Chute demoníaco: o chute varre em arco; o sangue espirra do golpe e cada gota acende em chamas
    (Arte Demoníaca: Sangue Explosivo), que sobem e estouram em volta do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    p = ease_out(rel(t, 0.0, 0.2), 2.2)
    arco = T.arc_band(0.68, 0.17, math.pi * 0.95, math.pi * 0.95 + 2.1 * p + 0.01, cx=0.05, cy=0.3, crescente=True)
    arco *= 1 - rel(t, 0.25, 0.5)
    G += T.glow(arco, 1.0, 1.0, 0.03) * env
    H += arco * 0.6 * env
    k = pulso(t, 0.15, 0.4)
    g, h = _clarao(T, k, 0.0, -0.05, 0.25, 0.7)
    G += g * env
    H += h * env
    # gotas de sangue espirram e acendem
    sub = np.random.default_rng(88)
    gotas, chamas, nucleos = [], [], []
    for i in range(6):
        a = (i / 6) * TAU + 0.3 + sub.uniform(-0.2, 0.2)
        d = sub.uniform(0.42, 0.58)
        tx, ty = math.cos(a) * d, 0.12 + math.sin(a) * d * 0.62
        voa = rel(t, 0.18, 0.34 + 0.015 * i)
        acende = 0.33 + 0.02 * i
        if 0 < voa and t < acende:
            gx, gy = tx * ease_out(voa, 2), -0.05 + (ty + 0.05) * ease_out(voa, 2)
            gotas.append((gx, gy, 1.0))
        q = rel(t, acende, acende + 0.5)
        if 0 < q < 1:
            alt = 0.55 * back(min(1.0, q * 2.5), 2.0) * (1 - q) ** 0.6
            ch = _chama(tx, ty + 0.08, alt + 0.02, 0.15, t * 40 + i * 2, 0.45)
            chamas.append((ch, 0.9))
            nucleos.append((_chama(tx, ty + 0.08, (alt + 0.02) * 0.55, 0.07, t * 40 + i * 2, 0.45), 1.0))
            chamas.append((estrela(tx, ty - alt * 0.25, 0.2 * pulso(q, 0.0, 0.45) + 0.005, i, 7, 0.45), 0.9))
    Go = T.splats(gotas, 0.022) * 2.2
    C = T.polys(chamas, 0.012)
    nucleo = T.polys(nucleos, 0.01)
    G += (Go + T.glow(C, 1.1, 0.9, 0.03)) * env
    H += (Go * 0.4 + nucleo * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Zenitsu
def saque_do_trovao(T, t, rng):
    """Saque do trovão (Primeira Forma): um risco de relâmpago horizontal atravessa a tela inteira
    de uma vez, clarão branco, e o rastro vira um raio em ziguezague que fica estalando e some."""
    G, H = vazio(T)
    inc = -0.06
    eixo = T.V - inc * T.U
    # o risco: atravessa em 2 quadros
    p = ease_out(rel(t, 0.0, 0.1), 2)
    cabeca = -1.0 + 2.1 * p
    faixa = np.exp(-(eixo / 0.035) ** 2) * smooth(cabeca - T.U, -0.02, 0.05) * smooth(T.U, -1.0, -0.6 + 1.2 * p)
    faixa *= 1 - rel(t, 0.12, 0.3)
    G += faixa * 2.2 + T.blur(faixa, 0.05) * 1.5
    H += faixa * 2.2
    k = pulso(t, 0.04, 0.32)
    G += T.gauss(0, 0, 0.6, 0.18) * k * 2.2
    H += (T.flare(0, 0, 2.0 * k + 0.01, inc, 0.01) + T.gauss(0, 0, 0.3, 0.08) * 1.5) * k * 1.5
    # o raio que fica: ziguezague largo, muda a cada quadro
    fica = janela(t, 0.08, 0.14) * (1 - rel(t, 0.5, 0.95))
    if fica > 0:
        sub = np.random.default_rng(300 + int(t * 11 + 0.5))
        pts = []
        n = 9
        for i in range(n + 1):
            x = -0.95 + 1.9 * i / n
            y = inc * x + (0.14 if i % 2 else -0.14) * (0.6 + 0.4 * sub.uniform()) * (i not in (0, n))
            pts.append((x, y))
        fino = []
        for a, b in zip(pts, pts[1:]):
            fino += jagged(sub, a[0], a[1], b[0], b[1], 2, 0.12)[:-1]
        fino.append(pts[-1])
        Z = T.polyline(fino, 0.03)
        gal = T.zero()
        for i in range(1, n, 2):
            ax, ay = pts[i]
            gal += T.polyline(jagged(sub, ax, ay, ax + sub.uniform(-0.1, 0.2), ay + sub.choice([-1, 1]) * sub.uniform(0.2, 0.35), 3, 0.3), 0.012)
        G += (T.glow(Z, 1.3, 1.4, 0.03) + T.glow(gal, 1, 1, 0.02) * 0.8) * fica
        H += (Z * 1.4 + gal * 0.6) * fica
    fa = faiscas(T, rng, t, 14, 0.5, 0.022, cone=(-math.pi, math.pi), gravidade=0.25, inicio=0.06)
    G += T.glow(fa, 1, 0.9, 0.02) * 0.9
    H += fa * 0.5
    return G, H


# ------------------------------------------------------------------ Inosuke
def laminas_serrilhadas(T, t, rng):
    """Lâminas serrilhadas: dois cortes em X com as bordas dentadas e lascadas, um atrás do outro,
    selvagens, com lascas voando."""
    G, H = vazio(T)
    cortes = [(-0.82, -0.72, 0.78, 0.66, 0.0), (-0.78, 0.7, 0.82, -0.66, 0.14)]
    for x1, y1, x2, y2, a0 in cortes:
        p = ease_out(rel(t, a0, a0 + 0.13), 2.2)
        if p <= 0:
            continue
        fim = ease_in(rel(t, a0 + 0.32, a0 + 0.78), 1.3)
        corpo = T.polys([(_serrilhada(x1, y1, x2, y2, 0.12, p, fim, dentes=12, fundo=0.35), 1.0)], 0.003)
        fio = T.polys([(lamina(x1, y1, x2, y2, 0.022, p, inicio=fim), 1.0)], 0.002)
        G += T.glow(corpo, 1.0, 0.9, 0.025) + fio
        H += fio * 1.6 + corpo * 0.3
    k = pulso(t, 0.14, 0.42)
    g, h = _clarao(T, k, 0, 0, 0.22, 0.7, ang=math.pi / 4)
    G += g
    H += h
    fa = faiscas(T, rng, t, 18, 0.65, 0.028, cone=(0, TAU), gravidade=0.35, inicio=0.06)
    G += T.glow(fa, 1, 1, 0.02)
    H += fa * 0.6
    return G, H


# ------------------------------------------------------------------ Nobara
def _prego(x, y, ang=0.0, esc=1.0):
    """Prego de perfil apontando para +x: cabeça larga atrás e ponta fina."""
    pts = [(-0.16, -0.05), (-0.13, -0.05), (-0.13, -0.016), (0.12, -0.012), (0.18, 0.0), (0.12, 0.012), (-0.13, 0.016),
           (-0.13, 0.05), (-0.16, 0.05)]
    return _gira([(px * esc, py * esc) for px, py in pts], ang, x, y)


def _martelo(cx, cy, ang, esc=1.0):
    """Martelo: cabo e cabeça (o pivô é a ponta do cabo, cx,cy; ang 0 = cabo para +x)."""
    cabo = [(0.0, -0.025), (0.42, -0.025), (0.42, 0.025), (0.0, 0.025)]
    cabeca = [(0.36, -0.15), (0.52, -0.15), (0.52, 0.12), (0.47, 0.15), (0.41, 0.15), (0.36, 0.12)]

    def f(pts):
        return _gira([(x * esc, y * esc) for x, y in pts], ang, cx, cy)
    return f(cabo), f(cabeca)


def martelo_e_prego(T, t, rng):
    """Martelo e prego (Nobara): três pregos voam e cravam no alvo; o martelo desce num prego e a
    ressonância estoura em cada prego, um atrás do outro."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    pregos = [(-0.08, -0.3, 0.0, -0.4), (0.1, 0.0, 0.04, 0.05), (-0.05, 0.3, 0.08, 0.42)]
    for i, (tx, ty, a0, y0) in enumerate(pregos):
        u = rel(t, a0, a0 + 0.18)
        if t < a0:
            continue
        x0 = -1.1
        x, y = x0 + (tx - x0) * ease_in(u, 1.2), y0 + (ty - y0) * u
        estoura = 0.5 + 0.09 * i
        some_ = 1 - rel(t, estoura, estoura + 0.05)
        P = T.polys([(_prego(x, y, math.atan2(ty - y0, tx - x0), 1.15), 1.0)], 0.003) * some_
        rastro = T.tapered([(x - 0.4, y - (ty - y0) * 0.3, x - 0.15, y, 1.0)], 0.04) * (1 - u) * 0.8
        G += (T.glow(P, 1.2, 0.6, 0.015) + rastro) * env
        H += (P * 0.8 + rastro * 0.3) * env
        k = pulso(t, a0 + 0.17, a0 + 0.3)
        if k > 0:
            fl = T.flare(tx + 0.18, ty, 0.25 * k + 0.01, 0.4, 0.02) * k
            G += fl * env
            H += fl * env
        # ressonância: estouro espinhoso em cada prego
        q = rel(t, estoura, estoura + 0.32)
        if 0 < q < 1:
            kk = pulso(q, 0.0, 1.0)
            st = T.polys([(estrela(tx + 0.1, ty, 0.25 * back(min(1, q * 2.5), 1.8) + 0.01, i * 0.7, 9, 0.35), 1.0)], 0.005) * (1 - q) ** 0.8
            anel = T.ring(0.05 + 0.3 * ease_out(q, 2), 0.025, tx + 0.1, ty) * kk
            G += (st * 1.3 + anel + T.gauss(tx + 0.1, ty, 0.12) * kk) * env
            H += (st * 0.8 + T.gauss(tx + 0.1, ty, 0.05) * kk * 1.5) * env
    # o martelo desce de cima (à esquerda) e bate
    m = rel(t, 0.3, 0.46)
    if 0 < m and t < 0.62:
        ang = -2.4 + 1.65 * ease_in(m, 2.2)
        cabo, cabeca = _martelo(-0.62, 0.45, ang, 1.3)
        vida = 1 - rel(t, 0.52, 0.62)
        M = T.polys([(cabo, 0.8), (cabeca, 1.0)], 0.004) * vida
        G += T.glow(M, 1.0, 0.6, 0.02) * env
        H += M * 0.4 * env
        if m < 1:
            arc = T.arc_band(0.6, 0.08, -2.2, -2.2 + 1.5 * m + 0.01, cx=-0.62, cy=0.45, taper=1.5) * 0.7
            G += arc * env
    k = pulso(t, 0.44, 0.62)
    if k > 0:
        st = T.polys([(estrela(-0.02, -0.0, 0.22 * k + 0.01, 0.3, 8, 0.4), 1.0)], 0.005) * k
        G += (st + T.gauss(0, 0, 0.18) * k) * env
        H += st * env
    return G, H


# ------------------------------------------------------------------ Minato
def _kunai3(x, y, ang, esc=1.0):
    """Kunai de três pontas do Minato (aponta para +x)."""
    pts = [(0.24, 0.0), (0.08, -0.035), (0.11, -0.11), (0.0, -0.05), (-0.05, -0.02), (-0.18, -0.016), (-0.18, 0.016),
           (-0.05, 0.02), (0.0, 0.05), (0.11, 0.11), (0.08, 0.035)]
    return _gira([(px * esc, py * esc) for px, py in pts], ang, x, y)


def kunai_de_hiraishin(T, t, rng):
    """Kunai de Hiraishin: a kunai de três pontas crava, a fórmula brilha, um clarão amarelo
    instantâneo (o teletransporte) e o golpe estoura no alvo no mesmo instante."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    tx, ty = -0.12, 0.08
    u = rel(t, 0.0, 0.2)
    x = -1.15 + (tx + 1.15) * u
    y = ty + 0.12 * (1 - u) * u
    K = T.polys([(_kunai3(x, y, -0.02, 1.6), 1.0)], 0.003)
    aro = T.ring(0.05, 0.011, x - 0.34, y)
    vida = 1 - rel(t, 0.62, 0.8)
    rastro = T.tapered([(x - 0.7, y, x - 0.2, y, 1.0)], 0.05) * (1 - u) * 0.8
    G += (T.glow(K + aro, 1.2, 0.6, 0.02) * vida + rastro) * env
    H += ((K + aro) * 0.8 * vida + rastro * 0.3) * env
    # a fórmula da marca acende no cabo
    f = pulso(t, 0.2, 0.45)
    if f > 0:
        marca = T.zero() + T.polyline([(tx - 0.2, ty - 0.08), (tx - 0.26, ty - 0.12), (tx - 0.32, ty - 0.06), (tx - 0.38, ty - 0.11)], 0.012)
        marca += T.polyline([(tx - 0.2, ty + 0.08), (tx - 0.27, ty + 0.12), (tx - 0.33, ty + 0.07)], 0.012)
        G += marca * f * 1.3 * env
        H += marca * f * env
    # o clarão do teleporte: instantâneo, enorme, vertical (a silhueta chegando)
    k = pulso(t, 0.26, 0.42)
    if k > 0:
        coluna = T.gauss(tx, ty - 0.1, 0.06 + 0.1 * k, 0.55) * k * 2.2
        G += (coluna + T.gauss(tx, ty, 0.5) * k * 1.3) * env
        H += (T.flare(tx, ty, 2.0 * k, 0.0, 0.012) * 1.6 + T.gauss(tx, ty - 0.1, 0.04, 0.4) * k * 2) * env
    # o golpe: corte rápido atravessando o alvo
    p = ease_out(rel(t, 0.36, 0.46), 2)
    if p > 0:
        fim = rel(t, 0.5, 0.8)
        cut = T.polys([(lamina(-0.6, 0.45, 0.65, -0.5, 0.07, p, inicio=fim), 1.0)], 0.003)
        G += T.glow(cut, 1.0, 1.1, 0.025) * env
        H += cut * 0.8 * env
    kk = pulso(t, 0.4, 0.66)
    st = T.polys([(estrela(0.0, 0.0, 0.3 * kk + 0.01, 0.2, 8, 0.4), 1.0)], 0.005) * kk
    G += (st * 1.2 + T.ring(0.1 + 0.55 * ease_out(rel(t, 0.4, 0.75), 2), 0.03) * kk) * env
    H += st * 0.8 * env
    sub = np.random.default_rng(12)
    raios = []
    for _ in range(10):
        a = sub.uniform(0, TAU)
        r0 = 0.25 + 0.4 * ease_out(rel(t, 0.4, 0.7), 2)
        raios.append((math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * (r0 + 0.25), math.sin(a) * (r0 + 0.25), 1.0))
    L = T.lines(raios, 0.016, 0.004) * pulso(t, 0.4, 0.72)
    G += L * env
    H += L * 0.5 * env
    return G, H


# ------------------------------------------------------------------ Madara
def _gunbai(cx, cy, ang, esc=1.0):
    """Gunbai: o grande leque de guerra (o leque do brasão Uchiha). Devolve (metade de cima, metade de
    baixo, cabo, contorno). O pivô (cx, cy) é a ponta do cabo, e a lâmina redonda fica em +x."""
    def g(pts):
        return _gira([(x * esc, y * esc) for x, y in pts], ang, cx, cy)
    # lâmina: oval mais larga que comprida (uma pá), presa no fim do cabo
    pa = [(0.52 + 0.22 * math.cos(a), 0.3 * math.sin(a) * (1 - 0.15 * math.cos(a))) for a in np.linspace(0, TAU, 44, endpoint=False)]
    cabo = [(0.0, -0.035), (0.32, -0.045), (0.32, 0.045), (0.0, 0.035)]
    nervura = [(0.3, 0.0), (0.72, 0.0)]
    return g(pa), g(cabo), g(nervura)


def leque_gunbai(T, t, rng):
    """Leque Gunbai: o grande leque varre de cima para baixo à esquerda e solta uma parede de vento
    em leque, em faixas curvas que atravessam o alvo, com riscos de vento."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    v = _suave(rel(t, 0.0, 0.26))
    ang = -1.25 + 1.75 * v
    piv = (-0.92, 0.35)
    vida = 1 - rel(t, 0.32, 0.5)
    # cópias fantasmas atrás do leque: o borrão da varrida
    for j, atraso in enumerate((0.0, 0.05, 0.1, 0.15)):
        aj = -1.25 + 1.75 * _suave(rel(t - atraso, 0.0, 0.26))
        pa, cabo, nerv = _gunbai(piv[0], piv[1], aj, 1.25)
        peso = (1.0, 0.35, 0.2, 0.1)[j]
        F = T.polys([(pa, 0.6), (cabo, 1.0)], 0.004) * vida * peso
        borda = (T.polyline(pa + [pa[0]], 0.024) + T.polyline(nerv, 0.018)) * vida * peso
        G += (F + T.glow(borda, 1.1, 0.6, 0.02)) * env
        H += (borda * 0.6 + F * 0.15) * env * (j == 0)
    if v < 1:
        rastro = T.arc_band(0.55, 0.2, -1.25, -1.25 + 1.75 * v + 0.01, cx=piv[0], cy=piv[1], taper=1.6) * 0.7
        G += rastro * env
    # a parede de vento: arcos concêntricos que avançam
    for i in range(4):
        a0 = 0.16 + i * 0.07
        q = rel(t, a0, a0 + 0.55)
        if 0 < q < 1:
            r = 0.35 + 1.45 * ease_out(q, 1.6)
            abre = 0.55 + 0.1 * i
            onda = T.arc_band(r, 0.07 * (1 - 0.4 * q) + 0.02, -abre, abre, cx=-1.05, cy=0.0, crescente=True)
            G += T.glow(onda, 1.0, 0.8, 0.03) * (1 - q) ** 0.9 * 1.2 * env
            H += onda * 0.35 * (1 - q) * env
    # riscos de vento retos dentro do leque
    q = rel(t, 0.2, 0.85)
    if 0 < q < 1:
        sub = np.random.default_rng(42)
        segs = []
        for _ in range(12):
            a = sub.uniform(-0.6, 0.6)
            d = -0.2 + 1.8 * q * sub.uniform(0.7, 1.1)
            L = sub.uniform(0.25, 0.45)
            segs.append((-1.05 + math.cos(a) * (d - L + 0.2), math.sin(a) * (d - L + 0.2), -1.05 + math.cos(a) * (d + 0.2), math.sin(a) * (d + 0.2), 1.0))
        W = T.tapered(segs, 0.025) * (1 - q)
        G += W * env
        H += W * 0.4 * env
    return G, H


# ------------------------------------------------------------------ Pain
def rinnegan(T, t, rng):
    """Golpe dos Seis Caminhos: o olho do Rinnegan (anéis concêntricos) se abre no alvo e as ondas
    de repulsão (Shinra Tensei curto) estouram para fora em círculos, empurrando os detritos."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    olho = janela(t, 0.0, 0.12) * (1 - rel(t, 0.3, 0.55))
    if olho > 0:
        esc = 0.6 + 0.4 * back(rel(t, 0.0, 0.14), 1.6)
        O = sum(T.ring(r * esc, 0.012) for r in (0.07, 0.13, 0.19, 0.25)) + T.gauss(0, 0, 0.028)
        G += T.glow(O, 1.3, 0.8, 0.02) * olho * env
        H += O * 0.8 * olho * env
    # ondas de repulsão
    for i in range(3):
        a0 = 0.18 + i * 0.12
        q = rel(t, a0, a0 + 0.5)
        if 0 < q < 1:
            r = 0.15 + 0.85 * ease_out(q, 2)
            w = 0.03 + 0.06 * (1 - q)
            onda = T.ring(r, w) * (1 - q) ** 1.1
            frente = T.ring(r + w * 0.6, 0.012) * (1 - q)
            G += (onda * 1.3 + T.blur(onda, 0.04) * 0.6) * env
            H += frente * 0.8 * env
    k = pulso(t, 0.15, 0.4)
    G += T.gauss(0, 0, 0.3) * k * 1.4 * env
    H += T.gauss(0, 0, 0.12) * k * 1.2 * env
    # detritos empurrados para fora
    q = rel(t, 0.2, 0.9)
    if 0 < q < 1:
        sub = np.random.default_rng(23)
        segs = []
        for _ in range(16):
            a = sub.uniform(0, TAU)
            d = 0.2 + 0.85 * ease_out(q, 1.8) * sub.uniform(0.6, 1.0)
            L = 0.12 * (1 - q) + 0.03
            segs.append((math.cos(a) * (d - L), math.sin(a) * (d - L), math.cos(a) * d, math.sin(a) * d, 1.0))
        D = T.tapered(segs, 0.03) * (1 - q)
        G += D * env
        H += D * 0.5 * env
    return G, H


# ------------------------------------------------------------------ Mikasa
def laminas_odm(T, t, rng):
    """Corte das lâminas: os dois cabos do equipamento de manobra disparam e cravam atrás do alvo,
    o gás sopra, duas lâminas cortam em X num instante e somem; os cabos recolhem."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    ancoras = [(0.72, -0.62), (0.72, 0.6)]
    orig = (-0.9, 0.05)
    for i, (ax, ay) in enumerate(ancoras):
        sai = ease_out(rel(t, 0.0 + 0.03 * i, 0.14 + 0.03 * i), 2)
        volta = ease_in(rel(t, 0.55, 0.72), 2)
        if sai <= 0 or volta >= 1:
            continue
        hx, hy = orig[0] + (ax - orig[0]) * sai, orig[1] + (ay - orig[1]) * sai
        tx, ty = orig[0] + (ax - orig[0]) * volta, orig[1] + (ay - orig[1]) * volta
        cabo = T.polyline([(tx, ty), ((tx + hx) / 2, (ty + hy) / 2 + 0.03 * (1 - sai)), (hx, hy)], 0.012)
        gancho = T.polys([(estrela(hx, hy, 0.05, math.atan2(ay - orig[1], ax - orig[0]), 3, 0.4), 1.0)], 0.003)
        G += (cabo * 0.9 + T.blur(cabo, 0.015) * 0.6 + gancho) * env
        H += (cabo * 0.6 + gancho * 0.7) * env
        k = pulso(t, 0.12 + 0.03 * i, 0.3 + 0.03 * i)
        if k > 0:
            G += T.flare(ax, ay, 0.3 * k + 0.01, 0.3, 0.02) * k * env
            H += T.flare(ax, ay, 0.3 * k + 0.01, 0.3, 0.02) * k * env
    # gás saindo do equipamento
    corpo, borda = _puf(T, -0.78, 0.08, rel(t, 0.08, 0.6), 0.2, seed=5)
    G += (corpo * 0.4 + borda * 0.6) * env
    # dois cortes em X
    for x1, y1, x2, y2, a0 in ((-0.7, -0.62, 0.66, 0.58, 0.24), (-0.7, 0.6, 0.66, -0.6, 0.3)):
        p = ease_out(rel(t, a0, a0 + 0.08), 2.5)
        if p <= 0:
            continue
        fim = ease_in(rel(t, a0 + 0.12, a0 + 0.38), 1.3)
        corpo = T.polys([(lamina(x1, y1, x2, y2, 0.08, p, inicio=fim), 1)], 0.003)
        fio = T.polys([(lamina(x1, y1, x2, y2, 0.02, p, inicio=fim), 1)], 0.0015)
        G += T.glow(corpo, 1.1, 1.0, 0.025) + fio
        H += fio * 1.8 + corpo * 0.35
    k = pulso(t, 0.28, 0.5)
    g, h = _clarao(T, k, 0, 0, 0.2, 0.7, ang=math.pi / 4)
    G += g
    H += h
    fa = faiscas(T, rng, t, 12, 0.55, 0.024, cone=(-1.0, 1.0), gravidade=0.3, inicio=0.28)
    G += T.glow(fa, 1, 1, 0.02)
    H += fa * 0.6
    return G, H


# ------------------------------------------------------------------ Eren
def soco_titanico(T, t, rng):
    """Soco titânico: um punho enorme de titã entra pela esquerda, o impacto é colossal (clarão,
    onda e estrela) e o vapor quente sobe em nuvens grossas do ponto do golpe."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.2), 1.8)
    recua = ease_out(rel(t, 0.3, 0.55), 2)
    if t < 0.55:
        px = -1.2 + 0.95 * vem - 0.45 * recua
        vida = 1 - rel(t, 0.38, 0.55)
        campo = _punho_campo(T, px, 0.0, 2.2)
        P = forma(campo, 0.45, 0.56) * vida
        B_ = contorno(campo, 0.42, 0.5, 0.56, 0.75) * vida
        nos = T.zero()
        for k in range(3):
            yy = (-0.09 + 0.09 * k) * 2.2
            nos = nos + T.polyline([(px + 0.12 * 2.2, yy), (px + 0.2 * 2.2, yy)], 0.016)
        nos = nos + T.polyline([(px - 0.2 * 2.2, -0.16 * 2.2), (px - 0.22 * 2.2, 0.16 * 2.2)], 0.016)
        nos = T.blur(nos, 0.006) * vida
        P = P * np.clip(1 - nos * 1.5, 0, 1)
        G += (P * 0.75 + T.glow(B_, 1.2, 0.5, 0.02)) * env
        H += (P * 0.15 + B_ * 0.5) * env
        linhas = rastro_de_velocidade(T, rng, 9, 0.0, 0.8, 0.45, 0.6 - 0.6 * vem, px - 0.1, 0.0, 0.02, seed=8) * (1 - rel(t, 0.18, 0.28))
        G += linhas * env
    k = pulso(t, 0.18, 0.5)
    g, h = _clarao(T, k, 0.15, 0.0, 0.4, 1.3)
    st = T.polys([(estrela(0.15, 0.0, 0.45 * k + 0.01, 0.15, 10, 0.4), 1.0)], 0.006) * k
    onda = T.ring(0.2 + 0.85 * ease_out(rel(t, 0.18, 0.6), 2), 0.06, 0.15, 0.0) * pulso(t, 0.18, 0.65) * 1.3
    G += (g * 1.2 + st * 1.3 + onda) * env
    H += (h + st + onda * 0.3) * env
    # vapor: bolotões que sobem, incham e esmaecem
    q = rel(t, 0.28, 1.0)
    if q > 0:
        # vapor: várias baforadas que nascem no ponto do golpe e sobem juntas, uma nuvem só que incha
        sub = np.random.default_rng(31)
        campo = T.zero()
        for i in range(7):
            nasce = 0.06 * i
            u = rel(q, nasce, nasce + 0.65)
            if not 0 < u < 1:
                continue
            x = 0.15 + (sub.uniform(-0.5, 0.5)) * (0.5 + 0.5 * u) + 0.05 * math.sin(u * 6 + i)
            y = 0.25 - 0.95 * ease_out(u, 1.2) * sub.uniform(0.7, 1.0)
            r = (0.1 + 0.1 * ease_out(u, 2)) * sub.uniform(0.85, 1.15)
            vida = (1 - u) ** 0.6
            for j in range(6):
                a = j / 6 * TAU + sub.uniform(-0.3, 0.3) + u * 1.5
                campo += T.gauss(x + math.cos(a) * r * 0.7, y + math.sin(a) * r * 0.6, r * 0.38, r * 0.38) * vida
            campo += T.gauss(x, y, r * 0.55, r * 0.5) * vida
        V = forma(campo, 0.5, 0.62)
        Vb = contorno(campo, 0.45, 0.55, 0.62, 0.85)
        G += (V * 0.5 + Vb * 0.9 + T.blur(V, 0.04) * 0.3) * env
        H += (V * 0.22 + Vb * 0.2) * env
        # fios de vapor quente ondulando para cima
        fios = T.zero()
        for i, x0 in enumerate((-0.25, 0.05, 0.35, 0.6)):
            base = 0.35 - 0.6 * ease_out(q, 1.5)
            pts = [(x0 + 0.05 * math.sin(k * 0.9 + t * 14 + i * 2), base - 0.06 * k) for k in range(8)]
            fios = fios + T.polyline(pts, 0.016)
        fios = T.blur(fios, 0.006) * pulso(q, 0.0, 1.0)
        G += fios * 0.9 * env
        H += fios * 0.3 * env
    return G, H


REGISTRO = [
    ("combo_dos_clones", combo_dos_clones, GRANDE, "Naruto: clones surgem na fumaça e chutam, o último para cima", False),
    ("kusanagi", kusanagi, GRANDE, "Sasuke: corte fino de katana com estalos de Chidori na lâmina", False),
    ("shuriken", shuriken, GRANDE, "Itachi: três shurikens de quatro pontas chegam girando e cravam", False),
    ("soco_de_chakra", soco_de_chakra, GRANDE, "Sakura: soco com estouro de chakra e o chão rachando", False),
    ("chute_demoniaco", chute_demoniaco, GRANDE, "Nezuko: chute em arco e o sangue explode em chamas", False),
    ("saque_do_trovao", saque_do_trovao, GRANDE, "Zenitsu: risco de relâmpago horizontal e o raio em ziguezague", False),
    ("laminas_serrilhadas", laminas_serrilhadas, GRANDE, "Inosuke: dois cortes em X com bordas dentadas", False),
    ("martelo_e_prego", martelo_e_prego, GRANDE, "Nobara: pregos cravam, o martelo bate e a ressonância estoura", False),
    ("kunai_de_hiraishin", kunai_de_hiraishin, GRANDE, "Minato: kunai de três pontas, clarão do teleporte e o golpe", False),
    ("leque_gunbai", leque_gunbai, GRANDE, "Madara: o gunbai varre e solta uma parede de vento em leque", False),
    ("rinnegan", rinnegan, GRANDE, "Pain: olho do Rinnegan e ondas de repulsão para fora", False),
    ("laminas_odm", laminas_odm, GRANDE, "Mikasa: cabos de manobra, gás e duas lâminas em X", False),
    ("soco_titanico", soco_titanico, GRANDE, "Eren: punho de titã, impacto colossal e vapor subindo", False),
]
