"""Elementos com variações: fogo, gelo, raio, água, terra, ar, natureza, sangue, lua, som."""
from __future__ import annotations

import math

import numpy as np

from .base import (FAIXA, GRANDE, TAU, _subindo, apaga, back, ease_in, ease_out, faiscas, girado, jagged, janela,
                   lamina, poeira, pulso, rel, smooth, some, vazio)


def _chama_em(T, t, seed, base, altura, largura, cx=0.0, vel=1.0):
    """Uma língua de fogo subindo de (cx, base): silhueta que dança e núcleo claro."""
    n1 = _subindo(T, seed, t, 0.09, 0.8 * vel)
    yr = (base - T.V) / altura
    y = np.clip(yr, 0, 1)
    du = T.U - cx + n1 * 0.12 * y
    larg = largura * (1 - y) ** 0.8 + 0.01
    topo = np.clip(1 - yr - 0.2 * n1 * y, 0, 1) * (yr < 1.3)
    chama = np.exp(-(du / larg) ** 2) * smooth(base + 0.05 - T.V, 0, 0.08) * topo ** 0.6
    nucleo = np.exp(-(du / (larg * 0.45)) ** 2) * smooth(base + 0.05 - T.V, 0, 0.08) * np.clip(1 - yr * 1.7, 0, 1)
    return chama, nucleo


def labareda(T, t, rng):
    """Labareda: uma coluna de fogo explode do chão até o alto e desaba em brasas."""
    G, H = vazio(T)
    sobe = ease_out(rel(t, 0, 0.25), 2)
    env = apaga(t, 0.55, 1)
    c, n = _chama_em(T, t, 401, 0.55, 0.2 + 1.3 * sobe, 0.32)
    c2, n2 = _chama_em(T, t, 402, 0.55, 0.15 + 0.7 * sobe, 0.18, -0.25)
    c3, n3 = _chama_em(T, t, 403, 0.55, 0.15 + 0.75 * sobe, 0.18, 0.25)
    brasas = []
    for _ in range(30):
        f = (rng.uniform(0, 1) + t * 1.6) % 1
        brasas.append((rng.uniform(-0.4, 0.4), 0.5 - f * 1.3, (1 - f) * rng.uniform(0.3, 1)))
    anel = T.ring(0.2 + 0.5 * sobe, 0.04, cy=0.55, squash=3.5) * (1 - t) * 1.3
    G += (np.maximum.reduce([c, c2, c3]) * 2.0 + T.splats(brasas, 0.01) * 1.1) * env + anel
    H += (np.maximum.reduce([n, n2, n3]) * 1.6 + T.splats(brasas, 0.008) * 0.8) * env
    return G, H


def sopro_de_fogo(T, t, rng):
    """Sopro de fogo: um jato em cone vem de trás e envolve o alvo, com fumaça no fim."""
    G, H = vazio(T)
    chega = ease_out(rel(t, 0, 0.3), 2)
    env = apaga(t, 0.55, 1)
    n = np.roll(T.noise(np.random.default_rng(411), 0.06, 3), int(-t * T.W * 0.6), axis=1)
    al, la = T.U, T.V
    alcance = -1 + 1.8 * chega
    cone = np.exp(-(la / (0.06 + 0.32 * np.clip(al + 1, 0, 2) * 0.5 + 0.06 * n)) ** 2) * smooth(alcance - al, -0.05, 0.25) * smooth(al + 1.05, 0, 0.3)
    nucleo = np.exp(-(la / (0.03 + 0.1 * np.clip(al + 1, 0, 2) * 0.5)) ** 2) * smooth(alcance - 0.2 - al, -0.05, 0.25)
    fumo = poeira(T, rng, t, 18, 0.5, -0.1, 0.4, 0.3, 0.05, inicio=0.4)
    G += (cone * (1.2 + 0.5 * np.clip(n, -1, 1)) + nucleo) * env + fumo * 0.5
    H += (nucleo * 1.5 + cone * 0.4) * env
    return G, H


