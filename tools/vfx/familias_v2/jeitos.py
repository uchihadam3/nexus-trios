"""Os jeitos de bater: o que o ataque básico faz além do golpe.

Pedido do jogador: "o ataque básico também ter uma animação própria que faça
sentido… e as mecânicas especiais do básico". Cada folha mostra a mecânica:
o golpe que quica no segundo rival (Ricochete), a varrida que pega dois
(Golpe largo), o golpe final da série com os três pontos do combo, a força do
golpe que vira cura no aliado, a Carga arrancada do rival e a que chega em quem
roubou, os cacos do golpe que viram escudo (Guarda do golpe) e o vulto de quem
acelera depois de bater.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.26, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.4
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.6 * k + 0.01, ang=ang + math.pi / 2, thin=0.012)) * k * 1.5
    return g, h


def _disco(cx, cy, r, giro):
    """Disco que gira: aro com três dentes (o escudo, a lâmina, o bumerangue)."""
    pts = []
    for k in range(18):
        a = giro + k / 18 * TAU
        rr = r * (1.0 if k % 6 else 1.25)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.8))
    return pts


# ------------------------------------------------------------------ Ricochete
def quique(T, t, rng):
    """Ricochete: o golpe vem quicando de fora (rastro em V com os vultos do disco), acerta o
    segundo rival com estalo e anel, e o resto da força espirra para cima em faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    # caminho: entra pelo alto à esquerda, desce até o centro (o quique)
    chega = ease_in(rel(t, 0.0, 0.34), 1.3)
    def caminho(u):
        x = -0.95 + 0.95 * u
        y = -0.75 + 0.75 * u + 0.25 * math.sin(math.pi * u)
        return x, y
    px, py = caminho(chega)
    vultos = []
    for k in range(5):
        u = chega - 0.08 * (k + 1)
        if u > 0:
            vx, vy = caminho(u)
            vultos.append((_disco(vx, vy, 0.09, -t * 30 - k), 0.5 * (1 - k / 5)))
    voo = 1 - rel(t, 0.32, 0.36)
    D = T.polys([(_disco(px, py, 0.1, -t * 30), 1.0)], 0.004) * voo
    V = T.polys(vultos, 0.01) * voo
    trilha = T.polyline([caminho(u / 20 * chega) for u in range(21)], 0.016) * janela(t, 0.04, 0.1) * (1 - rel(t, 0.3, 0.6))
    # o quique: estrela de impacto, anel e marca em V (entrada e saída)
    k = pulso(t, 0.32, 0.62)
    g, h = _clarao(T, k, 0, 0, 0.24, 0.75)
    est = T.polys([(estrela(0, 0, 0.3 * k + 0.01, 0.25, 7, 0.38), 1.0)], 0.006) * k
    anel = T.ring(0.1 + 0.55 * ease_out(rel(t, 0.33, 0.75), 2.2), 0.035) * pulso(t, 0.33, 0.8)
    sai = ease_out(rel(t, 0.36, 0.8), 2)
    saida = T.polys([(lamina(0.0, 0.0, 0.1 + 0.75 * sai, -0.1 - 0.7 * sai, 0.05, 1.0, rel(t, 0.5, 0.85)), 1.0)], 0.01) * pulso(t, 0.34, 0.9)
    sub = np.random.default_rng(41)
    fa = []
    for _ in range(16):
        a = sub.uniform(-1.45, -0.35)
        d = 0.15 + 0.7 * ease_out(rel(t, 0.34, 0.85), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a), d * math.sin(a) + 0.25 * rel(t, 0.4, 1) ** 2, pulso(t, 0.34, 0.95) * sub.uniform(0.5, 1)))
    F = T.splats(fa, 0.013)
    G += (D * 1.3 + V * 0.9 + T.blur(trilha, 0.012) * 1.2 + est * 1.2 + anel + saida * 1.2 + F * 1.6 + g) * env
    H += (D * 0.7 + V * 0.3 + trilha * 0.6 + est * 0.9 + anel * 0.4 + saida * 0.8 + F + h) * env
    return G, H


# ------------------------------------------------------------------ Golpe largo
def _meia_lua(cx, cy, rx, ry, a0, a1, larg, n=40):
    """Faixa em arco de elipse de a0 (cauda, fina) até a1 (cabeça, grossa e arredondada)."""
    fora, dentro = [], []
    for k in range(n + 1):
        u = k / n
        a = a0 + (a1 - a0) * u
        w = larg * (u ** 0.9) * (1 - 0.15 * u)
        fora.append((cx + (rx + w) * math.cos(a), cy + (ry + w * 0.7) * math.sin(a)))
        dentro.append((cx + (rx - w * 0.5) * math.cos(a), cy + (ry - w * 0.35) * math.sin(a)))
    return fora + dentro[::-1]


