"""Rodada 3 das Mecânicas únicas ativando como habilidade: Frieren, Anya, Loid, Yor, Jinwoo, Kaneki, Yugi, Kaiba,
Pantera Negra, Feiticeira Escarlate, Visão, Capitã Marvel, Justiceiro, Motoqueiro Fantasma, Blade, Cavaleiro da Lua,
Ciclope, Jean Grey, Vampira, Gambit, Venom, Carnificina, Doutor Destino, Loki, Ultron e Duende Verde.

- mana: o círculo mágico abre no chão e as flores de mana desabrocham em volta (a magia do campo de flores).
- waku: as ondas da leitura de mente saem da cabeça e as estrelinhas do "waku waku" piscam.
- strix: a mira fecha no alvo, trava, e as três barras de Carga enchem.
- espinho: o espinho dourado crava na diagonal e as pétalas de rosa voam.
- nivel: a janela azul do sistema abre com a seta e as sombras sobem (subiu de nível).
- kakuja: os quatro tentáculos de kagune saem das costas e o olho de ghoul acende.
- carta_yugi: a carta vira no ar, acende, e o Enigma do Milênio brilha atrás.
- olhos_azuis: a carta do Dragão Branco acende e o Raio da Destruição desce em diagonal.
- cinetico: o traje puxa a energia (os riscos que entram) e solta a onda cinética roxa com as garras.
- hex: os fios de magia do caos giram em espiral e o hex estala.
- joia_da_mente: a joia amarela acende na testa e solta o leque de luz que limpa a mente.
- energia_absorvida: a estrela do peito acende, a energia entra e as chamas de fótons sobem.
- interrogatorio: a caveira aparece sobre o rival e os tiros traçantes passam.
- pecados: a corrente em chamas gira em volta do pecador.
- cacador: a glaive de duas lâminas gira, corta e espirra a névoa.
- crescentes: os crescentes de prata giram em volta e cravam no alvo.
- raio_rubi: o raio dos olhos escapa sem controle e varre a tela.
- elo_mental: a Fênix abre as asas e o elo mental liga os aliados.
- toque: a energia sai do rival, corre e entra na Vampira.
- carta_carregada: a carta acende rosa, gira e explode.
- simbionte: a gosma preta escorre em tentáculos e o emblema da aranha branca aparece.
- carnificina: as lâminas vermelhas explodem do corpo para todo lado.
- doombot: o Doombot aparece, segura o golpe e se parte em pedaços.
- ilusao: a imagem quebra como vidro e os chifres do Loki aparecem na névoa verde.
- corpo_novo: os pedaços de metal voltam juntos, a varredura passa e os olhos acendem.
- abobora: a bomba-abóbora voa em arco, pisca e explode.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (ASA, CARTA, DIAMANTE, ESPADA, LUA, RAIO, SETA, anel, aura, cheio, circulo, clarao, converge, corte,
                         estouro, estrela_pts, flor, icone, onda_no_chao, orbita, particulas, poe, raios, runas, surge)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def mana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    g, h = runas(T, t, 0.0, 1.0, 0.55, 12, 0.35, 2.6, 1.0)
    G, H = G + g, H + h
    for j in range(7):
        a = TAU * j / 7 + 0.4
        x, y = 0.42 * math.cos(a), 0.35 + 0.42 * math.sin(a) / 2.6
        s = ease_out(rel(t, 0.15 + 0.06 * j, 0.4 + 0.06 * j), 2.5) * (1 - rel(t, 0.85, 1))
        g, h = icone(T, poe(flor(5, 1.0, 0.25), x, y - 0.05 * s, 0.09 * s, t * 2), s, 0.5)
        G, H = G + g, H + h
    G += particulas(T, t, 0.2, 1.0, 40, 5, 0, 0.3, 0.45, 0.8)
    g, h = aura(T, t, 0.3, 1.0, 0.3, -0.05, 0.7)
    return (G + g) * env, (H + h) * env


def waku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cy = -0.35
    for lado in (-1, 1):
        s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.8, 1))
        g, h = cheio(T, [(lado * 0.1, cy), (lado * 0.17, cy - 0.12 * s), (lado * 0.2, cy + 0.02)], 0.9 * s)
        G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.1 + 0.15 * j, 0.6 + 0.15 * j)
        if 0 < u < 1:
            r = 0.12 + 0.55 * u
            G += T.arc_band(r * 1.3, 0.05, -2.5, -0.64, 1.0, 0.0, 0, cy + 0.05, 0.0) * (1 - u) * 1.6
    q = np.random.default_rng(14)
    for j in range(9):
        x, y = q.uniform(-0.6, 0.6), q.uniform(-0.7, 0.3)
        k = pulso(t, 0.15 + q.uniform(0, 0.5), 0.45 + q.uniform(0, 0.5))
        if k > 0:
            g, h = cheio(T, poe(estrela_pts(4, 0.3), x, y, 0.11 * k), k * 1.4)
            G, H = G + g, H + h * 2
    return G * env, H * env


def strix(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = ease_out(rel(t, 0.0, 0.4), 2.5)
    k = 1 - rel(t, 0.7, 0.85)
    if fecha > 0 and k > 0:
        r = 0.8 - 0.5 * fecha
        G += T.ring(r, 0.012, 0, -0.05) * 1.3 * k + T.ring(r * 0.35, 0.008, 0, -0.05) * k
        segs = []
        for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
            segs.append((r * 0.45 * math.cos(a), -0.05 + r * 0.45 * math.sin(a), r * 1.15 * math.cos(a), -0.05 + r * 1.15 * math.sin(a), 1.0))
        G += T.lines(segs, 0.01) * 1.2 * k
        trava = pulso(t, 0.4, 0.55)
        H += T.gauss(0, -0.05, 0.03) * (0.5 + trava * 1.5) * k
        G += T.ring(r * 0.15, 0.02, 0, -0.05) * trava * 1.5
    for j in range(3):
        y = 0.3 + 0.1 * j
        enche = ease_out(rel(t, 0.55 + 0.05 * j, 0.85 + 0.05 * j), 2)
        if enche > 0:
            kk = 1 - rel(t, 0.92, 1)
            G += T.lines([(-0.3, y, 0.3, y, 1.0)], 0.04) * 0.25 * kk
            G += T.lines([(-0.3, y, -0.3 + 0.6 * enche * 0.4, y, 1.0)], 0.04) * 1.3 * kk
            H += T.lines([(-0.3, y, -0.3 + 0.6 * enche * 0.4, y, 1.0)], 0.015) * kk
    return G * env, H * env


def espinho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.1, 0.35), 2.5)
    ang = 2.4
    if u > 0 and t < 0.8:
        ex, ey = 0.9 * (1 - u) * math.cos(ang - math.pi), -0.9 * (1 - u) * math.sin(ang - math.pi) * -1
        x2, y2 = 0.1 * math.cos(ang) + ex * 0 + 0.75 * (1 - u), -0.75 * (1 - u) - 0.0
        P = T.polys([(lamina(x2 + 0.6, y2 - 0.6, x2, y2, 0.05), 1.0)])
        k = 1 - rel(t, 0.6, 0.8)
        G += P * 1.3 * k
        H += P * 0.8 * k
    g, h = clarao(T, t, 0.33, 0.55, 0, 0, 0.8, 1.4)
    G, H = G + g, H + h
    q = np.random.default_rng(9)
    for j in range(14):
        v = rel(t, 0.35, 0.95)
        if 0 < v < 1:
            a = q.uniform(0, TAU)
            d = 0.7 * ease_out(v) * q.uniform(0.5, 1)
            g, h = icone(T, poe(flor(5, 1.0, 0.35), d * math.cos(a), d * math.sin(a) + 0.2 * v, 0.045, a + v * 5), 1 - v, 0.6)
            G, H = G + g, H + h
    G += anel(T, t, 0.33, 0.7, 0.05, 0.5, 0.03)
    return G * env, H * env


def nivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 3)
    k = 1 - rel(t, 0.8, 1)
    if abre > 0:
        w, hh = 0.42 * abre, 0.22
        janela = [(-w, -0.55 - hh), (w, -0.55 - hh), (w, -0.55 + hh), (-w, -0.55 + hh)]
        g, h = icone(T, janela, k, 0.25)
        G, H = G + g, H + h
        G += T.lines([(-w, -0.55 - hh + 0.07, w, -0.55 - hh + 0.07, 1.0)], 0.008) * k
        s = surge(t, 0.2, 0.4)
        g, h = cheio(T, poe(SETA, 0, -0.52, 0.13 * s, -math.pi / 2), k * 1.2)
        G, H = G + g, H + h * 2
    G += particulas(T, t, 0.2, 1.0, 50, 21, 0, 0.35, 0.5, 0.9, 0.02)
    for j in range(3):
        G += anel(T, t, 0.25 + 0.15 * j, 0.7 + 0.15 * j, 0.1, 0.6, 0.03, 0.38, 3.0)
    return G * env, H * env


def kakuja(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.8, 1)
    for j in range(4):
        u = ease_out(rel(t, 0.05 + 0.06 * j, 0.45 + 0.06 * j), 2.2)
        if u > 0:
            lado = -1 if j < 2 else 1
            base_a = -math.pi / 2 + lado * (0.5 + 0.35 * (j % 2))
            pts = []
            for v in np.linspace(0, u, 20):
                a = base_a + lado * 0.9 * v * v + 0.15 * math.sin(t * 9 + j + v * 4)
                d = 0.75 * v
                pts.append((d * math.cos(a), 0.1 + d * math.sin(a)))
            for i in range(len(pts) - 1):
                w = 0.06 * (1 - i / len(pts)) + 0.012
                G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], w) * k
            H += T.gauss(pts[-1][0], pts[-1][1], 0.02) * k
    olho = pulso(t, 0.35, 0.9)
    if olho > 0:
        olho_pts = [(0.15 * math.cos(a), -0.05 + 0.06 * math.sin(a) * (1 if a < math.pi else 1)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        g, h = icone(T, olho_pts, olho, 0.2)
        G, H = G + g, H + h
        H += T.gauss(0, -0.05, 0.035) * olho * 2
        G += T.gauss(0, -0.05, 0.06) * olho * 1.2
    return G * env, H * env


def _carta_virando(T, t, a, b, cx, cy, s, k=1.0):
    u = rel(t, a, b)
    larg = abs(math.cos(math.pi * (1 - ease_out(u, 2)) * 1.5)) if u < 1 else 1.0
    pts = [(cx + x * s * max(larg, 0.05), cy + y * s) for x, y in CARTA]
    g, h = icone(T, pts, k, 0.3)
    if u >= 1:
        h = h + T.polys([([(cx + x * s * 0.75, cy + y * s * 0.75) for x, y in CARTA], 1.0)]) * 0.12 * k
    return g, h


def carta_yugi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.82, 1)
    s = surge(t, 0.0, 0.3)
    if s > 0:
        tri = [(0, 0.25 * s), (-0.3 * s, -0.27 * s), (0.3 * s, -0.27 * s)]
        G += T.polyline(tri + [tri[0]], 0.02) * 0.9 * k + T.gauss(0, -0.08, 0.35) * 0.3 * k
        olho = [(0.08 * s * math.cos(a), -0.12 * s + 0.035 * s * math.sin(a)) for a in np.linspace(0, TAU, 16, endpoint=False)]
        G += T.polyline(olho + [olho[0]], 0.01) * k
    g, h = _carta_virando(T, t, 0.15, 0.55, 0, 0.05, 0.28, k)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.55, 0.8, 0, 0.05, 0.8)
    G += particulas(T, t, 0.5, 1.0, 26, 4, 0, 0.1, 0.4, 0.5)
    return (G + g) * env, (H + h) * env


def olhos_azuis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.45, 0.6)
    g, h = _carta_virando(T, t, 0.0, 0.3, -0.45, -0.35, 0.32, k)
    G, H = G + g, H + h
    u = rel(t, 0.35, 0.9)
    if 0 < u < 1:
        kk = ease_out(rel(u, 0, 0.2)) * (1 - rel(u, 0.6, 1))
        x0, y0, x1, y1 = -0.9, -0.9, 0.1, 0.1
        n = 30
        for j in range(n):
            v = j / n
            x, y = x0 + (x1 - x0) * v, y0 + (y1 - y0) * v
            G += T.gauss(x, y, 0.07 + 0.05 * v) * 0.18 * kk
            H += T.gauss(x, y, 0.03 + 0.02 * v) * 0.18 * kk
        G += raios(T, t, 0.35, 0.9, 4, 3, 0.1, 0.1, 0.3)
        G += T.gauss(0.1, 0.1, 0.2) * kk * 1.2
    G += anel(T, t, 0.5, 0.9, 0.1, 0.7, 0.04, 0.1)
    return G * env, H * env


def cinetico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    G += converge(T, t, 0.0, 0.4, 24, 6, 0, 0, 0.7, 0.014)
    carga = rel(t, 0.0, 0.4) * (1 - rel(t, 0.42, 0.5))
    G += T.gauss(0, 0, 0.12 + 0.1 * carga) * carga * 1.2
    H += T.gauss(0, 0, 0.05) * carga * 1.5
    g, h = clarao(T, t, 0.4, 0.62, 0, 0, 0.9, 1.3)
    G, H = G + g, H + h
    G += anel(T, t, 0.42, 0.85, 0.1, 0.85, 0.06) + anel(T, t, 0.5, 0.95, 0.1, 0.6, 0.03)
    G += estouro(T, t, 0.42, 0.85, 20, 8, 0, 0, 0.75)
    for j in range(3):
        g, h = corte(T, t, 0.55 + 0.04 * j, 0.8 + 0.04 * j, 1.2, 0.8, 0.05, -0.15 + 0.15 * j, 0.0, 0.08)
        G, H = G + g, H + h
    return G * env, H * env


def hex_(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = (1 - rel(t, 0.8, 1))
    for j in range(5):
        u = ease_out(rel(t, 0.0 + 0.05 * j, 0.5 + 0.05 * j), 2)
        if u > 0:
            pts = _espiral(0, 0, 0.05, 0.6 * u, 1.2, TAU * j / 5 + t * 5)
            G += T.polyline(pts, 0.02) * k * 1.1
            H += T.polyline(pts, 0.006) * k * 0.6
            H += T.gauss(pts[-1][0], pts[-1][1], 0.03) * k
    g, h = clarao(T, t, 0.5, 0.75, 0, 0, 0.7)
    G += particulas(T, t, 0.3, 1.0, 30, 11, 0, 0, 0.5, 0.3)
    g2, h2 = aura(T, t, 0.0, 0.9, 0.3)
    return (G + g + g2) * env, (H + h + h2) * env


def joia_da_mente(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    cy = -0.35
    g, h = cheio(T, poe(DIAMANTE, 0, cy, 0.1 * s), 1.2 * s)
    G, H = G + g + T.gauss(0, cy, 0.12) * s * 0.7, H + h * 2
    u = rel(t, 0.25, 0.85)
    if 0 < u < 1:
        segs = []
        for j in range(9):
            a = math.pi / 2 + (j - 4) * 0.22
            segs.append((0, cy, 1.2 * ease_out(u) * math.cos(a), cy + 1.2 * ease_out(u) * math.sin(a), 1.0))
        G += T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.07) * (1 - u) * 0.9
    for j in range(3):
        G += anel(T, t, 0.4 + 0.12 * j, 0.85 + 0.05 * j, 0.1, 0.6, 0.025, -0.1)
    return G * env, H * env


def energia_absorvida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    G += converge(T, t, 0.0, 0.45, 26, 13, 0, -0.05, 0.75)
    s = surge(t, 0.1, 0.35) * (1 - rel(t, 0.85, 1))
    g, h = cheio(T, poe(estrela_pts(8, 0.35), 0, -0.05, 0.14 * s, t), 1.2 * s)
    G, H = G + g + T.gauss(0, -0.05, 0.16) * s * 0.6, H + h * 2
    sobe = rel(t, 0.4, 0.95)
    if 0 < sobe < 1:
        for j in range(9):
            x = -0.35 + 0.0875 * j
            alt = (0.35 + 0.15 * math.sin(j * 1.7 + t * 25)) * ease_out(sobe)
            G += T.polys([(lamina(x, 0.3, x + 0.03 * math.sin(j + t * 10), 0.3 - alt, 0.05), 1.0)]) * (1 - sobe) * 0.9
    g2, h2 = clarao(T, t, 0.38, 0.6, 0, -0.05, 0.9)
    return (G + g2) * env, (H + h2) * env


def _caveira(cx, cy, s):
    cabeca = [(cx + s * 0.5 * math.cos(a), cy - s * 0.15 + s * 0.45 * math.sin(a)) for a in np.linspace(math.pi * 0.85, math.pi * 2.15, 18)]
    cabeca += [(cx + s * 0.28, cy + s * 0.35), (cx + s * 0.28, cy + s * 0.55), (cx - s * 0.28, cy + s * 0.55), (cx - s * 0.28, cy + s * 0.35)]
    olhos = [(cx + lado * s * 0.2, cy - s * 0.05) for lado in (-1, 1)]
    dentes = [(cx + s * (-0.2 + 0.1 * j), cy + s * 0.35, cx + s * (-0.2 + 0.1 * j), cy + s * 0.55, 1.0) for j in range(5)]
    return cabeca, olhos, dentes


def interrogatorio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.05, 0.35)
    k = 1 - rel(t, 0.8, 1)
    if s > 0:
        cab, olhos, dentes = _caveira(0, -0.1, 0.55 * s)
        G += T.polyline(cab + [cab[0]], 0.022) * 1.3 * k
        for x, y in olhos:
            G += T.gauss(x, y, 0.06 * s, 0.075 * s) * 1.0 * k
            H += T.gauss(x, y, 0.025 * s) * k
        G += T.lines(dentes, 0.012) * k
    for j in range(5):
        a0 = 0.35 + 0.07 * j
        u = rel(t, a0, a0 + 0.12)
        if 0 < u < 1:
            y = -0.4 + 0.2 * j
            x = -1 + 2 * u
            G += T.tapered([(x - 0.4, y, x, y, 1.0)], 0.02) * 1.4
            H += T.gauss(x, y, 0.015) * 1.2
    return G * env, H * env


def pecados(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2.5)
    k = 1 - rel(t, 0.8, 1)
    if abre > 0:
        r = 0.62 * abre
        for j in range(18):
            a = TAU * j / 18 + t * 8
            x, y = r * math.cos(a), 0.05 + r * math.sin(a) * 0.45
            G += T.ring(0.05, 0.012, x, y, 1.6 if j % 2 else 0.6) * k * 1.3
            g, h = icone(T, poe([(px * 0.6, py) for px, py in [(0, -1), (0.4, -0.3), (0.5, 0.3), (0, 0.7), (-0.5, 0.3), (-0.4, -0.3)]], x, y - 0.1, 0.13 * (0.8 + 0.3 * math.sin(t * 40 + j))), k * 0.9, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.2, 1.0, 40, 31, 0, 0.0, 0.5, 0.7)
    g, h = aura(T, t, 0.0, 1.0, 0.3)
    return (G + g) * env, (H + h) * env


def cacador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.55)
    if 0 < u < 1:
        x = -0.85 + 0.85 * ease_out(u, 2)
        ang = t * 30
        for lado in (0, math.pi):
            P = T.polys([(lamina(x, 0, x + 0.45 * math.cos(ang + lado), 0.45 * math.sin(ang + lado), 0.11), 1.0)])
            G += P * 1.2
            H += P * 0.6
        G += T.ring(0.05, 0.015, x, 0) * 1.2
        G += T.ring(0.3, 0.02, x, 0) * 0.35
    for j in range(2):
        g, h = corte(T, t, 0.5 + 0.08 * j, 0.75 + 0.08 * j, 0.6 - 1.2 * j, 1.1, 0.07)
        G, H = G + g, H + h
    v = rel(t, 0.55, 1.0)
    if 0 < v < 1:
        q = np.random.default_rng(8)
        pts = [(q.normal(0, 0.15 + 0.2 * v), q.normal(0, 0.12 + 0.15 * v), (1 - v) * q.uniform(0.3, 1)) for _ in range(50)]
        G += T.splats(pts, 0.03) * 0.8
    return G * env, H * env


def crescentes(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    gira = rel(t, 0.0, 0.5)
    k = 1 - rel(t, 0.9, 1)
    if gira < 1:
        g, h = orbita(T, t, LUA, 5, 0.55 - 0.1 * gira, 9, 0.13 * min(1, gira * 4), 0, 0, 0.6, 1.3, True)
        G, H = G + g, H + h
    for j in range(5):
        a = TAU * j / 5 + 9 * 0.5
        u = ease_in(rel(t, 0.5 + 0.04 * j, 0.68 + 0.04 * j), 2)
        if 0 < u < 1:
            r = 0.4 * (1 - u)
            x, y = r * math.cos(a), r * math.sin(a) * 0.6
            g, h = icone(T, poe(LUA, x, y, 0.12, a), 1.3)
            G, H = G + g, H + h
            G += T.tapered([(x * 1.8, y * 1.8, x, y, 0.8)], 0.04)
    g, h = clarao(T, t, 0.68, 0.9, 0, 0, 0.6)
    G += anel(T, t, 0.68, 0.95, 0.05, 0.45, 0.03)
    return (G + g) * env * k, (H + h) * env * k


def raio_rubi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cx, cy = 0, -0.3
    u = rel(t, 0.1, 0.85)
    if 0 < u < 1:
        kk = ease_out(rel(u, 0, 0.1)) * (1 - rel(u, 0.75, 1))
        for j in range(3):
            ang = -0.3 + math.pi * u * 1.4 + j * 0.9 + 0.25 * math.sin(t * 30 + j)
            x2, y2 = cx + 1.4 * math.cos(ang), cy + 1.4 * math.sin(ang)
            G += T.lines([(cx, cy, x2, y2, 1.0)], 0.09) * 0.8 * kk + T.lines([(cx, cy, x2, y2, 1.0)], 0.04) * 0.8 * kk
            H += T.lines([(cx, cy, x2, y2, 1.0)], 0.018) * 1.4 * kk
        H += T.gauss(cx, cy, 0.06) * kk * 2
        G += T.gauss(cx, cy, 0.15) * kk * 1.2
    g, h = clarao(T, t, 0.08, 0.25, cx, cy, 0.8)
    return (G + g) * env, (H + h) * env


def elo_mental(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.45), 2.2)
    k = 1 - rel(t, 0.8, 1)
    if s > 0:
        bate = 0.12 * math.sin(t * 14)
        for lado in (-1, 1):
            asa = [(lado * x * 0.75 * s, -0.12 + (y + bate * x) * 0.55 * s) for x, y in ASA]
            g, h = icone(T, asa, k, 0.4)
            G, H = G + g, H + h
        corpo = [(0, -0.35 * s), (0.06 * s, -0.1), (0.04 * s, 0.25 * s), (0, 0.5 * s), (-0.04 * s, 0.25 * s), (-0.06 * s, -0.1)]
        g, h = cheio(T, corpo, k)
        G, H = G + g, H + h
        G += T.gauss(0, -0.05, 0.3 * s) * 0.4 * k
    u = rel(t, 0.4, 0.85)
    if 0 < u < 1:
        pts = [(-0.8 + 1.6 * v, 0.45 + 0.04 * math.sin(v * 20 - t * 30)) for v in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.015) * pulso(u, 0, 1) * 1.4
        for x in (-0.8, 0.8):
            H += T.gauss(x, 0.45, 0.04) * pulso(u, 0, 1) * 1.5
    return G * env, H * env


def toque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(19)
    u = rel(t, 0.05, 0.7)
    if 0 < u < 1:
        pts = []
        for j in range(60):
            fase = (u * 1.4 + q.uniform(0, 1)) % 1
            x = 0.9 - 0.9 * fase
            y = q.normal(0, 0.06) * (1 - fase) + 0.12 * math.sin(fase * 9 + j)
            pts.append((x, y, 0.4 + 0.6 * fase))
        G += T.splats(pts, 0.018) * 1.3 * (1 - rel(u, 0.85, 1))
        G += T.gauss(0.9, 0, 0.12) * (1 - u) * 0.8
    abs_ = rel(t, 0.2, 0.75)
    G += T.gauss(0, 0, 0.1 + 0.15 * abs_) * abs_ * 0.9 * (1 - rel(t, 0.8, 1))
    H += T.gauss(0, 0, 0.05) * abs_ * 1.2 * (1 - rel(t, 0.8, 1))
    G += anel(T, t, 0.65, 0.95, 0.05, 0.5, 0.03)
    return G * env, H * env


def carta_carregada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.45)
    if u < 1:
        x, y = -0.7 + 0.7 * ease_out(u, 2), -0.1 * math.sin(math.pi * u)
        brilho = 0.6 + 0.6 * u
        pts = poe(CARTA, x, y, 0.22, t * 18)
        g, h = icone(T, pts, brilho, 0.5)
        G, H = G + g + T.gauss(x, y, 0.15) * brilho * 0.6, H + h + T.gauss(x, y, 0.05) * brilho
        G += particulas(T, t, 0.0, 0.45, 20, 3, x, y, 0.15, 0.1)
    g, h = clarao(T, t, 0.45, 0.7, 0, 0, 1.0, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.45, 0.85, 0.05, 0.8, 0.05) + estouro(T, t, 0.45, 0.85, 22, 5, 0, 0, 0.75)
    G += particulas(T, t, 0.5, 1.0, 40, 17, 0, 0, 0.5, -0.2)
    return G * env, H * env


def simbionte(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.82, 1)
    q = np.random.default_rng(27)
    for j in range(7):
        u = ease_out(rel(t, 0.0 + 0.04 * j, 0.5 + 0.04 * j), 2)
        if u > 0:
            a = TAU * j / 7 + q.uniform(-0.3, 0.3)
            pts = [(0.6 * v * u * math.cos(a + 0.4 * math.sin(v * 5 + t * 6)), 0.6 * v * u * math.sin(a + 0.4 * math.sin(v * 5 + t * 6))) for v in np.linspace(0, 1, 14)]
            for i in range(len(pts) - 1):
                G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.05 * (1 - i / 14) + 0.01) * k * 0.9
    s = surge(t, 0.3, 0.55) * k
    if s > 0:
        corpo = [(0.05 * math.cos(a) * s * 2, -0.1 + 0.11 * math.sin(a) * s * 2) for a in np.linspace(0, TAU, 14, endpoint=False)]
        g, h = cheio(T, corpo, 1.2 * s)
        G, H = G + g, H + h * 2
        segs = []
        for lado in (-1, 1):
            for j in range(4):
                y0 = -0.2 + 0.07 * j
                segs.append((lado * 0.08 * s, y0, lado * 0.3 * s, y0 - 0.15 * s + 0.12 * j * s, 1.0))
                segs.append((lado * 0.3 * s, y0 - 0.15 * s + 0.12 * j * s, lado * 0.42 * s, y0 + 0.1 * s + 0.1 * j * s, 1.0))
        G += T.lines(segs, 0.022) * 1.2 * s
    return G * env, H * env


def carnificina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(33)
    for j in range(16):
        a = q.uniform(0, TAU)
        a0 = q.uniform(0.0, 0.25)
        u = ease_out(rel(t, a0, a0 + 0.3), 3)
        if u > 0:
            d = q.uniform(0.5, 0.9) * u
            k = 1 - rel(t, 0.6 + a0, 0.85 + a0)
            P = T.polys([(lamina(0.08 * math.cos(a), 0.08 * math.sin(a), d * math.cos(a + 0.2 * u), d * math.sin(a + 0.2 * u), 0.06), 1.0)])
            G += P * 1.2 * k
            H += P * 0.5 * k
    g, h = clarao(T, t, 0.0, 0.25, tam=1.0, forca=1.3)
    G += particulas(T, t, 0.15, 0.9, 40, 2, 0, 0, 0.4, -0.3)
    return (G + g) * env, (H + h) * env


def doombot(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    quebra = rel(t, 0.5, 0.95)
    if s > 0 and quebra < 1:
        x0 = -0.45
        partes = [[(-0.12, -0.45), (0.12, -0.45), (0.13, -0.2), (-0.13, -0.2)], [(-0.25, -0.17), (0.25, -0.17), (0.2, 0.2), (-0.2, 0.2)],
                  [(-0.18, 0.22), (-0.04, 0.22), (-0.06, 0.5), (-0.18, 0.5)], [(0.04, 0.22), (0.18, 0.22), (0.18, 0.5), (0.06, 0.5)]]
        for j, p in enumerate(partes):
            a = TAU * j / 4 + 0.5
            dx, dy = 0.5 * quebra * math.cos(a), 0.5 * quebra * math.sin(a) + 0.4 * quebra * quebra
            g, h = icone(T, poe(p, x0 + dx, dy, s, quebra * (j - 1.5) * 1.5), 1 - quebra, 0.45)
            G, H = G + g, H + h
        olhos = (1 - quebra)
        H += (T.gauss(x0 - 0.05, -0.34, 0.02, 0.008) + T.gauss(x0 + 0.05, -0.34, 0.02, 0.008)) * olhos * 3
    u = ease_in(rel(t, 0.3, 0.5), 2)
    if 0 < u < 1:
        G += T.tapered([(0.9, 0, 0.9 - 1.3 * u, 0, 1.0)], 0.06)
    g, h = clarao(T, t, 0.48, 0.7, -0.45, -0.1, 0.8, 1.3)
    G += particulas(T, t, 0.5, 1.0, 30, 7, -0.45, 0, 0.25, -0.3)
    return (G + g) * env, (H + h) * env


def ilusao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(41)
    quebra = rel(t, 0.1, 0.6)
    k0 = 1 - rel(t, 0.0, 0.1) * 0
    for j in range(14):
        a = q.uniform(0, TAU)
        r = q.uniform(0.05, 0.35)
        cx, cy = r * math.cos(a), r * math.sin(a) * 1.2
        caco = [(cx + 0.08 * math.cos(a + b), cy + 0.08 * math.sin(a + b)) for b in (0, 2.2, 4.0)]
        d = 0.6 * ease_out(quebra)
        g, h = icone(T, poe([(x - cx, y - cy) for x, y in caco], cx + d * math.cos(a), cy + d * math.sin(a) + 0.3 * quebra * quebra, 1.0, quebra * 4), (1 - quebra) * k0 if quebra > 0 else 0.7, 0.4)
        G, H = G + g, H + h
    nevoa = pulso(t, 0.3, 1.0)
    if nevoa > 0:
        pts = [(q.normal(0, 0.3), q.normal(0.1, 0.2), q.uniform(0.3, 1)) for _ in range(40)]
        G += T.splats(pts, 0.06) * nevoa * 0.5
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            chifre = [(lado * (0.08 + 0.25 * v + 0.05 * math.sin(v * 3)), -0.25 - 0.45 * v * v) for v in np.linspace(0, 1, 10)]
            G += T.polyline([(x * s, -0.1 + (y + 0.1) * s) for x, y in chifre], 0.035 * s) * 1.3
        G += T.arc_band(0.2 * s, 0.04, math.pi * 1.05, math.pi * 1.95, 1.0, 0.0, 0, -0.1) * 1.2 if hasattr(T, "arc_band") else 0
    return G * env, H * env


def corpo_novo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(51)
    junta = ease_in(rel(t, 0.0, 0.45), 1.6)
    for j in range(22):
        a = q.uniform(0, TAU)
        d = 0.8 * (1 - junta) + 0.0
        tx, ty = q.uniform(-0.2, 0.2), q.uniform(-0.45, 0.45)
        x, y = tx + d * math.cos(a), ty + d * math.sin(a)
        caco = poe([(-1, -0.6), (1, -0.6), (0.7, 0.6), (-0.7, 0.6)], x, y, 0.05, a * (1 - junta) * 3)
        g, h = icone(T, caco, 1 - rel(t, 0.7, 0.85), 0.5)
        G, H = G + g, H + h
    scan = rel(t, 0.45, 0.75)
    if 0 < scan < 1:
        y = -0.55 + 1.1 * scan
        G += T.lines([(-0.4, y, 0.4, y, 1.0)], 0.02) * 1.4
        H += T.lines([(-0.4, y, 0.4, y, 1.0)], 0.006) * 1.2
    olhos = pulso(t, 0.7, 1.0)
    if olhos > 0:
        for lado in (-1, 1):
            H += T.gauss(lado * 0.07, -0.35, 0.05, 0.012) * olhos * 2.5
            G += T.gauss(lado * 0.07, -0.35, 0.09, 0.03) * olhos * 1.2
    g, h = clarao(T, t, 0.42, 0.6, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def _abobora(cx, cy, s):
    return [(cx + s * (1 + 0.08 * math.cos(6 * a)) * math.cos(a), cy + s * 0.85 * (1 + 0.08 * math.cos(6 * a)) * math.sin(a)) for a in np.linspace(0, TAU, 36, endpoint=False)]


def abobora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.4)
    pisca = rel(t, 0.4, 0.55)
    if t < 0.56:
        x, y = -0.8 + 0.8 * min(u, 1), -0.6 * math.sin(math.pi * min(u, 1)) * 0.8
        s = 0.18
        g, h = icone(T, _abobora(x, y, s), 1.2, 0.5)
        G, H = G + g, H + h
        rosto = int(t * 30) % 2 if pisca > 0 else 1
        H += (T.gauss(x - 0.04, y - 0.02, 0.015) + T.gauss(x + 0.04, y - 0.02, 0.015) + T.gauss(x, y + 0.04, 0.035, 0.01)) * (1.5 + rosto) * 0.8
        G += T.lines([(x, y - s * 0.85, x + 0.02, y - s * 1.2, 1.0)], 0.012)
    g, h = clarao(T, t, 0.55, 0.78, 0, 0, 1.1, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.55, 0.9, 0.05, 0.85, 0.06) + estouro(T, t, 0.55, 0.9, 18, 21, 0, 0, 0.7)
    G += particulas(T, t, 0.58, 1.0, 40, 23, 0, 0, 0.45, 0.4, 0.025)
    return G * env, H * env


REGISTRO = [
    ("mu_mana", mana, GRANDE, "Frieren · o círculo mágico e as flores de mana", False),
    ("mu_waku", waku, GRANDE, "Anya · as ondas da leitura de mente e as estrelinhas", False),
    ("mu_strix", strix, GRANDE, "Loid · a mira travando e as barras de Carga", False),
    ("mu_espinho", espinho, GRANDE, "Yor · o espinho dourado e as pétalas", False),
    ("mu_nivel", nivel, GRANDE, "Jinwoo · a janela do sistema: subiu de nível", False),
    ("mu_kakuja", kakuja, GRANDE, "Kaneki · os tentáculos de kagune e o olho de ghoul", False),
    ("mu_carta_yugi", carta_yugi, GRANDE, "Yugi · a carta virando e o Enigma do Milênio", False),
    ("mu_olhos_azuis", olhos_azuis, GRANDE, "Kaiba · a carta do Dragão Branco e o raio", False),
    ("mu_cinetico", cinetico, GRANDE, "Pantera Negra · a onda cinética roxa e as garras", False),
    ("mu_hex", hex_, GRANDE, "Feiticeira Escarlate · os fios da magia do caos", False),
    ("mu_joia_da_mente", joia_da_mente, GRANDE, "Visão · a Joia da Mente e o leque de luz", False),
    ("mu_energia_absorvida", energia_absorvida, GRANDE, "Capitã Marvel · a estrela e as chamas de fótons", False),
    ("mu_interrogatorio", interrogatorio, GRANDE, "Justiceiro · a caveira e os tiros traçantes", False),
    ("mu_pecados", pecados, GRANDE, "Motoqueiro Fantasma · a corrente em chamas", False),
    ("mu_cacador", cacador, GRANDE, "Blade · a glaive girando e os cortes", False),
    ("mu_crescentes", crescentes, GRANDE, "Cavaleiro da Lua · os crescentes de prata", False),
    ("mu_raio_rubi", raio_rubi, GRANDE, "Ciclope · o raio sem controle varrendo", False),
    ("mu_elo_mental", elo_mental, GRANDE, "Jean Grey · a Fênix e o elo mental", False),
    ("mu_toque", toque, GRANDE, "Vampira · a energia roubada correndo", False),
    ("mu_carta_carregada", carta_carregada, GRANDE, "Gambit · a carta carregada explodindo", False),
    ("mu_simbionte", simbionte, GRANDE, "Venom · a gosma e a aranha branca", False),
    ("mu_carnificina", carnificina, GRANDE, "Carnificina · as lâminas vermelhas para todo lado", False),
    ("mu_doombot", doombot, GRANDE, "Doutor Destino · o Doombot que se parte", False),
    ("mu_ilusao", ilusao, GRANDE, "Loki · a imagem quebrando e os chifres", False),
    ("mu_corpo_novo", corpo_novo, GRANDE, "Ultron · o corpo novo se montando", False),
    ("mu_abobora", abobora, GRANDE, "Duende Verde · a bomba-abóbora explodindo", False),
]