def fenix(T, t, rng):
    """Fênix: duas asas de fogo se abrem do alvo e batem uma vez, com penas de brasa caindo."""
    G, H = vazio(T)
    abre = back(rel(t, 0, 0.35), 1.3)
    bate = 0.15 * math.sin(rel(t, 0.35, 0.8) * math.pi)
    env = apaga(t, 0.6, 1)
    asas, nucleo = T.zero(), T.zero()
    for lado in (-1, 1):
        for k in range(5):
            a = -0.2 - k * 0.22 + bate
            comp = (0.55 + 0.25 * (k == 1)) * abre
            x1, y1 = lado * 0.08, 0.0
            x2, y2 = lado * math.cos(a) * comp, math.sin(a) * comp * 0.9 - 0.05
            asas += T.polys([(lamina(x1, y1, x2, y2, 0.06 + 0.02 * (k < 2)), 1 - 0.12 * k)], 0.01)
            nucleo += T.polys([(lamina(x1, y1, x2 * 0.7, y2 * 0.7, 0.02), 1)], 0.005)
    n = _subindo(T, 421, t, 0.05, 1.2)
    asas = asas * (0.7 + 0.3 * np.clip(n, -1, 1))
    corpo = T.gauss(0, 0.05, 0.08, 0.16) * 1.8
    penas = []
    for _ in range(24):
        f = (rng.uniform(0, 1) + t) % 1
        penas.append((rng.uniform(-0.7, 0.7), -0.3 + f * 0.9, math.sin(math.pi * f) * rng.uniform(0.3, 1)))
    G += (T.glow(asas, 1.2, 1.2, 0.03) + corpo + T.splats(penas, 0.012)) * env
    H += (nucleo * 1.2 + corpo * 0.9) * env
    return G, H


def dragao(T, t, rng):
    """Dragão: um corpo serpenteando chega em espiral, a cabeça morde o alvo e estoura."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.45), 1.6)
    env = apaga(t, 0.6, 1)
    pts = []
    for k in range(60):
        u = k / 59
        s = p - (1 - u) * 0.55
        if s < 0:
            continue
        a = s * 5.5
        r = 0.85 * (1 - s) + 0.05
        pts.append((math.cos(a) * r, math.sin(a) * r * 0.7, u))
    corpo = T.zero()
    for (x1, y1, u1), (x2, y2, u2) in zip(pts, pts[1:]):
        corpo += T.lines([(x1, y1, x2, y2, 1)], 0.02 + 0.07 * u2, 0.01)
    cabeca = T.gauss(pts[-1][0], pts[-1][1], 0.09) * 2 if pts else T.zero()
    tt = rel(t, 0.42, 1)
    estouro = T.gauss(0, 0, 0.18 + 0.15 * tt) * some(t, 0.42, 0.7) * 2.6 + T.ring(0.1 + 0.6 * ease_out(tt, 2), 0.03) * (1 - tt) ** 1.3 * 1.5 * (t > 0.42)
    G += (T.glow(np.clip(corpo, 0, 1.5), 1, 1.2, 0.03) + cabeca) * env + estouro
    H += (np.clip(corpo, 0, 1) * 0.5 + cabeca * 0.8) * env + estouro
    return G, H


def nevasca(T, t, rng):
    """Nevasca: flocos girando num redemoinho largo, véu de frio e geada no chão."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.7, 1)
    flocos = []
    for _ in range(70):
        r0 = rng.uniform(0.1, 0.85)
        a = rng.uniform(0, TAU) + t * (3.2 - 2 * r0)
        flocos.append((math.cos(a) * r0, math.sin(a) * r0 * 0.6 + 0.1 * math.sin(a * 3), rng.uniform(0.3, 1)))
    f = T.splats(flocos, 0.011)
    veu = np.exp(-(T.RAD / 0.38) ** 2) * 0.3 * (0.7 + 0.3 * T.noise(np.random.default_rng(441), 0.08, 2))
    geada = T.ring(0.5, 0.06, cy=0.45, squash=3.5) * 0.8 * janela(t, 0.2, 0.5)
    G += (f * 1.5 + veu + geada) * env
    H += (f * 1.0 + geada * 0.3) * env
    return G, H


