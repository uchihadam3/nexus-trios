"""As habilidades da Toph (e o ataque básico dela) e do Gon, desenhadas para eles.

Pedido do jogador: "faz as três habilidades da Toph e do Gon… e da Toph faz
também o ataque base dela, com uma skill própria dela… verifica se é perto, de
longe, projétil… os efeitos sonoros muito bem feitos".

Toph
- pedra_bloco: o bloco de pedra arrancado do chão voando e girando, soltando
  terra (laço, viagem) — o ataque básico.
- pedra_estilhaca: o bloco bate no rival e se parte em pedaços, com a poeira.
- pisada_toph: a pisada dela no chão — a onda achatada e as pedrinhas pulando
  (nela, quando usa as técnicas).
- visao_sismica: as ondas da pisada chegam pelo chão até o rival, acendem o
  contorno dele (ela "vê") e a terra sobe e prende os pés.
- pedregulho_toph: a pedra da Muralha de terra voando e esmagando o rival
  (a muralha de espinhos que protege o trio é a espinhos_de_terra, na frente de
  cada aliado — pedido do jogador: "a muralha que ela fazia antes era mais da hora").
- metal_preparo: as placas de metal girando em volta dela no Preparo (laço).
- metal_dobrado: as faixas de metal se enrolam no rival, apertam e esmagam,
  com faíscas.

Gon
- nen_gon: a aura do Gon juntando no punho no Preparo do Jajanken (laço).
- jajanken_pedra: o punho cheio de aura acerta e estoura.
- jajanken_tesoura: a lâmina de aura saindo dos dois dedos, cortando em V.
- papel_bola: a bola de aura voando até o rival (laço, viagem).
- jajanken_papel: a bola de aura explode no rival.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _rocha(cx, cy, r, ang, seed, lados=7):
    """Um pedaço de rocha: polígono irregular."""
    sub = np.random.default_rng(seed)
    pts = []
    for k in range(lados):
        a = TAU * k / lados + sub.uniform(-0.25, 0.25)
        rr = r * sub.uniform(0.7, 1.1)
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return _gira(pts, ang, cx, cy)


def _bloco(cx, cy, esc, ang):
    """O bloco de pedra retangular, com a quina lascada."""
    pts = [(-0.2, -0.15), (0.16, -0.17), (0.21, -0.08), (0.2, 0.15), (-0.18, 0.17), (-0.22, 0.02)]
    return _gira([(x * esc, y * esc) for x, y in pts], ang, cx, cy)


# =================================================================== Toph
def pedra_bloco(T, t, rng):
    """O bloco de pedra da Toph voando e girando, com as rachaduras, a terra soltando atrás e as
    linhas de velocidade."""
    G, H = vazio(T)
    ang = TAU * t
    B = T.polys([(_bloco(0.3, 0.0, 1.4, ang), 1.0)], 0.004)
    rach = T.polyline(_gira([(-0.15, -0.1), (-0.02, 0.0), (0.05, -0.06), (0.15, 0.1)], ang, 0.3, 0.0), 0.012)
    sub = np.random.default_rng(301)
    terra = []
    for _ in range(14):
        f = (sub.uniform() + t * 1.3) % 1
        terra.append((0.1 - 0.85 * f, sub.normal(0, 0.06) + 0.12 * f * f, (1 - f) * sub.uniform(0.5, 1)))
    linhas = T.tapered([(-0.85, y, -0.05, y * 0.7, 0.7) for y in (-0.14, 0.0, 0.14)], 0.02)
    G += np.clip(B - rach * 0.7, 0, None) * 1.1 + T.splats(terra, 0.018) * 0.9 + linhas * 0.5
    H += B * 0.2 + T.splats(terra, 0.01) * 0.3
    return G, H


def pedra_estilhaca(T, t, rng):
    """O bloco bate no rival e se parte: os pedaços de rocha voam girando e caem, as pedrinhas
    espirram, a poeira sobe e a estrela do impacto."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.35)
    G += (T.polys([(estrela(0, 0, 0.38 * k + 0.01, 0.2, 8, 0.4), 1.0)], 0.005) * k * 1.1 + T.gauss(0, 0, 0.18) * k * 1.2) * env
    H += T.gauss(0, 0, 0.09) * k * 1.2 * env
    sub = np.random.default_rng(311)
    pedacos = []
    for j in range(9):
        a = sub.uniform(0, TAU)
        f = ease_out(rel(t, 0.02, 0.9), 1.7)
        d = 0.75 * f * sub.uniform(0.5, 1)
        x, y = d * math.cos(a), d * math.sin(a) + 0.7 * rel(t, 0.25, 1.0) ** 2
        pedacos.append((_rocha(x, y, 0.07 * sub.uniform(0.7, 1.3), a + 5 * f, 320 + j), pulso(t, 0.02, 0.95)))
    P = T.polys(pedacos, 0.003)
    pedrinhas = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.85 * ease_out(rel(t, 0.02, 0.7), 2) * sub.uniform(0.3, 1)
        pedrinhas.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.02, 0.75) * sub.uniform(0.4, 1)))
    po = T.splats([(sub.normal(0, 0.25), sub.normal(0.05, 0.15) - 0.25 * rel(t, 0.2, 1.0), 0.8) for _ in range(12)], 0.07) * pulso(t, 0.1, 1.0)
    G += (P * 1.1 + T.splats(pedrinhas, 0.01) + po * 0.55) * env
    H += (P * 0.2 + T.splats(pedrinhas, 0.006) * 0.4) * env
    return G, H


