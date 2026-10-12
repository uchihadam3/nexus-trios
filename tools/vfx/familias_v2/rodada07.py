"""Rodada 7 das habilidades próprias: Rukia, Aizen, Kenpachi (Bleach), Eren e Mikasa (Attack on Titan).

Rukia
- sode_no_shirayuki: a espada branca — a fita presa no cabo corre em espiral até o rival, os
  flocos de neve giram com ela e o golpe deixa a geada em estrela.
- circulo_de_gelo: a Primeira Dança (Tsukishiro) — o círculo perfeito acende no chão, e de dentro
  dele sobe a coluna de gelo, num estalo, com os cristais caindo.
- hakka_preparo: o Preparo do Bankai — a névoa fria girando e os flocos subindo (laço).
- hakka_no_togame: a Hakka no Togame — os cristais crescem em volta do rival como uma flor de gelo
  de seis pétalas que fecha nele, e trinca.

Aizen
- kyoka_suigetsu: a ilusão — a lua crescente no alto e o reflexo dela na água embaixo, as ondas
  tremendo, as pétalas caindo; nada é o que parece.
- plano_revelado: o plano revelado — um vidro enorme na frente do rival trinca do centro para fora
  e cai em pedaços; por trás, a estocada da espada.

Kenpachi
- instinto_de_batalha: a pancada com a espada lascada, e a pressão espiritual dele forma a caveira
  amarela atrás do golpe.
- corte_selvagem: três cortes brutos, tortos, de borda serrilhada (a lâmina cheia de dentes), e o
  sangue.
- limitador_preparo: o tapa-olho sai — a pressão sobe em labaredas pontudas (laço).
- retirar_o_limitador: a coluna de pressão amarela explode e o corte com as duas mãos desce, enorme.

Eren
- endurecimento_titan: o endurecimento — as placas de cristal hexagonais se juntam numa casca em
  volta do aliado, com o brilho das facetas.
- fundacao_preparo: o Preparo da Fundação — o raio amarelo da transformação desce e o vapor sobe
  (laço).
- rugido_da_fundacao: o Rugido — as pegadas dos titãs colossais marchando em fila, o chão tremendo,
  as colunas de vapor e o anel de choque em todos.

Mikasa
- manobra_odm: o equipamento de manobra — os dois cabos disparam e cravam, o corpo gira no arco
  com o jato de gás e o corte giratório.
- laminas_em_x: as duas lâminas em X; as pontas quebram e voam (as lâminas descartáveis), e o
  cachecol vermelho tremula no meio.
- golpe_na_nuca: o golpe decisivo — a queda de cima em espiral, o corte fundo e certeiro na nuca, e
  o vapor que sai.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _floco(cx, cy, r, ang=0.0):
    """O floco de neve: seis braços com dois galhos cada (segmentos)."""
    segs = []
    for k in range(6):
        a = ang + TAU * k / 6
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        segs.append((cx, cy, x2, y2, 1.0))
        for u, g in ((0.5, 0.35), (0.75, 0.25)):
            bx, by = cx + r * u * math.cos(a), cy + r * u * math.sin(a)
            for lado in (1, -1):
                aa = a + lado * 0.8
                segs.append((bx, by, bx + r * g * math.cos(aa), by + r * g * math.sin(aa), 0.8))
    return segs


def _cristal(cx, cy, comp, larg, ang):
    """Um cristal de gelo: o losango comprido com a ponta."""
    c, s = math.cos(ang), math.sin(ang)
    nx, ny = -s, c
    return [(cx, cy), (cx + c * comp * 0.35 + nx * larg, cy + s * comp * 0.35 + ny * larg), (cx + c * comp, cy + s * comp),
            (cx + c * comp * 0.35 - nx * larg, cy + s * comp * 0.35 - ny * larg)]


def _estilhacos(T, t, seed, n, t0, alcance=0.8, larg=0.02, cx=0.0, cy=0.0, gravidade=0.25):
    sub = np.random.default_rng(seed)
    shapes = []
    tt = rel(t, t0, 1.0)
    if tt <= 0:
        return T.zero()
    for _ in range(n):
        a = sub.uniform(0, TAU)
        d = sub.uniform(0.4, 1.0) * alcance * ease_out(tt, 1.8)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) + gravidade * tt * tt
        r = larg * sub.uniform(0.7, 1.6)
        g = sub.uniform(0, TAU) + tt * sub.uniform(-8, 8)
        shapes.append(([(x + r * math.cos(g), y + r * math.sin(g)), (x + r * 0.6 * math.cos(g + 2.3), y + r * 0.6 * math.sin(g + 2.3)),
                        (x + r * 0.8 * math.cos(g + 4.1), y + r * 0.8 * math.sin(g + 4.1))], (1 - tt) ** 1.2))
    return T.polys(shapes)


# =================================================================== Rukia
def sode_no_shirayuki(T, t, rng):
    """A fita branca do cabo corre em espiral até o rival, os flocos giram junto, e o golpe deixa a
    geada em estrela (o floco grande que acende e some)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corre = ease_out(rel(t, 0.0, 0.45), 1.6)
    pts = []
    for u in np.linspace(0, corre, 50):
        a = u * TAU * 1.6
        r = 0.7 * (1 - u) + 0.05
        pts.append((r * math.cos(a + 2.3), r * math.sin(a + 2.3) * 0.75))
    fita = T.polyline(pts, 0.022) if len(pts) > 1 else T.zero()
    G += (fita + T.blur(fita, 0.02) * 0.6) * (1 - rel(t, 0.5, 0.8))
    H += fita * 0.7 * (1 - rel(t, 0.5, 0.8))
    sub = np.random.default_rng(7)
    flocos = T.zero()
    for k in range(9):
        a0 = sub.uniform(0, TAU)
        r = 0.25 + 0.45 * sub.uniform()
        a = a0 + t * 3
        flocos += T.lines(_floco(r * math.cos(a), r * math.sin(a) * 0.8, 0.045 * sub.uniform(0.7, 1.2), t * 2 + k), 0.008)
    G += flocos * 0.9 * pulso(t, 0.0, 1.0)
    geada = rel(t, 0.42, 0.85)
    if geada > 0:
        F = T.lines(_floco(0, 0, 0.12 + 0.35 * ease_out(geada, 2), 0.3), 0.016)
        G += (F * 1.3 + T.blur(F, 0.02) * 0.6) * (1 - geada * 0.7)
        H += F * 0.6 * (1 - geada)
    H += T.gauss(0, 0, 0.08) * pulso(t, 0.4, 0.6) * 1.5
    return G * env, H * env