def bloco_de_gelo(T, t, rng):
    """Bloco de gelo: um cristal prende o alvo, as faces brilham e rachaduras correm por dentro."""
    G, H = vazio(T)
    sobe = ease_out(rel(t, 0, 0.3), 2.5)
    env = apaga(t, 0.75, 1)
    w, h = 0.42, 0.62 * sobe
    base = 0.55
    pts = [(-w, base), (-w * 1.05, base - h * 0.8), (-w * 0.5, base - h), (w * 0.55, base - h * 0.95), (w, base - h * 0.75), (w * 0.95, base)]
    corpo = T.polys([(pts, 1)], 0.004)
    arestas = T.polyline(pts + [pts[0]], 0.012, 1) + T.lines([(-w * 0.5, base - h, -w * 0.2, base, 0.7), (w * 0.55, base - h * 0.95, w * 0.25, base, 0.7)], 0.008, 0.002)
    sub = np.random.default_rng(451)
    rach = sum(T.polyline(jagged(sub, sub.uniform(-0.3, 0.3), base - 0.1, sub.uniform(-0.3, 0.3), base - h * 0.8, 3, 0.3), 0.006, 1) for _ in range(3)) * janela(t, 0.35, 0.5)
    brilho = T.flare(-w * 0.5, base - h, 0.8, 0.3) * pulso(t, 0.3, 0.6) * 1.6
    G += (corpo * 0.5 + arestas * 1.4 + rach + brilho) * env
    H += (arestas * 0.9 + rach * 0.8 + brilho) * env
    return G, H


def espinho_de_gelo(T, t, rng):
    """Espinho de gelo: lanças de cristal rompem o chão sob o alvo em sequência."""
    G, H = vazio(T)
    env = apaga(t, 0.65, 1)
    sub = np.random.default_rng(461)
    lancas, arestas = [], []
    for k in range(5):
        x = (k - 2) * 0.17 + sub.uniform(-0.04, 0.04)
        h = (0.75 - abs(k - 2) * 0.15) * back(rel(t, 0.04 * k, 0.2 + 0.04 * k), 1.6)
        w = 0.07 + 0.02 * (k == 2)
        incl = (k - 2) * 0.06
        topo = (x + incl * h, 0.5 - h)
        lancas.append(([(x - w, 0.5), topo, (x + w, 0.5)], 1))
        arestas.append((x, 0.5, topo[0], topo[1], 1))
    l = T.polys(lancas, 0.004)
    a = T.lines(arestas, 0.008, 0.002)
    poe = poeira(T, rng, t, 16, 0, 0.5, 0.6, 0.15, 0.03)
    G += (l * 0.9 + a * 1.4 + poe * 0.7) * env
    H += (a * 1.1 + l * 0.3) * env
    return G, H