def pisada_toph(T, t, rng):
    """A pisada da Toph: a onda achatada correndo no chão em volta dela, as rachaduras curtas e as
    pedrinhas pulando."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.9) ** 0.6
    chao = 0.45
    ondas = sum(T.ring(0.08 + 0.75 * ease_out(rel(t, 0.06 * j, 0.7 + 0.06 * j), 2), 0.03, cy=chao, squash=3.0) * pulso(t, 0.06 * j, 0.8 + 0.06 * j) for j in range(2))
    rach = T.zero()
    for j in range(6):
        a = math.pi * j / 5
        q = np.random.default_rng(330 + j)
        comp = 0.5 * ease_out(rel(t, 0.0, 0.3), 2)
        rach += T.polyline(jagged(q, 0, chao, comp * math.cos(a) * (1 if j % 2 else -1), chao + comp * 0.15, 3, 0.3), 0.012)
    sub = np.random.default_rng(341)
    pulos = []
    for _ in range(12):
        x0 = sub.normal(0, 0.35)
        f = rel(t, 0.05 + 0.1 * sub.uniform(), 0.8)
        pulos.append((estrela(x0, chao - 0.5 * math.sin(math.pi * f) * sub.uniform(0.4, 1), 0.025, x0 * 9, 4, 0.7), pulso(f, 0.0, 1.0)))
    G += (ondas * 1.2 + rach * (1 - rel(t, 0.5, 0.9)) + T.polys(pulos, 0.003)) * env
    H += (ondas * 0.4 + rach * 0.5) * env
    return G, H


def visao_sismica(T, t, rng):
    """Visão sísmica: as ondas sísmicas chegam pelo chão (vindo de −x), o contorno do rival acende como
    a Toph o "vê" pelas vibrações, e a terra sobe em volta dos pés dele e prende, com as rachaduras."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chao = 0.5
    ondas = T.zero()
    for j in range(4):
        f = rel(t, 0.05 * j, 0.35 + 0.05 * j)
        x = -1.0 + 1.0 * f
        ondas += T.arc_band(0.16, 0.02, -1.3, 1.3, squash=0.35, cx=x, cy=chao) * pulso(t, 0.05 * j, 0.42 + 0.05 * j)
    # o contorno do rival "visto" pelas vibrações
    ve = pulso(t, 0.3, 0.85)
    contorno = (T.ring(0.3, 0.02, cy=0.05, squash=0.7) + T.ring(0.13, 0.018, cy=-0.38)) * ve * (0.6 + 0.4 * math.sin(TAU * t * 4))
    # a terra sobe em volta dos pés e prende
    sobe = back(rel(t, 0.38, 0.6), 1.5)
    pedras = []
    for j in range(7):
        x = (j - 3) * 0.1
        alt = (0.28 - 0.04 * abs(j - 3)) * sobe
        pedras.append(([(x - 0.06, chao + 0.05), (x - 0.03, chao - alt), (x + 0.02, chao - alt * 1.1), (x + 0.06, chao + 0.05)], 1.0))
    P = T.polys(pedras, 0.004) * (1 - rel(t, 0.85, 1.0))
    rach = T.zero()
    for j in range(5):
        q = np.random.default_rng(350 + j)
        rach += T.polyline(jagged(q, 0, chao, (j - 2) * 0.35, chao + 0.08, 3, 0.25), 0.012)
    rach *= pulso(t, 0.38, 0.95)
    G += (ondas * 1.1 + contorno * 1.1 + P * 1.1 + rach) * env
    H += (ondas * 0.4 + contorno * 0.6 + P * 0.25 + rach * 0.5) * env
    return G, H