def circulo_de_gelo(T, t, rng):
    """A Primeira Dança: o círculo perfeito acende no chão (a linha que se desenha em volta), e de
    dentro dele sobe de uma vez a coluna de gelo, com as faces e o brilho; os cristais caem."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    desenha = ease_out(rel(t, 0.0, 0.3), 1.8)
    anel = T.arc_band(0.5, 0.03, -math.pi / 2, -math.pi / 2 + TAU * desenha + 0.01, squash=0.3, cy=0.42) if desenha > 0 else T.zero()
    G += anel * 1.4 + T.gauss(0, 0.42, 0.5 * desenha + 0.01, 0.14 * desenha + 0.01) * 0.35
    sobe = back(rel(t, 0.32, 0.5), 1.2)
    if sobe > 0:
        alt = 1.2 * sobe
        coluna = T.polys([([(-0.42, 0.42), (-0.36, 0.42 - alt), (0.36, 0.42 - alt), (0.42, 0.42)], 1.0)])
        faces = T.lines([(-0.14, 0.42, -0.12, 0.42 - alt, 1.0), (0.16, 0.42, 0.14, 0.42 - alt, 1.0)], 0.012)
        topo = T.polys([([(-0.36, 0.42 - alt), (0.0, 0.32 - alt), (0.36, 0.42 - alt)], 1.0)])
        derrete = 1 - rel(t, 0.7, 0.95)
        G += (coluna * 0.5 + T.blur(coluna, 0.03) * 0.5 + faces * 0.8 + topo * 0.7) * derrete
        H += (np.clip(coluna - T.blur(coluna, 0.01), 0, 1) * 0.9 + faces * 0.5) * derrete
    G += _estilhacos(T, t, 21, 24, 0.55, 0.8, 0.025, 0, -0.2, 0.6) * 1.2
    H += T.flare(0, -0.1, 0.9 * pulso(t, 0.32, 0.55) + 0.01, 0, 0.02) * pulso(t, 0.32, 0.55)
    return G * env, H * env


def hakka_preparo(T, t, rng):
    """O Preparo da Hakka no Togame: a névoa fria gira em volta (as faixas) e os flocos sobem (laço)."""
    G, H = vazio(T)
    for k in range(3):
        a0 = TAU * (t + k / 3)
        G += T.arc_band(0.5 - 0.08 * k, 0.05, a0, a0 + 2.2, squash=1.6, taper=0.8) * 0.7
    sub = np.random.default_rng(3)
    pts = []
    for _ in range(16):
        f = (sub.uniform() + t) % 1
        pts.append((sub.uniform(-0.5, 0.5), 0.6 - 1.2 * f, math.sin(math.pi * f)))
    G += T.splats(pts, 0.02) * 0.8
    G += T.gauss(0, 0, 0.3) * 0.25
    H += T.gauss(0, 0, 0.1) * (0.5 + 0.3 * math.sin(TAU * t))
    return G, H


def hakka_no_togame(T, t, rng):
    """A Hakka no Togame: os cristais crescem de fora para dentro em seis pétalas de gelo, fecham no
    rival (a flor de gelo), o miolo brilha frio, e no fim trinca e se desfaz em pó de neve."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cresce = ease_out(rel(t, 0.0, 0.5), 1.7)
    fecha = rel(t, 0.4, 0.6)
    shapes = []
    for k in range(12):
        a = TAU * k / 12 + 0.26
        grande = k % 2 == 0
        comp = (0.7 if grande else 0.45) * cresce
        larg = (0.12 if grande else 0.07) * (1 - 0.3 * fecha)
        ang = a + math.pi * (0.0 + 0.9 * fecha * 0.0)
        base = 0.85 * (1 - cresce) + 0.05
        shapes.append((_cristal(base * math.cos(a), base * math.sin(a), comp, larg, ang), 1.0))
    flor = T.polys(shapes) if cresce > 0.02 else T.zero()
    trinca = rel(t, 0.65, 0.8)
    some = 1 - rel(t, 0.78, 0.95)
    G += (flor * 0.6 + T.blur(flor, 0.025) * 0.6) * some
    H += np.clip(flor - T.blur(flor, 0.006), 0, 1) * 0.9 * some
    G += T.gauss(0, 0, 0.18) * fecha * 0.9 * some
    if trinca > 0:
        q = np.random.default_rng(15)
        for k in range(8):
            a = TAU * k / 8 + 0.2
            G += T.polyline(jagged(q, 0, 0, 0.6 * trinca * math.cos(a), 0.6 * trinca * math.sin(a), 3, 0.35), 0.01) * some * 1.3
    G += _estilhacos(T, t, 33, 30, 0.78, 0.7, 0.02, gravidade=0.4) * 1.2
    return G * env, H * env