def golpe_largo(T, t, rng):
    """Golpe largo: uma varrida enorme de lado a lado (meia-lua grossa com linhas de
    velocidade), dois clarões onde ela pega, e a poeira levantada embaixo."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    # a cabeça anda da direita para a esquerda por cima do alvo; a cauda vem atrás e some
    cab = -0.05 - 3.0 * ease_out(rel(t, 0.04, 0.42), 2.0)
    cauda = max(cab + 0.02, -0.05 - 3.0 * ease_in(rel(t, 0.18, 0.7), 1.4) + 0.0) if t > 0.18 else -0.05
    if cauda - cab > 1.8:
        cauda = cab + 1.8
    vivo = 1 - rel(t, 0.6, 0.82)
    A = T.polys([(_meia_lua(0.0, 0.18, 0.82, 0.5, cauda, cab, 0.16), 1.0)], 0.008) * vivo if cauda - cab > 0.05 else T.zero()
    fino = T.polyline([(0.0 + 0.7 * math.cos(cauda + (cab - cauda) * u / 30), 0.18 + 0.4 * math.sin(cauda + (cab - cauda) * u / 30)) for u in range(31)], 0.012) * vivo
    linhas = T.zero()
    for k in range(4):
        rx, ry = 0.95 + 0.06 * k, 0.6 + 0.05 * k
        a1 = cab + 0.35 + 0.1 * k
        a0 = min(cauda, a1 + 0.9)
        if a0 - a1 > 0.08:
            linhas += T.polyline([(rx * math.cos(a0 + (a1 - a0) * u / 20), 0.18 + ry * math.sin(a0 + (a1 - a0) * u / 20)) for u in range(21)], 0.008) * 0.6
    # os dois pontos em que pega: o primeiro rival e o segundo
    k1, k2 = pulso(t, 0.1, 0.38), pulso(t, 0.26, 0.56)
    g1, h1 = _clarao(T, k1, 0.5, -0.12, 0.17, 0.55)
    g2, h2 = _clarao(T, k2, -0.5, -0.12, 0.17, 0.55)
    sub = np.random.default_rng(57)
    po = []
    for _ in range(12):
        x = sub.uniform(-0.75, 0.75)
        tt = rel(t, 0.15 + 0.2 * (0.75 - x) / 1.5, 1.0)
        po.append((x - 0.15 * tt, 0.6 - 0.22 * ease_out(tt, 2) * sub.uniform(0.3, 1), (1 - tt) ** 1.3 * (tt > 0) * 0.45))
    P = T.blur(T.splats(po, 0.06), 0.03)
    G += (A * 1.3 + T.blur(A, 0.03) * 0.8 + fino * 1.2 + linhas * vivo + g1 + g2 + P * 0.8) * env
    H += (A * 0.6 + fino + linhas * 0.4 * vivo + h1 + h2 + P * 0.15) * env
    return G, H


# ------------------------------------------------------------------ Golpe da série
def golpe_da_serie(T, t, rng):
    """O golpe final da série: três pontos do combo acendem um a um em cima (com três
    estalos rápidos em volta do alvo) e o terceiro solta o golpe grande — clarão, onda
    dupla e linhas de força para fora."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    pontos = T.zero()
    estalos = T.zero()
    pos = [(-0.32, 0.12), (0.3, -0.18), (0.05, 0.3)]
    for i in range(3):
        a0 = 0.02 + 0.1 * i
        acende = janela(t, a0, a0 + 0.04) * (1 - rel(t, 0.6, 0.8))
        pontos += T.polys([(estrela(-0.3 + 0.3 * i, -0.72, 0.075 * (1 + 0.5 * pulso(t, a0, a0 + 0.12)), 0.0, 4, 0.5), 1.0)], 0.004) * acende
        pontos += T.ring(0.07, 0.012, -0.3 + 0.3 * i, -0.72) * 0.6 * (1 - rel(t, 0.6, 0.8))
        kk = pulso(t, a0, a0 + 0.12)
        x, y = pos[i]
        estalos += T.polys([(estrela(x, y, 0.16 * kk + 0.01, 0.4 * i, 5, 0.4), 1.0)], 0.005) * kk
    k = pulso(t, 0.32, 0.72)
    g, h = _clarao(T, k, 0, 0, 0.32, 1.0, 0.0)
    est = T.polys([(estrela(0, 0, 0.42 * k + 0.01, 0.0, 8, 0.32), 1.0)], 0.006) * k
    on1 = T.ring(0.12 + 0.75 * ease_out(rel(t, 0.33, 0.8), 2.2), 0.05) * pulso(t, 0.33, 0.85) * 1.2
    on2 = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.42, 0.85), 2.2), 0.03) * pulso(t, 0.42, 0.9)
    sub = np.random.default_rng(73)
    segs = []
    for j in range(16):
        a = j / 16 * TAU + sub.uniform(-0.1, 0.1)
        d0 = 0.2 + 0.5 * ease_out(rel(t, 0.34, 0.7), 2)
        d1 = d0 + 0.25 * sub.uniform(0.6, 1)
        segs.append((d0 * math.cos(a), d0 * math.sin(a), d1 * math.cos(a), d1 * math.sin(a), 1.0))
    L = T.tapered(segs, 0.02) * pulso(t, 0.34, 0.78)
    G += (pontos * 1.2 + estalos * 1.2 + est * 1.3 + on1 + on2 + L * 1.3 + g) * env
    H += (pontos * 0.8 + estalos * 0.8 + est + on1 * 0.4 + on2 * 0.3 + L * 0.9 + h) * env
    return G, H


