"""Elementos com variações: fogo, gelo, raio, água, terra, ar, natureza, sangue, lua, som."""
from __future__ import annotations

import math

import numpy as np

from .base import (FAIXA, GRANDE, TAU, _subindo, apaga, back, ease_in, ease_out, faiscas, girado, jagged, janela,
                   poeira, pulso, rel, smooth, some, vazio)


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


REGISTRO = [
    ("bloco_de_gelo", bloco_de_gelo, GRANDE, "bloco de gelo prendendo", False),
    ("areia", areia, GRANDE, "casulo de areia", False),
    ("espinhos_de_terra", espinhos_de_terra, GRANDE, "pontas de pedra em linha", False),
    ("metal", metal, GRANDE, "chapas de metal fechando", False),
    ("rajada_de_ar", rajada_de_ar, GRANDE, "arcos de vento", False),
    ("enxame", enxame, GRANDE, "enxame zumbindo", False),
    ("acido", acido, GRANDE, "respingo de ácido", False),
    ("sangue", sangue, GRANDE, "respingo de sangue", False),
    ("radiacao", radiacao, GRANDE, "radiação pulsando", False),
]
