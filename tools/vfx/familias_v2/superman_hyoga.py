"""As habilidades do Super-Homem e do Hyoga, desenhadas para eles.

Super-Homem
- olhos_brilhando: os dois olhos acendendo no Preparo da Visão de calor (laço).
- calor_faixa: os dois raios finos e paralelos saindo dos olhos até o rival,
  tremendo, com o ar quente em volta (faixa, laço).
- calor_impacto: o ponto queimando no rival, derretendo, com fumaça subindo e
  gotas de metal quente.
- eu_te_seguro: ele chega voando (o risco que desce), os braços fecham em volta
  do aliado e a bolha de proteção acende.
- krypton_carga: a luz do sol amarelo juntando nele — os raios girando e o
  brilho crescendo (Preparo, laço).
- ultimo_filho: o soco supersônico — os cones do estrondo sônico, o clarão, a
  onda no chão e os destroços.

Hyoga
- diamante_faixa: o Pó de Diamante — o ar gelado correndo do punho dele até o
  rival, com os cristais brilhando e os flocos (faixa, laço).
- diamante_impacto: o gelo cristalizando no rival — as agulhas de gelo
  crescendo, a geada e o brilho.
- aurora_preparo: os braços juntos acima da cabeça (a jarra de Aquário) — o
  círculo de gelo girando e a aurora em volta (Preparo, laço).
- aurora_faixa: a Execução Aurora — o raio largo de frio com as faixas de
  aurora ondulando e os cristais (faixa, laço).
- execucao_aurora: o rival preso num cristal de gelo que cresce de baixo para
  cima, com a geada e o estalo.
- zero_preparo: o frio girando em volta dele, com neve (Preparo, laço).
- zero_absoluto: o campo inteiro congelando — a geada abrindo no chão, as
  estacas de gelo subindo e a neve caindo (no centro dos rivais).
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


_RUIDOS: dict = {}


def _ruido(T, seed, escala=0.05, oitavas=3):
    chave = (T.W, T.H, seed, escala, oitavas)
    if chave not in _RUIDOS:
        _RUIDOS[chave] = T.noise(np.random.default_rng(seed), escala, oitavas)
    return _RUIDOS[chave]


def _floco(cx, cy, r, ang):
    """Um floco de neve: seis braços com dois galhinhos cada (segmentos para T.lines)."""
    segs = []
    for k in range(6):
        a = ang + TAU * k / 6
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        segs.append((cx, cy, ex, ey, 1.0))
        for s in (-1, 1):
            mx, my = cx + 0.55 * r * math.cos(a), cy + 0.55 * r * math.sin(a)
            b = a + s * 0.7
            segs.append((mx, my, mx + 0.3 * r * math.cos(b), my + 0.3 * r * math.sin(b), 1.0))
    return segs


def _cristal(cx, base, larg, alto, ang=0.0):
    """Um cristal de gelo (prisma pontudo) subindo da base."""
    pts = [(-larg, 0), (-larg, -alto * 0.75), (0, -alto), (larg, -alto * 0.75), (larg, 0)]
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, base + x * s + y * c) for x, y in pts]


# =================================================================== Super-Homem
def olhos_brilhando(T, t, rng):
    """Os dois olhos acendendo: dois pontos muito claros lado a lado, com a estrela de brilho de
    cada um crescendo e tremendo."""
    G, H = vazio(T)
    sobe = 0.6 + 0.4 * math.sin(TAU * t * 2) ** 2
    q = _quadro(t, 5)
    for x in (-0.16, 0.16):
        G += (T.gauss(x, 0, 0.05) * 1.6 + T.gauss(x, 0, 0.16) * 0.5 + T.flare(x, 0, 0.7 * sobe + q.uniform(0, 0.08), 0.0, 0.01) * 0.8) * sobe
        H += T.gauss(x, 0, 0.04) * 1.8 * sobe
    return G, H


def calor_faixa(T, t, rng):
    """A Visão de calor: os dois raios finos e paralelos dos olhos até o rival, tremendo de leve, e o
    ar quente ondulando em volta deles."""
    G, H = vazio(T)
    alto = T.H / T.W
    q = _quadro(t, 9)
    R = T.zero()
    for y in (-alto * 0.16, alto * 0.16):
        tremor = q.normal(0, alto * 0.015)
        R += T.lines([(-0.98, y + tremor, 0.98, y * 0.4 + tremor, 1.0)], 0.014)
    n = np.roll(_ruido(T, 11, 0.04, 2), int((t % 1) * T.W), axis=1)
    calor = np.exp(-(T.V / (alto * 0.45)) ** 2) * np.clip(0.5 + 0.35 * n, 0, 1) * 0.35
    G += R * 1.7 + T.blur(R, 0.012) * 1.6 + calor + T.gauss(-0.96, 0, 0.04, alto * 0.4) * 0.8
    H += R * 1.6 + T.blur(R, 0.006) * 0.6
    return G, H


def calor_impacto(T, t, rng):
    """O ponto queimando no rival: o clarão, a mancha incandescente que fica e vai apagando, as gotas
    de metal derretido pingando e a fumaça subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.3)
    clarao = T.gauss(0, 0, 0.2) * k * 1.6 + T.flare(0, 0, 0.9 * k + 1e-3, 0.3, 0.01) * k
    brasa = (T.gauss(0, 0, 0.13, 0.09) * (1 - rel(t, 0.3, 0.9))) * rel(t, 0.02, 0.15)
    sub = np.random.default_rng(21)
    gotas = []
    for _ in range(14):
        x = sub.normal(0, 0.08)
        ini = sub.uniform(0.05, 0.4)
        f = rel(t, ini, ini + 0.5)
        gotas.append((x + 0.15 * f * sub.normal(), 0.05 + 0.6 * f * f, pulso(t, ini, ini + 0.5) * sub.uniform(0.5, 1)))
    n = np.roll(_ruido(T, 23, 0.05, 2), -int((t * 0.8 % 1) * T.H), axis=0)
    coluna = np.exp(-(T.U / (0.12 + 0.15 * np.clip(-T.V, 0, 1))) ** 2) * (T.V < 0) * np.clip(1 + T.V / 0.9, 0, 1)
    fumaca = np.clip(coluna * (0.7 + 0.5 * n), 0, 1) * pulso(t, 0.2, 1.0) * 0.45
    G += (clarao + brasa * 1.5 + T.splats(gotas, 0.014) * 1.1 + fumaca) * env
    H += (clarao * 1.1 + brasa * 1.6 + T.splats(gotas, 0.008) * 0.6) * env
    return G, H