# =================================================================== Aizen
def kyoka_suigetsu(T, t, rng):
    """A ilusão do Kyoka Suigetsu: a lua crescente no alto e o reflexo dela na água embaixo (a linha
    d'água), as ondas tremem o reflexo, as pétalas caem; no fim tudo ondula e se desfaz."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    lua = T.arc_band(0.3, 0.13, 2.2, 5.2, cy=-0.38, crescente=True) * surge
    G += lua * 1.2 + T.blur(lua, 0.04) * 0.6
    H += lua * 0.6
    G += T.lines([(-0.85, 0.12, 0.85, 0.12, 1.0)], 0.006) * surge * 0.8
    reflexo = T.arc_band(0.3, 0.13, -5.2, -2.2, cy=0.62, crescente=True) * surge
    onda = 0.035 * math.sin(t * 20) * pulso(t, 0.2, 1.0)
    du = onda * np.sin(T.V * 40 + t * 15) * (T.V > 0.12)
    reflexo = T.warp(reflexo, du, T.zero())
    G += reflexo * 0.7
    for k in range(3):
        u = (t * 1.2 + k / 3) % 1
        G += T.ring(0.08 + 0.5 * u, 0.012, 0, 0.62, squash=4) * (1 - u) * 0.6 * surge
    sub = np.random.default_rng(9)
    petalas = []
    for k in range(12):
        f = (sub.uniform() + t * 0.8) % 1
        x = sub.uniform(-0.7, 0.7) + 0.08 * math.sin(f * 8 + k)
        petalas.append(([(x, -0.6 + 0.75 * f), (x + 0.03, -0.62 + 0.75 * f), (x + 0.05, -0.58 + 0.75 * f), (x + 0.02, -0.56 + 0.75 * f)], math.sin(math.pi * f)))
    G += T.polys(petalas) * 0.9
    desfaz = rel(t, 0.65, 0.95)
    if desfaz > 0:
        G = T.warp(G, 0.05 * desfaz * np.sin(T.V * 30), 0.03 * desfaz * np.sin(T.U * 25))
    return G * env, H * env


def plano_revelado(T, t, rng):
    """O plano revelado: um vidro enorme (o retângulo de luz) na frente do rival trinca do centro para
    fora, cai em pedaços, e por trás vem a estocada da espada (a lâmina fina e o clarão)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vidro = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.5, 0.55))
    borda = T.lines([(-0.55, -0.6, 0.55, -0.6, 1.0), (0.55, -0.6, 0.55, 0.6, 1.0), (0.55, 0.6, -0.55, 0.6, 1.0), (-0.55, 0.6, -0.55, -0.6, 1.0)], 0.012)
    plano = T.polys([([(-0.55, -0.6), (0.55, -0.6), (0.55, 0.6), (-0.55, 0.6)], 1.0)])
    reflexo = T.lines([(-0.4, -0.5, -0.15, -0.25, 1.0), (-0.35, -0.3, -0.25, -0.2, 0.6)], 0.02)
    G += (borda * 1.1 + plano * 0.12 + reflexo * 0.6) * vidro
    trinca = rel(t, 0.18, 0.48)
    if trinca > 0 and t < 0.56:
        q = np.random.default_rng(42)
        for k in range(10):
            a = TAU * k / 10 + 0.15
            G += T.polyline(jagged(q, 0, 0, 0.8 * trinca * math.cos(a), 0.8 * trinca * math.sin(a), 3, 0.3), 0.01) * 1.4
        G += T.ring(0.12 * trinca, 0.01) * 1.2
    G += _estilhacos(T, t, 48, 38, 0.52, 0.9, 0.05, gravidade=0.7) * 1.1
    vem = ease_in(rel(t, 0.5, 0.62), 2)
    if 0.5 < t < 0.85:
        L = T.polys([(lamina(0.9, -0.15, 0.9 - 1.0 * vem, -0.15 + 0.12 * vem, 0.035, 1.0), 1.0)])
        G += L * 1.4 + T.blur(L, 0.02) * 0.5
        H += L * 0.8
    estoc = pulso(t, 0.6, 0.85)
    H += (T.flare(-0.1, -0.03, 0.9 * estoc + 0.01, 0, 0.02) + T.gauss(-0.1, -0.03, 0.04) * 1.5) * estoc
    return G * env, H * env