def tempestade(T, t, rng):
    """Tempestade: uma nuvem escurece o alto e raios grossos descem no alvo, um, dois, três."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.75, 1)
    n = T.noise(np.random.default_rng(471), 0.07, 3)
    nuvem = smooth(0.22 + 0.15 * n - np.abs(T.V + 0.55) * 1.6, 0, 0.15) * smooth(0.7 - np.abs(T.U), 0, 0.25)
    raios = T.zero()
    for k, (a0, x) in enumerate(((0.15, 0.0), (0.38, -0.2), (0.6, 0.18))):
        if a0 <= t < a0 + 0.12:
            sub = np.random.default_rng(int(t * 997) + k)
            pts = jagged(sub, x + sub.uniform(-0.1, 0.1), -0.6, 0, 0.1, 6, 0.22)
            raios += T.polyline(pts, 0.03, 1)
    clarao = sum(T.gauss(0, 0.1, 0.13) * some(t, a0, a0 + 0.15) for a0 in (0.15, 0.38, 0.6)) * 2
    G += (nuvem * 0.9 * (0.6 + 0.4 * np.clip(n, -1, 1)) + T.glow(raios, 1.6, 2, 0.025) + clarao) * env
    H += (raios * 1.6 + clarao) * env
    return G, H


def raio_em_cadeia(T, t, rng):
    """Raio em cadeia: a descarga pula de um ponto a outro, três saltos, com estalo em cada um."""
    G, H = vazio(T)
    nos = [(-0.75, -0.2), (-0.2, 0.25), (0.3, -0.3), (0.7, 0.2)]
    sub = np.random.default_rng(int(t * 997) + 481)
    lin, est = T.zero(), T.zero()
    for k in range(3):
        a0 = k * 0.13
        if t < a0:
            continue
        (x1, y1), (x2, y2) = nos[k], nos[k + 1]
        vida = apaga(t, a0 + 0.2, a0 + 0.55)
        lin += T.polyline(jagged(sub, x1, y1, x2, y2, 5, 0.25), 0.018, 1) * vida
        est += (T.gauss(x2, y2, 0.07) * 2 + T.flare(x2, y2, 0.6, sub.uniform(0, 3))) * some(t, a0 + 0.05, a0 + 0.4)
    G += T.glow(lin, 1.5, 1.8, 0.02) + est
    H += lin * 1.4 + est * 0.9
    return G, H


def _raio_ramificado(T, sub, x0, y0, ang, comp, largura, ramos=2, peso=1.0):
    """Um raio com galhos: o tronco quebrado e um ou dois galhos saindo do meio, mais finos."""
    x1, y1 = x0 + math.cos(ang) * comp, y0 + math.sin(ang) * comp
    pts = jagged(sub, x0, y0, x1, y1, 4, 0.2)
    a = T.polyline(pts, largura, peso).copy()
    for _ in range(ramos):
        k = sub.integers(len(pts) // 4, max(len(pts) // 4 + 1, len(pts) * 3 // 4))
        bx, by = pts[k]
        b = ang + sub.choice((-1, 1)) * sub.uniform(0.4, 0.9)
        c = comp * sub.uniform(0.25, 0.45)
        a += T.polyline(jagged(sub, bx, by, bx + math.cos(b) * c, by + math.sin(b) * c, 3, 0.22), largura * 0.6, peso * 0.7)
    return a


def tsunami(T, t, rng):
    """Tsunami: uma onda alta entra pela esquerda, a crista quebra em espuma sobre o alvo."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.55), 1.8)
    env = apaga(t, 0.65, 1)
    frente = -1.1 + 1.6 * p
    n = np.roll(T.noise(np.random.default_rng(501), 0.05, 3), int(t * 40), axis=1)
    altura = 0.85 * np.exp(-((T.U - frente) / 0.45) ** 2) * smooth(frente + 0.2 - T.U, 0, 0.6) + 0.25 * smooth(frente - T.U, 0, 1)
    agua = smooth(T.V - (0.5 - altura) - 0.04 * n, -0.02, 0.06) * smooth(0.6 - T.V, 0, 0.05)
    crista = np.exp(-((T.V - (0.5 - altura)) / 0.03) ** 2) * smooth(altura, 0.15, 0.5)
    espuma = []
    for _ in range(40):
        x = frente + rng.uniform(-0.25, 0.15)
        y = 0.5 - 0.85 * math.exp(-((x - frente) / 0.45) ** 2) + rng.uniform(-0.08, 0.05)
        espuma.append((x, y, rng.uniform(0.3, 1) * janela(t, 0.2, 0.4)))
    G += (agua * (0.6 + 0.2 * n) + crista * 1.6 + T.splats(espuma, 0.014)) * env
    H += (crista * 1.2 + T.splats(espuma, 0.01) * 0.8) * env
    return G, H


def areia(T, t, rng):
    """Areia: grãos girando e subindo em volta do alvo até fecharem num casulo."""
    G, H = vazio(T)
    fecha = ease_out(rel(t, 0, 0.5), 2)
    env = apaga(t, 0.7, 1)
    graos = []
    for _ in range(120):
        h = rng.uniform(-0.6, 0.5)
        r = (0.75 - 0.4 * fecha) * (1 - 0.3 * abs(h + 0.05)) + rng.uniform(-0.05, 0.05)
        a = rng.uniform(0, TAU) + t * (4 + h)
        graos.append((math.cos(a) * r, h + math.sin(a) * r * 0.15, rng.uniform(0.3, 1) * (0.6 + 0.4 * (math.sin(a) > 0))))
    g = T.splats(graos, 0.008)
    casulo = T.gauss(0, 0, 0.3, 0.45) * fecha * 0.5
    poe = poeira(T, rng, t, 18, 0, 0.5, 0.7, 0.1, 0.04)
    G += (g * 1.6 + casulo + poe * 0.5) * env
    H += g * 0.6 * env
    return G, H


