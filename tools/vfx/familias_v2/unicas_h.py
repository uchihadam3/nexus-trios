"""Rodada 7 das Mecânicas únicas ativando como habilidade: Sailor Moon, Coringa, Arlequina, Lex Luthor, Invencível,
Omni-Man, Raphael, Donatello, Michelangelo, Constantine, Pica-Pau, Pernalonga, Aang, Samurai Jack, He-Man, Popeye,
Optimus Prime, Salsicha, Bob Esponja, Scooby-Doo, Rick, Finn, Megatron, Docinho, Mickey e Pato Donald.

- cristal_prata: a lua crescente e o Cristal de Prata acendem, com as penas de luz.
- hahaha: a carta do Coringa vira e o gás do riso verde se espalha em espirais.
- imprevisivel: o martelão gira e os corações e losangos voam.
- odio_herois: os cristais de kryptonita crescem e pulsam.
- viltrumita: o Invencível sobe rasgando o céu, com o estrondo sônico.
- orgulho_viltrumita: o soco de cima para baixo e a cratera.
- bravo: os dois sais cruzam e o símbolo de raiva pulsa.
- contencao: o campo de contenção de hexágonos fecha.
- improviso: o nunchaku gira e a fatia de pizza aparece.
- exorcismo: o pentagrama de Constantine acende e a fumaça sobe.
- pica_pau: o bico bica rápido e as lascas de madeira voam.
- pernalonga: a cenoura aparece sobre o buraco e brilha.
- planador: as espirais de ar giram e o planador abre.
- lamina_magica: o corte limpo e único da lâmina, e o escudo partido.
- grayskull: a Espada do Poder erguida recebe o raio.
- espinafre: a lata de espinafre abre e a âncora do braço acende.
- matriz: a Matriz da Liderança abre e solta a luz.
- poder_escondido: o 1% do poder — a aura sobe calma e enorme.
- esponja: as bolhas sobem e as gotas de cura caem nos aliados.
- scooby_lanche: o biscoito voa, é pego no ar e os corações sobem.
- portal_rick: o portal verde gira como líquido.
- heroi_finn: o chapéu de urso e a espada brilhando.
- canhao_fusao: o canhão de fusão carrega roxo e dispara.
- briguenta: o rastro verde corta e o soco estoura.
- vassoura: as vassouras encantadas marcham sob o chapéu de feiticeiro.
- quaaack: os socos de raiva, os rabiscos e o vapor.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (CARTA, CORACAO, DIAMANTE, ESPADA, FOLHA, GEMA, LUA, OSSO, PENA, anel, aura, cheio, chuva, circulo,
                         clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def cristal_prata(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = icone(T, poe(LUA, 0, -0.25, 0.35 * s, math.pi / 2 + 0.3), 1.1, 0.4)
        G, H = G + g, H + h
        g, h = cheio(T, poe(DIAMANTE, 0, 0.05, 0.13 * s), 1.4)
        G, H = G + g + T.gauss(0, 0.05, 0.2 * s) * 0.6, H + h * 2
    g, h = chuva(T, t, 0.2, 1.0, PENA, 10, 3, 0.05, -0.7, 0.45, 0.6, 2.0, 1.0)
    G, H = G + g, H + h
    G += particulas(T, t, 0.25, 1.0, 30, 9, 0, 0.0, 0.45, 0.4)
    g, h = clarao(T, t, 0.3, 0.55, 0, 0.05, 0.8)
    return (G + g) * env, (H + h) * env


def hahaha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.35)
    larg = abs(math.cos(math.pi * (1 - ease_out(u, 2)) * 1.5)) if u < 1 else 1.0
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        g, h = icone(T, [(x * 0.38 * max(larg, 0.05), -0.15 + y * 0.38) for x, y in CARTA], k * 1.2, 0.4)
        G, H = G + g, H + h
        if u >= 1:
            G += T.polyline(_espiral(0, -0.15, 0.01, 0.12, 2, t * 6), 0.012) * k
    q = np.random.default_rng(13)
    gas = rel(t, 0.35, 1.0)
    if gas > 0:
        for j in range(6):
            a = TAU * j / 6 + q.uniform(-0.3, 0.3)
            d = 0.55 * ease_out(gas)
            cx, cy = d * math.cos(a), d * math.sin(a) * 0.7
            G += T.gauss(cx, cy, 0.12 + 0.1 * gas) * (1 - gas) * 0.8
            G += T.polyline(_espiral(cx, cy, 0.01, 0.1, 1.5, t * 10 + j), 0.01) * (1 - gas)
    return G * env, H * env


def imprevisivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    gira = ease_in(rel(t, 0.0, 0.4), 1.6)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        ang = -2.2 + 2.6 * gira
        cx, cy = 0.0, 0.35
        hx, hy = cx + 0.6 * math.cos(ang), cy + 0.6 * math.sin(ang)
        G += T.lines([(cx, cy, hx, hy, 1.0)], 0.05) * k
        cabeca = poe([(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)], hx, hy, 0.22, ang + math.pi / 2)
        g, h = icone(T, cabeca, k * 1.3, 0.5)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.38, 0.58, 0.25, -0.15, 1.0, 1.4)
    G, H = G + g, H + h
    q = np.random.default_rng(3)
    for j in range(10):
        u = rel(t, 0.4, 0.95)
        if 0 < u < 1:
            a = q.uniform(0, TAU)
            d = 0.7 * ease_out(u) * q.uniform(0.6, 1)
            forma = CORACAO if j % 2 == 0 else DIAMANTE
            g, h = cheio(T, poe(forma, 0.25 + d * math.cos(a), -0.15 + d * math.sin(a) + 0.2 * u * u, 0.05, a), (1 - u) * 1.2)
            G, H = G + g, H + h
    return G * env, H * env


def odio_herois(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(7)
    k = 1 - rel(t, 0.85, 1)
    for j in range(6):
        a = -math.pi / 2 + (j - 2.5) * 0.35
        cresce = ease_out(rel(t, 0.05 * j, 0.35 + 0.05 * j), 2)
        if cresce > 0:
            comp = q.uniform(0.25, 0.45) * cresce
            base = (0.06 * math.cos(a), 0.25 + 0.06 * math.sin(a))
            pts = [(base[0] - 0.04 * math.sin(a), base[1] + 0.04 * math.cos(a)), (base[0] + comp * math.cos(a), base[1] + comp * math.sin(a)), (base[0] + 0.04 * math.sin(a), base[1] - 0.04 * math.cos(a))]
            g, h = icone(T, pts, k * 1.2, 0.55)
            G, H = G + g, H + h
    pulsa = pulso(t, 0.3, 1.0)
    G += T.gauss(0, 0.05, 0.25) * pulsa * 0.6 * (0.7 + 0.3 * math.sin(t * 40))
    for j in range(3):
        G += anel(T, t, 0.35 + 0.15 * j, 0.8 + 0.07 * j, 0.1, 0.65, 0.03, 0.1)
    return G * env, H * env


def viltrumita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.05, 0.45), 1.8)
    if 0 < u < 1:
        y = 0.4 - 1.5 * u
        G += T.tapered([(0, 0.45, 0, y, 1.0)], 0.12) * 1.1 + T.gauss(0, y, 0.08) * 1.2
        H += T.gauss(0, y, 0.035) * 1.6
    G += anel(T, t, 0.25, 0.6, 0.05, 0.6, 0.05, -0.3, 2.5) + anel(T, t, 0.3, 0.7, 0.05, 0.8, 0.03, -0.3, 2.5)
    g, h = clarao(T, t, 0.25, 0.45, 0, -0.3, 0.9)
    G += particulas(T, t, 0.3, 0.9, 30, 3, 0, 0.3, 0.4, -0.3, 0.015)
    q = np.random.default_rng(5)
    for j in range(5):
        v = rel(t, 0.45 + 0.04 * j, 0.95)
        if 0 < v < 1:
            a = q.uniform(0, TAU)
            d = 0.5 * ease_out(v)
            g2, h2 = cheio(T, poe([(0, -1), (0.6, 0.4), (-0.6, 0.4)], d * math.cos(a), -0.1 + d * math.sin(a) + 0.4 * v * v, 0.04), (1 - v))
            G, H = G + g2, H + h2
    return (G + g) * env, (H + h) * env


def orgulho_viltrumita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.2)
    if 0 < u < 1:
        y = -0.95 + 1.3 * u
        G += T.tapered([(0, -1.0, 0, y, 1.0)], 0.2) * 0.9 + T.gauss(0, y, 0.12) * 1.3
        H += T.gauss(0, y, 0.05) * 1.6
    g, h = clarao(T, t, 0.33, 0.55, 0, 0.35, 1.3, 1.8)
    G, H = G + g, H + h
    q = np.random.default_rng(9)
    racha = rel(t, 0.35, 0.6)
    if racha > 0:
        for j in range(8):
            a = math.pi * j / 7
            G += T.polyline(jagged(q, 0, 0.35, 0.8 * racha * math.cos(a), 0.35 + 0.2 * racha * math.sin(a), 3, 0.3), 0.016) * (1 - rel(t, 0.85, 1)) * 1.2
    G += onda_no_chao(T, t, 0.35, 0.8, 0.95, 0.38) + onda_no_chao(T, t, 0.4, 0.9, 0.7, 0.38)
    G += particulas(T, t, 0.36, 1.0, 50, 7, 0, 0.35, 0.6, 0.4, 0.02)
    return G * env, H * env


def _sai(cx, cy, s, ang):
    return poe([(0, -1), (0.05, -0.3), (0.3, -0.45), (0.25, -0.2), (0.07, -0.1), (0.06, 0.5), (-0.06, 0.5), (-0.07, -0.1), (-0.25, -0.2), (-0.3, -0.45),
                (-0.05, -0.3)], cx, cy, s, ang)


def bravo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cruza = ease_out(rel(t, 0.0, 0.3), 3)
    k = 1 - rel(t, 0.55, 0.7)
    for lado in (-1, 1):
        ang = lado * (0.2 + 0.6 * cruza)
        g, h = icone(T, _sai(lado * 0.15 * (1 - cruza), 0.05, 0.62, ang), k * 1.3, 0.45)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.25, 0.45, 0, -0.15, 0.7)
    G, H = G + g, H + h
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.85, 1)) * (1 + 0.15 * math.sin(t * 40))
    if s > 0:
        cx, cy = 0.25, -0.45
        for j in range(4):
            a = TAU * j / 4 + math.pi / 4
            pts = [(cx + 0.12 * s * math.cos(a + 0.6 * (v - 0.5)) + 0.04 * s * math.cos(a) * (1 - abs(v - 0.5) * 2) * -1,
                    cy + 0.12 * s * math.sin(a + 0.6 * (v - 0.5)) + 0.04 * s * math.sin(a) * (1 - abs(v - 0.5) * 2) * -1) for v in np.linspace(0, 1, 8)]
            G += T.polyline(pts, 0.03) * 1.4
    return G * env, H * env


def contencao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = ease_out(rel(t, 0.1, 0.5), 2)
    k = 1 - rel(t, 0.82, 1)
    segs = []
    for j in range(-3, 4):
        for i in range(-3, 4):
            cx = i * 0.12 + (0.06 if j % 2 else 0)
            cy = j * 0.105
            d = math.hypot(cx, cy)
            if d > 0.45:
                continue
            aparece = rel(fecha, d / 0.45 * 0.6, d / 0.45 * 0.6 + 0.4)
            if aparece <= 0:
                continue
            hexa = [(cx + 0.065 * math.cos(TAU * m / 6 + math.pi / 6), cy + 0.065 * math.sin(TAU * m / 6 + math.pi / 6)) for m in range(6)]
            segs += [(hexa[m][0], hexa[m][1], hexa[(m + 1) % 6][0], hexa[(m + 1) % 6][1], aparece) for m in range(6)]
    if segs:
        G += T.lines(segs, 0.01) * k * 1.3
        H += T.lines(segs, 0.003) * k * 0.6
    G += T.ring(0.48, 0.025, 0, 0) * fecha * k * 1.2
    u = ease_in(rel(t, 0.0, 0.2), 1.5)
    if t < 0.3:
        G += T.lines([(-0.9 + 0.5 * u, 0.5 - 0.5 * u, -0.5 + 0.5 * u, 0.1 - 0.5 * u, 1.0)], 0.03)
    return G * env, H * env


def improviso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        a = t * 28
        cx, cy = 0.0, -0.05
        x1, y1 = cx + 0.08 * math.cos(a), cy + 0.08 * math.sin(a)
        x2, y2 = cx + 0.4 * math.cos(a), cy + 0.4 * math.sin(a)
        G += T.lines([(cx - 0.35, cy + 0.1, cx - 0.05, cy + 0.02, 1.0)], 0.05) * k + T.lines([(x1, y1, x2, y2, 1.0)], 0.05) * k * 1.2
        G += T.lines([(cx - 0.05, cy + 0.02, x1, y1, 1.0)], 0.01) * k
        for r in range(1, 4):
            aa = a - 0.3 * r
            G += T.lines([(cx + 0.08 * math.cos(aa), cy + 0.08 * math.sin(aa), cx + 0.4 * math.cos(aa), cy + 0.4 * math.sin(aa), 1.0)], 0.04) * k * 0.25 / r
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.85, 1))
    if s > 0:
        fatia = [(0, -0.35 * s), (0.25 * s, 0.2 * s), (-0.25 * s, 0.2 * s)]
        g, h = icone(T, fatia, 1.2, 0.45)
        G, H = G + g, H + h
        G += T.lines([(-0.27 * s, 0.24 * s, 0.27 * s, 0.24 * s, 1.0)], 0.05 * s) * 1.1
        for dx, dy in ((-0.05, 0.05), (0.07, 0.08), (0.0, -0.1)):
            H += T.gauss(dx * s * 1.4, dy * s * 1.4, 0.025 * s) * 1.4
    return G * env, H * env


def exorcismo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    desenha = ease_out(rel(t, 0.0, 0.45), 1.6)
    k = 1 - rel(t, 0.82, 1)
    r = 0.42
    pts5 = [(r * math.cos(-math.pi / 2 + TAU * (2 * j % 5) / 5), 0.05 + r * math.sin(-math.pi / 2 + TAU * (2 * j % 5) / 5)) for j in range(6)]
    n = max(2, int(desenha * 6 + 0.5))
    G += T.polyline(pts5[:n], 0.016) * k * 1.4
    G += T.ring(r * 1.08, 0.015, 0, 0.05) * desenha * k * 1.2
    H += T.polyline(pts5[:n], 0.005) * k
    q = np.random.default_rng(31)
    fumo = rel(t, 0.3, 1.0)
    if fumo > 0:
        for j in range(3):
            x0 = q.uniform(-0.3, 0.3)
            pts = [(x0 + 0.08 * math.sin(v * 6 + t * 5 + j), 0.3 - 0.8 * v * fumo, (1 - v) * (1 - fumo) * 0.7) for v in np.linspace(0, 1, 14)]
            G += T.splats(pts, 0.05) * 0.7
    g, h = clarao(T, t, 0.45, 0.65, 0, 0.05, 0.8)
    return (G + g) * env, (H + h) * env


def pica_pau(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(3)
    for j in range(5):
        a0 = 0.05 + 0.12 * j
        k = pulso(t, a0, a0 + 0.12)
        if k > 0:
            x = -0.15 + 0.25 * k
            bico = [(x + 0.1, -0.1), (x - 0.5, -0.24), (x - 0.5, 0.04)]
            g, h = cheio(T, bico, 1.1)
            G, H = G + g, H + h
            H += T.gauss(x + 0.02, -0.1, 0.03) * k * 2
            G += T.gauss(x + 0.02, -0.1, 0.08) * k
            for m in range(4):
                a = q.uniform(-1.2, 1.2)
                d = 0.3 * k
                g2, h2 = cheio(T, poe([(-1, -0.4), (1, -0.4), (1, 0.4), (-1, 0.4)], x + 0.05 + d * math.cos(a), -0.1 + d * math.sin(a), 0.025, a * 3), 1 - k * 0.3)
                G, H = G + g2, H + h2
    G += particulas(T, t, 0.6, 1.0, 20, 9, 0.1, -0.1, 0.3, -0.3, 0.012)
    return G * env, H * env


def pernalonga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    buraco = ease_out(rel(t, 0.0, 0.25), 2) * (1 - rel(t, 0.85, 1))
    G += T.ring(0.25 * buraco, 0.02, 0, 0.35, 3.0) * 1.2 + T.gauss(0, 0.35, 0.22 * buraco + 0.001, 0.07 * buraco + 0.001) * 0.4
    sobe = ease_out(rel(t, 0.2, 0.5), 2.5)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        y = 0.35 - 0.6 * sobe
        cenoura = [(0, y + 0.3), (0.07, y - 0.08), (-0.07, y - 0.08)]
        g, h = icone(T, cenoura, k * 1.2, 0.6)
        G, H = G + g, H + h
        for a in (-0.4, 0.0, 0.4):
            g2, h2 = icone(T, poe(FOLHA, 0.1 * math.sin(a), y - 0.15, 0.08, a), k, 0.5)
            G, H = G + g2, H + h2
        G += T.lines([(-0.05, y + 0.05, 0.04, y + 0.03, 1.0), (-0.04, y + 0.15, 0.03, y + 0.13, 1.0)], 0.008) * k
    for j in range(5):
        kk = pulso(t, 0.45 + 0.08 * j, 0.7 + 0.08 * j)
        if kk > 0:
            g, h = cheio(T, poe(estrela_pts(4, 0.3), -0.3 + 0.15 * j, -0.5 + 0.12 * (j % 2), 0.06 * kk), kk * 1.3)
            G, H = G + g, H + h * 2
    return G * env, H * env


def planador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.9)
    for j in range(4):
        pts = _espiral(0, 0, 0.05, 0.55, 1.1, TAU * j / 4 + t * 9)
        for i in range(len(pts) - 1):
            G += T.lines([(pts[i][0], pts[i][1] * 0.7, pts[i + 1][0], pts[i + 1][1] * 0.7, 1.0)], 0.02 * (1 - i / 40) + 0.004) * k
    s = surge(t, 0.2, 0.45) * (1 - rel(t, 0.85, 1))
    if s > 0:
        asa = [(-0.55 * s, 0), (0, -0.15 * s), (0.55 * s, 0), (0, 0.06 * s)]
        g, h = icone(T, [(x, y - 0.35) for x, y in asa], 1.1, 0.4)
        G, H = G + g, H + h
        G += T.lines([(0, -0.5 * s - 0.35 + 0.35, 0, -0.35 + 0.05, 1.0)], 0.012) * s * 0
    G += particulas(T, t, 0.1, 1.0, 30, 5, 0, 0, 0.5, 0.2, 0.012, 0.3)
    return G * env, H * env


def lamina_magica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    pausa = pulso(t, 0.0, 0.3)
    H += T.gauss(-0.3, -0.2, 0.02) * pausa * 2
    G += T.flare(-0.3, -0.2, 0.3 * pausa + 0.01, 0.8, 0.008) * pausa
    g, h = corte(T, t, 0.25, 0.45, 0.0, 1.8, 0.14, 0, 0.0, 0.0)
    G, H = G + g * 1.3, H + h
    linha = pulso(t, 0.4, 0.75)
    G += T.lines([(-0.95, 0, 0.95, 0, 1.0)], 0.02) * linha * 1.4
    H += T.lines([(-0.95, 0, 0.95, 0, 1.0)], 0.006) * linha * 1.5
    q = np.random.default_rng(13)
    parte = rel(t, 0.45, 0.95)
    if parte > 0:
        for j in range(8):
            a = q.uniform(0, math.pi) * (1 if j % 2 else -1)
            lado = 1 if j % 2 else -1
            d = 0.35 * ease_out(parte)
            caco = poe([(-1, 0), (1, -0.5), (0.5, 0.7)], q.uniform(-0.4, 0.4), lado * (0.05 + d) + 0.2 * parte * parte, 0.1, a + parte * 3)
            g2, h2 = icone(T, caco, 1 - parte, 0.4)
            G, H = G + g2, H + h2
    return G * env, H * env


def grayskull(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        g, h = icone(T, poe(ESPADA, 0, 0.35 - 0.3 * sobe, 0.42), k * 1.2, 0.5)
        G, H = G + g, H + h
    raio = pulso(t, 0.25, 0.65)
    if raio > 0:
        q = np.random.default_rng(int(t * 30) % 5 + 1)
        for _ in range(3):
            bolt = jagged(q, q.uniform(-0.4, 0.4), -1.0, 0, -0.42, 5, 0.25)
            G += T.polyline(bolt, 0.035) * raio * 1.3
            H += T.polyline(bolt, 0.01) * raio * 1.5
    g, h = clarao(T, t, 0.3, 0.6, 0, -0.42, 1.0, 1.5)
    G, H = G + g, H + h
    G += estouro(T, t, 0.4, 0.9, 20, 3, 0, -0.1, 0.8)
    return G * env, H * env


def _ancora(cx, cy, s):
    segs = [(cx, cy - 0.5 * s, cx, cy + 0.45 * s, 1.0), (cx - 0.25 * s, cy - 0.3 * s, cx + 0.25 * s, cy - 0.3 * s, 1.0)]
    arco = [(cx + 0.38 * s * math.cos(a), cy + 0.2 * s + 0.25 * s * math.sin(a)) for a in np.linspace(0.1, math.pi - 0.1, 12)]
    return segs, arco


def espinafre(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.4, 0.5)
    if k > 0:
        aperta = ease_in(rel(t, 0.15, 0.3), 2)
        w = 0.2 * (1 - 0.4 * aperta)
        lata = [(-w, -0.3), (w, -0.3), (w, 0.25), (-w, 0.25)]
        g, h = icone(T, lata, k, 0.4)
        G, H = G + g, H + h
        G += T.ring(w, 0.012, 0, -0.2, 3.0) * k
    q = np.random.default_rng(5)
    voa = rel(t, 0.25, 0.5)
    if 0 < voa < 1:
        for j in range(8):
            g, h = icone(T, poe(FOLHA, 0 + q.normal(0, 0.05), -0.2 - 0.5 * voa + q.normal(0, 0.04), 0.05, q.uniform(0, TAU)), (1 - voa) * 1.2, 0.6)
            G, H = G + g, H + h
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        segs, arco = _ancora(0, 0.0, 0.6 * s)
        G += T.lines(segs, 0.035 * s) * 1.4 + T.polyline(arco, 0.035 * s) * 1.4
        G += T.gauss(0, 0, 0.3 * s) * 0.4
    g2, h2 = clarao(T, t, 0.5, 0.7, 0, 0, 0.8)
    return (G + g2) * env, (H + h2) * env


def matriz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.15, 0.45), 2.5)
    k = 1 - rel(t, 0.85, 1)
    s = surge(t, 0.0, 0.25)
    if s > 0:
        for lado in (-1, 1):
            x = lado * (0.12 + 0.12 * abre) * s
            G += T.polyline([(x, -0.3 * s), (x + lado * 0.05, -0.15 * s), (x + lado * 0.05, 0.15 * s), (x, 0.3 * s)], 0.035) * k * 1.2
        G += T.gauss(0, 0, 0.1 + 0.1 * abre) * (0.6 + abre) * k
        H += T.gauss(0, 0, 0.05 + 0.04 * abre) * (0.8 + abre) * k
    raios_ = pulso(t, 0.35, 0.95)
    if raios_ > 0:
        segs = [(0, 0, 0.9 * math.cos(TAU * j / 12 + t), 0.9 * math.sin(TAU * j / 12 + t), 1.0) for j in range(12)]
        G += T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.07) * raios_ * 0.7
    return G * env, H * env


def poder_escondido(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.6), 1.5)
    k = 1 - rel(t, 0.85, 1)
    if s > 0:
        for j in range(12):
            x = -0.3 + 0.055 * j
            alt = (0.6 + 0.25 * math.sin(j * 2.3)) * s
            G += T.polys([(lamina(x, 0.4, x + 0.01 * math.sin(t * 6 + j), 0.4 - alt, 0.05), 1.0)]) * k * 0.6
        G += T.gauss(0, 0.0, 0.35 * s, 0.5 * s) * 0.6 * k
        H += T.gauss(0, 0.0, 0.1 * s, 0.2 * s) * 0.7 * k
    G += particulas(T, t, 0.2, 1.0, 50, 7, 0, 0.2, 0.5, 1.0, 0.012)
    g, h = clarao(T, t, 0.45, 0.7, 0, -0.2, 1.0)
    return (G + g) * env, (H + h) * env


def esponja(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(3)
    for j in range(14):
        x0 = q.uniform(-0.45, 0.45)
        r = q.uniform(0.05, 0.1)
        a0 = q.uniform(0, 0.4)
        u = rel(t, a0, a0 + 0.55)
        if 0 < u < 1:
            y = 0.35 - 0.9 * u
            x = x0 + 0.05 * math.sin(u * 9 + j)
            G += T.ring(r, 0.01, x, y) * 1.3 * (1 - rel(u, 0.85, 1))
            H += T.gauss(x - r * 0.4, y - r * 0.4, r * 0.25) * (1 - u)
    for j in range(4):
        u = rel(t, 0.5 + 0.06 * j, 0.9 + 0.03 * j)
        if 0 < u < 1:
            x = -0.3 + 0.2 * j
            g, h = cheio(T, poe(CORACAO, x, -0.4 + 0.3 * u, 0.06), (1 - u) * 1.2)
            G, H = G + g, H + h
    return G * env, H * env


def scooby_lanche(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.5)
    if u < 1:
        x, y = -0.4 + 0.4 * u, 0.2 - 0.8 * math.sin(math.pi * u * 0.9)
        g, h = icone(T, poe(OSSO, x, y, 0.2, t * 12), 1.3, 0.5)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.48, 0.65, 0, -0.35, 0.6)
    G, H = G + g, H + h
    for j in range(5):
        v = rel(t, 0.5 + 0.06 * j, 0.95)
        if 0 < v < 1:
            x = -0.3 + 0.15 * j + 0.04 * math.sin(v * 8)
            g, h = cheio(T, poe(CORACAO, x * 1.3, -0.3 - 0.4 * v, 0.11), (1 - v) * 1.3)
            G, H = G + g, H + h
    return G * env, H * env


def portal_rick(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5) * (1 - ease_in(rel(t, 0.8, 1.0), 2))
    if abre > 0:
        r = 0.45 * abre
        G += T.gauss(0, 0, r * 0.75) * 0.8
        for j in range(5):
            pts = _espiral(0, 0, 0.02, r, 1.4, TAU * j / 5 - t * 10)
            G += T.polyline([(x, y * 0.95) for x, y in pts], 0.025) * 0.9
            H += T.polyline([(x, y * 0.95) for x, y in pts], 0.006) * 0.5
        G += T.ring(r, 0.04, 0, 0) * 1.3
        q = np.random.default_rng(int(t * 20) % 3)
        for j in range(5):
            a = q.uniform(0, TAU)
            G += T.splats([(r * math.cos(a) * 1.05, r * math.sin(a) * 1.05 + 0.05, 0.8)], 0.025)
    return G * env, H * env


def heroi_finn(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        chapeu = [(0.3 * s * math.cos(a), -0.15 + 0.28 * s * math.sin(a)) for a in np.linspace(math.pi, TAU, 16)]
        chapeu += [(0.3 * s, -0.15 + 0.15 * s), (-0.3 * s, -0.15 + 0.15 * s)]
        g, h = icone(T, chapeu, 1.2, 0.35)
        G, H = G + g, H + h
        for lado in (-1, 1):
            orelha = [(lado * 0.12 * s, -0.15 - 0.25 * s), (lado * 0.18 * s, -0.15 - 0.4 * s), (lado * 0.25 * s, -0.15 - 0.2 * s)]
            g, h = icone(T, orelha, 1.2, 0.4)
            G, H = G + g, H + h
    g, h = icone(T, poe(ESPADA, 0.4, 0.05, 0.35 * surge(t, 0.2, 0.45), 0.4), 1.2 * (1 - rel(t, 0.8, 0.95)), 0.5)
    G, H = G + g, H + h
    brilho = pulso(t, 0.45, 0.7)
    G += T.flare(0.52, -0.25, 0.5 * brilho + 0.01, 0.3, 0.012) * brilho * 1.4
    H += T.gauss(0.52, -0.25, 0.03) * brilho * 2
    return G * env, H * env


def canhao_fusao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    cx, cy = -0.5, 0.0
    carga = ease_in(rel(t, 0.0, 0.45), 1.6)
    if t < 0.5:
        hexa = [(cx + 0.13 * math.cos(TAU * m / 6), cy + 0.13 * math.sin(TAU * m / 6)) for m in range(6)]
        G += T.polyline(hexa + [hexa[0]], 0.025) * 1.2
        G += T.gauss(cx, cy, 0.05 + 0.08 * carga) * (0.6 + carga)
        H += T.gauss(cx, cy, 0.03 + 0.03 * carga) * (0.8 + carga)
        G += converge(T, t, 0.0, 0.45, 20, 9, cx, cy, 0.5)
    u = rel(t, 0.45, 0.95)
    if 0 < u < 1:
        kk = ease_out(rel(u, 0, 0.15)) * (1 - rel(u, 0.6, 1))
        G += T.gauss(0.25, cy, 0.75, 0.13) * kk * 1.4
        H += T.gauss(0.25, cy, 0.75, 0.045) * kk * 2.0
        G += raios(T, t, 0.45, 0.9, 3, 5, 0.3, cy, 0.3)
    return G * env, H * env


def briguenta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.6)
    if 0 < u < 1:
        x = -1.0 + 1.0 * u
        G += T.tapered([(-1.0, -0.3 + 0.3 * u * 0, x, -0.05 * u, 1.0)], 0.12) * 1.1
        H += T.gauss(x, -0.05 * u, 0.04) * 1.5
    g, h = clarao(T, t, 0.33, 0.55, 0, -0.05, 1.1, 1.5)
    G, H = G + g, H + h
    g, h = cheio(T, poe(estrela_pts(8, 0.45), 0, -0.05, 0.3 * pulso(t, 0.33, 0.7)), 1.2 * pulso(t, 0.33, 0.7))
    G, H = G + g, H + h
    G += anel(T, t, 0.35, 0.75, 0.05, 0.65, 0.05, -0.05)
    return G * env, H * env


def _vassoura(cx, cy, s):
    cabo = (cx, cy - 0.5 * s, cx, cy + 0.15 * s, 1.0)
    cerdas = [(cx - 0.12 * s, cy + 0.15 * s), (cx + 0.12 * s, cy + 0.15 * s), (cx + 0.18 * s, cy + 0.5 * s), (cx - 0.18 * s, cy + 0.5 * s)]
    return cabo, cerdas


def vassoura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        chapeu = [(0, -0.85), (0.2 * s, -0.45), (-0.2 * s, -0.45)]
        g, h = icone(T, [(x, -0.45 + (y + 0.45) * s) for x, y in chapeu], 1.2, 0.4)
        G, H = G + g, H + h
        G += T.ring(0.25 * s, 0.015, 0, -0.45, 4.0) * 1.2
        for dx, dy in ((-0.05, -0.6), (0.06, -0.52)):
            g, h = cheio(T, poe(estrela_pts(5, 0.45), dx * s, -0.45 + (dy + 0.45) * s, 0.04 * s), 1.4)
            G, H = G + g, H + h * 2
    for j in range(4):
        u = rel(t, 0.2 + 0.08 * j, 0.6 + 0.08 * j)
        if u > 0:
            x = -0.6 + 0.4 * j
            y = 0.1 - 0.06 * abs(math.sin(t * 20 + j))
            cabo, cerdas = _vassoura(x, y, 0.45 * min(1, u * 2))
            k = 1 - rel(t, 0.85, 1)
            G += T.lines([cabo], 0.02) * k
            g, h = icone(T, cerdas, k, 0.5)
            G, H = G + g, H + h
    G += particulas(T, t, 0.2, 1.0, 26, 3, 0, 0.0, 0.6, 0.3)
    return G * env, H * env


def quaaack(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(int(t * 25) % 6 + 1)
    k = pulso(t, 0.0, 0.85)
    if k > 0:
        pts = [(0.3 * math.cos(a) + q.normal(0, 0.03), -0.05 + 0.25 * math.sin(a) + q.normal(0, 0.03)) for a in np.linspace(0, TAU * 2.5, 50)]
        G += T.polyline(pts, 0.012) * k * 1.2
    for j in range(3):
        kk = pulso(t, 0.2 + 0.15 * j, 0.4 + 0.15 * j)
        if kk > 0:
            x, y = (-0.25, 0.1, 0.25)[j], (-0.2, 0.15, -0.1)[j]
            g, h = cheio(T, poe(estrela_pts(7, 0.4), x, y, 0.18 * kk, j), kk * 1.2)
            G, H = G + g, H + h * 2
    for lado in (-1, 1):
        u = rel(t, 0.3, 0.9)
        if 0 < u < 1:
            pts = [(lado * (0.2 + 0.05 * math.sin(v * 8)), -0.35 - 0.4 * v * u, (1 - v) * (1 - u)) for v in np.linspace(0, 1, 8)]
            G += T.splats(pts, 0.04) * 0.9
    return G * env, H * env


REGISTRO = [
    ("mu_cristal_prata", cristal_prata, GRANDE, "Sailor Moon · a lua e o Cristal de Prata", False),
    ("mu_hahaha", hahaha, GRANDE, "Coringa · a carta e o gás do riso", False),
    ("mu_imprevisivel", imprevisivel, GRANDE, "Arlequina · o martelão e os corações", False),
    ("mu_odio_herois", odio_herois, GRANDE, "Lex Luthor · os cristais de kryptonita", False),
    ("mu_viltrumita", viltrumita, GRANDE, "Invencível · subindo com o estrondo sônico", False),
    ("mu_orgulho_viltrumita", orgulho_viltrumita, GRANDE, "Omni-Man · o soco e a cratera", False),
    ("mu_bravo", bravo, GRANDE, "Raphael · os sais e o símbolo de raiva", False),
    ("mu_contencao", contencao, GRANDE, "Donatello · o campo de contenção", False),
    ("mu_improviso", improviso, GRANDE, "Michelangelo · o nunchaku e a pizza", False),
    ("mu_exorcismo", exorcismo, GRANDE, "Constantine · o pentagrama e a fumaça", False),
    ("mu_pica_pau", pica_pau, GRANDE, "Pica-Pau · as bicadas", False),
    ("mu_pernalonga", pernalonga, GRANDE, "Pernalonga · a cenoura e o buraco", False),
    ("mu_planador", planador, GRANDE, "Aang · as espirais de ar e o planador", False),
    ("mu_lamina_magica", lamina_magica, GRANDE, "Samurai Jack · o corte único", False),
    ("mu_grayskull", grayskull, GRANDE, "He-Man · a Espada do Poder e o raio", False),
    ("mu_espinafre", espinafre, GRANDE, "Popeye · o espinafre e a âncora", False),
    ("mu_matriz", matriz, GRANDE, "Optimus Prime · a Matriz da Liderança", False),
    ("mu_poder_escondido", poder_escondido, GRANDE, "Salsicha · o 1% do poder", False),
    ("mu_esponja", esponja, GRANDE, "Bob Esponja · as bolhas e a cura", False),
    ("mu_scooby_lanche", scooby_lanche, GRANDE, "Scooby-Doo · o Scooby-lanche", False),
    ("mu_portal_rick", portal_rick, GRANDE, "Rick · o portal verde", False),
    ("mu_heroi_finn", heroi_finn, GRANDE, "Finn · o chapéu e a espada", False),
    ("mu_canhao_fusao", canhao_fusao, GRANDE, "Megatron · o canhão de fusão", False),
    ("mu_briguenta", briguenta, GRANDE, "Docinho · o rastro verde e o soco", False),
    ("mu_vassoura", vassoura, GRANDE, "Mickey · as vassouras encantadas", False),
    ("mu_quaaack", quaaack, GRANDE, "Pato Donald · o ataque de nervos", False),
]