def pedregulho_toph(T, t, rng):
    """A pedra da Muralha de terra acertando o rival: o pedregulho chega girando, esmaga com o clarão
    seco, se parte em lascas grandes que voam e caem, e a poeira sobe."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chega = ease_in(rel(t, 0.0, 0.18), 1.6)
    cx, cy = -0.6 + 0.6 * chega, -0.5 + 0.5 * chega
    pedra = [(cx + 0.2 * math.cos(a + t * 6) * (1 + 0.15 * math.sin(3 * a)), cy + 0.18 * math.sin(a + t * 6) * (1 + 0.15 * math.cos(2 * a))) for a in np.linspace(0, TAU, 9)[:-1]]
    bloco = T.polys([(pedra, 1.0)], 0.006) * (1 - rel(t, 0.18, 0.22))
    k = pulso(t, 0.17, 0.45)
    clarao = T.gauss(0, 0, 0.2) * k * 1.4
    sub = np.random.default_rng(91)
    lascas = []
    for _ in range(10):
        a = sub.uniform(-math.pi, 0.2)
        d = (0.1 + 0.6 * ease_out(rel(t, 0.18, 0.6), 2) * sub.uniform(0.5, 1))
        x, y = d * math.cos(a), d * math.sin(a) + 0.5 * rel(t, 0.3, 1.0) ** 2
        r = sub.uniform(0.04, 0.08)
        lascas.append(([(x + r * math.cos(b + t * 5), y + r * math.sin(b + t * 5)) for b in np.linspace(0, TAU, 6)[:-1]], 1.0 * (1 - rel(t, 0.7, 1.0))))
    L = T.polys(lascas, 0.004) * rel(t, 0.18, 0.2)
    poeira = T.splats([(sub.normal(0, 0.3), 0.2 - 0.4 * ease_out(rel(t, 0.2, 0.9), 2) * sub.uniform(0.3, 1), pulso(t, 0.2, 0.95) * sub.uniform(0.3, 0.7)) for _ in range(18)], 0.05)
    G += (bloco * 0.9 + clarao + L * 0.9 + poeira * 0.4) * env
    H += (clarao * 0.8 + bloco * 0.2) * env
    return G, H

def metal_preparo(T, t, rng):
    """As placas de metal girando em volta da Toph no Preparo do Metal dobrado, com o brilho do aço."""
    G, H = vazio(T)
    placas = []
    brilhos = T.zero()
    for j in range(5):
        a = TAU * j / 5 + TAU * t
        x, y = 0.55 * math.cos(a), 0.42 * math.sin(a)
        placas.append((_gira([(-0.09, -0.04), (0.09, -0.05), (0.1, 0.04), (-0.08, 0.05)], a * 2, x, y), 1.0))
        brilhos += T.flare(x, y, 0.25, a, 0.012) * (0.5 + 0.5 * math.sin(TAU * t * 3 + j))
    P = T.polys(placas, 0.003)
    G += P * 1.2 + brilhos * 0.6 + T.ring(0.5, 0.012, squash=1.3) * 0.4
    H += P * 0.6 + brilhos
    return G, H


def metal_dobrado(T, t, rng):
    """Metal dobrado: as faixas de metal chegam girando, se enrolam no rival em espiral, apertam
    (o clarão do esmagamento) e soltam faíscas de metal; o rival fica preso no aço."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    enrola = ease_out(rel(t, 0.0, 0.4), 2)
    aperta = ease_in(rel(t, 0.35, 0.5), 2)
    faixas = T.zero()
    for b in range(3):
        pts = []
        for j in range(40):
            u = j / 39 * enrola
            a = TAU * 2.2 * u + TAU * b / 3
            r = (0.55 - 0.18 * aperta) * (1 - 0.15 * u)
            pts.append((r * math.cos(a), -0.45 + 0.9 * u + 0.12 * math.sin(a) * 0))
            pts[-1] = (r * math.cos(a), -0.4 + 0.85 * (j / 39) * enrola)
        faixas += T.polyline(pts, 0.045)
    k = pulso(t, 0.45, 0.7)
    esmaga = T.gauss(0, 0, 0.22) * k * 1.6 + T.polys([(estrela(0, 0, 0.35 * k + 0.01, 0.3, 10, 0.35), 1.0)], 0.005) * k
    sub = np.random.default_rng(381)
    fa = []
    for _ in range(22):
        a = sub.uniform(0, TAU)
        d = 0.15 + 0.7 * ease_out(rel(t, 0.45, 0.9), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a) * 0.5 - 0.2 + d * 0.9, d * math.sin(a), pulso(t, 0.45, 0.92) * sub.uniform(0.4, 1)))
    brilho = sum(T.flare(0.4 * math.cos(TAU * t + j), 0.3 * math.sin(TAU * t + j), 0.25, 0.4, 0.012) for j in range(3)) * pulso(t, 0.1, 0.9)
    G += (faixas * 1.2 + T.blur(faixas, 0.02) * 0.4 + esmaga + T.splats(fa, 0.01) * 1.2 + brilho * 0.6) * env
    H += (faixas * 0.6 + esmaga * 0.8 + T.splats(fa, 0.006) * 0.7 + brilho) * env
    return G, H


