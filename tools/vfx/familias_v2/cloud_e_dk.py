"""As três habilidades do Cloud e do Donkey Kong, desenhadas para eles.

Pedido do jogador: "faz as três habilidades do Cloud e as três do Donkey Kong…
sempre verifica se é de perto, de longe, se é projétil… o Donkey Kong taca o
barril direitinho… os efeitos sonoros, tudo muito perfeito".

Cloud
- golpe_ascendente: a Buster Sword sobe de baixo para cima num arco largo, com o
  rastro em meia-lua e os estilhaços subindo (de perto).
- guarda_buster: a espada de pé na frente dele, bloqueando, com o brilho da
  guarda e as faíscas do bloqueio (nele).
- contra_buster: o contra-ataque: o corte horizontal pesado no rival.
- limite_cloud: a aura do Limite subindo nele no Preparo do Omnislash (laço).
- omnislash: a chuva de cortes de todos os lados, cada vez mais rápida, e o
  corte final de cima para baixo que estoura.

Donkey Kong
- soco_giratorio: o braço gira (a espiral de vento) e o punho gigante acerta,
  levantando o pó do chão (de perto).
- barril_voando: o barril de madeira girando no ar, com os aros de ferro (laço).
- barril_quebrando: o barril se espatifa no rival — tábuas, aros e lascas voando.
- batida_preparo: o chão tremendo enquanto ele prepara a batida (laço).
- batida_do_gorila: a batida no chão: as rachaduras correm, as ondas de choque
  achatadas se espalham pelo chão e as pedras sobem (uma vez, no meio dos rivais).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


# =================================================================== Cloud
def _buster(comp=0.95, larg=0.13):
    """A Buster Sword deitada em +x: a lâmina larga e reta, a ponta chanfrada e o cabo."""
    lam = [(0.0, -larg / 2), (comp * 0.86, -larg / 2), (comp, -larg * 0.05), (comp, larg * 0.15), (comp * 0.9, larg / 2), (0.0, larg / 2)]
    guarda = [(-0.02, -larg * 0.7), (0.03, -larg * 0.7), (0.03, larg * 0.7), (-0.02, larg * 0.7)]
    cabo = [(-0.2, -larg * 0.18), (-0.02, -larg * 0.18), (-0.02, larg * 0.18), (-0.2, larg * 0.18)]
    return lam, guarda, cabo


def _espada(T, ang, cx, cy, esc=1.0, w=1.0):
    lam, guarda, cabo = _buster()
    f = lambda q: _gira([(x * esc, y * esc) for x, y in q], ang, cx, cy)
    S = T.polys([(f(lam), 1.0 * w), (f(guarda), 0.8 * w), (f(cabo), 0.6 * w)], 0.004)
    # os dois furos perto do cabo e o fio da lâmina
    furos = sum(T.gauss(*f([(0.12 + 0.07 * k, 0.0)])[0], 0.012) for k in range(2))
    fio = T.polyline(f([(0.05, -0.065), (0.8, -0.065)]), 0.008) * w
    return np.clip(S - furos * 1.2, 0, None), fio


def golpe_ascendente(T, t, rng):
    """A Buster Sword sobe de baixo (esquerda) para cima (direita) num arco largo: o rastro em meia-lua
    acompanha a lâmina, o clarão no meio do arco e os estilhaços de energia subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    u = ease_out(rel(t, 0.05, 0.38), 2.2)
    # a lâmina gira em volta das mãos (embaixo, à esquerda): de baixo-esquerda, passando pela esquerda e
    # por cima, até cima-direita
    px, py = -0.1, 0.35
    theta = 0.75 * math.pi + math.pi * u
    vis = pulso(t, 0.0, 0.55)
    S, fio = _espada(T, theta, px, py, 0.9)
    G += (S * 1.2 + fio * 0.6) * vis * env
    H += (S * 0.4 + fio * 0.9) * vis * env
    if u > 0.02:
        rastro = T.arc_band(0.72, 0.16, 0.75 * math.pi, theta, cx=px, cy=py, crescente=True) * (1 - rel(t, 0.4, 0.7))
        G += rastro * 1.2 * env
        H += rastro * 0.5 * env
    k = pulso(t, 0.2, 0.5)
    G += (T.gauss(0, 0, 0.2) * k * 1.6 + T.flare(0.1, -0.1, 1.1 * k + 1e-3, 0.8, 0.012)) * env
    H += T.gauss(0, 0, 0.1) * k * 1.4 * env
    sub = np.random.default_rng(101)
    cacos = []
    for _ in range(16):
        x0 = sub.normal(0.1, 0.25)
        f = rel(t, 0.22 + 0.15 * sub.uniform(), 0.95)
        cacos.append((estrela(x0 + 0.2 * f, 0.1 - 0.9 * ease_out(f, 1.6), 0.03, sub.uniform(0, TAU), 4, 0.35), pulso(f, 0.0, 1.0) * sub.uniform(0.5, 1)))
    C = T.polys(cacos, 0.003)
    G += C * 1.2 * env
    H += C * 0.5 * env
    return G, H