# =================================================================== Kenpachi
def _caveira(T, cx, cy, s):
    """A caveira da pressão espiritual: o crânio, as órbitas fundas, o nariz e os dentes."""
    cranio = T.gauss(cx, cy - 0.05 * s, 0.26 * s, 0.24 * s) + T.gauss(cx, cy + 0.17 * s, 0.17 * s, 0.11 * s) * 0.9
    orbitas = T.gauss(cx - 0.11 * s, cy - 0.02 * s, 0.065 * s, 0.07 * s) + T.gauss(cx + 0.11 * s, cy - 0.02 * s, 0.065 * s, 0.07 * s)
    nariz = T.polys([([(cx, cy + 0.06 * s), (cx - 0.03 * s, cy + 0.12 * s), (cx + 0.03 * s, cy + 0.12 * s)], 1.0)])
    dentes = T.lines([(cx + d * s, cy + 0.2 * s, cx + d * s, cy + 0.27 * s, 1.0) for d in np.linspace(-0.1, 0.1, 6)], 0.012)
    return np.clip(cranio, 0, 1), np.clip(orbitas, 0, 1) + nariz, dentes


def instinto_de_batalha(T, t, rng):
    """A espada lascada desce num golpe só, e atrás do impacto a pressão espiritual forma a caveira
    amarela, que ri (os dentes) e some na fumaça."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    caveira = pulso(t, 0.25, 1.0)
    cr, buracos, dentes = _caveira(T, 0, -0.1, 1.5 * (0.8 + 0.2 * ease_out(rel(t, 0.25, 0.5), 2)))
    G += (cr * 0.7 - buracos * 0.6 + dentes * 0.6) * caveira
    H += np.clip(cr - T.blur(cr, 0.03) * 1.1, 0, 1) * caveira * 0.8
    desce = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.5:
        L = T.polys([(lamina(-0.7, -0.8, -0.7 + 0.85 * desce, -0.8 + 0.95 * desce, 0.06, 1.0), 1.0)])
        dentes_lamina = T.zero()
        G += L * 1.2 + T.blur(L, 0.02) * 0.6 * (1 - rel(t, 0.3, 0.5))
    impacto = pulso(t, 0.22, 0.5)
    G += T.gauss(0.1, 0.12, 0.2) * impacto * 1.4
    H += T.flare(0.1, 0.12, 0.8 * impacto + 0.01, 0.8, 0.025) * impacto
    G += T.ring(0.1 + 0.6 * rel(t, 0.25, 0.7), 0.04, 0.1, 0.12) * (1 - rel(t, 0.25, 0.7)) * (t > 0.25)
    return G * env, H * env


def _serrilhado(x1, y1, x2, y2, larg, prog, dentes=11, seed=0):
    """Um corte de borda serrilhada: a lente com a borda de cima em dentes irregulares."""
    sub = np.random.default_rng(seed)
    dx, dy = x2 - x1, y2 - y1
    comp = math.hypot(dx, dy) or 1
    nx, ny = -dy / comp, dx / comp
    cima, baixo = [], []
    n = dentes * 2
    for k in range(n + 1):
        u = prog * k / n
        w = larg * math.sin(math.pi * min(1, u)) ** 0.7
        x, y = x1 + dx * u, y1 + dy * u
        bico = 1.0 + (0.9 * sub.uniform(0.4, 1) if k % 2 else -0.2)
        cima.append((x + nx * w * bico, y + ny * w * bico))
        baixo.append((x - nx * w * 0.6, y - ny * w * 0.6))
    return cima + baixo[::-1]


def corte_selvagem(T, t, rng):
    """Três cortes brutos, um atrás do outro, tortos e de borda serrilhada (a lâmina lascada), e o
    sangue espirrando pela linha de cada um."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cortes = (((-0.8, -0.5), (0.7, 0.35), 0.0), ((0.75, -0.6), (-0.6, 0.55), 0.17), ((-0.85, 0.1), (0.85, -0.05), 0.34))
    for k, ((x1, y1), (x2, y2), t0) in enumerate(cortes):
        p = ease_out(rel(t, t0, t0 + 0.12), 2)
        some = 1 - rel(t, t0 + 0.15, t0 + 0.45)
        if p <= 0 or some <= 0:
            continue
        S = T.polys([(_serrilhado(x1, y1, x2, y2, 0.06, p, 12, k), 1.0)])
        G += (S * 1.3 + T.blur(S, 0.02) * 0.5) * some
        H += S * 0.6 * some
        sub = np.random.default_rng(80 + k)
        gotas = []
        for _ in range(12):
            u = sub.uniform(0.2, 0.9)
            tt = rel(t, t0 + 0.08, t0 + 0.6)
            gotas.append((x1 + (x2 - x1) * u + sub.uniform(-0.1, 0.1) * tt, y1 + (y2 - y1) * u + 0.25 * tt * tt + sub.uniform(-0.05, 0.1) * tt, (1 - tt) * sub.uniform(0.4, 1)))
        G += T.splats(gotas, 0.014) * 1.1 * (t > t0 + 0.08)
    return G * env, H * env