# =================================================================== Gon
def nen_gon(T, t, rng):
    """A aura do Gon juntando no punho: a chama de aura subindo do corpo e afunilando para a mão, o
    punho brilhando cada vez mais ("Jan… ken…")."""
    G, H = vazio(T)
    pul = 0.8 + 0.2 * math.sin(TAU * t * 2)
    sub = np.random.default_rng(401)
    ps = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t) % 1
        d = 0.85 * (1 - f) + 0.08
        ps.append((d * math.cos(a), d * math.sin(a) * 0.9, f * sub.uniform(0.5, 1)))
    punho = T.gauss(0, 0, 0.13 * pul) * 1.5 + T.ring(0.18, 0.03) * 0.8 * pul
    aura = T.ring(0.42, 0.06, squash=0.85) * 0.5 * (0.6 + 0.4 * math.sin(TAU * t * 3))
    G += punho + aura + T.splats(ps, 0.016) * 1.1
    H += T.gauss(0, 0, 0.06) * 1.6 * pul + T.splats(ps, 0.009) * 0.5
    return G, H


def jajanken_pedra(T, t, rng):
    """Jajanken: Pedra — o punho cheio de aura entra (de −x) e acerta: a estrela enorme, o estouro
    da aura em anel, as ondas de choque e as rachaduras de ar."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.15), 1.8)
    px = -0.8 + 0.75 * vem
    vis = 1 - rel(t, 0.18, 0.32)
    punho = (T.gauss(px, 0, 0.13, 0.11) * 1.4 + T.ring(0.16, 0.03, cx=px) + T.tapered([(px - 0.7, 0, px - 0.05, 0, 1.0)], 0.28) * 0.7) * vis
    k = pulso(t, 0.13, 0.48)
    est = T.polys([(estrela(0.05, 0, 0.5 * k + 0.01, 0.15, 10, 0.38), 1.0)], 0.005) * k
    aneis = sum(T.ring(0.12 + 0.75 * ease_out(rel(t, 0.13 + 0.08 * j, 0.75), 2), 0.04 - 0.01 * j) * pulso(t, 0.13 + 0.08 * j, 0.8) for j in range(3))
    sub = np.random.default_rng(411)
    raios = T.tapered([(0.1 * math.cos(a), 0.1 * math.sin(a), (0.3 + 0.6 * ease_out(rel(t, 0.13, 0.6), 2)) * math.cos(a), (0.3 + 0.6 * ease_out(rel(t, 0.13, 0.6), 2)) * math.sin(a), pulso(t, 0.13, 0.65)) for a in [sub.uniform(0, TAU) for _ in range(14)]], 0.03)
    G += (punho + est * 1.3 + aneis + raios + T.gauss(0, 0, 0.25) * k * 1.3) * env
    H += (punho * 0.5 + est * 0.9 + aneis * 0.3 + raios * 0.6) * env
    return G, H


def jajanken_tesoura(T, t, rng):
    """Jajanken: Tesoura — a lâmina de aura sai dos dois dedos e corta duas vezes, em V; as linhas do
    corte brilham e se abrem, com as partículas de aura voando."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cortes = T.zero()
    for j, (x1, y1, x2, y2) in enumerate(((-0.7, -0.6, 0.6, 0.5), (-0.7, 0.6, 0.6, -0.5))):
        t0 = 0.05 + 0.15 * j
        u = ease_out(rel(t, t0, t0 + 0.14), 2.2)
        cortes += T.polys([(lamina(x1, y1, x2, y2, 0.06, prog=u, inicio=rel(t, t0 + 0.2, t0 + 0.6)), 1.0)], 0.004)
        # a lâmina dos dois dedos indo na frente
        if 0 < u < 1:
            bx, by = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
            cortes += T.gauss(bx, by, 0.06) * 1.2
    k = pulso(t, 0.3, 0.6)
    cruz = T.gauss(-0.03, 0.0, 0.2) * k * 1.4
    sub = np.random.default_rng(421)
    ps = []
    for _ in range(20):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.75 * ease_out(rel(t, 0.15, 0.85), 2) * sub.uniform(0.4, 1)
        ps.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.15, 0.88) * sub.uniform(0.4, 1)))
    G += (cortes * 1.3 + T.blur(cortes, 0.02) * 0.7 + cruz + T.splats(ps, 0.012) * 1.1) * env
    H += (cortes * 0.9 + cruz * 0.8 + T.splats(ps, 0.007) * 0.6) * env
    return G, H