def espinhos_de_terra(T, t, rng):
    """Espinhos de terra: o chão se abre numa linha e pontas de pedra saltam em sequência."""
    G, H = vazio(T)
    env = apaga(t, 0.6, 1)
    sub = np.random.default_rng(521)
    pedras, arestas = [], []
    for k in range(7):
        x = -0.75 + k * 0.25
        a0 = k * 0.05
        h = sub.uniform(0.35, 0.7) * back(rel(t, a0, a0 + 0.18), 1.5)
        w = sub.uniform(0.08, 0.12)
        topo = (x + sub.uniform(-0.05, 0.05), 0.5 - h)
        pedras.append(([(x - w, 0.5), (x - w * 0.4, 0.5 - h * 0.6), topo, (x + w * 0.5, 0.5 - h * 0.5), (x + w, 0.5)], 1))
        arestas.append((x, 0.5, topo[0], topo[1], 0.8))
    p = T.polys(pedras, 0.004)
    a = T.lines(arestas, 0.008, 0.002)
    fenda = np.exp(-((T.V - 0.52) / 0.02) ** 2) * smooth(-1 + 2.2 * rel(t, 0, 0.35) - T.U, 0, 0.1)
    poe = poeira(T, rng, t, 24, 0, 0.5, 0.8, 0.25, 0.035, inicio=0.05)
    G += (p * 0.9 + a * 1.1 + fenda + poe * 0.7) * env
    H += (a * 0.8 + fenda * 0.5) * env
    return G, H


def metal(T, t, rng):
    """Metal: chapas se dobram e fecham em volta do alvo, com estalos e reflexos."""
    G, H = vazio(T)
    fecha = ease_out(rel(t, 0, 0.35), 2.5)
    env = apaga(t, 0.7, 1)
    chapas, bordas = [], []
    for k in range(6):
        a = TAU * k / 6 + 0.3
        r = 0.8 - 0.42 * fecha
        c, s = math.cos(a), math.sin(a)
        w, h = 0.16, 0.07
        pts = [(c * r - s * w - c * h, s * r + c * w - s * h), (c * r + s * w - c * h, s * r - c * w - s * h), (c * r + s * w + c * h, s * r - c * w + s * h), (c * r - s * w + c * h, s * r + c * w + s * h)]
        chapas.append((pts, 0.7))
        bordas.append((pts[0][0], pts[0][1], pts[1][0], pts[1][1], 1))
    ch = T.polys(chapas, 0.003)
    bo = T.lines(bordas, 0.01, 0.002)
    reflexo = sum(T.flare(math.cos(TAU * k / 6 + 0.3) * 0.38, math.sin(TAU * k / 6 + 0.3) * 0.38, 0.5, 0.5) * pulso(t, 0.35 + 0.03 * k, 0.6 + 0.03 * k) for k in range(6))
    clang = T.ring(0.2 + 0.4 * rel(t, 0.35, 0.8), 0.015) * pulso(t, 0.35, 0.8) * 1.3
    G += (ch + bo * 1.3 + reflexo * 1.4) * env + clang
    H += (bo * 0.9 + reflexo) * env + clang * 0.4
    return G, H