def _labaredas(T, t, n, raio, alt, seed):
    sub = np.random.default_rng(seed)
    segs = []
    for k in range(n):
        a = TAU * k / n + sub.uniform(-0.15, 0.15)
        f = (t * 2.2 + sub.uniform()) % 1
        x = raio * math.cos(a)
        base = 0.5 + 0.1 * math.sin(a)
        segs.append((x, base, x * (1 - 0.3 * f) + 0.05 * math.sin(f * 9 + k), base - alt * (0.4 + 0.6 * f) * sub.uniform(0.6, 1.1), 1 - f * 0.7))
    return T.tapered(segs, 0.07)


def limitador_preparo(T, t, rng):
    """O tapa-olho sai: a pressão sobe em labaredas pontudas em volta do corpo (laço)."""
    G, H = vazio(T)
    L = _labaredas(T, t, 14, 0.38, 0.9, 5)
    G += T.blur(L, 0.02) * 1.0 + L * 0.4
    G += T.gauss(0, 0.1, 0.25, 0.45) * (0.6 + 0.3 * math.sin(TAU * t * 2))
    H += T.gauss(0, 0.1, 0.08, 0.3) * 0.6
    return G, H


def retirar_o_limitador(T, t, rng):
    """A coluna de pressão amarela explode para cima (as labaredas pontudas, a caveira de relance), e
    o corte com as duas mãos desce, enorme, partindo o chão; a poeira sobe dos lados."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    coluna = pulso(t, 0.0, 0.55)
    G += T.gauss(0, -0.1, 0.25, 0.8) * coluna * 1.0
    L = _labaredas(T, t, 18, 0.32, 1.2, 8)
    G += T.blur(L, 0.02) * coluna * 1.2
    cr, buracos, _ = _caveira(T, 0, -0.45, 0.9)
    G += (cr * 0.5 - buracos * 0.4) * pulso(t, 0.1, 0.45)
    desce = ease_in(rel(t, 0.38, 0.52), 2.2)
    if 0.38 < t < 0.75:
        S = T.polys([(lamina(0.85, -0.85, 0.85 - 1.7 * desce, -0.85 + 1.45 * desce, 0.16, 1.0, rel(t, 0.55, 0.75)), 1.0)])
        G += S * 1.4 + T.blur(S, 0.03) * 0.6
        H += S * 0.9
    racha = rel(t, 0.5, 0.75)
    if racha > 0:
        q = np.random.default_rng(4)
        for lado in (-1, 1):
            G += T.polyline(jagged(q, 0, 0.6, lado * 0.85 * racha, 0.62, 4, 0.2), 0.016) * (1 - rel(t, 0.8, 1)) * 1.3
        sub = np.random.default_rng(6)
        pts = [(lado * sub.uniform(0.1, 0.8) * racha, 0.6 - sub.uniform(0, 0.4) * racha, 1 - racha) for lado in (-1, 1) for _ in range(10)]
        G += T.splats(pts, 0.05) * 0.8
    H += T.gauss(0, 0.55, 0.12) * pulso(t, 0.48, 0.7) * 1.6
    return G * env, H * env


# =================================================================== Eren
def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * k / 6), cy + r * math.sin(ang + TAU * k / 6)) for k in range(6)]


def endurecimento_titan(T, t, rng):
    """O endurecimento: as placas de cristal hexagonais chegam de fora e se encaixam numa casca em volta
    do aliado (uma depois da outra), as facetas brilham, e o reflexo passa pela casca."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    placas = []
    bordas = T.zero()
    r = 0.11
    sub = np.random.default_rng(12)
    centros = []
    for q in range(-4, 5):
        for s_ in range(-4, 5):
            x = r * 1.75 * (q + s_ * 0.5)
            y = r * 1.52 * s_
            if x * x / 0.58 ** 2 + y * y / 0.68 ** 2 <= 1.0 and x * x / 0.42 ** 2 + y * y / 0.5 ** 2 >= 0.55:
                centros.append((x, y))
    for k, (x, y) in enumerate(centros):
        t0 = 0.02 + 0.4 * sub.uniform()
        chega = ease_out(rel(t, t0, t0 + 0.18), 2)
        if chega <= 0:
            continue
        d = 0.5 * (1 - chega)
        ang = math.atan2(y, x)
        px, py = x + d * math.cos(ang), y + d * math.sin(ang)
        placas.append((_hexagono(px, py, r * 0.92), 0.8 + 0.2 * sub.uniform()))
    if placas:
        P = T.polys(placas)
        G += P * 0.45 + T.blur(P, 0.02) * 0.3
        bordas = np.clip(P - T.blur(P, 0.006) * 1.2, 0, 1)
        G += bordas * 0.9
        H += bordas * 0.6
    reflexo = rel(t, 0.5, 0.8)
    if reflexo > 0:
        banda = np.exp(-((T.U + T.V * 0.6 - (-1.2 + 2.6 * reflexo)) / 0.08) ** 2)
        H += banda * np.clip(T.blur(bordas, 0.01) * 4, 0, 1) * 1.3
    G += T.gauss(0, 0, 0.5, 0.6) * pulso(t, 0.4, 1.0) * 0.15
    return G * env, H * env


