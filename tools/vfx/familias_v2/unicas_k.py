"""Rodada 10 das Mecânicas únicas ativando como habilidade: Thor, Ichigo, Rukia, Aizen, Kenpachi, Eren, Gon, Killua,
Hisoka, Kurapika, Edward, Alphonse, Roy, Guts, Griffith, Jotaro, Dio, Giorno, Denji, Power, Makima, Mewtwo, Heihachi
e Marceline.

- tempestade: o Mjolnir erguido puxa os raios do céu.
- hollow: a máscara Hollow se forma com as listras e a pressão vermelha.
- danca_branca: o círculo branco no chão e o pilar de gelo que sobe (Tsugi no Mai).
- ilusao_aizen: o espelho racha em teia e a imagem derrete.
- tapa_olho: o tapa-olho voa e a pressão espiritual amarela explode para cima.
- endurecer: as placas de cristal cobrem o corpo e o vapor sai.
- pedra_papel: o punho carrega a aura e os três sinais (pedra, papel, tesoura) giram.
- relampago: o Godspeed — os raios azuis no corpo e as imagens para trás.
- bungee_gum: os fios de goma esticam e os naipes de baralho aparecem.
- juramento: as correntes com pontas giram e os olhos escarlates acendem.
- transmutacao: as faíscas azuis correm no chão e as lanças de pedra sobem.
- parede: o muro de pedra sobe do chão.
- chamas_roy: o estalo da luva e as explosões em fila.
- berserker: a Marca do Sacrifício, os olhos vermelhos do elmo e a aura de espinhos.
- eclipse: o eclipse negro com a coroa e as penas caindo.
- za_warudo_jotaro: a esfera do tempo parado se expande e os ponteiros param.
- road_roller: o Road Roller cai do céu e as facas giram em volta.
- vida_demais: as vinhas brotam e as joaninhas e borboletas surgem.
- vrrrum: a corda puxa e as motosserras saem girando, com o sangue.
- escondida: o martelo de sangue e os chifres da Power.
- agora_e_meu: os olhos de anéis e a corrente que prende pelo dedo.
- disable: os anéis psíquicos travam o rival com o X.
- penhasco: o punho elétrico joga o rival para o alto.
- rainha_vampira: as presas e o vermelho sugado em fios.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .rodada13 import _borda
from .unicas_b import _silhueta
from .unicas_kit import (ASA, CORACAO, DIAMANTE, ESPADA, FOLHA, GOTA, PENA, anel, aura, cheio, chuva, circulo, clarao,
                         converge, corte, estouro, estrela_pts, flor, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def tempestade(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        y = 0.2 - 0.35 * sobe
        G += T.lines([(0, y, 0, y + 0.45, 1.0)], 0.035) * k
        g, h = icone(T, [(-0.2, y - 0.14), (0.2, y - 0.14), (0.2, y + 0.04), (-0.2, y + 0.04)], k * 1.2, 0.5)
        G, H = G + g, H + h
    r = pulso(t, 0.25, 0.85)
    if r > 0:
        q = np.random.default_rng(int(t * 30) % 5 + 1)
        for _ in range(4):
            bolt = jagged(q, q.uniform(-0.7, 0.7), -1.0, 0, -0.2, 5, 0.25)
            G += T.polyline(bolt, 0.025) * r * 1.3
            H += T.polyline(bolt, 0.008) * r * 1.4
        G += T.gauss(0, -0.15, 0.2) * r * 0.9
    G += raios(T, t, 0.4, 0.95, 5, 3, 0, -0.15, 0.6)
    return G * env, H * env


def hollow(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    forma = ease_out(rel(t, 0.0, 0.45), 2)
    k = 1 - rel(t, 0.85, 1)
    if forma > 0:
        mascara = [(0.25 * forma * math.cos(a), -0.15 + 0.32 * forma * math.sin(a) * (1.1 if math.sin(a) > 0 else 1)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, mascara, k * 1.2, 0.4)
        G, H = G + g, H + h
        for lado in (-1, 1):
            olho = [(lado * 0.09 * forma + 0.05 * forma * math.cos(a), -0.2 + 0.035 * forma * math.sin(a)) for a in np.linspace(0, TAU, 12, endpoint=False)]
            G += T.polyline(olho + [olho[0]], 0.012) * k * 1.3
            G += T.lines([(lado * 0.09 * forma, -0.32 * forma - 0.1, lado * 0.12 * forma, -0.05, 1.0)], 0.02) * k * 1.2
    g, h = aura(T, t, 0.3, 1.0, 0.45, -0.1, 1.1)
    G += raios(T, t, 0.35, 0.95, 4, 9, 0, -0.1, 0.6)
    return (G + g) * env, (H + h) * env


def danca_branca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    circ = ease_out(rel(t, 0.0, 0.3), 2.5) * (1 - rel(t, 0.85, 1))
    G += T.ring(0.5 * circ, 0.03, 0, 0.35, 3.0) * 1.3 + T.ring(0.45 * circ, 0.012, 0, 0.35, 3.0) * 0.8
    sobe = ease_out(rel(t, 0.3, 0.6), 2.5)
    k = 1 - rel(t, 0.8, 1)
    if sobe > 0:
        alt = 1.2 * sobe
        G += T.polys([([(-0.45, 0.35), (-0.4, 0.35 - alt), (0.4, 0.35 - alt), (0.45, 0.35)], 1.0)], 0.02) * 0.45 * k
        G += T.lines([(-0.42, 0.35, -0.4, 0.35 - alt, 1.0), (0.42, 0.35, 0.4, 0.35 - alt, 1.0)], 0.025) * k * 1.3
        H += T.gauss(0, 0.35 - alt * 0.5, 0.15, alt * 0.4 + 0.01) * k * 0.5
    G += particulas(T, t, 0.3, 1.0, 50, 7, 0, 0.0, 0.45, 0.6, 0.012)
    return G * env, H * env


def ilusao_aizen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(31)
    racha = ease_out(rel(t, 0.1, 0.45), 2)
    k = 1 - rel(t, 0.85, 1)
    if racha > 0:
        for j in range(10):
            a = TAU * j / 10 + q.uniform(-0.1, 0.1)
            G += T.polyline(jagged(q, 0, -0.05, 0.6 * racha * math.cos(a), -0.05 + 0.6 * racha * math.sin(a), 3, 0.15), 0.012) * k * 1.3
        for r in (0.15, 0.3, 0.45):
            if racha * 0.6 > r:
                pts = [(r * math.cos(a) * (1 + q.uniform(-0.05, 0.05)), -0.05 + r * math.sin(a) * (1 + q.uniform(-0.05, 0.05))) for a in np.linspace(0, TAU, 11)]
                G += T.polyline(pts, 0.008) * k
    derrete = rel(t, 0.5, 1.0)
    if derrete > 0:
        for j in range(8):
            x = -0.35 + 0.1 * j
            pts = [(x + 0.03 * math.sin(v * 8 + j), -0.4 + 0.8 * v * derrete) for v in np.linspace(0, 1, 12)]
            G += T.polyline(pts, 0.012) * (1 - derrete) * 1.1
    g, h = clarao(T, t, 0.1, 0.3, 0, -0.05, 0.7)
    return (G + g) * env, (H + h) * env


def tapa_olho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.4)
    if 0 < u < 1:
        x, y = 0.08 + 0.6 * u, -0.35 - 0.3 * math.sin(math.pi * u)
        g, h = cheio(T, poe([(-1, -0.6), (1, -0.6), (0.8, 0.6), (-0.8, 0.6)], x, y, 0.06, u * 10), 1.2)
        G, H = G + g, H + h
        G += T.polyline([(x - 0.06, y), (x - 0.25, y + 0.05)], 0.008)
    sobe = ease_out(rel(t, 0.2, 0.6), 2)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        for j in range(10):
            x = -0.35 + 0.078 * j
            alt = (0.7 + 0.25 * math.sin(j * 1.9)) * sobe
            G += T.polys([(lamina(x, 0.4, x + 0.02 * math.sin(t * 20 + j), 0.4 - alt, 0.06), 1.0)]) * k * 0.7
        G += T.gauss(0, -0.1, 0.35, 0.55) * sobe * 0.5 * k
        H += T.gauss(0, 0.0, 0.1, 0.35) * sobe * 0.6 * k
    for j in range(3):
        kk = pulso(t, 0.3 + 0.1 * j, 0.6 + 0.1 * j)
        G += T.ring(0.03, 0.012, -0.2 + 0.2 * j, -0.55) * kk * 1.3
    return G * env, H * env


def endurecer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(7)
    k = 1 - rel(t, 0.85, 1)
    for j in range(14):
        cx, cy = q.uniform(-0.25, 0.25), q.uniform(-0.45, 0.4)
        s = ease_out(rel(t, 0.03 * j, 0.25 + 0.03 * j), 2.5)
        if s > 0:
            hexa = [(cx + 0.07 * s * math.cos(TAU * m / 6), cy + 0.07 * s * math.sin(TAU * m / 6)) for m in range(6)]
            g, h = icone(T, hexa, k * 1.1, 0.4)
            G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.4 + 0.08 * j, 0.95)
        if 0 < u < 1:
            x = q.uniform(-0.3, 0.3)
            G += T.gauss(x, -0.3 - 0.4 * u, 0.06 + 0.1 * u) * (1 - u) * 0.8
    g, h = clarao(T, t, 0.4, 0.6, 0, 0, 0.6)
    return (G + g) * env, (H + h) * env


def pedra_papel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    carga = ease_in(rel(t, 0.0, 0.6), 1.5)
    k = 1 - rel(t, 0.82, 0.95)
    P, nos = _punho(T, 0, -0.05, 1.6 + 0.4 * carga, -math.pi / 2)
    G += P * 0.8 * k
    H += nos * 0.5 * k
    G += T.gauss(0, -0.05, 0.2 + 0.15 * carga) * (0.4 + 0.8 * carga) * k
    for j in range(3):
        a = TAU * j / 3 + t * 6
        x, y = 0.5 * math.cos(a), -0.05 + 0.5 * math.sin(a) * 0.5
        if j == 0:
            g, h = cheio(T, poe(circulo(12, 1.0), x, y, 0.06), k)
        elif j == 1:
            g, h = icone(T, poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], x, y, 0.06), k, 0.5)
        else:
            G += T.lines([(x, y + 0.06, x - 0.05, y - 0.07, 1.0), (x, y + 0.06, x + 0.05, y - 0.07, 1.0)], 0.018) * k * 1.2
            g, h = 0.0, 0.0
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.6, 0.82, 0, -0.05, 1.0, 1.4)
    return (G + g) * env, (H + h) * env


def relampago(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        u = rel(t, 0.0 + 0.1 * j, 0.5 + 0.1 * j)
        if 0 < u < 1:
            S = T.polys([(_silhueta(-0.45 + 0.3 * j, 0.05, 1.0), 1.0)])
            G += (S * 0.15 + _borda(T, S, 0.007) * 0.8) * (1 - u)
    k = pulso(t, 0.0, 0.9)
    q = np.random.default_rng(int(t * 40) % 7 + 1)
    for _ in range(5):
        a1, a2 = q.uniform(0, TAU), q.uniform(0, TAU)
        bolt = jagged(q, 0.15 + 0.2 * math.cos(a1), 0.05 + 0.32 * math.sin(a1), 0.15 + 0.2 * math.cos(a2), 0.05 + 0.32 * math.sin(a2), 4, 0.35)
        G += T.polyline(bolt, 0.016) * k * 1.4
        H += T.polyline(bolt, 0.005) * k
    G += raios(T, t, 0.2, 0.9, 4, 9, 0.15, 0.05, 0.6)
    g, h = aura(T, t, 0.0, 0.9, 0.3, 0.05)
    return (G + g) * env, (H + h) * env


def _naipe(j, cx, cy, s):
    if j == 0:
        return poe(CORACAO, cx, cy, s)
    if j == 1:
        return poe(DIAMANTE, cx, cy, s)
    if j == 2:
        return poe(CORACAO, cx, cy, s, math.pi)
    return poe(estrela_pts(3, 0.6), cx, cy, s, -math.pi / 2)


def bungee_gum(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    estica = ease_out(rel(t, 0.1, 0.5), 2)
    k = 1 - rel(t, 0.85, 1)
    if estica > 0:
        for j in range(3):
            ponta = (-0.6 + 1.2 * estica, -0.2 + 0.15 * j)
            balanco = 0.16 * math.sin(t * 14 + j) * (0.4 + 0.6 * (1 - estica))
            pts = [(-0.6 + (ponta[0] + 0.6) * v, -0.2 + 0.15 * j + (ponta[1] - (-0.2 + 0.15 * j)) * v + balanco * math.sin(math.pi * v)) for v in np.linspace(0, 1, 20)]
            G += T.polyline(pts, 0.022) * k * 1.2
            H += T.gauss(ponta[0], ponta[1], 0.03) * k
    for j in range(4):
        kk = surge(t, 0.35 + 0.06 * j, 0.55 + 0.06 * j) * k
        if kk > 0:
            g, h = cheio(T, _naipe(j, -0.36 + 0.24 * j, -0.5, 0.11 * kk), 1.4)
            G, H = G + g, H + h * 2
    return G * env, H * env


def juramento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(5):
        a = TAU * j / 5 + t * 5
        r = 0.55 * ease_out(rel(t, 0.0, 0.35), 2)
        elos = [(r * v * math.cos(a + 0.6 * v), -0.05 + r * v * math.sin(a + 0.6 * v) * 0.7) for v in np.linspace(0.15, 1, 9)]
        for i, (x, y) in enumerate(elos):
            G += T.ring(0.022, 0.007, x, y, 1.5 if i % 2 else 0.7) * k
        x, y = elos[-1]
        forma = [poe(ESPADA, x, y, 0.06, a + math.pi / 2), poe(circulo(10, 1.0), x, y, 0.035),
                 poe([(0, -1), (0.3, 0), (0, 1), (-0.3, 0)], x, y, 0.06, a), poe([(-0.2, -1), (0.2, -1), (0.2, -0.2), (1, -0.2), (1, 0.2), (0.2, 0.2), (0.2, 1), (-0.2, 1), (-0.2, 0.2), (-1, 0.2), (-1, -0.2), (-0.2, -0.2)], x, y, 0.05, a),
                 poe([(0, -1), (0.6, 0.6), (-0.6, 0.6)], x, y, 0.05, a + math.pi / 2)][j]
        g, h = cheio(T, forma, k * 1.2)
        G, H = G + g, H + h
    olhos = pulso(t, 0.35, 1.0)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.07, -0.4, 0.025, 0.015) * olhos * 2.5
        G += T.gauss(lado * 0.07, -0.4, 0.07, 0.04) * olhos * 1.2
    return G * env, H * env


def transmutacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = clarao(T, t, 0.0, 0.15, 0, -0.1, 0.5)
    G, H = G + g, H + h
    q = np.random.default_rng(int(t * 30) % 5 + 3)
    k = pulso(t, 0.05, 0.6)
    if k > 0:
        for lado in (-1, 1):
            bolt = jagged(q, 0, 0.38, lado * 0.85 * ease_out(rel(t, 0.05, 0.4)), 0.4, 5, 0.12)
            G += T.polyline(bolt, 0.016) * k * 1.4
            H += T.polyline(bolt, 0.005) * k
    for j in range(5):
        x = -0.6 + 0.3 * j
        sobe = ease_out(rel(t, 0.3 + 0.04 * abs(j - 2), 0.55 + 0.04 * abs(j - 2)), 3) * (1 - rel(t, 0.85, 1))
        if sobe > 0:
            alt = (0.45 - 0.08 * abs(j - 2)) * sobe
            g, h = icone(T, [(x - 0.06, 0.4), (x, 0.4 - alt), (x + 0.06, 0.4)], 1.2, 0.5)
            G, H = G + g, H + h
    return G * env, H * env


def parede(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    sobe = ease_out(rel(t, 0.1, 0.5), 2.5)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0:
        alt = 0.7 * sobe
        topo = 0.4 - alt
        g, h = icone(T, [(-0.45, 0.4), (-0.45, topo), (0.45, topo), (0.45, 0.4)], k * 1.1, 0.3)
        G, H = G + g, H + h
        segs = []
        linhas = int(alt / 0.12)
        for j in range(1, linhas + 1):
            y = 0.4 - 0.12 * j
            segs.append((-0.45, y, 0.45, y, 1.0))
            off = 0.0 if j % 2 else 0.15
            for x in np.arange(-0.45 + off, 0.45, 0.3):
                segs.append((x, y, x, y + 0.12, 1.0))
        if segs:
            G += T.lines(segs, 0.008) * k
    G += particulas(T, t, 0.1, 0.7, 30, 3, 0, 0.4, 0.5, 0.3, 0.02)
    G += onda_no_chao(T, t, 0.1, 0.6, 0.8, 0.42)
    return G * env, H * env


def chamas_roy(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.4))
    if s > 0:
        G += T.ring(0.1 * s, 0.015, -0.6, -0.1) * 1.3 + T.ring(0.06 * s, 0.01, -0.6, -0.1)
        tri = [(-0.6, -0.17), (-0.54, -0.06), (-0.66, -0.06)]
        G += T.polyline(tri + [tri[0]], 0.008) * s
        H += T.gauss(-0.6, -0.1, 0.02) * pulso(t, 0.15, 0.3) * 3
    for j in range(5):
        a0 = 0.25 + 0.07 * j
        x = -0.35 + 0.2 * j
        y = -0.1 + 0.05 * math.sin(j * 1.7)
        g, h = clarao(T, t, a0, a0 + 0.25, x, y, 0.35 + 0.06 * j, 1.0)
        G, H = G + g, H + h
        G += anel(T, t, a0, a0 + 0.35, 0.03, 0.2 + 0.03 * j, 0.03, y) * 0 + T.gauss(x, y, 0.08 + 0.04 * j) * pulso(t, a0, a0 + 0.35) * 0.9
    G += particulas(T, t, 0.3, 1.0, 40, 5, 0.2, -0.1, 0.6, 0.5, 0.016)
    return G * env, H * env


def berserker(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        marca = [(0, 0.1), (0, -0.25 * s - 0.05), (-0.15 * s, -0.42 * s - 0.05)]
        G += T.polyline(marca, 0.03) * 1.4 + T.lines([(0, -0.25 * s - 0.05, 0.15 * s, -0.42 * s - 0.05, 1.0), (-0.1 * s, 0.0, 0.1 * s, 0.0, 1.0)], 0.03) * 1.4
        H += T.polyline(marca, 0.01) * 1.2
    olhos = pulso(t, 0.3, 1.0)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.07, -0.55, 0.035, 0.012) * olhos * 2.5
        G += T.gauss(lado * 0.07, -0.55, 0.08, 0.03) * olhos * 1.2
    sobe = ease_out(rel(t, 0.25, 0.6), 2)
    if sobe > 0:
        g, h = icone(T, poe(estrela_pts(16, 0.6), 0, -0.05, 0.55 * sobe * (1 + 0.04 * math.sin(t * 60))), (1 - rel(t, 0.8, 1)) * 0.8, 0.25)
        G, H = G + g, H + h
    return G * env, H * env


def eclipse(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.45), 2)
    k = 1 - rel(t, 0.85, 1)
    if s > 0:
        r = 0.32 * s
        G += T.ring(r, 0.05, 0, -0.25) * 1.4 * k + T.ring(r * 1.2, 0.03, 0, -0.25) * 0.7 * k
        H += T.ring(r, 0.012, 0, -0.25) * k
        segs = []
        for j in range(24):
            a = TAU * j / 24 + t
            comp = 0.1 + 0.08 * math.sin(j * 2.3 + t * 10)
            segs.append((r * 1.05 * math.cos(a), -0.25 + r * 1.05 * math.sin(a), (r + comp) * math.cos(a), -0.25 + (r + comp) * math.sin(a), 1.0))
        G += T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.025) * k * 0.9
    g, h = chuva(T, t, 0.3, 1.0, PENA, 10, 5, 0.05, -0.4, 0.45, 0.7, 3.0, 0.9)
    return (G + g) * env, (H + h) * env


def za_warudo_jotaro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.45), 2)
    volta = rel(t, 0.7, 0.95)
    r = 1.0 * u * (1 - volta)
    if r > 0.01:
        G += T.ring(r, 0.05, 0, 0) * 1.3 + T.gauss(0, 0, r * 0.7) * 0.35
        H += T.ring(r, 0.015, 0, 0) * 0.9
        segs = []
        for j in range(8):
            a = TAU * j / 8
            segs.append((r * 0.3 * math.cos(a), r * 0.3 * math.sin(a), r * 0.95 * math.cos(a), r * 0.95 * math.sin(a), 1.0))
        G += T.lines(segs, 0.006) * 0.8
    k = pulso(t, 0.2, 0.95)
    if k > 0:
        G += T.ring(0.22, 0.02, 0, 0) * k * 1.2
        para = 1 - rel(t, 0.3, 0.5)
        a = -math.pi / 2 + t * 30 * para + 1.2
        G += T.lines([(0, 0, 0.18 * math.cos(a), 0.18 * math.sin(a), 1.0), (0, 0, 0.1 * math.cos(a * 0.3), 0.1 * math.sin(a * 0.3), 1.0)], 0.02) * k * 1.3
    return G * env, H * env


def road_roller(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(8):
        a = TAU * j / 8 + t * 4
        k = pulso(t, 0.0, 0.6)
        g, h = icone(T, poe([(0, -1), (0.15, -0.3), (0.12, 0.6), (-0.12, 0.6), (-0.15, -0.3)], 0.6 * math.cos(a), 0.2 * math.sin(a) - 0.1, 0.1, a - math.pi / 2), k, 0.5)
        G, H = G + g, H + h
    u = ease_in(rel(t, 0.15, 0.55), 2.2)
    if t < 0.75:
        y = -1.1 + 1.25 * u
        corpo = [(-0.5, y - 0.24), (0.5, y - 0.24), (0.5, y + 0.1), (-0.5, y + 0.1)]
        g, h = icone(T, corpo, (1 - rel(t, 0.6, 0.75)) * 1.2, 0.4)
        G, H = G + g, H + h
        G += T.ring(0.17, 0.05, -0.2, y + 0.24, 1.0) * (1 - rel(t, 0.6, 0.75)) * 1.2
        G += T.polys([([(0.1, y - 0.3), (0.3, y - 0.3), (0.3, y - 0.18), (0.1, y - 0.18)], 1.0)]) * 0.8 * (1 - rel(t, 0.6, 0.75))
    g, h = clarao(T, t, 0.53, 0.75, 0, 0.25, 1.3, 1.8)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.55, 0.95, 0.95, 0.35) + estouro(T, t, 0.55, 0.9, 20, 5, 0, 0.25, 0.8)
    return G * env, H * env


def vida_demais(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(4):
        u = ease_out(rel(t, 0.05 * j, 0.5 + 0.05 * j), 2)
        if u > 0:
            x0 = -0.45 + 0.3 * j
            pts = [(x0 + 0.12 * math.sin(v * 6 + j), 0.4 - 0.6 * v * u) for v in np.linspace(0, 1, 16)]
            G += T.polyline(pts, 0.022) * k
            if u > 0.6:
                g, h = icone(T, poe(FOLHA, pts[-1][0], pts[-1][1], 0.06, 0.5 * j), k, 0.5)
                G, H = G + g, H + h
    for j in range(3):
        s = surge(t, 0.4 + 0.1 * j, 0.6 + 0.1 * j) * k
        if s > 0:
            x, y = -0.3 + 0.3 * j, -0.3 - 0.1 * (j % 2) - 0.2 * rel(t, 0.6, 1.0)
            G += T.gauss(x, y, 0.05 * s) * 1.1 + T.lines([(x, y - 0.05 * s, x, y + 0.05 * s, 1.0)], 0.008) * s
            H += (T.gauss(x - 0.02, y - 0.01, 0.01) + T.gauss(x + 0.02, y + 0.015, 0.01)) * s * 1.5
    for j in range(2):
        u = rel(t, 0.5 + 0.1 * j, 1.0)
        if 0 < u < 1:
            x, y = 0.4 - 0.8 * j + 0.2 * u * (1 if j else -1), -0.1 - 0.5 * u
            bate = abs(math.sin(t * 30 + j))
            for lado in (-1, 1):
                G += T.polys([([(x, y), (x + lado * 0.1 * bate, y - 0.08), (x + lado * 0.08 * bate, y + 0.05)], 1.0)]) * (1 - u) * 1.1
    return G * env, H * env


def vrrrum(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    puxa = ease_out(rel(t, 0.0, 0.2), 2)
    if t < 0.3:
        G += T.lines([(0, 0.05, 0.3 * puxa, 0.05 + 0.25 * puxa, 1.0)], 0.01) * 1.2 + T.ring(0.03, 0.01, 0.3 * puxa, 0.05 + 0.25 * puxa) * 1.2
    for j, (bx, ang) in enumerate(((0, -math.pi / 2), (-0.2, -2.3), (0.2, -0.8))):
        sai = ease_out(rel(t, 0.2 + 0.05 * j, 0.45 + 0.05 * j), 3)
        k = 1 - rel(t, 0.85, 1)
        if sai > 0:
            comp = 0.45 * sai
            x0, y0 = bx, -0.3 if j == 0 else 0.0
            x1, y1 = x0 + comp * math.cos(ang), y0 + comp * math.sin(ang)
            G += T.lines([(x0, y0, x1, y1, 1.0)], 0.05) * k * 0.8
            dentes = []
            for m in range(10):
                v = (m / 10 + t * 6) % 1
                px, py = x0 + (x1 - x0) * v, y0 + (y1 - y0) * v
                nx, ny = -math.sin(ang), math.cos(ang)
                dentes.append((px + nx * 0.03, py + ny * 0.03, px + nx * 0.05 + math.cos(ang) * 0.02, py + ny * 0.05 + math.sin(ang) * 0.02, 1.0))
            G += T.lines(dentes, 0.01) * k * 1.3
    q = np.random.default_rng(3)
    u = rel(t, 0.4, 0.95)
    if 0 < u < 1:
        for j in range(10):
            a = q.uniform(0, TAU)
            d = 0.6 * ease_out(u) * q.uniform(0.5, 1)
            g, h = cheio(T, poe(GOTA, d * math.cos(a), -0.1 + d * math.sin(a) + 0.3 * u * u, 0.035, a + math.pi / 2), 1 - u)
            G, H = G + g, H + h
    return G * env, H * env


def escondida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            chifre = [(lado * 0.08 * s, -0.4), (lado * 0.2 * s, -0.4 - 0.28 * s), (lado * 0.14 * s, -0.4)]
            g, h = cheio(T, chifre, 1.2)
            G, H = G + g, H + h
    u = ease_in(rel(t, 0.25, 0.55), 2)
    k = 1 - rel(t, 0.75, 0.85)
    if u > 0 and k > 0:
        ang = -2.0 + 1.6 * u
        cx, cy = 0.0, 0.3
        hx, hy = cx + 0.6 * math.cos(ang), cy + 0.6 * math.sin(ang)
        G += T.lines([(cx, cy, hx, hy, 1.0)], 0.04) * k
        g, h = icone(T, poe([(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)], hx, hy, 0.18, ang + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.53, 0.72, 0.55, 0.0, 1.0, 1.3)
    G, H = G + g, H + h
    q = np.random.default_rng(9)
    v = rel(t, 0.55, 1.0)
    if 0 < v < 1:
        for j in range(10):
            a = q.uniform(0, TAU)
            d = 0.5 * ease_out(v)
            g2, h2 = cheio(T, poe(GOTA, 0.55 + d * math.cos(a), d * math.sin(a) + 0.3 * v * v, 0.04, a + math.pi / 2), 1 - v)
            G, H = G + g2, H + h2
    return G * env, H * env


def agora_e_meu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    for lado in (-1, 1):
        for r in (0.02, 0.045, 0.07):
            G += T.ring(r * 1.8 * s + 0.001, 0.011, lado * 0.2, -0.4) * s * 1.4
    u = ease_out(rel(t, 0.3, 0.65), 2)
    k = 1 - rel(t, 0.85, 1)
    if u > 0:
        x1 = -0.5 + 1.2 * u
        elos = [(-0.5 + (x1 + 0.5) * v, 0.0 + 0.05 * math.sin(v * 12)) for v in np.linspace(0, 1, int(4 + 14 * u))]
        for i, (x, y) in enumerate(elos):
            G += T.ring(0.025, 0.008, x, y, 1.6 if i % 2 else 0.6) * k
        G += T.ring(0.09, 0.025, x1, 0.0) * k * 1.2 * (u > 0.95)
    return G * env, H * env


def disable(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        G += anel(T, t, 0.0 + 0.1 * j, 0.5 + 0.1 * j, 0.7, 0.18, 0.03, 0.0)
    trava = ease_out(rel(t, 0.4, 0.6), 3) * (1 - rel(t, 0.85, 1))
    if trava > 0:
        G += T.ring(0.25, 0.025, 0, 0) * trava * 1.3
        for a in (math.pi / 4, -math.pi / 4):
            G += T.lines([(-0.22 * math.cos(a) * trava, -0.22 * math.sin(a) * trava, 0.22 * math.cos(a) * trava, 0.22 * math.sin(a) * trava, 1.0)], 0.04) * 1.3
        H += T.gauss(0, 0, 0.05) * trava
    g, h = aura(T, t, 0.0, 0.9, 0.35)
    return (G + g) * env, (H + h) * env


def penhasco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.4, 0.5)
    if k > 0:
        u = ease_in(rel(t, 0.0, 0.25), 2)
        P, nos = _punho(T, -0.4 + 0.3 * u, 0.15 - 0.2 * u, 1.4, -0.6)
        G += P * 0.9 * k
        H += nos * 0.5 * k
        G += raios(T, t, 0.0, 0.4, 3, 5, -0.15, -0.05, 0.3)
    g, h = clarao(T, t, 0.22, 0.42, -0.1, -0.05, 0.9, 1.3)
    G, H = G + g, H + h
    v = ease_out(rel(t, 0.3, 0.85), 1.6)
    if 0 < v < 1:
        y = -0.05 - 1.0 * v
        G += T.gauss(0.1, y, 0.06) * 1.2 + T.tapered([(0.05, 0.2, 0.1, y, 1.0)], 0.07) * 0.8
    return G * env, H * env


def rainha_vampira(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            presa = [(lado * 0.11 * s - 0.06 * s, -0.35), (lado * 0.11 * s + 0.06 * s, -0.35), (lado * 0.11 * s, -0.35 + 0.27 * s)]
            g, h = cheio(T, presa, 1.4)
            G, H = G + g, H + h * 1.5
        G += T.arc_band(0.26 * s, 0.022, 0.2, math.pi - 0.2, 1.0, 0.0, 0, -0.48, 0.0) * 1.2
    q = np.random.default_rng(13)
    u = rel(t, 0.15, 0.85)
    if 0 < u < 1:
        for j in range(6):
            y0 = q.uniform(-0.1, 0.4)
            fase = (u * 1.5 + j / 6) % 1
            pts = [(0.8 - (0.8 - 0.0) * min(1, fase + 0.1 * v), y0 + (-0.32 - y0) * min(1, fase + 0.1 * v) + 0.06 * math.sin(v * 6 + j)) for v in np.linspace(0, 1, 8)]
            G += T.polyline(pts, 0.018) * (1 - rel(u, 0.85, 1)) * 1.1
    G += T.gauss(0.8, 0.15, 0.15) * pulso(t, 0.1, 0.8) * 0.8
    return G * env, H * env


REGISTRO = [
    ("mu_tempestade", tempestade, GRANDE, "Thor · o Mjolnir e os raios do céu", False),
    ("mu_hollow", hollow, GRANDE, "Ichigo · a máscara Hollow", False),
    ("mu_danca_branca", danca_branca, GRANDE, "Rukia · o círculo e o pilar de gelo", False),
    ("mu_ilusao_aizen", ilusao_aizen, GRANDE, "Aizen · o espelho rachando", False),
    ("mu_tapa_olho", tapa_olho, GRANDE, "Kenpachi · o tapa-olho e a pressão espiritual", False),
    ("mu_endurecer", endurecer, GRANDE, "Eren · as placas de cristal", False),
    ("mu_pedra_papel", pedra_papel, GRANDE, "Gon · o Jajanken", False),
    ("mu_relampago", relampago, GRANDE, "Killua · o Godspeed", False),
    ("mu_bungee_gum", bungee_gum, GRANDE, "Hisoka · a Bungee Gum e os naipes", False),
    ("mu_juramento", juramento, GRANDE, "Kurapika · as correntes e os olhos escarlates", False),
    ("mu_transmutacao", transmutacao, GRANDE, "Edward · a transmutação e as lanças de pedra", False),
    ("mu_parede", parede, GRANDE, "Alphonse · o muro de pedra", False),
    ("mu_chamas_roy", chamas_roy, GRANDE, "Roy · o estalo e as explosões", False),
    ("mu_berserker", berserker, GRANDE, "Guts · a Marca e a Armadura do Berserker", False),
    ("mu_eclipse", eclipse, GRANDE, "Griffith · o Eclipse", False),
    ("mu_za_warudo_jotaro", za_warudo_jotaro, GRANDE, "Jotaro · o tempo parado", False),
    ("mu_road_roller", road_roller, GRANDE, "Dio · o Road Roller", False),
    ("mu_vida_demais", vida_demais, GRANDE, "Giorno · a vida brotando", False),
    ("mu_vrrrum", vrrrum, GRANDE, "Denji · as motosserras", False),
    ("mu_escondida", escondida, GRANDE, "Power · os chifres e o martelo de sangue", False),
    ("mu_agora_e_meu", agora_e_meu, GRANDE, "Makima · os olhos de anéis e a corrente", False),
    ("mu_disable", disable, GRANDE, "Mewtwo · o Disable", False),
    ("mu_penhasco", penhasco, GRANDE, "Heihachi · o punho que joga do penhasco", False),
    ("mu_rainha_vampira", rainha_vampira, GRANDE, "Marceline · as presas e o vermelho sugado", False),
]