def tornado(T, t, rng):
    """Tornado: um funil vertical girando, mais largo no alto, com detritos voando em volta."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.7, 1)
    y = T.V
    larg = 0.08 + 0.3 * np.clip((0.5 - y) / 1.3, 0, 1)
    dentro = smooth(larg - np.abs(T.U), -0.02, 0.04) * smooth(0.55 - y, 0, 0.08) * smooth(y + 0.9, 0, 0.1)
    listras = (0.5 + 0.5 * np.sin(T.U / np.maximum(larg, 0.05) * 3 + y * 12 - t * 30)) ** 2
    funil = dentro * (0.35 + 0.65 * listras)
    detritos = []
    for _ in range(26):
        h = rng.uniform(-0.8, 0.45)
        l = 0.08 + 0.3 * max(0, (0.5 - h) / 1.3) + 0.08
        a = rng.uniform(0, TAU) + t * 9
        detritos.append((math.cos(a) * l, h + math.sin(a) * 0.04, rng.uniform(0.4, 1) * (math.sin(a) > -0.3)))
    G += (funil * 1.3 + T.splats(detritos, 0.014) * 1.1) * env
    H += (funil * listras * 0.4) * env
    return G, H


def rajada_de_ar(T, t, rng):
    """Rajada de ar: arcos de vento em cone empurram o alvo para trás, com folhas carregadas."""
    G, H = vazio(T)
    env = apaga(t, 0.6, 1)
    arcos = T.zero()
    for k in range(5):
        u = rel(t, k * 0.07, 0.5 + k * 0.07)
        if 0 < u < 1:
            arcos += T.arc_band(0.25 + 0.5 * u, 0.05, -0.7, 0.7, cx=-0.6 + 0.6 * u, crescente=True) * math.sin(math.pi * u)
    folhas = []
    for _ in range(14):
        f = (rng.uniform(0, 1) + t * 1.3) % 1
        folhas.append((-0.8 + 1.6 * f, rng.uniform(-0.4, 0.4) + 0.08 * math.sin(f * 12), math.sin(math.pi * f) * rng.uniform(0.4, 1)))
    G += (arcos * 1.4 + T.splats(folhas, 0.015)) * env
    H += arcos * 0.6 * env
    return G, H


def vinhas(T, t, rng):
    """Vinhas: ramos brotam do chão, enrolam o alvo em espiral e soltam folhas."""
    G, H = vazio(T)
    cresce = ease_out(rel(t, 0, 0.5), 1.8)
    env = apaga(t, 0.75, 1)
    ramos, folhas = T.zero(), []
    for k in range(3):
        fase = TAU * k / 3
        pts = []
        for j in range(50):
            u = j / 49 * cresce
            y = 0.55 - u * 1.2
            r = 0.28 + 0.05 * math.sin(u * 7)
            a = fase + u * 9
            pts.append((math.cos(a) * r, y + math.sin(a) * 0.05))
            if j % 12 == 6 and u > 0:
                folhas.append((math.cos(a) * (r + 0.06), y, 1))
        ramos += T.polyline(pts, 0.022, 1)
    f = T.splats(folhas, 0.03)
    G += (T.glow(ramos, 1, 1, 0.02) + f * 1.3) * env
    H += (ramos * 0.4 + f * 0.6) * env
    return G, H


def petalas(T, t, rng):
    """Pétalas: uma flor abre no alvo e as pétalas se soltam num redemoinho."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.3), 2)
    env = apaga(t, 0.7, 1)
    flor = T.zero()
    for k in range(6):
        a = TAU * k / 6 + t * 0.5
        cx, cy = math.cos(a) * 0.18 * abre, math.sin(a) * 0.18 * abre
        al, la = girado(T, a, cx, cy)
        flor += np.exp(-((al / 0.16) ** 2 + (la / 0.07) ** 2)) * (1 - rel(t, 0.35, 0.7))
    voam = []
    for _ in range(36):
        a0 = rng.uniform(0, TAU)
        u = rel(t, 0.3 + rng.uniform(0, 0.2), 1)
        r = 0.15 + 0.7 * u
        a = a0 + u * 3
        voam.append((math.cos(a) * r, math.sin(a) * r * 0.7 - 0.2 * u, (1 - u) * (u > 0) * rng.uniform(0.5, 1)))
    G += (flor * 1.4 + T.splats(voam, 0.016) * 1.3 + T.gauss(0, 0, 0.06) * abre * 1.5) * env
    H += (flor * 0.5 + T.gauss(0, 0, 0.05) * abre) * env
    return G, H


def enxame(T, t, rng):
    """Enxame: dezenas de pontinhos zumbindo em nuvem, envolvendo o alvo e se espalhando."""
    G, H = vazio(T)
    env = janela(t, 0, 0.1) * apaga(t, 0.7, 1)
    pts = []
    for k in range(70):
        f = rng.uniform(0, TAU)
        r = rng.uniform(0.1, 0.55) * (1 + 0.5 * rel(t, 0.6, 1))
        w = rng.uniform(4, 9)
        x = math.cos(f + t * w) * r + 0.03 * math.sin(t * 60 + k)
        y = math.sin(f * 1.3 + t * w * 0.8) * r * 0.7 + 0.03 * math.cos(t * 55 + k)
        pts.append((x, y, rng.uniform(0.5, 1)))
    G += T.splats(pts, 0.012) * 1.8 * env
    H += T.splats(pts, 0.008) * 0.6 * env
    return G, H