def fundacao_preparo(T, t, rng):
    """O Preparo do Rugido: o raio amarelo da transformação desce do céu, o clarão, e o vapor subindo
    em volta (laço)."""
    G, H = vazio(T)
    q = np.random.default_rng(int(t * 6))
    bolt = T.polyline(jagged(q, 0.05, -1.0, 0.0, 0.45, 5, 0.3), 0.02)
    pisca = 0.5 + 0.5 * math.cos(TAU * t * 3)
    G += (bolt * 1.3 + T.blur(bolt, 0.03) * 0.8) * pisca
    H += bolt * pisca
    sub = np.random.default_rng(2)
    pts = []
    for _ in range(18):
        f = (sub.uniform() + t) % 1
        x = sub.uniform(-0.55, 0.55)
        pts.append((x * (1 + 0.4 * f), 0.5 - 0.9 * f, (1 - f) * 0.8))
    G += T.splats(pts, 0.06) * 0.6
    G += T.gauss(0, 0.45, 0.2, 0.08) * (0.6 + 0.4 * pisca)
    return G, H


def _pegada(cx, cy, s):
    """A pegada gigante: a sola e os cinco dedos."""
    sola = [(cx - 0.07 * s, cy), (cx - 0.08 * s, cy - 0.12 * s), (cx, cy - 0.17 * s), (cx + 0.08 * s, cy - 0.12 * s), (cx + 0.07 * s, cy), (cx, cy + 0.06 * s)]
    shapes = [(sola, 1.0)]
    for k in range(5):
        dx = (-0.08 + 0.04 * k) * s
        shapes.append(([(cx + dx - 0.015 * s, cy - 0.19 * s), (cx + dx + 0.015 * s, cy - 0.19 * s), (cx + dx + 0.012 * s, cy - 0.23 * s), (cx + dx - 0.012 * s, cy - 0.23 * s)], 1.0))
    return shapes