def papel_bola(T, t, rng):
    """Jajanken: Papel em voo — a bola de aura com o núcleo branco, as chamas de aura em volta e a
    cauda que se desfaz em faíscas."""
    G, H = vazio(T)
    cx = 0.35
    pul = 1 + 0.08 * math.sin(TAU * t * 3)
    bola = T.gauss(cx, 0, 0.16 * pul) * 1.5 + T.ring(0.2 * pul, 0.035, cx=cx)
    chamas = T.zero()
    for j in range(8):
        a = TAU * j / 8 + TAU * t
        chamas += T.gauss(cx + 0.24 * math.cos(a) - 0.06, 0.24 * math.sin(a), 0.05) * (0.6 + 0.4 * math.sin(TAU * t * 2 + j))
    cauda = T.tapered([(-0.9, 0.0, cx - 0.05, 0.0, 1.0)], 0.3) * 0.8
    sub = np.random.default_rng(431)
    fa = []
    for _ in range(16):
        f = (sub.uniform() + t * 1.4) % 1
        fa.append((cx - 0.15 - 0.8 * f, sub.normal(0, 0.06) * (1 + 2 * f), (1 - f) * sub.uniform(0.5, 1)))
    G += bola + chamas * 0.9 + cauda + T.blur(cauda, 0.03) * 0.5 + T.splats(fa, 0.012)
    H += T.gauss(cx, 0, 0.08) * 1.8 + cauda * 0.4 + T.splats(fa, 0.007) * 0.5
    return G, H