def eu_te_seguro(T, t, rng):
    """Eu te seguro: o Super-Homem chega voando (o risco claro descendo do alto à esquerda), os dois
    braços fecham em volta do aliado como um abraço e a bolha de proteção acende e fica."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    f = ease_in(rel(t, 0.0, 0.25), 1.6)
    hx, hy = -0.95 + 0.95 * f, -0.95 + 0.95 * f
    risco = T.tapered([(hx - 0.6, hy - 0.6, hx + 1e-3, hy, 1.0)], 0.16) * (1 - rel(t, 0.25, 0.4))
    cabeca = T.gauss(hx, hy, 0.08) * (1 - rel(t, 0.25, 0.35))
    fecha = ease_out(rel(t, 0.2, 0.45), 2.2)
    bracos = T.zero()
    if fecha > 0:
        bracos += T.arc_band(0.5, 0.05, math.pi * 1.05, math.pi * (1.05 + 0.55 * fecha), 1.0, 0.0)
        bracos += T.arc_band(0.5, 0.05, -math.pi * 0.05, -math.pi * (0.05 + 0.55 * fecha), 1.0, 0.0)
    bracos *= 1 - rel(t, 0.5, 0.7)
    k = pulso(t, 0.4, 0.75)
    clarao = T.gauss(0, 0, 0.25) * k * 1.0 + T.flare(-0.3, -0.45, 0.8 * k + 1e-3, 0.0, 0.01) * k
    bolha = (T.ring(0.62, 0.04) * 1.1 + np.clip(1 - T.RAD / 0.62, 0, 1) ** 0.5 * (T.RAD < 0.62) * 0.18) * rel(t, 0.4, 0.55)
    reflexo = T.arc_band(0.5, 0.03, math.pi * 1.1, math.pi * 1.4, 1.0, 0.0) * rel(t, 0.45, 0.6)
    respira = 0.85 + 0.15 * math.sin(TAU * t * 3)
    G += (risco * 1.2 + cabeca * 1.4 + bracos * 1.3 + clarao + (bolha + reflexo * 0.9) * respira) * env
    H += (risco * 0.7 + cabeca * 1.2 + bracos * 0.5 + clarao * 0.8 + reflexo * 0.8) * env
    return G, H


def krypton_carga(T, t, rng):
    """A luz do sol amarelo juntando no Super-Homem: os raios de sol girando devagar em volta dele, o
    brilho crescendo e as partículas de luz entrando."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 3)
    nucleo = T.gauss(0, 0, 0.22 * pul)
    raios = T.zero()
    for j in range(12):
        a = TAU * j / 12 + t * TAU / 6
        comp = 0.7 + 0.15 * math.sin(TAU * (t * 2 + j / 3))
        raios += T.tapered([(comp * math.cos(a), comp * math.sin(a), 0.15 * math.cos(a), 0.15 * math.sin(a), 1.0)], 0.07)
    sub = np.random.default_rng(31)
    pts = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t * 1.5) % 1
        r = 0.9 * (1 - f) + 0.15
        pts.append((r * math.cos(a), r * math.sin(a), f * sub.uniform(0.4, 1)))
    G += nucleo * 1.4 + T.blur(raios, 0.012) * 0.8 + T.splats(pts, 0.013) + T.ring(0.3, 0.06) * 0.3 * pul
    H += nucleo * 1.4 + raios * 0.2
    return G, H