def rugido_da_fundacao(T, t, rng):
    """O Rugido: as pegadas dos titãs colossais descem em fila (três fileiras, chegando), cada uma com
    o baque (o anel no chão), o vapor sobe em colunas e o grande anel de choque passa em todos."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    tremor = 0.02 * math.sin(t * 90) * pulso(t, 0.1, 0.9)
    pegadas = T.zero()
    for fila in range(2):
        for k in range(3):
            t0 = 0.05 + 0.16 * k + 0.07 * fila
            u = rel(t, t0, t0 + 0.4)
            if u <= 0:
                continue
            x = -0.6 + 0.6 * k + 0.25 * fila + tremor
            y = -0.1 + 0.5 * fila
            s = 1.0 + 0.35 * fila
            some = 1 - rel(t, t0 + 0.45, t0 + 0.75)
            # a cratera do passo: a borda achatada que afunda e o miolo escuro
            pegadas += T.ring(0.16 * s, 0.025 * s, x, y, squash=2.4) * some
            G -= T.gauss(x, y, 0.13 * s, 0.05 * s) * 0.5 * some
            q = np.random.default_rng(200 + 10 * fila + k)
            for j in range(6):
                a = math.pi * (j / 5) * 1.0 + (0 if j % 2 else math.pi)
                comp = (0.15 + 0.2 * ease_out(u, 2)) * s
                pegadas += T.polyline(jagged(q, x + 0.15 * s * math.cos(a), y + 0.06 * s * math.sin(a), x + comp * 1.5 * math.cos(a), y + comp * 0.5 * math.sin(a), 3, 0.3), 0.01) * some
            G += T.ring(0.1 + 0.35 * u, 0.02, x, y, squash=2.4) * (1 - u) * 1.2
            sub0 = np.random.default_rng(int(t0 * 100))
            poeira = [(x + sub0.uniform(-0.3, 0.3) * (0.3 + u), y - 0.25 * u * sub0.uniform(), (1 - u) * 0.8) for _ in range(10)]
            G += T.splats(poeira, 0.045) * 0.7
            H += T.gauss(x, y, 0.08 * s, 0.03 * s) * pulso(u, 0.0, 0.3) * 1.2
    G += pegadas * 0.8 + T.blur(pegadas, 0.02) * 0.4
    sub = np.random.default_rng(17)
    vapor = []
    for _ in range(30):
        t0 = sub.uniform(0.2, 0.6)
        f = rel(t, t0, t0 + 0.6)
        if 0 < f < 1:
            x = sub.uniform(-0.8, 0.8)
            vapor.append((x + 0.05 * math.sin(f * 6), 0.4 - 0.9 * f, (1 - f) * 0.7))
    G += T.splats(vapor, 0.07) * 0.7
    choque = rel(t, 0.55, 0.95)
    G += T.ring(0.1 + 1.0 * ease_out(choque, 1.6), 0.06) * (1 - choque) * 1.3 * (choque > 0)
    H += T.gauss(0, 0, 0.3) * pulso(t, 0.53, 0.7) * 0.6
    return G * env, H * env


# =================================================================== Mikasa
def manobra_odm(T, t, rng):
    """O equipamento de manobra: os dois cabos disparam para cima e cravam (o gancho acende), o corpo
    passa no arco com o jato de gás saindo em nuvem, e o corte giratório fecha no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    for k, (ax, ay) in enumerate(((-0.75, -0.85), (0.7, -0.8))):
        dispara = ease_out(rel(t, 0.0 + 0.04 * k, 0.18 + 0.04 * k), 2)
        solta = 1 - rel(t, 0.5, 0.6)
        ox, oy = -0.6 + 0.6 * ease_out(rel(t, 0.15, 0.5), 2), 0.45 - 0.3 * ease_out(rel(t, 0.15, 0.5), 2)
        cabo = T.lines([(ox, oy, ox + (ax - ox) * dispara, oy + (ay - oy) * dispara, 1.0)], 0.006) * solta
        G += cabo * 1.1
        G += T.gauss(ax, ay, 0.03) * pulso(t, 0.16 + 0.04 * k, 0.4) * 1.4
    arco = ease_out(rel(t, 0.15, 0.5), 2)
    if arco > 0:
        G += T.arc_band(0.6, 0.05, math.pi * 0.95, math.pi * (0.95 - 0.7 * arco), squash=0.7, cy=0.05, taper=0.6) * (1 - rel(t, 0.55, 0.75)) * 0.9
    sub = np.random.default_rng(5)
    gas = []
    for _ in range(26):
        t0 = sub.uniform(0.15, 0.5)
        f = rel(t, t0, t0 + 0.5)
        if 0 < f < 1:
            a = math.pi * (0.95 - 0.7 * rel(t0, 0.15, 0.5))
            x, y = 0.6 * math.cos(a), 0.05 + 0.42 * math.sin(a)
            gas.append((x + sub.uniform(-0.1, 0.1) * f, y + 0.15 * f, (1 - f) * 0.7))
    G += T.splats(gas, 0.05) * 0.8
    gira = ease_out(rel(t, 0.45, 0.7), 2)
    if gira > 0:
        for k in range(2):
            a0 = k * math.pi
            G += T.arc_band(0.32, 0.06, a0, a0 + 2.6 * gira, squash=0.55, taper=0.7) * (1 - rel(t, 0.68, 0.9)) * 1.3
        H += T.gauss(0, 0, 0.06) * pulso(t, 0.5, 0.75) * 1.5
    return G * env, H * env


