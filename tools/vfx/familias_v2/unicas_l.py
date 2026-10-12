"""Rodada 11 das Mecânicas únicas ativando como habilidade: Luigi, Peach, Zoro, Nami, Sanji, Nero, L, Morty, Tails,
Knuckles, Velma, Fred, Byakuya, Kitana, Shao Kahn, Snorlax, Patrick, Flecha, Gwen, Viúva Negra, Gavião Arqueiro,
Gamora, Drax, Mulher-Aranha, Mulher-Gato e Espantalho.

- coragem_luigi: a lanterna acende em cone e a coragem verde sobe.
- coracao_peach: a coroa brilha e os dois corações voam.
- nada_aconteceu: os três cortes do estilo de três espadas e a névoa vermelha.
- clima: o bastão do clima solta as bolhas e a nuvem com o raio.
- refeicao: a tampa do prato levanta, o vapor sobe e a perna pega fogo.
- puxado: a mão demoníaca fantasma agarra e puxa de volta.
- suspeita: o L gótico aparece e a barra da suspeita enche.
- tropecou: o tropeço, a gota de suor e o rodopio.
- carona: as duas caudas giram como hélice e o vento sai.
- soco_carregado: as luvas de espinhos carregam e o soco estoura.
- desmascarar: a lupa aproxima e a máscara cai.
- armadilha: a rede cai do alto e prende.
- mil_laminas: o Senbonzakura — as mil pétalas-lâmina girando.
- leque: os leques de aço giram e o vento levanta.
- fraco: o martelo da ira bate e as setas de fraqueza descem.
- soneca_pesada: o barrigão, os Z enormes e a cura.
- esconderijo: a pedra levanta e a estrela-do-mar se esconde.
- rapido_demais: o rastro de supervelocidade dando voltas.
- inversao: as setas se invertem dentro do círculo mágico.
- disfarce: a ampulheta vermelha e as faíscas das pulseiras.
- aljava: as quatro flechas de truque, uma de cada tipo.
- perigosa: os dois cortes da espada e o brilho verde.
- vinganca: as duas facas cruzam e as tatuagens vermelhas acendem.
- encanto: os fios de feromônio e a rajada de veneno.
- ladra: as garras arranham e as joias voam para ela.
- medo: o gás do medo com os rostos e os olhos que assustam.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (AMPULHETA, CHAMA, CORACAO, COROA, CRUZ, DIAMANTE, ESPADA, GEMA, GOTA, SETA, anel, aura, cheio, chuva,
                         circulo, clarao, converge, corte, estouro, estrela_pts, flor, icone, onda_no_chao, orbita, particulas,
                         poe, raios, surge, voa)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def coragem_luigi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.6)
    treme = 0.03 * math.sin(t * 80) * (1 - rel(t, 0.3, 0.5))
    if k > 0:
        G += T.polys([([(-0.35 + treme, 0.0), (0.9, -0.35), (0.9, 0.35)], 1.0)], 0.03) * k * 0.5
        H += T.polys([([(-0.35 + treme, 0.0), (0.9, -0.12), (0.9, 0.12)], 1.0)], 0.02) * k * 0.4
        G += T.ring(0.06, 0.02, -0.35 + treme, 0.0) * k * 1.3
    s = ease_out(rel(t, 0.4, 0.8), 2)
    if s > 0:
        g, h = aura(T, t, 0.4, 1.0, 0.35, 0, 1.2)
        G, H = G + g, H + h
        for j in range(3):
            u = rel(t, 0.5 + 0.08 * j, 0.95)
            if 0 < u < 1:
                g2, h2 = icone(T, poe(SETA, -0.3 + 0.3 * j, 0.3 - 0.6 * u, 0.13, -math.pi / 2), (1 - u) * 1.3, 0.5)
                G, H = G + g2, H + h2
    return G * env, H * env


def coracao_peach(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.5, 0.65))
    if s > 0:
        g, h = icone(T, poe(COROA, 0, -0.45, 0.32 * s), 1.3, 0.45)
        G, H = G + g, H + h
        for j in range(3):
            H += T.gauss(-0.1 + 0.1 * j, -0.53, 0.015) * s * 2
    for j, alvo in enumerate((-0.45, 0.45)):
        u = ease_in(rel(t, 0.3 + 0.08 * j, 0.75 + 0.08 * j), 1.4)
        if 0 < u < 1:
            x, y = alvo * u, -0.35 + 0.35 * u - 0.25 * math.sin(math.pi * u)
            g, h = cheio(T, poe(CORACAO, x, y, 0.17), 1.3)
            G, H = G + g + T.gauss(x, y, 0.12) * 0.5, H + h * 2
    for alvo in (-0.45, 0.45):
        G += T.ring(0.18 * rel(t, 0.75, 1.0), 0.02, alvo, 0.0) * pulso(t, 0.75, 1.0) * 1.2
    return G * env, H * env


def nada_aconteceu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        g, h = corte(T, t, 0.05 + 0.05 * j, 0.35 + 0.05 * j, -0.35 + 0.35 * j, 1.4, 0.1, 0.0, -0.15 + 0.15 * j, 0.15)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.5, 0, 0, 0.9)
    G, H = G + g, H + h
    q = np.random.default_rng(3)
    u = rel(t, 0.4, 1.0)
    if 0 < u < 1:
        pts = [(q.normal(0, 0.15 + 0.2 * u), q.normal(0, 0.12 + 0.12 * u) - 0.15 * u, (1 - u) * q.uniform(0.3, 1)) for _ in range(60)]
        G += T.splats(pts, 0.035) * 0.8
    return G * env, H * env


def clima(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        u = ease_out(rel(t, 0.0 + 0.08 * j, 0.4 + 0.08 * j), 2)
        if 0 < u < 1:
            x, y = -0.4 + 0.4 * j * u, 0.2 - 0.7 * u
            G += T.ring(0.06, 0.012, x, y) * 1.2
            H += T.gauss(x - 0.02, y - 0.02, 0.012) * 1.2
    nuvem = ease_out(rel(t, 0.35, 0.6), 2) * (1 - rel(t, 0.85, 1))
    if nuvem > 0:
        for dx, dy, r in ((-0.15, -0.5, 0.12), (0.0, -0.56, 0.15), (0.15, -0.5, 0.12), (0.05, -0.45, 0.12)):
            G += T.gauss(dx, dy, r * nuvem) * 0.9
    raio = pulso(t, 0.55, 0.8)
    if raio > 0:
        q = np.random.default_rng(int(t * 30) % 4 + 2)
        bolt = jagged(q, 0, -0.45, 0.05, 0.35, 5, 0.25)
        G += T.polyline(bolt, 0.035) * raio * 1.4
        H += T.polyline(bolt, 0.01) * raio * 1.5
    g, h = chuva(T, t, 0.5, 1.0, GOTA, 12, 5, 0.03, -0.45, 0.4, 0.4, 0.0, 0.9)
    return (G + g) * env, (H + h) * env


def refeicao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        G += T.ring(0.35 * s, 0.03, 0, 0.2, 4.0) * 1.2
        sobe = ease_out(rel(t, 0.25, 0.5), 2)
        cy = 0.15 - 0.35 * sobe
        tampa = [(0.28 * s * math.cos(a), cy + 0.22 * s * math.sin(a)) for a in np.linspace(math.pi, TAU, 18)]
        g, h = icone(T, tampa + [(0.28 * s, cy), (-0.28 * s, cy)], 1.1, 0.4)
        G, H = G + g, H + h
        G += T.ring(0.03, 0.012, 0, cy - 0.24 * s) * 1.2
        if sobe > 0.3:
            for j in range(3):
                pts = [(-0.12 + 0.12 * j + 0.04 * math.sin(v * 7 + t * 10 + j), 0.12 - 0.35 * v * sobe, (1 - v)) for v in np.linspace(0, 1, 10)]
                G += T.splats(pts, 0.035) * 0.7
    for j in range(5):
        k = pulso(t, 0.55, 0.95)
        g, h = icone(T, poe(CHAMA, 0.5 + 0.04 * j, 0.25 - 0.1 * j, 0.08), k, 0.6)
        G, H = G + g, H + h
    return G * env, H * env


def puxado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    vai = ease_out(rel(t, 0.0, 0.35), 2)
    volta = ease_in(rel(t, 0.5, 0.85), 2)
    x = -0.4 + 1.0 * vai - 0.9 * volta
    k = 1 - rel(t, 0.85, 1)
    fecha = rel(t, 0.35, 0.5)
    palma = [(x - 0.15, -0.15), (x + 0.05, -0.18), (x + 0.12, -0.1), (x + 0.12, 0.1), (x + 0.05, 0.18), (x - 0.15, 0.15)]
    g, h = icone(T, palma, k * 1.1, 0.4)
    G, H = G + g, H + h
    for j in range(4):
        y = -0.15 + 0.1 * j
        comp = 0.22 * (1 - 0.7 * fecha)
        G += T.polyline([(x + 0.1, y), (x + 0.1 + comp, y - 0.02), (x + 0.1 + comp + 0.05 * fecha, y + 0.06 * fecha)], 0.03) * k * 1.1
    G += T.tapered([(-0.8, 0.0, x - 0.15, 0.0, 0.7)], 0.12) * k * 0.6
    H += T.gauss(x, 0, 0.1) * k * 0.3
    g, h = clarao(T, t, 0.35, 0.5, 0.65, 0, 0.6)
    return (G + g) * env, (H + h) * env


def suspeita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        letra = [(-0.12, -0.45), (-0.06, -0.48), (-0.08, -0.4), (-0.08, 0.05), (0.15, 0.05), (0.2, 0.0)]
        G += T.polyline([(x * s * 1.5, y * s * 1.5 + 0.05) for x, y in letra], 0.05 * s) * 1.4
        H += T.polyline([(x * s * 1.5, y * s * 1.5 + 0.05) for x, y in letra], 0.015) * s
    enche = ease_out(rel(t, 0.35, 0.8), 2)
    k = 1 - rel(t, 0.85, 1)
    if t > 0.3:
        G += T.lines([(-0.4, 0.35, 0.4, 0.35, 1.0)], 0.06) * 0.25 * k
        G += T.lines([(-0.4, 0.35, -0.4 + 0.8 * enche * 0.35 + 0.0, 0.35, 1.0)], 0.06) * 1.3 * k
        H += T.lines([(-0.4, 0.35, -0.4 + 0.8 * enche * 0.35, 0.35, 1.0)], 0.02) * k
    return G * env, H * env


def tropecou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.3)
    if 0 < u < 1:
        G += T.tapered([(-0.6, 0.2, -0.6 + 0.6 * u, 0.2 - 0.3 * u * u, 1.0)], 0.05)
    g, h = clarao(T, t, 0.25, 0.4, 0, 0.0, 0.5)
    G, H = G + g, H + h
    G += T.polyline(_espiral(0, -0.3, 0.01, 0.24, 2.5, t * 15), 0.03) * pulso(t, 0.3, 1.0) * 1.4
    v = rel(t, 0.35, 0.9)
    if 0 < v < 1:
        g, h = icone(T, poe(GOTA, 0.3 + 0.05 * v, -0.45 + 0.2 * v, 0.15), (1 - rel(v, 0.8, 1)) * 1.3, 0.5)
        G, H = G + g, H + h
    return G * env, H * env


def carona(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.9)
    for j in range(2):
        a = t * 30 + math.pi * j
        cauda = [(0, 0.1)] + [(0.7 * v * math.cos(a + 0.4 * math.sin(math.pi * v)), 0.1 + 0.7 * v * math.sin(a + 0.4 * math.sin(math.pi * v)) * 0.5) for v in np.linspace(0.1, 1, 10)]
        cauda += [(0.7 * v * math.cos(a - 0.3 * math.sin(math.pi * v)), 0.1 + 0.7 * v * math.sin(a - 0.3 * math.sin(math.pi * v)) * 0.5) for v in np.linspace(1, 0.1, 10)]
        g, h = icone(T, cauda, k * 1.1, 0.5)
        G, H = G + g, H + h
        for r in range(1, 3):
            aa = a - 0.35 * r
            G += T.lines([(0, 0.1, 0.5 * math.cos(aa), 0.1 + 0.5 * math.sin(aa) * 0.35, 1.0)], 0.05) * k * 0.2 / r
    for j in range(4):
        G += anel(T, t, 0.1 + 0.15 * j, 0.5 + 0.15 * j, 0.2, 0.75, 0.025, 0.1, 3.0)
    return G * env, H * env


def soco_carregado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    carga = ease_in(rel(t, 0.0, 0.5), 1.5)
    k = 1 - rel(t, 0.55, 0.65)
    if k > 0:
        x = -0.3 - 0.1 * carga
        P, nos = _punho(T, x, 0, 1.8, 0)
        G += P * 0.8 * k
        H += nos * 0.5 * k
        for dy in (-0.07, 0.07):
            g, h = cheio(T, [(x + 0.2, dy - 0.03), (x + 0.33, dy), (x + 0.2, dy + 0.03)], k * 1.3)
            G, H = G + g, H + h
        G += T.gauss(x, 0, 0.15 + 0.1 * carga) * carga * 0.9 * k
        G += converge(T, t, 0.0, 0.5, 16, 3, x, 0, 0.5)
    g, h = clarao(T, t, 0.52, 0.75, 0.3, 0, 1.2, 1.6)
    G += anel(T, t, 0.53, 0.9, 0.05, 0.7, 0.05) + estouro(T, t, 0.53, 0.9, 20, 3, 0.3, 0, 0.6)
    return (G + g) * env, (H + h) * env


def desmascarar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        r = 0.22 * s
        G += T.ring(r, 0.035, 0.1, -0.15) * 1.3 + T.gauss(0.1, -0.15, r * 0.7) * 0.3
        G += T.lines([(0.1 + r * 0.7, -0.15 + r * 0.7, 0.1 + r * 1.8, -0.15 + r * 1.8, 1.0)], 0.05) * 1.1
        H += T.arc_band(r * 0.7, 0.015, 3.5, 4.4, 1.0, 0.0, 0.1, -0.15, 1.0) * 1.2
    cai = ease_in(rel(t, 0.45, 0.9), 2)
    if 0 < cai < 1:
        mascara = [(-0.2, -0.1), (0.2, -0.1), (0.15, 0.1), (0.0, 0.15), (-0.15, 0.1)]
        g, h = icone(T, poe(mascara, 0, -0.1 + 0.6 * cai, 1.0, cai * 2), (1 - rel(cai, 0.8, 1)) * 1.2, 0.4)
        G, H = G + g, H + h
    for j in range(3):
        k = pulso(t, 0.5 + 0.08 * j, 0.8 + 0.06 * j)
        g, h = cheio(T, poe(estrela_pts(4, 0.3), -0.35 + 0.35 * j, -0.5, 0.08 * k), k * 1.4)
        G, H = G + g, H + h * 2
    return G * env, H * env


def armadilha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.1, 0.45), 2)
    k = 1 - rel(t, 0.85, 1)
    y = -1.0 + 1.0 * u
    w = 0.45 + 0.1 * u
    segs = []
    for j in range(7):
        v = -1 + 2 * j / 6
        segs.append((v * w, y - 0.4, v * w * (0.85 if u >= 1 else 1), y + 0.4, 1.0))
        segs.append((-w, y - 0.4 + 0.8 * (j / 6), w, y - 0.4 + 0.8 * (j / 6), 1.0))
    G += T.lines(segs, 0.012) * k * 1.2
    G += T.lines([(0, y - 0.4, 0, -1.0, 1.0)], 0.012) * (1 - u) * 0.8
    g, h = clarao(T, t, 0.43, 0.6, 0, 0.2, 0.6)
    return (G + g) * env, (H + h) * env


def mil_laminas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(11)
    k = 1 - rel(t, 0.85, 1)
    gira = ease_out(rel(t, 0.0, 0.4), 2)
    shapes = []
    for j in range(80):
        a0, r0 = q.uniform(0, TAU), q.uniform(0.15, 0.65)
        a = a0 + t * 8 * (1 - 0.4 * r0)
        r = r0 * gira
        x, y = r * math.cos(a), r * math.sin(a) * 0.75
        c, s = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
        l = 0.035
        shapes.append(([(x - c * l, y - s * l), (x + 0.3 * s * l, y - 0.3 * c * l), (x + c * l, y + s * l), (x - 0.3 * s * l, y + 0.3 * c * l)], 1.0))
    P = T.polys(shapes)
    G += P * 1.1 * k
    H += P * 0.3 * k
    g, h = aura(T, t, 0.0, 1.0, 0.4, 0, 0.6)
    return (G + g) * env, (H + h) * env


def _leque(cx, cy, s, ang):
    pts = [(0, 0)] + [(math.cos(a), math.sin(a)) for a in np.linspace(-math.pi * 0.8, -math.pi * 0.2, 12)]
    return poe(pts, cx, cy, s, ang)


def leque(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j, lado in enumerate((-1, 1)):
        u = rel(t, 0.0 + 0.1 * j, 0.6 + 0.1 * j)
        if 0 < u < 1:
            x = lado * (0.7 - 0.7 * ease_out(u))
            y = -0.1 - 0.2 * math.sin(math.pi * u)
            g, h = icone(T, _leque(x, y + 0.1, 0.25, t * 20 * lado), 1.2 * (1 - rel(u, 0.85, 1)), 0.45)
            G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.4 + 0.06 * j, 0.95)
        if 0 < u < 1:
            x = -0.3 + 0.15 * j
            G += T.tapered([(x, 0.4 - 0.2 * u, x + 0.05 * math.sin(u * 6), 0.2 - 0.8 * u, 1.0)], 0.04) * (1 - u) * 1.1
    G += anel(T, t, 0.4, 0.8, 0.1, 0.6, 0.03, 0.3, 3.0)
    return G * env, H * env


def fraco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.2)
    k = 1 - rel(t, 0.5, 0.6)
    if k > 0:
        ang = -2.2 + 1.7 * u
        cx, cy = 0.0, 0.35
        hx, hy = cx + 0.7 * math.cos(ang), cy + 0.7 * math.sin(ang)
        G += T.lines([(cx, cy, hx, hy, 1.0)], 0.04) * k
        g, h = icone(T, poe([(-1, -0.7), (1, -0.7), (1, 0.7), (-1, 0.7)], hx, hy, 0.2, ang + math.pi / 2), k * 1.2, 0.45)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.33, 0.55, 0.3, 0.3, 1.0, 1.3)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.35, 0.8, 0.95, 0.38)
    for j in range(3):
        v = rel(t, 0.45 + 0.08 * j, 0.95)
        if 0 < v < 1:
            g2, h2 = icone(T, poe(SETA, -0.4 + 0.4 * j, -0.5 + 0.4 * v, 0.14, math.pi / 2), (1 - v) * 1.3, 0.5)
            G, H = G + g2, H + h2
    return G * env, H * env


def soneca_pesada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    respira = 1 + 0.06 * math.sin(t * 12)
    if s > 0:
        barriga = [(0.42 * s * respira * math.cos(a), 0.1 + 0.32 * s * respira * math.sin(a)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, barriga, 1.0, 0.3)
        G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.2 + 0.15 * j, 0.75 + 0.15 * j)
        if 0 < u < 1:
            x, y, w = 0.2 + 0.15 * j, -0.3 - 0.4 * u, 0.07 + 0.04 * j
            G += T.polyline([(x - w, y - w), (x + w, y - w), (x - w, y + w), (x + w, y + w)], 0.03) * (1 - u) * 1.5
    for j in range(4):
        u = rel(t, 0.5 + 0.06 * j, 0.95)
        if 0 < u < 1:
            x, y = -0.3 + 0.2 * j, 0.1 - 0.5 * u
            G += T.lines([(x - 0.04, y, x + 0.04, y, 1.0), (x, y - 0.04, x, y + 0.04, 1.0)], 0.018) * (1 - u) * 1.3
    return G * env, H * env


def esconderijo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    levanta = math.sin(math.pi * rel(t, 0.1, 0.7)) * 0.35
    k = 1 - rel(t, 0.85, 1)
    pedra = [(0.4 * math.cos(a), 0.35 - levanta - 0.3 * math.sin(a)) for a in np.linspace(0, math.pi, 18)]
    g, h = icone(T, pedra, k * 1.0, 0.35)
    G, H = G + g, H + h
    s = surge(t, 0.15, 0.4) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        g, h = cheio(T, poe(estrela_pts(5, 0.5), 0, 0.2, 0.18 * s, -math.pi / 2), 1.2)
        G, H = G + g, H + h
    G += particulas(T, t, 0.6, 1.0, 20, 5, 0, 0.35, 0.4, 0.2, 0.015)
    return G * env, H * env


def rapido_demais(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.85)
    if 0 < u < 1:
        voltas = 2.5 * u
        pts = []
        for v in np.linspace(max(0, voltas - 0.6), voltas, 30):
            a = v * TAU
            pts.append((0.5 * math.cos(a), 0.1 + 0.5 * math.sin(a) * 0.4))
        for i in range(len(pts) - 1):
            G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.06 * (i / 30) + 0.005) * 1.2
        H += T.gauss(pts[-1][0], pts[-1][1], 0.04) * 1.5
    G += anel(T, t, 0.2, 0.9, 0.3, 0.75, 0.025, 0.1, 2.5)
    G += particulas(T, t, 0.1, 0.9, 30, 3, 0, 0.25, 0.6, 0.1, 0.012)
    return G * env, H * env


def inversao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2.5) * (1 - rel(t, 0.85, 1))
    G += T.ring(0.42 * s, 0.025, 0, 0) * 1.2 + T.ring(0.34 * s, 0.01, 0, 0) * 0.8
    gira = ease_in(rel(t, 0.35, 0.65), 2) * math.pi
    if s > 0:
        for lado in (-1, 1):
            g, h = icone(T, poe(SETA, lado * 0.12, 0, 0.2 * s, -math.pi / 2 * lado + gira), 1.3, 0.5)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.6, 0.8, 0, 0, 0.6)
    G += particulas(T, t, 0.3, 1.0, 26, 9, 0, 0, 0.45, 0.3)
    return (G + g) * env, (H + h) * env


def disfarce(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = cheio(T, poe(AMPULHETA, 0, -0.1, 0.22 * s), 1.2)
        G, H = G + g, H + h
        G += T.ring(0.3 * s, 0.02, 0, -0.1) * 1.1
    k = pulso(t, 0.3, 0.9)
    for lado in (-1, 1):
        G += raios(T, t, 0.3, 0.9, 3, 5 + lado, lado * 0.45, 0.25, 0.2)
        G += T.ring(0.06, 0.015, lado * 0.45, 0.25, 2.0) * k * 1.2
    return G * env, H * env


def aljava(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        a0 = 0.05 + 0.15 * j
        u = rel(t, a0, a0 + 0.25)
        y = -0.35 + 0.23 * j
        if 0 < u < 1:
            x = -0.9 + 1.5 * ease_in(u, 1.3)
            G += T.lines([(x - 0.4, y, x, y, 1.0)], 0.022) * 1.3
            g, h = cheio(T, [(x + 0.12, y), (x, y - 0.05), (x, y + 0.05)], 1.4)
            G, H = G + g, H + h
            G += T.lines([(x - 0.4, y, x - 0.5, y - 0.06, 1.0), (x - 0.4, y, x - 0.5, y + 0.06, 1.0)], 0.016)
        k = pulso(t, a0 + 0.22, a0 + 0.45)
        if k > 0:
            if j == 0:
                g2, h2 = clarao(T, t, a0 + 0.22, a0 + 0.45, 0.6, y, 0.6)
                G, H = G + g2, H + h2
            elif j == 1:
                G += raios(T, t, a0 + 0.22, a0 + 0.45, 4, 3, 0.6, y, 0.3)
            elif j == 2:
                G += T.gauss(0.6, y, 0.18) * k * 1.4
                H += T.gauss(0.6, y, 0.05) * k
            else:
                segs = [(0.6 - 0.18, y - 0.18 + 0.09 * m, 0.6 + 0.18, y - 0.18 + 0.09 * m, 1.0) for m in range(5)] + [(0.42 + 0.09 * m, y - 0.18, 0.42 + 0.09 * m, y + 0.18, 1.0) for m in range(5)]
                G += T.lines(segs, 0.01) * k * 1.3
    return G * env, H * env


def perigosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = corte(T, t, 0.05, 0.35, 0.5, 1.5, 0.1, 0, 0, 0.18)
    G, H = G + g, H + h
    g, h = corte(T, t, 0.3, 0.6, -0.6, 1.5, 0.1, 0, 0, -0.18)
    G, H = G + g, H + h
    brilho = pulso(t, 0.55, 0.8)
    G += T.flare(0.2, -0.2, 0.6 * brilho + 0.01, 0.4, 0.012) * brilho * 1.4
    H += T.gauss(0.2, -0.2, 0.03) * brilho * 2
    G += particulas(T, t, 0.4, 1.0, 20, 3, 0, 0, 0.4, 0.2)
    return G * env, H * env


def vinganca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    cruza = ease_out(rel(t, 0.0, 0.3), 3)
    k = 1 - rel(t, 0.55, 0.7)
    for lado in (-1, 1):
        g, h = icone(T, poe(ESPADA, lado * 0.15 * (1 - cruza), -0.05, 0.38, lado * (0.3 + 0.5 * cruza)), k * 1.2, 0.45)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.25, 0.45, 0, -0.3, 0.7)
    G, H = G + g, H + h
    tat = ease_out(rel(t, 0.35, 0.7), 2) * (1 - rel(t, 0.88, 1))
    if tat > 0:
        for lado in (-1, 1):
            pts = [(lado * (0.1 + 0.25 * v), -0.3 + 0.6 * v + 0.08 * math.sin(v * 8)) for v in np.linspace(0, tat, 16)]
            G += T.polyline(pts, 0.02) * 1.3
            pts2 = [(lado * (0.05 + 0.15 * v), 0.0 + 0.4 * v + 0.05 * math.sin(v * 10 + 1)) for v in np.linspace(0, tat, 12)]
            G += T.polyline(pts2, 0.015) * 1.1
    return G * env, H * env


def encanto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.7)
    for j in range(5):
        pts = [(-0.3 + 1.1 * v, -0.3 + 0.12 * j + 0.08 * math.sin(v * 9 + t * 8 + j)) for v in np.linspace(0, 1, 20)]
        G += T.polyline(pts, 0.012) * k * (0.6 + 0.4 * math.sin(t * 6 + j))
    u = rel(t, 0.45, 0.8)
    if 0 < u < 1:
        x = -0.4 + 1.2 * ease_in(u, 1.3)
        G += T.gauss(x, 0.1, 0.12) * 1.3 + T.tapered([(x - 0.4, 0.1, x, 0.1, 0.8)], 0.15) * 0.6
        H += T.gauss(x, 0.1, 0.05) * 1.5
    g, h = clarao(T, t, 0.75, 0.92, 0.75, 0.1, 0.6)
    return (G + g) * env, (H + h) * env


def ladra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        g, h = corte(T, t, 0.05 + 0.03 * j, 0.3 + 0.03 * j, 1.2, 1.0, 0.06, 0.3 - 0.12 * j, 0.0 + 0.03 * j, 0.06)
        G, H = G + g, H + h
    q = np.random.default_rng(13)
    for j in range(5):
        u = ease_in(rel(t, 0.35 + 0.05 * j, 0.8 + 0.03 * j), 1.5)
        if 0 < u < 1:
            x0, y0 = 0.25 + q.uniform(-0.1, 0.1), q.uniform(-0.15, 0.15)
            x, y = x0 + (-0.5 - x0) * u, y0 - 0.25 * math.sin(math.pi * u)
            g2, h2 = cheio(T, poe(GEMA, x, y, 0.09), 1.4)
            G, H = G + g2, H + h2 * 2
    return G * env, H * env


def medo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(17)
    gas = rel(t, 0.0, 1.0)
    for j in range(5):
        a = TAU * j / 5 + q.uniform(-0.3, 0.3)
        d = 0.15 + 0.35 * ease_out(gas)
        cx, cy = d * math.cos(a), d * math.sin(a) * 0.7
        G += T.gauss(cx, cy, 0.14 + 0.06 * gas) * (1 - rel(gas, 0.75, 1)) * 0.7
        rosto = pulso(t, 0.25 + 0.08 * j, 0.75 + 0.05 * j)
        if rosto > 0:
            for lado in (-1, 1):
                H += T.gauss(cx + lado * 0.04, cy - 0.03, 0.015) * rosto * 1.6
            G += T.ring(0.03, 0.01, cx, cy + 0.05, 0.6) * rosto
    olhos = pulso(t, 0.3, 0.95)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.1, -0.45, 0.03, 0.02) * olhos * 2.5
        G += T.gauss(lado * 0.1, -0.45, 0.08, 0.05) * olhos * 1.2
    return G * env, H * env


REGISTRO = [
    ("mu_coragem_luigi", coragem_luigi, GRANDE, "Luigi · a lanterna e a coragem", False),
    ("mu_coracao_peach", coracao_peach, GRANDE, "Peach · a coroa e os corações", False),
    ("mu_nada_aconteceu", nada_aconteceu, GRANDE, "Zoro · os três cortes e a névoa", False),
    ("mu_clima", clima, GRANDE, "Nami · o bastão do clima e o raio", False),
    ("mu_refeicao", refeicao, GRANDE, "Sanji · o prato servido e a perna em fogo", False),
    ("mu_puxado", puxado, GRANDE, "Nero · a mão demoníaca", False),
    ("mu_suspeita", suspeita, GRANDE, "L · o L e a barra da suspeita", False),
    ("mu_tropecou", tropecou, GRANDE, "Morty · o tropeço", False),
    ("mu_carona", carona, GRANDE, "Tails · as caudas em hélice", False),
    ("mu_soco_carregado", soco_carregado, GRANDE, "Knuckles · o soco carregado", False),
    ("mu_desmascarar", desmascarar, GRANDE, "Velma · a lupa e a máscara caindo", False),
    ("mu_armadilha", armadilha, GRANDE, "Fred · a rede da armadilha", False),
    ("mu_mil_laminas", mil_laminas, GRANDE, "Byakuya · o Senbonzakura", False),
    ("mu_leque", leque, GRANDE, "Kitana · os leques de aço", False),
    ("mu_fraco", fraco, GRANDE, "Shao Kahn · o martelo da ira", False),
    ("mu_soneca_pesada", soneca_pesada, GRANDE, "Snorlax · a soneca pesada", False),
    ("mu_esconderijo", esconderijo, GRANDE, "Patrick · debaixo da pedra", False),
    ("mu_rapido_demais", rapido_demais, GRANDE, "Flecha · o rastro de supervelocidade", False),
    ("mu_inversao", inversao, GRANDE, "Gwen · o feitiço de inversão", False),
    ("mu_disfarce", disfarce, GRANDE, "Viúva Negra · a ampulheta e as pulseiras", False),
    ("mu_aljava", aljava, GRANDE, "Gavião Arqueiro · as flechas de truque", False),
    ("mu_perigosa", perigosa, GRANDE, "Gamora · os cortes da espada", False),
    ("mu_vinganca", vinganca, GRANDE, "Drax · as facas e as tatuagens", False),
    ("mu_encanto", encanto, GRANDE, "Mulher-Aranha · o feromônio e a rajada", False),
    ("mu_ladra", ladra, GRANDE, "Mulher-Gato · as garras e as joias", False),
    ("mu_medo", medo, GRANDE, "Espantalho · o gás do medo", False),
]