def jajanken_papel(T, t, rng):
    """A bola de aura do Papel explode no rival: a esfera de aura cresce, a casca brilha, os anéis
    correm, as línguas de aura sobem e as faíscas voam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cresce = ease_out(rel(t, 0.0, 0.35), 2.3)
    r = 0.12 + 0.6 * cresce
    disco = T.blur(T.polys([([(r * math.cos(a), r * math.sin(a)) for a in np.linspace(0, TAU, 48, endpoint=False)], 1.0)]), 0.05)
    esfera = (T.gauss(0, 0, r * 0.42) * 1.3 + disco * 0.55) * pulso(t, 0.0, 0.7)
    casca = T.ring(r, 0.05) * pulso(t, 0.0, 0.75)
    aneis = sum(T.ring(0.2 + 0.78 * ease_out(rel(t, 0.08 + 0.08 * j, 0.8), 2), 0.03) * pulso(t, 0.08 + 0.08 * j, 0.85) for j in range(2))
    sub = np.random.default_rng(441)
    linguas = []
    for j in range(10):
        a = TAU * j / 10 + sub.uniform(-0.2, 0.2)
        comp = (0.45 + 0.35 * sub.uniform()) * pulso(t, 0.1, 0.9)
        linguas.append((r * 0.8 * math.cos(a), r * 0.8 * math.sin(a), (r * 0.8 + comp) * math.cos(a), (r * 0.8 + comp) * math.sin(a), 1.0))
    L = T.tapered(linguas, 0.06)
    fa = []
    for _ in range(24):
        a = sub.uniform(0, TAU)
        d = 0.2 + 0.75 * ease_out(rel(t, 0.1, 0.85), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.1, 0.9) * sub.uniform(0.4, 1)))
    G += (esfera + casca * 1.1 + aneis + L * 0.7 + T.splats(fa, 0.012) * 1.1) * env
    H += (T.gauss(0, 0, r * 0.3) * pulso(t, 0.0, 0.5) * 1.8 + casca * 0.5 + aneis * 0.3 + T.splats(fa, 0.007) * 0.6) * env
    return G, H


REGISTRO = [
    ("pedra_bloco", pedra_bloco, MEDIA, "Toph · o bloco de pedra voando (laço, básico)", True),
    ("pedra_estilhaca", pedra_estilhaca, GRANDE, "Toph · o bloco se partindo no rival", False),
    ("pisada_toph", pisada_toph, MEDIA, "Toph · a pisada no chão (nela)", False),
    ("visao_sismica", visao_sismica, GRANDE, "Toph · Visão sísmica: as ondas, o contorno e a terra prendendo", False),
    ("pedregulho_toph", pedregulho_toph, GRANDE, "Toph · a pedra da Muralha esmagando o rival", False),
    ("metal_preparo", metal_preparo, MEDIA, "Toph · as placas de metal girando no Preparo (laço)", True),
    ("metal_dobrado", metal_dobrado, GRANDE, "Toph · Metal dobrado: as faixas enrolam e esmagam", False),
    ("nen_gon", nen_gon, MEDIA, "Gon · a aura juntando no punho (laço)", True),
    ("jajanken_pedra", jajanken_pedra, GRANDE, "Gon · Jajanken: Pedra, o punho de aura", False),
    ("jajanken_tesoura", jajanken_tesoura, GRANDE, "Gon · Jajanken: Tesoura, a lâmina dos dedos", False),
    ("papel_bola", papel_bola, MEDIA, "Gon · a bola de aura do Papel voando (laço)", True),
    ("jajanken_papel", jajanken_papel, GRANDE, "Gon · Jajanken: Papel explodindo", False),
]