def ultimo_filho(T, t, rng):
    """O soco do Último filho de Krypton (vem de −x, muito rápido): os cones do estrondo sônico em
    volta do punho, o clarão do golpe, a onda achatada no chão e os destroços voando."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    chega = ease_in(rel(t, 0.0, 0.16), 1.3)
    px = -0.7 + 0.7 * chega
    cones = T.zero()
    for j in range(4):
        x = px - 0.12 - 0.18 * j
        ry = 0.12 + 0.1 * j
        cones += T.arc_band(ry, 0.02, -1.3, 1.3, 1 / 0.45, 0.0, x + ry * 0.45, 0, 1.0, True) * (1 - 0.18 * j)
    cones *= 1 - rel(t, 0.2, 0.42)
    linhas = T.tapered([(px - 0.9, y, px - 0.15, y * 0.5, 1.0) for y in (-0.25, -0.12, 0.12, 0.25)], 0.02) * (1 - rel(t, 0.16, 0.3))
    punho = T.gauss(px, 0, 0.09) * (1 - rel(t, 0.15, 0.3))
    k = pulso(t, 0.1, 0.5)
    clarao = T.gauss(0, 0, 0.3) * k * 2.0 + T.flare(0, 0, 1.5 * k + 1e-3, 0.0, 0.009) * k
    onda = T.ring(0.15 + 0.85 * ease_out(rel(t, 0.12, 0.6), 2), 0.05, 0, 0.4, 3.5) * pulso(t, 0.12, 0.7)
    estrondo = T.ring(0.1 + 0.8 * ease_out(rel(t, 0.1, 0.45), 2.5), 0.03) * pulso(t, 0.1, 0.5)
    sub = np.random.default_rng(41)
    pedras = []
    for _ in range(18):
        a = sub.normal(0, 0.7)
        d = 0.1 + 0.85 * ease_out(rel(t, 0.12, 0.85), 2) * sub.uniform(0.3, 1)
        pedras.append((d * math.cos(a), d * math.sin(a) + 0.5 * rel(t, 0.35, 1.0) ** 2, pulso(t, 0.12, 0.95) * sub.uniform(0.4, 1)))
    G += (cones * 1.2 + linhas * 0.8 + punho * 1.3 + clarao + onda * 1.1 + estrondo + T.splats(pedras, 0.016) * 1.1) * env
    H += (cones * 0.5 + punho * 1.2 + clarao * 1.1 + onda * 0.4 + T.splats(pedras, 0.01) * 0.4) * env
    return G, H


# =================================================================== Hyoga
def diamante_faixa(T, t, rng):
    """O Pó de Diamante: o ar gelado correndo do punho do Hyoga até o rival (a névoa rolando), os
    cristais brilhando como diamante e os flocos girando dentro."""
    G, H = vazio(T)
    alto = T.H / T.W
    f = (T.U + 1) / 2
    larg = alto * (0.15 + 0.45 * f)
    n = np.roll(_ruido(T, 51, 0.04, 3), int((t % 1) * T.W), axis=1)
    nevoa = np.clip(np.exp(-(T.V / larg) ** 2) * (1.0 + 0.5 * n) - 0.2, 0, 1)
    sub = np.random.default_rng(53)
    brilhos, flocos = [], []
    for _ in range(40):
        ff = (sub.uniform() + t) % 1
        x = -0.98 + 1.96 * ff
        y = sub.normal(0, 0.35) * alto * (0.15 + 0.45 * ff) * 2
        brilhos.append((x, y, sub.uniform(0.5, 1) * (0.5 + 0.5 * math.sin(TAU * (t * 4 + sub.uniform())))))
    for _ in range(9):
        ff = (sub.uniform() + t) % 1
        x = -0.98 + 1.96 * ff
        y = sub.normal(0, 0.25) * alto
        flocos += _floco(x, y, alto * 0.13, t * 4 + sub.uniform(0, TAU))
    B = T.splats(brilhos, 0.006)
    Fl = T.lines(flocos, 0.005)
    G += nevoa * 0.7 + B * 1.6 + T.blur(B, 0.01) * 0.6 + Fl * 1.1 + T.gauss(-0.95, 0, 0.05, alto * 0.3)
    H += B * 1.4 + Fl * 0.7 + nevoa * 0.12
    return G, H


def diamante_impacto(T, t, rng):
    """O gelo cristalizando no rival (vem de −x): o sopro frio batendo, as agulhas de gelo crescendo
    em leque, a geada abrindo e os brilhos de diamante."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.3)
    sopro = T.gauss(-0.2, 0, 0.3, 0.2) * k * 1.0
    cresce = back(rel(t, 0.08, 0.4), 1.2)
    sub = np.random.default_rng(61)
    agulhas = []
    for j in range(9):
        a = math.pi + sub.normal(0, 0.8) + (math.pi if j % 3 == 0 else 0)
        comp = 0.45 * cresce * sub.uniform(0.6, 1)
        larg = 0.035 * sub.uniform(0.7, 1.2)
        if comp < 0.01:
            continue
        c, s = math.cos(a), math.sin(a)
        agulhas.append(([(-s * larg, c * larg), (comp * c, comp * s), (s * larg, -c * larg)], sub.uniform(0.7, 1)))
    A = T.polys(agulhas, 0.003)
    geada = T.ring(0.1 + 0.4 * ease_out(rel(t, 0.05, 0.5), 2), 0.08) * pulso(t, 0.05, 0.8) * 0.4
    brilhos = []
    for _ in range(18):
        a = sub.uniform(0, TAU)
        d = sub.uniform(0.05, 0.5)
        brilhos.append((d * math.cos(a), d * math.sin(a), max(0.0, math.sin(TAU * (t * 2 + sub.uniform()))) * rel(t, 0.2, 0.4)))
    G += (sopro + A * 1.2 + T.blur(A, 0.015) * 0.6 + geada + T.splats(brilhos, 0.008) * 1.5) * env
    H += (A * 0.6 + T.splats(brilhos, 0.005) * 1.2) * env
    return G, H