def acido(T, t, rng):
    """Ácido: um respingo grosso que escorre em gotas pesadas e borbulha corroendo."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    tt = rel(t, 0, 1)
    sub = np.random.default_rng(531)
    campo = T.gauss(0, -0.05, 0.25 * ease_out(rel(t, 0, 0.2), 2) + 0.01)
    for _ in range(7):
        x = sub.uniform(-0.3, 0.3)
        y = 0.05 + 0.6 * ease_in(rel(t, 0.15, 0.9), 1.6) * sub.uniform(0.5, 1)
        campo += T.gauss(x, y, 0.05) + T.gauss(x, (y + 0.05) / 2, 0.025, abs(y) * 0.3 + 0.01) * 0.6
    mancha = smooth(campo, 0.4, 0.55)
    bolhas = sum(T.ring(0.03, 0.008, sub.uniform(-0.2, 0.2), sub.uniform(-0.2, 0.1)) * pulso((tt * 3 + k * 0.3) % 1, 0, 1) for k in range(6))
    G += (mancha * 1.1 + bolhas * 1.2) * env
    H += (mancha * (1 - smooth(campo, 0.6, 1.0)) * 0.6 + bolhas * 0.5) * env
    return G, H


def sangue(T, t, rng):
    """Sangue: um respingo em coroa, gotas grossas em arco e um fio escorrendo."""
    G, H = vazio(T)
    env = apaga(t, 0.65, 1)
    tt = rel(t, 0, 1)
    gotas = []
    for _ in range(30):
        a = rng.uniform(-math.pi, 0) if rng.uniform() < 0.7 else rng.uniform(0, math.pi)
        v = rng.uniform(0.3, 0.8)
        x = math.cos(a) * v * ease_out(tt, 2)
        y = math.sin(a) * v * ease_out(tt, 2) + 0.9 * tt * tt
        gotas.append((x, y, (1 - tt * 0.6) * rng.uniform(0.5, 1)))
    g = T.splats(gotas, 0.022)
    mancha = smooth(T.gauss(0, 0, 0.18 * ease_out(rel(t, 0, 0.15), 2) + 0.01), 0.4, 0.6)
    fio = np.exp(-(T.U / 0.02) ** 2) * smooth(T.V, -0.05, 0.05) * smooth(0.6 * rel(t, 0.2, 0.9) - T.V, 0, 0.05)
    G += (g * 1.4 + mancha * 1.1 + fio) * env
    H += (g * 0.3 + mancha * 0.4) * env
    return G, H


def radiacao(T, t, rng):
    """Radiação: brilho doentio pulsando, o símbolo de três pás girando e partículas subindo."""
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.7, 1)
    pulsa = 0.8 + 0.2 * math.sin(t * 25)
    giro = t * 2
    pas = (np.cos(3 * (T.ANG - giro)) > 0.5).astype(np.float32) * smooth(T.RAD, 0.14, 0.18) * smooth(0.5 - T.RAD, 0, 0.04)
    centro = smooth(0.09 - T.RAD, -0.01, 0.01)
    aro = T.ring(0.58, 0.02)
    halo = T.gauss(0, 0, 0.3) * 0.5 * pulsa
    sobe = []
    for _ in range(26):
        f = (rng.uniform(0, 1) + t * 1.2) % 1
        sobe.append((rng.uniform(-0.6, 0.6), 0.5 - f * 1.2, math.sin(math.pi * f) * rng.uniform(0.3, 1)))
    G += (T.glow(pas + centro + aro, 1.2, 1, 0.02) * pulsa + halo + T.splats(sobe, 0.012)) * env
    H += ((pas + centro) * 0.6 * pulsa + T.splats(sobe, 0.008) * 0.6) * env
    return G, H


def lua(T, t, rng):
    """Lua: uma meia-lua grande se acende sobre o alvo, com halo frio e estrelas em volta."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.35), 2)
    env = apaga(t, 0.7, 1)
    r = 0.42 * abre + 0.01
    disco = smooth(r - np.hypot(T.U, T.V + 0.05), -0.01, 0.02)
    sombra = smooth(r * 0.92 - np.hypot(T.U - r * 0.45, T.V + 0.05 - r * 0.1), -0.01, 0.02)
    crescente = disco * (1 - sombra)
    halo = T.ring(r * 1.25, 0.06, cy=-0.05) * 0.6 + T.gauss(0, -0.05, r * 0.85 + 0.01) * 0.3
    sub = np.random.default_rng(541)
    est = sum(T.flare(sub.uniform(-0.8, 0.8), sub.uniform(-0.8, 0.8), 0.25, 0.4) * pulso((t * 2 + sub.uniform(0, 1)) % 1, 0, 1) for _ in range(9))
    G += (crescente * 1.6 + halo + est) * env
    H += (crescente * 1.2 + est * 0.8) * env
    return G, H