def guarda_buster(T, t, rng):
    """A guarda do Cloud: a Buster Sword de pé na frente dele, um brilho de escudo em volta da lâmina e
    as faíscas do bloqueio estalando."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.92) ** 0.5
    sobe = back(rel(t, 0.0, 0.2), 1.5)
    S, fio = _espada(T, -math.pi / 2, 0.12, 0.55 - 0.05 * sobe, 0.95 * sobe + 0.01)
    brilho = T.ring(0.55, 0.05, cx=0.12, squash=0.6) * (0.5 + 0.5 * math.sin(TAU * t * 3)) * pulso(t, 0.1, 0.9)
    k = pulso(t, 0.3, 0.55)
    sub = np.random.default_rng(111)
    fa = []
    for _ in range(14):
        a = sub.uniform(-1.2, 1.2) + math.pi
        d = 0.05 + 0.45 * ease_out(rel(t, 0.3, 0.7), 2) * sub.uniform(0.5, 1)
        fa.append((0.12 + d * math.cos(a), -0.1 + d * math.sin(a), pulso(t, 0.3, 0.75) * sub.uniform(0.5, 1)))
    G += (S * 1.2 + fio * 0.6 + brilho + T.flare(0.12, -0.1, 0.9 * k + 1e-3, 0.4, 0.012) + T.splats(fa, 0.012) * 1.3) * env
    H += (S * 0.4 + fio * 0.9 + T.flare(0.12, -0.1, 0.9 * k + 1e-3, 0.4, 0.012) * 0.8 + T.splats(fa, 0.008) * 0.8) * env
    return G, H


def contra_buster(T, t, rng):
    """O contra-ataque do Cloud: a Buster Sword corta deitada, da esquerda para a direita, num rastro largo;
    o clarão, as faíscas e a poeira que o golpe levanta."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2.4)
    S, fio = _espada(T, 0.15, -0.95 + 1.4 * u, 0.05, 0.8)
    vis = 1 - rel(t, 0.35, 0.55)
    corte = T.polys([(lamina(-0.95, 0.12, 0.95, -0.08, 0.075, prog=u, inicio=rel(t, 0.3, 0.7)), 1.0)], 0.005)
    k = pulso(t, 0.15, 0.45)
    sub = np.random.default_rng(121)
    fa = []
    for _ in range(18):
        a = sub.normal(-0.2, 0.6)
        d = 0.1 + 0.7 * ease_out(rel(t, 0.15, 0.75), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.15, 0.8) * sub.uniform(0.4, 1)))
    G += ((S * 1.1 + fio * 0.5) * vis + corte * 1.3 + T.blur(corte, 0.02) * 0.6 + T.gauss(0, 0, 0.2) * k * 1.5 + T.splats(fa, 0.012) * 1.2) * env
    H += ((S * 0.3 + fio * 0.8) * vis + corte * 0.9 + T.gauss(0, 0, 0.1) * k * 1.3 + T.splats(fa, 0.008) * 0.7) * env
    return G, H