def aurora_preparo(T, t, rng):
    """Os braços do Hyoga juntos acima da cabeça: o círculo de gelo girando com o floco no meio e as
    faixas da aurora subindo e ondulando em volta."""
    G, H = vazio(T)
    giro = t * TAU / 3
    circ = T.ring(0.38, 0.025) + T.ring(0.3, 0.012) * 0.6
    fl = T.lines(_floco(0, 0, 0.26, giro), 0.012)
    aurora = T.zero()
    for j in range(3):
        a0 = TAU * j / 3 + giro * 1.5
        aurora += T.arc_band(0.6 + 0.05 * j, 0.06, a0, a0 + 2.0, 1.0, 0.0, 0, 0, 1.0, True) * (0.6 + 0.4 * math.sin(TAU * (t * 2 + j / 3)))
    nucleo = T.gauss(0, 0, 0.1) * (0.8 + 0.2 * math.sin(TAU * t * 4))
    G += circ * 1.2 + fl * 1.2 + T.blur(aurora, 0.02) * 1.0 + nucleo * 1.2
    H += circ * 0.5 + fl * 0.6 + nucleo * 1.2
    return G, H


def aurora_faixa(T, t, rng):
    """A Execução Aurora: o raio largo de frio até o rival, com as faixas de aurora ondulando por
    dentro (duas fitas em onda) e os cristais correndo."""
    G, H = vazio(T)
    alto = T.H / T.W
    f = (T.U + 1) / 2
    larg = alto * (0.3 + 0.25 * f)
    corpo = np.exp(-(T.V / larg) ** 2) * np.clip(f / 0.05, 0, 1)
    fitas = T.zero()
    for j in range(3):
        y = alto * 0.35 * np.sin(TAU * (f * 2 - t * 2) + j * 2.1) * (0.4 + 0.6 * f)
        fitas += np.exp(-((T.V - y) / (alto * 0.06)) ** 2) * (0.6 + 0.4 * j / 2)
    nucleo = np.exp(-(T.V / (alto * 0.08)) ** 2)
    sub = np.random.default_rng(71)
    cr = []
    for _ in range(30):
        ff = (sub.uniform() + t * 1.5) % 1
        cr.append((-0.98 + 1.96 * ff, sub.normal(0, 0.3) * alto, sub.uniform(0.5, 1)))
    G += corpo * 0.45 + fitas * corpo * 0.9 + nucleo * 1.2 + T.splats(cr, 0.007) * 1.3
    H += nucleo * 1.3 + fitas * corpo * 0.3 + T.splats(cr, 0.004)
    return G, H