def raio_divino(T, t, rng):
    """Raio divino: um feixe estreito e afiado desce do céu, o chão se acende num círculo."""
    G, H = vazio(T)
    desce = ease_out(rel(t, 0.05, 0.2), 2)
    env = apaga(t, 0.6, 1)
    feixe = np.exp(-(T.U / (0.05 + 0.02 * math.sin(t * 50))) ** 2) * smooth(-1 + 1.5 * desce - T.V, -0.05, 0.05) * smooth(0.5 - T.V, 0, 0.05)
    nucleo = np.exp(-(T.U / 0.015) ** 2) * smooth(-1 + 1.5 * desce - T.V, -0.05, 0.05) * smooth(0.5 - T.V, 0, 0.05)
    aviso = np.exp(-(T.U / 0.008) ** 2) * janela(t, 0, 0.05) * (t < 0.15) * 0.8
    circulo = (T.ring(0.38, 0.02, cy=0.48, squash=3.5) + T.ring(0.25, 0.012, cy=0.48, squash=3.5)) * janela(t, 0.15, 0.25) * 1.4
    fa = faiscas(T, rng, t, 22, 0.7, 0.03, cone=(-math.pi + 0.3, -0.3), cy=0.45, inicio=0.2)
    G += (feixe * 1.5 + nucleo * 1.5 + circulo) * env + aviso + fa
    H += (nucleo * 2 + circulo * 0.5) * env + aviso
    return G, H


def rugido(T, t, rng):
    """Rugido: ondas de som em cone empurram o alvo, a imagem treme entre elas."""
    G, H = vazio(T)
    env = apaga(t, 0.65, 1)
    ondas = T.zero()
    for k in range(6):
        u = (t * 1.6 + k / 6) % 1
        ondas += T.arc_band(0.15 + 0.85 * u, 0.025 + 0.02 * u, -0.6, 0.6, cx=-0.75, crescente=True) * math.sin(math.pi * u)
    treme = 0.03 * math.sin(t * 60)
    clarao = T.gauss(-0.75, 0, 0.12) * 1.2
    G += (T.warp(ondas, treme, 0) * 1.6 + clarao) * env * janela(t, 0, 0.1)
    H += ondas * 0.4 * env
    return G, H


REGISTRO = [
    ("labareda", labareda, GRANDE, "coluna de fogo", False),
    ("sopro_de_fogo", sopro_de_fogo, GRANDE, "jato de fogo em cone", False),
    ("fenix", fenix, GRANDE, "asas de fogo", False),
    ("dragao", dragao, GRANDE, "dragão serpenteando", False),
    ("nevasca", nevasca, GRANDE, "flocos em redemoinho", False),
    ("bloco_de_gelo", bloco_de_gelo, GRANDE, "bloco de gelo prendendo", False),
    ("espinho_de_gelo", espinho_de_gelo, GRANDE, "lanças de gelo do chão", False),
    ("tempestade", tempestade, GRANDE, "nuvem e raios de cima", False),
    ("raio_em_cadeia", raio_em_cadeia, GRANDE, "raio pulando em cadeia", False),
    ("tsunami", tsunami, GRANDE, "onda gigante", False),
    ("areia", areia, GRANDE, "casulo de areia", False),
    ("espinhos_de_terra", espinhos_de_terra, GRANDE, "pontas de pedra em linha", False),
    ("metal", metal, GRANDE, "chapas de metal fechando", False),
    ("tornado", tornado, GRANDE, "funil de tornado", False),
    ("rajada_de_ar", rajada_de_ar, GRANDE, "arcos de vento", False),
    ("vinhas", vinhas, GRANDE, "vinhas enrolando", False),
    ("petalas", petalas, GRANDE, "flor e pétalas", False),
    ("enxame", enxame, GRANDE, "enxame zumbindo", False),
    ("acido", acido, GRANDE, "respingo de ácido", False),
    ("sangue", sangue, GRANDE, "respingo de sangue", False),
    ("radiacao", radiacao, GRANDE, "radiação pulsando", False),
    ("lua", lua, GRANDE, "meia-lua acesa", False),
    ("raio_divino", raio_divino, GRANDE, "feixe do céu", False),
    ("rugido", rugido, GRANDE, "ondas de som em cone", False),
]