def limite_cloud(T, t, rng):
    """A aura do Limite no Cloud: riscos de energia subindo em volta dele, o anel brilhando no chão e
    os pontos de luz que sobem."""
    G, H = vazio(T)
    sub = np.random.default_rng(131)
    riscos = []
    for _ in range(16):
        x = sub.normal(0, 0.3)
        f = (sub.uniform() + t) % 1
        y0 = 0.55 - 1.2 * f
        riscos.append((x, y0 + 0.25, x, y0, math.sin(math.pi * f) * sub.uniform(0.5, 1)))
    R = T.tapered(riscos, 0.025)
    anel = T.ring(0.42, 0.04, cy=0.55, squash=3.0) * (0.7 + 0.3 * math.sin(TAU * t * 2))
    ps = []
    for _ in range(18):
        f = (sub.uniform() + t * 0.7) % 1
        ps.append((sub.normal(0, 0.35), 0.5 - 1.1 * f, math.sin(math.pi * f) * sub.uniform(0.4, 1)))
    G += R * 1.1 + T.blur(R, 0.02) * 0.6 + anel + T.splats(ps, 0.012)
    H += R * 0.6 + anel * 0.3 + T.splats(ps, 0.008) * 0.6
    return G, H


def omnislash(T, t, rng):
    """Omnislash: o Cloud corta de todos os lados — cortes compridos cruzando o rival, um atrás do outro
    e cada vez mais rápidos, cada um deixando um clarão onde ele aparece — e o corte final de cima
    para baixo estoura em luz e estilhaços."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sub = np.random.default_rng(141)
    n = 12
    for j in range(n):
        t0 = 0.6 * (j / n) ** 0.8
        dur = 0.12
        a = sub.uniform(0, math.pi)
        u = ease_out(rel(t, t0, t0 + dur * 0.6), 2)
        some = rel(t, t0 + dur * 0.5, t0 + dur * 1.6)
        if u <= 0 or some >= 1:
            continue
        x1, y1 = -0.85 * math.cos(a), -0.85 * math.sin(a)
        x2, y2 = -x1, -y1
        corte = T.polys([(lamina(x1, y1, x2, y2, 0.035, prog=u, inicio=some), 1.0)], 0.004)
        G += (corte * 1.3 + T.gauss(x1 * 0.9, y1 * 0.9, 0.06) * pulso(t, t0, t0 + dur) * 1.2) * env
        H += corte * 0.9 * env
    # o corte final, de cima para baixo
    u = ease_in(rel(t, 0.66, 0.76), 1.6)
    final = T.polys([(lamina(0.05, -0.95, -0.05, 0.95, 0.08, prog=u, inicio=rel(t, 0.78, 0.95)), 1.0)], 0.005)
    k = pulso(t, 0.74, 0.95)
    estouro = T.gauss(0, 0, 0.3) * k * 1.8 + T.ring(0.12 + 0.75 * ease_out(rel(t, 0.74, 1.0), 2), 0.04) * k
    cacos = []
    for _ in range(18):
        a = sub.uniform(0, TAU)
        d = 0.15 + 0.7 * ease_out(rel(t, 0.75, 1.0), 2) * sub.uniform(0.5, 1)
        cacos.append((estrela(d * math.cos(a), d * math.sin(a), 0.03, a, 4, 0.35), k * sub.uniform(0.5, 1)))
    C = T.polys(cacos, 0.003)
    G += (final * 1.4 + T.blur(final, 0.02) * 0.7 + estouro + C * 1.2) * env
    H += (final * 1.0 + estouro * 0.9 + C * 0.5) * env
    return G, H


# =================================================================== Donkey Kong
def _punho_dk(cx, cy, esc):
    """O punho do gorila, grande e redondo, os nós dos dedos para +x."""
    pts = [(-0.32, -0.2), (0.05, -0.26), (0.18, -0.24), (0.27, -0.16), (0.31, -0.06), (0.32, 0.04), (0.29, 0.14),
           (0.2, 0.22), (0.05, 0.25), (-0.12, 0.27), (-0.28, 0.22), (-0.36, 0.08)]
    return [(cx + x * esc, cy + y * esc) for x, y in pts]


def soco_giratorio(T, t, rng):
    """O soco giratório do Donkey Kong: o braço gira (a espiral de vento cresce atrás), o punho gigante
    entra e acerta — estrela do impacto, anel, e o pó subindo do chão em volta do rival preso."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    # a espiral do braço girando, atrás do punho
    gira = pulso(t, 0.0, 0.35)
    espiral = T.zero()
    if gira > 0:
        for b in range(2):
            pts = [(-0.6 + (0.1 + 0.25 * u) * math.cos(TAU * 1.5 * u + TAU * t * 3 + math.pi * b), (0.1 + 0.25 * u) * math.sin(TAU * 1.5 * u + TAU * t * 3 + math.pi * b)) for u in np.linspace(0, 1, 30)]
            espiral += T.polyline(pts, 0.02)
        espiral *= gira
    vem = ease_in(rel(t, 0.12, 0.28), 2)
    px = -0.6 + 0.55 * vem
    vis = 1 - rel(t, 0.3, 0.46)
    P = T.polys([(_punho_dk(px, 0.0, 1.3), 1.0)], 0.005) * vis
    vincos = sum(T.polyline([(px + 0.18, y), (px + 0.36, y)], 0.014) for y in (-0.12, -0.02, 0.08)) * vis
    P = np.clip(P - vincos, 0, None)
    k = pulso(t, 0.26, 0.6)
    est = T.polys([(estrela(0.15, 0, 0.42 * k + 0.01, 0.3, 8, 0.4), 1.0)], 0.005) * k
    anel = T.ring(0.15 + 0.65 * ease_out(rel(t, 0.26, 0.7), 2), 0.045) * pulso(t, 0.26, 0.75)
    sub = np.random.default_rng(151)
    po = []
    for _ in range(20):
        x0 = sub.normal(0, 0.35)
        f = rel(t, 0.3 + 0.2 * sub.uniform(), 1.0)
        po.append((x0 * (1 + 0.6 * f), 0.55 - 0.3 * f, pulso(f, 0.0, 1.0) * sub.uniform(0.5, 1)))
    Po = T.splats(po, 0.05)
    G += (espiral * 1.0 + T.blur(espiral, 0.03) * 0.6 + P * 1.2 + T.blur(P, 0.03) * 0.5 + est * 1.2 + anel + Po * 0.7) * env
    H += (espiral * 0.4 + P * 0.5 + est * 0.9 + anel * 0.3) * env
    return G, H