def laminas_em_x(T, t, rng):
    """As duas lâminas cortam em X (uma depois da outra), as pontas quebram e voam girando (as lâminas
    descartáveis), e o cachecol vermelho tremula atravessando o meio."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    for k, (a, t0) in enumerate(((0.75, 0.05), (-0.75, 0.15))):
        p = ease_out(rel(t, t0, t0 + 0.15), 2)
        some = 1 - rel(t, t0 + 0.2, t0 + 0.5)
        if p <= 0:
            continue
        c, s = math.cos(a), math.sin(a)
        L = T.polys([(lamina(-0.75 * c, -0.75 * s, 0.75 * c, 0.75 * s, 0.05, p, rel(t, t0 + 0.12, t0 + 0.45)), 1.0)])
        G += (L * 1.3 + T.blur(L, 0.02) * 0.5) * some
        H += L * 0.7 * some
    sub = np.random.default_rng(9)
    pontas = []
    voa = rel(t, 0.3, 0.9)
    if voa > 0:
        for k in range(2):
            a = (-0.6 if k else 2.4) + sub.uniform(-0.3, 0.3)
            d = 0.25 + 0.6 * ease_out(voa, 1.6)
            x, y = d * math.cos(a), d * math.sin(a) + 0.3 * voa * voa
            g = voa * 12 + k
            pontas.append(([(x + 0.14 * math.cos(g), y + 0.14 * math.sin(g)), (x + 0.02 * math.cos(g + 1.6), y + 0.02 * math.sin(g + 1.6)),
                            (x - 0.1 * math.cos(g), y - 0.1 * math.sin(g)), (x + 0.02 * math.cos(g - 1.6), y + 0.02 * math.sin(g - 1.6))], 1 - voa))
        P = T.polys(pontas)
        G += P * 1.2
        H += P * 0.6
    cachecol = pulso(t, 0.1, 0.95)
    pts = [(-0.9 + 1.8 * u, 0.05 + 0.1 * math.sin(u * 7 - t * 18) * u) for u in np.linspace(0, 1, 30)]
    C = T.polyline(pts, 0.05)
    G += (C * 0.6 + T.blur(C, 0.02) * 0.3) * cachecol
    H -= C * 0.3 * cachecol
    return G * env, H * env


def golpe_na_nuca(T, t, rng):
    """O golpe decisivo: a queda de cima girando (o rastro em espiral descendo), o corte fundo e certeiro
    na altura da nuca (curto, brilhante), o clarão, e o vapor quente saindo do corte."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cai = ease_in(rel(t, 0.0, 0.35), 1.8)
    pts = []
    for u in np.linspace(0, cai, 40):
        a = u * TAU * 2.2
        pts.append((0.38 * math.cos(a) * (1 - u * 0.5), -0.95 + 0.75 * u))
    if len(pts) > 1:
        R = T.polyline(pts, 0.045)
        G += (T.blur(R, 0.015) * 1.1 + R * 0.4) * (1 - rel(t, 0.35, 0.6))
    nuca = (0.0, -0.22)
    corta = ease_out(rel(t, 0.33, 0.42), 2)
    if corta > 0:
        L = T.polys([(lamina(nuca[0] - 0.7, nuca[1] - 0.1, nuca[0] + 0.7, nuca[1] + 0.1, 0.07, corta, rel(t, 0.5, 0.85)), 1.0)])
        G += L * 1.6 + T.blur(L, 0.02) * 0.6
        H += L * 1.0
    flash = pulso(t, 0.33, 0.58)
    H += (T.flare(*nuca, 1.0 * flash + 0.01, 0.05, 0.015) + T.gauss(*nuca, 0.03) * 1.5) * flash
    sub = np.random.default_rng(23)
    vapor = []
    for _ in range(22):
        t0 = sub.uniform(0.4, 0.65)
        f = rel(t, t0, t0 + 0.4)
        if 0 < f < 1:
            x = nuca[0] + sub.uniform(-0.3, 0.3)
            vapor.append((x + 0.05 * math.sin(f * 7), nuca[1] - 0.6 * f, (1 - f) * 0.8))
    G += T.splats(vapor, 0.05) * 0.8
    return G * env, H * env


REGISTRO = [
    ("sode_no_shirayuki", sode_no_shirayuki, GRANDE, "Rukia · a fita branca em espiral e a geada", False),
    ("circulo_de_gelo", circulo_de_gelo, GRANDE, "Rukia · o círculo no chão e a coluna de gelo", False),
    ("hakka_preparo", hakka_preparo, MEDIA, "Rukia · a névoa fria e os flocos (Preparo, laço)", True),
    ("hakka_no_togame", hakka_no_togame, GRANDE, "Rukia · a flor de gelo que fecha e trinca", False),
    ("kyoka_suigetsu", kyoka_suigetsu, GRANDE, "Aizen · a lua, o reflexo na água e as pétalas", False),
    ("plano_revelado", plano_revelado, GRANDE, "Aizen · o vidro que trinca e a estocada por trás", False),
    ("instinto_de_batalha", instinto_de_batalha, GRANDE, "Kenpachi · o golpe e a caveira amarela", False),
    ("corte_selvagem", corte_selvagem, GRANDE, "Kenpachi · três cortes serrilhados", False),
    ("limitador_preparo", limitador_preparo, MEDIA, "Kenpachi · a pressão em labaredas (Preparo, laço)", True),
    ("retirar_o_limitador", retirar_o_limitador, GRANDE, "Kenpachi · a coluna de pressão e o corte com as duas mãos", False),
    ("endurecimento_titan", endurecimento_titan, GRANDE, "Eren · a casca de cristal hexagonal", False),
    ("fundacao_preparo", fundacao_preparo, MEDIA, "Eren · o raio da transformação e o vapor (Preparo, laço)", True),
    ("rugido_da_fundacao", rugido_da_fundacao, GRANDE, "Eren · as pegadas dos colossais, o vapor e o choque", False),
    ("manobra_odm", manobra_odm, GRANDE, "Mikasa · os cabos, o gás e o corte giratório", False),
    ("laminas_em_x", laminas_em_x, GRANDE, "Mikasa · o X das lâminas, as pontas que quebram e o cachecol", False),
    ("golpe_na_nuca", golpe_na_nuca, GRANDE, "Mikasa · a queda em espiral e o corte na nuca", False),
]