def execucao_aurora(T, t, rng):
    """O rival preso no gelo: o frio bate, o cristal de gelo cresce de baixo para cima e fecha em
    volta dele (as faces do prisma brilhando), a geada no chão e os brilhos; no fim, um estalo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.3)
    sopro = T.gauss(-0.15, 0, 0.32, 0.25) * k
    sobe = ease_out(rel(t, 0.08, 0.5), 2)
    base = 0.62
    formas = [(_cristal(0, base, 0.42, 1.3 * sobe + 1e-3), 0.55),
              (_cristal(-0.42, base, 0.16, 0.8 * sobe + 1e-3, -0.25), 0.8),
              (_cristal(0.42, base, 0.16, 0.85 * sobe + 1e-3, 0.25), 0.8),
              (_cristal(-0.18, base, 0.1, 0.55 * sobe + 1e-3, -0.1), 0.9),
              (_cristal(0.2, base, 0.1, 0.5 * sobe + 1e-3, 0.12), 0.9)]
    C = T.polys(formas, 0.004)
    arestas = T.zero()
    if sobe > 0.05:
        topo = base - 1.3 * sobe
        arestas += T.lines([(-0.42, base, -0.42, base - 0.97 * sobe, 1.0), (0.42, base, 0.42, base - 0.97 * sobe, 1.0),
                            (-0.42, base - 0.97 * sobe, 0, topo, 1.0), (0.42, base - 0.97 * sobe, 0, topo, 1.0),
                            (0.0, base, 0.0, topo, 0.6)], 0.012)
    varre = T.gauss(0, base - 1.3 * rel(t, 0.5, 0.75), 0.5, 0.05) * pulso(t, 0.5, 0.78) * (T.RAD < 0.9)
    geada = T.gauss(0, base, 0.6, 0.06) * rel(t, 0.05, 0.3) * 0.8
    estalo = pulso(t, 0.55, 0.8)
    brilho = T.flare(0.15, -0.3, 0.9 * estalo + 1e-3, 0.4, 0.01) * estalo
    G += (sopro + C * 0.9 + arestas * 1.3 + varre * 1.2 + geada + brilho) * env
    H += (C * 0.25 + arestas * 0.8 + varre * 0.8 + brilho * 0.9) * env
    return G, H


def zero_preparo(T, t, rng):
    """O frio girando em volta do Hyoga: a névoa em redemoinho, os flocos girando e o brilho no
    meio, cada vez mais forte."""
    G, H = vazio(T)
    sub = np.random.default_rng(81)
    pts = []
    for _ in range(50):
        a0 = sub.uniform(0, TAU)
        r = sub.uniform(0.25, 0.8)
        a = a0 + t * TAU * (0.6 / r)
        pts.append((r * math.cos(a), r * math.sin(a) * 0.55, sub.uniform(0.3, 1)))
    N = T.blur(T.splats(pts, 0.03), 0.02)
    flocos = []
    for j in range(5):
        a = TAU * j / 5 + t * TAU
        flocos += _floco(0.6 * math.cos(a), 0.33 * math.sin(a), 0.07, t * 6 + j)
    nucleo = T.gauss(0, 0, 0.15) * (0.8 + 0.2 * math.sin(TAU * t * 3))
    G += N * 1.2 + T.lines(flocos, 0.01) * 1.1 + nucleo * 1.2
    H += nucleo * 1.1 + T.lines(flocos, 0.01) * 0.5
    return G, H


def zero_absoluto(T, t, rng):
    """O Zero Absoluto no campo dos rivais: a geada abrindo no chão (o anel achatado), as estacas de
    gelo subindo uma depois da outra, a névoa branca e a neve caindo; tudo para."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chao = 0.45
    abre = ease_out(rel(t, 0.0, 0.4), 2)
    geada = np.clip(1 - np.hypot(T.U / (0.95 * abre + 1e-3), (T.V - chao) / (0.3 * abre + 1e-3)), 0, 1) ** 0.5 * 0.45
    borda = T.ring(0.95 * abre + 1e-3, 0.03, 0, chao, 3.2) * pulso(t, 0.0, 0.5)
    sub = np.random.default_rng(91)
    formas = []
    for j in range(11):
        x = -0.85 + 1.7 * j / 10 + sub.uniform(-0.04, 0.04)
        ini = 0.1 + 0.25 * abs(x)
        h = back(rel(t, ini, ini + 0.2), 1.3) * sub.uniform(0.35, 0.7) * (1.2 - 0.6 * abs(x))
        if h > 0.01:
            formas.append((_cristal(x, chao + sub.uniform(-0.04, 0.06), 0.06, h, sub.normal(0, 0.12)), sub.uniform(0.7, 1)))
    E = T.polys(formas, 0.004)
    n = np.roll(_ruido(T, 93, 0.06, 2), int((t * 0.5 % 1) * T.W), axis=1)
    nevoa = np.clip(np.exp(-((T.V - chao + 0.15) / 0.3) ** 2) * (0.7 + 0.4 * n), 0, 1) * pulso(t, 0.2, 1.0) * 0.35
    neve = []
    for _ in range(40):
        f = (sub.uniform() + t * 0.6) % 1
        neve.append((sub.uniform(-0.95, 0.95) + 0.05 * math.sin(TAU * (f * 2 + sub.uniform())), -0.9 + 1.4 * f, sub.uniform(0.3, 0.9) * rel(t, 0.15, 0.35)))
    k = pulso(t, 0.45, 0.75)
    brilho = T.flare(-0.3, -0.1, 0.8 * k + 1e-3, 0.3, 0.01) * k + T.flare(0.4, 0.05, 0.6 * k + 1e-3, 0.0, 0.01) * k
    G += (geada + borda * 1.1 + E * 1.1 + T.blur(E, 0.015) * 0.5 + nevoa + T.splats(neve, 0.008) * 1.1 + brilho) * env
    H += (borda * 0.4 + E * 0.4 + T.splats(neve, 0.005) * 0.8 + brilho * 0.9) * env
    return G, H