def _barril(ang, cx=0.0, cy=0.0, esc=1.0):
    """O barril visto de lado: o corpo abaulado, os dois aros e as tábuas."""
    corpo = []
    for k in range(25):
        u = k / 24
        corpo.append((-0.24 + 0.48 * u, -0.17 - 0.035 * math.sin(math.pi * u)))
    for k in range(25):
        u = 1 - k / 24
        corpo.append((-0.24 + 0.48 * u, 0.17 + 0.035 * math.sin(math.pi * u)))
    f = lambda q: _gira([(x * esc, y * esc) for x, y in q], ang, cx, cy)
    aros = [f([(x, -0.21), (x, 0.21)]) for x in (-0.13, 0.13)]
    tabuas = [f([(-0.24, y), (0.24, y)]) for y in (-0.07, 0.07)]
    return f(corpo), aros, tabuas


def barril_voando(T, t, rng):
    """O barril do Donkey Kong voando e girando, com os aros de ferro e as tábuas, e as linhas de
    velocidade atrás."""
    G, H = vazio(T)
    ang = TAU * t
    corpo, aros, tabuas = _barril(ang, 0.3, 0.0, 1.35)
    C = T.polys([(corpo, 1.0)], 0.004)
    A = sum(T.polyline(a, 0.03) for a in aros)
    Tb = sum(T.polyline(tb, 0.008) for tb in tabuas)
    linhas = T.tapered([(-0.8, y, -0.05, y * 0.7, 0.8) for y in (-0.15, 0.0, 0.15)], 0.025)
    G += np.clip(C * 1.0 - Tb * 0.6, 0, None) + A * 1.2 + linhas * 0.6
    H += A * 0.6 + C * 0.1
    return G, H