# ------------------------------------------------------------------ Golpe que cura
def golpe_que_cura(T, t, rng):
    """Golpe que cura: a força do golpe chega no aliado como uma fita de luz que serpenteia
    da esquerda, entra no peito e abre numa cruz suave, com pétalas e bolhas subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corre = ease_out(rel(t, 0.0, 0.4), 1.6)
    pts = []
    for k in range(40):
        u = k / 39 * corre
        x = -0.98 + 0.98 * u
        y = 0.22 * math.sin(u * 7.5) * (1 - u)
        pts.append((x, y))
    fita = T.polyline(pts, 0.022) * (1 - rel(t, 0.38, 0.6))
    cauda = rel(t, 0.25, 0.5)
    fita *= 1.0 if cauda <= 0 else 1.0 - cauda * 0.6
    cab = T.gauss(pts[-1][0], pts[-1][1], 0.06, 0.06) * janela(t, 0.0, 0.05) * (1 - rel(t, 0.4, 0.5)) * 2
    k = pulso(t, 0.38, 0.85)
    abre = ease_out(rel(t, 0.38, 0.6), 2)
    b, c = 0.08 * abre + 0.005, 0.3 * abre + 0.01
    cruz = T.polys([([(-b, -c), (b, -c), (b, -b), (c, -b), (c, b), (b, b), (b, c), (-b, c), (-b, b), (-c, b), (-c, -b), (-b, -b)], 1.0)], 0.01) * k
    petalas = []
    for j in range(6):
        a = j / 6 * TAU + t * 3
        r = 0.42 * abre
        petalas.append((lamina(0.1 * math.cos(a), 0.1 * math.sin(a), r * math.cos(a), r * math.sin(a), 0.05), 0.7))
    Pe = T.polys(petalas, 0.012) * k
    halo = T.ring(0.15 + 0.4 * abre, 0.06) * k * 0.7
    sub = np.random.default_rng(23)
    bol = []
    for _ in range(14):
        x = sub.uniform(-0.5, 0.5)
        tt = rel(t, 0.45 + sub.uniform(0, 0.15), 1.0)
        bol.append((x + 0.05 * math.sin(tt * 9 + x * 5), 0.3 - 0.9 * tt, pulso(tt, 0.0, 1.0) * sub.uniform(0.5, 1)))
    B = T.splats(bol, 0.02)
    G += (T.blur(fita, 0.015) * 1.3 + fita * 0.8 + cab + cruz * 1.3 + Pe + halo + B * 1.4) * env
    H += (fita * 1.1 + cab * 1.3 + cruz * 1.1 + Pe * 0.5 + halo * 0.3 + B * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Roubar Carga
def roubar_carga(T, t, rng):
    """Roubou Carga: as quatro barras de energia do rival se esvaziam de cima para baixo,
    e a energia sai dele em contas que giram em espiral e são puxadas para fora pela direita."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    aparece = janela(t, 0.0, 0.08) * (1 - rel(t, 0.7, 0.85))
    barras = T.zero()
    cheio = T.zero()
    for i in range(4):
        x = -0.27 + 0.18 * i
        borda = [(x - 0.06, -0.34), (x + 0.06, -0.34), (x + 0.06, 0.34), (x - 0.06, 0.34)]
        barras += T.polyline(borda + [borda[0]], 0.01)
        nivel = 1 - ease_in(rel(t, 0.12 + 0.06 * i, 0.45 + 0.06 * i), 1.4)
        topo = 0.3 - 0.6 * nivel
        if nivel > 0.02:
            cheio += T.polys([([(x - 0.04, topo), (x + 0.04, topo), (x + 0.04, 0.3), (x - 0.04, 0.3)], 1.0)], 0.004)
    sub = np.random.default_rng(97)
    contas = []
    for j in range(18):
        a0 = sub.uniform(0.12, 0.55)
        tt = rel(t, a0, a0 + 0.35)
        if 0 < tt < 1:
            ang = sub.uniform(0, TAU) + tt * 5
            r = 0.15 + 0.35 * tt
            x = r * math.cos(ang) + 1.1 * ease_in(tt, 2.2)
            y = r * math.sin(ang) * 0.7 - 0.1 * tt
            contas.append((x, y, (1 - tt * 0.5)))
    C = T.splats(contas, 0.025)
    puxa = T.zero()
    for j in range(5):
        y0 = -0.3 + 0.15 * j
        a0 = 0.15 + 0.07 * j
        u = rel(t, a0, a0 + 0.35)
        if 0 < u < 1:
            puxa += T.polys([(lamina(0.0 + 0.6 * u, y0 * (1 - u), 0.35 + 0.65 * u, y0 * (1 - u) * 0.6, 0.02, 1.0), 1.0)], 0.006) * math.sin(math.pi * u)
    G += (barras * 0.8 * aparece + cheio * 1.3 * aparece + C * 1.6 + puxa * 1.2) * env
    H += (barras * 0.4 * aparece + cheio * 0.9 * aparece + C * 1.1 + puxa * 0.7) * env
    return G, H