REGISTRO = [
    ("olhos_brilhando", olhos_brilhando, MEDIA, "Super-Homem · os olhos acendendo no Preparo (laço)", True),
    ("calor_faixa", calor_faixa, FAIXA, "Super-Homem · os dois raios da Visão de calor (faixa)", True),
    ("calor_impacto", calor_impacto, GRANDE, "Super-Homem · o ponto queimando, derretendo e soltando fumaça", False),
    ("eu_te_seguro", eu_te_seguro, GRANDE, "Super-Homem · chega voando, abraça o aliado e a bolha acende", False),
    ("krypton_carga", krypton_carga, MEDIA, "Super-Homem · a luz do sol juntando nele (laço)", True),
    ("ultimo_filho", ultimo_filho, GRANDE, "Super-Homem · o soco supersônico com o estrondo", False),
    ("diamante_faixa", diamante_faixa, FAIXA, "Hyoga · o Pó de Diamante correndo até o rival (faixa)", True),
    ("diamante_impacto", diamante_impacto, GRANDE, "Hyoga · as agulhas de gelo crescendo no rival", False),
    ("aurora_preparo", aurora_preparo, MEDIA, "Hyoga · o círculo de gelo e a aurora acima da cabeça (laço)", True),
    ("aurora_faixa", aurora_faixa, FAIXA, "Hyoga · o raio da Execução Aurora (faixa)", True),
    ("execucao_aurora", execucao_aurora, GRANDE, "Hyoga · o rival preso no cristal de gelo", False),
    ("zero_preparo", zero_preparo, MEDIA, "Hyoga · o frio girando em volta dele (laço)", True),
    ("zero_absoluto", zero_absoluto, GRANDE, "Hyoga · o campo congelando com as estacas de gelo", False),
]