def barril_quebrando(T, t, rng):
    """O barril chega girando e se espatifa no rival: as tábuas voam girando para todo lado, os aros
    se abrem e caem, lascas e a nuvem de pó."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    chega = ease_in(rel(t, 0.0, 0.12), 1.4)
    if t < 0.14:
        corpo, aros, _ = _barril(TAU * t * 2, -0.8 + 0.8 * chega, 0, 1.3)
        G += (T.polys([(corpo, 1.0)], 0.004) + sum(T.polyline(a, 0.03) for a in aros)) * env
    k = pulso(t, 0.12, 0.42)
    G += (T.gauss(0, 0, 0.22) * k * 1.4 + T.polys([(estrela(0, 0, 0.36 * k + 0.01, 0.2, 9, 0.4), 1.0)], 0.005) * k) * env
    H += T.gauss(0, 0, 0.1) * k * 1.2 * env
    sub = np.random.default_rng(161)
    tabuas = []
    for _ in range(8):
        a = sub.uniform(0, TAU)
        f = ease_out(rel(t, 0.12, 0.9), 1.8)
        d = 0.75 * f * sub.uniform(0.6, 1)
        x, y = d * math.cos(a), d * math.sin(a) + 0.5 * rel(t, 0.3, 1.0) ** 2
        rot = a + TAU * 1.5 * f * sub.choice([-1, 1])
        tabuas.append((_gira([(-0.13, -0.03), (0.13, -0.035), (0.13, 0.035), (-0.13, 0.03)], rot, x, y), pulso(t, 0.12, 0.95)))
    Tb = T.polys(tabuas, 0.004)
    aros = T.zero()
    for j, s in enumerate((-1, 1)):
        f = ease_out(rel(t, 0.12, 0.8), 2)
        aros += T.arc_band(0.18 + 0.2 * f, 0.025, -1.2 + s, 1.0 + s, cx=s * 0.25 * f, cy=0.3 * rel(t, 0.3, 1.0) ** 2) * pulso(t, 0.12, 0.85)
    lascas = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.85 * ease_out(rel(t, 0.12, 0.7), 2) * sub.uniform(0.3, 1)
        lascas.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.12, 0.75) * sub.uniform(0.4, 1)))
    po = T.splats([(sub.normal(0, 0.25), sub.normal(0.1, 0.15) - 0.2 * rel(t, 0.3, 1.0), 0.7) for _ in range(12)], 0.07) * pulso(t, 0.2, 1.0)
    G += (Tb * 1.2 + aros * 1.1 + T.splats(lascas, 0.01) * 1.1 + po * 0.6) * env
    H += (Tb * 0.25 + aros * 0.6 + T.splats(lascas, 0.006) * 0.5) * env
    return G, H


def batida_preparo(T, t, rng):
    """O Donkey Kong prepara a batida: anéis achatados batendo no chão, o pó pulando e o tremor."""
    G, H = vazio(T)
    bate = (t * 2) % 1
    an = T.ring(0.2 + 0.5 * ease_out(bate, 2), 0.035, cy=0.5, squash=3.2) * (1 - bate)
    sub = np.random.default_rng(171)
    po = []
    for _ in range(14):
        x = sub.normal(0, 0.35)
        f = (sub.uniform() + t * 2) % 1
        po.append((x, 0.5 - 0.25 * math.sin(math.pi * f), (1 - f) * sub.uniform(0.4, 1)))
    G += an * 1.2 + T.splats(po, 0.035) * 0.8
    H += an * 0.4
    return G, H


def batida_do_gorila(T, t, rng):
    """A batida do gorila no chão, no meio dos rivais: o clarão do impacto, as rachaduras correndo pelo
    chão, três ondas de choque achatadas se espalhando, as pedras subindo e caindo e a poeira."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chao = 0.18
    k = pulso(t, 0.0, 0.3)
    G += (T.gauss(0, chao, 0.3, 0.12) * k * 1.8 + T.polys([(estrela(0, chao, 0.4 * k + 0.01, 0.0, 10, 0.3, 0.45), 1.0)], 0.005) * k) * env
    H += T.gauss(0, chao, 0.15, 0.06) * k * 1.4 * env
    sub = np.random.default_rng(181)
    # rachaduras correndo pelo chão
    rach = T.zero()
    cresce = ease_out(rel(t, 0.02, 0.4), 2)
    for j in range(8):
        a = math.pi * (j + 0.5) / 8 * 2
        comp = 0.9 * cresce * sub.uniform(0.6, 1)
        q = np.random.default_rng(190 + j)
        rach += T.polyline(jagged(q, 0, chao, comp * math.cos(a), chao + comp * math.sin(a) * 0.35, 4, 0.3), 0.014)
    rach *= 1 - rel(t, 0.65, 0.95)
    ondas = sum(T.ring(0.1 + 0.85 * ease_out(rel(t, 0.04 + 0.1 * j, 0.7 + 0.08 * j), 2), 0.04, cy=chao, squash=2.8) * pulso(t, 0.04 + 0.1 * j, 0.78 + 0.08 * j) for j in range(3))
    pedras = []
    for _ in range(12):
        a = sub.uniform(-math.pi * 0.9, -math.pi * 0.1)
        v = sub.uniform(0.6, 1.1)
        f = rel(t, 0.05, 0.9)
        x = math.cos(a) * v * f * 0.8
        y = chao + math.sin(a) * v * f * 1.2 + 1.6 * f * f
        r = sub.uniform(0.03, 0.06)
        pedras.append((estrela(x, min(y, 0.9), r, sub.uniform(0, TAU) + f * 6, 4, 0.75), pulso(t, 0.05, 0.9)))
    Pd = T.polys(pedras, 0.003)
    po = T.splats([(sub.normal(0, 0.45), chao - 0.1 - 0.25 * rel(t, 0.2, 1.0) + sub.normal(0, 0.05), 0.8) for _ in range(16)], 0.08) * pulso(t, 0.15, 1.0)
    G += (rach * 1.3 + T.blur(rach, 0.015) * 0.6 + ondas * 1.1 + Pd * 1.2 + po * 0.6) * env
    H += (rach * 0.8 + ondas * 0.35 + Pd * 0.3) * env
    return G, H