def carga_roubada(T, t, rng):
    """A Carga roubada chega: contas de energia vêm de fora em espiral, caem num anel que
    se fecha como um medidor enchendo e terminam num estalo de "pronto"."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(31)
    contas = []
    for j in range(18):
        a0 = sub.uniform(0.0, 0.35)
        tt = rel(t, a0, a0 + 0.3)
        if 0 < tt < 1:
            ang = sub.uniform(0, TAU) - tt * 4
            r = 0.95 * (1 - ease_in(tt, 1.6)) + 0.2
            contas.append((r * math.cos(ang), r * math.sin(ang), 0.4 + 0.6 * tt))
    C = T.splats(contas, 0.022)
    enche = ease_out(rel(t, 0.15, 0.6), 1.6)
    medidor = T.arc_band(0.42, 0.05, -math.pi / 2, -math.pi / 2 + TAU * enche, taper=0.0) if enche > 0.02 else T.zero()
    trilho = T.ring(0.42, 0.012) * janela(t, 0.05, 0.12) * (1 - rel(t, 0.75, 0.9))
    k = pulso(t, 0.58, 0.85)
    g, h = _clarao(T, k, 0, 0, 0.22, 0.6)
    anel = T.ring(0.42 + 0.3 * ease_out(rel(t, 0.58, 0.85), 2), 0.03) * k
    G += (C * 1.5 + medidor * 1.2 * (1 - rel(t, 0.75, 0.92)) + trilho * 0.6 + g + anel) * env
    H += (C + medidor * 0.8 * (1 - rel(t, 0.75, 0.92)) + trilho * 0.3 + h + anel * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Guarda do golpe
def guarda_do_golpe(T, t, rng):
    """Guarda do golpe: os cacos do golpe voltam girando e se encaixam numa placa sextavada
    na frente de quem bateu; um brilho passa pela placa e ela segura um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    junta = ease_out(rel(t, 0.05, 0.42), 2.4)
    R = 0.42
    cacos = []
    sub = np.random.default_rng(61)
    for j in range(6):
        a = j / 6 * TAU + math.pi / 6
        b = a + TAU / 6
        tri = [(0.0, 0.0), (R * math.cos(a), R * math.sin(a)), (R * math.cos(b), R * math.sin(b))]
        ang_fora = (a + b) / 2
        d = 0.75 * (1 - junta)
        giro = (1 - junta) * sub.uniform(-3, 3)
        cx, cy = math.cos(ang_fora) * d, math.sin(ang_fora) * d
        cacos.append((_gira([(x * 0.92, y * 0.92) for x, y in tri], giro, cx, cy) if d > 0.002 else [(x * 0.92, y * 0.92) for x, y in tri], 1.0))
    placa = T.polys(cacos, 0.004) * janela(t, 0.02, 0.08)
    hexa = [(R * math.cos(j / 6 * TAU + math.pi / 6), R * math.sin(j / 6 * TAU + math.pi / 6)) for j in range(6)]
    borda = T.polyline(hexa + [hexa[0]], 0.022) * janela(t, 0.38, 0.46)
    k = pulso(t, 0.4, 0.62)
    g, h = _clarao(T, k, 0, 0, 0.3, 0.7, 0.0)
    passa = -0.6 + 1.2 * rel(t, 0.5, 0.72)
    brilho = T.polys([([(passa - 0.06, -0.5), (passa + 0.04, -0.5), (passa + 0.14, 0.5), (passa + 0.04, 0.5)], 1.0)], 0.01) * pulso(t, 0.5, 0.74)
    brilho *= np.clip(T.polys([([(x * 0.95, y * 0.95) for x, y in hexa], 1.0)], 0.0), 0, 1)
    G += (placa * 0.55 + borda * 1.3 + T.blur(borda, 0.03) + g + brilho * 1.2) * env
    H += (placa * 0.25 + borda * 0.9 + h + brilho * 1.4) * env
    return G, H