REGISTRO = [
    ("golpe_ascendente", golpe_ascendente, GRANDE, "Cloud · Golpe ascendente: a Buster Sword sobe num arco", False),
    ("guarda_buster", guarda_buster, MEDIA, "Cloud · a guarda com a Buster Sword de pé (nele)", False),
    ("contra_buster", contra_buster, GRANDE, "Cloud · o contra-ataque: corte horizontal pesado", False),
    ("limite_cloud", limite_cloud, MEDIA, "Cloud · a aura do Limite no Preparo (laço)", True),
    ("omnislash", omnislash, GRANDE, "Cloud · Omnislash: os cortes de todos os lados e o final", False),
    ("soco_giratorio", soco_giratorio, GRANDE, "Donkey Kong · Soco giratório: o braço gira e o punho gigante acerta", False),
    ("barril_voando", barril_voando, MEDIA, "Donkey Kong · o barril girando no ar (laço)", True),
    ("barril_quebrando", barril_quebrando, GRANDE, "Donkey Kong · o barril se espatifando no rival", False),
    ("batida_preparo", batida_preparo, MEDIA, "Donkey Kong · o chão tremendo no Preparo (laço)", True),
    ("batida_do_gorila", batida_do_gorila, GRANDE, "Donkey Kong · Batida do gorila: rachaduras, ondas e pedras", False),
]