# ------------------------------------------------------------------ Acelera
def acelera(T, t, rng):
    """Acelerou: três setas passam correndo, os vultos de quem bate ficam para trás e o
    ponteiro do relógio dá a volta inteira de uma vez (a próxima ação chega antes)."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    setas = T.zero()
    for i in range(3):
        a0 = 0.04 + 0.07 * i
        u = ease_out(rel(t, a0, a0 + 0.4), 1.8)
        if 0 < u < 1:
            x = -0.85 + 1.5 * u
            chevron = [(x - 0.12, -0.2), (x, -0.2), (x + 0.16, 0.0), (x, 0.2), (x - 0.12, 0.2), (x + 0.04, 0.0)]
            setas += T.polys([(chevron, 1.0)], 0.004) * math.sin(math.pi * u)
    vultos = T.zero()
    for i in range(4):
        x = 0.2 - 0.22 * i - 0.25 * ease_out(rel(t, 0.1, 0.6), 2)
        vultos += T.gauss(x, 0.0, 0.1, 0.22) * (0.7 - 0.15 * i) * pulso(t, 0.08 + 0.04 * i, 0.7 + 0.04 * i)
    giro = -math.pi / 2 + TAU * ease_out(rel(t, 0.15, 0.6), 2.2)
    relogio = T.ring(0.58, 0.014) * janela(t, 0.08, 0.15) * (1 - rel(t, 0.7, 0.88))
    marcas = T.zero()
    for j in range(12):
        a = j / 12 * TAU
        marcas += T.polyline([(0.5 * math.cos(a), 0.5 * math.sin(a)), (0.56 * math.cos(a), 0.56 * math.sin(a))], 0.01)
    marcas *= janela(t, 0.08, 0.15) * (1 - rel(t, 0.7, 0.88))
    ponteiro = T.polys([(lamina(0, 0, 0.5 * math.cos(giro), 0.5 * math.sin(giro), 0.035), 1.0)], 0.004) * (1 - rel(t, 0.7, 0.88)) * janela(t, 0.08, 0.15)
    rastro = T.arc_band(0.38, 0.12, giro - 1.4, giro, taper=1.0) * pulso(t, 0.15, 0.65) * 0.6 if rel(t, 0.15, 0.6) > 0 else T.zero()
    k = pulso(t, 0.55, 0.8)
    g, h = _clarao(T, k, 0, 0, 0.18, 0.5)
    G += (setas * 1.4 + vultos * 0.6 + relogio + marcas * 0.8 + ponteiro * 1.3 + rastro + g) * env
    H += (setas * 0.9 + vultos * 0.15 + relogio * 0.5 + marcas * 0.4 + ponteiro + rastro * 0.4 + h) * env
    return G, H


REGISTRO = [
    ("quique", quique, GRANDE, "Ricochete: o golpe quica e acerta o segundo rival", False),
    ("golpe_largo", golpe_largo, GRANDE, "Golpe largo: varrida que pega dois", False),
    ("golpe_da_serie", golpe_da_serie, GRANDE, "Série: os três pontos do combo e o golpe final", False),
    ("golpe_que_cura", golpe_que_cura, GRANDE, "Golpe que cura: a força do golpe vira cura no aliado", False),
    ("roubar_carga", roubar_carga, GRANDE, "Roubou Carga: a energia sai do rival", False),
    ("carga_roubada", carga_roubada, GRANDE, "A Carga roubada enche a habilidade de quem roubou", False),
    ("guarda_do_golpe", guarda_do_golpe, GRANDE, "Guarda do golpe: os cacos viram placa de escudo", False),
    ("acelera", acelera, GRANDE, "Acelerou: setas, vultos e o relógio que dá a volta", False),
]
